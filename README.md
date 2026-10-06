# S-201 AtoN Studio

A single-file web app for **IHO/IALA S-201 Aids to Navigation** data: it parses S-201 GML datasets, draws every aid with its official Annex D chart symbol, authors new datasets through a guided form, validates them against the IHO and IALA sources it cites, packages and checks S-100 Exchange Sets, compares two editions, and converts spreadsheet AtoN lists into S-201 (the spreadsheet conversion still needs some work — it is not finished).

Version **2.4.12**. No install, no internet needed at runtime (one optional base-map overlay is the only feature that fetches anything).

See [DEVELOPER-NOTES.md](DEVELOPER-NOTES.md) for how the code is organised and how to change it safely.

---

## Quick start

The app must be served over `http://` (browsers block `fetch()` from `file://`, and the symbol library, fonts and catalogue are fetched). Any static file server works.

**Windows** — double-click `start-server.bat`. It finds Python or Node, serves the folder on port 8080 and opens the browser. Ctrl+C in the console stops it.

**macOS / Linux**
```bash
chmod +x start-server.sh
./start-server.sh
```

**By hand, any platform**
```bash
python3 -m http.server 8080
```
then open <http://localhost:8080/s201_aton_studio.html>.

Opening the HTML file directly also works, but the preview then falls back to a hand-drawn renderer instead of the official symbols, and a banner says so. Parsing, validation and generation are the same either way.

---

## What it does

| Tab | Purpose |
|---|---|
| **Drawing** | Paste data in GML format: every feature is parsed and rendered with its Annex D symbol (topmark and light flare composed on the body), listed as a parent/child tree with a summary and a filterable check table, and plotted on an auto-scaled map. |
| **Builder** | A step-by-step form for authoring datasets from scratch — every S-201 feature type, component stacking (lights, topmarks, fog signals, AIS, mooring), multi-colour bands, DMS or decimal positions, parent/peer references, several aids in one dataset. Hands the GML to the Validator. |
| **Validator** | Structural GML checks, per-feature rules from the S-100, S-158, S-201 and IALA sources, Exchange-Set ZIP ingest with package checks and CRC verification, inline "Apply fix" buttons, downloads of the dataset or a complete Exchange Set, and SHA-256 delivery-integrity checks. Findings use the IHO S-158 classification (critical / error / warning) plus an advisory info tier for IALA best practice. |
| **Compare** | The change record between two deliveries — two `.gml` files or two Exchange Set `.zip`s: features added, removed and modified with old and new values, geometry moves, metadata changes, renumbering hints. |
| **Excel → S-201** | Load a workbook, CSV or pasted cells, map its columns to S-201 fields, fill what the sheet omits with IALA conventions or same-for-all values, convert, read the conversion report, and hand the result to the Builder, the Validator or a file. |

Everything runs in the browser; nothing is uploaded anywhere.

---

## What is in the tree

```
s201_aton_studio.html       the application (markup + CSS + one script)
Annex_D/                    S-201 Annex D portrayal library: symbols, fonts, XSL templates,
                            colour profiles, portrayal catalogue (© IHO / IALA, see NOTICE.txt)
lib/leaflet/                Leaflet 1.9.4, loaded only for the optional base map
dev/validator-rules.json    machine-readable mirror of the validator corpus (read by a built-in self-check)
dev/spec-sources/MANIFEST.md every IHO / IALA / OGC / ISO / W3C document, schema and text extract the
                            code cites (846 files), with size, SHA-256 and where to obtain it
start-server.bat / .sh      launchers
LICENSE, NOTICE.txt         MIT for the code; third-party terms for the bundled material
```

This tree holds what the app needs to run: the HTML file, `Annex_D/`, `lib/` for the map, and `dev/validator-rules.json`, which a built-in self-check reads. The one other file under `dev/` is the citation manifest. The development tools (the command-line gates, sample data, the rule notes) are not part of it; they run on every cut of this tree before it is published.

---

## Check that it works

Open the Validator tab and click **Use example** — a bundled three-feature dataset loads and validates cleanly. The first validation after the page is opened runs the built-in self-test suite first, behind a cover, and shows its result in a banner above the findings. Click **Run tests** at the top of that tab (or open the app with `?test=1`) to run the built-in self-test suite; it should report every invariant passed.

---

## Sources

The app implements the **IALA S-201 Product Specification 2.0.0** (May 2025) on the IHO S-100 framework. Every enumeration, multiplicity, symbol rule, colour value and validator rule is taken from a primary document — the S-201 Feature Catalogue 2.0.0 XML, the S-201 DCEG and Portrayal Catalogue, IHO S-100 Ed 5.2.0, IHO S-158, and the IALA R- and G-series recommendations (R1001 Maritime Buoyage System, R0110 rhythmic characters, R0106, R0126, R0201, R0202, R0108 and others). The rule corpus in `dev/validator-rules.json` carries the citation of every rule.

Datasets are written in the namespace of the S-201 2.0.0 Annex B schema, `http://www.iho.int/S-201/gml/cs0/1.0`, since app version 2.0.0. Files written by earlier versions (namespace `http://www.iho.int/S-201/gml/cs0/2.0`) still open everywhere; the Validator reports their namespace as critical and offers a one-click fix, and the Builder writes them back in the 2.0.0 namespace and says so on import.

The publications, the Feature Catalogue XML, the schemas and the text extracts are not included; all are freely available from their official sources, and `dev/spec-sources/MANIFEST.md` lists each file with its size, SHA-256 and where to obtain it.

---

## License

The code is free. It is licensed under the **MIT License** ([LICENSE](LICENSE)) — you can use it, change it and share it.

The chart symbols and portrayal data in the `Annex_D/` folder come from the IHO/IALA S-201 specification and are **© IHO / IALA**. To reuse that material, check with the IHO and IALA. Full third-party terms are in [NOTICE.txt](NOTICE.txt).
