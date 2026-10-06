#!/usr/bin/env python3
"""
build-end-user-version.py — regenerate the end-user test-build snapshot.

The end-user build is a disposable snapshot sent to testers for feedback; it is
NOT kept in sync with ongoing dev. Regenerate it (rarely) with this one command
whenever a new test round goes out. It always builds from the CURRENT version.

What it produces in --out:
  s201_aton_studio.html   the app with ALL comments removed (HTML/CSS/JS), the
                          developer "Run tests" button removed, the ?test=1
                          auto-run neutralised (testers never see QA internals),
                          and an IHO / IALA portrayal credit injected next to the
                          version badge
  Annex_D/Symbols/        the symbol library (*.svg + svgStyle.css)
  Annex_D/Fonts/          the four *.ttf fonts + the tracked LICENSE (Apache-2.0
                          notice header + full licence text)
  Annex_D/portrayal_catalogue.xml
  lib/leaflet/            leaflet.js, leaflet.css + LICENSE (optional map layer)
  dev/validator-rules.json   machine-readable rule catalogue — the app's self-test
                          suite (which runs before a session's first validation) fetches
                          it; without it every validation shows a red self-test
  start-server.bat/.sh    copied from --assets-root when present
  README.txt, NOTICE.txt  written from the templates in this script

Everything else is dropped: Annex_D/Rules/ and Annex_D/ColorProfiles/ (the app
never fetches them — the XSL dispatch is ported to JS and the colour profile to
CSS; both are only cited in comments/self-tests), the rest of dev/, and all
documentation.

Comment stripping uses a JS/CSS/HTML-aware lexer (a real parser can't be used —
the file uses ES2020 optional chaining). The `<!--` occurrences that remain
(about two dozen) are functional — generated SVG / GML / catalogue output, the
app's own comment-stripping regex and self-test fixtures — never source notes.

Usage:
  python dev/scripts/build-end-user-version.py \
      --src  s201_aton_studio.html \
      --out  "_local/end user version" \
      --assets-root .

--apache-license <path> overwrites Annex_D/Fonts/LICENSE with FONT_LICENSE_HEADER
+ the given licence text. Do NOT pass it for a rebuild: the tracked
Annex_D/Fonts/LICENSE already carries exactly that header and text, so the flag
only re-creates what the copy step already shipped.

The build then VERIFIES itself by default: it serves --out and runs the app's
full self-test suite in headless Chromium (the same Playwright harness as
run-browser-smoke-gate.py), asserting the suite size matches the pre-commit
ground truth, every test passes, and the _SRC_COMMENTS_KEPT probe reports the
comments stripped (so comment-anchored source lints ran in their explicit-skip
mode instead of false-failing), and the gate's other legs (its header names
them; the XSD leg needs lxml and validates against this development tree's
S-201 2.0.0 schema) pass on the bundle. A tester-visible self-test failure
is a BUILD failure. Skip only with --no-verify — the bundle is then unverified.
"""
import argparse
import os
import shutil
import sys

# The lexer that removes the comments is shared with code_notes.py (pre-commit check #22), so the two never
# disagree about what is a comment; the script's own directory is put on the import path for it.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from source_scan import CLOSE, strip_comments  # noqa: E402  (the path is set on the line above)

TEST_BTN_LABEL = "Run tests</button>"        # the Validator tab's "Run tests" button (label + closing tag, so the plain words cannot match elsewhere)
TEST_URL_ANCHOR = 'params.get("test")==="1"'


def remove_test_button(html):
    idx = html.find(TEST_BTN_LABEL)
    # the button must be found exactly once: removing a guess could cut the wrong markup (messages in ASCII, which every
    # console can print)
    if idx == -1:
        raise SystemExit("FATAL: could not find the 'Run tests' button to remove - anchor changed?")
    if html.find(TEST_BTN_LABEL, idx + 1) != -1:
        raise SystemExit("FATAL: 'Run tests' appears more than once after comment strip - refusing to guess.")
    start = html.rfind("<button", 0, idx)
    end = html.find("</button>", idx)
    if start == -1 or end == -1:
        raise SystemExit("FATAL: could not bound the test button element.")
    end += len("</button>")
    # also swallow leading indentation + trailing newline so no blank line is left
    ls = start
    while ls > 0 and html[ls - 1] in " \t":
        ls -= 1
    te = end
    if te < len(html) and html[te] == "\n":
        te += 1
    return html[:ls] + html[te:]


def neutralize_test_url(html):
    if html.count(TEST_URL_ANCHOR) != 1:
        raise SystemExit(f"FATAL: expected exactly 1 '{TEST_URL_ANCHOR}', found {html.count(TEST_URL_ANCHOR)}.")
    return html.replace(TEST_URL_ANCHOR, "false")


# --- IHO / IALA attribution for the reproduced Annex D portrayal library ---
# Wording follows the IHO standard acknowledgement clauses (non-endorsement +
# not-verified + no-logo). It credits the source and copyright; it does NOT
# claim an IHO reproduction permission (that is the distributor's to obtain).
IHO_CREDIT_SHORT = "Portrayal: © IHO / IALA (S-201 Annex D)"
IHO_CREDIT_TITLE = (
    "Portrayal symbols, fonts and catalogue are reproduced from Annex D of the "
    "IHO/IALA S-201 Product Specification. © International Hydrographic "
    "Organization (IHO) / IALA. Incorporation of IHO material does not imply IHO "
    "endorsement of this product; the IHO has not verified this reproduction and "
    "accepts no responsibility for its accuracy."
)
IHO_ANCHOR = 'id="appVersionBadge"'

NOTICE = """S-201 AtoN Studio - Attribution & Acknowledgements
===================================================

PORTRAYAL LIBRARY (IHO / IALA)
------------------------------
This software reproduces the official portrayal symbols, fonts and Portrayal
Catalogue from Annex D of the IHO/IALA S-201 Product Specification (Aids to
Navigation), found in the Annex_D/ folder.

This material is copyright of the International Hydrographic Organization (IHO)
and the International Association of Marine Aids to Navigation and Lighthouse
Authorities (IALA).

  - The incorporation of material sourced from the IHO shall not be construed as
    constituting an endorsement by the IHO of this product.
  - This product has not been checked by the IHO, and the IHO takes no
    responsibility for the accuracy of the reproduction.
  - The IHO logo and other IHO identifiers are not used in this product.

Reproduction of IHO copyright material may require prior written permission from
the IHO; obtaining any permission required for your distribution is the
responsibility of the distributor.

FONTS
-----
Droid Sans, Droid Sans Bold, Open Sans and Open Sans Bold are licensed under the
Apache License, Version 2.0 - see Annex_D/Fonts/LICENSE.

BUNDLED LIBRARIES
-----------------
Leaflet - BSD 2-Clause License - see lib/leaflet/LICENSE
"""


def inject_iho_credit(html):
    at = html.find(IHO_ANCHOR)
    if at == -1:
        raise SystemExit(f"FATAL: could not find {IHO_ANCHOR} to attach the IHO credit.")
    close = html.find("</span>", at)
    if close == -1:
        raise SystemExit("FATAL: could not find the end of the version-badge span.")
    insert_at = close + len("</span>")
    credit = (
        '<span class="iho-credit" title="' + IHO_CREDIT_TITLE + '"'
        ' style="font-size:10px;color:var(--muted);margin-left:8px;letter-spacing:.2px">'
        + IHO_CREDIT_SHORT + '</span>'
    )
    return html[:insert_at] + credit + html[insert_at:]


README = """S-201 AtoN Studio
=================

An offline, in-browser tool for authoring, validating and drawing IHO/IALA
S-201 Aids-to-Navigation GML datasets.


HOW TO RUN
----------
Windows    : double-click  start-server.bat
Mac / Linux: run  ./start-server.sh
             (or, in this folder:  python3 -m http.server 8080 )

Then open in your browser:

    http://localhost:8080/s201_aton_studio.html

The app must be served over http:// - a small local server is enough.
Opening the .html file directly (file://) makes the browser block loading of
the official Annex D symbol library, so the drawing falls back to simplified
symbols. Parsing, building and validation still work either way.

Everything runs 100% in your browser. No internet connection is required and
no data ever leaves your computer. (The optional base-map layer is OFF by
default; only turning it on makes any network request.)

Requires Python 3 (recommended) or Node.js installed, to run the local server.


WHAT'S IN THIS FOLDER
---------------------
s201_aton_studio.html   the application (single file)
Annex_D/                official IHO/IALA S-201 symbols, fonts and catalogue
lib/leaflet/            Leaflet map library (optional map layer)
dev/                    machine-readable catalogue of the validation rules
                        (read by the app's built-in self-checks)
start-server.bat        local-server launcher for Windows
start-server.sh         local-server launcher for Mac / Linux
NOTICE.txt              attribution & acknowledgements (IHO/IALA, fonts, libs)


CREDITS
-------
The portrayal symbols, fonts and catalogue in Annex_D/ are reproduced from
Annex D of the IHO/IALA S-201 Product Specification and are (c) IHO / IALA.
Incorporation of IHO material does not imply IHO endorsement, and the IHO has
not verified this reproduction. See NOTICE.txt for the full acknowledgement.
"""

FONT_LICENSE_HEADER = (
    "The fonts bundled in this folder (Droid Sans, Droid Sans Bold, Open Sans,\n"
    "Open Sans Bold) are licensed under the Apache License, Version 2.0. The full\n"
    "license text is reproduced below.\n"
    "\n"
    "================================================================================\n\n"
)


def _load_smoke_gate_module():
    """importlib-load run-browser-smoke-gate.py (same folder; the hyphenated filename rules out a
    normal import). It is import-safe (main() behind a __main__ guard). precommit-check.py is NEVER
    imported here — it executes its entire gate and sys.exit()s at module top level."""
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run-browser-smoke-gate.py")
    spec = importlib.util.spec_from_file_location("smoke_gate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verify_bundle(out_dir):
    """Serve the built bundle and run the app's full self-test suite in headless Chromium.

    This is the only harness that exercises the suite in the exact form testers run it
    (comment-stripped): the _SRC_COMMENTS_KEPT probe must report False (comment-anchored
    source lints skip explicitly instead of false-failing), the suite size must match the
    pre-commit ground truth, and every test must pass — the same banner a tester sees on
    "Run validation" must be green. The gate's other legs run too (its header names them): the XSD
    leg validates the GML the bundle writes against the S-201 2.0.0 schema of this development tree
    (s201_xsd.py; lxml required), and the first-validation leg is the one that matters most here —
    in the bundle, which has no Run tests button, a session's first validation is the only way the
    suite ever runs. Any
    failure (including Playwright or lxml missing) fails the build; --no-verify is the only
    bypass.

    Returns the number of passed tests."""
    import asyncio
    gate = _load_smoke_gate_module()
    prev_cwd = os.getcwd()
    server, port = gate._start_http_server(0, serve_root=out_dir)
    try:
        url = f"http://127.0.0.1:{port}/s201_aton_studio.html"
        ident_err = gate._assert_served_app_is_this_repo(
            url, local_path=os.path.join(out_dir, "s201_aton_studio.html")
        )
        if ident_err:
            raise SystemExit(f"FATAL: bundle verify identity check failed: {ident_err}")
        exit_code, results = asyncio.run(
            gate._run_gate(port, verbose=False, expect_src_comments=False)
        )
        if exit_code != 0:
            raise SystemExit(
                f"FATAL: bundle verify: the browser gate failed with exit {exit_code} (see message above). "
                "Use --no-verify only if you accept shipping an UNVERIFIED bundle."
            )
        size_err = gate._assert_suite_size(results)
        if size_err:
            raise SystemExit(f"FATAL: bundle verify: {size_err}")
        # each failing self-test is named with its detail, then the build stops: testers must never get a bundle whose
        # banner is red
        failed = [t for t in results if not t.get("passed")]
        if failed:
            for t in failed:
                print(f"  [FAIL] {t.get('name')} - {t.get('detail') or 'failed'}", file=sys.stderr)
            raise SystemExit(
                f"FATAL: bundle verify: {len(failed)} self-test(s) failed in the built bundle - "
                "testers would see a red self-test banner on every validation. Not shipping."
            )
        return len(results)
    finally:
        server.shutdown()
        server.server_close()
        os.chdir(prev_cwd)


def copytree_files(src_dir, dst_dir, names=None, pattern=None):
    os.makedirs(dst_dir, exist_ok=True)
    for fn in sorted(os.listdir(src_dir)):
        sp = os.path.join(src_dir, fn)
        if not os.path.isfile(sp):
            continue
        if names is not None and fn not in names:
            continue
        if pattern is not None and not fn.endswith(pattern):
            continue
        shutil.copy2(sp, os.path.join(dst_dir, fn))


def main():
    # a path or a test's name the console cannot write is shown escaped rather than stopping the build (a cp932 or
    # cp1252 console, not only UTF-8); the build's own messages are ASCII
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Regenerate the end-user test-build snapshot.")
    ap.add_argument("--src", required=True, help="source s201_aton_studio.html (the CURRENT version)")
    ap.add_argument("--out", required=True, help="output bundle directory")
    ap.add_argument("--assets-root", required=True, help="root containing Annex_D/, lib/, start-server.*")
    ap.add_argument("--apache-license", default=None, help="path to Apache-2.0 license text for the fonts")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip the post-build self-test verification (the bundle is then UNVERIFIED)")
    a = ap.parse_args()

    src = os.path.abspath(a.src)
    out = os.path.abspath(a.out)
    root = os.path.abspath(a.assets_root)

    with open(src, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert text.count(CLOSE) == 1, f"expected 1 </script>, got {text.count(CLOSE)}"

    # the comments are stripped, and stripping again must change nothing: a second pass that finds more means the lexer
    # missed some
    html = strip_comments(text)
    if strip_comments(html) != html:
        raise SystemExit("FATAL: idempotence check failed - comments may remain.")
    html = remove_test_button(html)
    html = neutralize_test_url(html)
    html = inject_iho_credit(html)

    # sanity gates
    assert html.startswith("<!DOCTYPE html>"), "lost DOCTYPE"
    assert html.rstrip().endswith("</html>"), "lost closing </html>"
    assert TEST_BTN_LABEL not in html, "test button still present"
    assert 'if(false){' in html or 'if (false)' in html, "test-url not neutralised"
    assert 'class="iho-credit"' in html, "IHO credit not injected"

    # (re)create output
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "s201_aton_studio.html"), "w", encoding="utf-8", newline="") as f:
        f.write(html)

    # runtime assets only
    ad = os.path.join(root, "Annex_D")
    copytree_files(os.path.join(ad, "Symbols"), os.path.join(out, "Annex_D", "Symbols"))          # *.svg + svgStyle.css
    copytree_files(os.path.join(ad, "Fonts"), os.path.join(out, "Annex_D", "Fonts"), pattern=".ttf")
    # the tracked LICENSE (Apache-2.0 notice header + licence text, per Apache-2.0 §4) ships with the fonts; --apache-license would only overwrite it with the same header (see the module docstring)
    copytree_files(os.path.join(ad, "Fonts"), os.path.join(out, "Annex_D", "Fonts"), names={"LICENSE"})
    shutil.copy2(os.path.join(ad, "portrayal_catalogue.xml"), os.path.join(out, "Annex_D", "portrayal_catalogue.xml"))
    copytree_files(os.path.join(root, "lib", "leaflet"), os.path.join(out, "lib", "leaflet"),
                   names={"leaflet.js", "leaflet.css", "LICENSE"})
    # machine-readable rule catalogue — the self-test suite (run before a session's first validation)
    # fetches dev/validator-rules.json and hard-fails on a 404, so a bundle without it shows a red
    # self-test banner on every validation; ship the current copy (it must match the app's RULES,
    # which the verify step's suite run asserts)
    vr = os.path.join(root, "dev", "validator-rules.json")
    if not os.path.isfile(vr):
        raise SystemExit("FATAL: dev/validator-rules.json not found under --assets-root - "
                         "cannot build a self-test-clean bundle.")
    os.makedirs(os.path.join(out, "dev"), exist_ok=True)
    shutil.copy2(vr, os.path.join(out, "dev", "validator-rules.json"))
    for launcher in ("start-server.bat", "start-server.sh"):
        sp = os.path.join(root, launcher)
        if os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(out, launcher))

    with open(os.path.join(out, "README.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(README)

    with open(os.path.join(out, "NOTICE.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(NOTICE)

    if a.apache_license:
        with open(a.apache_license, "r", encoding="utf-8") as f:
            lic = f.read()
        with open(os.path.join(out, "Annex_D", "Fonts", "LICENSE"), "w", encoding="utf-8", newline="\n") as f:
            f.write(FONT_LICENSE_HEADER + lic)

    n_sym = len([x for x in os.listdir(os.path.join(out, "Annex_D", "Symbols")) if x.endswith(".svg")])
    n_files = sum(len(fs) for _, _, fs in os.walk(out))
    print(f"[OK] built end-user bundle -> {out}")
    print(f"   source        : {src}")
    print(f"   html          : {len(text):,} -> {len(html):,} bytes ({100*len(html)/len(text):.1f}%)")
    print(f"   symbols       : {n_sym} svg")
    print(f"   total files   : {n_files}")
    print(f"   test button   : removed;  ?test=1 auto-run: neutralised")
    print(f"   IHO credit    : injected in topbar; NOTICE.txt + README credits written")
    # the fonts' licence and whether --apache-license replaced it, then the self-tests' verdict (ASCII, as every message)
    print("   font LICENSE  : copied from the tracked Annex_D/Fonts/LICENSE (Apache-2.0 with the bundle header)" + (" - replaced by --apache-license" if a.apache_license else ""))

    if a.no_verify:
        print("   self-tests    : SKIPPED (--no-verify) - the bundle is UNVERIFIED")
    else:
        n_pass = verify_bundle(out)
        print(f"   self-tests    : all {n_pass} passed in the built bundle "
              f"(headless Chromium; source-comment probe reports stripped)")


if __name__ == "__main__":
    main()
