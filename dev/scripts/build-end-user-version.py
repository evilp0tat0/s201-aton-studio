#!/usr/bin/env python3
"""
build-end-user-version.py — regenerate the end-user test-build snapshot.

The end-user build is a disposable snapshot sent to testers for feedback; it is
NOT kept in sync with ongoing dev. Regenerate it (rarely) with this one command
whenever a new test round goes out. It always builds from the CURRENT version.

What it produces in --out:
  s201_aton_studio.html   the app with ALL comments removed (HTML/CSS/JS), the
                          developer "Run tests" button removed, and the ?test=1
                          auto-run neutralised (testers never see QA internals)
  Annex_D/{Symbols,Fonts,portrayal_catalogue.xml}   runtime-only portrayal assets
  lib/leaflet             map library (+ its LICENSE file)
  dev/validator-rules.json   machine-readable rule catalogue — the app's self-test
                          suite (which runs on every "Run validation" click) fetches
                          it; without it every validation shows a red self-test
  Annex_D/Fonts/LICENSE   Apache-2.0 text for the bundled fonts (if --apache-license given)
  start-server.bat/.sh, README.txt

Everything else not needed at runtime is dropped: Annex_D/Rules/,
Annex_D/ColorProfiles/, the rest of dev/, _local/old docs/ (verified never fetched —
only cited in comments/self-tests).

Comment stripping uses a JS/CSS/HTML-aware lexer (a real parser can't be used —
the file uses ES2020 optional chaining). The 17 `<!--` that legitimately remain
are functional (generated SVG/GML output + one comment-stripping regex), never
source notes.

Usage:
  python dev/scripts/build-end-user-version.py \
      --src  s201_aton_studio.html \
      --out  "_local/end user version" \
      --assets-root . \
      --apache-license path/to/apache-2.0.txt

The build then VERIFIES itself by default: it serves --out and runs the app's
full self-test suite in headless Chromium (the same Playwright harness as
run-browser-smoke-gate.py), asserting the suite size matches the pre-commit
ground truth, every test passes, and the _SRC_COMMENTS_KEPT probe reports the
comments stripped (so comment-anchored source lints ran in their explicit-skip
mode instead of false-failing). A tester-visible self-test failure is a BUILD
failure. Skip only with --no-verify — the bundle is then unverified.
"""
import argparse
import os
import shutil
import sys

OPEN = "<script>"
CLOSE = "</script>"
TEST_BTN_LABEL = "Run tests</button>"        # the Validator tab's "Run tests" button (label + closing tag, so the plain words cannot match elsewhere)
TEST_URL_ANCHOR = 'params.get("test")==="1"'

REGEX_PRECEDING_KEYWORDS = {
    "return", "typeof", "instanceof", "in", "of", "new", "delete", "void",
    "do", "else", "yield", "await", "throw", "case", "default",
}


def _preceding_ws_count(out):
    cnt = 0
    k = len(out) - 1
    while k >= 0:
        ch = out[k]
        if ch == "\n":
            break
        if ch == " " or ch == "\t":
            cnt += 1
            k -= 1
            continue
        return -1
    return cnt


class JSStripper:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.n = len(s)
        self.out = []
        self.prev = ""

    def run(self):
        self._scan_code(top=True)
        return "".join(self.out)

    def _regex_allowed(self):
        return self.prev in ("", "op", "rbrace", "kw_expr")

    def _scan_string(self, quote):
        s, n, out = self.s, self.n, self.out
        out.append(quote)
        i = self.i + 1
        while i < n:
            c = s[i]
            if c == "\\":
                out.append(s[i:i + 2]); i += 2; continue
            out.append(c); i += 1
            if c == quote:
                break
        self.i = i; self.prev = "str"

    def _scan_regex(self):
        s, n, out = self.s, self.n, self.out
        out.append("/")
        i = self.i + 1
        in_class = False
        while i < n:
            c = s[i]
            if c == "\\":
                out.append(s[i:i + 2]); i += 2; continue
            if c == "\n":
                break
            if c == "[":
                in_class = True; out.append(c); i += 1; continue
            if c == "]":
                in_class = False; out.append(c); i += 1; continue
            if c == "/" and not in_class:
                out.append(c); i += 1
                while i < n and s[i].isalpha():
                    out.append(s[i]); i += 1
                self.i = i; self.prev = "regex"; return
            out.append(c); i += 1
        self.i = i; self.prev = "regex"

    def _scan_ident(self):
        s, n = self.s, self.n
        j = self.i
        while j < n and (s[j].isalnum() or s[j] == "_" or s[j] == "$"):
            j += 1
        word = s[self.i:j]
        self.out.append(word)
        self.i = j
        self.prev = "kw_expr" if word in REGEX_PRECEDING_KEYWORDS else "ident"

    def _scan_template(self):
        s, n, out = self.s, self.n, self.out
        out.append("`")
        i = self.i + 1
        while i < n:
            c = s[i]
            if c == "\\":
                out.append(s[i:i + 2]); i += 2; continue
            if c == "`":
                out.append(c); i += 1; self.i = i; self.prev = "str"; return
            if c == "$" and i + 1 < n and s[i + 1] == "{":
                out.append("${"); self.i = i + 2; self.prev = "op"
                self._scan_code(top=False)
                if self.i < self.n and self.s[self.i] == "}":
                    out.append("}"); self.i += 1
                i = self.i
                continue
            out.append(c); i += 1
        self.i = i; self.prev = "str"

    def _scan_code(self, top):
        s, out = self.s, self.out
        depth = 0
        while self.i < self.n:
            n = self.n
            i = self.i
            c = s[i]
            nx = s[i + 1] if i + 1 < n else ""

            if c == "}":
                if not top and depth == 0:
                    return
                if depth > 0:
                    depth -= 1
                out.append(c); self.i = i + 1; self.prev = "rbrace"; continue
            if c == "{":
                depth += 1
                out.append(c); self.i = i + 1; self.prev = "op"; continue
            if c in " \t\r\n":
                out.append(c); self.i = i + 1; continue

            if c == "/" and nx == "/":
                pw = _preceding_ws_count(out)
                j = i + 2
                while j < n and s[j] != "\n":
                    j += 1
                if pw >= 0:
                    for _ in range(pw):
                        out.pop()
                    self.i = j + 1 if j < n else j
                else:
                    while out and (out[-1] == " " or out[-1] == "\t"):
                        out.pop()
                    self.i = j
                continue
            if c == "/" and nx == "*":
                end = s.find("*/", i + 2)
                if end == -1:
                    end = n - 2
                after = end + 2
                pw = _preceding_ws_count(out)
                k = after
                while k < n and s[k] in " \t":
                    k += 1
                line_ends = (k >= n or s[k] == "\n")
                if pw >= 0 and line_ends:
                    for _ in range(pw):
                        out.pop()
                    self.i = (k + 1) if (k < n and s[k] == "\n") else k
                else:
                    out.append(" "); self.i = after
                continue

            if c == "/":
                if self._regex_allowed():
                    self._scan_regex()
                else:
                    out.append(c); self.i = i + 1; self.prev = "op"
                continue
            if c == '"' or c == "'":
                self._scan_string(c); continue
            if c == "`":
                self._scan_template(); continue
            if c.isalpha() or c == "_" or c == "$":
                self._scan_ident(); continue
            if c.isdigit():
                out.append(c); self.i = i + 1; self.prev = "num"; continue
            if c == "+" and nx == "+":
                out.append("++"); self.i = i + 2; self.prev = "num"; continue
            if c == "-" and nx == "-":
                out.append("--"); self.i = i + 2; self.prev = "num"; continue
            if c == "." and self.prev == "num":
                out.append("."); self.i = i + 1; self.prev = "num"; continue
            if c == ")":
                out.append(c); self.i = i + 1; self.prev = "rparen"; continue
            if c == "]":
                out.append(c); self.i = i + 1; self.prev = "rbracket"; continue
            out.append(c); self.i = i + 1; self.prev = "op"
        return


class HtmlCssStripper:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.n = len(s)
        self.out = []

    def run(self):
        s, n, out = self.s, self.n, self.out
        while self.i < n:
            i = self.i
            if s[i:i + 6].lower() == "<style" and (i + 6 >= n or not s[i + 6].isalnum()):
                tag_end = s.find(">", i)
                if tag_end == -1:
                    out.append(s[i:]); self.i = n; break
                out.append(s[i:tag_end + 1]); self.i = tag_end + 1
                self._scan_css()
                continue
            if s[i:i + 4] == "<!--":
                end = s.find("-->", i + 4)
                if end == -1:
                    self.i = n; break
                after = end + 3
                pw = _preceding_ws_count(out)
                k = after
                while k < n and s[k] in " \t":
                    k += 1
                line_ends = (k >= n or s[k] == "\n")
                if pw >= 0 and line_ends:
                    for _ in range(pw):
                        out.pop()
                    self.i = (k + 1) if (k < n and s[k] == "\n") else k
                else:
                    self.i = after
                continue
            out.append(s[i]); self.i = i + 1
        return "".join(out)

    def _scan_css(self):
        s, n, out = self.s, self.n, self.out
        while self.i < n:
            i = self.i
            if s[i:i + 8].lower() == "</style>":
                out.append("</style>"); self.i = i + 8; return
            c = s[i]
            if c == '"' or c == "'":
                out.append(c); i += 1
                while i < n:
                    d = s[i]
                    if d == "\\":
                        out.append(s[i:i + 2]); i += 2; continue
                    out.append(d); i += 1
                    if d == c:
                        break
                self.i = i; continue
            if s[i:i + 4].lower() == "url(":
                out.append(s[i:i + 4]); i += 4
                while i < n and s[i] != ")":
                    out.append(s[i]); i += 1
                if i < n:
                    out.append(")"); i += 1
                self.i = i; continue
            if c == "/" and i + 1 < n and s[i + 1] == "*":
                end = s.find("*/", i + 2)
                if end == -1:
                    end = n - 2
                after = end + 2
                pw = _preceding_ws_count(out)
                k = after
                while k < n and s[k] in " \t":
                    k += 1
                line_ends = (k >= n or s[k] == "\n")
                if pw >= 0 and line_ends:
                    for _ in range(pw):
                        out.pop()
                    self.i = (k + 1) if (k < n and s[k] == "\n") else k
                else:
                    out.append(" "); self.i = after
                continue
            out.append(c); self.i = i + 1
        return


def strip_comments(text):
    a = text.index(OPEN)
    b = text.index(CLOSE)
    assert a < b
    pre = text[:a]
    js = text[a + len(OPEN):b]
    tail = text[b:]
    return HtmlCssStripper(pre).run() + OPEN + JSStripper(js).run() + HtmlCssStripper(tail).run()


def remove_test_button(html):
    idx = html.find(TEST_BTN_LABEL)
    if idx == -1:
        raise SystemExit("FATAL: could not find the 'Run tests' button to remove — anchor changed?")
    if html.find(TEST_BTN_LABEL, idx + 1) != -1:
        raise SystemExit("FATAL: 'Run tests' appears more than once after comment strip — refusing to guess.")
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
    "Run validation" must be green. Any failure (including Playwright missing) fails the
    build; --no-verify is the only bypass.

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
                "FATAL: bundle verify could not run the self-test suite (see message above). "
                "Use --no-verify only if you accept shipping an UNVERIFIED bundle."
            )
        size_err = gate._assert_suite_size(results)
        if size_err:
            raise SystemExit(f"FATAL: bundle verify: {size_err}")
        failed = [t for t in results if not t.get("passed")]
        if failed:
            for t in failed:
                print(f"  [FAIL] {t.get('name')} — {t.get('detail') or 'failed'}", file=sys.stderr)
            raise SystemExit(
                f"FATAL: bundle verify: {len(failed)} self-test(s) failed in the built bundle — "
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

    html = strip_comments(text)
    if strip_comments(html) != html:
        raise SystemExit("FATAL: idempotence check failed — comments may remain.")
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
    # tracked Apache-2.0 text ships with the fonts (Apache-2.0 §4); --apache-license may overwrite it below
    copytree_files(os.path.join(ad, "Fonts"), os.path.join(out, "Annex_D", "Fonts"), names={"LICENSE"})
    shutil.copy2(os.path.join(ad, "portrayal_catalogue.xml"), os.path.join(out, "Annex_D", "portrayal_catalogue.xml"))
    copytree_files(os.path.join(root, "lib", "leaflet"), os.path.join(out, "lib", "leaflet"),
                   names={"leaflet.js", "leaflet.css", "LICENSE"})
    # machine-readable rule catalogue — the self-test suite (auto-run on every "Run validation")
    # fetches dev/validator-rules.json and hard-fails on a 404, so a bundle without it shows a red
    # self-test banner on every validation; ship the current copy (it must match the app's RULES,
    # which the verify step's suite run asserts)
    vr = os.path.join(root, "dev", "validator-rules.json")
    if not os.path.isfile(vr):
        raise SystemExit("FATAL: dev/validator-rules.json not found under --assets-root — "
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
    print(f"   font LICENSE  : {'added (Apache-2.0)' if a.apache_license else 'NOT added (--apache-license not given)'}")

    if a.no_verify:
        print("   self-tests    : SKIPPED (--no-verify) — the bundle is UNVERIFIED")
    else:
        n_pass = verify_bundle(out)
        print(f"   self-tests    : all {n_pass} passed in the built bundle "
              f"(headless Chromium; source-comment probe reports stripped)")


if __name__ == "__main__":
    main()
