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
#   1. precommit-check.py        — fast static (a few seconds, 23 checks, every commit)
#   2. run-browser-smoke-gate.py — slow runtime (full smoke suite, then the mount oracle, then
#                                  the XSD leg, then a fresh page's first validation; before
#                                  push/release; can be wired into CI)
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
#   2 playwright or lxml not installed, or the requested engine cannot launch (--browser firefox: no
#     Firefox found at --firefox-exe / $FIREFOX_BIN / the standard install paths, or a Playwright
#     without the moz-firefox channel)   3 Playwright error / suite did not settle within 180s
#   4 could not own the port, or the served app is not this worktree's file
#   5 source-comment probe polarity mismatch (wrong build for this harness)
#   6 an uncaught page exception occurred during the run
#   7 console output deviates from the expected baseline (unlisted message, more of a listed
#     one than it allows, or fewer of an exact one than its floor — see _CONSOLE_BASELINE)
#   8 the mount oracle failed: for some fixture, the GML the Builder writes after opening every
#     feature differs from the GML of the import candidate the import report measured, either of
#     them is not well-formed XML, the import report could not be made, opening a feature changed
#     its own GML (the per-mount sentinel), or a fixture could not be run — see MOUNT_ORACLE_JS
#   9 the first-validation leg failed: on a fresh page, a real click on Run validation did not
#     reach the button, or did not run the self-checks first, or the data was validated or
#     painted before their verdict was held, or without the hand-over cover, or the validation
#     the click queued did not finish, or a self-check failed on that path — see
#     _first_validation_faults
#  10 the XSD leg failed: GML the app writes for a fixture — the dataset and each feature alone,
#     written from the parse and from the import candidate — does not validate against the S-201
#     2.0.0 Annex B XSD, could not be written, or the schema is missing from the development
#     tree — see XSD_EMIT_JS
#  11 keyboard focus did not come back: the gate focuses a control before the suite runs (FOCUS_SEED_JS), and after
#     the run focus is on another element, on the page body, or the suite recorded that it could not give it back
#     (runSmokeTests._focusBack) — see FOCUS_AFTER_JS
#
# DEPENDENCIES (one-time setup)
# -----------------------------
#   pip install playwright lxml
#   playwright install chromium
#   lxml is the XSD leg's validator (dev/scripts/s201_xsd.py); a snapshot tree ships no schema and
#   runs without the leg, so it needs no lxml.
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
# import fold stopped folding one of them). The sentinel is written in http://www.iho.int/S-201/gml/cs0/2.0,
# the namespace the app wrote before 2.0.0, on purpose: every gate run then imports a legacy-namespace dataset through
# the real path (Rule 4), while the samples, the suite's fixtures and the FC kitchen are in the S-201 2.0.0 namespace.
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
# bundled example the import refuses, for any reason, fails. The texts compared are also parsed: a candidate or a
# Builder output that is not well-formed XML fails, and so does a fixture whose import report could not be made (its
# verdict is read through the same wrapper) — two equal texts can both be broken, and a report that failed describes
# nothing. Each failed parse is counted (badParses): in Gecko it is also a report in the error console, which the
# console baseline allows for exactly.
MOUNT_ORACLE_TIMEOUT_S = 240
MOUNT_ORACLE_JS = r"""async (fixtures) => {
  const GMLNS = "http://www.opengis.net/gml/3.2";
  const out = { fixtures: [], warns: 0, badParses: 0 };
  /* the engine's own verdict on a text: null when it is well-formed XML, else its parser's message */
  const wfErr = xml => {
    const d = new DOMParser().parseFromString(xml, "application/xml");
    const pe = d.getElementsByTagName("parsererror")[0];
    if (!pe) return null;
    out.badParses++;
    return (pe.textContent || "parsererror").replace(/This page contains the following errors:|Below is a rendering of the page up to the first error\.?/g, " ")
      .replace(/\s+/g, " ").trim().slice(0, 240);
  };
  const members = xml => {
    const d = new DOMParser().parseFromString(xml, "application/xml");
    if (d.getElementsByTagName("parsererror").length) { out.badParses++; return null; }
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
    try { cap = { text: String(generateAllGML(cand)), reportFailed: rep && rep.failed ? String(rep.why || "unknown") : null }; }
    catch (e) { cap = { error: String((e && e.message) || e) }; }
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
        if (cap.reportFailed) r.reportFailed = cap.reportFailed;
        const nwf = [];
        { const w = wfErr(cap.text); if (w) nwf.push("the import candidate's GML: " + w); }
        for (let i = 1; i < builderFeats.length; i++) builderSelectFeat(i);
        builderUp();
        const mounted = String(generateAllGML(builderFeats));
        r.features = builderFeats.length;
        r.ms = Math.round(performance.now() - t0);
        r.same = mounted === cap.text;
        if (!r.same) {
          const w = wfErr(mounted); if (w) nwf.push("the Builder's GML: " + w);
          r.diff = diffDocs(cap.text, mounted);
        }
        /* and again in the other order: what the Builder writes does not depend on the order the features are opened in */
        if (r.same && builderFeats.length > 1) {
          for (let i = builderFeats.length - 2; i >= 0; i--) builderSelectFeat(i);
          builderUp();
          const again = String(generateAllGML(builderFeats));
          if (again !== cap.text) {
            r.same = false; r.reversed = true;
            const w = wfErr(again); if (w) nwf.push("the Builder's GML, the features opened in the other order: " + w);
            r.diff = diffDocs(cap.text, again);
          }
        }
        if (nwf.length) r.nwf = nwf;
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
    bad = [r for r in fx if r.get("error") or r.get("same") is False or r.get("sentinel") or r.get("nwf") or r.get("reportFailed")]
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
        for w in r.get("nwf") or []:
            print(f"    not well-formed XML — {w}", file=sys.stderr)
        if r.get("reportFailed"):
            print(f"    the import report could not be made: {r['reportFailed']}", file=sys.stderr)
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
              "report measured, or what either writes is not well-formed XML.", file=sys.stderr)
        return False
    feats = sum(r.get("features", 0) for r in run)
    print(f"[OK] mount oracle: {len(run)} fixture(s), {feats} feature(s) opened — the import report was made for each, the "
          "Builder writes the import candidate's GML, well-formed, and no opening changed a feature.", file=sys.stderr)
    return True


# ── The XSD leg ─────────────────────────────────────────────────────────────────────────────────────
# Run after the mount oracle, on the same page. S-201 PS 2.0.0 §11 requires feature instances to validate against the
# S-201 2.0.0 schema (dev/spec-sources/s-201-xsd/S-201_Ed2.0.0_Annex_B_DataProductFormatSchemas.xsd, loaded by
# s201_xsd.py as pre-commit check #20 loads it). Check #20 holds the bundled samples and csv_to_s201.py's output to it;
# this leg holds the dataset GML the app itself writes (CATALOG.XML and the ISO metadata are not validated against a
# schema). For each fixture — fc_kitchen.fixtures(dii=True), the oracle's documents
# with a complete identification block (the generator writes only the identification fields a file has, so without one
# every output would fail there alone), and the four bundled examples — it writes, with generateAllGML (the writer of
# the Builder's output: its copy and its hand-over to the Validator, from which the Validator tab exports): the dataset
# from the parse, each
# feature of the parse alone, the import candidate the Builder is loaded with, and each candidate feature alone (with
# the components folded into it). The schema checks the root, the identification block, the members wrapper and each
# member's name and namespace, and a member's content laxly (s201_xsd). Nothing in the page is changed: the parse is
# the fixture's own, the candidate is built as the import builds it, and the writer keeps the Builder's state.
XSD_LEG_TIMEOUT_S = 60   # per fixture, one page.evaluate each
XSD_EMIT_JS = r"""async (fx) => {
  const out = { texts: [], error: null, warns: 0 };
  const ow = console.warn;
  console.warn = () => { out.warns++; };
  const put = (label, fn) => {
    try { out.texts.push({ label, text: String(fn()) }); }
    catch (e) { out.texts.push({ label, error: String((e && e.message) || e).slice(0, 300) }); }
  };
  try {
    const text = typeof fx.idx === "number" ? exGML[fx.idx] : fx.text;
    const parsed = parseAllGML(text);
    if (!Array.isArray(parsed) || !parsed.length) { out.error = "the parse gave no features" + (parsed && parsed.error ? ": " + parsed.error : ""); return out; }
    const loadable = parsed.filter(f => _fcIsType(f.featureType));
    const idOf = (f, i) => f.gmlId || f.featureId || "#" + (i + 1);
    put("the dataset, written from the parse", () => generateAllGML(loadable));
    loadable.forEach((f, i) => put(idOf(f, i) + " (" + f.featureType + ") alone, from the parse", () => generateAllGML([Object.assign({}, f, { _compStack: [] })])));
    const cand = _buildImportCandidate(loadable);
    put("the import candidate", () => generateAllGML(cand));
    cand.forEach((f, i) => put(idOf(f, i) + " (" + f.featureType + ") alone, from the import candidate", () => generateAllGML([f])));
  } catch (e) { out.error = String((e && e.stack) || e).slice(0, 600); }
  finally { console.warn = ow; }
  return out;
}"""


def _xsd_fixtures() -> tuple[list[dict], list[str]]:
    """The XSD leg's fixtures (the page adds exGML) and the notes on what could not be included — as _oracle_fixtures,
    with the complete identification block."""
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    try:
        import fc_kitchen
    finally:
        sys.path.pop(0)
    if os.path.exists(fc_kitchen.FC_XML):
        return [{"name": n, "text": t} for n, t in fc_kitchen.fixtures(dii=True)], []
    return ([{"name": n, "text": f(True)} for n, f in fc_kitchen.EDGE_FIXTURES],
            ["the FC kitchen fixtures were not built: the FC XML is not in this tree (" + os.path.relpath(fc_kitchen.FC_XML, REPO_ROOT) + ")"])


async def _xsd_leg(page, schema, s201_xsd) -> tuple[list[dict], list[str]]:
    """Write every fixture's texts in the page (XSD_EMIT_JS, one fixture per bounded evaluate) and validate each
    against the schema here; the texts are not kept, only each one's problems."""
    fx, notes = _xsd_fixtures()
    n_ex = await page.evaluate("Array.isArray(exGML) ? exGML.length : 0")
    fx += [{"name": f"exGML[{i}]", "idx": i} for i in range(n_ex)]
    out = []
    for f in fx:
        r = await asyncio.wait_for(page.evaluate(XSD_EMIT_JS, f), timeout=XSD_LEG_TIMEOUT_S)
        rec = {"name": f["name"], "error": r.get("error"), "texts": []}
        for t in r.get("texts") or []:
            if "error" in t:
                rec["texts"].append({"label": t["label"], "error": t["error"]})
            else:
                rec["texts"].append({"label": t["label"], "problems": s201_xsd.problems(schema, t["text"])})
        out.append(rec)
    return out, notes


def _report_xsd(results: list[dict], notes: list[str]) -> bool:
    """Print the XSD leg's outcome (stderr, so --json stdout stays JSON); True when every text was written and validates."""
    for n in notes:
        print(f"[note] XSD leg: {n}", file=sys.stderr)
    bad = 0
    for r in results:
        fails = [t for t in r["texts"] if t.get("error") or t.get("problems")]
        if not r.get("error") and not fails:
            continue
        bad += 1
        print(f"[X] XSD leg: {r['name']}", file=sys.stderr)
        if r.get("error"):
            print(f"    {r['error']}", file=sys.stderr)
        for t in fails[:6]:
            if t.get("error"):
                print(f"    {t['label']}: could not be written — {t['error']}", file=sys.stderr)
            else:
                print(f"    {t['label']}: " + " | ".join(t["problems"])[:400], file=sys.stderr)
        if len(fails) > 6:
            print(f"    … and {len(fails) - 6} more text(s) that fail", file=sys.stderr)
    texts = sum(len(r["texts"]) for r in results)
    if bad:
        print(f"[X] XSD leg: {bad} of {len(results)} fixture(s) failed — GML the app writes does not validate against "
              "the S-201 2.0.0 Annex B XSD.", file=sys.stderr)
        return False
    print(f"[OK] XSD leg: {len(results)} fixture(s), {texts} text(s) the app writes — every one validates against the "
          "S-201 2.0.0 Annex B XSD.", file=sys.stderr)
    return True


# ── The first-validation leg ────────────────────────────────────────────────────────────────
# The suite run above calls runSmokeTests directly, so it never takes the path a user takes:
# a session's first validation, which waits for the self-checks (_selfChecksFirst in the app).
# The in-suite order locks drive that path against a stand-in run; this leg drives it for
# real, on a FRESH page, with a real click on the Run validation button, and checks the order
# from outside. It records three things:
#   - the two covers, by a MutationObserver. The record of the self-check cover's mount also
#     holds what the click had left at that instant (results, stamp, findings in the pane,
#     verdict): the observer's callback runs in the task that mounted the cover, before any
#     self-check has run.
#   - the app state, by a sampler on a self-rescheduling zero-delay timer, logged each time a
#     sample differs from the one before it. That is one sample per timer turn, which the
#     browser spaces a few milliseconds apart, and none while a task runs: a state that comes
#     and goes between two samples is not seen, so the checks read only states that persist.
#   - what the document held as the callbacks of each frame began, by a requestAnimationFrame
#     logger. It registers itself again from its own callback, so in every frame it runs ahead
#     of what the page registered since the frame before. The record is completed in the task
#     after the frame (`after`: whether the pane held findings then), by a timer taken from the
#     window before any page script ran: what a callback of that frame did is seen there.
# Records and frames share one counter, so their order does not depend on the clock's grain.
# The leg wraps neither runVal nor runSmokeTests: several locks read those functions' source
# and go red under a wrapper.
FIRST_VALIDATION_TIMEOUT_S = 180
# The bound on the page's answer when it is asked for its record, after the first validation has finished.
FIRST_VALIDATION_REPORT_TIMEOUT_S = 60
# The bound on the leg as a whole. It is the only bound on the calls that put no question to the page and
# take none of their own: the init script, the mouse click, closing the context.
FIRST_VALIDATION_LEG_TIMEOUT_S = FIRST_VALIDATION_TIMEOUT_S + 120
# How far under the hold the measured hold may read: the clock is rounded to a millisecond, with jitter, in
# Firefox, and the timer that starts the hold follows the frame it is measured from by a few milliseconds.
FIRST_VALIDATION_HOLD_SLACK_MS = 8

FIRST_VALIDATION_INIT_JS = r"""
(() => {
  const T = window.__fv = {ev: [], frames: [], seq: 0, clickAt: null, clickHit: false, clickOn: ''};
  const now = () => +performance.now().toFixed(1);
  T.log = (k, x) => T.ev.push(Object.assign({k, t: now(), n: T.seq++}, x || {}));
  const held = () => { try { const vr = document.getElementById('valRes');
    return {feats: Array.isArray(lastValAll) ? lastValAll.length : null, stamped: typeof runVal._lastText === 'string',
      findings: !!(vr && vr.querySelector('.vfeat-head')), verdict: Array.isArray(lastSmokeResults) ? lastSmokeResults.length : null};
  } catch (e) { return {error: String(e)}; } };
  const mo = new MutationObserver(ms => { for (const m of ms) {
    for (const n of m.addedNodes) if (n.id === 'smokeScrim' || n.id === 'valHandover') T.log('mount:' + n.id, {held: held()});
    for (const n of m.removedNodes) if (n.id === 'smokeScrim' || n.id === 'valHandover') T.log('unmount:' + n.id); } });
  const arm = () => { if (document.body) mo.observe(document.body, {childList: true}); else setTimeout(arm, 0); };
  arm();
  document.addEventListener('click', e => { if (e.isTrusted && T.clickAt === null) {
    const el = e.target;
    T.clickAt = now();
    T.clickHit = !!(el && el.closest && el.closest('button[onclick="runVal()"]'));
    T.clickOn = el && el.tagName ? el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') : '';
    T.log('click', {hit: T.clickHit}); } }, true);
  const later = window.setTimeout.bind(window);
  const painted = () => { const vr = document.getElementById('valRes'); return !!(vr && vr.querySelector('.vfeat-head')); };
  const frame = () => {
    const ho = document.getElementById('valHandover');
    const rec = {t: now(), n: T.seq++, scrim: !!document.getElementById('smokeScrim'), hand: !!ho,
      says: !!(ho && (ho.textContent || '').trim()), findings: painted(), after: null};
    T.frames.push(rec);
    later(() => { rec.after = painted(); }, 0);
    if (T.frames.length < 20000) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
})();
"""

FIRST_VALIDATION_SAMPLER_JS = r"""
(() => {
  const T = window.__fv;
  let last = '';
  const tick = () => {
    const vr = document.getElementById('valRes'), root = document.querySelector('.root');
    const s = {verdict: Array.isArray(lastSmokeResults) ? lastSmokeResults.length : null, running: !!_smokeRunning,
      feats: Array.isArray(lastValAll) ? lastValAll.length : null, stamped: typeof runVal._lastText === 'string',
      scrim: !!document.getElementById('smokeScrim'), hand: !!document.getElementById('valHandover'),
      inert: !!(root && root.inert), findings: !!(vr && vr.querySelector('.vfeat-head')), queued: _scf.q.length, armed: !!_scf.armed};
    const k = JSON.stringify(s);
    if (k !== last) { last = k; T.log('state', s); }
    const sc = document.getElementById('smokeScrim'), ho = document.getElementById('valHandover');
    if (sc && sc.textContent && !T.coverText) T.coverText = sc.textContent;
    if (ho && !sc) { T.handSamples = (T.handSamples || 0) + 1; if (ho.textContent && !T.handText) T.handText = ho.textContent; }
    setTimeout(tick, 0);
  };
  tick();
})();
"""

FIRST_VALIDATION_CLICKED_JS = "({at: window.__fv.clickAt, hit: window.__fv.clickHit, on: window.__fv.clickOn, queued: _scf.q.length, armed: !!_scf.armed, running: !!_smokeRunning})"

FIRST_VALIDATION_DONE_JS = (
    "Array.isArray(lastSmokeResults) && !_smokeRunning && !document.getElementById('smokeScrim')"
    " && !document.getElementById('valHandover') && !_scf.q.length && !_scf.armed"
)

FIRST_VALIDATION_REPORT_JS = r"""
() => {
  const T = window.__fv, vr = document.getElementById('valRes'), root = document.querySelector('.root');
  const sm = Array.isArray(lastSmokeResults) ? lastSmokeResults : [];
  const first = vr ? vr.firstElementChild : null;
  return {ev: T.ev, frames: T.frames, clickAt: T.clickAt, coverText: T.coverText || '',
    handText: T.handText || '', handSamples: T.handSamples || 0,
    smoke: sm.map(t => ({name: t.name, category: t.category, passed: !!t.passed, detail: t.detail || ''})),
    feats: Array.isArray(lastValAll) ? lastValAll.length : null,
    structural: Array.isArray(lastStructResults) ? lastStructResults.length : null,
    bannerFirst: !!(first && first.classList.contains('val-selfcheck')),
    bannerOk: !!(vr && vr.querySelector('.val-selfcheck-ok')) && !(vr && vr.querySelector('.val-selfcheck-bad')),
    notices: vr ? vr.querySelectorAll('.val-breach,.val-drain-error,.val-late-report').length : -1,
    translated: /translated-(ltr|rtl)/.test(document.documentElement.className),
    inert: !!(root && root.inert), valIn: document.getElementById('valIn').value, example: exGML[0],
    resultsText: Array.isArray(lastValAll) ? ((_valAllRun.get(lastValAll) || {}).text === document.getElementById('valIn').value) : null,
    hold: typeof _SCF_DWELL_MS === 'number' ? _SCF_DWELL_MS : null,
    blocks: vr ? vr.querySelectorAll('.vfeat-head').length : -1};
}
"""


def _first_validation_faults(rep: dict) -> list[str]:
    """What the first-validation record shows that the order forbids. Empty list: the order held.
    Presence comes before validity throughout: a record that is missing is a fault, not a pass."""
    faults: list[str] = []
    ev, frames, click = rep.get("ev") or [], rep.get("frames") or [], rep.get("clickAt")
    if click is None:
        return ["the click on Run validation was not seen by the page"]
    after = [e for e in ev if e["t"] >= click]
    states = [e for e in after if e["k"] == "state"]
    mounts = [e for e in after if e["k"] == "mount:smokeScrim"]
    unmounts = [e for e in after if e["k"] == "unmount:smokeScrim"]
    if len(mounts) != 1 or len(unmounts) != 1:
        return [f"expected one run of the self-checks behind its cover, saw {len(mounts)} cover mount(s) "
                f"and {len(unmounts)} removal(s)"]
    up, down = mounts[0], unmounts[0]
    # 1. nothing validated, stamped or painted when the self-checks started
    held = up.get("held")
    if not isinstance(held, dict) or "error" in held:
        faults.append(f"what the click had left when the self-check cover went up was not recorded ({held!r}): "
                      "the check that nothing was validated before the self-checks examined nothing")
    elif held["feats"] is not None or held["stamped"] or held["findings"] or held["verdict"] is not None:
        faults.append(f"when the self-check cover went up the data had been validated, stamped or painted, "
                      f"or a verdict was held already: {held}")
    for s in states:
        if s["n"] > up["n"]:
            break
        if s["feats"] is not None or s["stamped"] or s["findings"]:
            faults.append(f"before the self-checks started the data had been validated or painted "
                          f"(state at {s['t']} ms)")
            break
    # Frames are required under the self-check cover, where the suite runs for seconds: they show that the
    # frame logger ran, and each of them must have seen the cover. None is required between the click and
    # the mount — the run starts on a zero-delay timer and a frame need not fall there — so that window is
    # held by the record taken at the mount (held, above), which is required; a frame that does fall there
    # must not show findings. (Under the cover the pane holds the suite's own fixture findings.)
    covered = [f for f in frames if up["n"] < f["n"] < down["n"]]
    if not covered:
        faults.append(f"no frame was recorded while the self-check cover was up ({len(frames)} frame(s) in the "
                      "whole record): the frame logger did not run, and the frame checks examined nothing")
    elif any(not f["scrim"] for f in covered):
        faults.append("a frame recorded between the mount and the removal of the self-check cover did not see "
                      "the cover")
    if any(f["findings"] and not f["scrim"] and not f["hand"] for f in frames if click <= f["t"] and f["n"] < up["n"]):
        faults.append("a frame presented between the click and the self-check cover showed findings")
    # 2. the verdict precedes the findings, which are computed behind the hand-over cover
    first = next((s for s in states if s["n"] > down["n"] and s["feats"] is not None and not s["running"]), None)
    if first is None:
        faults.append("the validation that waited behind the self-checks never ran")
    else:
        if first["verdict"] is None:
            faults.append(f"the data was validated with no verdict held (state at {first['t']} ms)")
        if not first["hand"] or not first["inert"]:
            faults.append(f"the data was validated without the hand-over cover up and the app shell inert "
                          f"(state at {first['t']} ms: hand-over cover {first['hand']}, inert {first['inert']})")
    hand_up = [e for e in after if e["k"] == "mount:valHandover" and e["n"] > down["n"]]
    hand_down = [e for e in after if e["k"] == "unmount:valHandover" and e["n"] > down["n"]]
    if len(hand_up) != 1 or len(hand_down) != 1:
        faults.append(f"expected one hand-over cover after the self-checks, saw {len(hand_up)} mount(s) and "
                      f"{len(hand_down)} removal(s)")
    else:
        hu = hand_up[0].get("held")
        if not isinstance(hu, dict) or "error" in hu:
            faults.append(f"what was held when the hand-over cover went up was not recorded ({hu!r})")
        elif hu["verdict"] is None or hu["feats"] is not None or hu["findings"]:
            faults.append(f"when the hand-over cover went up no verdict was held, or the data had been validated "
                          f"or painted already: {hu}")
        between = [f for f in frames if down["n"] < f["n"] < hand_down[0]["n"]]
        if not between:
            faults.append("no frame was recorded between the end of the self-checks and the removal of the "
                          "hand-over cover: the check for a frame with no cover examined nothing")
        # The hold, measured to the removal of the cover from the latest instant known to precede its start:
        # the first sampled state that holds the findings (taken after the validation had returned) or, when
        # it follows within a tenth of a second, the first frame that shows the findings under the cover.
        # That frame is the one the drain waits for after the last queued call, and the frame logger's
        # callback, registered a frame ahead of the drain's, runs first in it.
        hold = rep.get("hold")
        shown_at = next((f for f in between if f["findings"] and f["hand"]), None)
        start = first["t"] if first is not None else None
        if start is not None and shown_at is not None and 0 <= shown_at["t"] - start < 100:
            start = shown_at["t"]
        # The frame that counts shows the hand-over cover and no findings, both as its callbacks begin and
        # in the task after it. The validation paints in the task it runs in, so a frame with findings is a
        # frame after it, and that frame can be sequenced ahead of the sampler's first state with findings.
        # Findings in the task after a frame mean that the data was validated inside that frame's callbacks,
        # before the frame was presented, or in a task that was queued ahead of the frame: the wait had gone
        # on without it. A record that was never completed does not count. With no frame at all in the
        # hand-over window the fault above has said so.
        # Neither fault has one cause, and the record cannot tell the causes apart. A frame without the
        # line can also fall between the mount and the turn that writes the line, and it is the only frame
        # ahead of the validation when none is presented after that turn.
        ahead = [] if first is None else [f for f in frames if hand_up[0]["n"] < f["n"] < first["n"]
                                          and f["hand"] and not f["findings"] and f.get("after") is False]
        if first is not None and between and not ahead:
            faults.append(f"no frame showed the hand-over cover, and no findings, between its mount "
                          f"({hand_up[0]['t']} ms) and the first state that holds findings ({first['t']} ms, "
                          f"{first['t'] - hand_up[0]['t']:.0f} ms later): either the queued call ran without "
                          "waiting for a frame, or no frame was presented in the time the drain waits for one "
                          "before it goes on (_scfYield), or the wait ended inside the callbacks of the frame "
                          "it waited for and the data was validated before that frame was presented")
        elif ahead and not any(f.get("says") for f in ahead):
            faults.append(f"{len(ahead)} frame(s) showed the hand-over cover, and no findings, between its mount "
                          f"({hand_up[0]['t']} ms) and the first state that holds findings ({first['t']} ms), "
                          f"the last of them at {ahead[-1]['t']} ms, and none of them showed its line: either "
                          "the line was written after the frame the drain waits for, or no frame was "
                          "presented between the turn that writes the line and the queued call (the call ran "
                          "without waiting for a frame, the drain went on with none presented, or the wait "
                          "ended inside the callbacks of the frame it waited for; _scfYield); the cover is "
                          "empty for as long as the data takes to validate")
        if not isinstance(hold, (int, float)) or hold <= 0:
            faults.append(f"the hold of the hand-over cover could not be read from the app ({hold!r})")
        elif start is not None and hand_down[0]["t"] - start < hold - FIRST_VALIDATION_HOLD_SLACK_MS:
            faults.append(f"the hand-over cover came down {hand_down[0]['t'] - start:.0f} ms after the findings "
                          f"were held, under its hold of {hold} ms: a click made on the cover while the page "
                          "validated reaches the page after that")
        bare = [f for f in between if not f["scrim"] and not f["hand"]]
        if bare:
            faults.append(f"{len(bare)} frame(s) were presented with no cover between the end of the "
                          f"self-checks and the end of the validation (first at {bare[0]['t']} ms)")
    # 3. what the user is left with
    smoke = rep.get("smoke") or []
    failed = [t for t in smoke if not t["passed"]]
    try:
        expected = _expected_smoke_count()
    except Exception as e:  # the suite-size ground truth is reported by the main leg
        expected = None
        faults.append(f"cannot read the suite size ground truth: {e}")
    if expected is not None and len(smoke) != expected:
        faults.append(f"the verdict holds {len(smoke)} checks, the suite has {expected}")
    for t in failed[:10]:
        faults.append(f"self-check failed on the first-validation path: {t['name'][:160]} — {t['detail'][:300]}")
    if len(failed) > 10:
        faults.append(f"… and {len(failed) - 10} more failed self-check(s)")
    if not rep.get("feats"):
        faults.append("no validation results are held after the first validation")
    if rep.get("inert"):
        faults.append("the app shell was left inert")
    if rep.get("valIn") != rep.get("example"):
        faults.append("the Validator text is not the text that was put in")
    if rep.get("resultsText") is not True:
        faults.append("the results held are not those of the text in the Validator")
    if rep.get("feats") and rep.get("blocks") != rep.get("feats"):
        faults.append(f"the pane shows {rep.get('blocks')} feature block(s) for {rep.get('feats')} validated feature(s)")
    if not rep.get("bannerFirst") or (not failed and not rep.get("bannerOk")):
        faults.append("the findings are not painted under the self-check banner")
    if rep.get("notices"):
        faults.append(f"a plain first validation left {rep.get('notices')} notice(s) in the pane "
                      "(a custody breach, an internal error or a deferred report)")
    if not rep.get("translated"):
        if "validated" not in (rep.get("coverText") or ""):
            faults.append("the self-check cover does not say that the data is validated next "
                          f"(cover text: {rep.get('coverText')!r})")
        if not rep.get("handSamples"):
            faults.append("the hand-over cover was never sampled while it was the cover on screen: the check "
                          "of its line examined nothing")
        elif not (rep.get("handText") or "").strip():
            faults.append("the hand-over cover says nothing while it is the cover on screen")
    return faults


# SG-17: the control the gate focuses before the suite runs, as a user's focus would sit on one: the Validator's
# text area, on the tab the suite fronts anyway. Returns its id when it took focus, else null (the gate then fails:
# a focus check that seeded nothing proves nothing).
FOCUS_SEED_JS = """() => {
  showTab(2);
  const c = document.getElementById("valIn");
  if (!c) return null;
  c.focus();
  return document.activeElement === c ? c.id : null;
}"""

# SG-17: where keyboard focus is after the suite returned, and the suite's own record of a focus it could not give back
FOCUS_AFTER_JS = """() => {
  const a = document.activeElement;
  return {id: (a && a.id) || "", tag: a ? a.tagName.toLowerCase() : "", note: runSmokeTests._focusBack || null};
}"""


async def _first_validation_leg(browser_obj, url: str, engine: str) -> tuple[int, list[dict], list[str]]:
    """Fresh page, the bundled example in the Validator, a real click on Run validation.
    Returns (exit code, console records, reason lines): 0 when the order held; 9 when it did not,
    when the click did not reach the button, or when the validation the click queued did not
    finish; 3 when the page never became usable (load, readiness, the button, the record); 6/7 for
    a page exception or console output outside the baseline."""
    context = await browser_obj.new_context(viewport={"width": 1280, "height": 720})
    page = await context.new_page()
    records: list[dict] = []

    def _on_console(msg):
        if msg.type in ("error", "warning"):
            loc = ""
            try:
                l = msg.location or {}
                loc = (l.get("url") or "") + (f":{l['lineNumber']}" if l.get("lineNumber") else "")
            except Exception:
                pass
            records.append({"kind": "console", "type": msg.type, "text": msg.text, "location": loc, "stack": ""})

    def _on_pageerror(exc):
        name = (getattr(exc, "name", "") or "").strip() or "Error"
        message = getattr(exc, "message", None) or str(exc)
        stack = (getattr(exc, "stack", "") or "").strip()
        if engine == "firefox" and not re.search(r"^\s+at ", stack, re.M):
            records.append({"kind": "console", "type": "error", "text": f"{name}: {message}",
                            "location": "", "stack": "", "gecko_report": True})
            return
        records.append({"kind": "pageerror", "type": "pageerror", "text": f"{name}: {message}",
                        "location": "", "stack": stack})

    page.on("console", _on_console)
    page.on("pageerror", _on_pageerror)

    async def _ask(expr, arg=None, what="the page"):
        # Playwright does not time out page.evaluate: a page whose main thread is blocked would
        # hold the gate for ever (see the suite leg above)
        left = max(1.0, deadline - time.monotonic())
        try:
            return await asyncio.wait_for(page.evaluate(expr, arg) if arg is not None else page.evaluate(expr), timeout=left)
        except asyncio.TimeoutError:
            raise TimeoutError(f"{what} did not answer within {bound[0]}s of {bound[1]} (bounded "
                               f"page.evaluate) — the main thread is blocked {bound[2]}")

    # `bound` is set wherever `deadline` is: the seconds allowed, what they are counted from, and where the
    # page is when an answer does not come — the words a timeout under that deadline is reported in
    deadline = time.monotonic() + FIRST_VALIDATION_TIMEOUT_S
    bound = (FIRST_VALIDATION_TIMEOUT_S, "the start of the leg", "while the page is prepared, before any click")
    waiting = False   # True while the validation the click queued is awaited
    try:
        await page.add_init_script(FIRST_VALIDATION_INIT_JS)
        await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        # true at Playwright's first check: a later poll of a string expression would be refused
        # by the app's Content-Security-Policy (see the wait below)
        await page.wait_for_function("typeof runSmokeTests === 'function'", timeout=10_000)
        await _ask("showTab(2)", what="the page, asked to front the Validator tab,")
        await _ask("document.getElementById('valIn').value=exGML[0];syncLineGutter('valIn')",
                   what="the page, asked to take the example text,")
        await _ask(FIRST_VALIDATION_SAMPLER_JS, what="the page, asked to start the sampler,")
        await page.wait_for_timeout(300)
        # the button by its handler, brought into view: a click at coordinates outside the viewport,
        # or on something that lies over the button, reaches nothing
        btn = page.locator('button[onclick="runVal()"]').first
        await btn.scroll_into_view_if_needed(timeout=10_000)
        box = await btn.bounding_box()
        if box is None:
            raise RuntimeError('the Run validation button (button[onclick="runVal()"]) is not visible on the '
                               "Validator tab of a fresh page")
        deadline = time.monotonic() + FIRST_VALIDATION_TIMEOUT_S
        bound = (FIRST_VALIDATION_TIMEOUT_S, "the click", "in the self-checks or in the validation behind them")
        await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        clicked = await _ask(FIRST_VALIDATION_CLICKED_JS, what="the page, asked where the click landed,")
        if clicked["at"] is None or not clicked["hit"]:
            reason = ("the click on Run validation did not reach the button: "
                      + ("no trusted click was seen by the page" if clicked["at"] is None
                         else f"it landed on <{clicked['on']}>"))
            print(f"[X] first validation: {reason}", file=sys.stderr)
            _report_page_messages(records)
            await context.close()
            return 9, records, [reason]
        if not (clicked["queued"] or clicked["armed"] or clicked["running"]):
            reason = ("the click on Run validation queued no validation behind the self-checks and started no "
                      "run: the first validation did not wait")
            print(f"[X] first validation: {reason}", file=sys.stderr)
            _report_page_messages(records)
            await context.close()
            return 9, records, [reason]
        # The end of the first validation is polled with page.evaluate. wait_for_function evaluates
        # its string in the page on every poll, and every poll after the first runs from a page
        # callback, where the app's Content-Security-Policy (no 'unsafe-eval') refuses it.
        waiting = True
        while not await _ask(FIRST_VALIDATION_DONE_JS, what="the page, asked whether the first validation had finished,"):
            if time.monotonic() > deadline:
                raise TimeoutError(
                    f"the self-checks and the validation behind them did not finish within "
                    f"{FIRST_VALIDATION_TIMEOUT_S}s of the click")
            await asyncio.sleep(0.1)
        waiting = False
        await page.wait_for_timeout(500)   # the frames after the hand-over cover has gone
        deadline = time.monotonic() + FIRST_VALIDATION_REPORT_TIMEOUT_S
        bound = (FIRST_VALIDATION_REPORT_TIMEOUT_S, "the end of the first validation",
                 "after the self-checks and the validation had finished")
        rep = await _ask(FIRST_VALIDATION_REPORT_JS, what="the page, asked for its record,")
    except Exception as e:
        reason = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
        reason = reason.splitlines()[0][:300]
        if waiting:
            # the click reached the button and queued the call: what ends here is the first validation
            # itself, not the page's readiness
            rc, reason = 9, f"the first validation did not finish — {reason}"
        else:
            rc, reason = 3, f"the page did not reach a usable state — {reason}"
        print(f"[{'X' if rc == 9 else 'FAIL'}] first validation: {reason}", file=sys.stderr)
        _report_page_messages(records)
        try:
            await asyncio.wait_for(context.close(), timeout=15)
        except Exception:
            pass
        return rc, records, [reason]
    await context.close()

    faults = _first_validation_faults(rep)
    if faults:
        print(f"[X] first validation: {len(faults)} fault(s) on a fresh page's first Run validation click:",
              file=sys.stderr)
        for f in faults:
            print(f"    - {f}", file=sys.stderr)
        _report_page_messages(records)
        return 9, records, faults
    if any(r["kind"] == "pageerror" for r in records):
        reason = "an uncaught page exception occurred on the first-validation page"
        print(f"[X] first validation: {reason}.", file=sys.stderr)
        _report_page_messages(records)
        return 6, records, [reason]
    unexpected, over, under = _console_baseline_breaches(records, engine)
    if unexpected or over or under:
        reason = "console output on the first-validation page deviates from the baseline"
        print(f"[X] first validation: {reason}.", file=sys.stderr)
        lines = [reason]
        for label, seen, cap in over:
            lines.append(f"over baseline: {label} — {seen} occurrence(s), baseline allows {cap}")
        for label, seen, floor in under:
            lines.append(f"under baseline: {label} — {seen} occurrence(s), baseline expects {floor}")
        for e in unexpected[:10]:
            lines.append(f"unlisted [{e['type']}] {e['text'][:150]}")
        for ln in lines[1:]:
            print(f"    {ln}", file=sys.stderr)
        return 7, records, lines
    ev = rep["ev"]
    click = rep["clickAt"]
    up = next(e["t"] for e in ev if e["k"] == "mount:smokeScrim" and e["t"] >= click)
    down = next(e["t"] for e in ev if e["k"] == "unmount:smokeScrim" and e["t"] >= click)
    print(
        f"[OK] first validation: on a fresh page the self-checks ran first (cover up {up - click:.0f} ms after the "
        f"click, {(down - up) / 1000:.1f} s), then the data was validated behind the hand-over cover and painted "
        f"under the banner ({len(rep['smoke'])}/{len(rep['smoke'])} checks, {rep['feats']} feature(s)).",
        file=sys.stderr,
    )
    return 0, records, []


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

    # The XSD leg's schema and validator, settled before a browser starts: the development tree must have both — a
    # missing schema there is exit 10, a missing lxml exit 2 like a missing Playwright — and a snapshot tree ships no
    # reference schema, so there the leg is left out with a note (s201_xsd.snapshot_tree, the test pre-commit asks).
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import s201_xsd
    finally:
        sys.path.pop(0)
    xsd_schema, xsd_skip = None, None
    if not os.path.exists(s201_xsd.xsd_path(REPO_ROOT)):
        if not s201_xsd.snapshot_tree(REPO_ROOT):
            print(f"[X] XSD leg: {s201_xsd.XSD_REL} is missing from the development tree", file=sys.stderr)
            return 10, []
        xsd_skip = f"not run — this snapshot tree ships no reference schema ({s201_xsd.XSD_REL})"
    else:
        try:
            import lxml  # noqa: F401 — the XSD leg's validator
        except ImportError:
            print("[FAIL] lxml not installed (the XSD leg's validator). Run:\n  pip install lxml", file=sys.stderr)
            return 2, []
        try:
            xsd_schema, _xsd_doc = s201_xsd.load(REPO_ROOT)
        except RuntimeError as e:
            print(f"[X] XSD leg: {e}", file=sys.stderr)
            return 10, []

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
            # _rafT's 120ms fallback stall-proofs only rAF waits. 180s is well above the
            # suite's normal runtime; a timeout surfaces as a distinct failure.
            # SG-17: keyboard focus on a control, as a user's would be; the suite must hand it back
            focus_seed = await page.evaluate(FOCUS_SEED_JS)
            results = await asyncio.wait_for(
                page.evaluate("(async () => await runSmokeTests())()"),
                timeout=180,
            )
            # read before the oracle, which drives the Builder and may move focus on its own
            focus_after = await page.evaluate(FOCUS_AFTER_JS)
            # Then the mount oracle (see MOUNT_ORACLE_JS), on the same page: it replaces the Builder's
            # dataset, so it runs after the suite has restored the seeded workspace, never before.
            stage = "oracle"
            oracle_fx, oracle_notes = _oracle_fixtures()
            oracle = await asyncio.wait_for(
                page.evaluate(MOUNT_ORACLE_JS, oracle_fx),
                timeout=MOUNT_ORACLE_TIMEOUT_S,
            )
            # Then the XSD leg (see XSD_EMIT_JS), on the same page: it writes, and changes nothing there.
            stage = "xsd"
            xsd_results, xsd_notes = ([], []) if xsd_schema is None else await _xsd_leg(page, xsd_schema, s201_xsd)
            # Then the first-validation leg, on a page and in a context of its own: the page above has
            # been driven by the suite and by the oracle, and the leg is about the page a user opens.
            # The suite page stays open meanwhile, so what Gecko reports late for it still arrives.
            stage = "first-validation"
            first_rc, _first_records, first_reasons = await asyncio.wait_for(
                _first_validation_leg(browser_obj, url, browser),
                timeout=FIRST_VALIDATION_LEG_TIMEOUT_S,
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
            elif stage == "xsd":
                reason = (f"the XSD leg did not settle within {XSD_LEG_TIMEOUT_S}s for one fixture (bounded page.evaluate)"
                          if isinstance(e, asyncio.TimeoutError) else f"the XSD leg raised {type(e).__name__}: {e}")
            elif stage == "first-validation":
                reason = (f"the first-validation leg did not return within {FIRST_VALIDATION_LEG_TIMEOUT_S}s of its "
                          "start (the bound on the leg as a whole)" if isinstance(e, asyncio.TimeoutError)
                          else f"the first-validation leg raised {type(e).__name__}: {e}")
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

    # What the mount oracle adds to the suite page's Gecko parse reports is read from the oracle's
    # own result: one report for each fixture the import refused as not well-formed, one for each
    # parse the oracle made that failed (badParses — a text that is not well-formed is parsed for the
    # comparison and again for its member census), and one for each fixture whose import
    # report failed on a text that is not well-formed (the report's census parsed it). The XSD leg
    # parses only the fixtures, which are well-formed, and adds none.
    gecko_extra = {}
    if browser == "firefox":
        _ofx = (oracle or {}).get("fixtures") or []
        gecko_extra = {_GECKO_XML_LABEL: sum(1 for r in _ofx if r.get("notRun"))
                       + int((oracle or {}).get("badParses") or 0)
                       + sum(1 for r in _ofx if "not well-formed" in (r.get("reportFailed") or ""))}
    unexpected, over, under = _console_baseline_breaches(console_errors, browser, gecko_extra)
    if unexpected or over or under:
        print(
            "[X] console output deviates from the expected baseline — a green suite cannot be "
            "trusted alongside output nobody has accounted for.",
            file=sys.stderr,
        )
        for label, seen, cap in over:
            print(f"    over baseline: {label} — {seen} occurrence(s), baseline allows {cap}", file=sys.stderr)
        for label, seen, floor in under:
            print(f"    under baseline: {label} — {seen} occurrence(s), baseline expects {floor}", file=sys.stderr)
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
    if xsd_schema is None:
        print(f"[note] XSD leg: {xsd_skip}", file=sys.stderr)
    elif not _report_xsd(xsd_results, xsd_notes):
        return 10, results
    # SG-17: the seeded control holds focus again, and the suite recorded no miss
    if not focus_seed or focus_after.get("id") != focus_seed or focus_after.get("note"):
        where = ("#" + focus_after["id"]) if focus_after.get("id") else ("<" + (focus_after.get("tag") or "nothing") + ">")
        why = ("the gate could not focus #valIn before the run" if not focus_seed
               else f"focus was on #{focus_seed} before the suite and is on {where} after it")
        # the failure names where focus fell, and the suite's own record when it made one
        print(f"[X] focus custody (exit 11): {why}" + (f" — the suite recorded: {focus_after['note']}" if focus_after.get("note") else ""),
              file=sys.stderr)
        return 11, results
    if first_rc != 0:
        # said again here, so that the reason is the last failure line this function writes to stderr, as
        # it is for 6, 7 and 8; main() follows it only with the suite outcome and its diagnosis note
        print(f"[X] first validation (exit {first_rc}): " + (first_reasons[0] if first_reasons else "failed"),
              file=sys.stderr)
        for r in first_reasons[1:10]:
            print(f"    - {r}", file=sys.stderr)
        return first_rc, results
    return 0, results


# Expected console output, and nothing else. Before this existed the gate blocked only on
# `pageerror`, and `_report_page_messages` groups by message TEXT — so the app's own Rule-25
# alarm ("validation modified the validator textarea"), which one smoke invariant emits
# DELIBERATELY to prove the sentinel works, made a REAL breach invisible: a second occurrence
# only bumped the printed count from (x1) to (x2) and the gate still exited 0. Each entry
# carries the reason it is expected; an unlisted message, more of a listed one than the
# baseline allows, or fewer of an exact one than its floor, blocks with exit 7.
#
# `cap` is an upper bound; an entry whose count is exact also has a `floor` (the sixth field), the
# count it must reach, so a count that drops is caught as surely as one that grows — a deliberate
# emission that stops, or a parse the suite no longer makes, is a lock that stopped running. Where
# a count is environment-sensitive there is no floor, and the text says why.
_GECKO_XML_LABEL = "Gecko XML parsing reports for the suite's own malformed or set-aside text"

_CONSOLE_BASELINE = [
    (
        "meta-CSP frame-ancestors note",
        lambda e: "frame-ancestors" in e["text"],
        2,
        "Chromium reports that `frame-ancestors` cannot be enforced from a <meta> CSP. The app "
        "ships its policy that way deliberately — it is a static file with no server to set a "
        "header — so the directive is inert by design, not misconfigured. Chromium says it once per "
        "page load and Gecko not at all, so the entry has a cap and no floor.",
    ),
    (
        "Annex D symbol fetch failures (PORT-1, fixed in pass 677)",
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
        None,
        0,
    ),
    (
        "deliberate Rule-25 invariant-breach emission",
        lambda e: "invariant breach" in e["text"] and "validator textarea" in e["text"],
        1,
        "The data-custody invariant monkey-patches renderAllVal to corrupt valIn mid-run and "
        "asserts the sentinel restores it verbatim and banners. EXACTLY ONE is expected, in either "
        "engine, on every page that runs the suite: cap and floor are 1. A second occurrence is a REAL "
        "custody breach — that is precisely what this baseline exists to surface, so this cap must "
        "not be raised; none means the invariant no longer runs.",
        None,
        1,
    ),
    # ── Firefox only (the fifth field): Gecko error-console categories that _on_pageerror
    # reclassifies as console entries (see there). Chromium reports neither, so neither can
    # match on a Chromium run; the entries are skipped outright for it.
    (
        _GECKO_XML_LABEL,
        lambda e: bool(e.get("gecko_report")) and "/s201_aton_studio.html" in e["text"],
        # the cap: every report the suite makes on purpose, counted below
        16,
        "Gecko reports every DOMParser failure to its error console, naming the page URL; the "
        "suite parses ill-formed fixtures on purpose and re-validates the set-aside comment text "
        "in per-test teardowns (no root element), and the validator answers each with GML-STR-01. "
        # each report the suite makes on purpose, and the count they come to
        "Measured on Firefox 156: exactly 16 per run (12 of the set-aside text, one per teardown "
        "that re-validates it; 1 prefix not bound; 1 declaration not at the start; 1 the result "
        "a quick fix would have written, which is not well-formed and which the fix refuses; 1 the "
        "result a stand-in document fix returns, which applyDocFix refuses). Before the "
        "pass-732 serializer fix the suite added 13 more: the ill-formed quick-fix documents "
        # why the count is exact, both ways
        "themselves, so this count is a detector — an increase that no new teardown accounts for "
        "means some path writes XML the parser rejects, and a decrease a parse the suite no longer "
        "makes: cap and floor are 16. Do not raise it to make a regression fit. "
        "It is the figure of ONE page that runs the suite once: the "
        "first-validation page is held to it as it stands. On the suite page the mount oracle runs "
        "after the suite and adds its own reports, which Gecko delivers after the oracle has returned "
        "(they were lost while the browser was closed straight after the oracle, and arrive now that "
        "it stays open for the XSD and first-validation legs): one for each fixture the import refuses "
        "as not well-formed, one for each text the oracle finds not well-formed, and one for each "
        "fixture whose import report failed on a text that is not well-formed. That allowance is "
        "computed from the oracle's own result where the suite page is judged (_run_gate), not "
        "written here, and applies to the cap and the floor alike.",
        ("firefox",),
        # the floor, the same as the cap: the count is exact
        16,
    ),
    (
        "Gecko downloadable-font sanitizer notes for the bundled OpenSans faces",
        lambda e: bool(e.get("gecko_report")) and "font-family:" in e["text"] and "Annex_D/Fonts/" in e["text"],
        4,
        "Gecko's OpenType sanitizer discards the kern table of Annex_D/Fonts/OpenSans-Regular.ttf and "
        "OpenSans-Bold.ttf ('Too large subtable' then 'Table discarded': two notes per face, four "
        "in all). The faces still load and render; the note is about a table the app does not "
        "rely on. Exact: a fifth note means another face or table went wrong, a third that a face was "
        "not loaded — cap and floor are 4.",
        ("firefox",),
        4,
    ),
]


def _baseline_entries(engine: str):
    """The baseline entries that apply to `engine`, as (label, matcher, cap, floor, why): a fifth field
    names the engines an entry is for (None, or absent: every engine; the Gecko report categories are
    Firefox-only), a sixth its floor (absent: 0)."""
    out = []
    for entry in _CONSOLE_BASELINE:
        label, matcher, cap, why = entry[:4]
        engines = entry[4] if len(entry) > 4 else None
        floor = entry[5] if len(entry) > 5 else 0
        if engines is None or engine in engines:
            out.append((label, matcher, cap, floor, why))
    return out


def _console_baseline_breaches(msgs: list[dict], engine: str = "chromium", extra: dict | None = None):
    """Split console output into (unlisted messages, listed-but-over-cap entries, entries under their floor).

    `extra` adds to the cap, and to the floor of an entry that has one, of the entries it names, for a
    page that does more than run the suite (the suite page also runs the mount oracle); the bound
    reported is the one that was applied.

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
        for label, matcher, _cap, _floor, _why in entries:
            try:
                hit = matcher(e)
            except Exception:
                hit = False
            if hit:
                counts[label] = counts.get(label, 0) + 1
                break
        else:
            unexpected.append(e)
    extra = extra or {}
    over = [
        (label, counts[label], cap + extra.get(label, 0))
        for label, _m, cap, _f, _w in entries
        if counts.get(label, 0) > cap + extra.get(label, 0)
    ]
    under = [
        (label, counts.get(label, 0), floor + extra.get(label, 0))
        for label, _m, _c, floor, _w in entries
        if floor and counts.get(label, 0) < floor + extra.get(label, 0)
    ]
    return unexpected, over, under


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
    # a message holding a character the console cannot write (an em dash in a cp932 console) is written escaped rather
    # than stopping the gate with an encoding error
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
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
            # Exits 6, 7, 8, 9, 10 and 11 (a page exception, the console baseline, the mount oracle, the
            # first-validation leg, the XSD leg, focus custody) still carry a
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
