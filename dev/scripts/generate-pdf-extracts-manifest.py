#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Generate dev/pdf-extracts/MANIFEST.sha256 — the integrity manifest for the
# pdf-extract corpus.
#
# WHY (Rule 5/8 — the citation trust anchor): dev/pdf-extracts/*.txt is the
# grep-able ground truth behind hundreds of validator-rule `ref` citations and
# inline spec comments ("r0110_ed5_full.txt L1063-1068" style). Before this
# manifest existed the corpus had NO gate at all: a silent re-extraction, a
# truncated regeneration, or a re-bundle at a newer edition would invalidate
# the line-number ground truth behind every extract-based citation with
# nothing to detect it. The precommit gate verifies every file in
# dev/pdf-extracts/ against this manifest, so ANY byte change to the corpus
# blocks until the manifest is deliberately regenerated with this script —
# making corpus changes a visible, reviewed act instead of a silent one.
#
# RESIDUAL (disclosed in HANDOFF § 13): the manifest freezes the EXTRACTS, not
# the source PDFs. A PDF re-bundled at a newer edition while its extract stays
# untouched does not trip this gate (the extract still matches its hash); the
# extract-vs-PDF edition agreement remains a manual re-bundling-time duty.
#
# Usage:
#   python dev/scripts/generate-pdf-extracts-manifest.py            # (re)write manifest
#   python dev/scripts/generate-pdf-extracts-manifest.py --check    # exit non-zero on drift
#
# Format: one "sha256␠␠filename" line per file (sha256sum-compatible), sorted
# by filename, LF endings, hashing raw bytes (line endings included — a CRLF
# rewrite of an extract IS a change to the cited byte ground truth).
# ---------------------------------------------------------------------------

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTS_DIR = os.path.normpath(os.path.join(HERE, '..', 'pdf-extracts'))
MANIFEST = os.path.join(EXTRACTS_DIR, 'MANIFEST.sha256')


def corpus_hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in sorted(os.listdir(EXTRACTS_DIR)):
        path = os.path.join(EXTRACTS_DIR, name)
        if not os.path.isfile(path) or name == 'MANIFEST.sha256':
            continue
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        out[name] = h.hexdigest()
    return out


def render(hashes: dict[str, str]) -> str:
    return ''.join(f"{digest}  {name}\n" for name, digest in sorted(hashes.items()))


def parse_manifest(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        digest, _, name = line.partition('  ')
        out[name] = digest
    return out


def main() -> int:
    check_only = '--check' in sys.argv[1:]
    hashes = corpus_hashes()
    if not hashes:
        print(f"[FAIL] no extract files found under {EXTRACTS_DIR}", file=sys.stderr)
        return 1
    content = render(hashes)
    if check_only:
        if not os.path.exists(MANIFEST):
            print(f"[FAIL] {MANIFEST} missing — run this script without --check to create it",
                  file=sys.stderr)
            return 1
        recorded = parse_manifest(open(MANIFEST, 'r', encoding='utf-8').read())
        problems = []
        for name, digest in hashes.items():
            if name not in recorded:
                problems.append(f"UNLISTED file (new extract?): {name}")
            elif recorded[name] != digest:
                problems.append(f"HASH MISMATCH (extract changed since manifest): {name}")
        for name in recorded:
            if name not in hashes:
                problems.append(f"MISSING file (listed in manifest, absent on disk): {name}")
        if problems:
            print(f"[FAIL] pdf-extracts corpus drifted from MANIFEST.sha256 "
                  f"({len(problems)} problem(s)):", file=sys.stderr)
            for p in problems[:20]:
                print(f"  {p}", file=sys.stderr)
            print("  If the change is DELIBERATE (new/updated extract), regenerate with:\n"
                  "    python dev/scripts/generate-pdf-extracts-manifest.py", file=sys.stderr)
            return 1
        print(f"[OK] pdf-extracts corpus matches MANIFEST.sha256 ({len(hashes)} files)")
        return 0
    with open(MANIFEST, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print(f"wrote {MANIFEST} ({len(hashes)} files)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
