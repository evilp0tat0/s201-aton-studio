#!/usr/bin/env python3
"""generate-spec-sources-manifest.py — regenerate dev/spec-sources/MANIFEST.md.

The public snapshot repository redistributes NONE of the third-party reference
material the development repository holds: the IHO and IALA publications, the
S-201 Feature Catalogue XML, the IHO S-100 / S-201 schema families and the OGC,
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
  python dev/scripts/generate-spec-sources-manifest.py
"""
import hashlib
import os

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
        "IHO Geospatial Information Registry <https://registry.iho.int>."),
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
        "Plain-text extractions of the publications above (PyMuPDF; the `.docx`-derived one by a "
        "zipfile + document.xml parse), regenerable from the originals; `MANIFEST.sha256` is the "
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


def main():
    groups = collect()
    lines = []
    lines.append("# Reference-source manifest\n")
    lines.append(
        "The public snapshot of S-201 AtoN Studio redistributes **none** of the third-party reference "
        "material listed here: the IHO and IALA publications, the S-201 Feature Catalogue XML, the IHO "
        "S-100 / S-201 schema families with the OGC, ISO and W3C schemas they import, the S-158 check "
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
        "publications, not downloaded.\n")
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
            lines.append(f"| {os.path.basename(full)} | {size:,} | `{sha256(full)}` |")
    lines.append(f"\n---\n\n**Total: {total_n} files, {total_b:,} bytes.** "
                 "Regenerate this manifest with `python dev/scripts/generate-spec-sources-manifest.py` "
                 "whenever a file under these folders is added, replaced or removed.\n")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[OK] wrote {OUT}: {total_n} files, {total_b:,} bytes across {len(groups)} folders")


if __name__ == "__main__":
    main()
