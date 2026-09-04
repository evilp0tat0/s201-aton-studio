#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Generate dev/validator-rules.json from the in-app RULES array.
#
# Per Rule 19 (Machine-readable foundational rules), extended to the validator
# corpus: the canonical authoring surface is the inline RULES array in
# s201_aton_studio.html (grep `const RULES=[` for its current position —
# the file grows every pass, so no line number is stated here). The
# downstream JSON mirror exists for external tooling that wants to query the
# rule corpus without parsing JS.
#
# Approach:
#   1. Read s201_aton_studio.html
#   2. Find the RULES array bounds via `const RULES=` + matching `];` using
#      a brace-counting state machine that respects string/comment/regex
#      boundaries
#   3. Walk each top-level rule entry (each starts with `{` at depth 1)
#   4. For each entry, extract serializable fields via targeted regex:
#        id, ref, s (-> severity), m (-> message), noFix,
#        expected.kind, expected.values (literal string array) or
#        expected.valuesConst (+ valuesExclude for the `CONST.filter(x=>x!=="lit")`
#        form), expected.regex, expected.description, expected.min/max,
#        fix.field, fix.inputType, fix.label, fix.placeholder, fix.kind,
#        fix.wrapper, fix.target, fix.options (literal) or fix.optionsConst
#        (+ optionsExclude), fix.childType, fix.skipFts, fix.skipNote,
#        fix.fields (compound multi-field presets, each {field, wrapper?, value}),
#        fix.keys / fix.keysConst, fix.min, fix.max, fix.step (number OR the
#        "any" string form), fix.unit
#      Skip (deliberately not mirrored — functions, and their presence is
#      already smoke-locked in-app by the Rule-16 census):
#        t (validator predicate function)
#        actualOf (extractor function)
#      The walkers share the regex-literal tokenizer (_starts_regex/_regex_end)
#      with the structural extractor, and _selftest() re-proves it on every
#      invocation (a walker bug feeds the byte-identity check its own garbled
#      output, so without the self-test it would be gate-invisible).
#   5. Also walk the validateGMLStructure(text) function body for the
#      GML-STR-NN structural rules — these are emitted in a different code
#      shape (push("GML-STR-NN", severity, ref, message, ...) to a results
#      array; sourceLayer "structural").
#   5b. Same walk over validateExchangeSet(ctx) for the exchange-set package
#      corpus (push("S158-PKG-NN"|"S201-ES-NN", …) — sourceLayer "exchange-set");
#      both function-body corpora share one extraction core (extract_push_rules).
#   6. Write the combined corpus to dev/validator-rules.json (per-feature
#      entries in array order, then the structural and exchange-set corpora
#      sorted by id)
#
# Usage:
#   python dev/scripts/generate-validator-rules-json.py            # write file
#   python dev/scripts/generate-validator-rules-json.py --check    # exit non-zero if drift
#
# Per Rule 11 (Smoke-test-or-die) + Rule 13 (Atomic delivery):
#   the pre-commit gate (check #5) calls this script in --check mode to detect
#   drift between the in-app RULES array and the checked-in JSON mirror.
# ---------------------------------------------------------------------------

import json
import os
import re
import sys
from typing import Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HTML_PATH = os.path.join(REPO_ROOT, 's201_aton_studio.html')
JSON_PATH = os.path.join(REPO_ROOT, 'dev', 'validator-rules.json')


# ---------------------------------------------------------------------------
# JS string-literal escape decoder
# ---------------------------------------------------------------------------
# Replaces a naive `s.encode('utf-8').decode('unicode_escape', errors='replace')`
# decode, which double-decoded UTF-8 bytes via Latin-1 reinterpretation —
# every `§` became `Â§`, `–` became `â`, etc., across the whole output corpus.
# Because `--check` (see main()) compares regen-to-file byte-for-byte, such a
# bug is self-consistent and the gate masks it — the mirror looked in sync
# while carrying mojibake.
#
# Why `unicode_escape` is wrong: it's a Python-2-era codec that interprets
# the input as Latin-1 + handles Python-style escapes. When fed UTF-8 bytes
# (e.g. § = 0xC2 0xA7), it decodes byte-by-byte as Latin-1: 0xC2 → Â,
# 0xA7 → §, yielding `Â§`. The intent was to handle JS-style escapes like
# `\"`, `\n`, `\uXXXX` while preserving UTF-8 — exactly what this function does.

def _js_unescape(s: str) -> str:
    """Decode JS string-literal escape sequences while preserving UTF-8.

    Recognized escapes (per ECMAScript 2015 §11.8.4):
      \\n \\t \\r \\b \\f \\v \\0 \\\\ \\" \\' \\`
      \\xHH (2-digit hex)
      \\uHHHH (4-digit hex)
      \\u{HHHHHH} (extended hex, 1-6 digits)
      \\<other> → <other> (unknown escape — strip backslash, keep char)

    Non-escape characters pass through untouched (preserves UTF-8 cleanly).
    """
    if '\\' not in s:
        return s
    out = []
    i = 0
    n = len(s)
    SIMPLE = {'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f',
              'v': '\v', '0': '\0', '\\': '\\', '"': '"', "'": "'", '`': '`'}
    while i < n:
        c = s[i]
        if c != '\\' or i + 1 >= n:
            out.append(c)
            i += 1
            continue
        nxt = s[i + 1]
        if nxt in SIMPLE:
            out.append(SIMPLE[nxt])
            i += 2
        elif nxt == 'u':
            if i + 2 < n and s[i + 2] == '{':
                j = s.find('}', i + 3)
                if j != -1:
                    try:
                        out.append(chr(int(s[i + 3:j], 16)))
                        i = j + 1
                        continue
                    except ValueError:
                        pass
                # malformed \u{...} — keep literal
                out.append(c)
                i += 1
            elif i + 5 < n:
                try:
                    out.append(chr(int(s[i + 2:i + 6], 16)))
                    i += 6
                except ValueError:
                    out.append(c)
                    i += 1
            else:
                out.append(c)
                i += 1
        elif nxt == 'x':
            if i + 3 < n:
                try:
                    out.append(chr(int(s[i + 2:i + 4], 16)))
                    i += 4
                except ValueError:
                    out.append(c)
                    i += 1
            else:
                out.append(c)
                i += 1
        else:
            # Unknown escape — JS behavior: strip backslash, keep next char
            out.append(nxt)
            i += 2
    return ''.join(out)


# ---------------------------------------------------------------------------
# Brace-counter that respects JS string + comment boundaries
# ---------------------------------------------------------------------------

def find_array_bounds(src: str, decl_pattern: str) -> tuple[int, int]:
    """Find the start (just after [) and end (just before ]) of an array
    declared as `const NAME=[ ... ];`. Returns (open_idx, close_idx) where
    src[open_idx:close_idx] is the inner array content."""
    m = re.search(decl_pattern, src)
    if not m:
        raise ValueError(f"declaration pattern not found: {decl_pattern}")
    # Find the [ that starts the array (right after the match)
    open_idx = src.index('[', m.end() - 1)
    # Walk forward, tracking depth, ignoring string/comment contents
    depth = 1  # we're inside the outer [
    i = open_idx + 1
    n = len(src)
    while i < n:
        c = src[i]
        # block comment
        if c == '/' and i + 1 < n and src[i+1] == '*':
            j = src.find('*/', i + 2)
            i = j + 2 if j != -1 else n
            continue
        # line comment
        if c == '/' and i + 1 < n and src[i+1] == '/':
            j = src.find('\n', i + 2)
            i = j + 1 if j != -1 else n
            continue
        # regex literal — the quote/bracket/brace characters inside (e.g. /["']/ or
        # an unbalanced [{]) must not corrupt the string/depth state. Same
        # tokenizer guard extract_push_rules carries; without it the RULES-array
        # walkers treated a regex as plain code, so ONE quote-bearing regex in a
        # predicate collapsed extraction (mutation-verified: the whole per-feature
        # corpus extracted as a single rule).
        if c == '/' and _starts_regex(src, i):
            j = _regex_end(src, i, n)
            if j is not None:
                i = j
                continue
        # double-quoted string
        if c == '"':
            i += 1
            while i < n:
                if src[i] == '\\':
                    i += 2
                    continue
                if src[i] == '"':
                    i += 1
                    break
                i += 1
            continue
        # single-quoted string
        if c == "'":
            i += 1
            while i < n:
                if src[i] == '\\':
                    i += 2
                    continue
                if src[i] == "'":
                    i += 1
                    break
                i += 1
            continue
        # template literal
        if c == '`':
            i += 1
            while i < n:
                if src[i] == '\\':
                    i += 2
                    continue
                if src[i] == '`':
                    i += 1
                    break
                # template literal ${...} interpolation is NOT tracked: the walker
                # just scans to the closing backtick, which is correct as long as
                # no interpolation nests another backtick/template inside. RULES
                # entries DO use ${...} in messages/actualOf, but none nest
                # backticks — if one ever does, this needs full template tracking.
                i += 1
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return open_idx + 1, i
        i += 1
    raise ValueError("unbalanced brackets in array")


def walk_rule_entries(inner: str):
    """Yield (start, end) tuples for each top-level {...} entry inside an
    array's inner content. Respects strings + comments + nested braces."""
    depth = 0
    i = 0
    n = len(inner)
    entry_start: Optional[int] = None
    while i < n:
        c = inner[i]
        # block comment
        if c == '/' and i + 1 < n and inner[i+1] == '*':
            j = inner.find('*/', i + 2)
            i = j + 2 if j != -1 else n
            continue
        # line comment
        if c == '/' and i + 1 < n and inner[i+1] == '/':
            j = inner.find('\n', i + 2)
            i = j + 1 if j != -1 else n
            continue
        # regex literal — see find_array_bounds (same tokenizer guard)
        if c == '/' and _starts_regex(inner, i):
            j = _regex_end(inner, i, n)
            if j is not None:
                i = j
                continue
        # strings
        if c in ('"', "'", '`'):
            quote = c
            i += 1
            while i < n:
                if inner[i] == '\\':
                    i += 2
                    continue
                if inner[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == '{':
            if depth == 0:
                entry_start = i
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0 and entry_start is not None:
                yield entry_start, i + 1
                entry_start = None
        i += 1


# ---------------------------------------------------------------------------
# Field extraction — targeted regex per known field shape
# ---------------------------------------------------------------------------

def _extract_string_field(entry: str, key: str) -> Optional[str]:
    """Extract a single quoted-string value for `key:"..."`. Handles escaped quotes."""
    # match key:"..." with escaped char support
    pattern = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r'\s*:\s*"((?:[^"\\]|\\.)*)"')
    m = pattern.search(entry)
    if not m:
        # try single quotes
        pattern2 = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r"\s*:\s*'((?:[^'\\]|\\.)*)'")
        m = pattern2.search(entry)
    if m:
        return _js_unescape(m.group(1))
    return None


def _extract_const_filter(entry: str, key: str):
    """Extract `key:CONST.filter(x=>x!=="lit")` -> (const_name, excluded_literal) or None.
    A bare _extract_const_ref match on this form silently drops the .filter, so the
    mirror overstates the value/option set (the sentinel the app excludes reappears)."""
    pattern = re.compile(re.escape(key) + r'\s*:\s*([A-Z][A-Z0-9_]+)\.filter\(\s*([A-Za-z_$][\w$]*)\s*=>\s*\2\s*!==\s*"((?:[^"\\]|\\.)*)"\s*\)')
    m = pattern.search(entry)
    return (_js_unescape(m.group(1)), _js_unescape(m.group(3))) if m else None


def _extract_const_ref(entry: str, key: str) -> Optional[str]:
    """Extract `key:CONSTANT_NAME` (uppercase identifier reference; a leading
    underscore is allowed — module-private consts like `_S158_REAL_KEYS` follow
    the same SCREAMING_SNAKE convention with a `_` prefix)."""
    pattern = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r'\s*:\s*(_?[A-Z][A-Z0-9_]+)\b')
    m = pattern.search(entry)
    return m.group(1) if m else None


def _extract_array_of_strings(entry: str, key: str) -> Optional[list[str]]:
    """Extract `key:["a","b","c"]` (literal string array)."""
    pattern = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r'\s*:\s*\[([^\]]*)\]')
    m = pattern.search(entry)
    if not m:
        return None
    body = m.group(1)
    # split on commas not inside strings
    items = []
    for s in re.findall(r'"((?:[^"\\]|\\.)*)"', body):
        items.append(_js_unescape(s))
    return items if items else None


def _extract_array_of_objects(body: str, key: str, obj_fields: tuple) -> Optional[list]:
    """Extract `key:[{...},{...}]` where each object carries string fields from
    obj_fields (the fix.fields compound-preset shape: {field, wrapper?, value}).
    Walks to the matching ] with the same comment/string/regex tokenizer as the
    other walkers, then reuses walk_rule_entries for the {...} sub-objects."""
    pattern = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r'\s*:\s*\[')
    m = pattern.search(body)
    if not m:
        return None
    start = m.end()  # right after the opening [
    depth = 1
    i = start
    n = len(body)
    while i < n:
        c = body[i]
        if c == '/' and i + 1 < n and body[i+1] == '*':
            j = body.find('*/', i + 2)
            i = j + 2 if j != -1 else n
            continue
        if c == '/' and i + 1 < n and body[i+1] == '/':
            j = body.find('\n', i + 2)
            i = j + 1 if j != -1 else n
            continue
        if c == '/' and _starts_regex(body, i):
            j = _regex_end(body, i, n)
            if j is not None:
                i = j
                continue
        if c in ('"', "'", '`'):
            quote = c
            i += 1
            while i < n:
                if body[i] == '\\':
                    i += 2
                    continue
                if body[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                break
        i += 1
    inner = body[start:i]
    out = []
    for s, e in walk_rule_entries(inner):
        obj = {}
        for fld in obj_fields:
            v = _extract_string_field(inner[s:e], fld)
            if v is not None:
                obj[fld] = v
        if obj:
            out.append(obj)
    return out if out else None


def _extract_number_field(entry: str, key: str) -> Optional[float]:
    """Extract `key:number`."""
    pattern = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r'\s*:\s*([\-]?[0-9]+(?:\.[0-9]+)?)\b')
    m = pattern.search(entry)
    return float(m.group(1)) if m else None


def _extract_subobject(entry: str, key: str) -> Optional[str]:
    """Extract the textual content inside `key:{...}` (top-level brace match)."""
    pattern = re.compile(r'(?<![A-Za-z0-9_$])' + re.escape(key) + r'\s*:\s*\{')
    m = pattern.search(entry)
    if not m:
        return None
    start = m.end()  # position right after the opening {
    depth = 1
    i = start
    n = len(entry)
    while i < n:
        c = entry[i]
        # comments
        if c == '/' and i + 1 < n and entry[i+1] == '*':
            j = entry.find('*/', i + 2)
            i = j + 2 if j != -1 else n
            continue
        if c == '/' and i + 1 < n and entry[i+1] == '/':
            j = entry.find('\n', i + 2)
            i = j + 1 if j != -1 else n
            continue
        # regex literal — see find_array_bounds (same tokenizer guard)
        if c == '/' and _starts_regex(entry, i):
            j = _regex_end(entry, i, n)
            if j is not None:
                i = j
                continue
        # strings
        if c in ('"', "'", '`'):
            quote = c
            i += 1
            while i < n:
                if entry[i] == '\\':
                    i += 2
                    continue
                if entry[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return entry[start:i]
        i += 1
    return None


# ---------------------------------------------------------------------------
# Per-rule projection
# ---------------------------------------------------------------------------

def project_rule(entry: str, source_layer: str = 'per-feature') -> Optional[dict]:
    """Build a serializable projection of one RULES entry."""
    rule_id = _extract_string_field(entry, 'id')
    if not rule_id:
        return None
    out: dict = {
        'id': rule_id,
        'ref': _extract_string_field(entry, 'ref'),
        'severity': _extract_string_field(entry, 's'),
        'message': _extract_string_field(entry, 'm'),
        'sourceLayer': source_layer,
    }
    # noFix: the user-facing no-automatic-fix explanation rendered in the finding
    # card. Previously dropped from the mirror entirely, so editing (or deleting)
    # a noFix reason regenerated byte-identical JSON and check 5 passed on the drift.
    no_fix = _extract_string_field(entry, 'noFix')
    if no_fix:
        out['noFix'] = no_fix
    # expected sub-object
    expected_body = _extract_subobject(entry, 'expected')
    if expected_body:
        exp = {}
        kind = _extract_string_field(expected_body, 'kind')
        if kind:
            exp['kind'] = kind
        # values: either a literal array of strings or a CONSTANT reference
        vals = _extract_array_of_strings(expected_body, 'values')
        if vals is not None:
            exp['values'] = vals
        else:
            # `values:CONST.filter(x=>x!=="lit")` — the bare const-ref regex matched
            # the CONST name and silently DROPPED the .filter, so the JSON mirror
            # stamped the FULL const (whose element [0] is the "none" UI sentinel)
            # for rules whose in-app expected set deliberately excludes it. Emit
            # valuesConst + valuesExclude so the mirror carries the same set as the app.
            cf = _extract_const_filter(expected_body, 'values')
            if cf:
                exp['valuesConst'] = cf[0]
                exp['valuesExclude'] = [cf[1]]
            else:
                const_ref = _extract_const_ref(expected_body, 'values')
                if const_ref:
                    exp['valuesConst'] = const_ref
        # range/pattern/description for non-enum rules
        for fld in ('regex', 'description'):
            v = _extract_string_field(expected_body, fld)
            if v:
                exp[fld] = v
        for fld in ('min', 'max'):
            v = _extract_number_field(expected_body, fld)
            if v is not None:
                exp[fld] = v
        if exp:
            out['expected'] = exp
    # fix sub-object
    fix_body = _extract_subobject(entry, 'fix')
    if fix_body:
        fix = {}
        for fld in ('field', 'inputType', 'label', 'placeholder', 'kind',
                    'wrapper', 'target'):
            v = _extract_string_field(fix_body, fld)
            if v:
                fix[fld] = v
        # options: array of strings or constant reference
        opts = _extract_array_of_strings(fix_body, 'options')
        if opts is not None:
            fix['options'] = opts
        else:
            # same filtered-const handling as expected.values — a bare const-ref match
            # on `options:CONST.filter(x=>x!=="lit")` silently dropped the exclusion,
            # overstating the quick-fix option set in the mirror (affected TOP-01 /
            # FOG-01 / STA-02 / ENUM-TMS at the time this was added).
            ocf = _extract_const_filter(fix_body, 'options')
            if ocf:
                fix['optionsConst'] = ocf[0]
                fix['optionsExclude'] = [ocf[1]]
            else:
                const_ref = _extract_const_ref(fix_body, 'options')
                if const_ref:
                    fix['optionsConst'] = const_ref
        # childType is an array of strings
        children = _extract_array_of_strings(fix_body, 'childType')
        if children is not None:
            fix['childType'] = children
        # skipFts: array of feature types whose quick-fix is suppressed (the write
        # would fabricate a spec-invalid element on that FT); skipNote is the
        # user-facing explanation rendered in the no-automatic-fix block.
        skip_fts = _extract_array_of_strings(fix_body, 'skipFts')
        if skip_fts is not None:
            fix['skipFts'] = skip_fts
        skip_note = _extract_string_field(fix_body, 'skipNote')
        if skip_note:
            fix['skipNote'] = skip_note
        # fields: compound multi-field preset (e.g. R1001-EWM-01 writes colour +
        # rhythmOfLight + signalPeriod in one click) — each {field, wrapper?, value}
        # object serialized. Previously dropped, so editing a preset value was
        # gate-invisible drift (byte-identical regen).
        compound = _extract_array_of_objects(fix_body, 'fields', ('field', 'wrapper', 'value'))
        if compound is not None:
            fix['fields'] = compound
        # keys: the per-attribute coverage list (S158-FMT-01's keys:_S158_REAL_KEYS
        # const ref); literal-array form handled first for future rules.
        keys_lit = _extract_array_of_strings(fix_body, 'keys')
        if keys_lit is not None:
            fix['keys'] = keys_lit
        else:
            keys_const = _extract_const_ref(fix_body, 'keys')
            if keys_const:
                fix['keysConst'] = keys_const
        for fld in ('min', 'max', 'step'):
            v = _extract_number_field(fix_body, fld)
            if v is not None:
                fix[fld] = v
        # step:"any" (S201-FEA-17/19) — a STRING, dropped by the numeric-only
        # extraction above; fall back to the string form so the mirror carries it.
        if 'step' not in fix:
            v = _extract_string_field(fix_body, 'step')
            if v:
                fix['step'] = v
        unit = _extract_string_field(fix_body, 'unit')
        if unit:
            fix['unit'] = unit
        if fix:
            out['fix'] = fix
    # purge None values for clean output
    return {k: v for k, v in out.items() if v is not None}


# ---------------------------------------------------------------------------
# Structural rules (GML-STR-01..N)
# ---------------------------------------------------------------------------

# Structural rules are emitted as push("GML-STR-NN","severity","ref","msg",pass,...)
# The args can contain ternaries with string concatenation, template literals,
# and other complex expressions — so we walk character-by-character and split
# on top-level commas (respecting strings + parens + brackets).
STRUCTURAL_RULE_OPEN = re.compile(r'push\(\s*"(GML-STR-\d+)"\s*,')

# Exchange-set package rules use the SAME push shape inside validateExchangeSet:
# push("S158-PKG-NN"|"S201-ES-NN","severity","ref","msg",pass). One extraction
# core (extract_push_rules) serves both function-body corpora.
EXCHANGESET_RULE_OPEN = re.compile(r'push\(\s*"((?:S158-PKG|S201-ES)-\d+)"\s*,')


def _split_top_args(body: str) -> list[str]:
    """Split a function-call argument body on top-level commas, respecting
    strings, parens, brackets, and template literals."""
    args = []
    depth_p = 0
    depth_b = 0
    depth_c = 0  # curly braces (inside object literals)
    in_string = None
    escape = False
    cur_start = 0
    n = len(body)
    i = 0
    while i < n:
        c = body[i]
        if escape:
            escape = False
            i += 1
            continue
        if c == '\\':
            escape = True
            i += 1
            continue
        if in_string:
            if c == in_string:
                in_string = None
            i += 1
            continue
        if c in ('"', "'", '`'):
            in_string = c
            i += 1
            continue
        if c == '(': depth_p += 1
        elif c == ')': depth_p -= 1
        elif c == '[': depth_b += 1
        elif c == ']': depth_b -= 1
        elif c == '{': depth_c += 1
        elif c == '}': depth_c -= 1
        elif c == ',' and depth_p == 0 and depth_b == 0 and depth_c == 0:
            args.append(body[cur_start:i].strip())
            cur_start = i + 1
        i += 1
    if cur_start < n:
        args.append(body[cur_start:n].strip())
    return args


def _starts_regex(js: str, i: int) -> bool:
    """Heuristic: does the '/' at js[i] open a REGEX LITERAL (vs. division)?
    Looks back at the last non-whitespace char: after an operator/opener/keyword a
    '/' can only start a regex. Without this, the tokenizer walks treated regex
    literals as plain code, so the quote characters inside e.g.
    `/(?:"([^"]+)"|'([^']+)')/` put the walker into a phantom-string state that only
    re-synced by APOSTROPHE PARITY LUCK — one added apostrophe in a later comment
    (e.g. "wrapper's") flipped the parity and silently truncated the extraction."""
    k = i - 1
    while k >= 0 and js[k] in ' \t\r\n':
        k -= 1
    if k < 0:
        return True
    if js[k] in '=(,[{;:!&|?+-*%~^<>':
        return True
    return bool(re.search(r'(?:\breturn|\bcase|\btypeof|\bin|\bof|\bnew|\bdelete|\bvoid|\bdo|\belse)$', js[max(0, k-7):k+1]))


def _regex_end(js: str, i: int, n: int):
    """js[i] == '/' opening a regex literal: return the index just past the literal
    (including trailing flags), or None if it can't be one (newline before close —
    JS regex literals cannot span lines; caller then treats the '/' as division)."""
    j = i + 1
    in_class = False
    while j < n:
        c = js[j]
        if c == '\\':
            j += 2
            continue
        if c == '\n':
            return None
        if in_class:
            if c == ']':
                in_class = False
        elif c == '[':
            in_class = True
        elif c == '/':
            j += 1
            break
        j += 1
    while j < n and js[j].isalpha():
        j += 1
    return j


def extract_structural_rules(js: str) -> list[dict]:
    """Structural corpus: push("GML-STR-NN", …) inside validateGMLStructure."""
    return extract_push_rules(js, 'validateGMLStructure', STRUCTURAL_RULE_OPEN, 'structural')


def extract_exchangeset_rules(js: str) -> list[dict]:
    """Exchange-set package corpus: push("S158-PKG-NN"|"S201-ES-NN", …) inside
    validateExchangeSet — same push shape as the structural rules."""
    return extract_push_rules(js, 'validateExchangeSet', EXCHANGESET_RULE_OPEN, 'exchange-set')


def extract_push_rules(js: str, fn_name: str, open_re: 're.Pattern', source_layer: str) -> list[dict]:
    """Find `function <fn_name>(` and extract its push("<ID>",sev,ref,msg,pass)
    findings. The function body uses a different shape from the RULES array —
    each finding is pushed to a local `results` array; args are parsed with the
    shared paren/string/regex-aware tokenizer."""
    # Find the function's bounds
    m = re.search(r'function\s+' + re.escape(fn_name) + r'\s*\(', js)
    if not m:
        return []
    start = js.index('{', m.end()) + 1
    depth = 1
    i = start
    n = len(js)
    while i < n and depth > 0:
        c = js[i]
        if c == '/' and i + 1 < n and js[i+1] == '*':
            j = js.find('*/', i + 2)
            i = j + 2 if j != -1 else n
            continue
        if c == '/' and i + 1 < n and js[i+1] == '/':
            j = js.find('\n', i + 2)
            i = j + 1 if j != -1 else n
            continue
        if c == '/' and _starts_regex(js, i):
            j = _regex_end(js, i, n)
            if j is not None:
                i = j
                continue
        if c in ('"', "'", '`'):
            quote = c
            i += 1
            while i < n:
                if js[i] == '\\':
                    i += 2
                    continue
                if js[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        i += 1
    fn_body = js[start:i-1]
    seen: dict[str, dict] = {}
    # Walk forward looking for `push("<ID>",` openings; for each, parse
    # the full argument list with proper paren tracking.
    pos = 0
    while True:
        om = open_re.search(fn_body, pos)
        if not om:
            break
        rid = om.group(1)
        # Position right after the comma that follows the rule-id literal
        args_start = om.end()
        # Find matching close paren
        depth = 1
        in_string = None
        escape = False
        i = args_start
        n = len(fn_body)
        while i < n and depth > 0:
            c = fn_body[i]
            if escape:
                escape = False
                i += 1
                continue
            if c == '\\':
                escape = True
                i += 1
                continue
            if in_string:
                if c == in_string:
                    in_string = None
                i += 1
                continue
            # regex literals inside push args (e.g. GML-STR-21's text.search(/.../))
            # carry quotes/parens that must not leak into the string/paren state —
            # same tokenizer guard as the function-bounds walk above.
            if c == '/' and i + 1 < n and fn_body[i+1] not in ('*', '/') and _starts_regex(fn_body, i):
                j = _regex_end(fn_body, i, n)
                if j is not None:
                    i = j
                    continue
            if c in ('"', "'", '`'):
                in_string = c
                i += 1
                continue
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        args_body = fn_body[args_start:i]
        args = _split_top_args(args_body)
        if len(args) >= 3 and rid not in seen:
            sev = _strip_string_literal(args[0])
            ref = _strip_string_literal(args[1]) if len(args) > 1 else None
            msg_expr = args[2] if len(args) > 2 else ''
            msg = _extract_fail_message(msg_expr)
            seen[rid] = {
                'id': rid,
                'ref': ref,
                'severity': sev,
                'message': msg,
                'sourceLayer': source_layer,
            }
        pos = i + 1
    # Sort by (prefix, numeric suffix) — for a single-prefix corpus (GML-STR-01..N)
    # this is the plain numeric order; the exchange-set corpus groups S158-PKG before S201-ES.
    return [seen[k] for k in sorted(seen.keys(), key=lambda x: (x.rsplit('-', 1)[0], int(x.rsplit('-', 1)[1])))]


def _strip_string_literal(s: str) -> Optional[str]:
    """If `s` is a quoted string literal, return its decoded content; else None."""
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'", '`'):
        return _js_unescape(s[1:-1])
    return s


def _extract_fail_message(msg_expr: str) -> str:
    """Given a JS message expression (literal string or ternary `cond?"ok":"fail"`),
    extract the user-facing fail message. Strips template-literal interpolations
    like ${expr} since the JSON mirror is static."""
    msg_expr = msg_expr.strip()
    # Walk forward looking for the ternary :  separator at top depth
    depth_paren = 0
    depth_bracket = 0
    in_string = None
    escape = False
    in_question = False
    fail_start = None
    for i, c in enumerate(msg_expr):
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if in_string:
            if c == in_string:
                in_string = None
            continue
        if c in ('"', "'", '`'):
            in_string = c
            continue
        if c == '(': depth_paren += 1
        elif c == ')': depth_paren -= 1
        elif c == '[': depth_bracket += 1
        elif c == ']': depth_bracket -= 1
        elif c == '?' and depth_paren == 0 and depth_bracket == 0:
            in_question = True
        elif c == ':' and in_question and depth_paren == 0 and depth_bracket == 0:
            fail_start = i + 1
            break
    if fail_start is None:
        # not a ternary — take the whole expression and try to extract the
        # outermost string literal
        body = msg_expr
    else:
        body = msg_expr[fail_start:].strip()
    # A fully-PARENTHESIZED fail arm is a nested ternary (GML-STR-09's
    # `(dsBbEl?"empty…":"missing…")`) — strip the parens and recurse so its own
    # fail arm comes back as prose instead of collapsing into a bare placeholder
    # (the paren would otherwise put the whole arm at depth>0 = expression).
    # String-aware matching: the arms' text contains parens ("element(s)").
    body = body.strip()
    if body.startswith('('):
        _d = 0
        _j = 0
        _ins = None
        _esc = False
        _close = -1
        while _j < len(body):
            _ch = body[_j]
            if _esc:
                _esc = False
            elif _ch == '\\':
                _esc = True
            elif _ins:
                if _ch == _ins:
                    _ins = None
            elif _ch in ('"', "'", '`'):
                _ins = _ch
            elif _ch == '(':
                _d += 1
            elif _ch == ')':
                _d -= 1
                if _d == 0:
                    _close = _j
                    break
            _j += 1
        if _close == len(body) - 1:
            return _extract_fail_message(body[1:-1])
    # Join ALL top-level string literals of the (possibly concatenated) expression,
    # substituting an ASCII '<...>' placeholder for every non-literal segment
    # (identifiers/counts like `_srsIndet.length`, call expressions, ${...}
    # interpolations). The previous leading-literal-only extraction had two
    # failure legs: a "literal"+expr+"tail" concatenation LOST its tail (the
    # GML-STR-04 remediation text), and a non-string-LED expression fell all the
    # way through to raw JS source in the mirror (GML-STR-21's message shipped as
    # literal code with a dangling quote). Literals inside nested parens/brackets
    # (e.g. the ", " inside .join(", ")) are part of the expression, not message
    # text — depth-tracked so they collapse into the placeholder.
    parts: list[str] = []
    pending_expr = False

    def _flush() -> None:
        nonlocal pending_expr
        if pending_expr:
            parts.append('<...>')
            pending_expr = False

    i, n, depth = 0, len(body), 0
    while i < n:
        c = body[i]
        if c in ('"', "'", '`'):
            q = c
            j = i + 1
            buf: list[str] = []
            while j < n:
                ch = body[j]
                if ch == '\\':
                    buf.append(body[j:j+2])
                    j += 2
                    continue
                if q == '`' and ch == '$' and j + 1 < n and body[j+1] == '{':
                    k = j + 2
                    d = 1
                    while k < n and d:
                        if body[k] == '{':
                            d += 1
                        elif body[k] == '}':
                            d -= 1
                        k += 1
                    buf.append('<...>')
                    j = k
                    continue
                if ch == q:
                    break
                buf.append(ch)
                j += 1
            if depth == 0:
                _flush()
                parts.append(_js_unescape(''.join(buf)))
            else:
                pending_expr = True  # a literal inside a call arg is expression material
            i = j + 1
            continue
        if c in '([':
            depth += 1
            pending_expr = True
        elif c in ')]':
            depth = max(0, depth - 1)
            pending_expr = True
        elif depth == 0 and c != '+' and c.strip():
            pending_expr = True
        i += 1
    _flush()
    text = ''.join(parts).strip()
    return text if text else body


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def extract_all_rules() -> list[dict]:
    src = open(HTML_PATH, 'r', encoding='utf-8').read()
    sm = re.search(r'<script>(.*?)</script>', src, re.DOTALL)
    if not sm:
        raise ValueError("no <script> tag in HTML")
    js = sm.group(1)
    open_idx, close_idx = find_array_bounds(js, r'const\s+RULES\s*=')
    inner = js[open_idx:close_idx]
    rules: list[dict] = []
    for s, e in walk_rule_entries(inner):
        proj = project_rule(inner[s:e], 'per-feature')
        if proj:
            rules.append(proj)
    rules.extend(extract_structural_rules(js))
    rules.extend(extract_exchangeset_rules(js))
    return rules


def write_json(rules: list[dict]) -> None:
    # newline='\n' is load-bearing on Windows, not cosmetic. Python's text mode translates
    # every '\n' to '\r\n' by default, so a regen here emitted a CRLF mirror while the
    # committed blob is LF (.gitattributes: `* text=auto eol=lf`). git status stays silent
    # about that — it normalises when comparing — but the bundle build and the zip packer
    # read RAW BYTES off disk, so the CRLF copy was packed into the shipped tester archive
    # and the delivered zip no longer matched the reviewed source. That defect reached a
    # deliverable once and was cleaned up by hand; this kwarg is what stops it recurring.
    # Same reason the pdf-extracts manifest generator writes newline='\n' — its check hashes
    # raw bytes too.
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
        f.write('\n')


def _selftest() -> None:
    """Tokenizer self-test, run on EVERY invocation (regen and --check, so the
    precommit gate re-proves it each run). The extraction walkers feed a
    byte-identity check (check 5), so a walker bug that garbles extraction is
    self-consistent and gate-invisible — the exact failure mode this guards.
    The fixture carries the shapes that historically broke extraction: a
    quote-bearing regex literal (which, before the tokenizer, collapsed the
    whole corpus to a single rule), a division that must NOT be read as a
    regex, comments containing quotes and braces, a template literal with
    ${...}, and a nested sub-object."""
    fixture = (
        'const RULES=['
        '/* comment with "quotes" and {braces} and it\'s an apostrophe */'
        '{id:"T-1",ref:"r1",s:"info",m:"msg one",t:f=>!/["\']/.test(String(f.a||"")),'
        'expected:{kind:"text",description:"no quotes"}},'
        '{id:"T-2",ref:"r2",s:"warning",m:`tpl ${1+1} msg`,t:(f,all)=>(f.x||0)/(f.y||1)>2,'
        'fix:{field:"x",inputType:"number",step:1}},'
        '];'
    )
    try:
        a, b = find_array_bounds(fixture, r'const\s+RULES\s*=\s*\[')
        inner = fixture[a:b]
        entries = [project_rule(inner[s:e]) for s, e in walk_rule_entries(inner)]
        entries = [r for r in entries if r]
        assert len(entries) == 2, f"expected 2 fixture rules, extracted {len(entries)}"
        assert entries[0]['id'] == 'T-1' and entries[0]['message'] == 'msg one', entries[0]
        assert entries[0].get('expected', {}).get('description') == 'no quotes', entries[0]
        assert entries[1]['id'] == 'T-2' and entries[1].get('fix', {}).get('field') == 'x', entries[1]
    except AssertionError:
        raise
    except Exception as e:  # a walker crash is equally a self-test failure
        raise AssertionError(f"tokenizer self-test crashed: {type(e).__name__}: {e}")


def main() -> int:
    args = sys.argv[1:]
    check_only = '--check' in args
    try:
        _selftest()
    except AssertionError as e:
        print(f"[FAIL] extraction tokenizer self-test: {e}", file=sys.stderr)
        return 1
    rules = extract_all_rules()
    n_per_feat = sum(1 for r in rules if r.get('sourceLayer') == 'per-feature')
    n_struct = sum(1 for r in rules if r.get('sourceLayer') == 'structural')
    n_exch = sum(1 for r in rules if r.get('sourceLayer') == 'exchange-set')
    print(f"extracted {len(rules)} rules ({n_per_feat} per-feature + {n_struct} structural + {n_exch} exchange-set)")
    if check_only:
        if not os.path.exists(JSON_PATH):
            print(f"[FAIL] {JSON_PATH} does not exist", file=sys.stderr)
            return 1
        existing = open(JSON_PATH, 'r', encoding='utf-8').read()
        regen = json.dumps(rules, indent=2, ensure_ascii=False) + '\n'
        if existing != regen:
            print(f"[FAIL] {JSON_PATH} differs from regenerated content", file=sys.stderr)
            return 1
        print(f"[OK] {JSON_PATH} is in sync with in-app RULES")
        return 0
    write_json(rules)
    print(f"wrote {JSON_PATH}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
