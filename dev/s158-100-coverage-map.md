# S-158:100 coverage map — Collection A dispositions

Machine-generated disposition of ALL 324 IHO S-158:100 Ed 1.0.0 **Collection A** checks against the app's validator corpus (per-check verdicts produced by the grounded parallel-agent mining sweep; sources: `dev/pdf-extracts/s158_100_checks_table.txt` [machine-readable check table], `s158_100_full.txt`, `s158_intro_structure_full.txt`). Collection B (88 checks) is reference-only by the spec's own instruction — S-158:100 §4.2: Collection B checks "are not expected to be implemented in validation software for datasets, exchange sets, and exchange catalogues" (`s158_100_full.txt` L388-393).

**Verdict key:** `covered` = an existing rule already tests it · `partial` = subset covered, gap noted · `candidate` = implementable on the parsed single-dataset feat model (BACKLOG unless an Implemented rule is named) · `candidate-parser` = needs parser extension first · `na-format` = other data format (ISO 8211 / HDF5 — omission permitted by §4.2) · `na-package` = exchange-set/catalogue level checks the offline app still cannot run (PKI verification / producer history / unsatisfiable preconditions) — since pass 637 the app INGESTS exchange sets (validateExchangeSet), so implementable package checks are classified covered/partial/candidate instead · `na-other` = not expressible in S-201 vector GML (reason noted).

**Totals:** 324 checks — na-format: 179 · na-package: 17 · candidate: 77 · partial: 17 · covered: 24 · na-other: 9 · candidate-parser: 1. Pass-637 exchange-set batch: 18 S158-PKG rules closing 15 checks fully + 5 partially, and 30 formerly-na-package checks re-classified candidate (ZIP-ingest context now exists).

**Severity map** (S-158 Introduction Table 7-1 + §7.1, `s158_intro_structure_full.txt` L991-1014; PS §6.2 publication gate `s201_ps_2_0_0_main_full.txt` L812-822): the Classification letters are carried natively — C → `critical`, E → `error`, W → `warning`. (The app's `info` severity is the advisory tier for rules outside the S-158 ring and never encodes a check letter; disclosed adaptations — S158-PKG-18, S201-LGT-05 — report below their letter with the deviation stated at the rule.)

| Check | Cls | Verdict | Implemented | Note |
|---|---|---|---|---|
| 100_0001 | C | partial |  | S201-DEP-01 flags 12 known legacy/orphan attributes and GML-STR-12 flags extraneous DII fields, but _findFeatures/_parseFeEl silently skip any unknown feature/information element or attribute — gap needs a structural DOM sweep of <members> children + attribute element names against ATYPES/FC lists. |
| 100_0002 | E | candidate | S158-DUP-01 | DUP: t(f,all) pairwise-compares a canonical key-sorted serialization of each feat (all parsed attributes + geometry lat/lon/coordinates, excluding gmlId and _-internal keys) and fails when another feat is byte-identical; GML-STR-16 only catches duplicate gml:id, not duplicate objects. |
| 100_0003 | C | covered |  | S100-GML-03 (geometry presence or parent-xlink inheritance, FC noGeometry types skipped) + S100-GML-05 (parsed point/curve/surface primitive must be in the feature type's FC GEOM_PRIM permittedPrimitives) — both predicates confirmed. |
| 100_0004 | C | partial |  | Dozens of per-binding multiplicity rules exist (S201-FEA-02/03/23, S201-COL-01 1..*, S201-FEA-37/38/39 inner 1..1, S201-EQP-PARENT-01 parent 1..1, GML-STR-19 lightSector 1..10) but coverage is hand-picked, not FC-exhaustive, and attribute bindings NOT in the FC pass silently (parser ignores unknown elements). |
| 100_0005 | C | partial |  | Enum-membership rules cover the major attributes (S201-FEA-04/05, S201-ENUM-SPM/TMS, S201-COL-01..06, S201-FEA-44/45, S201-STA-02) and S100-NIL-01 validates permitted nil values, but many FC-bound enum attributes have no membership rule. |
| 100_0006 | C | partial | S158-FMT-01 | S158-FMT-01 now flags non-canonical lexical reals (leading/trailing-dot like .6 / 6.) across the 26 flat FC real/integer keys, with a rewrite quick-fix + Builder canonicalization via the shared `_canonSweepAuthoring` helper at BOTH the collect sweep and the `builderImportFromDrawing` boundary (flat keys + the internal aliases nominalRange / fogSignalFrequency / fogSignalOutput / fogValueOfMaximumRange + the light/topmark sub-object scalars the standalone emits read; visible import receipt). Residual gaps: (a) nested numeric leaves (rhythmOfLight.signalPeriod, sector scalars, signalSequence durations, complex-attr leaves — incl. radarWaveLength.waveLengthValue); (b) boolean/URL lexical forms; (c) PREDICATE blind spot: a parsed FogSignal stores its numerics under the fog*-prefixed flat aliases, so the rule never fires on a raw FogSignal `.5` even though FC-based external validators reject it — the Builder sweep heals authored/imported output, but detection on raw files needs a predicate alias extension (+ validator-rules.json regen) in a future pass. |
| 100_0007 | C | candidate | S158-ASSOC-01 | ASSOC: predicate fails when f.gmlId appears in f.componentRefs / f.parentRefs / f.aisBroadcastByRefs / f.aisBroadcastsRefs / f._assocRoleRefs[role].refs (parser strips leading '#'); no existing rule tests self-reference. |
| 100_0008 | C | candidate |  | ASSOC: must be a structural DOM check (validateGMLStructure) counting same-role xlink:href occurrences per target per feature element and flagging >1 — the parser dedupes refs via a `seen` Set in componentRefs/parentRefs/_assocRoleRefs, so per-feature predicates cannot see repeats. |
| 100_0009 | E | partial | S158-ASSOC-02 | S201-REL-01 (feature must not be both parent and child) catches loops in bidirectionally-encoded data, but a unidirectional <parent>-only cycle (A.parentRefs→B, B.parentRefs→A) passes — gap needs a DFS cycle walk over parentRefs/componentRefs across allFeats. |
| 100_0010 | C | covered |  | GML-STR-17 — every fragment-style xlink:href must resolve to a gml:id declared in the same document (document-wide, comment/CDATA-masked, quote-agnostic; predicate confirmed); non-fragment external refs are outside single-dataset scope. |
| 100_0011 | C | candidate | S158-ASSOC-01 | ASSOC: same self-reference predicate as 100_0007 scoped to information-type feats (ATYPES g=itype are parsed as feats and carry _assocRoleRefs for the info-association roles). |
| 100_0012 | C | partial |  | S201-EQP-PARENT-01 (Equipment/Topmark parent binding exactly 1..1) + S201-EQP-PARENT-02 (parent target must be a StructureObject) cover the key FC binding; gap: no generic FC featureBinding/informationBinding validity+multiplicity check — the 25 _ASSOC_ROUNDTRIP_ROLES are round-tripped but never validated. |
| 100_0013 | E | candidate |  | CRS: structural DOM scan flagging any srsName attribute on gml:pos/gml:posList (DirectPosition level) rather than on the geometry primitive or Envelope; nothing tests srsName placement today (GML-STR-21 tests determinability, S100-CRS-01 tests value). |
| 100_0014 | C | na-other |  | S-100 Part 10b inline GML geometry has no GM_PointRef encoding — curve/surface segments carry direct positions (gml:pos/posList) only, and feature-level geometry reuse via xlink is a separate, permitted Part 10b mechanism, so the indirect-position construct cannot occur in S-201 GML. |
| 100_0015 | E | candidate |  | GEOM: structural DOM scan of gml:segments children whitelisting S-100-permitted segment types / interpolation attribute values (linear, geodesic, loxodromic, arc forms) and flagging others — the parser reads only posList so this must live in validateGMLStructure. |
| 100_0016 | E | candidate |  | GEOM: DOM check that every surface patch (gml:PolygonPatch/gml:Polygon) has interpolation absent, 'none', or 'planar'. |
| 100_0017 | E | candidate |  | GEOM: DOM check that all patches inside one gml:Surface/gml:patches share a single interpolation value. |
| 100_0018 | E | candidate |  | GEOM: DOM check gml:Polygon/PolygonPatch interpolation='planar' when the attribute is present. |
| 100_0019 | C | candidate | S158-GEOM-01 | GEOM: DOM check every gml:Curve carries a gml:segments child with >=1 segment element — the parser silently yields an empty coordinates[] for a segmentless curve and S100-CRS-02's .every() passes vacuously. |
| 100_0020 | C | candidate | S158-CRS-01 | CRS: collect distinct srsName values across all geometry elements + Envelope (DOM, or f.geometry.srsName over allFeats) and flag >1 distinct CRS — S100-CRS-01 only tests each value against 4326/CRS84 individually, so a mixed EPSG:4326/CRS84 dataset passes. |
| 100_0021 | C | candidate |  | GEOM: O(n²) segment-pair intersection test per ring over DOM gml:exterior/gml:interior posList pairs (parser keeps only the exterior ring, so DOM-level; exterior-only version could use f.geometry.coordinates). |
| 100_0022 | E | candidate |  | GEOM: DOM check every gml:Surface patch is a PolygonPatch (or the geometry is a gml:Polygon), flagging any other patch subtype. |
| 100_0023 | C | candidate |  | GEOM: DOM check each Polygon/PolygonPatch has exactly one gml:exterior child (and only gml:interior siblings) — parser takes the first ring found and never checks boundary structure. |
| 100_0024 | C | candidate | S158-GEOM-02 | GEOM: first-vertex==last-vertex check per ring — exterior ring available on f.geometry.coordinates for surfaces, interior rings via DOM posList. |
| 100_0025 | C | candidate |  | GEOM: DOM check each gml:Point contains exactly one gml:pos whose token count equals srsDimension (2) — the parser silently truncates extra coordinate tokens. |
| 100_0026 | C | na-other |  | No S-201 FC AtoN type permits a multipoint primitive, and gml:MultiPoint members are Points by GML schema construction, so the violation is not expressible in S-201 vector GML. |
| 100_0027 | C | candidate |  | GEOM: DOM read of S100/gml ArcByCenterPoint startAngle, flag values outside [0.0, 360.0] (parser ignores arc segments entirely, so structural). |
| 100_0028 | C | candidate |  | GEOM: DOM read of ArcByCenterPoint angularDistance, flag values outside [-360.0, +360.0]. |
| 100_0029 | C | candidate |  | GEOM: DOM read of ArcByCenterPoint radius (+uom), flag radius >= ~20,004 km (minimum geodesic centre-to-antipode distance on WGS84) as a conservative constant bound. |
| 100_0030 | C | candidate |  | GEOM: DOM scan for geometry primitives (Point/Curve/Surface with gml:id) that are neither descendants of a recognised feature element nor referenced by any feature's geometry-property xlink:href — orphans are currently invisible ( _findFeatures ignores them, GML-STR-17 checks the opposite direction). |
| 100_0031 | C | covered |  | S100-GML-05 — a curve-primitive feature type (per FC GEOM_PRIM, e.g. NavigationLine) carrying point/surface geometry fails the permittedPrimitives membership test (the 8211 'geometry field' distinction collapses onto the same predicate in GML). |
| 100_0032 | C | na-format |  | RCNM record-name codes are ISO/IEC 8211 (Part 10a) constructs; the GML analogue — only Point/Curve/Surface primitives — is inherent in the parser's geometry model plus S100-GML-05. |
| 100_0033 | C | covered |  | S100-GML-05 — a surface-primitive feature type carrying non-surface geometry fails the same FC permittedPrimitives test (the RCNM!=130 example is the 10a encoding of the identical constraint). |
| 100_0034 | C | candidate |  | GEOM: DOM ring math counting vertices shared between the exterior posList and each interior posList, flagging >1 shared node (interior rings are dropped by the parser, so structural). |
| 100_0035 | C | candidate |  | GEOM: DOM check that consecutive curve segments / composite-curve members have coincident end/start coordinates (parser flattens all segment posLists, hiding the discontinuity). |
| 100_0036 | C | candidate |  | GEOM: shoelace signed-area over the surface exterior ring (f.geometry.coordinates or DOM posList), flagging counter-clockwise exterior boundaries. |
| 100_0037 | C | candidate |  | GEOM: shoelace signed-area over each gml:interior ring (DOM — parser discards interiors), flagging clockwise interior boundaries. |
| 100_0038 | C | candidate |  | GEOM: point-in-polygon test of each interior ring's vertices against every other interior ring (DOM posList), flagging nested interiors. |
| 100_0039 | C | candidate |  | GEOM: point-in-polygon test that every interior ring lies within the exterior ring (DOM posList), flagging escapees. |
| 100_0040 | C | candidate |  | GEOM: point-in-polygon test flagging an exterior boundary contained within an interior boundary (DOM posList). |
| 100_0041 | C | candidate |  | GEOM: DOM count of geometry-carrying property children per feature element, flagging >1 — the parser silently keeps only the first geometry it finds. |
| 100_0042 | C | candidate | S158-GEOM-05 | GEOM: segment-pair self-intersection sweep over curve coordinates (f.geometry.coordinates for parsed curves; DOM posList for composite curves). |
| 100_0043 | C | na-format |  | SPAS/ORNT are ISO/IEC 8211 (Part 10a) spatial-association fields; GML has no point-orientation construct to violate. |
| 100_0044 | C | na-format |  | PTAS/INSERT are ISO/IEC 8211 update-record mechanics with no equivalent in a GML dataset. |
| 100_0045 | C | candidate | S158-GEOM-03 | GEOM: consecutive-duplicate-vertex check over f.geometry.coordinates for curves (and the surface exterior ring) — the parser already collects the pairs, making this a pure per-feature predicate. |
| 100_0046 | C | candidate | S158-GEOM-04 | GEOM: flag a closed curve/ring (first==last vertex) whose total vertex count is <4 (fewer than 2 intermediate vertices) using f.geometry.coordinates / DOM posList. |
| 100_0047 | E | na-format |  | Part 8 coverage-dataset content rule (collection of coverages + metadata); the vector analogue — at least one feature inside <members> — is already enforced by GML-STR-14. |
| 100_0048 | C | na-format |  | CV_GridCoordinate/axisNames ordering is a Part 8 grid-coverage construct; S-201 is a vector GML product with no coverages. |
| 100_0049 | C | na-format |  | Grid-coordinate offset values are Part 8 coverage constructs absent from S-201 vector GML. |
| 100_0050 | C | na-format |  | S100_IF_GridValues/rangeType value records are Part 8 coverage constructs absent from S-201 vector GML. |
| 100_0051 | E | na-format |  | ISO/IEC 8211 record field-count rule (Part 10a); S-201 delivery is Part 10b GML, not 8211. |
| 100_0052 | C | na-format |  | ISO/IEC 8211 repetition-factor rule (Part 10a); no GML equivalent. |
| 100_0053 | C | na-format |  | ISO/IEC 8211 mandatory record/field/subfield rule (Part 10a); the GML-side mandatory-element analogues are separately enforced by GML-STR-10/11/13/14 plus the per-feature mandatory-attribute rules. |
| 100_0054 | C | na-format |  | ISO/IEC 8211 prohibited record/field rule (Part 10a); no GML equivalent (extraneous DII fields are the one GML analogue, flagged by GML-STR-12). |
| 100_0055 | C | na-format |  | ISO/IEC 8211 record-update check (RUIN Insert/Modify with no further fields, Part 10a); S-201 GML has no 8211 records. |
| 100_0056 | C | na-format |  | Part 10a 10a-7.3.1 FOID record-splitting mechanics (same FOID across multiple 8211 records) do not exist in the Part 10b GML encoding. |
| 100_0057 | C | na-format |  | Part 10a 10a-7.3.1 FOID/geometric-primitive record rule for 8211 feature records; no GML counterpart of shared-FOID record chains. |
| 100_0058 | C | na-format |  | PTAS field is an ISO 8211 curve-record construct (Part 10a 10a-7.2.4.1); GML curves carry inline posList, no PTAS. |
| 100_0059 | C | candidate-parser |  | Duplicate-edge-reference test (Part 7 7-4.3.2) would need the parser to collect xlink-referenced curve/edge ids from composite curves and surface boundaries; it currently parses only inline posList coordinates (Point/LineStringSegment/LinearRing branches in _parseFeEl), so no edge references exist on feat objects. |
| 100_0060 | C | na-format |  | Explicitly an ISO 8211 record-order check (Part 10a); the GML-level DII element-order analogue is separately handled but this check targets 8211 files. |
| 100_0061 | C | na-format |  | RUIN/RVER are ISO 8211 update-record subfields (Part 10a); S-201 GML datasets carry no RUIN/RVER. |
| 100_0062 | C | na-format |  | RVER sequencing is 8211 update-mechanism bookkeeping (Part 10a); not present in GML. |
| 100_0063 | C | na-format |  | RCNM/RCID record-identifier uniqueness is 8211-specific (Part 10a); the GML identity analogue (document-unique gml:id) is already enforced by GML-STR-16. |
| 100_0064 | C | na-format |  | Delete/Modify update records referencing nonexistent RCNM/RCID pairs is 8211 update-dataset mechanics (Part 10a); the app validates single base GML datasets. |
| 100_0065 | C | na-format |  | RCNM/RCID uniqueness for records without RVER is 8211-specific (Part 10a); GML analogue gml:id uniqueness is covered by GML-STR-16. |
| 100_0066 | C | na-format |  | Permissible-range test on ISO 8211 subfield values (Part 10a 10a-5/6/7); GML attribute-value range/enum validity is a different construct handled by the S201-* attribute rules. |
| 100_0067 | C | na-format |  | Data descriptive fields are ISO 8211 DDR constructs (Part 10a); no counterpart in GML. |
| 100_0068 | C | na-format |  | UTF-8 implementation-level-1 constraint on 8211 Character Data subfields (Part 10a 10a-4.5); GML encoding declaration is separately checked (GML-STR-03) but this check targets 8211 files. |
| 100_0069 | C | na-format |  | The %/G escape sequence is an ISO 8211 lexical-level construct (Part 10a 10a-4.5); not applicable to GML. |
| 100_0070 | C | na-format |  | ATTR-NATC numeric attribute codes and the ATCS-ANCD dictionary are 8211 encoding artifacts (Part 10a 10a-5.1.5); GML uses named attribute elements. |
| 100_0071 | C | na-format |  | ATTR-ATIX index sequencing is 8211 attribute-record bookkeeping (Part 10a); no counterpart in GML. |
| 100_0072 | C | na-format |  | ATTR-ATIX validity under Modify is 8211 update mechanics (Part 10a); not applicable to GML base datasets. |
| 100_0073 | C | na-format |  | ATTR-PAIX parent-attribute indexing is an 8211 subfield construct (Part 10a); GML nests complex attributes as XML elements. |
| 100_0074 | C | na-format |  | RUIN/ATIN insert-consistency is 8211 update mechanics (Part 10a); not applicable to GML. |
| 100_0075 | C | na-format |  | RCID range [1, 2^32-2] is an 8211 record-identifier constraint (Part 10a 10a-4.4); GML uses gml:id NCName strings (checked by GML-STR-15/16). |
| 100_0076 | C | na-format |  | RRNM/RRID/NIAC/NARC information-association keying is 8211-specific (Part 10a 10a-5.2.1); GML associations use xlink:href (resolution checked by GML-STR-17). |
| 100_0077 | C | na-format |  | INAS-NIAC numeric codes against the IACS-IANC dictionary are 8211 encoding artifacts (Part 10a 10a-5.2.2). |
| 100_0078 | C | na-format |  | INAS-NARC role numeric codes against ARCS-ARNC are 8211 encoding artifacts (Part 10a 10a-5.2.2); GML roles are named elements. |
| 100_0079 | C | na-format |  | INAS-NATC numeric attribute codes against ATCS-ANCD are 8211 encoding artifacts (Part 10a 10a-5.2.2). |
| 100_0080 | C | na-format |  | RUIN/IUIN insert-consistency is 8211 update mechanics (Part 10a 10a-5.2.2); not applicable to GML. |
| 100_0081 | C | na-format |  | INAS ATIX index sequencing is 8211 bookkeeping (Part 10a 10a-5.2.2); no GML counterpart. |
| 100_0082 | C | na-format |  | INAS-ATIX validity under Modify is 8211 update mechanics (Part 10a 10a-5.2.2). |
| 100_0083 | C | na-format |  | INAS-PAIX indexing is an 8211 subfield construct (Part 10a 10a-5.2.2). |
| 100_0084 | C | na-format |  | IUIN/ATIN insert-consistency is 8211 update mechanics (Part 10a 10a-5.2.2). |
| 100_0085 | E | na-format |  | DSSI-NOIR record-count field exists only in the ISO 8211 Dataset General Information record (Part 10a 10a-6.1.2.2); GML datasets carry no DSSI counts. |
| 100_0086 | E | na-format |  | DSSI-NOPN point-record count is an 8211 DSSI field (Part 10a 10a-6.1.2.2); no GML counterpart. |
| 100_0087 | E | na-format |  | DSSI-NOMN multi-point-record count is an 8211 DSSI field (Part 10a 10a-6.1.2.2); no GML counterpart. |
| 100_0088 | E | na-format |  | DSSI-NOCN curve-record count is an 8211 DSSI field (Part 10a 10a-6.1.2.2); no GML counterpart. |
| 100_0089 | E | na-format |  | DSSI-NOXN composite-curve-record count is an 8211 DSSI field (Part 10a 10a-6.1.2.2); no GML counterpart. |
| 100_0090 | E | na-format |  | DSSI-NOSN surface-record count is an 8211 DSSI field (Part 10a 10a-6.1.2.2); no GML counterpart. |
| 100_0091 | E | na-format |  | DSSI-NOFR feature-record count is an 8211 DSSI field (Part 10a 10a-6.1.2.2); no GML counterpart. |
| 100_0092 | C | na-format |  | ATCS attribute-code dictionary uniqueness is an 8211 lexical-level construct (Part 10a 10a-6.1.2.3); GML has no in-file code dictionaries. |
| 100_0093 | C | na-format |  | ATCS-ANCD numeric-code uniqueness is an 8211 dictionary construct (Part 10a 10a-6.1.2.3). |
| 100_0094 | C | na-format |  | ATCS-ATCD vs feature catalogue is a check on the 8211 in-file dictionary (Part 10a); the GML-side unknown-attribute-vs-FC concern belongs to check 100_0001, not this construct. |
| 100_0095 | C | na-format |  | ITCS information-type-code dictionary uniqueness is an 8211 construct (Part 10a 10a-6.1.2.4). |
| 100_0096 | C | na-format |  | ITCS-ITNC numeric-code uniqueness is an 8211 dictionary construct (Part 10a 10a-6.1.2.4). |
| 100_0097 | C | na-format |  | ITCS-ITCD vs feature catalogue is a check on the 8211 in-file dictionary (Part 10a 10a-6.1.2.4); no such dictionary exists in GML. |
| 100_0098 | C | na-format |  | FTCS feature-type-code dictionary uniqueness is an 8211 construct (Part 10a 10a-6.1.2.5). |
| 100_0099 | C | na-format |  | FTCS-FTNC numeric-code uniqueness is an 8211 dictionary construct (Part 10a 10a-6.1.2.5). |
| 100_0100 | C | na-format |  | FTCS-FTCD vs feature catalogue is a check on the 8211 in-file dictionary (Part 10a 10a-6.1.2.5); GML feature-type-vs-FC validity is a different construct (check 100_0001 territory). |
| 100_0101 | C | na-format |  | IACS information-association-code dictionary uniqueness is an 8211 construct (Part 10a 10a-6.1.2.6). |
| 100_0102 | C | na-format |  | IACS-IANC numeric-code uniqueness is an 8211 dictionary construct (Part 10a 10a-6.1.2.6). |
| 100_0103 | C | na-format |  | IACS-IACD vs feature catalogue is a check on the 8211 in-file dictionary (Part 10a 10a-6.1.2.6). |
| 100_0104 | C | na-format |  | FACS feature-association-code dictionary uniqueness is an 8211 construct (Part 10a 10a-6.1.2.7). |
| 100_0105 | C | na-format |  | FACS-FANC numeric-code uniqueness is an 8211 dictionary construct (Part 10a 10a-6.1.2.7). |
| 100_0106 | C | na-format |  | FACS-FACD vs feature catalogue is a check on the 8211 in-file dictionary (Part 10a 10a-6.1.2.7). |
| 100_0107 | C | na-format |  | ARCS association-role-code dictionary uniqueness is an 8211 construct (Part 10a 10a-6.1.2.8); GML roles are named elements, no code dictionary. |
| 100_0108 | C | na-format |  | ARCS-ARNC numeric-code uniqueness is an 8211 dictionary construct (Part 10a 10a-6.1.2.8). |
| 100_0109 | C | na-format |  | ARCS-ARCD is an ISO/IEC 8211 code-string subfield (Part 10a); GML S-201 has no ARCS record — the FC-validity analogue for association roles is a separate GML-side check. |
| 100_0110 | C | na-format |  | CSID-NCRC/CRSH field counting is 8211 CRS-record structure; GML carries CRS via srsName (already policed by GML-STR-21), no CSID/CRSH records exist. |
| 100_0111 | C | na-format |  | CRSH-CRIX index uniqueness is an 8211 record construct absent from the GML encoding. |
| 100_0112 | W | na-format |  | CRSH-CRSS/SCRI subfield pairing is 8211-specific; GML srsName has no 'Other Source' code/free-text pair. |
| 100_0113 | W | na-format |  | Inverse of 100_0112 on the same 8211 CRSH-CRSS/SCRI pair; no GML counterpart. |
| 100_0114 | C | na-format |  | CSAX-AXTY axis-type uniqueness within a CRSH record is 8211 CRS-record structure; GML references EPSG CRS by URI. |
| 100_0115 | W | na-format |  | VDAT-DTSR/SCRI vertical-datum source pairing is an 8211 record field; GML S-201 has no VDAT record. |
| 100_0116 | W | na-format |  | Duplicate of 100_0113 (same CRSH-CRSS=254/SCRI predicate, different clause ref); 8211-only construct. |
| 100_0117 | C | na-format |  | IRID-NITC numeric-code lookup against ITCS is the 8211 code-table mechanism; GML identifies information types by element name, checked by the FC-conformance checks elsewhere in the table. |
| 100_0118 | W | na-format |  | DSSI coordinate multiplication factors and C2FT/C3FL/DRVF binary coordinate fields exist only in the 8211 encoding; GML posList is decimal text. |
| 100_0119 | C | na-format |  | COCC coordinate-update index ranges belong to the 8211 update-record mechanism; GML S-201 datasets have no COCC fields. |
| 100_0120 | C | na-format |  | COCC-NCOR tuple-count consistency is 8211 update-record structure with no GML counterpart. |
| 100_0121 | C | na-format |  | VCID vertical-CRS index references into CRSH records are 8211-only; GML has no per-tuple vertical-CRS index. |
| 100_0122 | C | na-format |  | KNOT-KVAL monotonicity governs 8211 spline knot fields; S-201 GML geometry (Point/Curve/Surface posLists) carries no KNOT fields. |
| 100_0123 | C | na-format |  | DRVF/DRVI derivative-order fields are 8211 spline encoding constructs absent from GML. |
| 100_0124 | C | na-format |  | Coordinate-tuple dimension match between update and base records presupposes the 8211 base/update record mechanism. |
| 100_0125 | C | na-format |  | 'More than one type of coordinate list field' contrasts 8211 field types (C2IL vs C2FL etc.); GML has a single posList/pos representation. |
| 100_0126 | C | na-format |  | Mixed vertical-datum references within a Multi Point/Curve record use the 8211 VCID mechanism; no GML counterpart in S-201. |
| 100_0127 | C | na-format |  | SEGH-INTP=7 requiring CIPM/ARPM is 8211 curve-segment field structure; GML arcs are typed elements, not field sequences. |
| 100_0128 | C | na-format |  | Inverse pairing of 100_0127 on the same 8211 SEGH/CIPM/ARPM fields. |
| 100_0129 | C | na-format |  | Tuple-count rule for 8211 CircularArcCenterPointWithRadius segments; not representable in S-201 GML. |
| 100_0130 | C | na-format |  | SEGH-INTP spline values requiring a PSPL field is 8211 segment structure; S-201 GML uses no polynomial/bezier spline fields. |
| 100_0131 | C | na-format |  | Inverse PSPL pairing of 100_0130; same 8211-only construct. |
| 100_0132 | C | na-format |  | SPLI/PSPL KSPC/KNOT field pairing is 8211 spline encoding; no GML counterpart. |
| 100_0133 | C | na-format |  | SEGH-INTP=10 (bSpline) requiring SPLI is 8211 segment structure; not applicable to GML. |
| 100_0134 | C | na-format |  | Inverse SPLI pairing of 100_0133; 8211-only. |
| 100_0135 | C | na-format |  | PTAS-TOPI point-association coincidence is the 8211 topology-record mechanism; S-201 GML curves carry inline coordinates without PTAS point references. |
| 100_0136 | C | na-format |  | End-point twin of 100_0135 on the same 8211 PTAS mechanism. |
| 100_0137 | C | na-format |  | SECC segment-update index validity belongs to the 8211 update-record mechanism. |
| 100_0138 | C | na-format |  | SECC-NSEG count consistency is 8211 update-record structure. |
| 100_0139 | C | na-format |  | Multiple PTAS fields defining the beginning point is 8211 point-association structure; no GML counterpart. |
| 100_0140 | C | na-format |  | End-point twin of 100_0139; 8211 PTAS-only. |
| 100_0141 | C | na-format |  | CCOC composite-curve update index ranges are 8211 update-record mechanics. |
| 100_0142 | C | na-format |  | CCOC-NCCO component-count consistency is 8211 update-record structure. |
| 100_0143 | C | candidate |  | Part-7 continuity substance ports to GML gml:CompositeCurve: a DOM-level structural check (validateGMLStructure style, like GML-STR-21) walks each CompositeCurve's curveMember children in order (resolving xlink members via the existing _resolveXlink pattern), parses each member's posList, and flags when a component's last coord pair differs from the next component's first pair — tag GEOM; parser currently flattens curves so feat objects lack per-component data. |
| 100_0144 | C | candidate | S158-GEOM-02 | GML analogue is LinearRing closure (Part 7 / OGC GML 3.2.2, which the generator already auto-closes on emit but the validator never checks on input): predicate on feat.geometry.type==='surface' flagging coordinates[0] pair !== coordinates[last] pair (DOM sweep over all LinearRing posLists also covers interior rings) — tag GEOM, C maps to error. |
| 100_0145 | C | candidate |  | Cites Part 7 (7-4.3.2) so format-neutral: DOM-level count of gml:exterior children per Polygon/PolygonPatch, flagging patches with 0 or >1 exterior (GML schema permits zero, so this is a real gap) — tag GEOM; no existing GML-STR/GEO rule touches ring structure (grep-confirmed). |
| 100_0146 | C | candidate |  | Part-7 (7-4.3.2) topology, implementable via DOM: read each surface's interior LinearRing posLists (parser only collects the exterior ring onto feat.geometry.coordinates, ~L5659-5681) and ray-cast interior vertices against the exterior ring, flagging interiors not WITHIN it — tag GEOM. |
| 100_0147 | C | candidate |  | Part-7 (7-4.3.2) topology: pairwise segment-intersection test between each interior ring and the exterior/other interiors from the same DOM ring set as 100_0146, flagging >1 intersection point — tag GEOM; heavier geometry math but self-contained JS. |
| 100_0148 | C | candidate |  | Part-7 (7-4.3.2) topology: ray-cast each interior ring's vertices against every other interior ring of the same surface, flagging interior-within-interior nesting — tag GEOM, shares the DOM ring extraction of 100_0146/0147. |
| 100_0149 | C | na-format |  | FRID-NFTC numeric feature-type codes against FTCS are the 8211 code-table mechanism; GML identifies feature types by element name and FC-conformance is a separate GML-side check. |
| 100_0150 | C | na-format |  | FOID matching between base and update records presupposes the 8211 update mechanism; the app validates single base GML datasets. |
| 100_0151 | C | na-format |  | FASC-NFAC numeric feature-association codes are 8211 code-table constructs; GML associations use xlink:href elements (policed by GML-STR-17 for resolvability, a different concern). |
| 100_0152 | C | na-format |  | FASC-NARC numeric role codes are 8211-only; GML roles are element names. |
| 100_0153 | C | na-format |  | RUIN/FASC-FAUI insert-instruction consistency is 8211 update-record semantics. |
| 100_0154 | C | na-format |  | FASC-NATC numeric attribute codes against ATCS are the 8211 code-table mechanism. |
| 100_0155 | C | na-format |  | ATIX index sequencing within FASC insert fields is 8211 update-record structure. |
| 100_0156 | C | na-format |  | ATIX index validity for FASC modify instructions is 8211 update-record structure. |
| 100_0157 | C | na-format |  | FASC-PAIX parent-attribute indexing is an 8211 field construct with no GML counterpart. |
| 100_0158 | C | na-format |  | FAUI/ATIN insert-instruction pairing is 8211 update-record semantics. |
| 100_0159 | C | na-format |  | RUIN/THAS-TAUI insert consistency concerns 8211 thematic-association update records. |
| 100_0160 | E | na-format |  | RUIN/MASK-MUIN insert consistency concerns 8211 masking update records; GML S-201 has no MASK fields. |
| 100_0161 | E | na-format |  | MASK-MIND dataset-limit truncation references RRNM/PRID spatial record pointers, all 8211-only constructs. |
| 100_0162 | C | na-format |  | 'Delete record contains further fields' is pure 8211 update-record structure; the app validates single base GML datasets with no record-level delete instructions. |
| 100_0163 | E | candidate |  | No rule scans for the gml:StandardObjectProperties group (0 hits for metaDataProperty/description/descriptionReference in the app); predicate: DOM scan each feature element for GML-namespace children with localName in {metaDataProperty, description, descriptionReference, identifier, name} — segment STDPROP. |
| 100_0164 | C | partial |  | GML-STR-01..21 (well-formedness, namespaces, root Dataset, DII block, members wrapper, gml:id NCName/uniqueness, href resolution, SRS) plus the FC-derived S100-*/S201-* enum/multiplicity rules approximate schema conformance, but there is no full in-browser XSD validation against the S-201 application schema. |
| 100_0165 | C | candidate |  | Parser reads posList/pos and ignores segment types entirely (no 'interpolation' handling in the app); predicate: DOM scan each Curve's gml:segments children — localName must be a Part 10b-permitted segment type (e.g. LineStringSegment) and any interpolation attribute must be a permitted value — segment GEOM. |
| 100_0166 | W | candidate |  | Parser reads inline geometry only (no xlink handling in the geometry branch at _parseFeEl) and nothing flags the duplicate; predicate: DOM check each geometry property wrapper (geometry/pointProperty/curveProperty/surfaceProperty) for BOTH an xlink:href attribute and an inline child geometry element — segment GEOM. |
| 100_0167 | C | na-other |  | The S-201 Ed1.1.0 Annex B1 application schema contains zero maskReference elements, so masks cannot occur in conformant S-201 GML — irrelevant-check omission per S-158:100 §4.2. |
| 100_0168 | C | na-other |  | maskReference does not exist in the S-201 application schema (0 occurrences in the bundled Annex B1 XSD), so its xlink:role constraint cannot apply to S-201 data. |
| 100_0169 | W | na-other |  | maskReference does not exist in the S-201 application schema, so the superfluous-attribute check on mask references cannot apply to S-201 data. |
| 100_0170 | E | na-other |  | maskReference does not exist in the S-201 application schema, so the #identifier-format check on mask references cannot apply to S-201 data. |
| 100_0171 | C | candidate |  | No rule flags prohibited spatial primitives (0 hits for CircleByCenterPoint/ArcByCenterPoint in the app); predicate: DOM scan the whole document for element localNames in the prohibited set (CircleByCenterPoint, ArcByCenterPoint, GML 3.3 compact encodings) — segment GEOM. |
| 100_0172 | C | partial |  | GML-STR-17 (error) verifies every fragment-style xlink:href doc-wide resolves to a declared gml:id, but non-#-form hrefs are skipped by its regex scan, so the requirement that association hrefs USE the #identifier convention is not itself enforced. |
| 100_0173 | W | candidate |  | The app has no xlink:arcrole handling anywhere; predicate: DOM scan for xlink:arcrole attributes and test the value is a non-relative legacy extended IRI (absolute-scheme regex) — segment ASSOC. |
| 100_0174 | W | candidate |  | No handling of xlink:show/actuate/type exists; predicate: DOM scan every element carrying xlink:href for prohibited xlink:show, xlink:actuate, or xlink:type attributes — segment ASSOC. |
| 100_0175 | E | candidate |  | Parser collects xlink:title only for round-trip (f._componentTitles/_parentTitles/_assocRoleRefs.titles — explicitly informational, never validated); predicate: DOM check that every association element with xlink:href also carries xlink:title — segment ASSOC. |
| 100_0176 | C | candidate |  | No rule validates role-element name + xlink:title against FC bindings (S201-EQP-PARENT-01/02 cover only the Equipment/Topmark parent binding); predicate: for each xlink-bearing child element, localName must be an FC-permitted role for f.featureType and its title must match the FC association code — groundable in the bundled FC XML plus the existing _ASSOC_ROUNDTRIP_ROLES/_ASSOC_ROLE_UI carrier predicates, reading f._assocRoleRefs/componentRefs/parentRefs — segment ASSOC. |
| 100_0177 | C | na-other |  | The S-201 application schema defines no generic informationAssociation tag (0 occurrences in the Annex B1 XSD) — information-type links use named FC role elements (e.g. atonStatus), so the arcrole-on-informationAssociation requirement cannot apply. |
| 100_0178 | C | covered |  | GML-STR-17 (error) — confirmed predicate scans the whole comment-stripped document and flags every fragment xlink:href whose target gml:id is not declared, which is exactly the referenced-object-not-present test for S-100's dataset-internal #id convention. |
| 100_0179 | C | partial |  | GML-STR-10 (DII present), GML-STR-11 (12 mandatory Table 10b-4 fields), GML-STR-12 (no extraneous fields), GML-STR-20 (canonical order), S100-DII-01 (datasetPurpose enum) and S100-DII-04 (MD_TopicCategoryCode enum) cover presence/structure plus two field-value constraints; gap = value-format conformance of the remaining fields (e.g. datasetLanguage code, datasetReferenceDate format). |
| 100_0180 | E | covered |  | GML-STR-21 — confirmed predicate errors when geometry primitives exist and neither a feature-collection gml:Envelope srsName nor each geometry element's own srsName is present, matching the check exactly (app severity error vs S-158 E). |
| 100_0181 | C | partial |  | S100-CRS-01 flags any per-feature geometry srsName not matching EPSG:4326/CRS84 (so mixed-CRS datasets surface indirectly), but no rule directly compares all srsName occurrences for equality — envelope-vs-geometry disagreement between two 4326 spellings (URN vs HTTP) passes; a direct DOM equality check (segment CRS) would close it. |
| 100_0182 | C | candidate |  | Nothing checks ordinate counts — _parseCoordList silently drops an odd trailing number and srsDimension is emitted but never validated; predicate: DOM/text check that each gml:pos has exactly 2 tokens and each gml:posList token count is even (srsDimension=2) — segment GEOM. |
| 100_0183 | C | covered |  | S100-CRS-02 (error) — confirmed predicate requires lat ∈ [−90,90] and lon ∈ [−180,180] for point lat/lon and for every curve/surface coordinate pair, with NaN counted as out-of-range. |
| 100_0184 | E | partial |  | S100-CRS-01 (warning) flags srsName values that don't reference EPSG:4326/CRS84, but its regex accepts non-URI spellings (e.g. bare 'EPSG:4326'), so conformance to the OGC URI convention format itself is not enforced. |
| 100_0185 | C | covered |  | GML-STR-08 (error) — confirmed predicate requires root localName === 'Dataset' exactly (case-sensitive, any prefix allowed). |
| 100_0186 | E | na-format |  | Part 10c HDF5 object-uniqueness check; S-201 is a Part 10b GML product — irrelevant format per S-158:100 §4.2. |
| 100_0187 | E | na-format |  | Part 10c HDF5 named-object link check; not applicable to GML datasets. |
| 100_0188 | C | na-format |  | Part 10c HDF5 data-field range check (Table 10c-1); not applicable to GML datasets. |
| 100_0189 | C | na-format |  | Part 10c HDF5 PS-constraint range check; not applicable to GML datasets. |
| 100_0190 | C | na-format |  | Part 10c HDF5 element-naming-vs-FC check; the equivalent GML-side FC conformance is handled by the S201-* FC rules, and this HDF5-specific form is irrelevant. |
| 100_0191 | C | na-format |  | Part 10c general HDF5 file-structure check; not applicable to GML datasets. |
| 100_0192 | E | na-format |  | Part 10c HDF5 metaFeatures carrier-metadata reference check; not applicable to GML datasets. |
| 100_0193 | C | na-format |  | Part 10c irregular-grid cell-location/sequencingRule check; S-201 has no gridded coverages. |
| 100_0194 | E | na-format |  | Part 10c tileIndex component check for irregular grids; not applicable to GML vector data. |
| 100_0195 | C | na-format |  | Part 10c HDF5 'Group_nnn' data-group naming check; not applicable to GML datasets. |
| 100_0196 | E | na-format |  | Part 10c 999-data-group cap; not applicable to GML datasets. |
| 100_0197 | C | na-format |  | Part 10c root-group embedded carrier-metadata content check (Table 10c-6); not applicable to GML datasets. |
| 100_0198 | C | na-format |  | Part 10c root-group metadata datatype check; not applicable to GML datasets. |
| 100_0199 | C | na-format |  | Part 10c root-group metadata attribute-value constraint check; not applicable to GML datasets. |
| 100_0200 | C | na-format |  | Part 10c user-defined-CRS restriction for HDF5 carrier metadata; S-201 GML CRS handling is covered on the GML side (S100-CRS-01/GML-STR-21). |
| 100_0201 | C | na-format |  | Part 10c horizontal-datum restriction in HDF5 carrier metadata; not applicable to GML datasets. |
| 100_0202 | C | na-format |  | Part 10c projection-method restriction (Table 10c-24); not applicable to GML datasets. |
| 100_0203 | W | na-format |  | Part 10c superfluous-CRS-element check for EPSG-coded HDF5 CRS metadata; not applicable to GML datasets. |
| 100_0204 | C | na-format |  | Part 10c Feature Information Group (Group_F) mandatory-component check; Group_F is an HDF5 construct with no GML equivalent. |
| 100_0205 | C | na-format |  | Part 10c Group_F component-type check; not applicable to GML datasets. |
| 100_0206 | W | na-format |  | Part 10c Group_F unrecognized-metadata check; not applicable to GML datasets. |
| 100_0207 | C | na-format |  | Part 10c Group_F numeric-string validity check; not applicable to GML datasets. |
| 100_0208 | C | na-format |  | Part 10c Group_F-must-describe-all-features check; not applicable to GML datasets. |
| 100_0209 | C | na-format |  | Part 10c Group_F mandatory-attribute listing check; the GML-side FC mandatory-attribute coverage lives in the S201-* rules, and this HDF5 feature-description form is irrelevant. |
| 100_0210 | W | na-format |  | Part 10c Group_F optional-attribute listing check; not applicable to GML datasets. |
| 100_0211 | C | na-format |  | Part 10c Feature Container Group mandatory-component check (dataCodingFormat-dependent); not applicable to GML datasets. |
| 100_0212 | C | na-format |  | Part 10c Feature Container Group component-type check; not applicable to GML datasets. |
| 100_0213 | C | na-format |  | Part 10c Feature Container Group embedded-metadata content check (Table 10c-10); not applicable to GML datasets. |
| 100_0214 | C | na-format |  | Part 10c Feature Container Group metadata attribute-value check; not applicable to GML datasets. |
| 100_0215 | W | na-format |  | Part 10c feature-attribute-table id-column positivity check; not applicable to GML datasets. |
| 100_0216 | W | na-format |  | Part 10c feature-attribute-table id-referenced-by-values-record check; not applicable to GML datasets. |
| 100_0217 | W | na-format |  | Part 10c HDF5 Feature Attribute Table check; S-201 is Part 10b GML, no such structure exists. |
| 100_0218 | W | na-format |  | Part 10c HDF5 Feature Attribute Table column-content check; not applicable to GML. |
| 100_0219 | W | na-format |  | Part 10c HDF5 Feature Attribute Table simple-type restriction; not applicable to GML. |
| 100_0220 | C | na-format |  | Part 10c HDF5 Feature Instance Group component check; GML datasets have no instance groups. |
| 100_0221 | C | na-format |  | Part 10c HDF5 Feature Instance Group component-type check; not applicable to GML. |
| 100_0222 | C | na-format |  | Part 10c HDF5 instance-group carrier-metadata (Table 10c-12) check; not applicable to GML. |
| 100_0223 | E | na-format |  | Part 10c HDF5 feature-instance attribute whitelist (Table 10c-12/10c-9.7.1); not applicable to GML. |
| 100_0224 | C | na-format |  | Part 10c HDF5 instance-group bounding-box attributes (west/east/south/northBound*); GML envelopes are covered separately by GML-STR envelope rules, this HDF5 construct is not applicable. |
| 100_0225 | C | na-format |  | Part 10c HDF5 instance-group bbox east<=west/north<=south consistency; the HDF5 attribute quartet does not exist in GML. |
| 100_0226 | C | na-format |  | Part 10c HDF5 instance-bbox-within-root-bbox check; HDF5 group hierarchy does not exist in GML. |
| 100_0227 | C | na-format |  | Part 10c HDF5 gridOriginLongitude/Latitude check; S-201 GML has no coverage grids. |
| 100_0228 | C | na-format |  | Part 10c HDF5 gridSpacing positivity check; no grids in S-201 vector GML. |
| 100_0229 | C | na-format |  | Part 10c HDF5 gridSpacing-vs-bbox check; no grids in S-201 vector GML. |
| 100_0230 | C | na-format |  | Part 10c HDF5 numPoints 1x1-grid minimum check; no grids in S-201 vector GML. |
| 100_0231 | C | na-format |  | Part 10c HDF5 grid-dimensions-vs-bbox consistency; no grids in S-201 vector GML. |
| 100_0232 | C | na-format |  | Part 10c HDF5 grid-origin-vs-bbox coincidence with dataOffsetCode; no grids in S-201 vector GML. |
| 100_0233 | W | na-format |  | Part 10c HDF5 startSequence/sequencingRule.scanDirection compatibility; coverage-only construct, not applicable to GML. |
| 100_0234 | E | na-format |  | Part 10c HDF5 Tiling Information Group tile-count check; S-201 GML has no tiling group. |
| 100_0235 | E | na-format |  | Part 10c HDF5 tiling-surfaces-cover-all-features check; no tiling group in GML datasets. |
| 100_0236 | E | na-format |  | Part 10c HDF5 Tiling Information Group structure (Table 10c-13); not applicable to GML. |
| 100_0237 | C | na-format |  | Part 10c HDF5 Indexes Group structure (Table 10c-14); not applicable to GML. |
| 100_0238 | C | na-format |  | Part 10c HDF5 Positioning Group mandatory-components check; coverage-only construct, not applicable to GML. |
| 100_0239 | C | na-format |  | Part 10c HDF5 Positioning Group component-type check; not applicable to GML. |
| 100_0240 | W | na-format |  | Part 10c HDF5 Positioning Group embedded-metadata whitelist; not applicable to GML. |
| 100_0241 | C | na-format |  | Part 10c HDF5 Positioning-Group-only-for-dataCodingFormat 1/3/4/7/8 check; dataCodingFormat is an HDF5 coverage concept, not applicable to GML. |
| 100_0242 | C | na-format |  | Part 10c HDF5 Values Group mandatory-components check; no values groups in vector GML. |
| 100_0243 | C | na-format |  | Part 10c HDF5 Values Group component-type check; not applicable to GML. |
| 100_0244 | C | na-format |  | Part 10c HDF5 values-group metadata constraints (Table 10c-19); not applicable to GML. |
| 100_0245 | C | na-format |  | Part 10c HDF5 time-series group-structure check; S-201 GML carries no time-series coverages. |
| 100_0246 | C | na-format |  | Part 10c HDF5 Data Values Group sequential-naming (001,002,...) check; not applicable to GML. |
| 100_0247 | C | na-format |  | Part 10c HDF5 numGRP-vs-values-group-count check; not applicable to GML. |
| 100_0248 | W | na-format |  | Part 10c HDF5 values-group extra-attribute whitelist (Table 10c-19); not applicable to GML. |
| 100_0249 | E | na-format |  | Part 10c HDF5 timeRecordInterval>0 check; attribute exists only in HDF5 carrier metadata, not in S-201 GML. |
| 100_0250 | C | na-format |  | Part 10c HDF5 grid-cell-index-into-Feature-Attribute-Table check; not applicable to GML. |
| 100_0251 | C | na-format |  | Part 10c-13 extObjRef:<fileName>:<recordIdentifier> external-vector-reference format is an HDF5-carrier construct; S-201 GML embeds its geometry inline. |
| 100_0252 | C | partial |  | S100-CRS-01 (warning) tests every parsed f.geometry.srsName against the DPS CRS (EPSG:4326/CRS84, S-201 PS 2.0.0 sec 5.2 WGS84) and GML-STR-21 enforces SRS determinability, but neither validates the Envelope-level srsName VALUE - the parser injects an EPSG:4326 default when a geometry element lacks srsName, so a dataset whose only CRS declaration is a non-WGS84 Envelope srsName passes silently. |
| 100_0253 | C | covered |  | S-201 encodes the dataset vertical reference not as a GML vertical CRS but as the verticalDatum enum on the VerticalDatumOfData/SoundingDatum meta-features (PS 2.0.0 sec 5.3: 'shall be selected from the list in verticalDatum enumeration'), and S201-FEA-20 (verified predicate) enforces exactly that DPS constraint - presence (1..1) plus VERT_DATUM enum membership. |
| 100_0254 | C | na-other |  | S-201 PS 2.0.0 sec 5.4 fixes units by specification (metres/NM/degrees/etc.) and the GML application schema encodes plain decimals with no uom attributes (zero uom occurrences in samples/generator), so there is no in-dataset unit encoding for a predicate to test. |
| 100_0255 | W | candidate |  | S-201 PS 2.0.0 sec 11.3 (extract L1132-1133) sets a 50 MB dataset limit and no size check exists in the app - add a document-level check in validateGMLStructure: new TextEncoder().encode(txt).length > 50*1024*1024 -> info, tag SIZE. |
| 100_0256 | E | na-package |  | Part 15 protection-scheme SA root certificate check; app validates a single GML text, no exchange-set/certificate input (documented limitation). |
| 100_0257 | E | na-package |  | Part 15 IHO SA root-certificate validity-period check; certificate material is exchange-set-level, outside single-dataset scope. |
| 100_0258 | E | na-package |  | Part 15 Data-Server-certificate-issued-by-IHO check; exchange-set signing infrastructure, outside app scope. |
| 100_0259 | E | na-package |  | Part 15 Data Server certificate expiry check; exchange-set signing infrastructure, outside app scope. |
| 100_0260 | E | candidate |  | Part 15 requires signature certificates defined in CATALOG.XML; the app has no exchange-set catalogue input (documented limitation). [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0261 | C | covered |  | S158-PKG-10 — every discovery block's digitalSignatureReference must be "ECDSA-384-SHA2" (S-100 §15-8.7 normative clause), checked on Exchange-Set ZIP ingest (validateExchangeSet). |
| 100_0262 | E | na-package |  | Pt 15 §15-5.2 (s100_ed5_2_0_full.txt L43558-43565): compressionFlag=true means the NAMED RESOURCE is itself a per-file ZIP archive, not that the outer archive's entry uses DEFLATE — an outer-entry-method comparison would test the wrong thing, so no rule is implemented despite the ZIP ingest (divergence documented in the validateExchangeSet header; _zipDecode itself reads DEFLATE members per this clause). |
| 100_0263 | C | candidate |  | Part 15 PERMIT.XML/PERMIT.SIGN digital-signature check; permit files are exchange-set support files, outside app scope. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0264 | C | na-package |  | Part 15 dataset-decryption check; the app has no encrypted-dataset or permit-key input (documented limitation). |
| 100_0265 | E | na-package |  | Part 15 User Permit M-ID check; permits are protection-scheme support files, outside single-dataset scope. |
| 100_0266 | E | candidate |  | Part 15 unique-signature-ID check operates on exchange-set signature definitions, not on the dataset GML. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0267 | E | candidate |  | Part 15-8.10 MRN-reference hash/signature resolution is an exchange-set/protection-scheme mechanism, outside app scope. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0268 | C | covered |  | S158-PKG-01 (CATALOG.XML presence) + S158-PKG-02 (CATALOG.SIGN presence) on ZIP ingest, per Pt 17 §17-4.2 rule 1. |
| 100_0269 | C | covered |  | S158-PKG-03 — all content rooted in S100_ROOT with the catalogue pair directly in it (ENC_ROOT/INFO S-57 co-existence siblings tolerated per Pt 17 §17-4.2). |
| 100_0270 | C | partial |  | S158-PKG-04 covers the folder-existence arm (a subfolder per product named by the catalogue's fileName paths); verifying the folder NAME against the live IHO GI Registry is not possible offline. |
| 100_0271 | C | covered |  | S158-PKG-05 — every product-subfolder file under DATASET_FILES / SUPPORT_FILES / CATALOGUES (the "as required" conditionality honoured: no empty folder demanded; deeper producer subfolders permitted per rule 5). |
| 100_0272 | W | covered |  | S158-PKG-06 — MD_*.XML located in a SUPPORT_FILES folder (info severity per the W letter). |
| 100_0273 | W | covered |  | S158-PKG-07 — every MD_*.XML name matches MD_<data file base name>.XML for a dataset in the set (info severity per the W letter). |
| 100_0274 | C | covered |  | S158-PKG-08 — exactly one CATALOG.XML, at S100_ROOT/CATALOG.XML (also enforces the S-201 PS §11.9 "No other file… may be named CATALOG.XML" addition). |
| 100_0275 | C | candidate |  | Digital signature presence for all exchange-set files — no package or signature input path exists. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0276 | E | covered |  | S158-PKG-11 — every discovery block carries at least one digitalSignatureValue (presence check; verification is the 100_0277 PKI territory that stays out of scope). |
| 100_0277 | E | na-package |  | Signature validation requires the Part 15 signature material from the exchange set — not available in dataset-only input. |
| 100_0278 | E | covered |  | S158-PKG-16 — support dataType in the 10-value S100_SupportFileFormat enumeration (XSD L801-817), with "other" additionally prohibited per S-201 PS §11.6. |
| 100_0279 | E | partial |  | S158-PKG-13 covers the in-set arm (every member declared by a discovery block); the previously-issued-dataset and shared-resource exemptions need producer history the archive does not carry. |
| 100_0280 | E | partial |  | S158-PKG-05's placement enforcement covers the physical-location arm (support files under the product's SUPPORT_FILES); the cancelled-resource and shared-system-resource exemptions are not evaluable offline. |
| 100_0281 | E | covered |  | S158-PKG-12 — every declared file present at its fileName path resolved from S100_ROOT (shared rule with 100_0301). |
| 100_0282 | E | na-other |  | S-201 FC external-resource references (fileReference/fileLocator/pictorialRepresentation, FC L7764/7787) are text-typed filenames, not URI primitives — the only URI-typed attribute (AtoNNumber, an MRN identifier) is not an external-resource reference, so the check's construct does not occur in S-201 dataset content. |
| 100_0283 | E | covered |  | S158-PKG-14 — base dataset filenames unique across the discovery metadata. |
| 100_0284 | E | covered |  | S158-PKG-15 — the actual DATASET_FILES entry names (not the DII proxy this row once proposed) validated against the S-201 §11.4 pattern 201CCCCXXXXXXXX_EEE.GML; shape-only (the EEE↔editionNumber cross-check is ungroundable — §11.4 L1154 vs §8.1 L874-875 contradiction documented in the validateExchangeSet header). |
| 100_0285 | E | na-package |  | Non-reuse of the variable name component requires producer-wide dataset history, not a single dataset. |
| 100_0286 | E | candidate |  | Cross-product-specification support-file sharing is an exchange-set fileLocation check. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0287 | C | na-package |  | Update-number sequencing needs the predecessor dataset/metadata series; only the current dsUpdateNumber is parsed. |
| 100_0288 | C | na-package |  | Re-issue edition/update alignment requires the prior issue's metadata from the exchange-set series. |
| 100_0289 | E | na-package |  | Issue-date ordering vs the previous issue requires the predecessor dataset's discovery metadata. |
| 100_0290 | E | na-package |  | Unsatisfiable as written: purpose=cancellation with editionNumber=0 cannot be encoded in a schema-valid catalogue (editionNumber is xs:positiveInteger, XSD L660), and the S-201 PS §11.5 never establishes the file-based-cancellation precondition — documented in the validateExchangeSet header; no rule (Rule 8). |
| 100_0291 | E | na-package |  | File-less cancellation metadata identity is a discovery-metadata vs cancelled-dataset comparison across the package. |
| 100_0292 | E | na-package |  | Issue-date ordering against a cancelled dataset with a reused name requires the cancelled dataset's metadata. |
| 100_0293 | E | na-package |  | Base+update sequential ordering is inherently a multi-file exchange-set check. |
| 100_0294 | E | candidate |  | The Part 17 §17-4.5 bounding polygon (Level 3a conformance) is in discovery metadata, which the app never ingests. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0295 | E | candidate |  | CI_Individual population rules apply to exchange-catalogue contact metadata; the app only emits CI blocks in generated CATALOG.XML, never validates them. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0296 | E | candidate |  | CI_Organisation name/positionName rule is exchange-catalogue metadata (producingAgency/pointOfContact) — no catalogue input. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0297 | E | candidate |  | CI_Organisation partyIdentifier fallback rule — same exchange-catalogue metadata scope, not present in dataset text. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0298 | E | candidate |  | CI contact-information completeness targets catalogue CI blocks the validator never sees. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0299 | C | candidate |  | Producer+product membership requires the external IHO S-62 register (not bundled — checking would violate Rule 8) and the producingAgency element in catalogue metadata; S201-DII-03 only format-checks the 4-char CCCC code. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0300 | C | partial |  | S158-PKG-09 — well-formedness + S100_ExchangeCatalogue root + the XSD's mandatory-element lists (DDM L590-L715, SFD L458-L513) as an element-presence profile; full XSD validation stays out of reach in-browser (same limitation as the dataset side, HANDOFF §13). |
| 100_0301 | C | covered |  | S158-PKG-12 — declared support files with revisionStatus new/replacement present at the declared path (deletion-status entries exempt per the check text). |
| 100_0302 | C | candidate |  | The dataset side (f.informationFileReference) is parsed, but confirming the referenced file's presence requires the exchange-set contents. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0303 | C | covered |  | S158-PKG-15 — dataset filenames validated against the S-201 PS §11.4 convention (the Data Product Specification this Critical check defers to). |
| 100_0304 | C | na-package |  | Support-file naming per the PS is an exchange-set file check; no support-file input. |
| 100_0305 | E | candidate |  | defaultLocale/otherLocale language codes are exchange-catalogue (§17-4.7) elements, distinct from the parsed dataset DII datasetLanguage. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0306 | E | candidate |  | PT_Locale id uniqueness is scoped to the S100_ExchangeCatalogue document. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0307 | E | candidate |  | userDefinedMaintenanceFrequency duration decimal form is exchange-catalogue §17-4.9 metadata. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0308 | E | candidate |  | Maintenance-frequency reduced-precision rule — same catalogue-metadata scope, never parsed by the app. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0309 | E | candidate |  | Duration 'T' designator rule applies to the catalogue's maintenance-frequency element. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0310 | E | candidate |  | Duration 'P' designator rule — same catalogue maintenance-frequency element. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0311 | E | candidate |  | Zero/negative duration prohibition — same catalogue maintenance-frequency element. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0312 | E | candidate |  | Comparing maintenance-frequency instants to issue date/time precision needs the catalogue metadata block. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0313 | E | candidate |  | protectionScheme=S100p15 is discovery metadata tied to package encryption, neither of which the app handles. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0314 | E | covered |  | S158-PKG-17 — discovery-metadata boundingBox vs the dataset's own gml:boundedBy envelope, lat/lon axis order, 1e-5° tolerance. |
| 100_0315 | E | candidate |  | Temporal-extent match between discovery metadata and dataset requires the catalogue side. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0316 | E | candidate |  | timeInstantBegin<timeInstantEnd applies to the S100_TemporalExtent attributes of the discovery metadata block (§17-4.5), not to dataset content. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0317 | E | candidate |  | Issue date/time match between discovery metadata and dataset requires the catalogue side (dataset dsIssueTime alone cannot be compared). [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0318 | E | candidate |  | Data-coverage polygon single-Polygon/ring restriction is on the discovery-metadata polygon in CATALOG.XML. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0319 | E | candidate |  | EPSG-4326-via-OGC-http-URI rule targets the discovery-metadata coverage polygon SRS, not the dataset srsName (dataset CRS is separately covered by S100-CRS-01). [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0320 | E | candidate |  | Exterior-ring >=4 closed positions rule applies to the discovery-metadata coverage polygon. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0321 | E | candidate |  | Interior-ring >=4 closed positions rule — same discovery-metadata polygon scope. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0322 | E | candidate |  | GML identifier on the discovery-metadata coverage polygon — catalogue scope, not dataset. [Re-classified pass 637: the Exchange-Set ZIP ingest (validateExchangeSet ctx) now provides the package input — implementable as a future S158-PKG rule; backlog.] |
| 100_0323 | C | na-format |  | approximateGridResolution vs gridSpacing applies to HDF5 gridded-coverage products; S-201 is vector GML with no coverage features (also catalogue-level). |
| 100_0324 | C | partial |  | S158-PKG-18 (info) compares catalogue issueDate against the dataset's S100:datasetReferenceDate — the only date-bearing DII equivalent; other equivalent-field pairs (title, language) remain candidates. |
