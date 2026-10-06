#!/usr/bin/env python3
"""generate-spec-sources-manifest.py — regenerate dev/spec-sources/MANIFEST.md.

The public snapshot repository redistributes NONE of the third-party reference
material the development repository holds: the IHO and IALA publications, the
S-201 and S-125 Feature Catalogue XML, the IHO S-100 / S-201 / S-125 schema families and the OGC,
ISO and W3C schemas they import, the S-158 check tables and the S-62 producer-code
data under dev/spec-sources/; the plain-text extracts under dev/pdf-extracts/
derived from those publications; and dev/tmp_verify_imgs/. All of it is freely
obtainable from its official source (the IALA documents carry no redistribution
grant in their text, and the IHO copyright terms permit free-of-charge
redistribution only with an IHO-Secretariat permission statement this project does
not hold), so the snapshot ships THIS MANIFEST instead: every file with its size
and SHA-256, grouped by folder, with where to obtain it. A reader who fetches the
same file and matches the hash holds byte-for-byte what the validator's citations
were checked against, so the line-number citations in the source resolve.

Run from the project root:
  python dev/scripts/generate-spec-sources-manifest.py           (rewrite MANIFEST.md)
  python dev/scripts/generate-spec-sources-manifest.py --check   (verify it, write nothing)

--check exits 1 naming every file whose size or SHA-256 differs from its manifest row, every file on disk the
manifest does not list and every manifest row with no file on disk, and also when the manifest's text is not
exactly what this script would write (its prose, folder counts or totals); it exits 0 when the manifest is
current. Pre-commit runs it, so a replaced source cannot pass unseen. Do not answer a red --check by
regenerating until the changed bytes are explained: rewriting the manifest over an unexplained change would
record the change as the new truth.
"""
import hashlib
import os
import re
import sys

# the project root, found from this script's place in dev/scripts, and the manifest it writes and checks
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SPEC = os.path.join(ROOT, "dev", "spec-sources")
OUT = os.path.join(SPEC, "MANIFEST.md")
OUT_NAME = "MANIFEST.md"

# Where each folder's files come from. Longest matching prefix wins.
SOURCES = {
    "dev/spec-sources": (
        "The IALA S-201 Product Specification family (main document, DCEG Annex A, Feature "
        "Catalogue Annex C1, overview) and the IALA R-, G- and S-series publications: "
        "<https://www.iala.int>. The Feature Catalogue XML `201_Feature_Catalogue_2.0.0.xml`: "
        "the IHO Geospatial Information Registry <https://registry.iho.int> (S-201 product "
        "specification entry). IHO S-100, S-97, S-99 and the S-100 Roadmap annex: <https://iho.int>."),
    "dev/spec-sources/s-100-xsd": (
        "IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information "
        "catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information "
        "Registry <https://registry.iho.int>. The package's own README and licence files are listed "
        "with it."),
    "dev/spec-sources/ogc-gml": (
        "OGC GML 3.2 schemas: <https://schemas.opengis.net/gml/> (OGC document and software licence)."),
    "dev/spec-sources/iso-xsd": (
        "ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): "
        "<https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are "
        "in the folder's ISO_LICENCE.TXT, listed below."),
    "dev/spec-sources/w3c-xsd": (
        "W3C `xml.xsd` and `xlink.xsd`: <https://www.w3.org/2001/xml.xsd>, "
        "<https://www.w3.org/1999/xlink.xsd> (W3C software and document licence, LICENCE.TXT listed below)."),
    "dev/spec-sources/s-201-xsd": (
        "IALA S-201 Ed 1.1.0 Annex B1 data-product-format schema: <https://www.iala.int> and the "
        "IHO Geospatial Information Registry <https://registry.iho.int>. The Ed 2.0.0 Annex B schema "
        "(`S-201_Ed2.0.0_Annex_B_DataProductFormatSchemas.xsd`, published as "
        "`4. S-201 Data Product Format Schemas - Annex B.xsd`): IALA's S-201 repository "
        "<https://github.com/IALA-IGO/S-201_AtoN-Information>."),
    "dev/spec-sources/s-125": (
        "IHO S-125 Marine Aids to Navigation (AtoN) Edition 1.0.0: the product specification, Annex A "
        "DCEG, the HSSC-18 interoperability guidance (Draft 005), the Feature Catalogue XML and the "
        "Portrayal Catalogue zip are the files attached to the S-125 entry of the IHO Geospatial "
        "Information Registry <https://registry.iho.int/productspec/view.do?idx=222>; the GML schema "
        "`125_1.0.0.xsd`: the IHO schema server "
        "<https://schemas.s100dev.net/schemas/S125/1.0.0/20260303/125_1.0.0.xsd>."),
    "dev/spec-sources/s-158": (
        "IHO S-158 validation-check publications and check tables: <https://iho.int> (S-158 series) "
        "and the S-100 Validation Checks working repository "
        "<https://github.com/iho-ohi/S-100-Validation-Checks>."),
    "dev/spec-sources/iho-additional": (
        "IHO S-62 producer-code register and the other IHO documents: <https://iho.int> and "
        "<https://registry.iho.int>. `S-62_ProducerCodes.csv` / `.json` are extracted from the S-62 "
        "register snapshot by `extract_producer_codes.py` (the development repository's own script, "
        "listed here because it lives in this folder)."),
    "dev/spec-sources/iala-additional": (
        "IALA guidelines and recommendations: <https://www.iala.int>."),
    "dev/pdf-extracts": (
        "Plain-text extractions of the publications above (PyMuPDF; the three `s125_*` extracts by "
        "pypdf; the `.docx`-derived one by a zipfile + document.xml parse), regenerable from the originals; `MANIFEST.sha256` is the "
        "development repository's integrity manifest for them (pre-commit check #17)."),
    "dev/tmp_verify_imgs": (
        "Courseware-derived verification scratch; not a source."),
}


def _lp(path):
    """Windows long-path guard: deep checkout paths + long IHO/IALA filenames can
    exceed MAX_PATH (260); the \\\\?\\ prefix lifts the limit. No-op elsewhere."""
    if os.name == "nt":
        p = os.path.abspath(path)
        if not p.startswith("\\\\?\\"):
            return "\\\\?\\" + p
    return path


def sha256(path):
    h = hashlib.sha256()
    with open(_lp(path), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _source_for(rel_dir):
    best = ""
    for key in SOURCES:
        if (rel_dir == key or rel_dir.startswith(key + "/")) and len(key) > len(best):
            best = key
    return SOURCES.get(best, "")


def collect():
    """Every file under dev/spec-sources (except this manifest), dev/pdf-extracts and
    dev/tmp_verify_imgs, grouped by folder (relative to the project root)."""
    groups = {}
    roots = [SPEC, os.path.join(ROOT, "dev", "pdf-extracts"), os.path.join(ROOT, "dev", "tmp_verify_imgs")]
    for top in roots:
        if not os.path.isdir(top):
            continue
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
            for fn in sorted(filenames):
                if fn == OUT_NAME and os.path.normpath(dirpath) == os.path.normpath(SPEC):
                    continue
                if fn.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, fn)
                rel_dir = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
                groups.setdefault(rel_dir, []).append(full)
    return groups


def render():
    """The manifest as this script writes it, read from the disk now: (text, rows, files, bytes, folders), where
    rows maps (folder, file name) to (size, sha256). Writing (main) and checking (check) both start here, so the
    check compares against exactly what a regeneration would write."""
    groups = collect()
    rows = {}   # (folder relative to the root, file name) -> (size in bytes, sha256 hex), for check()
    lines = []
    lines.append("# Reference-source manifest\n")
    lines.append(
        "The public snapshot of S-201 AtoN Studio redistributes **none** of the third-party reference "
        "material listed here: the IHO and IALA publications, the S-201 and S-125 Feature Catalogue XML, "
        "the IHO S-100 / S-201 / S-125 schema families with the OGC, ISO and W3C schemas they import, the S-158 check "
        "tables and the S-62 producer-code data under `dev/spec-sources/`; the plain-text extracts under "
        "`dev/pdf-extracts/` derived from those publications; and `dev/tmp_verify_imgs/`. All of it is "
        "freely obtainable from its official source (the IALA publications carry no redistribution grant "
        "in their text, and the IHO copyright terms permit free-of-charge redistribution only together "
        "with an IHO-Secretariat permission statement this project does not hold), so the snapshot ships "
        "this manifest instead.\n")
    lines.append(
        "To follow a citation in the source (`FC 2.0.0 XML L11003-11023`, `r1001_ed2_full.txt L384-393`, "
        "`S-100 Pt 10b §10b-11.7`, an XSD line), obtain the named file from the source given for its "
        "folder, check that its SHA-256 matches the value below, and place it at the manifest path "
        "relative to the project root; the line numbers then resolve byte-for-byte to what the "
        "validator's citations were checked against. The extracts are regenerated from the "
        "publications, not downloaded. Text files (XML, XSD, the extracts) are kept with LF line "
        "endings (the repository's `.gitattributes`), so an original published with CRLF line endings "
        "matches its SHA-256 here after a CRLF-to-LF conversion; the line numbers are the same either way.\n")
    lines.append(
        "The development repository keeps all of these files; `Annex_D/` (the S-201 Annex D portrayal "
        "library, © IHO / IALA) is the one third-party component the snapshot does ship, because the "
        "app cannot render without it — see NOTICE.txt.\n")
    total_n = 0
    total_b = 0
    for rel_dir in sorted(groups):
        files = groups[rel_dir]
        lines.append(f"\n## `{rel_dir}/` ({len(files)} files)\n")
        src = _source_for(rel_dir)
        if src:
            lines.append(f"Obtain from: {src}\n")
        lines.append("| File | Size (bytes) | SHA-256 |")
        lines.append("|---|---:|---|")
        for full in files:
            size = os.path.getsize(_lp(full))
            total_n += 1
            total_b += size
            digest = sha256(full)   # hashed once: the row written and the row checked are the same value
            rows[(rel_dir, os.path.basename(full))] = (size, digest)   # the row check() compares, keyed as read_manifest keys it
            lines.append(f"| {os.path.basename(full)} | {size:,} | `{digest}` |")   # the written row, from the same digest
    lines.append(f"\n---\n\n**Total: {total_n} files, {total_b:,} bytes.** "
                 "Regenerate this manifest with `python dev/scripts/generate-spec-sources-manifest.py` "
                 "whenever a file under these folders is added, replaced or removed.\n")
    # the text main() writes and check() compares, with the rows and totals each reports
    return "\n".join(lines), rows, total_n, total_b, len(groups)


def read_manifest(text):
    """The file rows of a written manifest: (folder, file name) -> (size, sha256), the folder taken from the
    `## `folder/` (N files)` heading the row sits under - the shape render() writes."""
    rows = {}
    folder = None   # the section a row belongs to; a row before any section heading is not a file row
    for line in text.split("\n"):
        # a folder heading opens its section
        m = re.match(r"^## `(.+)/` \(\d+ files\)$", line)
        if m:
            folder = m.group(1)
            continue
        # a file row: name, size with thousands commas, backticked lowercase sha256
        m = re.match(r"^\| (.+) \| ([\d,]+) \| `([0-9a-f]{64})` \|$", line)
        if m and folder is not None:
            rows[(folder, m.group(1))] = (int(m.group(2).replace(",", "")), m.group(3))
    return rows


def check():
    """--check: compare the manifest on disk with the disk it describes and say every difference, in ASCII (a
    Windows console without a UTF-8 code page cannot print every character, and the gate must not die on its own
    message). Returns the exit code: 1 on any difference, 0 when the manifest is current. Writes nothing."""
    # a missing manifest is a failure, not a pass: there is nothing for a reader to verify a source against
    if not os.path.isfile(OUT):
        print(f"[FAIL] {OUT} does not exist - nothing to check against")
        return 1
    # the manifest as written (line endings kept, so the text comparison is byte-exact), the manifest the disk
    # would give now, and the rows each holds
    with open(OUT, encoding="utf-8", newline="") as f:
        written = f.read()
    text, disk, total_n, _total_b, _folders = render()
    listed = read_manifest(written)
    problems = []   # one line per difference, named by its path relative to the project root
    # a listed file whose bytes changed, and a listed file that is gone
    for key in sorted(listed):
        path = key[0] + "/" + key[1]
        if key not in disk:
            problems.append(f"listed in the manifest, missing on disk: {path}")
        elif disk[key] != listed[key]:
            # both records, so the reader sees whether the size moved or only the bytes did
            problems.append(f"changed: {path} - manifest {listed[key][0]} bytes sha256 {listed[key][1][:16]}..., "
                            f"disk {disk[key][0]} bytes sha256 {disk[key][1][:16]}...")
    # a file on disk the manifest does not list
    for key in sorted(set(disk) - set(listed)):
        problems.append(f"on disk, not in the manifest: {key[0]}/{key[1]}")
    # every row agrees, yet the text differs: its prose, a folder's file count or the totals are not current
    if not problems and written != text:
        problems.append("every file row matches, but the manifest's text (prose, folder counts or totals) is not "
                        "what the generator writes now")
    # every difference is printed, then the reminder that a regeneration is not the answer to an unexplained one
    if problems:
        print(f"[FAIL] dev/spec-sources/MANIFEST.md is not current ({len(problems)} difference(s)):")
        for p in problems:
            print("  " + p.encode("ascii", "backslashreplace").decode("ascii"))   # a non-ASCII name prints escaped
        print("  Explain every changed source before regenerating: a regeneration records the disk as the truth.")
        return 1
    # no difference: the manifest is exactly what a regeneration would write
    print(f"[OK] dev/spec-sources/MANIFEST.md is current: {total_n} files, every size and SHA-256 matches")
    return 0


def main():
    """Rewrite MANIFEST.md from the disk (the default), or verify it with --check."""
    # --check reports and writes nothing; its exit code is the result
    if "--check" in sys.argv[1:]:
        sys.exit(check())
    text, _rows, total_n, total_b, folders = render()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"[OK] wrote {OUT}: {total_n} files, {total_b:,} bytes across {folders} folders")


if __name__ == "__main__":
    main()
