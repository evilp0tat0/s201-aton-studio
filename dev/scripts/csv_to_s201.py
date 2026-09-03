#!/usr/bin/env python3
"""
csv_to_s201.py — Convert an AtoN-list CSV → S-201 GML 2.0.0 dataset.

Input format (CSV columns):
  National Number, Name, Type, IALA Cat, Shape and Topmark, Position, Character, Range

Output: S-201 Dataset GML with parent feature + Light child + Topmark child.

Region A (Oman): port=red, starboard=green.

Type column → S-201 feature type:
  safe water        → SafeWaterBuoy + sphere topmark
  port lateral      → LateralBuoy (red, can-shape topmark)
  stbd lateral      → LateralBuoy (green, cone-shape topmark)
  P to Stbd lateral → LateralBuoy (preferred channel to starboard, red/green/red, cone)
  N/E/S/W Cardinal  → CardinalBuoy (cones topmark per direction, yellow/black bands)
  Special / special → SpecialPurposeGeneralBuoy (yellow, X topmark)
  Sector            → SpecialPurposeGeneralBeacon + LightSectored child
  minor light       → SpecialPurposeGeneralBeacon (small pole/pile) + LightAllAround
  Beacon            → SpecialPurposeGeneralBeacon + LightAllAround
  harbour light     → SpecialPurposeGeneralBeacon (small pole) + LightAllAround
  stbd lateral with 'pile' shape → LateralBeacon (a beacon serving as lateral mark)

Light character ('Character' column) parsed to lightCharacteristic + signalGroup +
colour + signalPeriod. Modifiers: 'Sync' → synchronised flag (info), 'Dir' →
directional, '(vert)' → vertical multi-light, '2 Fl' → number of lights. A compound
'Q(6)+LFl' / 'VQ(6)+LFl' (south-cardinal notation) maps to the single FC listedValue
'… plus long-flash' with the group on the first token; a character with no colour
letter is a WHITE light by IHO/IALA convention.

Usage:  python csv_to_s201.py [<input.csv> [<output.gml>]]   (defaults: CSV_PATH/OUT_PATH)

Conformance: the emitted GML validates with ZERO error/warning findings against the
S-201 AtoN Studio validator (structural GML-STR + per-feature RULES) across all type
branches — see dev/scripts/precommit-check.py's converter self-test. FC-mandatory
attributes the source CSV may omit are defaulted to IALA-typical, FC-listed values
(buoyShape port=can/starboard=conical/safe-water=spherical/else pillar; beaconShape
'stake, pole, perch, post'; light colour white; categoryOfSpecialPurposeMark
'mark with unknown purpose') rather than left absent. Child Light/Topmark features carry
no <featureName> (DCEG §3.2 — the name lives on the parent only). Residual INFO-level
notes only: minor/harbour/sector lights modelled as SpecialPurposeGeneralBeacon are lit
navigation beacons, not yellow special marks (R1001-SPM-01/02) — forcing yellow would
misrepresent a white light, so their true colour is kept.
"""
import csv
import re
import os
import sys

# Default in/out paths (overridable via argv — see main()). Reuse for a new input by editing
# these OR by running:  python csv_to_s201.py <input.csv> <output.gml>
CSV_PATH = r"aton-list.csv"
OUT_PATH = r"output_S201.gml"
DS_ID = "DS.001"
DS_NAME = "Example Port AtoN Dataset"
PRODUCER_CODE = "XX01"  # fictional S-62-style producer code placeholder

# ───────── DMS parser ─────────
def parse_dms(s):
    """Parse 'dd mm.mmmL dd mm.mmmL' → (lat, lon) decimal-degrees (7 places)."""
    if not s: return None, None
    s = s.strip()
    m = re.match(r"(\d+)\s+([\d.]+)\s*([NS])\s+(\d+)\s+([\d.]+)\s*([EW])", s)
    if not m: return None, None
    lat_d, lat_m, lat_h, lon_d, lon_m, lon_h = m.groups()
    lat = float(lat_d) + float(lat_m) / 60
    lon = float(lon_d) + float(lon_m) / 60
    if lat_h == "S": lat = -lat
    if lon_h == "W": lon = -lon
    return round(lat, 7), round(lon, 7)

# ───────── Light character parser ─────────
LCHAR_MAP = {
    "F":   "fixed",
    "Fl":  "flashing",
    "LFl": "long-flashing",
    "L Fl":"long-flashing",
    "Q":   "quick-flashing",
    "VQ":  "very quick-flashing",
    "UQ":  "ultra quick-flashing",
    "Iso": "isophased",
    "Oc":  "occulting",
    "Mo":  "morse",
    "Al":  "alternating",
}
COL_MAP = {"R":"red","G":"green","W":"white","Y":"yellow","B":"blue","M":"violet"}

def parse_character(s):
    """Parse light character → dict."""
    out = {
        "lightCharacteristic": None,
        "signalGroup": None,
        "colour": None,
        "signalPeriod": None,
        "isSynced": False,
        "isDirectional": False,
        "isVertical": False,
        "multipleLights": False,
    }
    if not s: return out
    s = s.strip()
    # Sync
    if re.search(r"sync\.?\)?|^Sync\b", s, re.IGNORECASE):
        out["isSynced"] = True
        s = re.sub(r"\(sync\.?\)|Sync\s*", "", s, flags=re.IGNORECASE).strip()
    # Vertical
    if "(vert" in s.lower():
        out["isVertical"] = True
        s = re.sub(r"\(vert[^)]*\)", "", s).strip()
    # Directional
    if s.startswith("Dir "):
        out["isDirectional"] = True
        s = s[4:].strip()
        m = re.match(r"([WRGY]+)\s*(.*)", s)
        if m:
            cs = m.group(1)
            out["colour"] = "/".join(COL_MAP[c] for c in cs)
            s = m.group(2)
        out["lightCharacteristic"] = "fixed"
        return out
    # Multi-light prefix "2 Fl"
    m = re.match(r"^(\d+)\s+(.+)", s)
    if m:
        out["multipleLights"] = True
        s = m.group(2)
    # lightCharacteristic
    for c in ["L Fl", "LFl", "VQ", "UQ", "Iso", "Oc", "Mo", "Al", "Fl", "Q", "F"]:
        if re.match(r"^" + re.escape(c) + r"(\s|\(|$)", s):
            char = c
            s = s[len(c):].strip()
            # Composite group "(2+1)" comes first
            mc = re.match(r"\((\d+)\+(\d+)\)\s*(.*)", s)
            if mc:
                out["signalGroup"] = f"({mc.group(1)}+{mc.group(2)})"
                s = mc.group(3).strip()
            else:
                mg = re.match(r"\(([^)]+)\)\s*(.*)", s)
                if mg:
                    out["signalGroup"] = f"({mg.group(1)})"
                    s = mg.group(2).strip()
            out["lightCharacteristic"] = LCHAR_MAP.get(char, char.lower())
            # Compound "+LFl" tail (south cardinal "Q(6)+LFl", "VQ(6)+LFl", etc.). The app models
            # this as ONE FC lightCharacteristic listedValue ("… plus long-flash") with the group
            # on the FIRST token — NOT two <lightCharacteristic> elements. Upgrade the rhythm and
            # consume the tail; otherwise "+LFl" is silently dropped and R1001-CAR-02 rejects the
            # cardinal (a south cardinal must read Q(6)+LFl / VQ(6)+LFl).
            mplus = re.match(r"\+\s*L\s*Fl\b", s, re.IGNORECASE)
            if mplus and char in ("Q", "VQ", "UQ"):
                out["lightCharacteristic"] = {
                    "Q":  "quick-flash plus long-flash",
                    "VQ": "very quick-flash plus long-flash",
                    "UQ": "ultra quick-flash plus long-flash",
                }[char]
                s = s[mplus.end():].strip()
            break
    # Colour single letter
    mcol = re.match(r"^([WRGYBM])\s*(.*)", s)
    if mcol:
        out["colour"] = COL_MAP.get(mcol.group(1))
        s = mcol.group(2).strip()
    # Period (digits + s)
    mp = re.match(r"^(\d+(?:\.\d+)?)\s*s\b", s)
    if mp:
        out["signalPeriod"] = mp.group(1)
    return out

# ───────── Type mapping ─────────
def classify(type_col, shape_col):
    """Return (parent_ft, light_ft, topmark_shape, buoy_shape, beacon_shape, category_attr)."""
    t = (type_col or "").strip()
    shape = (shape_col or "").strip().lower()
    tl = t.lower()
    light_ft = "LightAllAround"
    topmark = None
    buoy_shape = None
    beacon_shape = None
    category = None
    if tl == "safe water":
        parent = "SafeWaterBuoy"
        if "pillar" in shape: buoy_shape = "pillar"
        elif "spar"  in shape: buoy_shape = "spar"
        if "sphere" in shape: topmark = "sphere"
    elif "lateral" in tl:
        if "pile" in shape:
            parent = "LateralBeacon"
            beacon_shape = "pile beacon"
        elif "pillar" in shape:
            parent = "LateralBuoy"
            buoy_shape = "pillar"
        elif "spar" in shape:
            parent = "LateralBuoy"
            buoy_shape = "spar"
        else:
            parent = "LateralBuoy"
        if "cone" in shape: topmark = "cone (point up)"
        elif "can"  in shape: topmark = "cylinder"
        # categoryOfLateralMark is FC 1..1 MANDATORY (S201-FEA-02) on BOTH LateralBuoy AND
        # LateralBeacon. Match by SUBSTRING (not `==`) so variants like "stbd lateral with pile"
        # still resolve — the "p to …" preferred-channel forms are checked FIRST because they
        # themselves contain "port"/"stbd" as substrings.
        if "p to stbd" in tl: category = "preferred channel to starboard lateral mark"
        elif "p to port" in tl: category = "preferred channel to port lateral mark"
        elif "port" in tl: category = "port-hand lateral mark"
        elif "stbd" in tl or "starboard" in tl: category = "starboard-hand lateral mark"
    elif "cardinal" in tl:
        parent = "CardinalBuoy"
        if "pillar" in shape: buoy_shape = "pillar"
        if   t.startswith("N"): category = "north cardinal mark"; topmark = "2 cones (points upward)"
        elif t.startswith("S"): category = "south cardinal mark"; topmark = "2 cones (points downward)"
        elif t.startswith("E"): category = "east cardinal mark";  topmark = "2 cones (base to base)"
        elif t.startswith("W"): category = "west cardinal mark";  topmark = "2 cones (point to point)"
    elif tl == "special":
        if "spar"   in shape: parent = "SpecialPurposeGeneralBuoy"; buoy_shape = "spar"
        elif "pillar" in shape: parent = "SpecialPurposeGeneralBuoy"; buoy_shape = "pillar"
        else: parent = "SpecialPurposeGeneralBeacon"; beacon_shape = "stake, pole, perch, post"
        if "x top" in shape or "x-top" in shape: topmark = "x-shaped"
    elif tl == "sector":
        parent = "SpecialPurposeGeneralBeacon"
        beacon_shape = "beacon tower"
        light_ft = "LightSectored"
    elif tl in ("minor light", "harbour light", "beacon"):
        parent = "SpecialPurposeGeneralBeacon"
        if "pole" in shape or "post" in shape: beacon_shape = "stake, pole, perch, post"
        elif "pile" in shape: beacon_shape = "pile beacon"
        elif "tower" in shape: beacon_shape = "beacon tower"
        elif "metal" in shape: beacon_shape = "beacon tower"
    else:
        parent = "SpecialPurposeGeneralBeacon"
    # buoyShape is FC 2.0.0 1..1 MANDATORY (FC line 6238, enum = BSHAPES); the CSV 'Shape and
    # Topmark' column is topmark-focused and often omits the buoy body, so default to the
    # IALA-typical body when absent — port=can / starboard=conical (IALA lateral convention),
    # safe-water=spherical, otherwise pillar. Emitting nothing would fail S201-SHP-01.
    if parent.endswith("Buoy") and not buoy_shape:
        cat = (category or "").lower()
        if "starboard" in cat:      buoy_shape = "conical"
        elif "port" in cat:         buoy_shape = "can"
        elif parent == "SafeWaterBuoy": buoy_shape = "spherical"
        else:                       buoy_shape = "pillar"
    # beaconShape is FC 2.0.0 1..1 MANDATORY (FC line 7321, enum = BEASHAPES); default an
    # unspecified beacon body to the generic pole/pile form so S201-SHP-04 is satisfied.
    if parent.endswith("Beacon") and not beacon_shape:
        beacon_shape = "stake, pole, perch, post"
    return parent, light_ft, topmark, buoy_shape, beacon_shape, category

# Buoy/beacon colour based on type AND light colour.
# Region A (Oman): port=red, starboard=green. When the CSV Type column disagrees
# with the actual light colour (e.g., "P to Stbd lateral" labelled but light is
# green → contradicts IALA Region A which requires red light for that type),
# the LIGHT colour wins because it's unambiguous (no plausible mis-encoding).
# This auto-corrects that mislabelled-buoy class of local labelling quirks.
def parent_colour(type_col, light_colour=None):
    # SUBSTRING matching (not `==`) so lateral variants like "stbd lateral with pile" resolve;
    # colour is FC 1..* MANDATORY on every buoy/beacon body (S201-COL-01). The "p to …" preferred-
    # channel forms are tested FIRST because they contain "port"/"stbd" as substrings.
    t = (type_col or "").lower()
    if "p to stbd" in t:
        # IALA standard P-to-Stbd: red+green+red body + red light.
        # If light is green (and not red), this is locally mis-labelled — treat as starboard.
        if light_colour == "green":
            return ["green"]  # regular starboard-hand
        return ["red","green","red"]
    if "p to port" in t:
        # IALA standard P-to-Port: green+red+green body + green light.
        # If light is red, locally mis-labelled — treat as port.
        if light_colour == "red":
            return ["red"]  # regular port-hand
        return ["green","red","green"]
    if "port lateral" in t:
        return ["red"]
    if "stbd lateral" in t or "starboard lateral" in t:
        return ["green"]
    if t == "safe water": return ["red","white"]
    if "cardinal" in t:
        if (type_col or "").startswith("N"): return ["black","yellow"]
        if (type_col or "").startswith("S"): return ["yellow","black"]
        if (type_col or "").startswith("E"): return ["black","yellow","black"]
        if (type_col or "").startswith("W"): return ["yellow","black","yellow"]
    if t in ("special","sector"): return ["yellow"]
    if t in ("minor light","beacon","harbour light"): return ["white"]
    return None

# Also auto-correct the categoryOfLateralMark + colourPattern + topmark colour
# when Type and Light colour disagree.
def lateral_category_resolved(type_col, light_colour):
    """Return (categoryOfLateralMark, colourPattern, topmark_colour) after auto-correction."""
    t = (type_col or "").lower()
    if "p to stbd" in t:
        if light_colour == "green":
            # locally mis-labelled → regular starboard
            return "starboard-hand lateral mark", None, "green"
        return "preferred channel to starboard lateral mark", "horizontal stripes", "red"
    if "p to port" in t:
        if light_colour == "red":
            return "port-hand lateral mark", None, "red"
        return "preferred channel to port lateral mark", "horizontal stripes", "green"
    if "port lateral" in t:
        return "port-hand lateral mark", None, "red"
    if "stbd lateral" in t or "starboard lateral" in t:
        return "starboard-hand lateral mark", None, "green"
    return None, None, None

def colour_pattern(type_col, light_colour=None):
    t = (type_col or "").lower()
    if "p to stbd" in t and light_colour == "green":
        return None  # locally mis-labelled — single colour, no pattern
    if "p to port" in t and light_colour == "red":
        return None
    if "p to" in t: return "horizontal stripes"
    if t == "safe water": return "vertical stripes"
    if "cardinal" in t: return "horizontal stripes"
    return None

# ───────── XML helpers ─────────
def xe(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&apos;")

def el(tag, content, indent=10):
    if content is None or content == "": return ""
    return f"{' '*indent}<{tag}>{xe(content)}</{tag}>\n"

# ───────── Feature builders ─────────
def build_geometry(gml_id, lat, lon, indent=10):
    return (f"{' '*indent}<geometry>\n"
            f"{' '*(indent+2)}<S100:pointProperty>\n"
            f"{' '*(indent+4)}<S100:Point gml:id=\"{xe(gml_id)}\" srsName=\"http://www.opengis.net/def/crs/EPSG/0/4326\" srsDimension=\"2\">\n"
            f"{' '*(indent+6)}<gml:pos>{lat:.7f} {lon:.7f}</gml:pos>\n"
            f"{' '*(indent+4)}</S100:Point>\n"
            f"{' '*(indent+2)}</S100:pointProperty>\n"
            f"{' '*indent}</geometry>\n")

def build_parent(pid, parent_ft, name, atonNumber, lat, lon, type_col,
                 buoy_shape, beacon_shape, category, child_ids, topmark_id,
                 light_colour=None):
    """Build the parent feature XML. light_colour is the parsed primary colour of the
    light child (red/green/yellow/etc.) — used to auto-correct lateral category and
    body colour when CSV Type column disagrees with the light (e.g., a buoy
    labelled 'P to Stbd lateral' but with green light → actually a starboard mark)."""
    out = [f"      <S201:{parent_ft} gml:id=\"{xe(pid)}\">\n"]
    # category attribute (lateral / cardinal / special)
    if "lateral" in parent_ft.lower():
        # Auto-correct category using light colour
        cat_resolved, _, _ = lateral_category_resolved(type_col, light_colour)
        out.append(el("categoryOfLateralMark", cat_resolved or category))
    elif "cardinal" in parent_ft.lower():
        out.append(el("categoryOfCardinalMark", category))
    elif "special" in parent_ft.lower():
        # categoryOfSpecialPurposeMark is FC 2.0.0 1..* MANDATORY on SpecialPurposeGeneral*
        # (FC — S201-FEA-06 / S201-ENUM-SPM). When the CSV gives no specific purpose (sector /
        # minor-light / harbour-light / plain "special"), emit the FC listed catch-all
        # "mark with unknown purpose" (SPMCATS) rather than omitting the mandatory attribute.
        out.append(el("categoryOfSpecialPurposeMark", category or "mark with unknown purpose"))
    # shape
    if buoy_shape:
        out.append(el("buoyShape", buoy_shape))
    if beacon_shape:
        out.append(el("beaconShape", beacon_shape))
    # colour (multi-value) — auto-corrected based on light colour
    cols = parent_colour(type_col, light_colour)
    if cols:
        for c in cols:
            out.append(el("colour", c))
    cp = colour_pattern(type_col, light_colour)
    if cp:
        out.append(el("colourPattern", cp))
    out.append(el("status", "permanent"))
    if atonNumber:
        out.append(el("AtoNNumber", atonNumber))
    # featureName
    if name:
        out.append("          <featureName>\n")
        out.append("            <displayName>true</displayName>\n")
        out.append("            <language>eng</language>\n")
        out.append(f"            <name>{xe(name)}</name>\n")
        out.append("          </featureName>\n")
    # children
    for cid in child_ids:
        out.append(f"          <child xlink:href=\"#{xe(cid)}\"/>\n")
    if topmark_id:
        out.append(f"          <child xlink:href=\"#{xe(topmark_id)}\"/>\n")
    # geometry
    out.append(build_geometry(f"GEO.{pid}", lat, lon))
    out.append(f"      </S201:{parent_ft}>\n")
    return "".join(out)

def build_light(lid, light_ft, name, lat, lon, parent_id, char, range_col, raw_char):
    """Build the Light* child feature."""
    out = [f"      <S201:{light_ft} gml:id=\"{xe(lid)}\">\n"]
    # colour is FC 2.0.0 1..* MANDATORY on LightAllAround/LightSectored (S201-LGT-12). A light
    # character with no colour letter means a WHITE light by IHO/IALA convention (e.g. "Fl 5s"
    # is white flashing) — so default the parsed colour to white rather than emit no <colour>,
    # which would fail S201-LGT-12. May be slash-separated for a multi-colour light.
    light_colours = [c.strip() for c in (char["colour"] or "white").split("/") if c.strip()]
    for c in light_colours:
        out.append(el("colour", c))
    out.append(el("exhibitionConditionOfLight", "night light"))
    if range_col and range_col.strip().replace(".","").isdigit():
        out.append(el("valueOfNominalRange", range_col.strip()))
    # rhythmOfLight or sectorCharacteristics
    if light_ft == "LightSectored":
        out.append("          <sectorCharacteristics>\n")
        if char["lightCharacteristic"]:
            out.append(f"            <lightCharacteristic>{xe(char['lightCharacteristic'])}</lightCharacteristic>\n")
        out.append("            <lightSector>\n")
        for c in light_colours:   # white-defaulted above; lightSector.colour is FC 1..* (S201-LGT-08)
            out.append(f"              <colour>{xe(c)}</colour>\n")
        out.append("            </lightSector>\n")
        if char["signalGroup"]:
            out.append(f"            <signalGroup>{xe(char['signalGroup'])}</signalGroup>\n")
        if char["signalPeriod"]:
            out.append(f"            <signalPeriod>{xe(char['signalPeriod'])}</signalPeriod>\n")
        out.append("          </sectorCharacteristics>\n")
    else:
        out.append("          <rhythmOfLight>\n")
        if char["lightCharacteristic"]:
            out.append(f"            <lightCharacteristic>{xe(char['lightCharacteristic'])}</lightCharacteristic>\n")
        if char["signalGroup"]:
            out.append(f"            <signalGroup>{xe(char['signalGroup'])}</signalGroup>\n")
        if char["signalPeriod"]:
            out.append(f"            <signalPeriod>{xe(char['signalPeriod'])}</signalPeriod>\n")
        out.append("          </rhythmOfLight>\n")
    # No <featureName> on the child: DCEG 2.0.0 §3.2 requires the name to live on the PARENT
    # only and NOT be repeated on child features (S201-REL-03). The child Light is an anonymous
    # component of its parent; the parent<->child xlink pair carries the relationship.
    out.append(f"          <parent xlink:href=\"#{xe(parent_id)}\"/>\n")
    out.append(build_geometry(f"GEO.{lid}", lat, lon))
    out.append(f"      </S201:{light_ft}>\n")
    return "".join(out)

def build_topmark(tid, name, lat, lon, parent_id, topmark_shape, colour):
    out = [f"      <S201:Topmark gml:id=\"{xe(tid)}\">\n"]
    if colour:
        out.append(el("colour", colour))
    out.append(el("topmarkDaymarkShape", topmark_shape))
    # No <featureName> on the child (DCEG §3.2 / S201-REL-03) — see build_light; the Topmark is
    # an anonymous component whose name lives on the parent only.
    out.append(f"          <parent xlink:href=\"#{xe(parent_id)}\"/>\n")
    out.append(build_geometry(f"GEO.{tid}", lat, lon))
    out.append("      </S201:Topmark>\n")
    return "".join(out)

def topmark_colour(type_col, parent_ft, light_colour=None):
    """Decide topmark colour per S-201/IALA conventions. Auto-corrects P-to-Stbd/P-to-Port
    when light colour disagrees (the mislabelled-buoy case)."""
    t = (type_col or "").lower()
    if "p to stbd" in t:
        # Standard: red can topmark. If light is green → locally mis-labelled, use green cone.
        return "green" if light_colour == "green" else "red"
    if "p to port" in t:
        # Standard: green cone topmark. If light is red → locally mis-labelled, use red.
        return "red" if light_colour == "red" else "green"
    if "port lateral" in t: return "red"
    if "stbd lateral" in t or "starboard lateral" in t: return "green"
    if t == "safe water":   return "red"
    if "cardinal" in t:     return "black"
    if t == "special":      return "yellow"
    return "yellow"

# ───────── Main ─────────
def main():
    # Paths from argv when supplied, else the module defaults (usage: script <in.csv> <out.gml>).
    # This lets the converter run against any input without hand-editing the source constants.
    csv_path = sys.argv[1] if len(sys.argv) > 1 else CSV_PATH
    out_path = sys.argv[2] if len(sys.argv) > 2 else OUT_PATH
    if not os.path.exists(csv_path):
        print("CSV not found:", csv_path); return
    rows = []
    # CSV has cp1252-encoded degree symbol; use that encoding for safety
    with open(csv_path, "r", encoding="cp1252") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("National Number"):
                rows.append(row)
    print(f"Parsed {len(rows)} rows from CSV.")

    # Bounding box
    lats, lons = [], []
    parsed = []
    for row in rows:
        lat, lon = parse_dms(row["Position"])
        if lat is None:
            print(" SKIP: cannot parse position", row["Position"]); continue
        lats.append(lat); lons.append(lon)
        parsed.append((row, lat, lon))
    if not parsed:
        print("No valid rows."); return
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)

    # Build features
    parent_n = 1
    child_n  = 200
    feats = []

    for row, lat, lon in parsed:
        national = (row["National Number"] or "").strip()
        name    = (row["Name"] or "").strip()
        type_col= (row["Type"] or "").strip()
        shape_col=(row["Shape and Topmark"] or "").strip()
        char_col= (row["Character"] or "").strip()
        range_col=(row["Range"] or "").strip()

        parent_ft, light_ft, topmark_shape, buoy_shape, beacon_shape, category = classify(type_col, shape_col)
        char = parse_character(char_col)

        pid  = f"AtoN.{parent_n:03d}"; parent_n += 1
        lid  = None
        tid  = None
        children = []
        if char["lightCharacteristic"]:
            lid = f"AtoN.{child_n:03d}"; child_n += 1
            children.append(lid)
        if topmark_shape:
            tid = f"AtoN.{child_n:03d}"; child_n += 1

        # Parsed light colour (first colour token if multi-valued) — feeds the
        # auto-correction logic for body colour + lateral category + topmark colour.
        light_colour = None
        if char["colour"]:
            light_colour = char["colour"].split("/")[0].strip()
        # Also auto-correct topmark shape if "P to Stbd" but light is green → use cone (starboard)
        if "p to stbd" in (type_col or "").lower() and light_colour == "green":
            topmark_shape = "cone, point up"
        elif "p to port" in (type_col or "").lower() and light_colour == "red":
            topmark_shape = "cylinder"
        feats.append(build_parent(pid, parent_ft, name, national, lat, lon, type_col,
                                  buoy_shape, beacon_shape, category, [lid] if lid else [], tid,
                                  light_colour=light_colour))
        if lid:
            feats.append(build_light(lid, light_ft, name, lat, lon, pid, char, range_col, char_col))
        if tid:
            feats.append(build_topmark(tid, name, lat, lon, pid, topmark_shape, topmark_colour(type_col, parent_ft, light_colour)))

    # Wrap in dataset
    dataset = f'''<?xml version="1.0" encoding="UTF-8"?>
<S201:Dataset xmlns:S201="http://www.iho.int/S-201/gml/cs0/2.0"
              xmlns:S100="http://www.iho.int/s100gml/5.0"
              xmlns:gml="http://www.opengis.net/gml/3.2"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              gml:id="{DS_ID}">
  <gml:boundedBy>
    <gml:Envelope srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
      <gml:lowerCorner>{min_lat:.7f} {min_lon:.7f}</gml:lowerCorner>
      <gml:upperCorner>{max_lat:.7f} {max_lon:.7f}</gml:upperCorner>
    </gml:Envelope>
  </gml:boundedBy>
  <S100:DatasetIdentificationInformation>
    <S100:encodingSpecification>S-100 Pt 10b GML</S100:encodingSpecification>
    <S100:encodingSpecificationEdition>5.2.0</S100:encodingSpecificationEdition>
    <S100:productIdentifier>S-201</S100:productIdentifier>
    <S100:productEdition>2.0.0</S100:productEdition>
    <S100:applicationProfile>S-201</S100:applicationProfile>
    <S100:datasetFileIdentifier>{xe(PRODUCER_CODE)}PORTSUHAR</S100:datasetFileIdentifier>
    <S100:datasetTitle>{xe(DS_NAME)}</S100:datasetTitle>
    <S100:datasetReferenceDate>2025-05-11</S100:datasetReferenceDate>
    <S100:datasetLanguage>eng</S100:datasetLanguage>
    <S100:datasetTopicCategory>oceans</S100:datasetTopicCategory>
    <S100:datasetTopicCategory>transportation</S100:datasetTopicCategory>
    <S100:datasetPurpose>Base</S100:datasetPurpose>
    <S100:updateNumber>0</S100:updateNumber>
  </S100:DatasetIdentificationInformation>
  <members>
{''.join(feats)}  </members>
</S201:Dataset>
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(dataset)
    print(f"Wrote {len(parsed)} features ({len(feats)} elements incl. children) -> {out_path}")

if __name__ == "__main__":
    main()
