#!/usr/bin/env python3
"""S-201 AtoN Studio — pre-commit smoke gate (Rule 11 + Rule 13 enforcement).

Lightweight static checks that run in a few seconds before each git commit.
They verify the most common ship-breakers without requiring a browser.
Numbers below are the `check #N` citations used throughout this file and the
docs; the registration order at the foot of the file differs only in that
checks 2 + 4 share one function (`check_foundational_rules_json_shape`), the
const-length half of check 2 is its own function, and both are registered
before check 3.

  1. APP_VERSION in the JS matches the preface "Current: X.Y.Z" line, the
     preface "current as of pass N / vX.Y.Z" phrase, and (development tree
     only) the HANDOFF § 15 Live-state `Current pass` + `APP_VERSION` footer
     rows — version drift between code and prose is the most common
     atomic-delivery failure.
  2. dev/foundational-rules.json parses as valid JSON with N entries where N
     matches the FOUNDATIONAL_RULES const length in the HTML.
  3. The 'across N passes' phrasings in HANDOFF.md / README.md / dev/README.md
     agree with each other (pass-count drift between docs).
  4. dev/foundational-rules.json passes a shape check (every entry has
     number/name/theme/summary/addedPass; numbers are 1..N in order).
  5. dev/validator-rules.json is in sync with the in-app RULES array (runs
     generate-validator-rules-json.py in --check mode — catches a rule edited
     in the HTML without the JSON mirror being regenerated).
  6. The inline <script> in s201_aton_studio.html parses as valid JS (V8 via
     py-mini-racer — the engine browsers run). If py-mini-racer is absent the
     check raises SkippedCheck, which blocks the gate: a check that could not
     run is not a pass.
  7. Intra-section pass-count staleness in HANDOFF.md: check #3's `max()`
     masks a stale heading such as `### ... across the 109 passes` when a
     higher count exists elsewhere in the file, so this check walks every
     heading and flags any "across N passes" / "Over N passes" whose N differs
     from the document's max — unless the heading is marked historical
     (`(historical — as of pass N)` or a pattern in
     `_INTENTIONAL_HISTORICAL_HEADING_PATTERNS`).
  8. Function-reference anchor freshness in the HANDOFF.md "Key functions"
     tables: every backticked-function row's claimed line is compared with the
     actual `^function NAME(` declaration in the HTML; drift beyond ±2 fails.
     Rows with a ~ prefix (documented approximate) or a range (NN-MM) are
     skipped. Exists because the manual doc refresh tended to cover only the
     parser/generator/validator anchors while the rest drifted by hundreds of
     lines.
  9. Constants-table anchor freshness in HANDOFF.md: same as #8 for the
     Constants table — single-name, single-line rows are checked against
     `^const NAME` within ±2; aggregate names (joined with /) and ranges are
     skipped.
 10. Sample-data file existence: every fixture named in the `dev/sample-data/`
     table of dev/README.md exists on disk (a fixture renamed or deleted
     without the README being updated).
 11. Source-file tour anchor freshness: Part A walks the HANDOFF.md
     "Source-file tour" table's `` `<snippet>` (line ~NNN) `` anchors, Part B
     any `| NNN | `<snippet>` |` rows in CLAUDE.md, Part C `` `<snippet>` ...
     (HTML line NNN) `` prose anchors anywhere in HANDOFF.md, and Part D
     `[s201_aton_studio.html:NNN]` markdown links in CLAUDE.md. Each snippet
     is resolved to a top-level `^const`/`^let`/`^var` or `^[async ]function`
     in the HTML; drift beyond ±10 (approximate `~` refs) or ±2 (exact refs)
     fails. Identifiers not found at top level (prose, methods, parameters)
     are silently skipped — a self-correcting false-positive guard. Closes
     the gap #8/#9 leave: they scan only the two dedicated tables. (CLAUDE.md
     currently anchors to symbols, not line numbers, so Parts B + D find
     nothing there; they remain as guards.)
 12. Count-phrase freshness in the HTML <script> + preface and in
     dev/scripts/*.py: known count-phrase patterns (`N deterministic ...`,
     `1 of N tests`, `N checks, every commit`, `N per-feature`, `N structural
     rules`, `= N total`, ...) must match ground truth. Ground truth is the
     module-level `_COUNT_GROUND_TRUTH` dict (change it when the suite / rule
     corpus / asset set changes); the precommit count is self-derived from
     `re.findall(r"^check\\(", __file__)` so it auto-bumps when a check is
     added. Every pattern requires a number AND a context noun, so bare
     numbers never match.
 13. Doc count-phrase freshness in .md surfaces (Rule 23): scans CLAUDE.md /
     README.md / dev/README.md / dev/HANDOFF.md (clipped before § 15) for
     count-phrases (gate results `N/N`, `N-check`, smoke-invariant /
     validator-rule / foundational-rule / ATYPES / Annex D corpus sizes, ...)
     against the same ground truth, then pins the § 15 Live-state footer rows
     (file size, rule counts, smoke count, foundational count) and rejects any
     other restatement of the current line count or an `APP_VERSION` value.
 14. Rule-21 narrative-residue purity in s201_aton_studio.html: rejects
     per-pass-narrative residue patterns (pass-N / Agent-X / audit-finding /
     quoted-user-dialogue markers) in the app source — that history belongs
     in dev/CHANGELOG.md.
 15. csv_to_s201.py output conformance self-test: runs the converter against
     its bundled self-test CSV (dev/scripts/csv_to_s201_selftest.csv) and
     asserts the emitted GML keeps its conformance guarantees (FC-mandatory
     attributes present, no extraneous DII fields, no child featureName).
 16. Bundled-asset count/version phrase freshness (Rule 23): doc phrases
     stating bundled-asset facts must match the assets on disk — `Leaflet
     X.Y.Z` vs the lib/leaflet/leaflet.js banner; `N SVG files/symbols` vs
     Annex_D/Symbols/*.svg; `N XSL` vs Annex_D/Rules/*.xsl; `N codes` vs the
     S-62 producer-code CSV data-row count.
 17. pdf-extracts integrity manifest (Rule 5/8 — the citation trust anchor):
     every file in dev/pdf-extracts/ must match dev/pdf-extracts/MANIFEST.sha256
     (runs generate-pdf-extracts-manifest.py --check), so a silent
     re-extraction can no longer invalidate the cited line numbers.

Snapshot-tree mode:
  dev/scripts/build-public-snapshot.py cuts a redistributable tree without the
  development documentation and stamps dev/SNAPSHOT.json. When that marker is
  present AND dev/HANDOFF.md is absent, the checks anchored to those documents
  (3, 7, 8, 9, 10, 11, 13 and the HANDOFF half of 1; 17 when the extracts were
  not shipped) are reported as [n/a ] and do not block; everything else runs
  unchanged. The marker cannot downgrade a tree that has dev/HANDOFF.md.

Exit code:
  0 = all checks pass — commit proceeds
  1 = one or more checks failed — commit blocked

Usage:
  Manual:        python dev/scripts/precommit-check.py
  As git hook:   .git/hooks/pre-commit calls this (see setup-precommit.sh)

Per Rule 11 (Smoke-test-or-die) the FULL smoke gate (the runSmokeTests
suite; size single-sourced in `_COUNT_GROUND_TRUTH['smoke']` below) runs in
the browser via the Validator tab's "Run tests" button (also runnable
headless via `dev/scripts/run-browser-smoke-gate.py`). This script catches
the cheap-to-detect drift that doesn't need a browser; the full gate is
still required before declaring a pass complete.
"""
import re
import sys
import json
import os

# Force UTF-8 on stdout/stderr: check messages carry non-ASCII (em-dashes, ±,
# →), which raises UnicodeEncodeError on Windows consoles that default to
# cp1252. reconfigure() is Py3.7+; the guards keep the script working on older
# Pythons + non-TTY pipelines.
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

# Walk up from script location to find the project root
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, "..", ".."))

HTML = os.path.join(PROJECT_ROOT, "s201_aton_studio.html")
HANDOFF = os.path.join(PROJECT_ROOT, "dev", "HANDOFF.md")
README = os.path.join(PROJECT_ROOT, "README.md")
DEV_README = os.path.join(PROJECT_ROOT, "dev", "README.md")
FRULES_JSON = os.path.join(PROJECT_ROOT, "dev", "foundational-rules.json")
VRULES_JSON = os.path.join(PROJECT_ROOT, "dev", "validator-rules.json")
VRULES_GEN_SCRIPT = os.path.join(PROJECT_ROOT, "dev", "scripts", "generate-validator-rules-json.py")

# Snapshot-tree mode. `dev/scripts/build-public-snapshot.py` cuts a
# redistributable tree that carries the app, its runtime assets, the machine-
# readable rule corpora and these scripts, but NOT the development
# documentation (dev/HANDOFF.md, dev/README.md, CLAUDE.md, dev/CHANGELOG.md),
# and stamps `dev/SNAPSHOT.json` (provenance: source repo + commit + version).
# In such a tree the doc-anchored checks have nothing to read; they report as
# NOT APPLICABLE (listed, not counted as a pass, not blocking) so the code-
# anchored checks still gate the snapshot. The marker alone never downgrades
# the development tree: while dev/HANDOFF.md is present every check runs
# exactly as before.
SNAPSHOT_MARKER = os.path.join(PROJECT_ROOT, "dev", "SNAPSHOT.json")


def _snapshot_tree():
    return os.path.isfile(SNAPSHOT_MARKER) and not os.path.isfile(HANDOFF)


class NotApplicable(Exception):
    """A check whose subject is deliberately absent from a snapshot tree.

    Distinct from SkippedCheck: a skip is a check that SHOULD have run and
    could not (missing tool) — it blocks. Not-applicable is a check whose
    input files are not shipped in a snapshot tree by design (the development
    docs); it is reported and does not block. Raised only when
    `_snapshot_tree()` holds, so it cannot fire in the development tree."""


def _needs_dev_docs(*names):
    """Raise NotApplicable in a snapshot tree for a check anchored to the
    development documentation named in `names`."""
    if _snapshot_tree():
        raise NotApplicable("snapshot tree — " + " + ".join(names) + " not shipped")

failures = []
passes = []
skips = []
not_applicable = []


class SkippedCheck(Exception):
    """A check that could not RUN (missing optional dependency, unavailable tool).

    A skip is not a pass. Before this existed, `check_inline_script_js_syntax`
    printed a "[skip]" notice and `return`ed, and `check()` — which counted any
    function that returned without raising as a pass — appended it to `passes`.
    The gate then printed an all-passed N/N summary while the V8 syntax check
    had never executed. That is precisely the Rule-9 shape (absence read as
    validity) applied to the gate itself, and it is worse here than in a
    validator predicate: every other gate result is trusted BECAUSE this one is
    green. Raise this instead, and the gate blocks with a remedy.
    """


def check(label, fn):
    try:
        fn()
        passes.append(label)
    except SkippedCheck as e:
        skips.append(f"{label}: {e}")
    except NotApplicable as e:
        not_applicable.append(f"{label}: {e}")
    except AssertionError as e:
        failures.append(f"{label}: {e}")
    except Exception as e:
        failures.append(f"{label}: EXCEPTION {type(e).__name__}: {e}")


def check_app_version_consistency():
    """Check 1: APP_VERSION in the JS matches every prose restatement of it.
    The preface "Current:" line carries a version like "X.Y.Z" or "X.Y.Z-beta" —
    possibly followed by a trailing period or other prose. We accept either a
    bare "Current: X.Y.Z[-suffix]." or the older "Current: X (Session …)" form
    so the gate is stable across the no-log-in-HTML policy change. The preface
    "current as of pass N / vX.Y.Z" phrase and (development tree only) the
    HANDOFF § 15 footer rows are checked below.
    """
    with open(HTML, encoding="utf-8") as f:
        content = f.read()
    js_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', content)
    # Strip any trailing punctuation/parenthesis from the captured version token.
    preface_match = re.search(r"Current:\s+([0-9][0-9A-Za-z.\-]*)", content)
    assert js_match, "cannot find 'const APP_VERSION = \"...\"'"
    assert preface_match, "cannot find 'Current: X.Y.Z' line in preface"
    js_ver = js_match.group(1)
    preface_ver = preface_match.group(1).rstrip(".")
    assert js_ver == preface_ver, (
        f"version mismatch — JS={js_ver}  preface={preface_ver}"
    )
    # The HANDOFF §15 Live-state footer row `| `APP_VERSION` | `X` |` is a Rule-13
    # required update site that no other gate scans (check #13 clips HANDOFF before
    # §15, and its volatile-fact regex matches only the `APP_VERSION = "N` restatement
    # form). Mirror of the neighbouring gated 'HTML file size' footer row.
    # A fourth restatement lives in the HTML preface tab-3 sentence ("current as of
    # pass N / vX.Y.Z-beta"). The count nouns on that line are gated by check #13's
    # preface patterns, but the version/pass tokens were gate-blind (the
    # (?<![Pp]ass[.s-]) lookbehind in the count patterns deliberately skips them).
    pref2 = re.search(r"current as of pass\s+(\d+)\s*/\s*v([0-9A-Za-z.\-]+)", content)
    assert pref2, "cannot find the preface 'current as of pass N / vX' phrase"
    assert pref2.group(2) == js_ver, (
        f"version mismatch — JS={js_ver}  preface-'as of' phrase={pref2.group(2)}"
    )
    if _snapshot_tree():
        # The HANDOFF § 15 footer is not shipped in a snapshot tree; the JS-vs-
        # preface half above is the whole check there.
        return
    with open(HANDOFF, encoding="utf-8") as f:
        handoff = f.read()
    ho_pass = re.search(r"\|\s*Current pass\s*\|\s*(\d+)\s*\|", handoff)
    assert ho_pass, "cannot find the HANDOFF §15 'Current pass' footer row"
    assert ho_pass.group(1) == pref2.group(1), (
        f"pass-number mismatch — preface 'as of pass'={pref2.group(1)}  HANDOFF §15 footer={ho_pass.group(1)}"
    )
    ho_match = re.search(r"\|\s*`APP_VERSION`\s*\|\s*`([^`]+)`\s*\|", handoff)
    assert ho_match, "cannot find the HANDOFF §15 Live-state `APP_VERSION` footer row"
    assert ho_match.group(1) == js_ver, (
        f"version mismatch — JS={js_ver}  HANDOFF §15 Live-state footer={ho_match.group(1)}"
    )


def check_foundational_rules_json_shape():
    """Check 2 + 4: foundational-rules.json is valid + every entry has required fields."""
    with open(FRULES_JSON, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list), "JSON root is not an array"
    assert len(data) > 0, "JSON is empty"
    required_fields = {"number", "name", "theme", "summary", "addedPass"}
    for i, entry in enumerate(data):
        missing = required_fields - set(entry.keys())
        assert not missing, f"entry {i} ({entry.get('name', '?')}) missing: {missing}"
        assert entry["number"] == i + 1, (
            f"entry {i} has number {entry['number']}, expected {i+1}"
        )


def check_foundational_rules_in_app_const_count():
    """Check 2 (continued): FOUNDATIONAL_RULES const length matches JSON length."""
    with open(HTML, encoding="utf-8") as f:
        content = f.read()
    # Count entries in the const by counting `{number:` patterns inside the
    # FOUNDATIONAL_RULES = [ ... ] block
    block_match = re.search(
        r"const FOUNDATIONAL_RULES\s*=\s*\[(.*?)\];",
        content,
        re.DOTALL,
    )
    assert block_match, "cannot find 'const FOUNDATIONAL_RULES = [ ... ];' in HTML"
    block = block_match.group(1)
    count_in_html = len(re.findall(r"\{number:\s*\d+", block))

    with open(FRULES_JSON, encoding="utf-8") as f:
        data = json.load(f)
    count_in_json = len(data)

    assert count_in_html == count_in_json, (
        f"FOUNDATIONAL_RULES const has {count_in_html} entries, "
        f"foundational-rules.json has {count_in_json}"
    )


def check_validator_rules_json_sync():
    """Check 5: dev/validator-rules.json is in sync with the in-app RULES array.
    Runs `generate-validator-rules-json.py --check` as a subprocess; succeeds if
    the regeneration produces byte-identical output to the checked-in file.
    Catches drift when a contributor adds/edits a rule in the HTML but forgets
    to regenerate the JSON mirror."""
    import subprocess
    if not os.path.exists(VRULES_GEN_SCRIPT):
        # Generator missing — the mirror-sync check cannot RUN. A skip is not a
        # pass (see the SkippedCheck docstring): this check is the one thing standing
        # between a drifted validator-rules.json and a green gate, and every other
        # result is trusted BECAUSE it is green. A bare `return` counted as a pass,
        # so a renamed/moved generator made the check a permanent silent pass while
        # the mirror drifted arbitrarily. Block with a remedy instead.
        raise SkippedCheck(
            f"generator script missing at {VRULES_GEN_SCRIPT} — mirror sync never ran; "
            f"restore it or remove this check"
        )
    if not os.path.exists(VRULES_JSON):
        raise AssertionError(
            f"validator-rules.json missing at {VRULES_JSON} — run "
            f"`python dev/scripts/generate-validator-rules-json.py` to create it"
        )
    result = subprocess.run(
        [sys.executable, VRULES_GEN_SCRIPT, "--check"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0, (
        f"validator-rules.json drift detected — re-run generator: "
        f"`python dev/scripts/generate-validator-rules-json.py`. "
        f"Generator stderr:\n{result.stderr.strip()}"
    )


def check_inline_script_js_syntax():
    """Check 6: the inline <script> block in s201_aton_studio.html parses as
    valid JavaScript. Uses V8 (via py-mini-racer) — the same engine browsers
    run — so a syntax error is caught before it reaches the browser.

    Exists because a syntax error (a bare block that detached an else-if
    chain) once shipped for an entire pass: static checks + manual review let
    it through, and it surfaced only when the browser could finally be
    exercised. V8's parser reports the exact "Unexpected token 'else'" + line
    number that took a full pass to find manually.

    Requires py-mini-racer. If it is absent the check cannot RUN, and a check
    that cannot run must not be reported as a pass — it raises SkippedCheck,
    which blocks the gate with the install command. To install:
      pip install py-mini-racer
    """
    try:
        import py_mini_racer
    except ImportError:
        raise SkippedCheck(
            "py-mini-racer not installed, so the inline <script> was never parsed — "
            "run `pip install py-mini-racer` to enable this check"
        )
    with open(HTML, encoding="utf-8") as f:
        content = f.read()
    sm = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
    assert sm, "no <script> tag found in HTML"
    js = sm.group(1)
    ctx = py_mini_racer.MiniRacer()
    try:
        # Use Function ctor to syntax-check without executing the body
        # (so we don't run the actual app code on every commit).
        # repr() escapes the source as a JS string literal.
        ctx.eval("new Function(" + repr(js) + ")")
    except Exception as e:
        # Strip the V8-internal stack trace; keep the user-relevant first lines.
        msg = str(e)
        first_lines = "\n      ".join(msg.split("\n")[:5])
        raise AssertionError(
            f"inline <script> has JS syntax error:\n      {first_lines}"
        )


def check_pass_count_consistency():
    """Check 3: the 'across N passes' phrasing agrees across the three docs.

    Uses re.findall and takes the MAX match per document (the current-state
    count). HANDOFF.md's narrative contains a chronological history with
    several "across X passes" phrasings — only the highest is the current
    state; a first-match read compared a historical figure in HANDOFF.md and
    dev/README.md against the current one in README.md and reported a false
    drift. Pass counts grow monotonically, so max() is always current."""
    _needs_dev_docs("dev/HANDOFF.md", "README.md", "dev/README.md")
    files = [(HANDOFF, "HANDOFF.md"), (README, "README.md"), (DEV_README, "dev/README.md")]
    counts = {}
    for path, name in files:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        # Find ALL "across N passes" / "across the N passes" matches; take max
        # (the highest pass count = the current state, since pass count grows monotonically)
        matches = re.findall(r"across\s+(?:the\s+)?(\d+)\s+passes", txt)
        if matches:
            counts[name] = max(int(m) for m in matches)
    if not counts:
        return  # no doc has the phrasing — nothing to compare
    unique_values = set(counts.values())
    assert len(unique_values) == 1, (
        f"pass-count drift across docs: {counts}"
    )


# Section headings that are intentionally historical and should NOT be flagged
# by the intra-section staleness check (check #7). Each entry is a regex
# pattern that, when present in a heading line, exempts that heading from the
# "must match max pass count" check.
#
# Why "Session N" is exempt: Session-headings are narrative summaries that
# enumerate the full work of that session (e.g. "Session 23 (... pass 54 ... pass 57 ...)").
# The pass-count phrasings inside are historical references to specific moments
# of that session, not current-state claims, and refreshing them every new pass
# would distort the historical record.
_INTENTIONAL_HISTORICAL_HEADING_PATTERNS = [
    r"\(historical",                         # explicit "(historical — as of pass N)" markers
    r"as of pass \d+",                       # "as of pass 13"
    r"The 88 Validation Rules",              # historical pass-13 inventory snapshot
    r"Session\s+\d+\s",                      # Session-N narrative headings (Session 23, Session 22, ...)
    r"Session\s+\d+\s*\(",                   # Same with paren-list summary
]


def check_intra_section_staleness():
    """Check 7: catch stale 'across N passes' phrasings inside section headings
    (### / ## / #) that don't match the document's current max pass count.

    Background: the pass-count consistency check (check #3) uses `max()` to
    accommodate the master-narrative megaline that contains historical pass
    references. But that masks intra-section staleness: e.g. HANDOFF once had
    `### Concrete rules maintained across the 109 passes` while the doc's
    max-pass narrative said 120+ — the heading itself was stale because the
    `max()` check ignored it.

    Rule 13 (Atomic delivery) requires every doc-touching pass to keep ALL
    pass-count phrasings synced — not just the max one. This check enforces
    that for SECTION HEADINGS specifically (where the pass count is part of
    the heading semantics, not historical narrative).

    Headings explicitly marked historical (matching one of
    `_INTENTIONAL_HISTORICAL_HEADING_PATTERNS`) are exempted.
    """
    _needs_dev_docs("dev/HANDOFF.md")
    with open(HANDOFF, encoding="utf-8") as f:
        txt = f.read()
    matches = re.findall(r"across\s+(?:the\s+)?(\d+)\s+passes", txt)
    if not matches:
        return
    max_pass = max(int(m) for m in matches)
    # Walk line-by-line looking for headings (## / ### / ####) containing
    # "across N passes" or "Over N passes" phrasings.
    stale = []
    for lineno, line in enumerate(txt.splitlines(), start=1):
        if not re.match(r"^\s{0,3}#{1,6}\s", line):
            continue
        # Skip if this heading is intentionally historical
        if any(re.search(p, line, re.IGNORECASE) for p in _INTENTIONAL_HISTORICAL_HEADING_PATTERNS):
            continue
        # Find pass-count phrasings inside this heading
        m = re.search(r"(across\s+(?:the\s+)?|over\s+)(\d+)\s+passes?", line, re.IGNORECASE)
        if not m:
            continue
        n = int(m.group(2))
        if n != max_pass:
            stale.append(f"line {lineno}: '{line.strip()[:120]}' says {n}, doc max is {max_pass}")
    assert not stale, (
        "intra-section pass-count staleness in HANDOFF.md (heading lines):\n      "
        + "\n      ".join(stale)
        + "\n      Either refresh the heading to match the current max pass count, or "
        "mark the section explicitly historical (e.g. '(historical — as of pass N)')."
    )


# Tolerance (in lines) for anchor freshness checks. ±2 absorbs the small drift
# from rare comment-block-insertion-after-anchor scenarios while still catching
# meaningful staleness (drift found in practice ranged from +30 to +756 lines).
_ANCHOR_TOLERANCE = 2


def check_function_anchor_freshness():
    """Check 8: walk every `**`functionName(args)`**` row in HANDOFF.md
    "Key functions" tables, extract (name, claimed line), grep HTML for
    `^function NAME(`, fail if the actual line drifts more than
    ±_ANCHOR_TOLERANCE from the claimed.

    Exists because the manual doc refresh tended to cover only the parser/
    generator/validator subset of anchors; the Builder/Annex-D/SVG anchors
    drifted silently for many passes (+30 to +756 lines when first measured).

    Skips:
      - Entries with `~` prefix (documented approximate, e.g. "~5135")
      - Entries with range line numbers (e.g. "**4255-4263**")
      - Lines outside the "Key functions" section (lines preceding "### Key
        functions" header are constants, narrative, etc.)
    """
    _needs_dev_docs("dev/HANDOFF.md")
    with open(HANDOFF, encoding="utf-8") as f:
        handoff_lines = f.read().splitlines()
    with open(HTML, encoding="utf-8") as f:
        html_text = f.read()

    # Locate the "Key functions" section. Limit to lines after this heading
    # (otherwise we'd snag function-name backticks in narrative prose).
    start = None
    for i, line in enumerate(handoff_lines):
        if re.match(r"^###\s+Key functions\b", line):
            start = i
            break
    if start is None:
        # Section not found — gate is opt-in on this doc shape.
        return

    # End of "Key functions" section is the next ## or ### heading at same/higher
    # depth, OR the end of the file.
    end = len(handoff_lines)
    for i in range(start + 1, len(handoff_lines)):
        line = handoff_lines[i]
        if re.match(r"^##\s|^###\s", line) and not re.match(r"^####\s", line):
            end = i
            break

    # Pattern: `| **`name(args)`** | **NNNN** |` or `| `name()` | **NNNN** |` or
    #          `| **`name(arg`** | **NNNN** |` (no closing `)` — observed in the
    # actual HANDOFF Key Functions tables where entries are written `name(arg`
    # without a closing paren, e.g. ``**`renderMap(`**``.
    # Capture (name, line). Tolerate optional whitespace, optional bold around the
    # line number, optional inline ~ prefix.
    # The closing `)` is OPTIONAL: every actual Key Functions table entry omits
    # it, and a regex that required it matched NOTHING — the check was a Rule 9
    # silent pass for many passes while +50 to +361 lines of drift went
    # unobserved. `[^`)]*` ensures we don't eat past the closing backtick when
    # there's no `)`. `\)?` makes the closing paren optional.
    row_re = re.compile(
        r"\|\s*\*?\*?`(_?[A-Za-z][\w$]*)\([^`)]*\)?`\*?\*?\s*\|\s*(~?)\*?\*?(\d+(?:-\d+)?)\*?\*?\s*\|"
    )
    stale = []
    for i in range(start, end):
        line = handoff_lines[i]
        m = row_re.search(line)
        if not m:
            continue
        name, approx, lineno_str = m.group(1), m.group(2), m.group(3)
        if approx == "~":
            continue  # documented approximate
        if "-" in lineno_str:
            continue  # range — multi-anchor row, skip
        claimed = int(lineno_str)
        # Find actual location in HTML
        actual_match = re.search(rf"^function\s+{re.escape(name)}\(", html_text, re.MULTILINE)
        if not actual_match:
            # Function not found at top level — could be a method or removed.
            # Don't flag as stale; flag as missing only with helpful context.
            stale.append(
                f"line {i+1}: '{name}()' anchor cited as {claimed} but `^function {name}(` not found in HTML"
            )
            continue
        # Compute actual line number (1-indexed)
        actual_line = html_text[:actual_match.start()].count("\n") + 1
        drift = actual_line - claimed
        if abs(drift) > _ANCHOR_TOLERANCE:
            stale.append(
                f"line {i+1}: '{name}()' cited as {claimed}, actual {actual_line} (drift {drift:+d})"
            )

    assert not stale, (
        "function-anchor freshness drift in HANDOFF.md 'Key functions' tables:\n      "
        + "\n      ".join(stale)
        + f"\n      Refresh anchors to match `^function NAME(` line in HTML "
        f"(tolerance ±{_ANCHOR_TOLERANCE}). Round-5 R5-D-1 / R5-D-4 — see "
        "pass 129 narrative."
    )


def check_constants_anchor_freshness():
    """Check 9: walk
    every single-name + single-line row in HANDOFF.md "Constants" table and
    verify each `^const NAME` matches within ±_ANCHOR_TOLERANCE lines.

    Skips:
      - Aggregate names (multiple constants with `/` separator) — e.g.
        `COLOURS / CPATTERNS / BSHAPES / BEASHAPES / TMSHAPES`
      - Range line numbers (NN-MM) — multi-constant rows
      - Names with embedded special chars (e.g. `(Path B singleton)` parens
        in the row label)
    """
    _needs_dev_docs("dev/HANDOFF.md")
    with open(HANDOFF, encoding="utf-8") as f:
        handoff_lines = f.read().splitlines()
    with open(HTML, encoding="utf-8") as f:
        html_text = f.read()

    # Locate the "Constants" section
    start = None
    for i, line in enumerate(handoff_lines):
        if re.match(r"^###\s+Constants\b", line):
            start = i
            break
    if start is None:
        return

    # End at the next ## or ### heading
    end = len(handoff_lines)
    for i in range(start + 1, len(handoff_lines)):
        line = handoff_lines[i]
        if re.match(r"^##\s|^###\s", line):
            end = i
            break

    # Pattern: `| NAME | **NNNN** |` or `| **\`NAME\`** | **NNNN** |`
    # Single name = letters/digits/underscores, NO `/` separator anywhere in
    # the name field (excludes aggregates).
    row_re = re.compile(
        r"\|\s*\*?\*?`?([A-Z][A-Z0-9_]+)`?\*?\*?\s*\|\s*\*?\*?(\d+)\*?\*?\s*\|"
    )
    stale = []
    for i in range(start, end):
        line = handoff_lines[i]
        # Skip the header / separator rows
        if re.match(r"^\s*\|---", line):
            continue
        m = row_re.search(line)
        if not m:
            continue
        # Reject aggregate row (label cell contains a slash)
        # Look at the first cell explicitly
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 3:
            continue
        first_cell = cells[1] if cells[0] == "" else cells[0]
        if "/" in first_cell or "(" in first_cell:
            continue  # aggregate or qualified name (e.g. "(Path B singleton)")
        # Reject if line-number cell is a range
        line_cell = cells[2] if cells[0] == "" else cells[1]
        if re.search(r"\d+\s*-\s*\d+", line_cell):
            continue
        name, claimed_str = m.group(1), m.group(2)
        claimed = int(claimed_str)
        # Find actual `^const NAME` line in HTML
        actual_match = re.search(rf"^const\s+{re.escape(name)}\b", html_text, re.MULTILINE)
        if not actual_match:
            stale.append(
                f"line {i+1}: '{name}' anchor cited as {claimed} but `^const {name}` not found in HTML"
            )
            continue
        actual_line = html_text[:actual_match.start()].count("\n") + 1
        drift = actual_line - claimed
        if abs(drift) > _ANCHOR_TOLERANCE:
            stale.append(
                f"line {i+1}: '{name}' cited as {claimed}, actual {actual_line} (drift {drift:+d})"
            )

    assert not stale, (
        "constants-table anchor freshness drift in HANDOFF.md:\n      "
        + "\n      ".join(stale)
        + f"\n      Refresh anchors to match `^const NAME` line in HTML "
        f"(tolerance ±{_ANCHOR_TOLERANCE}). Round-5 R5-D-2 / R5-D-5 — see "
        "pass 129 narrative."
    )


def _extract_identifier(snippet):
    """Helper for check 11: from a backticked code snippet inside the Source-file
    tour table, extract the canonical top-level identifier to look up via
    `^const NAME` or `^function NAME(...)` in the HTML.

    Handles:
      - `const NAME = ...` → NAME
      - `function NAME(args)` → NAME
      - `NAME(args)` or `NAME` (bare identifier) → NAME
      - English prose inside backticks → returns the first identifier-shaped
        token; lookup will then fail with no top-level match and the check
        will skip the entry (self-correcting false-positive guard).
    """
    s = snippet.strip()
    m = re.match(r"^const\s+([A-Za-z_][\w$]*)", s)
    if m:
        return m.group(1)
    m = re.match(r"^function\s+([A-Za-z_][\w$]*)", s)
    if m:
        return m.group(1)
    m = re.match(r"^(_?[A-Za-z][\w$]*)", s)
    if m:
        return m.group(1)
    return None


# Tolerance for the Source-file tour table — larger than _ANCHOR_TOLERANCE
# because the tour table convention uses `~NNN` to mean "approximate within
# a handful of lines"; we only want to flag SIGNIFICANT drift (the drift cases
# that motivated this check were +35 and +20 lines, which are clearly outside
# any reasonable "approximate" interpretation).
_TOUR_TOLERANCE_APPROX = 10
_TOUR_TOLERANCE_EXACT = _ANCHOR_TOLERANCE  # exact (`| NNN |` cells) get ±2 like checks 8/9


def check_source_file_tour_anchor_freshness():
    """Check 11: walk Source-file tour table line anchors in HANDOFF.md
    "Source-file tour" section AND CLAUDE.md's architecture table, verify each
    cited line matches the actual `^const NAME` or `^function NAME(` in the
    HTML. Closes a silent-drift gap: checks #8/#9 scan only the dedicated
    Constants + Key functions tables in HANDOFF.md, so the tour table's
    `(line ~NNN)` anchors and CLAUDE.md's `| NNN |` rows drifted undetected
    (+35 and +20 lines when first noticed).

    Scope:
      - Part A — HANDOFF.md "### Source-file tour" section: regex matches
        `` `<code>` (line ~NNN) `` or `` `<code>` (line NNN) `` patterns inside
        the table's description cells. The backticked content is decoded via
        `_extract_identifier` to get the canonical top-level name.
      - Part B — CLAUDE.md source-file region table: regex matches
        `| NNN | `<code>` ` single-line rows. Range rows like `| 720-820 |` are
        skipped (no specific anchor to check). CLAUDE.md currently anchors to
        symbols rather than line numbers, so this part (and Part D) finds
        nothing there; both stay as guards should such rows return.
      - Part C — `` `<code>` ... (HTML line NNN) `` prose anchors anywhere in
        HANDOFF.md (the foundational-rules intro uses this form).
      - Part D — `` `<code>` ... [s201_aton_studio.html:NNN](...) `` markdown
        links in CLAUDE.md.

    Tolerance:
      - Approximate refs (with `~` prefix): ±_TOUR_TOLERANCE_APPROX (10 lines)
        — honors the "approximate" convention while still flagging significant
        drift.
      - Exact refs (no `~`, or CLAUDE.md `| NNN |` cells): ±_TOUR_TOLERANCE_EXACT
        (±2 — same as checks #8/#9).

    Self-correcting false-positive guard: if the extracted identifier is not
    found at the HTML top level (e.g., backticked prose, method name, parameter
    name), the entry is silently skipped — only KNOWN top-level symbols can
    fire this check.
    """
    _needs_dev_docs("dev/HANDOFF.md")
    with open(HTML, encoding="utf-8") as f:
        html_text = f.read()

    stale = []

    def _resolve_identifier(name):
        """Return the (1-indexed) line number of `^[async ]function NAME(`,
        `^const NAME` or `^let|var NAME`, or None if not found. Matches
        `async function NAME(...)` too — runSmokeTests is declared async, and
        a `^function`-only regex silently skipped it."""
        m = re.search(rf"^(?:async\s+)?function\s+{re.escape(name)}\(", html_text, re.MULTILINE)
        if not m:
            m = re.search(rf"^const\s+{re.escape(name)}\b", html_text, re.MULTILINE)
        if not m:
            # let/var module-scope state (compStack, builderFeats, …) — without
            # this fallback, let-declared tour anchors were silently skipped by the
            # unknown-identifier guard and drifted by thousands of lines undetected.
            m = re.search(rf"^(?:let|var)\s+{re.escape(name)}\b", html_text, re.MULTILINE)
        if not m:
            return None
        return html_text[:m.start()].count("\n") + 1

    # === Part A: HANDOFF.md "Source-file tour" table ===
    with open(HANDOFF, encoding="utf-8") as f:
        handoff_lines = f.read().splitlines()
    start = None
    for i, line in enumerate(handoff_lines):
        if re.match(r"^###\s+Source-file tour\b", line):
            start = i
            break
    if start is not None:
        end = len(handoff_lines)
        for i in range(start + 1, len(handoff_lines)):
            if re.match(r"^###\s|^##\s", handoff_lines[i]):
                end = i
                break
        # Match `<backticked snippet>` followed by `(line ~NNN)` or `(line NNN)`.
        # The backticked snippet is captured greedily up to the next backtick.
        # `(?:\*\*)?` after the closing backtick allows bold-wrapped refs like
        # ``**`runVal()`** (line ~8966)`` — the trailing `**` would otherwise
        # leave the regex unable to bridge the closing backtick → `(line ...)`.
        # `\s*` then allows zero-or-more whitespace before `(line`.
        # Terminate on a digit word-boundary (`\b`) instead of requiring a literal
        # `)` immediately after the number, so the `(line ~NNN — prose)` /
        # `(line ~NNN; prose)` em-dash/semicolon-description format is not
        # gate-invisible (the Exchange Set row used it and drifted ~1400 lines
        # undetected). The unknown-identifier guard below still skips any captured
        # snippet that is not a real top-level symbol, so the looser match is safe.
        ref_re = re.compile(r"`([^`]+)`(?:\*\*)?\s*\(line\s+(~?)(\d+)\b")
        for i in range(start, end):
            for m in ref_re.finditer(handoff_lines[i]):
                snippet, approx, lineno_str = m.group(1), m.group(2), m.group(3)
                name = _extract_identifier(snippet)
                if name is None:
                    continue
                actual_line = _resolve_identifier(name)
                if actual_line is None:
                    continue  # not a top-level symbol — skip per self-correcting guard
                claimed = int(lineno_str)
                tolerance = _TOUR_TOLERANCE_APPROX if approx == "~" else _TOUR_TOLERANCE_EXACT
                drift = actual_line - claimed
                if abs(drift) > tolerance:
                    stale.append(
                        f"HANDOFF.md line {i+1}: '{name}' cited as "
                        f"{'~' if approx else ''}{claimed}, actual {actual_line} "
                        f"(drift {drift:+d}, tolerance ±{tolerance})"
                    )

    # === Part B: CLAUDE.md architecture/source-file region table ===
    # Format: `| NNN | `code` description |` for single-line rows.
    # Range rows like `| 720-820 | ... |` are skipped (only `^\|\s*\d+\s*\|`
    # matches; the `-` in a range prevents the `\d+\s*\|` second-cell-boundary
    # from matching). The backticked identifier extraction is the same as Part A.
    CLAUDE_MD = os.path.join(PROJECT_ROOT, "CLAUDE.md")
    if os.path.exists(CLAUDE_MD):
        with open(CLAUDE_MD, encoding="utf-8") as f:
            claude_lines = f.read().splitlines()
        # Match `| NNN | `<snippet>` ...` — exact-line rows only.
        # `(?!\s*-)` after the line number rejects ranges (which have `-` after
        # the first digit run before the second `|`).
        row_re = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`")
        for i, line in enumerate(claude_lines):
            m = row_re.match(line)
            if not m:
                continue
            claimed_str, snippet = m.group(1), m.group(2)
            name = _extract_identifier(snippet)
            if name is None:
                continue
            actual_line = _resolve_identifier(name)
            if actual_line is None:
                continue
            claimed = int(claimed_str)
            drift = actual_line - claimed
            if abs(drift) > _TOUR_TOLERANCE_EXACT:
                stale.append(
                    f"CLAUDE.md line {i+1}: '{name}' cited as {claimed}, "
                    f"actual {actual_line} "
                    f"(drift {drift:+d}, tolerance ±{_TOUR_TOLERANCE_EXACT})"
                )

    # === Part C: HANDOFF.md prose anchors outside Source-file tour ===
    # Part A only matches the Source-file tour table format. Prose elsewhere in
    # HANDOFF.md cites the same symbols as `` `NAME` ... (HTML line NNN) `` (the
    # foundational-rules intro does), and one such anchor drifted +35 lines
    # unseen; this Part C catches that phrasing anywhere in HANDOFF.md.
    #
    # Pattern: backticked identifier + up to 50 chars of intervening text
    # (excluding backticks, so we anchor to the IMMEDIATELY-PRECEDING backtick
    # rather than skipping over another backticked identifier in between) +
    # literal `(HTML line NNN)`. The `[^`\n]{0,50}?` is crucial — without
    # excluding backticks, "`parseGML` and `parseAllGML` (HTML line 5288)"
    # would falsely associate the line ref with parseGML instead of parseAllGML.
    #
    # Exact tolerance (`(HTML line NNN)` has no `~` so the author is claiming
    # exact line — use _TOUR_TOLERANCE_EXACT = ±2, same as CLAUDE.md anchors).
    #
    # Scope: HANDOFF.md only — CLAUDE.md doesn't use this phrasing, the
    # `(HTML line NNN)` pattern appears only in HANDOFF Section 2 prose so far.
    # Extending to CLAUDE.md / dev/README.md / root README.md would be a one-line
    # change if the convention spreads.
    prose_re = re.compile(r"`([^`]+)`[^`\n]{0,50}?\(HTML line (\d+)\)")
    for i, line in enumerate(handoff_lines):
        for m in prose_re.finditer(line):
            snippet, lineno_str = m.group(1), m.group(2)
            name = _extract_identifier(snippet)
            if name is None:
                continue
            actual_line = _resolve_identifier(name)
            if actual_line is None:
                continue  # not a top-level symbol — skip per self-correcting guard
            claimed = int(lineno_str)
            drift = actual_line - claimed
            if abs(drift) > _TOUR_TOLERANCE_EXACT:
                stale.append(
                    f"HANDOFF.md line {i+1}: '{name}' cited as (HTML line {claimed}), "
                    f"actual {actual_line} "
                    f"(drift {drift:+d}, tolerance ±{_TOUR_TOLERANCE_EXACT})"
                )

    # === Part D: CLAUDE.md markdown-link anchors `[s201_aton_studio.html:NNN]` ===
    # Rule 23 (single-source-or-gate): a markdown link of the form
    # `[s201_aton_studio.html:NNN](s201_aton_studio.html:NNN)` next to a backticked
    # symbol once drifted by 20 lines with no gate scanning it. Part B catches
    # `| NNN | \`code\` |` table rows; Part D catches the
    # `\`code\` ... [s201_aton_studio.html:NNN]` prose pattern.
    #
    # Pattern: backticked identifier + up to 80 chars of intervening text
    # (excluding backticks + newlines) + markdown link to s201_aton_studio.html:NNN.
    # The 80-char window is wider than Part C's 50 because prose like
    # "in the in-app `FOUNDATIONAL_RULES` const at [s201_aton_studio.html:NNN]"
    # exceeds 50 characters of intervening text.
    #
    # Exact tolerance — the link cites an exact line, not approximate.
    md_link_re = re.compile(r"`([^`]+)`[^`\n]{0,80}?\[s201_aton_studio\.html:(\d+)\]\(s201_aton_studio\.html:\d+\)")
    if os.path.exists(CLAUDE_MD):
        for i, line in enumerate(claude_lines):
            for m in md_link_re.finditer(line):
                snippet, lineno_str = m.group(1), m.group(2)
                name = _extract_identifier(snippet)
                if name is None:
                    continue
                actual_line = _resolve_identifier(name)
                if actual_line is None:
                    continue  # not a top-level symbol — skip per self-correcting guard
                claimed = int(lineno_str)
                drift = actual_line - claimed
                if abs(drift) > _TOUR_TOLERANCE_EXACT:
                    stale.append(
                        f"CLAUDE.md line {i+1}: '{name}' cited as "
                        f"[s201_aton_studio.html:{claimed}], actual {actual_line} "
                        f"(drift {drift:+d}, tolerance ±{_TOUR_TOLERANCE_EXACT})"
                    )

    assert not stale, (
        "Source-file tour table anchor freshness drift:\n      "
        + "\n      ".join(stale)
        + "\n      Refresh anchors to match actual `^const NAME` or `^function NAME(` "
        "line in HTML. Added pass 255 (closes the gap pass 254 found at HANDOFF L149 + "
        "CLAUDE.md L66+L67); Part C added pass 257 (closes gap pass 256 found at HANDOFF L25); "
        "Part D added pass 259 (closes gap pass-259 audit found at CLAUDE.md L15 markdown link)."
    )


# Count-phrase ground truth — maintained alongside the gate definitions. Used
# by check_count_phrase_freshness (#12), check_doc_count_phrase_freshness (#13)
# and, read via regex, by run-browser-smoke-gate.py + build-public-snapshot.py.
# Update when the underlying count changes (most counts only change when a new
# check/test/rule is added). The precommit count is self-derived from this
# file's own `check()` registration count below (so it auto-bumps when a new
# check is added).
_COUNT_GROUND_TRUTH = {
    "smoke": 336,        # in-app smoke invariants: the runSmokeTests suite size, also the browser-gate baseline. Single source of truth for the suite size; what each pass added or removed lives in dev/CHANGELOG.md (Rule 21/23), not here.
    "foundational": 25,  # FOUNDATIONAL_RULES const length + foundational-rules.json entries
    # Rule 23 (single-source-or-gate): counts that once appeared ungated across
    # .md surfaces. Each value is the current canonical count; bump in lockstep
    # with the underlying code.
    "validator_total": 246,         # per-feature + structural + exchange-set (lockstep-asserted below)
    "validator_per_feature": 195,   # RULES[] array length — also locked at runtime by the smoke assertion on RULES.length
    "validator_structural": 24,     # GML-STR-* rule count (validateGMLStructure push calls) — also locked by the smoke assertion that a full-DII dataset yields every GML-STR id
    "validator_exchange_set": 27,   # exchange-set package rule count (validateExchangeSet push calls: S158-PKG-NN per S-158:100 Ed 1.0.0 Collection A Part 15/17 + S201-ES-NN per S-201 PS 2.0.0 §11 Data Product Delivery / §12.2.3 discovery metadata) — run when a full Exchange Set ZIP is ingested on the Validator tab
    "atypes": 76,                   # ATYPES catalogue length (59 S-201 + 17 nonS201:true)
    "xsl_templates": 65,            # Annex_D/Rules/*.xsl file count (Annex D portrayal source templates)
    "svg_symbols": 236,             # Annex_D/Symbols/*.svg file count (Annex D portrayal symbol library)
}
# Rule-23 lockstep guard: the validator counts move together. per_feature is
# anchored to runtime (the smoke RULES.length assertion) and structural to the
# smoke assertion that a full-DII dataset yields every GML-STR id, but
# validator_total is anchored only to doc phrases — so a rule-add pass that bumps
# per_feature (forced by the smoke gate) while forgetting the total would have
# checks 12/13 actively ENFORCING the stale total across every "N validator
# rules" / "= N total" phrase (gate-PINNED wrong prose). Module-level so the gate
# refuses to run at all in that state, naming the slip.
assert _COUNT_GROUND_TRUTH["validator_total"] == (
    _COUNT_GROUND_TRUTH["validator_per_feature"] + _COUNT_GROUND_TRUTH["validator_structural"]
    + _COUNT_GROUND_TRUTH["validator_exchange_set"]
), (
    "_COUNT_GROUND_TRUTH lockstep broken: validator_total "
    f"{_COUNT_GROUND_TRUTH['validator_total']} != per_feature "
    f"{_COUNT_GROUND_TRUTH['validator_per_feature']} + structural "
    f"{_COUNT_GROUND_TRUTH['validator_structural']} + exchange_set "
    f"{_COUNT_GROUND_TRUTH['validator_exchange_set']} — bump all four together"
)


def _self_count_precommit_checks():
    """Return the number of `check(...)` registrations in this script.

    Reads __file__ rather than counting from a hardcoded constant so the
    precommit ground-truth auto-bumps when a new check is added — eliminating
    the maintenance burden of manually updating a count constant alongside
    each new `check()` call.
    """
    with open(__file__, encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"^check\(", content, re.MULTILINE))


def check_count_phrase_freshness():
    """Check 12: scan known drift surfaces (HTML <script> block content, the
    HTML preface comment, dev/scripts/*.py file content) for count-phrase
    references and flag any that don't match the ground-truth count.

    These surfaces were gate-blind: two smoke-count phrasings in <script>
    comments (`N deterministic in-process tests`, `1 of N tests fetches`) and
    the precommit-count phrasing in run-browser-smoke-gate.py (`N checks,
    every commit`) each sat several bumps behind the truth with nothing to
    detect it — the Rule-9 silent-drift class.

    Pattern list (compiled): (regex, count_key, friendly_name) tuples. Each
    regex's first capture group MUST be the count digit. Adding a new count
    surface = add a new tuple here.

    False-positive guard: every pattern requires both a number AND a context
    noun (`deterministic`, `tests fetches`, `checks, every commit`). Bare
    numbers don't match. Counts inside historical CHANGELOG entries are not
    scanned (CHANGELOG.md isn't in the file list).

    Scope (which files):
      - HTML s201_aton_studio.html `<script>` block (extracted via the same
        regex as check #6's syntax check), plus the preface before it for the
        validator-count patterns only (Part A2)
      - dev/scripts/*.py — every Python file in the scripts dir except this
        one (see Part B)
      - HANDOFF.md / CLAUDE.md / README.md / dev/README.md / CHANGELOG.md are
        EXCLUDED — the .md count phrases are check #13's job (pass counts and
        anchors are #3/#7/#11's), and CHANGELOG.md is frozen history.
    """
    GROUND_TRUTH = dict(_COUNT_GROUND_TRUTH)
    GROUND_TRUTH["precommit"] = _self_count_precommit_checks()

    PATTERNS = [
        # (regex, count_key, friendly_name)
        # Smoke count phrasings inside HTML <script> + .py docstrings.
        # Pattern requires a context noun (`in-process` / `invariants` / `tests`)
        # to avoid false-positive on phrases like "Rule-18 deterministic-placeholder"
        # where `18` is the rule number, not a count.
        (re.compile(r"\b(\d+)\s+deterministic\s+(?:in-process|invariants|tests)\b"), "smoke", "N deterministic (in-process|invariants|tests)"),
        (re.compile(r"\b1\s+of\s+(\d+)\s+tests\s+fetches\b"), "smoke", "1 of N tests fetches"),
        # Precommit count phrasings inside .py docstrings + HTML <script>.
        # The `, every commit` suffix excludes historical Live-State references
        # like "Pre-commit 10/10" which use a different phrasing.
        (re.compile(r"\b(\d+)\s+checks,\s+every commit\b"), "precommit", "N checks, every commit"),
        # Validator rule-count phrases in HTML script comments (`N per-feature` /
        # `N structural checks` / `= N total`) — the same Rule-23 gate-blind class
        # check #13 gates in .md surfaces, applied to the HTML script-comment
        # surface here (three such numbers once sat one rule-add behind the truth).
        #
        # Lookbehind `(?<![Pp]ass[\s-])` excludes "pass-125" / "pass 125" /
        # "Pass-125" which appear in `<script>` comments referring to pass
        # numbers (same false-positive guard as check #13's PATTERNS).
        #
        # Digit quantifier `\d{2,}` (NOT `\d+`) excludes single-digit matches
        # that would false-positive on (a) version-segment last-digits like the
        # `0` in `S-100 5.2.0 per-feature rules` and (b) bare narrative integers
        # like `REMOVED 4 per-feature rules`. Every validator count in this
        # codebase is ≥2 digits (see _COUNT_GROUND_TRUTH; bump to `\d{2,4}`
        # if/when a count exceeds 999).
        #
        # Phrasing variants mirror check #13's PATTERNS: `per-feature rules` /
        # `per-feature validator rules` both name the same count. Structural
        # supports both `structural rules` and `structural checks` — same
        # underlying GML-STR-* count regardless of author's word choice.
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+per-feature(?!-)"), "validator_per_feature", "N per-feature"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+(?:GML\s+)?structural\s+(?:rules?|checks?)\b"), "validator_structural", "N structural rules/checks"),
        # `= N total` form — narrow anchor on the leading `=` to avoid false-
        # positiving on `expected 150 total labels` (`150` is not preceded by
        # `=`; it counts CD_ENUMS labels, not validator rules). The bare
        # `\d+ total` form would false-positive there; the `= N total`
        # narrowing rescues it. Same `\d{2,}` rule as above.
        (re.compile(r"=\s*(\d{2,})\s+total\b"), "validator_total", "= N total"),
        # Three more phrasings that drifted ungated in HTML <script> comments —
        # "N validator rules" (smoke-test comment headers), "N per-feature in
        # RULES" (the `in` form the `per-feature rules` pattern above misses),
        # and "features × N rules" (runVal's PERFORMANCE NOTE).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+validator\s+rules?\b"), "validator_total", "N validator rules"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+per-feature\s+in\b"), "validator_per_feature", "N per-feature in RULES"),
        (re.compile(r"features\s*[×x]\s*(\d{2,})\s+rules?\b"), "validator_per_feature", "features × N rules"),
        # Two count phrasings seen in the HTML preface comment: `N-rule validator`
        # (the inverted word order check #13 already gates) and bare `N GML
        # structural` (no rules?/checks? suffix, which the structural pattern above
        # requires). Mirror both here so check #12's HTML/py scan stays in lockstep.
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})-rule\s+validator\b"), "validator_total", "N-rule validator"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+GML\s+structural\b"), "validator_structural", "N GML structural"),
        # The `N GML-STR-* structural` / `N GML-STR structural` form — the hyphenated
        # rule-prefix interposed between the number and "structural" defeats the bare
        # "N GML structural" pattern above (a stale HANDOFF § 3 phrase slipped the
        # gate for exactly this reason).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+GML-STR-?\*?\s+structural\b"), "validator_structural", "N GML-STR-* structural"),
        # The exchange-set package corpus (validateExchangeSet) gets its own phrase
        # gate — "N exchange-set rules/checks" — so the third count component can
        # never drift ungated the way the sibling counts once did (Rule 23).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+exchange-set\s+(?:rules?|checks?)\b"), "validator_exchange_set", "N exchange-set rules/checks"),
        # Foundational-count phrases in the FOUNDATIONAL_RULES smoke test: a length-only
        # bump once left the test's title/comment/loop/detail at the previous count
        # precisely because NO pattern matched "N entries with (consecutive )numbers 1..N".
        # Gate both the leading count and the range end (two single-group tuples — the
        # scan compares one group per pattern). The per-entry loop bound itself is code
        # (derives from FOUNDATIONAL_RULES.length), so prose is the only drift surface left.
        (re.compile(r"\b(\d+)\s+entries\s+with\s+(?:consecutive\s+)?numbers\s+1\.\."), "foundational", "N entries with numbers 1.."),
        (re.compile(r"\bentries\s+with\s+(?:consecutive\s+)?numbers\s+1\.\.(\d+)\b"), "foundational", "entries with numbers 1..N"),
        # The FOUNDATIONAL_RULES preface bump-checklist "(currently N → N+1)" — went two
        # rule-adds stale because nothing matched it. Gate the current-count arm; bumping
        # it forces the author through the whole phrase. Anchored on the checklist's own
        # "N to N+1 (" lead-in — a bare `currently N →` would misfire on the first future
        # "currently 247 → 248"-style comment for a NON-foundational count (the
        # script already carries many unrelated arrow pairs).
        (re.compile(r"N\s+to\s+N\+1\s+\(currently\s+(\d+)\s+→"), "foundational", "N to N+1 (currently N →"),
        # The length-check failure-detail template "expected N rules, got ${...}" — the one
        # remaining prose literal in the test (renders only on an already-failing run, but
        # can lie about WHAT was expected). Comma+got anchor keeps it site-specific.
        (re.compile(r"expected\s+(\d+)\s+rules,\s+got"), "foundational", "expected N rules, got"),
    ]

    stale = []

    # === Part A: HTML <script> block content ===
    with open(HTML, encoding="utf-8") as f:
        html_text = f.read()
    sm = re.search(r"<script>(.*?)</script>", html_text, re.DOTALL)
    if sm:
        script = sm.group(1)
        # Line offset where <script> body starts (so we can report absolute HTML
        # line numbers, not script-relative ones).
        script_offset = html_text[:sm.start()].count("\n") + 1
        for pattern, key, friendly in PATTERNS:
            for m in pattern.finditer(script):
                claimed = int(m.group(1))
                truth = GROUND_TRUTH[key]
                if claimed != truth:
                    rel_line = script[:m.start()].count("\n")
                    abs_line = script_offset + rel_line
                    stale.append(
                        f"s201_aton_studio.html line {abs_line}: '{friendly}' shows "
                        f"{claimed}, ground truth is {truth} ({key} count)"
                    )

    # === Part A2: HTML preface comment block (before <script>) — validator-count patterns ===
    # The big <!-- ... --> preface restates the validator counts (per-feature /
    # structural / total) in end-user prose, but Part A scans ONLY the <script>
    # block, so a stale preface count was gate-blind (the preface once lagged a
    # rule-add behind the live truth). Scan the pre-<script> region with the
    # validator patterns so the preface stays in lockstep (Rule 23 —
    # single-source-or-gate). Restricted to the validator keys: the smoke/precommit
    # phrasings only occur inside <script>, and the quick-fix-coverage phrase
    # "~50 of N rules" carries no matching pattern context (no
    # "per-feature"/"structural"/leading "="), so it is not gated to the exact total.
    if sm:
        preface = html_text[:sm.start()]
        _validator_keys = {"validator_per_feature", "validator_structural", "validator_total"}
        for pattern, key, friendly in PATTERNS:
            if key not in _validator_keys:
                continue
            for m in pattern.finditer(preface):
                claimed = int(m.group(1))
                truth = GROUND_TRUTH[key]
                if claimed != truth:
                    abs_line = preface[:m.start()].count("\n") + 1
                    stale.append(
                        f"s201_aton_studio.html line {abs_line}: '{friendly}' shows "
                        f"{claimed}, ground truth is {truth} ({key} count) [preface]"
                    )

    # === Part B: dev/scripts/*.py file content ===
    # Excludes this script itself — its comments and docstrings legitimately quote
    # example / historical count values (the pattern documentation above), so
    # self-scanning would always fail. Self-exclusion is safe because the
    # precommit ground-truth IS self-derived via _self_count_precommit_checks(),
    # so internal drift in THIS script's prose is cosmetic-only — the check count
    # it reports is always live.
    SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "dev", "scripts")
    SELF_PATH = os.path.abspath(__file__)
    if os.path.isdir(SCRIPTS_DIR):
        for fname in sorted(os.listdir(SCRIPTS_DIR)):
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(SCRIPTS_DIR, fname)
            if os.path.abspath(fpath) == SELF_PATH:
                continue  # skip self per the docstring-quote rationale above
            with open(fpath, encoding="utf-8") as f:
                content = f.read()
            for pattern, key, friendly in PATTERNS:
                for m in pattern.finditer(content):
                    claimed = int(m.group(1))
                    truth = GROUND_TRUTH[key]
                    if claimed != truth:
                        rel_line = content[:m.start()].count("\n") + 1
                        stale.append(
                            f"dev/scripts/{fname} line {rel_line}: '{friendly}' shows "
                            f"{claimed}, ground truth is {truth} ({key} count)"
                        )

    assert not stale, (
        "count-phrase freshness drift in gate-blind surfaces:\n      "
        + "\n      ".join(stale)
        + f"\n      Ground truth: smoke={GROUND_TRUTH['smoke']}, "
        f"precommit={GROUND_TRUTH['precommit']} (self-derived from `check()` "
        f"registrations), foundational={GROUND_TRUTH['foundational']}. "
        "Refresh the cited count or update _COUNT_GROUND_TRUTH if the truth changed. "
        "Added pass 257 (closes the gate-blind surfaces pass 256 found: HTML <script> "
        "comments + .py docstrings)."
    )


def check_doc_count_phrase_freshness():
    """Check 13 (Rule 23 — single-source-or-gate): scan markdown documentation
    surfaces for count-phrase references and flag any that don't match the
    ground-truth count. Companion to check #12, which covers HTML <script> +
    .py files; this check covers the .md files #12 deliberately excludes.

    Exists because the shared counts were duplicated ungated across
    HANDOFF.md / README.md / CLAUDE.md / dev/README.md — the foundational
    count in 9+ places, the validator total / per-feature / structural split
    across the READMEs, the feature-type / XSL-template / SVG-symbol counts
    in HANDOFF + root README prose — and drifted independently. Each was a
    Rule-23 violation (ungated duplicated state); this check gates them.

    Scope:
      - CLAUDE.md (full)
      - README.md (root, full)
      - dev/README.md (full)
      - dev/HANDOFF.md — only content BEFORE `## 15. Live state` header.
        The Live State section + everything below contains historical pass
        entries with frozen historical counts (a row that names the
        foundational count as it stood at that pass) that intentionally
        don't match current ground truth. The § 15 footer rows that MUST be
        current are pinned separately by the volatile-fact block below.
      - dev/CHANGELOG.md is EXCLUDED — it's an append-only historical log
        per Rule 21, frozen historical counts are by design.

    Patterns: shape similar to check #12 but tuned for prose phrasing
    rather than code-comment phrasing. Each requires a context noun so
    bare numbers don't match.
    """
    _needs_dev_docs("dev/HANDOFF.md", "dev/README.md", "CLAUDE.md")
    GROUND_TRUTH = dict(_COUNT_GROUND_TRUTH)
    GROUND_TRUTH["precommit"] = _self_count_precommit_checks()

    # Every pattern is prefixed with `(?<![Pp]ass[\s-])` — a negative lookbehind
    # that prevents matching when the number is preceded by "pass-" / "Pass-" /
    # "pass " / "Pass " (catches "Pre-pass-188 validator rule" false positives
    # where 188 is a pass number, not a count — the first run of this check
    # flagged exactly that HANDOFF phrase as a 188-validator-rules drift).
    # Fixed-length 5 chars so Python re supports it.
    PATTERNS = [
        # Foundational rules count
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+foundational\s+(?:engineering\s+)?rules?\b"), "foundational", "N foundational rules"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)-entry\s+(?:machine-readable\s+)?mirror\b"), "foundational", "N-entry mirror"),
        # Validator total / split
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+validator\s+rules?\b"), "validator_total", "N validator rules"),
        # "N-rule validator" compound-adjective form (CLAUDE.md's intro once drifted
        # ungated here — the bare-count pattern above needs "validator" to FOLLOW
        # "rules", which this word order inverts).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)-rule\s+validator\b"), "validator_total", "N-rule validator"),
        # The Layer-2 schema range "GML-STR-02..N" (HANDOFF Rule-17 row + expansion +
        # foundational-rules.json) — N is the highest GML-STR id = the structural-rule
        # count (01..N contiguous). Drifted ungated when structural rules were added.
        (re.compile(r"GML-STR-02\.\.(\d+)\b"), "validator_structural", "GML-STR-02..N range"),
        # The suffixed structural patterns (further down) require a rules?/checks? suffix,
        # so the BARE `N GML structural` noun form drifted ungated — CLAUDE.md + the HANDOFF
        # intro carried a stale count with no suffix. Add the bare form. Historical
        # pre-pass counts live only in § 15 Live state, clipped below.
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+GML\s+structural\b"), "validator_structural", "N GML structural"),
        # The `N GML-STR-* structural` / `N GML-STR structural` form — the hyphenated
        # rule-prefix interposed between the number and "structural" defeats the bare
        # "N GML structural" pattern above (a stale HANDOFF § 3 phrase slipped the
        # gate for exactly this reason).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+GML-STR-?\*?\s+structural\b"), "validator_structural", "N GML-STR-* structural"),
        # The exchange-set package corpus (validateExchangeSet) gets its own phrase
        # gate — "N exchange-set rules/checks" — so the third count component can
        # never drift ungated the way the sibling counts once did (Rule 23).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+exchange-set\s+(?:rules?|checks?)\b"), "validator_exchange_set", "N exchange-set rules/checks"),
        # General "N per-feature" form — catches every wording the specific
        # "per-feature rules" pattern missed ("N per-feature in RULES", "N per-feature +",
        # "N per-feature (in RULES[]") that drifted ungated in the .md surfaces.
        # \d{2,} avoids matching small narrative integers like "added 5 per-feature rules".
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d{2,})\s+per-feature(?!-)"), "validator_per_feature", "N per-feature"),
        # §10 rule-count breakdown table total row ("| **Total** | **N** |").
        (re.compile(r"\*\*Total\*\*\s*\|\s*\*\*(\d{2,})\*\*"), "validator_total", "breakdown table Total"),
        # "layered validator (N rules: ...)" prose form (HANDOFF intro) — drifted ungated.
        (re.compile(r"validator\*?\*?\s*\((\d{2,})\s+rules\b"), "validator_total", "validator (N rules)"),
        # ATYPES feature-type count
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+registered\s+(?:S-201\s+)?feature\s+types?\b"), "atypes", "N registered feature types"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)-entry\s+feature-type\s+catalogue\b"), "atypes", "N-entry feature-type catalogue"),
        # Annex-D counts
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+SVG\s+files?\b"), "svg_symbols", "N SVG files"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+SVG\s+symbols?\b"), "svg_symbols", "N SVG symbols"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+XSL\s+rule\s+templates?\b"), "xsl_templates", "N XSL rule templates"),
        # Smoke-gate invariants (Rule 23). Catches the unambiguous named-noun
        # forms: `N-invariant`, `N in-app smoke invariants`, `N in-browser
        # invariants`, `N deterministic in-process invariants`, `N smoke
        # invariants`. The bare `N/N` slash form is gated separately by the
        # self-paired set-membership scan below the PATTERNS loop: it is
        # gate-ambiguous between smoke and precommit, which a single (regex,
        # key) tuple can't express — and an `N/N` does NOT always sit beside a
        # named form (`13/13` / `12/12` were once stranded across README +
        # HANDOFF + CLAUDE with no adjacent named form to force the fix).
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)-invariant\b"), "smoke", "N-invariant"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+in-app\s+smoke\s+invariants?\b"), "smoke", "N in-app smoke invariants"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+in-browser\s+(?:smoke\s+)?invariants?\b"), "smoke", "N in-browser invariants"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+deterministic\s+in-(?:app|process|browser)\s+invariants?\b"), "smoke", "N deterministic invariants"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+smoke\s+invariants?\b"), "smoke", "N smoke invariants"),
        # Pre-commit gate count (Rule 23). Catches the unambiguous named-noun
        # forms: `N static checks`, `N-check gate`. Bare `N/N` is gated by the
        # self-paired set-membership scan below.
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+static\s+checks?\b"), "precommit", "N static checks"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)-check\s+(?:static\s+)?gate\b"), "precommit", "N-check gate"),
        # GML structural rule count (Rule 23). Catches `N structural`, `N GML
        # structural`, `N document-level structural` with a rules?/checks?
        # suffix. `GML-STR-*` rules are emitted by validateGMLStructure.
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+(?:GML\s+)?structural\s+(?:rules?|checks?)\b"), "validator_structural", "N structural rules"),
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)\s+document-level\s+structural\s+checks?\b"), "validator_structural", "N document-level structural checks"),
        # Validator total in compound-adjective / section-header forms (Rule 23):
        # the HANDOFF § 10 header (`Validator — N rules`) and prose sites
        # (`N-rule corpus`) drifted after a rule-add because no existing pattern
        # matched these phrasings.
        (re.compile(r"(?<![Pp]ass[\s-])\b(\d+)-rule\s+corpus\b"), "validator_total", "N-rule corpus"),
        (re.compile(r"(?<![Pp]ass[\s-])Validator\s+[—–-]\s+(\d+)\s+rules?\b"), "validator_total", "Validator — N rules"),
        # `validator-rules.json (N rules)` form (Rule 23). The root README drifted
        # here because "N rules" (no "validator") matched no pattern. Anchored on
        # the filename to stay false-positive-safe.
        (re.compile(r"validator-rules\.json[^\d]{0,5}(\d+)\s+rules?\b"), "validator_total", "validator-rules.json (N rules)"),
        # `foundational-rules.json (N rules ...)` form — root README drifted here ungated
        # (filename-anchored, mirroring the validator-rules.json pattern above).
        (re.compile(r"foundational-rules\.json[^\d]{0,5}(\d+)\s+rules?\b"), "foundational", "foundational-rules.json (N rules)"),
        # The "Rules 1-N" foundational range form (dev/README onboarding steps) — drifted
        # ungated because the other foundational patterns require the noun "foundational".
        # Anchored on the onboarding verbs (Internalise / skim) so a future legitimate
        # SUBSET range like "Rules 1-4" in prose can't false-fail (adversarial-verify catch).
        (re.compile(r"(?:[Ii]nternalise|skim)\s+Rules\s+1-(\d+)\b"), "foundational", "Internalise/skim Rules 1-N"),
        # Smoke result in the Tab-3 `report N passed` form (Rule 23) — drifted in
        # dev/README.md because no smoke pattern matched the "report N passed"
        # phrasing.
        (re.compile(r"(?<![Pp]ass[\s-])\breport\s+(\d+)\s+passed\b"), "smoke", "report N passed"),
    ]

    DOCS = [
        # (relpath-from-project-root, optional clip-before-marker)
        ("CLAUDE.md", None),
        ("README.md", None),
        (os.path.join("dev", "README.md"), None),
        (os.path.join("dev", "HANDOFF.md"), "## 15. Live state"),
    ]

    stale = []

    for relpath, clip_header in DOCS:
        fpath = os.path.join(PROJECT_ROOT, relpath)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        if clip_header:
            idx = content.find(clip_header)
            if idx != -1:
                content = content[:idx]
        for pattern, key, friendly in PATTERNS:
            for m in pattern.finditer(content):
                claimed = int(m.group(1))
                truth = GROUND_TRUTH[key]
                if claimed != truth:
                    rel_line = content[:m.start()].count("\n") + 1
                    stale.append(
                        f"{relpath} line {rel_line}: '{friendly}' shows "
                        f"{claimed}, ground truth is {truth} ({key} count)"
                    )

        # Self-paired `N/N` gate-result form (Rule 23). A self-paired `N/N` in a
        # prose doc is, by construction, a gate result — so its value must be
        # one of the two live gate counts: pre-commit (self-derived) or smoke.
        # Set-membership (not a single (regex, key) tuple) is required because
        # the slash form is gate-ambiguous between the two. Distinct-pair forms
        # like ISO `19115/19139` (g1 != g2) are skipped, so XSD refs don't
        # false-positive. Known limitation: a precommit phrase mis-written with
        # the smoke count (or vice versa) passes — both are valid members, so
        # cross-gate confusion is not caught, only out-of-range staleness.
        valid_pairs = {GROUND_TRUTH["precommit"], GROUND_TRUTH["smoke"]}
        for m in re.finditer(r"(?<![Pp]ass[\s-])\b(\d+)/(\d+)\b", content):
            if m.group(1) != m.group(2):
                continue  # only self-paired N/N are gate results
            claimed = int(m.group(1))
            if claimed not in valid_pairs:
                rel_line = content[:m.start()].count("\n") + 1
                stale.append(
                    f"{relpath} line {rel_line}: gate-result 'N/N' shows "
                    f"{claimed}/{claimed}, expected one of {sorted(valid_pairs)} "
                    f"(pre-commit {GROUND_TRUTH['precommit']} / smoke {GROUND_TRUTH['smoke']})"
                )

    assert not stale, (
        "doc count-phrase freshness drift (.md surfaces — Rule 23):\n      "
        + "\n      ".join(stale)
        + f"\n      Ground truth: foundational={GROUND_TRUTH['foundational']}, "
        f"validator_total={GROUND_TRUTH['validator_total']}, "
        f"validator_per_feature={GROUND_TRUTH['validator_per_feature']}, "
        f"validator_structural={GROUND_TRUTH['validator_structural']}, "
        f"atypes={GROUND_TRUTH['atypes']}, "
        f"xsl_templates={GROUND_TRUTH['xsl_templates']}, "
        f"svg_symbols={GROUND_TRUTH['svg_symbols']}. "
        "Refresh the cited count or update _COUNT_GROUND_TRUTH if the truth changed. "
        "Added pass 259 (Rule 23 — single-source-or-gate; closes the .md gate-blind class)."
    )

    # === Volatile-fact single-source enforcement (Rule 23) ===
    # The HTML file-size and APP_VERSION drifted repeatedly despite discipline —
    # HANDOFF § 3 table headers went stale on the line count; CLAUDE.md kept a
    # stale `APP_VERSION = "..."` for several versions — because (unlike
    # counts/anchors/narrative, watched by checks #11-14) nothing watched THESE
    # two. This block watches them: the current line count + the APP_VERSION
    # value may live ONLY in the HANDOFF § 15 Live State footer (human single
    # source) + the § 3 tour anchors (gate-protected by check #11, which carry no
    # `lines` word so they are exempt below). Restating either in scanned prose,
    # or letting the footer drift from reality, fails.
    vfs = []
    with open(HTML, encoding="utf-8") as f:
        # `wc -l` convention (count newlines) — matches the footer figure + check
        # #11's anchor. NOT `+ 1`: a trailing newline would then overcount by one
        # and the `<actual> lines` restatement scan (b) would key on the wrong
        # number (caught when proving this gate via a planted `10888 lines`).
        actual_lines = f.read().count("\n")
    # (a) the single-source footer must match reality (so it can't go stale the way
    #     the § 3 table headers silently did before this block existed).
    with open(os.path.join(PROJECT_ROOT, "dev", "HANDOFF.md"), encoding="utf-8") as f:
        _handoff_full = f.read()
    _fm = re.search(r"\|\s*HTML file size[^|]*\|\s*~?(\d[\d,]*)\s+lines", _handoff_full)
    if not _fm:
        vfs.append("dev/HANDOFF.md: the § 15 Live State 'HTML file size' footer row is missing — it is the single source for the current line count (Rule 23).")
    elif abs(int(_fm.group(1).replace(",", "")) - actual_lines) > 10:
        vfs.append(f"dev/HANDOFF.md: 'HTML file size' footer says ~{_fm.group(1)} but the file is {actual_lines} lines (drift > 10) — refresh the single source.")
    # (a2/a3) the § 15 rule-count and smoke rows sit below check #13's clip with no
    # other gate — pin both to _COUNT_GROUND_TRUTH so they can never silently drift
    # the way the sibling footer rows once did.
    _rm = re.search(r"\|\s*Validator rule count\s*\|\s*(\d+)\s*\((\d+)\s+per-feature\s*\+\s*(\d+)\s+structural\s*\+\s*(\d+)\s+exchange-set\)", _handoff_full)
    if not _rm:
        vfs.append("dev/HANDOFF.md: the § 15 'Validator rule count | N (X per-feature + Y structural + Z exchange-set)' footer row is missing or reformatted (Rule 23 gate, pass 575; exchange-set component added pass 637).")
    elif (int(_rm.group(1)), int(_rm.group(2)), int(_rm.group(3)), int(_rm.group(4))) != (_COUNT_GROUND_TRUTH["validator_total"], _COUNT_GROUND_TRUTH["validator_per_feature"], _COUNT_GROUND_TRUTH["validator_structural"], _COUNT_GROUND_TRUTH["validator_exchange_set"]):
        vfs.append(f"dev/HANDOFF.md: § 15 'Validator rule count' row says {_rm.group(1)} ({_rm.group(2)}+{_rm.group(3)}+{_rm.group(4)}) but ground truth is {_COUNT_GROUND_TRUTH['validator_total']} ({_COUNT_GROUND_TRUTH['validator_per_feature']}+{_COUNT_GROUND_TRUTH['validator_structural']}+{_COUNT_GROUND_TRUTH['validator_exchange_set']}).")
    _sm = re.search(r"\|\s*Browser smoke invariants\s*\|\s*(\d+)", _handoff_full)
    if not _sm:
        vfs.append("dev/HANDOFF.md: the § 15 'Browser smoke invariants | N' footer row is missing or reformatted (Rule 23 gate, pass 575).")
    elif int(_sm.group(1)) != _COUNT_GROUND_TRUTH["smoke"]:
        vfs.append(f"dev/HANDOFF.md: § 15 'Browser smoke invariants' row says {_sm.group(1)} but ground truth is {_COUNT_GROUND_TRUTH['smoke']}.")
    # (a4) the § 15 'Foundational-rule count' row — same below-the-clip gap as a2/a3;
    #      pinned by nothing until this block.
    _fr = re.search(r"\|\s*Foundational-rule count\s*\|\s*(\d+)", _handoff_full)
    if not _fr:
        vfs.append("dev/HANDOFF.md: the § 15 'Foundational-rule count | N' footer row is missing or reformatted (Rule 23 gate, pass 582).")
    elif int(_fr.group(1)) != _COUNT_GROUND_TRUTH["foundational"]:
        vfs.append(f"dev/HANDOFF.md: § 15 'Foundational-rule count' row says {_fr.group(1)} but ground truth is {_COUNT_GROUND_TRUTH['foundational']}.")
    # (b) no OTHER doc may restate the current line count (`<actual> lines`) or an
    #     APP_VERSION value. Keyed on the actual count so historical figures
    #     (18,830 / 9,757) and deltas (~1,100 lines) are not flagged.
    _count_re = re.compile(r"~?\s*(?:" + re.escape(format(actual_lines, ",")) + r"|" + re.escape(str(actual_lines)) + r")\s+lines\b")
    _ver_re = re.compile(r'APP_VERSION\s*=\s*"[0-9]')
    for relpath, clip_header in DOCS:
        fpath = os.path.join(PROJECT_ROOT, relpath)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        if clip_header:
            idx = content.find(clip_header)
            if idx != -1:
                content = content[:idx]
        for mm in _count_re.finditer(content):
            rel_line = content[:mm.start()].count("\n") + 1
            vfs.append(f"{relpath} line {rel_line}: restates the current line count ('{mm.group(0).strip()}') — single-source it to the § 15 Live State footer (Rule 23).")
        for mm in _ver_re.finditer(content):
            rel_line = content[:mm.start()].count("\n") + 1
            vfs.append(f"{relpath} line {rel_line}: restates an `APP_VERSION` value — the version lives in the HTML const + the § 15 Live State footer only (Rule 23).")
    assert not vfs, (
        "volatile-fact single-source drift (Rule 23 — file-size / APP_VERSION):\n      "
        + "\n      ".join(vfs)
        + "\n      These two facts drifted repeatedly across passes 280-284; they now live in exactly one "
        "human source (HANDOFF § 15 Live State footer) + the gate-protected § 3 tour anchor. Added pass 285."
    )


def check_sample_data_files_exist():
    """Check 10: walk the sample-data table in dev/README.md and assert each
    backticked filename actually exists on disk in `dev/sample-data/`.

    Without it the gate had no way to detect doc-vs-file drift if a fixture
    was renamed/deleted without updating README — a cheap defense-in-depth
    guard.

    Scoping: extracts ONLY the "## `dev/sample-data/` ..." section so the
    check doesn't false-positive on backticked filenames mentioned in other
    sections (e.g. spec-sources/, pdf-extracts/).
    """
    _needs_dev_docs("dev/README.md")
    sample_dir = os.path.join(PROJECT_ROOT, "dev", "sample-data")
    if not os.path.isdir(sample_dir):
        # Sample-data dir doesn't exist — nothing to check; skip rather than fail.
        return
    with open(DEV_README, encoding="utf-8") as f:
        txt = f.read()
    # Find the sample-data section header
    sec_re = re.compile(r"^##\s+`?dev/sample-data/?`?", re.MULTILINE)
    sm = sec_re.search(txt)
    if not sm:
        return  # section not found — opt-in on this doc shape
    sec_start = sm.start()
    # Section ends at the next `##` heading at the same depth (or end-of-file)
    next_re = re.compile(r"^##\s", re.MULTILINE)
    nm = next_re.search(txt, sm.end())
    sec_end = nm.start() if nm else len(txt)
    section = txt[sec_start:sec_end]
    # Find table-row backticked filenames with .gml/.xml/.zip extension
    referenced = set()
    for m in re.finditer(r"\|\s*`([^`]+\.(?:gml|xml|zip))`\s*\|", section):
        referenced.add(m.group(1))
    if not referenced:
        return
    # Verify each referenced file exists on disk
    missing = []
    for fname in sorted(referenced):
        path = os.path.join(sample_dir, fname)
        if not os.path.exists(path):
            missing.append(fname)
    assert not missing, (
        "sample-data files referenced in dev/README.md but missing on disk:\n      "
        + "\n      ".join(missing)
        + f"\n      Either restore the file under {sample_dir} or remove the "
        "row from dev/README.md. Round-6 R6-D-5 — see pass 135 narrative."
    )


def check_rule21_narrative_purity():
    """Check 14 (Rule 21 enforcement): scan s201_aton_studio.html inline
    comments for log-style narrative markers — the residue a full-file log
    purge is meant to eliminate.

    Prose guidance in CLAUDE.md + HANDOFF describing the residues to avoid
    ("Pass-N (Agent X CATEGORY-N)", "pre-Session-N", "Path B Phase N",
    "Agent-B BUG #N", ...) proved hortative, not gating: dozens of such
    residues survived several cleanup passes before an audit caught them.
    This check gates the discipline mechanically: any HTML inline-comment
    introduction of a pass-N / Agent-X / Session-N / audit-finding /
    quoted-user-dialogue marker fails the gate immediately. The patterns are
    explicit (specific narrative tokens), not heuristic (so no false
    positives on legitimate prose like "FC line 12200" or "the parser at
    line ~5500").

    Scope:
      - s201_aton_studio.html only (the source file; comments in CHANGELOG
        + HANDOFF historical rows are by design — Rule 21 says log-style
        content belongs in CHANGELOG/HANDOFF, NOT in the source).

    Pattern classes (see PATTERNS below for the exact regexes):
      - pass attribution: `Pass-NNN (Agent X ...)`, `Pass-NNN:` / `Pass NNN:`,
        bare `Pass-NNN` / `pass-NNN` / `pass NNN` (3+ digits), `pre-pass-N`
      - agent attribution: `Agent X`, `Agent-X`, `Agent-X BUG #N`,
        `Agent X BUG-N`, `BUG #N`
      - audit-campaign markers: `finding GAP #N`, `finding-N`, `Finding #N`,
        `GAP #N` / `GAP C-N`, `Round-N`, `deep-scan`,
        `Phase N IHO/IALA audit`, `Path B Phase N`, `pre-Session-N`
      - quoted user dialogue: `per (the) user`, `user said`, `the user
        asked`, `user reported`, `user "..."`

    Exemptions / NOT flagged:
      - two-digit pass references (`pass 5/5`, foundational-rule numbers) —
        the bare-form patterns require 3+ digits.
      - the `addedPass:N` field INSIDE the FOUNDATIONAL_RULES const literal
        (intentional metadata; the literal is excluded from the scan).
      - FC line references like `FC line 12200` (Rule 5 spec citation).
      - everything ABOVE `const FOUNDATIONAL_RULES = [` — the HTML preface
        `<!-- ... -->` block that describes the project at the top of the
        file. Everything below the literal is the JS body where Rule 21
        fully applies.

    Future: if new narrative-residue classes surface, add patterns here.
    """
    fpath = HTML
    if not os.path.isfile(fpath):
        return
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
    # Scope: HTML inline JS-body comments. Two regions are exempt:
    #
    #   (1) Everything ABOVE `const FOUNDATIONAL_RULES = [` — this is the
    #       HTML <!-- preface --> block, which is the canonical "what is
    #       this app" header AND a deliberate snapshot of project history
    #       (kept for offline-clone scenarios by design).
    #
    #   (2) The FOUNDATIONAL_RULES literal `[...]` block itself — its
    #       `summary:` fields are curated rule documentation, not inline
    #       comments, and carry an intentional `addedPass:N` metadata field.
    #       The summaries themselves are kept free of pass-attribution prose:
    #       illustrative examples are phrased generically (e.g. Rule 23 cites
    #       "a CLAUDE.md architecture table that drifted by hundreds of lines"
    #       — the failure mode, not "pass N did X"). The canonical authority
    #       for these summaries is dev/foundational-rules.json; both surfaces
    #       MUST agree, and the smoke test verifies entry count + shape.
    #
    # All other JS-body comments + string literals + code are scanned.
    m_open = re.search(r"^const\s+FOUNDATIONAL_RULES\s*=\s*\[", content, re.MULTILINE)
    if m_open:
        rest = content[m_open.end():]
        # Find the matching `];` on its own line (the literal closing — the
        # FOUNDATIONAL_RULES const literal holds one entry per rule, each ending
        # in `},`, with `];` only at the very end of the array).
        m_close = re.search(r"^\];", rest, re.MULTILINE)
        body_start = m_open.end() + (m_close.end() if m_close else 0)
    else:
        body_start = 0
    body = content[body_start:]
    line_offset = content[:body_start].count("\n")

    PATTERNS = [
        (re.compile(r"Pass-?\d+\s*\([Aa]gent\s+[A-Z]"), "Pass-N (Agent X ...)"),
        (re.compile(r"Pass-?\d+:"), "Pass-N: prefix narrative"),
        # Space-form colon prefix ("Pass 269:" — a space between "Pass" and the
        # digits, which the `Pass-?\d+:` pattern above doesn't match: `-?` is an
        # optional hyphen, not optional whitespace).
        (re.compile(r"Pass\s+\d+:"), "Pass N: (space-form) prefix narrative"),
        # Lowercase "pre-pass-N" narrative residues ("pre-pass-181 beacon viewingGroup
        # fix", "Pre-pass-250 the predicates checked", "pre-pass-242 free-text shape")
        # — log-style narrative belonging in CHANGELOG, not HTML comments. The
        # `pre-Session-N` pattern further down doesn't cover this form (distinct
        # narrative class).
        (re.compile(r"[Pp]re-pass-?\d+"), "pre-pass-N narrative residue"),
        # Bare "Pass-NNN " / "pass-NNN " / "pass NNN " forms (no colon), which the
        # colon-only patterns above miss: "(pass-230)" test-title suffixes, "from
        # pass-235 xlink:href fix" cross-references, "Pass-249 defensive ..." prefixes.
        # These are pure attribution that belongs in CHANGELOG — strip while keeping
        # the WHY content (e.g. "split-and-validate pattern from pass-230" →
        # "split-and-validate pattern"; the WHY is the pattern name, not the pass
        # attribution).
        # `\d{3,}` (3+ digits) excludes legitimate uses like "pass 5/5" or 2-digit
        # foundational-rule references, and avoids matching `addedPass: 22` inside
        # the FOUNDATIONAL_RULES literal (`\b` before "Pass" requires non-word char
        # boundary — "added" + "Pass" has no boundary since both are word chars).
        (re.compile(r"\bpass[\s-]\d{3,}"), "lowercase pass-NNN narrative"),
        (re.compile(r"\bPass[\s-]\d{3,}"), "Pass-NNN narrative (no colon)"),
        # Bare "Agent X" attribution — the BUG-framing forms below (Agent-X BUG #N /
        # Agent X BUG-N) don't cover residues like "(Agent I/K MED)", "Closes Agent P
        # HIGH-3", "Agent D MEDIUM-1"; all agent attribution belongs in CHANGELOG. Word
        # boundary `\b` after the letter prevents matching legitimate names like
        # "AgentBased" or "AgentTracker".
        (re.compile(r"\bAgent\s+[A-Z]\b"), "Agent X attribution"),
        (re.compile(r"Agent-[A-Z]\s+BUG\s*#\d"), "Agent-X BUG #N attribution"),
        (re.compile(r"Agent\s+[A-Z]\s+BUG-?\d"), "Agent X BUG-N attribution"),
        (re.compile(r"\bBUG\s*#\d"), "BUG #N attribution"),
        (re.compile(r"pre-Session-\d"), "pre-Session-N marker"),
        (re.compile(r"Path\s+B\s+Phase\s+\d"), "Path B Phase N marker"),
        (re.compile(r"finding\s+GAP\s*#\d", re.IGNORECASE), "finding GAP #N attribution"),
        # lowercase hyphen-digit audit-finding attribution `finding-N` (e.g. "finding-6 fix:",
        # "(finding-6)"). The `finding GAP #N` pattern above requires the literal "GAP" + "#",
        # so this no-GAP no-# form slipped the gate — 5 `finding-6` markers from an earlier
        # audit lived ungated in the JS body. `\b` + required digit means it won't collide with
        # FC spec citations ("FC line 6") or words like "wayfinding".
        (re.compile(r"\bfinding-\d", re.IGNORECASE), "finding-N audit attribution"),
        (re.compile(r"Phase\s+\d\s+IHO/IALA\s+(audit|validator-audit)", re.IGNORECASE), "Phase N IHO/IALA audit marker"),
        # Verbatim user-DIALOGUE attribution class — comments that quote the
        # user ("Per user "...", "User said ...", "the user asked", "user reported", "per user
        # request") instead of stating the durable design rationale. Per Rule 21 the dialogue
        # belongs in dev/CHANGELOG.md. Patterns are NARROW so legitimate behaviour descriptions
        # ("as the user scrolls", "a user wants to nil a field", "stay the user's call", "the user
        # can flip the side") are NOT flagged — they describe behaviour, not quoted dialogue. The
        # trailing class [\s,"*] on the per-user form excludes "user-agent" / "user-defined", and
        # the `\s+"` on the quote form excludes string literals like "user" (no space before the quote).
        (re.compile(r'[Pp]er (the )?user[\s,"*]'), "per-user dialogue attribution"),
        (re.compile(r"\buser said\b", re.IGNORECASE), "User-said dialogue attribution"),
        (re.compile(r"\bthe user asked\b", re.IGNORECASE), "the-user-asked attribution"),
        (re.compile(r"\buser reported\b", re.IGNORECASE), "user-reported attribution"),
        (re.compile(r'\buser\s+\*?"'), "verbatim user-quote attribution"),
        # Audit-attribution classes that survived in JS-body comments (the portrayal
        # SYMBOL_RULES block, RULES headers, generator FT-gates, Builder restore
        # comments) because the patterns above catch only the compound "Agent-X BUG #N"
        # + space-form "Agent X" forms — NOT the bare audit-finding, audit-campaign,
        # dash-form-agent, audit-round, or GAP markers. All belong in dev/CHANGELOG.md
        # + the audit ledgers (dev/*-findings-*.md), NOT the source. Rule citations
        # (Rule 8) + spec citations (FC 9332) are KEPT — only the audit attribution is
        # stripped.
        (re.compile(r"Finding\s*#\d"), "Finding #N audit attribution"),
        (re.compile(r"deep-scan"), "deep-scan audit-campaign attribution"),
        (re.compile(r"\bAgent-[A-Z]\b"), "Agent-X (dash form) attribution"),
        (re.compile(r"\bRound[\s-]\d+"), "Round-N audit marker"),
        (re.compile(r"\bGAPs?\s*(#\d|C\d)"), "GAP-N / GAP C-N audit attribution"),
    ]
    residues = []
    for pattern, friendly in PATTERNS:
        for m in pattern.finditer(body):
            rel_line = body[:m.start()].count("\n") + 1
            abs_line = rel_line + line_offset
            # Capture surrounding context for the error message (max 80 chars)
            ctx_start = max(0, m.start() - 30)
            ctx_end = min(len(body), m.end() + 30)
            ctx = body[ctx_start:ctx_end].replace("\n", " ").strip()
            residues.append(f"HTML line {abs_line}: {friendly} — '...{ctx}...'")

    assert not residues, (
        "Rule-21 narrative residue in s201_aton_studio.html inline comments "
        "(log-style markers belong in CHANGELOG/HANDOFF, NOT the source file):\n      "
        + "\n      ".join(residues[:200])
        + (f"\n      ...and {len(residues)-200} more" if len(residues) > 200 else "")
        + "\n      Rewrite each comment to describe WHAT the code does + WHY (durable parts) "
        "but not WHEN/WHO (log-style — belongs in dev/CHANGELOG.md). "
        "Added pass 276 (Rule 21 enforcement gate — closes the gate-blind class "
        "user flagged in pass 276 'rule 7 and it look like updated CLAUDE.md "
        "and other dev docs did not do what they supposed to do')."
    )


def check_csv_to_s201_conformance():
    """Check 15: run the CSV->S-201 converter (dev/scripts/csv_to_s201.py) on the bundled
    fictional self-test fixture and assert the emitted GML carries the FC-mandatory attributes
    the converter defaults + drops the extraneous DII fields. This LOCKS the converter's
    conformance guarantees so a regression cannot silently re-introduce schema-invalid output
    the app's own validator would reject (GML-STR-11/12, S201-SHP-01/04, S201-LGT-12,
    S201-FEA-02/06, S201-REL-03). Structural presence-checks only (no FC enum lists duplicated
    here, Rule 23); the exact enum-label correctness is verified out-of-band against the
    in-browser validator."""
    import subprocess
    import tempfile
    import xml.etree.ElementTree as ET
    conv = os.path.join(_SCRIPT_DIR, "csv_to_s201.py")
    fixture = os.path.join(_SCRIPT_DIR, "csv_to_s201_selftest.csv")
    if not (os.path.exists(conv) and os.path.exists(fixture)):
        raise SkippedCheck("csv_to_s201.py or its self-test fixture is missing")
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "out.gml")
        r = subprocess.run([sys.executable, conv, fixture, out],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            raise AssertionError("converter run failed: " + ((r.stderr or r.stdout) or "")[:300])
        with open(out, encoding="utf-8") as fh:
            text = fh.read()
    root = ET.fromstring(text)   # must be well-formed
    # Namespace-agnostic local-name matching: the converter emits some elements prefixed
    # (S201:/S100:) and the members/DII wrappers bare, exactly as the app's own parser accepts.
    def _ln(e):
        return e.tag.split("}")[-1]

    dii = next((c for c in root if _ln(c) == "DatasetIdentificationInformation"), None)
    assert dii is not None, "DII block missing from converter output"
    dii_tags = {_ln(c) for c in dii}
    assert "datasetLanguage" in dii_tags, \
        "converter DII missing mandatory datasetLanguage (GML-STR-11 regressed)"
    extraneous = dii_tags & {"metadataLanguage", "metadataCharacterEncoding"}
    assert not extraneous, \
        f"converter DII carries extraneous field(s) {sorted(extraneous)} (GML-STR-12 regressed)"

    members = next((c for c in root if _ln(c) == "members"), None)
    assert members is not None, "<members> block missing from converter output"
    problems = []
    n_parents = 0
    for feat in list(members):
        ln = _ln(feat)
        tags = [_ln(c) for c in feat]
        if ln.endswith("Buoy"):
            n_parents += 1
            if "buoyShape" not in tags:
                problems.append(f"{ln} missing mandatory buoyShape (S201-SHP-01)")
        if ln.endswith("Beacon"):
            n_parents += 1
            if "beaconShape" not in tags:
                problems.append(f"{ln} missing mandatory beaconShape (S201-SHP-04)")
        if ln.startswith("Light"):
            if "colour" not in tags:
                problems.append(f"{ln} missing mandatory colour (S201-LGT-12)")
            if "featureName" in tags:
                problems.append(f"{ln} child repeats parent featureName (S201-REL-03)")
        if ln == "Topmark" and "featureName" in tags:
            problems.append("Topmark child repeats parent featureName (S201-REL-03)")
        if "SpecialPurpose" in ln and "categoryOfSpecialPurposeMark" not in tags:
            problems.append(f"{ln} missing mandatory categoryOfSpecialPurposeMark (S201-FEA-06)")
        if "Lateral" in ln and "categoryOfLateralMark" not in tags:
            problems.append(f"{ln} missing mandatory categoryOfLateralMark (S201-FEA-02)")
    assert n_parents >= 10, \
        f"converter emitted only {n_parents} parent marks — the self-test fixture did not convert"
    assert not problems, "csv_to_s201.py emitted non-conformant S-201 (pass-550 fix regressed):\n      " + \
        "\n      ".join(problems)


def check_bundled_asset_count_phrases():
    """Check 16 (Rule 23): bundled-asset facts stated in the docs must match the
    assets on disk. The Leaflet version and the SVG / XSL / S-62-code counts were
    restated across README.md + dev/HANDOFF.md — accurate at the time but with no
    gate, the Rule-23 ungated-duplication class. Gated families (README.md,
    dev/README.md, dev/HANDOFF.md):
      - `Leaflet X.Y.Z`  vs the version in lib/leaflet/leaflet.js's @preserve banner
      - `N SVG files` / `N SVG symbols` / `N SVGs` / `N symbols + fonts`
                         vs the count of Annex_D/Symbols/*.svg
      - `N XSL`          vs the count of Annex_D/Rules/*.xsl
      - `N codes`        vs the data-row count of the S-62 producer-code CSV
        ("S-62 producer codes" never matches — the digits are not adjacent to
        the word `codes`, so no special-casing is needed). In a snapshot tree
        the CSV is not shipped and this family is skipped.
    """
    import glob as _glob
    leaflet_js = os.path.join(PROJECT_ROOT, "lib", "leaflet", "leaflet.js")
    assert os.path.isfile(leaflet_js), "lib/leaflet/leaflet.js missing"
    with open(leaflet_js, encoding="utf-8", errors="replace") as fh:
        banner = fh.read(300)
    m = re.search(r"Leaflet (\d+\.\d+\.\d+)", banner)
    assert m, "lib/leaflet/leaflet.js banner carries no `Leaflet X.Y.Z` version"
    leaflet_ver = m.group(1)
    svg_count = len(_glob.glob(os.path.join(PROJECT_ROOT, "Annex_D", "Symbols", "*.svg")))
    xsl_count = len(_glob.glob(os.path.join(PROJECT_ROOT, "Annex_D", "Rules", "*.xsl")))
    csv_path = os.path.join(PROJECT_ROOT, "dev", "spec-sources", "iho-additional",
                            "S-62_ProducerCodes.csv")
    if _snapshot_tree() and not os.path.isfile(csv_path):
        # The snapshot ships no reference material (dev/spec-sources holds only
        # MANIFEST.md), so the `N codes` phrase has no ground truth there; the
        # SVG / XSL / Leaflet phrases are still checked below.
        s62_count = None
    else:
        assert os.path.isfile(csv_path), "S-62_ProducerCodes.csv missing"
        with open(csv_path, encoding="utf-8", errors="replace") as fh:
            s62_count = sum(1 for ln in fh if ln.strip()) - 1  # minus header row
        assert s62_count > 0, f"asset scan degenerate (s62={s62_count})"
    assert svg_count > 0 and xsl_count > 0, \
        f"asset scan degenerate (svg={svg_count}, xsl={xsl_count})"
    stale = []
    for rel in ("README.md", os.path.join("dev", "README.md"), os.path.join("dev", "HANDOFF.md")):
        fpath = os.path.join(PROJECT_ROOT, rel)
        if not os.path.isfile(fpath):
            continue
        for lineno, line in enumerate(open(fpath, encoding="utf-8").read().splitlines(), 1):
            for vm in re.finditer(r"Leaflet (\d+\.\d+\.\d+)", line):
                if vm.group(1) != leaflet_ver:
                    stale.append(f"{rel} line {lineno}: 'Leaflet {vm.group(1)}' vs bundled leaflet.js {leaflet_ver}")
            for cm in re.finditer(r"\b(\d+) (?:SVG files|SVG symbols|SVGs\b|symbols \+ fonts)", line):
                if int(cm.group(1)) != svg_count:
                    stale.append(f"{rel} line {lineno}: '{cm.group(0)}' vs {svg_count} files in Annex_D/Symbols/")
            for xm in re.finditer(r"\b(\d+) XSL\b", line):
                if int(xm.group(1)) != xsl_count:
                    stale.append(f"{rel} line {lineno}: '{xm.group(0)}' vs {xsl_count} files in Annex_D/Rules/")
            for sm in re.finditer(r"\b(\d+) codes\b", line):
                if s62_count is not None and int(sm.group(1)) != s62_count:
                    stale.append(f"{rel} line {lineno}: '{sm.group(0)}' vs {s62_count} S-62 CSV data rows")
    assert not stale, "bundled-asset phrases out of sync with disk (Rule 23):\n      " + \
        "\n      ".join(stale)


PDF_EXTRACTS_MANIFEST_SCRIPT = os.path.join(_SCRIPT_DIR, "generate-pdf-extracts-manifest.py")


def check_pdf_extracts_manifest():
    """Check 17 (Rule 5/8 — the citation trust anchor): every file in
    dev/pdf-extracts/ must match dev/pdf-extracts/MANIFEST.sha256.

    The extract corpus is the grep-able ground truth behind hundreds of
    validator-rule `ref` citations and inline spec comments (cited by file +
    line number). Before this check it was the one wholly-ungated layer of the
    verification chain: a silent re-extraction, truncated regeneration, or
    re-bundle would invalidate the cited line numbers with nothing to detect
    it. Any corpus change now blocks the gate until the manifest is
    deliberately regenerated (`python dev/scripts/generate-pdf-extracts-manifest.py`),
    turning corpus changes into visible, reviewed acts. Residual (disclosed in
    HANDOFF § 13): the manifest freezes the extracts, not the source PDFs — a
    PDF re-bundled while its extract stays untouched does not trip this."""
    if _snapshot_tree() and not os.path.isdir(os.path.join(PROJECT_ROOT, "dev", "pdf-extracts")):
        raise NotApplicable("snapshot tree cut without dev/pdf-extracts/ — nothing to verify")
    import subprocess
    if not os.path.exists(PDF_EXTRACTS_MANIFEST_SCRIPT):
        # Same SkippedCheck doctrine as check 5 — a check that cannot run must
        # not report as a pass.
        raise SkippedCheck(
            f"manifest script missing at {PDF_EXTRACTS_MANIFEST_SCRIPT} — corpus "
            f"integrity never verified; restore it or remove this check"
        )
    result = subprocess.run(
        [sys.executable, PDF_EXTRACTS_MANIFEST_SCRIPT, "--check"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0, (
        f"pdf-extracts corpus drifted from MANIFEST.sha256 — if deliberate, regenerate: "
        f"`python dev/scripts/generate-pdf-extracts-manifest.py`. Checker output:\n"
        f"{(result.stderr or result.stdout).strip()}"
    )


# Run all checks
check("APP_VERSION consistency (HTML JS vs preface)", check_app_version_consistency)
check("foundational-rules.json shape", check_foundational_rules_json_shape)
check("FOUNDATIONAL_RULES const length matches JSON", check_foundational_rules_in_app_const_count)
check("pass-count consistency across HANDOFF + README + dev/README", check_pass_count_consistency)
check("validator-rules.json in sync with in-app RULES (pass 116)", check_validator_rules_json_sync)
check("inline <script> JS syntax via V8 (pass 117)", check_inline_script_js_syntax)
check("intra-section pass-count staleness in HANDOFF.md (pass 123)", check_intra_section_staleness)
check("function-anchor freshness in HANDOFF.md Key functions (pass 129)", check_function_anchor_freshness)
check("constants-table anchor freshness in HANDOFF.md (pass 129)", check_constants_anchor_freshness)
check("sample-data files referenced in dev/README.md exist on disk (pass 135)", check_sample_data_files_exist)
check("Source-file tour table anchor freshness (pass 255)", check_source_file_tour_anchor_freshness)
check("count-phrase freshness in HTML <script> + .py files (pass 257)", check_count_phrase_freshness)
check("doc count-phrase freshness in .md surfaces (pass 259, Rule 23)", check_doc_count_phrase_freshness)
check("Rule-21 narrative-residue purity in s201_aton_studio.html (pass 276)", check_rule21_narrative_purity)
check("csv_to_s201.py output conformance self-test (pass 550)", check_csv_to_s201_conformance)
check("bundled-asset count/version phrases match disk (pass 570, Rule 23)", check_bundled_asset_count_phrases)
check("pdf-extracts integrity manifest (Rule 5/8 citation trust anchor)", check_pdf_extracts_manifest)

# Report
# `_total` is every check() invocation above — passed + failed + skipped. Reporting
# "len(passes)/len(passes)" was self-referential: it printed "N/N passed" for whatever
# N happened to run, so a SKIPPED check (which check() counted as a pass) read as a
# full green gate. The denominator must be the number of checks ATTEMPTED.
#
# A DELETED check is a different failure mode and is already gated elsewhere: removing
# a `check(...)` line drops `_self_count_precommit_checks()` to N-1, and check #13
# (doc count-phrase freshness, Rule 23) then fails because dev/README.md's "N/N" and
# "N-check gate" phrases no longer match the self-count. Verified 2026-07-08 by deleting
# a check() invocation in a temp copy: check #13 reported the dev/README.md 'N-check gate'
# phrase as one above the (now smaller) ground truth.
# Do NOT add a `_COUNT_GROUND_TRUTH["precommit_checks"]` constant to "fix" this — it would
# duplicate the self-count and rot independently, which is precisely what Rule 23 forbids.
_total = len(passes) + len(failures) + len(skips)  # attempted; not-applicable checks are listed, not counted
_na_note = (f" ({len(not_applicable)} not applicable in this snapshot tree — development docs not shipped)"
            if not_applicable else "")
print(f"\n=== S-201 AtoN Studio pre-commit smoke gate ===\n")
for p in passes:
    print(f"  [pass] {p}")
for s in skips:
    print(f"  [SKIP] {s}")
for n in not_applicable:
    print(f"  [n/a ] {n}")
for f in failures:
    print(f"  [FAIL] {f}")

print()
if failures or skips:
    if failures:
        print(f"[X] Pre-commit blocked: {len(failures)} check(s) failed.")
    if skips:
        print(f"[X] Pre-commit blocked: {len(skips)} check(s) could not run (a skip is not a pass).")
    print(f"  {len(passes)}/{_total} static checks passed.{_na_note}")
    print("  Fix the issue(s) and re-stage. To bypass (NOT recommended), use 'git commit --no-verify'.")
    print("  For the full smoke gate, open the app in a browser and click 'Run tests' on the Validator tab.")
    sys.exit(1)
else:
    print(f"[OK] Pre-commit OK: {len(passes)}/{_total} static checks passed.{_na_note}")
    print("  Reminder: also run the full browser smoke gate (Validator tab -> Run tests) before declaring a pass complete (Rule 11).")
    sys.exit(0)
