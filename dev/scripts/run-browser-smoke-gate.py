#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Playwright headless smoke gate runner (Session 23 pass 118).
#
# WHY THIS EXISTS
# ---------------
# The in-app smoke invariants in `s201_aton_studio.html` (`runSmokeTests`)
# (current count: `_COUNT_GROUND_TRUTH["smoke"]` in precommit-check.py — single
# source per Rule 23; was 66 when this runner was written in pass 118 — count
# grew via subsequent passes adding round-trip, determinism, Builder, and
# download-equality tests)
# only fully run in a real browser — they exercise DOMParser, fetch(),
# round-trip parser/generator on bundled exGML samples, validateGMLStructure,
# downloadCatalogXML, etc. Pre-commit's V8 syntax check (pass 117) catches
# structural JS errors but cannot run the smoke tests because they need DOM.
#
# Throughout passes 113-117, the Preview MCP iframe state was unreliable
# (chrome-error://chromewebdata/ stickiness — see HANDOFF "Tooling caveats").
# Pass 118 introduces this Playwright-based runner so the smoke gate becomes
# automatable: any contributor can run `python dev/scripts/run-browser-smoke-
# gate.py` and get a full-suite PASS verdict — same engine the user runs, no
# iframe weirdness.
#
# THREE-LAYER GATE STACK (Rule 11 + Rule 13)
# ------------------------------------------
#   1. precommit-check.py        — fast static (~1s, 17 checks, every commit)
#   2. run-browser-smoke-gate.py — slow runtime (~10s, full smoke suite, before
#                                  push/release; can be wired into CI)
#   3. Manual [Run tests]     — final visual confirmation in any real
#                                  browser tab the user trusts
#
# USAGE
# -----
#   python dev/scripts/run-browser-smoke-gate.py            # default, exit 1 on fail
#   python dev/scripts/run-browser-smoke-gate.py --json     # machine-readable output
#   python dev/scripts/run-browser-smoke-gate.py --port 8090   # pin a port (default: OS-assigned)
#   python dev/scripts/run-browser-smoke-gate.py --verbose  # print every test
#
# DEPENDENCIES (one-time setup)
# -----------------------------
#   pip install playwright
#   playwright install chromium
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
import socket
import socketserver
import sys
import threading
import time
import urllib.request

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


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
SENTINEL_SEED_JS = """(() => {
  const pt = '<geometry><S100:pointProperty><S100:Point gml:id="P.SEN.001" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>1.1000000 2.2000000</gml:pos></S100:Point></S100:pointProperty></geometry>';
  const sentinel = '<?xml version="1.0" encoding="UTF-8"?>\\n<Dataset xmlns="http://www.iho.int/S-201/gml/cs0/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:S100="http://www.iho.int/s100gml/5.0" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="DS.SEN">\\n<members>\\n<LateralBeacon gml:id="SEN.001"><featureName><name>Sentinel Alfa</name></featureName><AtoNNumber>0900</AtoNNumber><child xlink:href="#SEN.002"/><colour>Red</colour><beaconShape>Pile Beacon</beaconShape><categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark>' + pt + '</LateralBeacon>\\n<Topmark gml:id="SEN.002"><parent xlink:href="#SEN.001"/><colour>Red</colour><topmarkDaymarkShape>Cylinder</topmarkDaymarkShape><verticalLength>0.6</verticalLength>' + pt.replace(/SEN\\.001/g, 'SEN.002') + '</Topmark>\\n</members></Dataset>';
  const gi = document.getElementById('gmlIn');
  gi.value = sentinel;
  const oc = window.confirm, oa = window.alert;
  try {
    window.confirm = () => true; window.alert = () => {};
    builderImportFromDrawing();
  } finally { window.confirm = oc; window.alert = oa; }
  // Force the colour-surface MISMATCH: the import mounts a coloured feature and sets
  // _colourUserSet=true (matched); a user sitting on an auto-prefilled coloured mark is instead at
  // _colourUserSet=false with a coloured feature. Seeding false makes the containment lock exercise the
  // _swapBuilderToFeat colour re-derive, so a leaking teardown (or a broken _restoreColourSurface)
  // goes red instead of hiding behind the matched start.
  _colourUserSet = false;
  document.getElementById('valIn').value = sentinel;
  // Leave `_colourUserSet` at its LEAK-REVEALING value. The import above sets it true (the imported
  // beacon carries <colour>Red</colour>), and the containment lock compares end-of-run against
  // start-of-run — so a start of `true` can never observe a false->true leak. That is exactly what hid
  // the leak this seed was written to catch: a pristine page starts false, the restorative
  // `_swapBuilderToFeat` in each test's finally recomputes it to true from the mounted feat's colours,
  // and the gate saw nothing while a real user clicking "Run tests" got a red containment banner.
  // The seeded FEATURE state (the reason this sentinel exists) is untouched by this reset.
  _colourUserSet = false;
})()"""


async def _run_gate(port: int, verbose: bool, expect_src_comments: bool = True) -> tuple[int, list[dict]]:
    """Launch headless Chromium, navigate to the app, await runSmokeTests,
    return (exit_code, test_results).

    expect_src_comments pins the _SRC_COMMENTS_KEPT probe's polarity: the dev file keeps its
    comments (True); the comment-stripped end-user bundle must report False, proving every
    comment-anchored source lint ran in its explicit-skip mode rather than false-failing.
    A mismatch means this harness is pointed at the wrong kind of build."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print(
            "[FAIL] playwright not installed. Run:\n"
            "  pip install playwright\n"
            "  playwright install chromium",
            file=sys.stderr,
        )
        return 2, []

    url = f"http://127.0.0.1:{port}/s201_aton_studio.html"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
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
            console_errors.append(
                {
                    "kind": "pageerror",
                    "type": "pageerror",
                    "text": f"{name}: {message}",
                    "location": "",
                    "stack": (getattr(exc, "stack", "") or "").strip(),
                }
            )

        page.on("console", _on_console)
        page.on("pageerror", _on_pageerror)

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
            # Pin the source-comment probe polarity BEFORE trusting the suite outcome: with the
            # wrong polarity the comment-anchored lints either false-fail (stripped build under
            # the dev expectation) or silently skip (dev build under the stripped expectation).
            probe = await page.evaluate(
                "typeof _SRC_COMMENTS_KEPT === 'boolean' ? _SRC_COMMENTS_KEPT : null"
            )
            if probe is not expect_src_comments:
                await browser.close()
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
            # _rafT's 120ms fallback stall-proofs only rAF waits. 180s is ~15x the
            # suite's normal ~10s runtime; a timeout surfaces as a distinct failure.
            results = await asyncio.wait_for(
                page.evaluate("(async () => await runSmokeTests())()"),
                timeout=180,
            )
        except Exception as e:
            await browser.close()
            # asyncio.TimeoutError IS TimeoutError on 3.11+, and str() of it is EMPTY — the
            # bounded-evaluate path would otherwise print "[FAIL] Playwright error: " with no
            # reason at all, on the one path where the operator has no results to fall back on.
            if isinstance(e, asyncio.TimeoutError):
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
            return 3, []
        await browser.close()

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

    return 0, results


def _report_page_messages(msgs: list[dict], stream=None) -> None:
    """Print EVERY distinct console/page message once, with an occurrence count.

    The previous report printed `console_errors[:10]` verbatim. That defeats the half of
    SG-BLD-1 this exists for: one noisy benign class (headless symbol preload emits
    hundreds of `ERR_INSUFFICIENT_RESOURCES` lines) fills all ten slots and silently
    crowds out every other distinct message, so a genuinely interesting one appears on a
    quiet run and vanishes on a noisy one — which reads as an intermittent regression.
    Grouping makes the flood cost ONE line instead of ten, so there is no reason to cap:
    the output length is bounded by message VARIETY, not volume.

    Note the blocking half of SG-BLD-1 was never broken — `pageerror` filtering has always
    run over the full list, so an uncaught exception still fails the gate no matter how many
    messages precede it. This is an observability fix; the pass/fail contract is unchanged.

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
    lines.append("\n=== S-201 AtoN Studio browser smoke gate (pass 118 runner) ===\n")

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

        exit_code, results = asyncio.run(_run_gate(port, args.verbose))
        if exit_code != 0:
            # Exit 6 (uncaught page exception) still carries a fully populated results list.
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
                        "gate still fails on the page-level error reported above.",
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
