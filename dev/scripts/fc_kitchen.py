"""Fixtures for the browser gate's mount oracle (run-browser-smoke-gate.py): GML documents whose import candidate must
emit exactly what the Builder emits after it has opened every feature.

kitchen(mode) builds one member per concrete type of the S-201 Feature Catalogue 2.0.0
(dev/spec-sources/201_Feature_Catalogue_2.0.0.xml, read as fc_bindings.py reads it), carrying every attribute its
binding chain binds — supertypes included, complex attributes with every sub-attribute, a value of the attribute's
valueType, a multi-valued enumeration with two values in reverse FC order. The modes write the values in forms a
Builder control cannot always hold:

    plain  ordinary values
    lex    a line break in text, a signed real and integer ("+1.50", "+02"), an impossible date ("2020-13-01")
    lex2   padded text, a trailing-dot real ("5."), a zero-padded integer ("007"), an unpadded date ("2020-1-2")
    lex3   a leading-dot real (".5"), an exponent integer ("1e3"), markup characters in text
    nil    every top-level attribute nilled (nilReason="unknown")

EDGE_FIXTURES are hand-written cases for the same invariant: numbers and dates a control cannot show, line breaks,
carriage returns in one-line and multi-line fields and in the dataset abstract, a YYYYMMDD date in a date field, a
line's own srsName, a nilReason that is not a valid one, repeated values, the legacy inline forms (a light, a topmark,
a racon, a fog signal, a rhythm on a beacon, a legacy <component> link), and colour-less lights whose rhythm holds only
signal groups or signal-sequence rows; and the edge cases again with a producer's prefixes (S-201 as ns4:, GML as ns1:,
S-100 as ns2:). Names are fictional; positions are synthetic.

fixtures(dii=True) gives the same documents with a complete dataset identification block (_dii: every mandatory
field DataSetIdentificationType declares, s100gmlbase.xsd L208-280, with fictional values — the optional
datasetAbstract only where a fixture passes one) for the browser gate's XSD leg:
the generator writes only the fields a file has beyond the three fixed ones, so a fixture without the block yields GML
the S-201 2.0.0 schema rejects at the identification block alone. The mount oracle keeps fixtures(), whose documents
carry no block, so the path that leaves the missing fields missing stays covered.
"""
import os
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FC_XML = os.path.normpath(os.path.join(HERE, "..", "spec-sources", "201_Feature_Catalogue_2.0.0.xml"))
NS = {"f": "http://www.iho.int/S100FC/5.0", "b": "http://www.iho.int/S100Base/5.0"}
MODES = ("plain", "lex", "lex2", "lex3", "nil")


def _load(fc_path=FC_XML):
    root = ET.parse(fc_path).getroot()
    F = "{%s}" % NS["f"]
    simple, complex_, types = {}, {}, {}
    for a in root.iter(F + "S100_FC_SimpleAttribute"):
        code = a.find("f:code", NS).text.strip()
        vt = a.find("f:valueType", NS).text.strip()
        lv = {}
        for v in a.findall("f:listedValues/f:listedValue", NS):
            lv[v.find("f:code", NS).text.strip()] = v.find("f:label", NS).text.strip()
        simple[code] = (vt, lv)

    def bindings(el, tag):
        out = []
        for b in el.findall("f:" + tag, NS):
            up = b.find("f:multiplicity/b:upper", NS)
            upper = None if (up is not None and up.get("infinite") == "true") else (int(up.text) if up is not None and up.text else 1)
            pv = [v.text.strip() for v in b.findall("f:permittedValues/f:value", NS)]
            out.append((b.find("f:attribute", NS).get("ref"), upper, pv))
        return out

    for a in root.iter(F + "S100_FC_ComplexAttribute"):
        complex_[a.find("f:code", NS).text.strip()] = bindings(a, "subAttributeBinding")
    for tag in ("S100_FC_FeatureType", "S100_FC_InformationType"):
        for t in root.iter(F + tag):
            code = t.find("f:code", NS).text.strip()
            sup = t.find("f:superType", NS)
            types[code] = {"abstract": t.get("isAbstract") == "true", "super": sup.text.strip() if sup is not None and sup.text else None,
                           "binds": bindings(t, "attributeBinding"), "prims": [p.text.strip() for p in t.findall("f:permittedPrimitives", NS)]}
    return simple, complex_, types


def kitchen(mode="plain", fc_path=FC_XML, dii=False):
    assert mode in MODES, mode
    simple, complex_, types = _load(fc_path)

    def chain(code):
        out, c, seen = [], code, set()
        while c and c not in seen:
            seen.add(c)
            out = types[c]["binds"] + out
            c = types[c]["super"]
        return out

    def prims(code):
        c = code
        while c:
            if types[c]["prims"]:
                return types[c]["prims"]
            c = types[c]["super"]
        return ["point"]

    def val(ref, pv):
        vt, lv = simple[ref]
        if mode == "lex":
            if vt == "text":
                return ["Alfa\nBravo " + ref]
            if vt == "real":
                return ["+1.50"]
            if vt == "integer":
                return ["+02"]
            if vt in ("date", "S100_TruncatedDate"):
                return ["2020-13-01"]
        if mode == "lex2":
            if vt == "text":
                return ["  Alfa  Bravo " + ref + "  "]
            if vt == "real":
                return ["5."]
            if vt == "integer":
                return ["007"]
            if vt in ("date", "S100_TruncatedDate"):
                return ["2020-1-2"]
        if mode == "lex3":
            if vt == "real":
                return [".5"]
            if vt == "integer":
                return ["1e3"]
            if vt == "text":
                return ["Alfa & <Bravo> " + ref]
        if vt in ("enumeration", "S100_CodeList"):
            return [lv.get(c, c) for c in (pv or list(lv.keys()))]
        return {"text": ["Alfa " + ref], "real": ["1.5"], "integer": ["2"], "boolean": ["true"], "date": ["2020-01-02"],
                "S100_TruncatedDate": ["2020-01-02"], "URI": ["http://example.invalid/alfa"]}.get(vt, ["Alfa"])

    def emit(ref, upper, pv, ind):
        if mode == "nil" and len(ind) == 2:
            return '%s<%s nilReason="unknown"/>\n' % (ind, ref)
        if ref in complex_:
            inner = "".join(emit(r, u, p, ind + "  ") for (r, u, p) in complex_[ref])
            return "%s<%s>\n%s%s</%s>\n" % (ind, ref, inner, ind, ref)
        vals = val(ref, pv)
        if simple[ref][0] in ("enumeration", "S100_CodeList"):
            vals = [vals[1], vals[0]] if (upper is None or upper > 1) and len(vals) >= 2 else vals[:1]
        return "".join("%s<%s>%s</%s>\n" % (ind, ref, escape(v), ref) for v in vals)

    def geom(code, gid, k):
        p = prims(code)[0]
        lat = 1.0 + k * 0.001
        if p == "noGeometry":
            return ""
        srs = 'srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"'
        if p == "point":
            return '<geometry><S100:pointProperty><S100:Point gml:id="P.%s" %s><gml:pos>%.7f 2.0000000</gml:pos></S100:Point></S100:pointProperty></geometry>\n' % (gid, srs, lat)
        if p == "curve":
            return ('<geometry><S100:curveProperty><S100:Curve gml:id="C.%s" %s><gml:segments><gml:LineStringSegment><gml:posList>%.7f 2.0000000 %.7f 2.1000000</gml:posList>'
                    '</gml:LineStringSegment></gml:segments></S100:Curve></S100:curveProperty></geometry>\n') % (gid, srs, lat, lat + 0.0005)
        return ('<geometry><S100:surfaceProperty><S100:Surface gml:id="S.%s" %s><gml:patches><gml:PolygonPatch><gml:exterior><gml:LinearRing><gml:posList>'
                '%.7f 2.0000000 %.7f 2.1000000 %.7f 2.1000000 %.7f 2.0000000</gml:posList></gml:LinearRing></gml:exterior></gml:PolygonPatch></gml:patches></S100:Surface></S100:surfaceProperty></geometry>\n') % (gid, srs, lat, lat, lat + 0.0005, lat)

    members = []
    for k, code in enumerate(sorted(c for c, t in types.items() if not t["abstract"])):
        gid = "FK.%03d" % (k + 1)
        body = "".join(emit(r, u, p, "  ") for (r, u, p) in chain(code))
        members.append('<%s gml:id="%s">\n%s%s</%s>\n' % (code, gid, body, geom(code, gid, k), code))
    return _doc("DS.FK", "".join(members), _dii() if dii else "")


def _dii(abstract=None):
    """A complete dataset identification block in the order DataSetIdentificationType declares it (s100gmlbase.xsd
    L208-280): the two fixed encoding values, the product S-201 2.0.0, and fictional values for the rest; `abstract`
    (already escaped) is written as datasetAbstract, the one optional field."""
    f = [("encodingSpecification", "S-100 Part 10b"), ("encodingSpecificationEdition", "1.0"), ("productIdentifier", "S-201"),
         ("productEdition", "2.0.0"), ("applicationProfile", "1"), ("datasetFileIdentifier", "XX00FIXTURE.gml"),
         ("datasetTitle", "Fixture dataset Alfa"), ("datasetReferenceDate", "2020-01-02"), ("datasetLanguage", "eng")]
    if abstract is not None:
        f.append(("datasetAbstract", abstract))
    f += [("datasetTopicCategory", "oceans"), ("datasetPurpose", "base"), ("updateNumber", "0")]
    return ("<S100:DatasetIdentificationInformation>" + "".join("<S100:%s>%s</S100:%s>" % (k, v, k) for k, v in f)
            + "</S100:DatasetIdentificationInformation>\n")


def _doc(dsid, members, head=""):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<Dataset xmlns="http://www.iho.int/S-201/gml/cs0/1.0" xmlns:gml="http://www.opengis.net/gml/3.2" '
            'xmlns:S100="http://www.iho.int/s100gml/5.0" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="%s">\n%s<members>\n%s</members>\n</Dataset>\n') % (dsid, head, members)


def _pt(gid, lat, lon=2.0):
    return ('<geometry><S100:pointProperty><S100:Point gml:id="P.%s" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">'
            '<gml:pos>%.7f %.7f</gml:pos></S100:Point></S100:pointProperty></geometry>') % (gid, lat, lon)


def _edge(dii=False):
    m = []
    m.append('<LateralBuoy gml:id="ED.1"><colour>Red</colour><buoyShape>Can</buoyShape><categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark><height>1,5</height><verticalLength>.6</verticalLength>%s</LateralBuoy>\n' % _pt("ED.1", 1.01))
    m.append('<LateralBuoy gml:id="ED.2"><colour>Green</colour><buoyShape>Conical</buoyShape><categoryOfLateralMark>Starboard-Hand Lateral Mark</categoryOfLateralMark><height>+2.5</height><installationDate>2020-13-01</installationDate><sourceDate>2020-02-30</sourceDate>%s</LateralBuoy>\n' % _pt("ED.2", 1.02))
    m.append('<QualityOfNonBathymetricData gml:id="ED.3"><categoryOfTemporalVariation>Unassessed</categoryOfTemporalVariation><horizontalPositionUncertainty><uncertaintyFixed>+2.5</uncertaintyFixed></horizontalPositionUncertainty>'
             '<geometry><S100:surfaceProperty><S100:Surface gml:id="S.ED.3" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:patches><gml:PolygonPatch><gml:exterior><gml:LinearRing><gml:posList>1.0 2.0 1.0 2.1 1.1 2.1 1.0 2.0</gml:posList></gml:LinearRing></gml:exterior></gml:PolygonPatch></gml:patches></S100:Surface></S100:surfaceProperty></geometry></QualityOfNonBathymetricData>\n')
    m.append('<Pile gml:id="ED.5"><featureName><name>Alfa\nBravo</name></featureName><AtoNNumber>0005</AtoNNumber><height>2.50</height><inspectionRequirements>first line\nsecond line</inspectionRequirements>%s</Pile>\n' % _pt("ED.5", 1.05))
    m.append('<CardinalBuoy gml:id="ED.6"><colour>Black</colour><colour>Yellow</colour><colourPattern>Horizontal Stripes</colourPattern><buoyShape>Pillar</buoyShape><categoryOfCardinalMark>North Cardinal Mark</categoryOfCardinalMark><status>Temporary</status><status>Permanent</status><height>1e1</height>%s</CardinalBuoy>\n' % _pt("ED.6", 1.06))
    m.append('<Daymark gml:id="ED.7"><colour>Red</colour><colour>White</colour><colour>Red</colour><topmarkDaymarkShape>Board</topmarkDaymarkShape>%s</Daymark>\n' % _pt("ED.7", 1.07))
    m.append('<Pile gml:id="ED.8"><information><language>eng</language><text>one&#13;two</text></information><information><language>eng</language><text>three&#13;\nfour</text></information>%s</Pile>\n' % _pt("ED.8", 1.08))
    m.append('<NavigationLine gml:id="ED.9"><categoryOfNavigationLine>Clearing Line</categoryOfNavigationLine><geometry><S100:curveProperty><S100:Curve gml:id="C.ED.9" srsName="urn:ogc:def:crs:EPSG::4326" srsDimension="2">'
             '<gml:segments><gml:LineStringSegment><gml:posList>1.0900000 2.0000000 1.0910000 2.1000000</gml:posList></gml:LineStringSegment></gml:segments></S100:Curve></S100:curveProperty></geometry></NavigationLine>\n')
    m.append('<Pile gml:id="ED.10"><height nilReason="not known"/>%s</Pile>\n' % _pt("ED.10", 1.10))
    m.append('<Pile gml:id="ED.11"><featureName><name>Charlie&#13;Delta</name></featureName><installationDate>20200102</installationDate>%s</Pile>\n' % _pt("ED.11", 1.11))
    # links as a producer writes them: role, arcrole and title on each, a same-document and a cross-dataset member, a child
    # link to a URN, a nilled association role, a positioningMethod link beside the complex it names
    XLA = ' xlink:role="urn:x-fixture:%s" xlink:arcrole="urn:x-fixture:arc:%s" xlink:title="%s"'
    m.append('<NavigationLine gml:id="ED.12"><categoryOfNavigationLine>Clearing Line</categoryOfNavigationLine><navigableTrack xlink:href="#ED.13"%s/>'
             '<geometry><S100:curveProperty><S100:Curve gml:id="C.ED.12" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:segments><gml:LineStringSegment><gml:posList>1.12 2.0 1.13 2.1</gml:posList></gml:LineStringSegment></gml:segments></S100:Curve></S100:curveProperty></geometry></NavigationLine>\n'
             % (XLA % ("navigableTrack", "navigableTrack", "Echo track")))
    m.append('<RecommendedTrack gml:id="ED.13"><navigationLine xlink:href="#ED.12"%s/><trafficFlow>Inbound</trafficFlow>'
             '<geometry><S100:curveProperty><S100:Curve gml:id="C.ED.13" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:segments><gml:LineStringSegment><gml:posList>1.12 2.0 1.13 2.1</gml:posList></gml:LineStringSegment></gml:segments></S100:Curve></S100:curveProperty></geometry></RecommendedTrack>\n'
             % (XLA % ("navigationLine", "navigationLine", "Foxtrot line")))
    m.append('<AtonAggregation gml:id="ED.14"><categoryOfAggregation>Leading Line</categoryOfAggregation><atonAggregationBy xlink:href="#ED.5"%s/><atonAggregationBy xlink:href="other-dataset.gml#XX.9" xlink:title="Golf"/></AtonAggregation>\n'
             % (XLA % ("atonAggregationBy", "atonAggregationBy", "Hotel")))
    m.append('<Pile gml:id="ED.15"><peerAtonAggregation xlink:href="#ED.14"%s/><Statuspart nilReason="unknown"/><fixingMethod nilReason="withheld"/><positioningMethod xlink:href="#ED.16" xlink:title="India"/><child xlink:href="urn:x-fixture:child:1" xlink:title="Kilo"/>%s</Pile>\n'
             % (XLA % ("peerAtonAggregation", "peerAtonAggregation", "Juliett"), _pt("ED.15", 1.15)))
    m.append('<PositioningInformation gml:id="ED.16"><positioningMethod><positioningEquipment>GPS Receiver</positioningEquipment></positioningMethod></PositioningInformation>\n')
    # components folded on import that carry links, void values and a position of their own: a RadioStation with a
    # role/arcrole parent link, a titled Statuspart, a physical AIS link and a nilled category; a light at its own point
    # with a parent link that does not resolve; a light two buoys claim (a feature of its own); an inline <topmark>
    # holding a Statuspart
    m.append('<LateralBuoy gml:id="ED.17"><child xlink:href="#ED.18"/><child xlink:href="#ED.20"/><child xlink:href="#ED.21"/>'
             '<colour>Red</colour><buoyShape>Can</buoyShape><categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark>%s</LateralBuoy>\n' % _pt("ED.17", 1.17))
    m.append('<RadioStation gml:id="ED.18"><parent xlink:href="#ED.17" xlink:role="urn:x-fixture:parent" xlink:arcrole="urn:x-fixture:arc:parent"/>'
             '<Statuspart xlink:href="#ED.3" xlink:title="Lima"/><physicalAISbroadcastBy xlink:href="#ED.19"/><categoryOfRadioStation nilReason="unknown"/>%s</RadioStation>\n' % _pt("ED.18", 1.17))
    m.append('<PhysicalAISAidToNavigation gml:id="ED.19"><physicalAISbroadcasts xlink:href="#ED.18"/><mMSICode>992356001</mMSICode>%s</PhysicalAISAidToNavigation>\n' % _pt("ED.19", 1.19))
    m.append('<LightAllAround gml:id="ED.20"><parent xlink:href="#ED.17"/><parent xlink:href="#ZZ.9"/><Statuspart nilReason="unknown"/><colour>White</colour>'
             '<rhythmOfLight><lightCharacteristic>Flashing</lightCharacteristic><signalPeriod>5</signalPeriod></rhythmOfLight>%s</LightAllAround>\n' % _pt("ED.20", 1.18, 2.1))
    m.append('<LightAllAround gml:id="ED.21"><parent xlink:href="#ED.17"/><parent xlink:href="#ED.22"/><colour>Green</colour>%s</LightAllAround>\n' % _pt("ED.21", 1.17))
    m.append('<LateralBuoy gml:id="ED.22"><child xlink:href="#ED.21"/><colour>Green</colour><buoyShape>Conical</buoyShape><categoryOfLateralMark>Starboard-Hand Lateral Mark</categoryOfLateralMark>'
             '<topmark><colour>Green</colour><topmarkDaymarkShape>Cone, point up</topmarkDaymarkShape><Statuspart xlink:href="#ED.3"/></topmark>%s</LateralBuoy>\n' % _pt("ED.22", 1.22))
    head = ('<gml:boundedBy><gml:Envelope srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:lowerCorner>1.000000000 2.000000000</gml:lowerCorner>'
            '<gml:upperCorner>1.123456789 2.987654321</gml:upperCorner></gml:Envelope></gml:boundedBy>\n'
            + (_dii("abs one&#13;abs two") if dii else
               '<S100:DatasetIdentificationInformation><S100:datasetAbstract>abs one&#13;abs two</S100:datasetAbstract></S100:DatasetIdentificationInformation>\n'))
    return _doc("DS.ED", "".join(m), head)


def _legacy(dii=False):
    m = []
    m.append('<LateralBuoy gml:id="LG.1"><colour>Red</colour><buoyShape>Can</buoyShape><categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark><light><lightCharacter>Fl</lightCharacter><colour>Red</colour><signalPeriod>4</signalPeriod></light>%s</LateralBuoy>\n' % _pt("LG.1", 1.01))
    m.append('<LateralBuoy gml:id="LG.2"><colour>Green</colour><buoyShape>Conical</buoyShape><categoryOfLateralMark>Starboard-Hand Lateral Mark</categoryOfLateralMark><topmark><topmarkShape>Cone (Point Up)</topmarkShape><colour>Green</colour><colourPattern>Horizontal Stripes</colourPattern><status>Occasional</status><status>Temporary</status><verticalLength>0.8</verticalLength><iDCode>XX-TM-2</iDCode><fixedDateRange><dateStart>20250101</dateStart></fixedDateRange></topmark>%s</LateralBuoy>\n' % _pt("LG.2", 1.02))
    m.append('<CardinalBuoy gml:id="LG.3"><colour>Black</colour><colour>Yellow</colour><colourPattern>Horizontal Stripes</colourPattern><buoyShape>Pillar</buoyShape><categoryOfCardinalMark>North Cardinal Mark</categoryOfCardinalMark>'
             '<radarTransponderBeacon><raconCode>K</raconCode><categoryOfRadarTransponderBeacon>Racon, Radar Transponder Beacon</categoryOfRadarTransponderBeacon><status>Occasional</status><valueOfNominalRange>12</valueOfNominalRange><iDCode>XX-RT-3</iDCode></radarTransponderBeacon><fogSignal><categoryOfFogSignal>Horn</categoryOfFogSignal><signalPeriod>30</signalPeriod><status>Occasional</status></fogSignal>%s</CardinalBuoy>\n' % _pt("LG.3", 1.03))
    m.append('<LateralBeacon gml:id="LG.4"><colour>Red</colour><beaconShape>Pile Beacon</beaconShape><categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark><rhythmOfLight><lightCharacteristic>Flashing</lightCharacteristic><signalGroup>(2)</signalGroup></rhythmOfLight><signalPeriod>6</signalPeriod>%s</LateralBeacon>\n' % _pt("LG.4", 1.04))
    m.append('<SafeWaterBuoy gml:id="LG.5"><colour>Red</colour><colour>White</colour><colourPattern>Vertical Stripes</colourPattern><buoyShape>Spherical</buoyShape><component xlink:href="#LG.6"/>%s</SafeWaterBuoy>\n' % _pt("LG.5", 1.05))
    m.append('<Topmark gml:id="LG.6"><parent xlink:href="#LG.5"/><colour>Red</colour><topmarkDaymarkShape>Sphere</topmarkDaymarkShape>%s</Topmark>\n' % _pt("LG.6", 1.05))
    # values nested in another element: a light sector's visibility and range, an ObscuredSector, a sinker's
    # dimensions, a beacon's own sector limits, a Topmark linked by buoyPart
    sec = '<lightSector><colour>%s</colour><sectorLimit><sectorLimitOne><sectorBearing>%d</sectorBearing></sectorLimitOne><sectorLimitTwo><sectorBearing>%d</sectorBearing></sectorLimitTwo></sectorLimit>%s</lightSector>'
    obs = '<ObscuredSector><sectorLimit><sectorLimitOne><sectorBearing>100</sectorBearing></sectorLimitOne><sectorLimitTwo><sectorBearing>200</sectorBearing></sectorLimitTwo></sectorLimit></ObscuredSector>'
    m.append('<LightSectored gml:id="LG.7"><colour>White</colour><sectorCharacteristics><lightCharacteristic>Flashing</lightCharacteristic><signalPeriod>5</signalPeriod>%s%s</sectorCharacteristics>%s%s</LightSectored>\n'
             % (sec % ("Red", 10, 20, "<valueOfNominalRange>7.5</valueOfNominalRange><lightVisibility>Faint</lightVisibility>"), sec % ("Green", 20, 30, ""), obs, _pt("LG.7", 1.07)))
    m.append('<LightSectored gml:id="LG.8"><colour>White</colour>%s%s</LightSectored>\n' % (obs, _pt("LG.8", 1.08)))
    m.append('<SinkerAnchor gml:id="LG.9"><sinkerDimensions><heightLengthUnits>Metres</heightLengthUnits><verticalLength>3.25</verticalLength></sinkerDimensions>%s</SinkerAnchor>\n' % _pt("LG.9", 1.09))
    m.append('<RadarTransponderBeacon gml:id="LG.10"><categoryOfRadarTransponderBeacon>Racon, Radar Transponder Beacon</categoryOfRadarTransponderBeacon><sectorLimitOne><sectorBearing>30</sectorBearing><sectorLineLength>2</sectorLineLength></sectorLimitOne><sectorLimitTwo><sectorBearing>60</sectorBearing></sectorLimitTwo>%s</RadarTransponderBeacon>\n' % _pt("LG.10", 1.10))
    m.append('<Topmark gml:id="LG.11"><buoyPart xlink:href="#LG.1"/><colour>Red</colour><topmarkDaymarkShape>Cylinder</topmarkDaymarkShape>%s</Topmark>\n' % _pt("LG.11", 1.01))
    return _doc("DS.LG", "".join(m), _dii() if dii else "")


def _rhythm(dii=False):
    """Colour-less lights whose rhythm holds only signal groups, only complete signal-sequence rows, both, or a half row."""
    seq = "<signalSequence><signalDuration>0.5</signalDuration><signalStatus>Lit</signalStatus></signalSequence><signalSequence><signalDuration>1.5</signalDuration><signalStatus>Eclipsed</signalStatus></signalSequence>"
    bodies = {"G": "<signalGroup>(2)</signalGroup><signalGroup>(3)</signalGroup>", "S": seq, "GS": "<signalGroup>(2)</signalGroup>" + seq,
              "H": "<signalGroup>(2)</signalGroup><signalSequence><signalDuration>0.5</signalDuration></signalSequence>"}
    m, k = [], 0
    for ft in ("LightAllAround", "LightAirObstruction", "LightFogDetector"):
        for key, body in bodies.items():
            k += 1
            gid = "RH.%02d" % k
            m.append('<%s gml:id="%s"><rhythmOfLight>%s</rhythmOfLight>%s</%s>\n' % (ft, gid, body, _pt(gid, 1.0 + k * 0.001), ft))
    return _doc("DS.RH", "".join(m), _dii() if dii else "")


def _prefixed(text):
    """The same dataset with the S-201 namespace bound to ns4:, GML to ns1: and S-100 to ns2: (a producer's prefixes)."""
    import re
    t = text.replace('xmlns="http://www.iho.int/S-201/gml/cs0/1.0"', 'xmlns:ns4="http://www.iho.int/S-201/gml/cs0/1.0"')
    t = re.sub(r"<(/?)([A-Za-z_][\w.-]*)(?=[\s/>])", lambda m: "<" + m.group(1) + ("ns4:" if not m.group(2).startswith("?") else "") + m.group(2), t)
    t = t.replace("xmlns:gml=", "xmlns:ns1=").replace("xmlns:S100=", "xmlns:ns2=")
    return t.replace("gml:", "ns1:").replace("S100:", "ns2:")


EDGE_FIXTURES = (("edge cases", _edge), ("legacy inline forms", _legacy), ("colour-less rhythms", _rhythm),
                 ("edge cases, S-201 as ns4:, GML as ns1:", lambda dii=False: _prefixed(_edge(dii))))


def fixtures(dii=False):
    """[(name, text)] — the kitchen in every mode, then the hand-written cases; with dii=True each carries a complete
    dataset identification block (see _dii)."""
    return [("FC kitchen (%s)" % m, kitchen(m, dii=dii)) for m in MODES] + [(n, f(dii)) for (n, f) in EDGE_FIXTURES]


if __name__ == "__main__":
    for name, text in fixtures():
        print("%-28s %8d bytes" % (name, len(text)))
    if len(sys.argv) > 1:
        open(sys.argv[1], "w", encoding="utf-8").write(dict(fixtures())[sys.argv[2] if len(sys.argv) > 2 else "FC kitchen (plain)"])
