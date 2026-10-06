# Developer notes — S-201 AtoN Studio

For someone who wants to run the app from source, change it, or reuse parts of it in another program. They describe the tree you are holding: version `2.4.12`, cut from commit `facb543` of the development repository (https://github.com/evilp0tat0/s201-aton-studio-dev). The per-change history, the long architecture reference and the commentary on the engineering rules live in that repository; this tree carries what the code needs and what a reader needs to understand it.

Contents: 1 the shape of the tree · 2 running it · 3 reading the source · 4 the feature object · 5 validator rules · 6 verifying a change · 7 sources and citations · 8 the rules the code was written under · 9 reusing parts elsewhere · 10 known limitations · 11 provenance

---

## 1. The shape of the tree

The whole application is one file, `s201_aton_studio.html`: markup, CSS and a single `<script>` block. There is no build step, no package manager and no runtime dependency beyond a browser and a static file server. Everything else is either an asset the page fetches, the machine-readable rule mirror a built-in self-check reads, or the manifest of the specification sources the file cites. The development tools — the command-line gates, sample data, the rule notes — are not in this tree; they run on every cut of it before it is published (section 11).

| Path | What it is | Needed at runtime? |
|---|---|---|
| `s201_aton_studio.html` | The application | yes |
| `Annex_D/Symbols/*.svg` | The S-201 Annex D chart symbols (236 files), fetched one by one as `Annex_D/Symbols/<id>.svg` | for the official symbol preview |
| `Annex_D/portrayal_catalogue.xml` | The Annex D portrayal catalogue, fetched at start | for the official symbol preview |
| `Annex_D/Fonts/` | Droid Sans and Open Sans, referenced by the page's `@font-face` rules | for faithful symbol text |
| `Annex_D/Rules/*.xsl` | The 65 Annex D XSL portrayal templates — the source the JavaScript symbol dispatch was ported from; not fetched | reference |
| `Annex_D/ColorProfiles/` | The Annex D colour profile and SVG style; the palette constants were taken from `colorProfile.xml`; not fetched | reference |
| `lib/leaflet/` | Leaflet 1.9.4, injected only when a user switches a base map on | for the optional map |
| `dev/validator-rules.json` | Machine-readable mirror of the validator corpus, generated from the source; one built-in self-test fetches it from exactly this path | yes — the self-tests run before a session's first validation, and that one reports a failure if the file is missing |
| `dev/spec-sources/MANIFEST.md` | The only file shipped from the reference corpus: the 846 IHO / IALA / OGC / ISO / W3C documents, schemas and text extracts the code cites, each with size, SHA-256 and where to obtain it (section 7) | no — verification aid |
| `start-server.bat`, `start-server.sh` | Launchers: probe for a runtime, serve the folder on port 8080, open the browser | convenience |
| `LICENSE`, `NOTICE.txt` | MIT for the code; third-party terms for Annex D, the fonts and Leaflet | keep with the tree |

If you move things around, keep the fetched paths as they are: `Annex_D/Symbols/<id>.svg`, `Annex_D/portrayal_catalogue.xml`, `Annex_D/Fonts/*.ttf`, `lib/leaflet/leaflet.js` + `leaflet.css`, `dev/validator-rules.json`. They are string literals in the source.

---

## 2. Running it

Serve the folder and open `s201_aton_studio.html` over `http://` (the launchers do exactly that; `python3 -m http.server 8080` is enough). Over `file://` the browser refuses `fetch()`, the symbol preview falls back to a hand-drawn renderer, a banner explains why, and the one self-test that fetches the rule mirror is skipped with a notice. Parsing, validation and generation do not depend on the server.

Two ways to run the built-in self-test suite: the **Run tests** button at the top of the Validator tab, or the query string `?test=1`. The suite also runs once by itself before the first validation of a session, behind an opaque cover: it drives the real screens (switches tabs, walks Builder types, calls the real validator many times) and restores the user's state afterwards. While it runs, the Validator result pane shows fixture findings, not the user's. The data is validated when the run has finished, behind a second cover that stays up for a short hold (`_SCF_DWELL_MS`) after the validation has returned, so that a click made on it cannot reach the app, so the first findings appear once, under the self-test banner; every later validation is immediate. What waits for the self-tests is what the Validator pane shows and the building of a validation report. Rule predicates are evaluated by callers that do not wait, too: the Excel tab's conversion readback (`_impReadback`) and the Builder's import question (`_importGMLTextToBuilder`) show findings on a surface of their own, and the Builder's step gate (`_bwizGateOk`) and nil-reason field list (`_nilFieldOptionsForCurrentFt`) use a predicate's answer to drive a control.

---

## 3. Reading the source

Read the preface comment at the top of the file first: it states what the app is, the four specification layers it stacks (OGC GML 3.2 → IHO S-100 Part 10b → the S-201 Feature Catalogue and DCEG → the IALA recommendations), the precedence rule (IHO/IALA over OGC when they conflict), and the reading discipline — every spec claim in a comment is a pointer to verify against the document, not a fact to trust. The preface also tells you to read the development repository's HANDOFF, CHANGELOG and README; those are not in this tree, and these notes stand in for them.

The script is laid out in this order. Positions move as the file grows, so anchor to symbols with grep, never to line numbers.

| Region | Grep for |
|---|---|
| Version and the machine-readable rule mirror | `const APP_VERSION`, `const FOUNDATIONAL_RULES` |
| Enumerations taken verbatim from the Feature Catalogue — colours, colour patterns, buoy/beacon/topmark shapes, light characters and colours, mark categories, statuses, conditions, fog signals, the navigational-system enum, the ChangeDetails sub-enums, legacy element-name aliases | `const COLOURS`, `COLOURS_STD13`, `CPATTERNS`, `BSHAPES`, `BEASHAPES`, `TMSHAPES`, `LICHARS`, `LICOLS`, `LATCATS`, `CARDCATS`, `SPMCATS`, `STATUSES`, `CONDITIONS`, `FOGSIGNALS`, `MARKS_NAV_NSM`, `CD_ENUMS`, `ALT_FEAT_NAMES` |
| Annex D portrayal engine: the engine singleton, the JavaScript port of the XSL templates, the topmark code map, symbol dispatch and loading | `const PORTRAYAL`, `const SYMBOL_RULES`, `const TOPMARK_SHAPE_CODE`, `function selectSymbolForFeature`, `loadSymbol`, `loadPortrayalCatalogue` |
| The feature-type catalogue (76 entries: the S-201 types plus a few cross-product types tagged `nonS201`) and the group/component helpers that every cross-feature rule uses | `const ATYPES`, `function _aG`, `_compLight`, `_compTopmark`, `_compParent` |
| The per-feature validator rules | `const RULES` |
| The bundled example datasets the self-tests round-trip | `const exGML` |
| Drawing-tab map and the optional Leaflet layer | `function renderMap`, `_loadLeaflet`, `_atonDivIcon`, `_renderMapLeaflet` |
| Symbol composition for one feature (body + topmark + light flare) | `function _renderOfficialSymbol`, `function buildSVG` |
| Parser | `function _parseFeEl` (the per-feature attribute extractor, organised by feature group), `_findFeatures`, `_detectNS`, `function parseGML`, `function parseAllGML` |
| Generator | `_synthesizeShorthandComponents`, `function generateGML`, `function generateAllGML`, `_genCompIM` |
| Exchange Set: catalogue and metadata writers, the ZIP encoder and decoder, the package validator, the download | `generateCatalogXML`, `generateMetadataXML`, `_zipEncode`, `_zipDecode`, `validateExchangeSet`, `downloadExchangeSet`, `_sha256Hex` |
| Builder: form rendering, form → feature sync, feature → form load, the gated import with its fidelity report | `function renderBuilderFields`, `function builderUp`, `_swapBuilderToFeat`, `_importGMLTextToBuilder`, `_importFidelityReport` |
| Compare | `_gmlCompare`, `_cmpZip` |
| Excel → S-201: the native workbook reader, the column mapper, the converter and its readback | `_impParseXlsx`, `_impParseDelimited`, `_IMP_TARGETS`, `_impConvert`, `_impReadback`, `_impRequiredChecks`, `_IMP_SAMPLE_TSV` |
| Builder state arrays (after the import region) | `let compStack`, `let builderFeats` |
| Validator: structural rules, the inline quick-fix, the orchestrator | `function validateGMLStructure`, `function applyQuickFix`, `function runVal`, `_deepFreeze` |
| Self-tests | `async function runSmokeTests` |

Every region opens with a block comment that explains what it does and where its behaviour comes from, with the source cited by document and line range (section 7).

---

## 4. The feature object

The hub of the program is the in-memory feature object — "feat" throughout the source. `parseGML` / `parseAllGML` build feats from XML; `generateGML` / `generateAllGML` emit XML from feats; the Builder loads a feat into its form (`_swapBuilderToFeat`) and writes the form back into it (`builderUp`); validator predicates inspect feats. Four surfaces, one object. Keeping them mutually consistent is the whole game.

What a feat looks like, in outline:

- `ft` is the feature type (`LateralBuoy`, `Lighthouse`, `Topmark`, …) — the element name in the GML, one of the `ATYPES` ids. `gmlId` is the `gml:id`.
- Attribute keys are named after the FC attributes they carry; read `_parseFeEl` for the complete list per feature group, and the FC XML for what each may hold.
- Multi-valued colours are stored as one slash-joined string (`"red/white/red"`) and emitted as one `<colour>` element per band.
- Positions are decimal degrees; the generator writes 7 decimals, as the S-201 Product Specification requires. The Builder accepts DMS and converts on input.
- Child components (lights, topmarks, fog signals, AIS, mooring) ride on the parent as `_compStack` entries and are emitted as separate top-level features with a `<parent xlink:href>` back-link; the component helpers resolve the links in both directions.
- The dataset-level identification block (`S100:DatasetIdentificationInformation`) and the bounding envelope are written by `generateAllGML` from the feature set.

Two invariants protect the object, and the self-test suite asserts both on every bundled sample:

1. **Round trip.** Parsing what the generator produced from a parsed dataset yields the same feats, deep-equal. The moment a field becomes authorable in the generator, the parser must read it back, the Builder must restore it, and a self-test must round-trip it — in the same change. Half-wired fields are the most common bug class in the project's history.
2. **Backward compatibility of the parser.** Every emission an earlier version of the generator produced keeps a read path (the namespace variants, legacy element names in `ALT_FEAT_NAMES`, the older component link forms). A new emission becomes canonical; the old one must still parse.

The Builder UI is a view of the feat, never a second store: the module-scope arrays (`compStack`, `builderFeats`, the sector and colour lists) serialise to and from feat keys, and the DOM is not state.

---

## 5. Validator rules

`runVal` orchestrates (on a session's first validation, after the self-test suite has finished — `_selfChecksFirst`): `validateGMLStructure(text)` runs the structural rules on the raw text first (well-formedness, namespaces, root element, the identification block, `gml:id` uniqueness, link resolution, element order …) and halts if the document is not well-formed; then `parseAllGML` builds the feats and every `RULES` predicate runs on every feat; then the findings render, grouped and sorted by severity, with an inline input and **Apply fix** button under each failing rule that declares a fix. When an Exchange Set ZIP is loaded, `validateExchangeSet` adds the package rules (archive layout, CATALOG.XML content, file naming, declared-versus-shipped cross-references) before the dataset rules.

A per-feature rule is one object in `RULES`:

| Field | Meaning |
|---|---|
| `id` | Prefix declares the source family: `GML-STR-*` structural, `S100-*` S-100 Part 10b, `S158-*` S-158:100 checks, `S201-*` the S-201 Feature Catalogue and DCEG, `R1001-*` / `R0110-*` / `R0106-*` / `R0126-*` / `R0201-*` / `R0108-*` the IALA recommendations, `RNG-*` / `GEO-*` range computations, `ENC-*` S-158:101 cross-checks, `S158-PKG-*` / `S201-ES-*` exchange-set packages |
| `s` | Severity. `critical`, `error` and `warning` are the IHO S-158 check classifications C / E / W carried natively; `info` is the advisory tier for rules outside that classification (IALA recommendations, ENC cross-checks, informative computations) |
| `m` | The message. It names the source in prose — a finding must teach the specification, "invalid value" alone is not acceptable |
| `ref` | The citation, resolvable in a source listed in the manifest (section 7) |
| `t(feat, allFeats)` | The predicate: `true` passes, `false` fails. It asserts **presence before validity** — a missing value must fail a rule that requires one; the shape `!f.x || f.x === "valid"` is forbidden because an empty field would pass silently |
| `fix`, `actualOf`, `expected` | Optional: the quick-fix declaration (field, input type, options, wrapper, target) and the structured actual / expected values the finding is rendered from |

The corpus totals 268 rules: 216 per-feature entries in `RULES`, 25 structural rules in `validateGMLStructure`, 27 package rules in `validateExchangeSet`. `dev/validator-rules.json` mirrors all of them (id, severity, message, citation, layer, fix declaration); it is generated from the source in the development repository, and a built-in self-check compares it with the in-app rules. The self-test suite also asserts `RULES.length` against a literal, so adding a rule means bumping that assertion.

To add a rule: find the constraint in the source document and note the line range; choose the prefix; write the object with its citation in the inline comment; bring `dev/validator-rules.json` in step (the self-check that reads it reports any drift); bump the length assertion in `runSmokeTests`; run the self-test suite.

---

## 6. Verifying a change

Run the built-in self-test suite: **Run tests** at the top of the Validator tab, or open the app with `?test=1`. It holds 558 invariants and should report every one passed.

The suite covers the round trip of every bundled sample, determinism of the output, the rule corpus size and shape, the structural rules against known-good and known-bad documents, Builder form ↔ feat fidelity, quick fixes, the ZIP encoder and decoder, the SHA-256 implementation against the FIPS vectors, the spreadsheet importer end to end, and XSS inertness of every surface that renders user-file text. When you add an invariant, register it with the suite's `_t` helper next to the region it protects.

The command-line gates (a static pre-commit check, a headless browser run of the same suite with its import and schema legs, the rule-mirror generator) live in the development repository and are not part of this tree; every cut of it passes them before it is published.

---

## 7. Sources and citations

Precedence: **IHO and IALA over OGC.** S-201 is a profile of S-100, and S-100 restricts and overrides OGC GML wherever it says so; OGC is the substrate, not the authority.

The single source of truth for enumerations, multiplicities and feature types is the S-201 Feature Catalogue 2.0.0 XML. Every enum constant's values, every `ATYPES` entry and every mandatory-attribute rule was copied from it, and the inline comments cite it by line range (`FC 2.0.0 XML L11003-11023`). The multiplicity flag deserves care: `infinite="false"` with an upper bound of 1 means 0..1, not 0..*; misreading it caused a real round-trip bug once.

**None of the cited material is in this tree.** The publications, the Feature Catalogue XML, the schema families and the text extracts are all freely available from their official sources, and `dev/spec-sources/MANIFEST.md` lists every file the development repository holds, with its size, SHA-256 and the place to obtain it. To follow a citation: fetch the named file, check that its SHA-256 matches the manifest, and put it at the manifest path relative to the project root (`dev/spec-sources/201_Feature_Catalogue_2.0.0.xml`, `dev/pdf-extracts/r1001_ed2_full.txt`, …). A matching hash means you hold byte-for-byte what the citations were checked against, so the line numbers resolve. The text extracts are regenerated from the publications (PyMuPDF), not downloaded — the manifest says so per folder.

Where the citation forms point:

| Citation looks like | Resolves in |
|---|---|
| `FC 2.0.0 XML Lnnnn`, `FC line N-M` | `201_Feature_Catalogue_2.0.0.xml` from the IHO Geospatial Information Registry, at the manifest path |
| `r1001_ed2_full.txt L384-393`, `s201_ps_2_0_0_main_full.txt L1091-1093`, `s158_100_checks_table.txt L271` (a file name plus a line range) | The named plain-text extract of the IHO or IALA publication, at `dev/pdf-extracts/<name>` once regenerated; the manifest names the publication behind each extract |
| `S-100 Pt 10b §10b-11.7`, `S-201 PS §10.14`, `DCEG §2.4.7`, `R1001 Table 3` | The named section of the IHO or IALA publication (edition and SHA-256 in the manifest) |
| OGC GML 3.2 schema, S-100 XSDs, ISO 19115/19139 XSDs, `xlink.xsd` / `xml.xsd` | The schema files at the manifest paths `dev/spec-sources/ogc-gml/`, `s-100-xsd/`, `iso-xsd/`, `w3c-xsd/` |
| S-201 Annex B XSD | `dev/spec-sources/s-201-xsd/` — the edition 2.0.0 schema (its targetNamespace is the dataset namespace `NS_S201`, its imports the S-100 and GML namespaces `NS_S100` / `NS_GML`; the structural rules cite it for the namespaces, the root, the member container and the order) and the edition 1.1.0 Annex B1 XSD (a legacy namespace; the `<imember>` / `<member>` containers its Annex B2 document describes, which the parser still reads) |
| S-62 producer codes | `dev/spec-sources/iho-additional/S-62_ProducerCodes.csv` + `.json`, extracted from the IHO S-62 register |
| Annex D symbol dispatch | `Annex_D/Rules/*.xsl` (the templates `SYMBOL_RULES` was ported from) and `Annex_D/portrayal_catalogue.xml` — these ARE in the tree |
| PKZIP APPNOTE, FIPS 180-4 | General-knowledge specifications for the ZIP layout and SHA-256; the SHA-256 is locked to the published test vectors by the self-tests |

A rule's `ref` and a comment's citation are hypotheses to check, not facts to trust: open the cited lines before relying on them, and never add a citation from memory. If a claim cannot be traced to a manifest-listed source, it does not ship.

---

## 8. The rules the code was written under

The in-app `FOUNDATIONAL_RULES` constant holds all 26 engineering rules with their rationale; the development repository keeps their machine-readable form, and a self-test checks the constant is complete. The ones that will bite you first:

- **Verify before you code.** A change that touches a specification construct is checked against the primary source first, and the inline comment cites the exact lines.
- **Zero fabrications.** No enum value, attribute, element, formula or section number that is not in a cited, manifest-listed source.
- **No silent passes.** Predicates assert presence before validity.
- **Round trip is invariant; the parser stays backward-compatible** (section 4).
- **The feat is the only state.** The Builder UI is a view; the DOM is not state.
- **Determinism.** Identical input gives byte-identical output; no clock, no randomness, no network in the parser, generator or validator.
- **Data custody.** User text moving between the app's surfaces (Builder output, Drawing input, Validator input, the clipboard, a download, an Exchange Set member) travels byte-verbatim or through a transform the user explicitly chose and can see reported.
- **Official nomenclature verbatim.** Labels, dropdown values and messages that name a spec concept use the source's exact words.
- **Findings teach the spec.** Every message names its source and the finding carries structured actual / expected fields.
- **Single source or gate.** A count, a version or an anchor that lives in more than one place is either generated from one source or checked by a gate. (That is why these notes carry their numbers as placeholders filled at build time.)
- **Bump `APP_VERSION` on every change**, following the semver policy stated above the constant: MAJOR when GML output changes shape, MINOR for new rules, types or UI, PATCH for fixes.

---

## 9. Reusing parts elsewhere

The script defines everything at module scope, so any function can be lifted; what each piece depends on:

- **Parser and generator** (`parseAllGML`, `generateAllGML` and their helpers) need the enum constants, `ATYPES`, the component helpers, and the browser's `DOMParser` / `XMLSerializer`. In Node or a worker, supply a DOM implementation with namespace-aware parsing.
- **Validator predicates** are functions of the parsed feats (`t(feat, allFeats)`) and need the same constants; `validateGMLStructure` works on the raw text with `DOMParser`. The JSON mirror is enough for tooling that only needs the rule list, severities and citations.
- **Portrayal** (`selectSymbolForFeature`, `_renderOfficialSymbol`, `buildSVG`) needs `fetch` for the symbols and catalogue and an SVG-capable DOM; the colour classes the symbols reference are in the page's CSS.
- **ZIP and hashing:** `_zipEncode` is pure JavaScript; `_zipDecode` uses `DecompressionStream` for DEFLATE members; `_sha256Hex` is pure JavaScript by design (WebCrypto is a secure-context API, unavailable over plain `http://` on a LAN).
- **The spreadsheet reader** (`_impParseXlsx`, `_impParseDelimited`) is pure JavaScript over `_zipDecode` and `DOMParser` — no library.

Keep the S-201 namespace (`NS_S201`, the S-201 2.0.0 schema's), the element order and the component link form as the generator writes them; other validators check them. The code is MIT; the Annex D material is © IHO / IALA and travels with `NOTICE.txt`.

---

## 10. Known limitations

- Validation is rule-based, not XSD or Schematron; the schema families are reference material (manifest-listed, not shipped). A pure-JS XSD validator would be needed to add schema validation. In the development repository, pre-commit check #20 validates the bundled samples against the S-201 2.0.0 schema and checks that shapes the structural rules report fail it, and the browser gate's XSD leg validates the GML the app writes against it; in this tree neither runs (the schema is not shipped).
- No S-158:201 (S-201-specific validation checks) has been published by the IHO yet; the corpus will be cross-referenced against it when one appears. The subgroup's development repository is <https://github.com/iho-ohi/S-100-Validation-Checks>.
- Package validation covers structure, catalogue content and cross-references; Part 15 digital signatures are checked for presence and algorithm only (verification needs the IHO Data Protection Scheme certificate chain).
- The producer-code rule accepts any four-character `[A-Z0-9]` code; strict membership in the S-62 list is future work.
- Over `file://` the symbol library cannot be fetched (fallback renderer). The optional base map fetches public tiles when switched on; off means no network.
- `Annex_D/portrayal_catalogue.xml` registers fewer symbols than `Annex_D/Symbols/` holds; the loader fetches by file name, so rendering does not depend on the registry.
- For clean fixtures, use the in-app `exGML` samples.
- A set of optional FC sub-attributes round-trips through parser, generator and validator but has no Builder authoring field yet.

---

## 11. Provenance

The header of these notes names the source repository, the commit this tree was cut from and the `APP_VERSION` at that commit. Left out on purpose: the development documents and tools, and every piece of third-party reference material (listed in the manifest instead). The tree is produced by the development repository's `build-public-snapshot.py`. It first cuts the full development set and verifies it with the command-line gates, then keeps under `dev/` only the paths the app's code names plus the citation manifest. `README.md` and these notes are rendered from templates at that moment, with every number filled from the tree itself.
