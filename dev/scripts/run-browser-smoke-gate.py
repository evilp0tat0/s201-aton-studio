#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Playwright headless smoke gate runner.
#
# WHY THIS EXISTS
# ---------------
# The in-app smoke invariants in `s201_aton_studio.html` (`runSmokeTests`;
# current count: `_COUNT_GROUND_TRUTH["smoke"]` in precommit-check.py — single
# source per Rule 23) only fully run in a real browser — they exercise
# DOMParser, fetch(), round-trip parser/generator on bundled exGML samples,
# validateGMLStructure, downloadCatalogXML, etc. Pre-commit's V8 syntax check
# (check #6) catches structural JS errors but cannot run the smoke tests
# because they need a DOM.
#
# Driving the suite through an embedded preview browser proved unreliable, so
# this runner makes the smoke gate automatable: any contributor can run
# `python dev/scripts/run-browser-smoke-gate.py` and get a full-suite PASS
# verdict — same engine the user runs, no iframe weirdness. It owns the HTTP
# server it tests against and proves (SHA-256) that the served app is this
# worktree's file before trusting a verdict.
#
# THREE-LAYER GATE STACK (Rule 11 + Rule 13)
# ------------------------------------------
#   1. precommit-check.py        — fast static (a few seconds, 19 checks, every commit)
#   2. run-browser-smoke-gate.py — slow runtime (full smoke suite, then the mount oracle,
#                                  before push/release; can be wired into CI)
#   3. Manual [Run tests]        — final visual confirmation in any real
#                                  browser tab the user trusts
#
# USAGE
# -----
#   python dev/scripts/run-browser-smoke-gate.py            # default, exit 1 on fail
#   python dev/scripts/run-browser-smoke-gate.py --json     # machine-readable output
#   python dev/scripts/run-browser-smoke-gate.py --port 8090   # pin a port (default: OS-assigned)
#   python dev/scripts/run-browser-smoke-gate.py --verbose  # print every test
#   python dev/scripts/run-browser-smoke-gate.py --browser firefox   # second engine: the Firefox already
#                                    # installed, driven over Playwright's moz-firefox (WebDriver BiDi) channel
#   python dev/scripts/run-browser-smoke-gate.py --browser firefox --firefox-exe "C:\path\to\firefox.exe"
#
# The default engine is Chromium and its verdict is the definition of done (HANDOFF "What ships
# together"). The Firefox leg exists because a fault can be engine-specific and invisible here:
# Gecko's XML serializer writes a line break after every document-level node, and the quick fixes
# escaped it into the prolog, so every quick fix in Firefox produced an ill-formed document from
# 1.22.1 to 1.26.2 while this gate stayed green. Run the second engine before a release, and
# whenever a change touches the DOM/XML serializer, DOMParser output, or anything the browser
# words (error messages, computed styles).
#
# EXIT CODES
# ----------
#   0 all tests passed   1 a test failed, or the suite size deviates from ground truth
#   2 playwright not installed, or the requested engine cannot launch (--browser firefox: no
#     Firefox found at --firefox-exe / $FIREFOX_BIN / the standard install paths, or a Playwright
#     without the moz-firefox channel)   3 Playwright error / suite did not settle within 180s
#   4 could not own the port, or the served app is not this worktree's file
#   5 source-comment probe polarity mismatch (wrong build for this harness)
#   6 an uncaught page exception occurred during the run
#   7 console output deviates from the expected baseline (unlisted message, or more of a
#     listed one than it allows — see _CONSOLE_BASELINE)
#   8 the mount oracle failed: for some fixture, the GML the Builder writes after opening every
#     feature differs from the GML of the import candidate the import report measured, opening
#     a feature changed its own GML (the per-mount sentinel), or a fixture could not be run —
#     see MOUNT_ORACLE_JS
#
# DEPENDENCIES (one-time setup)
# -----------------------------
#   pip install playwright
#   playwright install chromium
#   --browser firefox downloads nothing: it drives the Firefox already installed on the machine
#   (--firefox-exe, then $FIREFOX_BIN, then the standard install paths) through Playwright's
#   moz-firefox channel (WebDriver BiDi; Playwright 1.62 verified). No Playwright Firefox build needed.
#
# Per Rule 17 (Layered validation hierarchy) the gate stack mirrors the
# validator's own layered design — each tier catches what the others can't.
# ---------------------------------------------------------------------------

import argparse
import asyncio
import hashlib
import http.server
import json
import os
import re
import socket
import socketserver
import sys
import threading
import time
import urllib.request

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# --browser firefox: where an installed Firefox is looked for when --firefox-exe and $FIREFOX_BIN
# are not given. Playwright's own moz-firefox discovery covers the Windows Program Files and macOS
# app-bundle paths but not a Linux distro package at /usr/bin/firefox, so the list is consulted
# first and the driver's discovery is the fallback (None → launch with no executable_path).
FIREFOX_CANDIDATES = (
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
    "/usr/bin/firefox",
    "/Applications/Firefox.app/Contents/MacOS/firefox",
)


def _find_firefox(explicit: str | None) -> str | None:
    """The Firefox executable to drive: the flag, then $FIREFOX_BIN, then the standard paths; None
    when none exists on disk (the driver then tries its own discovery, and a miss is exit 2)."""
    for c in (explicit, os.environ.get("FIREFOX_BIN"), *FIREFOX_CANDIDATES):
        if c and os.path.isfile(c):
            return c
    return None


# The engine that produced the verdict, named in the report header so a log reader can tell a
# Chromium run from a Firefox run. Set once per run right after the browser launches.
_ENGINE_LABEL = "chromium"


def _start_http_server(port: int, serve_root: str = REPO_ROOT):
    """Start a Python http.server in a background thread bound to serve_root (default REPO_ROOT).

    Returns (server, actual_port). `port=0` asks the OS for a free ephemeral port,
    which is the default and the only contention-free option: with a fixed port,
    a server left running by another worktree already owns it, and the two
    platforms then diverge in dangerous ways.
      * POSIX: our bind() fails, and the gate used to shrug ("assuming external
        server") and validate whatever answered.
      * Windows: our bind() SUCCEEDS anyway (SO_REUSEADDR permits a second
        listener on the same address), leaving TWO servers racing to accept —
        so an identity probe and the browser can be answered by different
        processes serving different code. Verified empirically 2026-07-08.
    Owning the only listener removes the race outright; the SHA-256 identity
    check below then backstops the explicit `--port` escape hatch.

    `allow_reuse_address` must be set BEFORE the bind to have any effect — it is
    a class attribute consulted inside TCPServer.__init__ (server_bind). Setting
    it on the instance after construction, as this function used to, was a no-op.
    """
    handler_cls = http.server.SimpleHTTPRequestHandler

    class _QuietHandler(handler_cls):
        def log_message(self, fmt, *args):  # silence per-request logs
            pass

    class _Server(socketserver.TCPServer):
        allow_reuse_address = False  # never silently hijack a port someone else owns

        def server_bind(self):
            # Windows permits a SECOND bind to an address whose current owner set
            # SO_REUSEADDR (which `python -m http.server` does), and then routes new
            # connections to the most recent binder. Two live listeners means an
            # identity probe and the browser can be answered by different processes.
            # SO_EXCLUSIVEADDRUSE restores the POSIX-ish contract: if someone else
            # owns this port, our bind fails and the caller aborts.
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            super().server_bind()

    os.chdir(serve_root)
    server = _Server(("127.0.0.1", port), _QuietHandler)
    actual_port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    # Brief settle time so the bind completes before Playwright connects
    time.sleep(0.3)
    return server, actual_port


# Seeds a distinctive NON-DEFAULT workspace before the suite runs, so the suite's final
# "Suite containment (state)" lock can detect any test that mutates user state without a
# full restore. Module-level so the end-user-bundle verify (build-end-user-version.py)
# reuses the exact same seed instead of a drifting copy.
#
# The mounted sentinel beacon carries ONE CHILD OF EVERY COMPONENT FAMILY the generator's
# shorthand synthesizer consults before reconstructing a referenced child (its has(type)
# guard: Topmark, LightAllAround / LightSectored, FogSignal, RadarTransponderBeacon,
# RadarReflector — grep `const has=` in _synthesizeShorthandComponents). generateGML reads
# the global compStack as the emitted feature's own components, so a suite lock that emits a
# parsed fixture WITHOUT isolating that stack reports the mounted children instead of the
# fixture's — exactly what a user with a real dataset loaded sees ("4 of N FAILED" on the
# round-trip reconstruct locks), and what a Topmark-only sentinel could never show. With
# every family mounted, any such bare emit goes red here. SEED_FAMILIES below is asserted
# on the live stack after seeding, so the seed cannot silently lose a family (e.g. if the
# import fold stopped folding one of them).
SEED_FAMILIES = ("Topmark", "LightAllAround", "FogSignal", "RadarTransponderBeacon", "RadarReflector")
SENTINEL_SEED_JS = """(() => {
  const pt = '<geometry><S100:pointProperty><S100:Point gml:id="P.SEN.001" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>1.1000000 2.2000000</gml:pos></S100:Point></S100:pointProperty></geometry>';
  const sentinel = '<?xml version="1.0" encoding="UTF-8"?>\\n<Dataset xmlns="http://www.iho.int/S-201/gml/cs0/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:S100="http://www.iho.int/s100gml/5.0" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="DS.SEN">\\n<members>\\n<LateralBeacon gml:id="SEN.001"><featureName><name>Sentinel Alfa</name></featureName><AtoNNumber>0900</AtoNNumber><child xlink:href="#SEN.002"/><child xlink:href="#SEN.003"/><child xlink:href="#SEN.004"/><child xlink:href="#SEN.005"/><child xlink:href="#SEN.006"/><colour>Red</colour><beaconShape>Pile Beacon</beaconShape><categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark>' + pt + '</LateralBeacon>\\n<Topmark gml:id="SEN.002"><parent xlink:href="#SEN.001"/><colour>Red</colour><topmarkDaymarkShape>Cylinder</topmarkDaymarkShape><verticalLength>0.6</verticalLength>' + pt.replace(/SEN\\.001/g, 'SEN.002') + '</Topmark>\\n<LightAllAround gml:id="SEN.003"><parent xlink:href="#SEN.001"/><colour>Green</colour><rhythmOfLight><lightCharacteristic>Morse</lightCharacteristic><signalGroup>A</signalGroup></rhythmOfLight><signalPeriod>8</signalPeriod>' + pt.replace(/SEN\\.001/g, 'SEN.003') + '</LightAllAround>\\n<FogSignal gml:id="SEN.004"><parent xlink:href="#SEN.001"/><categoryOfFogSignal>Horn</categoryOfFogSignal><signalPeriod>30</signalPeriod><status>Permanent</status>' + pt.replace(/SEN\\.001/g, 'SEN.004') + '</FogSignal>\\n<RadarTransponderBeacon gml:id="SEN.005"><parent xlink:href="#SEN.001"/><categoryOfRadarTransponderBeacon>Racon, Radar Transponder Beacon</categoryOfRadarTransponderBeacon><signalGroup>(B)</signalGroup>' + pt.replace(/SEN\\.001/g, 'SEN.005') + '</RadarTransponderBeacon>\\n<RadarReflector gml:id="SEN.006"><parent xlink:href="#SEN.001"/><height>3</height>' + pt.replace(/SEN\\.001/g, 'SEN.006') + '</RadarReflector>\\n</members></Dataset>';
  const gi = document.getElementById('gmlIn');
  gi.value = sentinel;
  const oc = window.confirm, oa = window.alert;
  try {
    window.confirm = () => true; window.alert = () => {};
    builderImportFromDrawing();
  } finally { window.confirm = oc; window.alert = oa; }
  // Force the colour-surface MISMATCH: the import mounts a feature and _swapBuilderToFeat sets
  // _colourUserSet=true; a user sitting on an auto-prefilled coloured mark is instead at
  // _colourUserSet=false with a coloured feature. Seeding false makes the containment lock exercise the
  // swap's flag write, so a leaking teardown (or a broken _restoreColourSurface) goes red instead of
  // hiding behind the matched start.
  _colourUserSet = false;
  document.getElementById('valIn').value = sentinel;
  // Leave `_colourUserSet` at its LEAK-REVEALING value. The import above sets it true (every mount
  // does), and the containment lock compares end-of-run against start-of-run — so a start of `true`
  // can never observe a false->true leak. That is exactly what hid the leak this seed was written to
  // catch: a pristine page starts false, the restorative `_swapBuilderToFeat` in each test's finally
  // sets it to true,
  // and the gate saw nothing while a real user clicking "Run tests" got a red containment banner.
  // The seeded FEATURE state (the reason this sentinel exists) is untouched by this reset.
  _colourUserSet = false;
})()"""


# The mount oracle, run after the suite. The import report (_importFidelityReport) compares a file with the GML of the
# import candidate; the user then works in the Builder, whose output is what the Builder writes after it has opened
# the features. The two must be the same document, or the report describes a file the user never gets: opening a
# feature must change nothing in it (control custody, _bldKeep). The suite's locks hold that for chosen cases; the
# oracle holds it for every feature of every fixture, through the real import path (_importGMLTextToBuilder, whose
# report call is wrapped only to read the candidate it measured) and the real pill path (builderSelectFeat), opening
# every feature in document order and then again in the other order (the output must not depend on it). It also
# reads the per-mount sentinel's log (_bldSentinelLog), which names a feature whose own GML changed when it was opened.
# The fixtures are fc_kitchen.fixtures() (every FC type with every bound attribute, in five lexical forms, plus the
# edge, legacy-inline and colour-less-rhythm cases), the four bundled examples (exGML) and dev/sample-data/*.gml*.
# A sample file that is not well-formed XML is refused by the import and reported as not run; a generated fixture or a
# bundled example the import refuses, for any reason, fails.
MOUNT_ORACLE_TIMEOUT_S = 240
MOUNT_ORACLE_JS = r"""async (fixtures) => {
  const GMLNS = "http://www.opengis.net/gml/3.2";
  const out = { fixtures: [], warns: 0 };
  const members = xml => {
    const d = new DOMParser().parseFromString(xml, "application/xml");
    if (d.getElementsByTagName("parsererror").length) return null;
    const m = new Map(), hdr = [];
    for (const c of Array.from(d.documentElement.children)) {
      if (c.localName === "members" || c.localName === "imember") {
        const list = c.localName === "members" ? Array.from(c.children) : [c.firstElementChild].filter(Boolean);
        list.forEach((e, i) => m.set(e.getAttributeNS(GMLNS, "id") || ("(no id #" + i + ")"), e));
      } else hdr.push(c);
    }
    return { m, hdr };
  };
  const leaves = el => { const L = []; const walk = (e, p) => { const kids = Array.from(e.children);
      const at = Array.from(e.attributes).filter(a => !(a.localName === "id" && a.namespaceURI === GMLNS)).map(a => a.name + "=" + a.value).join(",");
      if (!kids.length) { L.push(p + "=" + (e.textContent || "").trim() + (at ? " [" + at + "]" : "")); return; }
      kids.forEach(c => walk(c, p + "/" + c.localName)); };
    walk(el, el.localName); return L; };
  const msDiff = (a, b) => { const n = new Map(); a.forEach(x => n.set(x, (n.get(x) || 0) + 1)); b.forEach(x => n.set(x, (n.get(x) || 0) - 1));
    const lost = [], gained = []; for (const [x, k] of n) { for (let i = 0; i < k; i++) lost.push(x); for (let i = 0; i < -k; i++) gained.push(x); } return { lost, gained }; };
  const diffDocs = (A, B) => {
    const a = members(A), b = members(B);
    if (!a || !b) return { fatal: (!a ? "the candidate's GML" : "the Builder's GML") + " is not well-formed" };
    const r = { members: [], onlyCandidate: [], onlyBuilder: [], header: null };
    for (const [id, e] of a.m) { const f = b.m.get(id); if (!f) { r.onlyCandidate.push(id + " (" + e.localName + ")"); continue; }
      if (e.outerHTML !== f.outerHTML) { const d = msDiff(leaves(e), leaves(f)); r.members.push({ id, ft: e.localName, lost: d.lost.slice(0, 4), gained: d.gained.slice(0, 4), orderOnly: !d.lost.length && !d.gained.length }); } }
    for (const [id, f] of b.m) if (!a.m.has(id)) r.onlyBuilder.push(id + " (" + f.localName + ")");
    const hd = msDiff(a.hdr.map(leaves).flat(), b.hdr.map(leaves).flat());
    if (hd.lost.length || hd.gained.length) r.header = { lost: hd.lost.slice(0, 4), gained: hd.gained.slice(0, 4) };
    r.nMembers = r.members.length; r.members = r.members.slice(0, 5);
    return r;
  };
  const all = fixtures.concat(exGML.map((t, i) => ({ name: "exGML[" + i + "]", text: t, must: true })));
  const oc = window.confirm, oa = window.alert, ow = console.warn, oF = _importFidelityReport;
  let alerts = [], cap = null;
  window.confirm = () => true;
  window.alert = m => { alerts.push(String(m)); };
  console.warn = () => { out.warns++; };
  _importFidelityReport = function (txt, loadable, cand) {
    const rep = oF.apply(this, arguments);
    try { cap = { text: String(generateAllGML(cand)) }; } catch (e) { cap = { error: String((e && e.message) || e) }; }
    return rep;
  };
  try {
    for (const fx of all) {
      const r = { name: fx.name };
      alerts = []; cap = null;
      try {
        const s0 = _bldSentinelLog.length, t0 = performance.now();
        const ok = _importGMLTextToBuilder(fx.text, { fixWhere: "in the fixture", cancelHint: "", keepNote: "", receiptTail: "", heldWhere: "the fixture" });
        if (!ok) {
          const a = alerts[0] || "no message";
          if (/not well-formed/.test(a) && !fx.must) r.notRun = "the import refuses it: not well-formed XML";
          else r.error = "the import refused it: " + a.slice(0, 200);
          out.fixtures.push(r); continue;
        }
        if (!cap || cap.error) { r.error = "the import candidate could not be read" + (cap ? ": " + cap.error : " (the report was not made)"); out.fixtures.push(r); continue; }
        for (let i = 1; i < builderFeats.length; i++) builderSelectFeat(i);
        builderUp();
        const mounted = String(generateAllGML(builderFeats));
        r.features = builderFeats.length;
        r.ms = Math.round(performance.now() - t0);
        r.same = mounted === cap.text;
        if (!r.same) r.diff = diffDocs(cap.text, mounted);
        /* and again in the other order: what the Builder writes does not depend on the order the features are opened in */
        if (r.same && builderFeats.length > 1) {
          for (let i = builderFeats.length - 2; i >= 0; i--) builderSelectFeat(i);
          builderUp();
          const again = String(generateAllGML(builderFeats));
          if (again !== cap.text) { r.same = false; r.reversed = true; r.diff = diffDocs(cap.text, again); }
        }
        const sent = _bldSentinelLog.slice(s0);
        if (sent.length) r.sentinel = { n: sent.length, first: sent.slice(0, 3) };
      } catch (e) { r.error = String((e && e.stack) || e).slice(0, 600); }
      out.fixtures.push(r);
    }
  } finally {
    window.confirm = oc; window.alert = oa; console.warn = ow; _importFidelityReport = oF;
  }
  return out;
}"""


def _oracle_fixtures() -> tuple[list[dict], list[str]]:
    """The mount oracle's fixtures (the page adds exGML) and the notes on what could not be included.

    The FC kitchen needs the FC XML, which the public snapshot does not ship (dev/spec-sources holds only its
    MANIFEST.md there): without it the kitchen is left out and a note says so; the other fixtures still run."""
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    try:
        import fc_kitchen
    finally:
        sys.path.pop(0)
    notes: list[str] = []
    fx: list[dict] = []
    if os.path.exists(fc_kitchen.FC_XML):
        fx += [{"name": n, "text": t, "must": True} for n, t in fc_kitchen.fixtures()]
    else:
        notes.append("the FC kitchen fixtures were not built: the FC XML is not in this tree (" + os.path.relpath(fc_kitchen.FC_XML, REPO_ROOT) + ")")
        fx += [{"name": n, "text": f(), "must": True} for n, f in fc_kitchen.EDGE_FIXTURES]
    sd = os.path.join(REPO_ROOT, "dev", "sample-data")
    for fn in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
        if fn.endswith(".gml") or fn.endswith(".gml.xml"):
            with open(os.path.join(sd, fn), encoding="utf-8") as f:
                fx.append({"name": "dev/sample-data/" + fn, "text": f.read(), "must": False})
    return fx, notes


def _report_oracle(oracle: dict, notes: list[str]) -> bool:
    """Print the oracle's outcome (stderr, so --json stdout stays JSON); True when it passed."""
    fx = oracle.get("fixtures") or []
    bad = [r for r in fx if r.get("error") or r.get("same") is False or r.get("sentinel")]
    run = [r for r in fx if "same" in r]
    for n in notes:
        print(f"[note] mount oracle: {n}", file=sys.stderr)
    for r in fx:
        if r.get("notRun"):
            print(f"[note] mount oracle: {r['name']} not run — {r['notRun']}", file=sys.stderr)
    for r in bad:
        print(f"[X] mount oracle: {r['name']}" + (" (after opening the features again, in the other order)" if r.get("reversed") else ""), file=sys.stderr)
        if r.get("error"):
            print(f"    {r['error']}", file=sys.stderr)
        d = r.get("diff") or {}
        if d.get("fatal"):
            print(f"    {d['fatal']}", file=sys.stderr)
        for m in d.get("members", []):
            what = "the order of its elements" if m.get("orderOnly") else (
                ("lost " + " | ".join(m["lost"]) if m["lost"] else "") + ("; " if m["lost"] and m["gained"] else "")
                + ("gained " + " | ".join(m["gained"]) if m["gained"] else ""))
            print(f"    {m['id']} ({m['ft']}): {what}", file=sys.stderr)
        if d.get("nMembers", 0) > len(d.get("members", [])):
            print(f"    … and {d['nMembers'] - len(d['members'])} more feature(s) that differ", file=sys.stderr)
        for k, label in (("onlyCandidate", "only in the candidate"), ("onlyBuilder", "only in the Builder's output")):
            if d.get(k):
                print(f"    {label}: {', '.join(d[k][:6])}", file=sys.stderr)
        if d.get("header"):
            print(f"    dataset header: lost {d['header']['lost']} gained {d['header']['gained']}", file=sys.stderr)
        s = r.get("sentinel")
        if s:
            print(f"    opening a feature changed its own GML {s['n']} time(s); first: {json.dumps(s['first'])[:400]}", file=sys.stderr)
    if bad:
        print(f"[X] mount oracle: {len(bad)} of {len(fx)} fixture(s) failed — the Builder does not write what the import "
              "report measured.", file=sys.stderr)
        return False
    feats = sum(r.get("features", 0) for r in run)
    print(f"[OK] mount oracle: {len(run)} fixture(s), {feats} feature(s) opened — the Builder writes the import "
          "candidate's GML, and no opening changed a feature.", file=sys.stderr)
    return True


async def _run_gate(port: int, verbose: bool, expect_src_comments: bool = True,
                    browser: str = "chromium", firefox_exe: str | None = None) -> tuple[int, list[dict]]:
    """Launch the requested engine headless (Chromium, the default and the definition of done; or
    an installed Firefox over Playwright's moz-firefox BiDi channel), navigate to the app, await
    runSmokeTests, return (exit_code, test_results).

    expect_src_comments pins the _SRC_COMMENTS_KEPT probe's polarity: the dev file keeps its
    comments (True); the comment-stripped end-user bundle must report False, proving every
    comment-anchored source lint ran in its explicit-skip mode rather than false-failing.
    A mismatch means this harness is pointed at the wrong kind of build."""
    global _ENGINE_LABEL
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print(
            "[FAIL] playwright not installed. Run:\n"
            "  pip install playwright\n"
            + ("  playwright install chromium" if browser == "chromium"
               else "  (--browser firefox needs no browser download: install Firefox, or pass --firefox-exe)"),
            file=sys.stderr,
        )
        return 2, []

    url = f"http://127.0.0.1:{port}/s201_aton_studio.html"
    async with async_playwright() as p:
        # The launch is inside its own guard: an engine that cannot start is an operator matter
        # (exit 2, like a missing Playwright), not a traceback.
        try:
            if browser == "firefox":
                exe = _find_firefox(firefox_exe)
                launched = await p.firefox.launch(
                    headless=True, channel="moz-firefox", **({"executable_path": exe} if exe else {})
                )
                _ENGINE_LABEL = f"firefox {launched.version} via moz-firefox ({exe or 'driver discovery'})"
            else:
                launched = await p.chromium.launch(headless=True)
                _ENGINE_LABEL = f"chromium {launched.version}"
        except Exception as e:
            first = (str(e).splitlines() or [type(e).__name__])[0]
            print(
                f"[FAIL] browser engine '{browser}' could not launch: {first}\n"
                "  --browser firefox: pass --firefox-exe, set FIREFOX_BIN, or install Firefox at a "
                "standard path; the moz-firefox channel needs Playwright 1.5x or later.",
                file=sys.stderr,
            )
            return 2, []
        print(f"[note] engine: {_ENGINE_LABEL}", file=sys.stderr)
        browser_obj = launched
        context = await browser_obj.new_context()
        page = await context.new_page()

        # Capture console errors so JS issues bubble up to the gate output.
        # Errors are surfaced even when smoke tests pass (might indicate
        # benign deprecation warnings vs real problems).
        #
        # Records are STRUCTURED, not pre-formatted strings: the reporter below groups
        # identical messages and prints a count, which needs the parts separable. It also
        # keeps msg.location — for the resource-failure class that floods this gate, the
        # URL is the whole diagnostic ("which asset?"), and the text alone never says.
        console_errors: list[dict] = []

        def _on_console(msg):
            if msg.type not in ("error", "warning"):
                return
            loc = ""
            try:
                l = msg.location or {}
                if l.get("url"):
                    loc = l["url"]
                    if l.get("lineNumber"):
                        loc += f":{l['lineNumber']}"
            except Exception:
                pass
            console_errors.append(
                {"kind": "console", "type": msg.type, "text": msg.text, "location": loc, "stack": ""}
            )

        def _on_pageerror(exc):
            # The ONLY class that blocks the gate (exit 6), so it is stored with the most
            # diagnostic content available. f"{exc}" alone yields just the message, dropping
            # the class name and the whole JS stack — on a headless run the operator cannot
            # reproduce, that stack is the only pointer to the failing line. `.name` may be
            # present-but-EMPTY for a non-Error throw, so the fallback tests truthiness, not
            # attribute presence.
            name = (getattr(exc, "name", "") or "").strip() or "Error"
            message = getattr(exc, "message", None) or str(exc)
            stack = (getattr(exc, "stack", "") or "").strip()
            # Gecko hands the BiDi bridge its error-console CATEGORIES as page errors too: the XML
            # parsing error an app DOMParser call produced (the suite parses malformed text on
            # purpose, and re-validates the set-aside comment text), a downloadable-font sanitizer
            # note — reports, not exceptions. They carry no script frame (a thrown error's stack
            # has "    at " lines under Playwright, in both engines), and their `name` is the
            # category in the browser's UI locale, so the shape tells them apart, not the words.
            # They go to the console baseline, where each expected category is listed with its
            # cap; an unlisted one still blocks (exit 7). Chromium reports none of this class, so
            # the classification is Firefox-only and a bare thrown string there stays blocking.
            if browser == "firefox" and not re.search(r"^\s+at ", stack, re.M):
                console_errors.append(
                    {"kind": "console", "type": "error", "text": f"{name}: {message}",
                     "location": "", "stack": "", "gecko_report": True}
                )
                return
            console_errors.append(
                {
                    "kind": "pageerror",
                    "type": "pageerror",
                    "text": f"{name}: {message}",
                    "location": "",
                    "stack": stack,
                }
            )

        page.on("console", _on_console)
        page.on("pageerror", _on_pageerror)

        stage = "suite"
        results: list[dict] = []
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            # Wait for the inline script to define runSmokeTests
            await page.wait_for_function(
                "typeof runSmokeTests === 'function'", timeout=10_000
            )
            # Seed the sentinel workspace (see SENTINEL_SEED_JS above). On a pristine page the
            # mounted default is a blank LateralBuoy — the exact end-state several historical
            # leaks converged on, which made them gate-invisible. The sentinel is a fictional
            # LateralBeacon (NATO-phonetic name, synthetic coords) imported through the REAL
            # strict-gated import path, plus sentinel textarea texts.
            await page.evaluate(SENTINEL_SEED_JS)
            # The seed's whole point (see SEED_FAMILIES) is the composition of the mounted
            # stack: prove it before trusting a green suite.
            mounted = await page.evaluate("(compStack || []).map(c => c && c.type)")
            missing = [f for f in SEED_FAMILIES if f not in (mounted or [])]
            if missing:
                await browser_obj.close()
                print(
                    "[FAIL] sentinel seed: the mounted stack lacks "
                    + ", ".join(missing)
                    + f" (got {mounted}) — the suite would run without the family a bare fixture "
                    "emit leaks, and this gate would be blind to it again.",
                    file=sys.stderr,
                )
                return 5, []
            # Pin the source-comment probe polarity BEFORE trusting the suite outcome: with the
            # wrong polarity the comment-anchored lints either false-fail (stripped build under
            # the dev expectation) or silently skip (dev build under the stripped expectation).
            probe = await page.evaluate(
                "typeof _SRC_COMMENTS_KEPT === 'boolean' ? _SRC_COMMENTS_KEPT : null"
            )
            if probe is not expect_src_comments:
                await browser_obj.close()
                got = "kept" if probe is True else ("stripped" if probe is False else "undetectable (_SRC_COMMENTS_KEPT missing)")
                want = "kept" if expect_src_comments else "stripped"
                print(
                    f"[FAIL] source-comment probe polarity: this harness expects comments {want}, "
                    f"but the served app reports {got} — wrong build for this harness.",
                    file=sys.stderr,
                )
                return 5, []
            # Run the in-app smoke invariants
            # Bounded: Playwright does NOT time out page.evaluate by default, so a
            # non-rAF await that never settles (e.g. a fetch against a wedged server
            # thread) used to hang the gate — and any CI wrapping it — indefinitely
            # instead of exiting non-zero (observed live 2026-08-12: a 70-minute hang).
            # _rafT's 120ms fallback stall-proofs only rAF waits. 180s is over 10x the
            # suite's normal ~10-15s runtime; a timeout surfaces as a distinct failure.
            results = await asyncio.wait_for(
                page.evaluate("(async () => await runSmokeTests())()"),
                timeout=180,
            )
            # Then the mount oracle (see MOUNT_ORACLE_JS), on the same page: it replaces the Builder's
            # dataset, so it runs after the suite has restored the seeded workspace, never before.
            stage = "oracle"
            oracle_fx, oracle_notes = _oracle_fixtures()
            oracle = await asyncio.wait_for(
                page.evaluate(MOUNT_ORACLE_JS, oracle_fx),
                timeout=MOUNT_ORACLE_TIMEOUT_S,
            )
        except Exception as e:
            await browser_obj.close()
            # asyncio.TimeoutError IS TimeoutError on 3.11+, and str() of it is EMPTY — the
            # bounded-evaluate path would otherwise print "[FAIL] Playwright error: " with no
            # reason at all, on the one path where the operator has no results to fall back on.
            if isinstance(e, asyncio.TimeoutError) and stage == "oracle":
                reason = (
                    f"the mount oracle did not settle within {MOUNT_ORACLE_TIMEOUT_S}s (bounded page.evaluate)"
                )
            elif isinstance(e, asyncio.TimeoutError):
                reason = (
                    "the smoke suite did not settle within 180s (bounded page.evaluate) — "
                    "an await inside runSmokeTests never resolved"
                )
            else:
                reason = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
            print(f"[FAIL] Playwright error: {reason}", file=sys.stderr)
            # Same reporter as the success path: on this path the console log is the ONLY
            # diagnostic (results is empty, so _format_results never runs), which is exactly
            # where truncation hurt most.
            _report_page_messages(console_errors)
            return 3, results
        await browser_obj.close()

    # Surface console/page messages on EVERY run (not just --verbose): a pageerror
    # or resource failure that does not abort page.evaluate would otherwise ship a
    # green suite. Benign console warnings (e.g. the meta-CSP `frame-ancestors` note
    # this app emits, captured as an [error]-type console message) print here as
    # information; only UNCAUGHT page exceptions ([pageerror]) block, since a green
    # suite cannot be trusted alongside a real page-level exception.
    pageerrors = [e for e in console_errors if e["kind"] == "pageerror"]
    _report_page_messages(console_errors)
    if pageerrors:
        print(
            f"[X] {len(pageerrors)} uncaught page exception(s) during the smoke run — "
            f"a green suite cannot be trusted alongside a page error.",
            file=sys.stderr,
        )
        return 6, results

    unexpected, over = _console_baseline_breaches(console_errors, browser)
    if unexpected or over:
        print(
            "[X] console output deviates from the expected baseline — a green suite cannot be "
            "trusted alongside output nobody has accounted for.",
            file=sys.stderr,
        )
        for label, seen, cap in over:
            print(f"    over baseline: {label} — {seen} occurrence(s), baseline allows {cap}", file=sys.stderr)
        for e in unexpected[:10]:
            loc = f"  at {e['location']}" if e.get("location") else ""
            print(f"    unlisted [{e['type']}] {e['text'][:150]}{loc}", file=sys.stderr)
        if len(unexpected) > 10:
            print(f"    … and {len(unexpected) - 10} more unlisted message(s)", file=sys.stderr)
        print(
            "    If the message is benign, add it to _CONSOLE_BASELINE in this file WITH the reason "
            "it is expected. Do not widen a count to make a real regression fit.",
            file=sys.stderr,
        )
        return 7, results

    if not _report_oracle(oracle, oracle_notes):
        return 8, results
    return 0, results


# Expected console output, and nothing else. Before this existed the gate blocked only on
# `pageerror`, and `_report_page_messages` groups by message TEXT — so the app's own Rule-25
# alarm ("validation modified the validator textarea"), which one smoke invariant emits
# DELIBERATELY to prove the sentinel works, made a REAL breach invisible: a second occurrence
# only bumped the printed count from (x1) to (x2) and the gate still exited 0. Each entry
# carries the reason it is expected; an unlisted message, or more of a listed one than the
# baseline allows, now blocks with exit 7.
#
# `cap` is an upper bound, not a pin. Where a count is environment-sensitive the bound is wide
# and says so; where it is exact (the deliberate emission) it is exact, because that exactness
# is the whole point.
_CONSOLE_BASELINE = [
    (
        "meta-CSP frame-ancestors note",
        lambda e: "frame-ancestors" in e["text"],
        2,
        "Chromium reports that `frame-ancestors` cannot be enforced from a <meta> CSP. The app "
        "ships its policy that way deliberately — it is a static file with no server to set a "
        "header — so the directive is inert by design, not misconfigured.",
    ),
    (
        "Annex D symbol fetch failures (known open defect PORT-1)",
        lambda e: "Annex_D/Symbols/" in (e.get("location") or "")
        or ("Failed to load resource" in e["text"] and "Annex_D" in (e.get("location") or "")),
        0,
        "PORT-1 has landed: loadSymbol now acquires one of SYMBOL_LANES before fetching, so the "
        "app never holds more symbol requests open than a browser would issue per origin anyway "
        "and this single-threaded server no longer sheds connections. The entry is KEPT at 0 "
        "rather than deleted so the expectation is stated where the next operator will look: a "
        "recurrence reports as 'over baseline: … 1 occurrence, baseline allows 0', which names "
        "the defect, instead of an anonymous 'unlisted message'. Measured before the fix: 1701 "
        "in a single run. Do not raise this to make a regression fit.",
    ),
    (
        "deliberate Rule-25 invariant-breach emission",
        lambda e: "invariant breach" in e["text"] and "validator textarea" in e["text"],
        1,
        "The data-custody invariant monkey-patches renderAllVal to corrupt valIn mid-run and "
        "asserts the sentinel restores it verbatim and banners. EXACTLY ONE is expected. A second "
        "occurrence is a REAL custody breach — that is precisely what this baseline exists to "
        "surface, so this cap must not be raised.",
    ),
    # ── Firefox only (the fifth field): Gecko error-console categories that _on_pageerror
    # reclassifies as console entries (see there). Chromium reports neither, so neither can
    # match on a Chromium run; the entries are skipped outright for it.
    (
        "Gecko XML parsing reports for the suite's own malformed or set-aside text",
        lambda e: bool(e.get("gecko_report")) and "/s201_aton_studio.html" in e["text"],
        12,
        "Gecko reports every DOMParser failure to its error console, naming the page URL; the "
        "suite parses ill-formed fixtures on purpose and re-validates the set-aside comment text "
        "in per-test teardowns (no root element), and the validator answers each with GML-STR-01. "
        "Measured on Firefox 156 after the pass-732 serializer fix: exactly 12 per run (10 of the "
        "set-aside text, 1 prefix not bound, 1 declaration not at the start). Before the fix the "
        "figure was 25: the 13 extra were the ill-formed quick-fix documents themselves, so this "
        "count is a detector — an increase means some path writes XML the parser rejects. Do not "
        "raise it to make a regression fit.",
        ("firefox",),
    ),
    (
        "Gecko downloadable-font sanitizer notes for the bundled OpenSans faces",
        lambda e: bool(e.get("gecko_report")) and "font-family:" in e["text"] and "Annex_D/Fonts/" in e["text"],
        4,
        "Gecko's OpenType sanitizer discards the kern table of Annex_D/Fonts/OpenSans-Regular.ttf and "
        "OpenSans-Bold.ttf ('Too large subtable' then 'Table discarded': two notes per face, four "
        "in all). The faces still load and render; the note is about a table the app does not "
        "rely on. Exact: a fifth note means another face or table went wrong.",
        ("firefox",),
    ),
]


def _baseline_entries(engine: str):
    """The baseline entries that apply to `engine`: a four-field entry applies to every engine,
    a fifth field names the engines it is for (the Gecko report categories are Firefox-only)."""
    out = []
    for entry in _CONSOLE_BASELINE:
        label, matcher, cap, why = entry[:4]
        engines = entry[4] if len(entry) > 4 else None
        if engines is None or engine in engines:
            out.append((label, matcher, cap, why))
    return out


def _console_baseline_breaches(msgs: list[dict], engine: str = "chromium"):
    """Split console output into (unlisted messages, listed-but-over-cap entries).

    `pageerror` entries are excluded: they have their own blocking arm above and would
    otherwise be reported twice. The Gecko reports _on_pageerror reclassifies arrive here as
    console entries (kind "console", gecko_report True) and are judged like any other.
    """
    entries = _baseline_entries(engine)
    counts: dict[str, int] = {}
    unexpected: list[dict] = []
    for e in msgs:
        if e.get("kind") == "pageerror":
            continue
        for label, matcher, _cap, _why in entries:
            try:
                hit = matcher(e)
            except Exception:
                hit = False
            if hit:
                counts[label] = counts.get(label, 0) + 1
                break
        else:
            unexpected.append(e)
    over = [
        (label, counts[label], cap)
        for label, _m, cap, _w in entries
        if counts.get(label, 0) > cap
    ]
    return unexpected, over


def _report_page_messages(msgs: list[dict], stream=None) -> None:
    """Print EVERY distinct console/page message once, with an occurrence count.

    The previous report printed `console_errors[:10]` verbatim. That defeats the
    observability half of finding SG-BLD-1 (dev/full-audit-findings-2026-08.md)
    this exists for: one noisy benign class (headless symbol preload emits
    hundreds of `ERR_INSUFFICIENT_RESOURCES` lines) fills all ten slots and silently
    crowds out every other distinct message, so a genuinely interesting one appears on a
    quiet run and vanishes on a noisy one — which reads as an intermittent regression.
    Grouping makes the flood cost ONE line instead of ten, so there is no reason to cap:
    the output length is bounded by message VARIETY, not volume.

    Note the blocking half of that finding was never broken — `pageerror` filtering has
    always run over the full list, so an uncaught exception still fails the gate no matter
    how many messages precede it. This is an observability fix; the pass/fail contract is
    unchanged.

    Writes to stderr by default so `--json` stdout stays parseable JSON.
    """
    stream = stream or sys.stderr
    if not msgs:
        return
    groups: dict[tuple, dict] = {}
    for m in msgs:
        key = (m["kind"], m["type"], m["text"])
        g = groups.setdefault(key, {**m, "count": 0, "locations": []})
        g["count"] += 1
        if m.get("location") and m["location"] not in g["locations"]:
            g["locations"].append(m["location"])
    # pageerrors first (the only blocking class), then by descending frequency
    ordered = sorted(groups.values(), key=lambda g: (g["kind"] != "pageerror", -g["count"]))
    print(
        f"\n[note] {len(msgs)} console/page message(s) during run, "
        f"{len(ordered)} distinct:",
        file=stream,
    )
    for g in ordered:
        times = f"  (x{g['count']})" if g["count"] > 1 else ""
        print(f"  [{g['type']}] {g['text']}{times}", file=stream)
        if g["locations"]:
            shown = g["locations"][:3]
            more = len(g["locations"]) - len(shown)
            print(
                "      at " + ", ".join(shown) + (f" (+{more} more)" if more > 0 else ""),
                file=stream,
            )
        if g.get("stack"):
            for line in g["stack"].splitlines():
                print(f"      {line}", file=stream)


def _expected_smoke_count() -> int:
    """Single-source the expected suite size from precommit-check.py's
    _COUNT_GROUND_TRUTH (Rule 23 — no second copy of the number here).
    Without a suite-size assertion the gate checks only per-test pass flags,
    so an empty/truncated results list (a refactor early-returning `tests`,
    or conditionally skipped _t() registrations) ships green as
    "0/0 tests passed"."""
    import re as _re
    pc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "precommit-check.py")
    with open(pc, encoding="utf-8") as f:
        src = f.read()
    # Scope the search to the _COUNT_GROUND_TRUTH literal instead of the whole file. A bare
    # file-wide `"smoke": N` search silently binds to the FIRST such pair anywhere — a doc
    # string, a comment, or a future unrelated dict — and the gate would then assert the suite
    # size against a number that is not the ground truth, while looking like it passed (Rule 9:
    # assert the source, do not assume the first match is it).
    block = _re.search(r"_COUNT_GROUND_TRUTH\s*(?::[^=]*)?=\s*\{(.*?)\}", src, _re.S)
    if not block:
        raise RuntimeError(
            "cannot locate _COUNT_GROUND_TRUTH in precommit-check.py — the suite-size "
            "ground truth has moved or been renamed"
        )
    m = _re.search(r'"smoke"\s*:\s*(\d+)', block.group(1))
    if not m:
        raise RuntimeError('cannot read the "smoke" ground truth from _COUNT_GROUND_TRUTH')
    return int(m.group(1))


def _assert_suite_size(results: list[dict]) -> str | None:
    """Return an error string when the suite size deviates from the ground truth."""
    expected = _expected_smoke_count()
    if len(results) != expected:
        return (f"suite-size mismatch: runSmokeTests() registered {len(results)} tests, "
                f"ground truth (_COUNT_GROUND_TRUTH['smoke']) is {expected} — "
                "a skipped/duplicated _t() registration or a stale ground truth")
    return None


def _format_results(results: list[dict], verbose: bool) -> tuple[int, str]:
    """Return (exit_code, human_readable_text)."""
    size_err = _assert_suite_size(results)
    if size_err:
        return 1, f"[X] Browser smoke gate: {size_err}"
    total = len(results)
    failed = [t for t in results if not t.get("passed")]
    by_category: dict[str, list[dict]] = {}
    for t in results:
        by_category.setdefault(t.get("category", "?"), []).append(t)

    lines = []
    lines.append(f"\n=== S-201 AtoN Studio browser smoke gate — {_ENGINE_LABEL} ===\n")

    if verbose:
        for cat, tests in by_category.items():
            n_pass = sum(1 for t in tests if t.get("passed"))
            n_fail = len(tests) - n_pass
            cat_marker = "[OK]" if n_fail == 0 else "[X]"
            lines.append(f"  {cat_marker} {cat}: {n_pass}/{len(tests)}")
            for t in tests:
                marker = "[pass]" if t.get("passed") else "[FAIL]"
                detail = t.get("detail") or ""
                detail_suffix = f" — {detail}" if detail and (verbose or not t.get("passed")) else ""
                lines.append(f"      {marker} {t.get('name')}{detail_suffix}")
        lines.append("")

    if failed:
        if not verbose:
            lines.append("Failed tests:")
            for t in failed:
                lines.append(f"  [FAIL] {t.get('name')} — {t.get('detail') or 'failed'}")
            lines.append("")
        lines.append(f"[X] Browser smoke gate: {len(failed)}/{total} test(s) failed.")
        return 1, "\n".join(lines)
    lines.append(f"[OK] Browser smoke gate: {total}/{total} tests passed.")
    return 0, "\n".join(lines)


def _assert_served_app_is_this_repo(url: str, local_path: str | None = None) -> str | None:
    """Prove the app answering on `url` is byte-identical to the file at local_path
    (default: this worktree's s201_aton_studio.html; the end-user-bundle verify passes
    the bundle's own copy).

    Rule 11/13 let every other gate result rest on "the browser gate is green".
    That inference is only sound if the browser ran THIS code. When the port is
    already bound the gate does not own the server, and this project is developed
    with one worktree (and one server) per session, plus a main tree that
    routinely carries uncommitted work at a newer APP_VERSION. A stale server
    therefore serves *real, plausible, wrong* code — same app, different bytes.

    A version-string comparison is not enough: two worktrees at the same
    APP_VERSION can differ by an entire pass of uncommitted edits. Compare the
    SHA-256 of the served bytes against the file on disk.

    Returns an error string, or None when the served bytes match.
    """
    if local_path is None:
        local_path = os.path.join(REPO_ROOT, "s201_aton_studio.html")
    with open(local_path, "rb") as f:
        local_digest = hashlib.sha256(f.read()).hexdigest()
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            served = resp.read()
    except Exception as e:  # noqa: BLE001 - any transport failure is fatal for the gate
        return f"cannot fetch {url} to verify app identity: {e}"
    served_digest = hashlib.sha256(served).hexdigest()
    if served_digest != local_digest:
        return (
            "the server on this port is NOT serving this worktree's app — refusing to\n"
            "      report a verdict on code that was never tested.\n"
            f"      served  sha256: {served_digest[:16]}…  ({len(served)} bytes)\n"
            f"      on-disk sha256: {local_digest[:16]}…  ({os.path.getsize(local_path)} bytes)\n"
            f"      file: {local_path}\n"
            "      Stop the other server (another worktree? an earlier run?) or pass --port with a free port."
        )
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the in-app smoke gate headlessly via Playwright."
    )
    parser.add_argument("--port", type=int, default=0, help="HTTP server port (default 0 = OS-assigned free port)")
    parser.add_argument("--json", action="store_true", help="Emit JSON results to stdout")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print every test (default: only failures)")
    parser.add_argument("--browser", choices=("chromium", "firefox"), default="chromium",
                        help="engine (default chromium, the definition of done); firefox drives the installed "
                             "Firefox over Playwright's moz-firefox BiDi channel — no download")
    parser.add_argument("--firefox-exe", default=None,
                        help="Firefox executable for --browser firefox (default: $FIREFOX_BIN, then the standard install paths)")
    args = parser.parse_args()

    server = None
    try:
        try:
            server, port = _start_http_server(args.port)
        except OSError as e:
            # Someone else owns this port. The gate must NOT validate a stranger:
            # every other Rule-11/13 result is trusted because "the browser gate is
            # green", and that inference only holds if the browser ran THIS code.
            print(
                f"[X] could not bind port {args.port} ({e}).\n"
                f"      Another process owns it — very likely a server from a different git worktree.\n"
                f"      Refusing to run the suite against code this gate did not serve.\n"
                f"      Re-run without --port to use an OS-assigned free port.",
                file=sys.stderr,
            )
            return 4

        ident_err = _assert_served_app_is_this_repo(f"http://127.0.0.1:{port}/s201_aton_studio.html")
        if ident_err:
            print(f"[X] {ident_err}", file=sys.stderr)
            return 4

        exit_code, results = asyncio.run(
            _run_gate(port, args.verbose, browser=args.browser, firefox_exe=args.firefox_exe)
        )
        if exit_code != 0:
            # Exits 6, 7 and 8 (a page exception, the console baseline, the mount oracle) still carry a
            # fully populated results list, and so does exit 3 when only the oracle timed out.
            # Returning here discarded it, so the operator was told "a page error invalidates
            # this run" with no way to see WHICH invariants had failed alongside it — often the
            # fastest route to the cause. Print what we have, then keep the blocking exit code.
            if results:
                if args.json:
                    print(json.dumps(results, indent=2))
                else:
                    _rc, txt = _format_results(results, args.verbose)
                    print(txt)
                    print(
                        "[note] the suite outcome above is reported for diagnosis only — the "
                        "gate still fails on the failure reported above.",
                        file=sys.stderr,
                    )
            return exit_code

        if args.json:
            print(json.dumps(results, indent=2))
            size_err = _assert_suite_size(results)
            if size_err:
                print(f"[X] {size_err}", file=sys.stderr)
                return 1
            return 1 if any(not t.get("passed") for t in results) else 0

        rc, txt = _format_results(results, args.verbose)
        print(txt)
        return rc
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    sys.exit(main())
