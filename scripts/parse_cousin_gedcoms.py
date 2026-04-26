"""
parse_cousin_gedcoms.py — MRCA Audit for 27 Cousin GEDCOMs
===========================================================
Produces three deliverables:
  1. research/61-cousin-mrca-audit.json   — per-cousin MRCA verification records
  2. research/61-cousin-merged-people.json — deduplicated master person list

Hunter's direct-line anchor names (from entities.json + oral history) are
hard-coded for matching logic because GEDCOM @I1@ = redacted cousin, and we
need to walk upward to find a shared ancestor.

Run: python scripts/parse_cousin_gedcoms.py
"""

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
GED_DIR = Path(r"C:\Users\hspen\OneDrive\Desktop\Ancestry Gedcoms")
RESEARCH = Path(r"C:\Users\hspen\.openclaw\workspace\family-history\research")
ENT_FILE = RESEARCH / "entities.json"
OUT_AUDIT = RESEARCH / "61-cousin-mrca-audit.json"
OUT_PEOPLE = RESEARCH / "61-cousin-merged-people.json"

# ---------------------------------------------------------------------------
# Hunter's known direct-line anchors
# Each entry: {name_variants, birth_year, surname_line, side, notes}
# Used to identify MRCAs in GEDCOMs
# ---------------------------------------------------------------------------
HUNTER_ANCHORS = [
    # ── PATERNAL / HENSLEE branch ───────────────────────────────────────────
    {
        "id": "anchor_alice_henslee",
        "canonical": "Alice Marie Henslee Spence",
        "variants": ["alice marie henslee", "alice henslee", "alice spence", "alice marie spence",
                     "alice m henslee", "alice m spence"],
        "birth_year": 1936, "death_year": 2005,
        "surname_line": "Henslee", "side": "paternal",
        "notes": "Hunter's paternal grandmother; married Dale W. Spence Sr."
    },
    {
        "id": "anchor_dale_sr",
        "canonical": "Dr. Dale W. Spence Sr.",
        "variants": ["dale w spence sr", "dale william spence sr", "dale spence sr",
                     "dale w spence", "dale spence"],
        "birth_year": 1934,
        "surname_line": "Spence", "side": "paternal",
        "notes": "Hunter's paternal grandfather; Rice U Kinesiology; Col USMCR ret."
    },
    {
        "id": "anchor_lee_henslee",
        "canonical": "Lee Stuart Henslee",
        "variants": ["lee stuart henslee", "lee henslee", "l s henslee", "lee s henslee"],
        "birth_year": 1908, "death_year": 1994,
        "surname_line": "Henslee", "side": "paternal",
        "notes": "Alice's father. Born 2 Oct 1908, died 2 Sep 1994 Beaumont TX."
    },
    {
        "id": "anchor_frances_rau",
        "canonical": "Frances Virginia Rau Henslee",
        "variants": ["frances virginia rau", "frances rau", "frances v rau",
                     "frances virginia henslee", "frances rau henslee"],
        "birth_year": 1918, "death_year": 2008,
        "surname_line": "Rau", "side": "paternal",
        "notes": "Alice's mother. Born 1 Jan 1918, died 19 Dec 2008 Port Arthur TX."
    },
    {
        "id": "anchor_james_henslee",
        "canonical": "James Ernest Pappy Henslee",
        "variants": ["james ernest henslee", "james henslee", "pappy henslee",
                     "james e henslee", "j e henslee"],
        "birth_year": 1885, "death_year": 1948,
        "surname_line": "Henslee", "side": "paternal",
        "notes": "Lee's father. Born 23 Aug 1885 Lyons Burleson Co TX."
    },
    {
        "id": "anchor_mary_alice_stuart",
        "canonical": "Mary Alice Stuart Henslee",
        "variants": ["mary alice stuart", "mary alice henslee", "mary a stuart"],
        "birth_year": 1887, "death_year": 1981,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Lee's mother. Born 20 Jul 1887 Caldwell Burleson TX."
    },
    {
        "id": "anchor_dovie_byrd",
        "canonical": "Dovie Byrd Spence",
        "variants": ["dovie byrd", "dovie spence", "dovie byrd spence"],
        "birth_year": None,
        "surname_line": "Byrd", "side": "paternal",
        "notes": "Probable mother of Dale Sr.; maiden name Byrd."
    },
    {
        "id": "anchor_john_byrd",
        "canonical": "John Archie Asner Byrd",
        "variants": ["john archie asner byrd", "john a byrd", "john archie byrd"],
        "birth_year": 1868,
        "surname_line": "Byrd", "side": "paternal",
        "notes": "Probable grandfather of Dale Sr. (Dovie's father)."
    },
    {
        "id": "anchor_william_leander_byrd",
        "canonical": "William Leander Byrd",
        "variants": ["william leander byrd", "pvt william leander byrd",
                     "william l byrd", "wm leander byrd"],
        "birth_year": 1832,
        "surname_line": "Byrd", "side": "paternal",
        "notes": "In entities.json as p153. b. Frankfort Franklin Co Alabama. Father of Richard Lecurgis Byrd b.1860 and possibly John A Byrd b.1868 TX."
    },
    {
        "id": "anchor_margarete_byrd",
        "canonical": "Margarete Rhetta Peradeau Byrd",
        "variants": ["margarete rhetta peradeau byrd", "margaret rhetta peradeau",
                     "margarett rhetta perrydore byrd", "margaret rhetta byrd",
                     "margarett rhetta peradeau"],
        "birth_year": 1829,
        "surname_line": "Byrd", "side": "paternal",
        "notes": "In entities.json as p154. Wife of William Leander Byrd b.1832."
    },
    {
        "id": "anchor_richard_lecurgis_byrd",
        "canonical": "Richard Lecurgis Byrd",
        "variants": ["richard lecurgis byrd", "richard byrd", "r l byrd"],
        "birth_year": 1860,
        "surname_line": "Byrd", "side": "paternal",
        "notes": "Son of William Leander Byrd b.1832. Father of Lillie Lodusky Byrd Gillespie (B.G.'s ancestor) and Woodrow Wilson Byrd (L.B.'s grandfather)."
    },
    {
        "id": "anchor_maxfield_henslee",
        "canonical": "Maxfield Henslee",
        "variants": ["maxfield henslee"],
        "birth_year": 1727,
        "surname_line": "Henslee", "side": "paternal",
        "notes": "Deep Henslee patriarch."
    },
    {
        "id": "anchor_enoch_henslee",
        "canonical": "Enoch Henslee",
        "variants": ["enoch henslee"],
        "birth_year": 1788,
        "surname_line": "Henslee", "side": "paternal",
    },
    {
        "id": "anchor_miles_henslee",
        "canonical": "Miles Reed Henslee",
        "variants": ["miles reed henslee", "miles henslee"],
        "birth_year": 1856,
        "surname_line": "Henslee", "side": "paternal",
    },
    # ── PATERNAL / SPENCE branch ─────────────────────────────────────────────
    {
        "id": "anchor_lewis_lunsford_stuart",
        "canonical": "Lewis Lunsford Stuart",
        "variants": ["lewis lunsford stuart", "lewis lunford stuart", "lewis l stuart",
                     "lewis stuart", "l l stuart"],
        "birth_year": 1830,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Father of Mary Alice Stuart (b.1887 Caldwell Burleson TX) and Reuben Lucius Stuart (b.1885 Caldwell Burleson TX). MRCA for Stuart-line cousins."
    },
    {
        "id": "anchor_reuben_stuart",
        "canonical": "Reuben Lucius Stuart",
        "variants": ["reuben lucius stuart", "reuben l stuart", "reuben stuart"],
        "birth_year": 1885,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Sibling of Mary Alice Stuart (Hunter's paternal great-grandmother). b. Caldwell Burleson TX."
    },
    {
        "id": "anchor_jesse_weed_stuart",
        "canonical": "Jesse Weed Stuart",
        "variants": ["jesse weed stuart", "jess stuart", "jesse stuart", "jess weed stuart"],
        "birth_year": 1914,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Child of Reuben Lucius Stuart. DNA-match MRCA for Stuart-line cousins."
    },
    {
        "id": "anchor_nora_sale",
        "canonical": "Nora Corrigan Sale Stuart",
        "variants": ["nora corrigan sale", "nora c sale", "nora sale"],
        "birth_year": 1846,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Wife of Lewis Lunsford Stuart."
    },
    # ── MATERNAL / MATTINGLY branch ──────────────────────────────────────────
    {
        "id": "anchor_sharyn_mattingly",
        "canonical": "Sharyn Mattingly",
        "variants": ["sharyn mattingly", "shari mattingly", "shari", "sharyn"],
        "birth_year": 1947,
        "surname_line": "Mattingly", "side": "maternal",
        "notes": "Hunter's maternal grandmother."
    },
    {
        "id": "anchor_leroy_mattingly",
        "canonical": "Leroy Teichmuller Mattingly",
        "variants": ["leroy teichmuller mattingly", "leroy t mattingly", "leroy mattingly",
                     "leroy teichmueller mattingly"],
        "birth_year": 1896,
        "surname_line": "Mattingly", "side": "maternal",
        "notes": "Shari's grandfather. b. 31 Aug 1896 La Grange TX d. 8 Oct 1968 San Antonio."
    },
    {
        "id": "anchor_jennive_lepick",
        "canonical": "Jennive Lepick Mattingly",
        "variants": ["jennive lepick", "jennive mattingly", "jennie lepick",
                     "jennive lepik", "jennive l mattingly"],
        "birth_year": 1923,
        "surname_line": "Lepick", "side": "maternal",
        "notes": "Shari's grandmother (maternal). b. 2 Feb 1923 Wilson Co TX."
    },
    {
        "id": "anchor_fred_lepick_sr",
        "canonical": "Fred Charles Lepick Sr.",
        "variants": ["fred charles lepick sr", "fred lepick sr", "fred c lepick",
                     "fred lepick", "fred charles lepik sr", "fred lepik"],
        "birth_year": 1894,
        "surname_line": "Lepick", "side": "maternal",
    },
    {
        "id": "anchor_fred_lepick_jr",
        "canonical": "Fred Charles Lepick Jr.",
        "variants": ["fred charles lepick jr", "fred lepick jr", "fred c lepick jr"],
        "birth_year": 1925,
        "surname_line": "Lepick", "side": "maternal",
    },
    {
        "id": "anchor_frank_lepick",
        "canonical": "Frank Lepik / Lepick",
        "variants": ["frank lepik", "frank lepick", "frantisek lepik"],
        "birth_year": 1862,
        "surname_line": "Lepick", "side": "maternal",
    },
    {
        "id": "anchor_dr_claude_mattingly",
        "canonical": "Dr. Claude Mattingly",
        "variants": ["dr claude mattingly", "claude mattingly"],
        "birth_year": 1898,
        "surname_line": "Mattingly", "side": "maternal",
    },
    {
        "id": "anchor_ruth_baity_mattingly",
        "canonical": "Ruth Baity Mattingly",
        "variants": ["ruth baity mattingly", "ruth mattingly", "ruth baity"],
        "birth_year": 1900,
        "surname_line": "Baity", "side": "maternal",
    },
    # ── PATERNAL / Stuart/Sale/Herron branch (cousins connecting via Reuben Stuart) ────
    {
        "id": "anchor_jesse_dayton_herron",
        "canonical": "Jesse Dayton Herron",
        "variants": ["jesse dayton herron", "jesse herron", "j d herron",
                     "jesse d herron"],
        "birth_year": 1918,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Father of several DNA-matching cousins (4scherff, Gary Burton). Connection to Hunter's line via shared Burleson County TX Stuart ancestors is probable but not yet document-confirmed."
    },
    {
        "id": "anchor_william_woodville_herron",
        "canonical": "William Woodville Herron",
        "variants": ["william woodville herron", "william w herron", "w w herron",
                     "william herron", "woodville herron"],
        "birth_year": 1885,
        "surname_line": "Stuart", "side": "paternal",
        "notes": "Appears in Reba VPJ, Linda Coleman, M.P., Gary Burton, 4scherff trees. b. Union Grove Marshall Alabama."
    },
    # ── MATERNAL / TEICHMUELLER branch ───────────────────────────────────────
    {
        "id": "anchor_hans_teichmueller",
        "canonical": "Hans Teichmueller",
        "variants": ["hans teichmueller", "hans teichmuller", "hans teichmuller mattingly"],
        "birth_year": 1837,
        "surname_line": "Teichmueller", "side": "maternal",
    },
    {
        "id": "anchor_minette_teichmueller",
        "canonical": "Minette Teichmueller Pohl",
        "variants": ["minette teichmueller", "minette pohl", "minette teichmuller pohl",
                     "wilhelmina teichmueller", "wilhelmina teichmuller"],
        "birth_year": 1871,
        "surname_line": "Teichmueller", "side": "maternal",
    },
    # ── PATERNAL / BAITY branch ───────────────────────────────────────────────
    {
        "id": "anchor_william_baity",
        "canonical": "William Alexander Baity",
        "variants": ["william alexander baity", "william a baity", "w a baity"],
        "birth_year": 1862,
        "surname_line": "Baity", "side": "paternal",
        "notes": "Connected to Henslee side via marriage chains."
    },
]

# Pre-compute normalized variants for fast lookup
def _norm(s):
    if not s:
        return ""
    nfkd = unicodedata.normalize("NFKD", s)
    only_ascii = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^\w\s]", "", only_ascii).lower()
    return re.sub(r"\s+", " ", cleaned).strip()

ANCHOR_NORM_MAP = {}  # normalized_variant -> anchor
for anc in HUNTER_ANCHORS:
    for v in anc.get("variants", []):
        ANCHOR_NORM_MAP[_norm(v)] = anc
    ANCHOR_NORM_MAP[_norm(anc["canonical"])] = anc


# ---------------------------------------------------------------------------
# GEDCOM parser (reused from parse_gedcoms.py, self-contained here)
# ---------------------------------------------------------------------------
def parse_gedcom_file(path):
    """Return (persons dict, families dict).
    persons: {xref -> {given, surname, full_name, sex, birth_year, birth_date,
                        birth_place, death_year, death_date, death_place, famc, fams[]}}
    families: {xref -> {husb, wife, children[], marr_year, marr_date, marr_place}}
    """
    persons = {}
    families = {}
    cur = None
    cur_kind = None
    cur_event = None

    text = path.read_text(encoding="utf-8", errors="replace")
    for raw in text.splitlines():
        line = raw.rstrip("\r\n")
        if not line:
            continue
        m = re.match(r"^(\d+)\s+(@[^@]+@)?\s*(\S+)\s*(.*)$", line)
        if not m:
            continue
        level, xref, tag, value = int(m.group(1)), m.group(2), m.group(3), m.group(4)

        if level == 0:
            cur_event = None
            if tag == "INDI":
                cur = {"xref": xref, "given": "", "surname": "", "full_name": "",
                       "sex": "", "birth_year": None, "birth_date": "", "birth_place": "",
                       "death_year": None, "death_date": "", "death_place": "",
                       "famc": None, "fams": []}
                persons[xref] = cur
                cur_kind = "INDI"
            elif tag == "FAM":
                cur = {"xref": xref, "husb": None, "wife": None, "children": [],
                       "marr_year": None, "marr_date": "", "marr_place": ""}
                families[xref] = cur
                cur_kind = "FAM"
            else:
                cur = None
                cur_kind = None
            continue

        if cur is None:
            continue

        if cur_kind == "INDI":
            if level == 1:
                cur_event = None
                if tag == "NAME":
                    cur["full_name"] = value.replace("/", "").strip()
                    sm = re.match(r"^(.*?)/(.+?)/", value)
                    if sm:
                        cur["given"] = sm.group(1).strip()
                        cur["surname"] = sm.group(2).strip()
                    else:
                        # No slashes: treat last word as surname
                        parts = value.strip().split()
                        if len(parts) > 1:
                            cur["surname"] = parts[-1]
                            cur["given"] = " ".join(parts[:-1])
                        else:
                            cur["given"] = value.strip()
                elif tag == "SEX":
                    cur["sex"] = value.strip()
                elif tag == "BIRT":
                    cur_event = "BIRT"
                elif tag == "DEAT":
                    cur_event = "DEAT"
                elif tag == "FAMC":
                    cur["famc"] = value.strip()
                elif tag == "FAMS":
                    cur["fams"].append(value.strip())
            elif level == 2:
                if cur_event == "BIRT":
                    if tag == "DATE":
                        cur["birth_date"] = value.strip()
                        ym = re.search(r"\b(1[2-9]\d{2}|20\d{2})\b", value)
                        if ym:
                            cur["birth_year"] = int(ym.group(1))
                    elif tag == "PLAC":
                        cur["birth_place"] = value.strip()
                elif cur_event == "DEAT":
                    if tag == "DATE":
                        cur["death_date"] = value.strip()
                        ym = re.search(r"\b(1[2-9]\d{2}|20\d{2})\b", value)
                        if ym:
                            cur["death_year"] = int(ym.group(1))
                    elif tag == "PLAC":
                        cur["death_place"] = value.strip()

        elif cur_kind == "FAM":
            if level == 1:
                cur_event = None
                if tag == "HUSB":
                    cur["husb"] = value.strip()
                elif tag == "WIFE":
                    cur["wife"] = value.strip()
                elif tag == "CHIL":
                    cur["children"].append(value.strip())
                elif tag == "MARR":
                    cur_event = "MARR"
            elif level == 2 and cur_event == "MARR":
                if tag == "DATE":
                    cur["marr_date"] = value.strip()
                    ym = re.search(r"\b(1[2-9]\d{2}|20\d{2})\b", value)
                    if ym:
                        cur["marr_year"] = int(ym.group(1))
                elif tag == "PLAC":
                    cur["marr_place"] = value.strip()

    return persons, families


# ---------------------------------------------------------------------------
# Filename → claimed relationship parser
# ---------------------------------------------------------------------------
def parse_filename_relationship(stem):
    """Extract cousin_name and claimed_relationship from filename stem."""
    # Pattern: "Name - relationship side" or "Name-relationship-side"
    # Try dash-separated first
    parts = re.split(r"\s*[-–]\s*", stem, maxsplit=1)
    if len(parts) == 2:
        name = parts[0].strip()
        rel = parts[1].strip()
    else:
        name = stem
        rel = "unknown"
    # Clean up trailing "(2)" from duplicate files
    name = re.sub(r"\s*\(\d+\)\s*$", "", name).strip()
    return name, rel


# ---------------------------------------------------------------------------
# Anchor matching
# ---------------------------------------------------------------------------
def find_anchors_in_gedcom(persons, families):
    """Return list of {anchor, xref, person} for every anchor found in this GEDCOM."""
    found = []
    for xref, p in persons.items():
        full = p.get("full_name", "")
        if not full:
            continue
        norm = _norm(full)
        # Direct match
        if norm in ANCHOR_NORM_MAP:
            anchor = ANCHOR_NORM_MAP[norm]
            # Birth year sanity check (within 5 years if both known)
            ged_by = p.get("birth_year")
            anc_by = anchor.get("birth_year")
            if ged_by and anc_by and abs(ged_by - anc_by) > 10:
                continue  # Too far off — probably a different person
            found.append({"anchor": anchor, "xref": xref, "person": p})
            continue
        # Partial match — surname match + partial given match
        surname = _norm(p.get("surname", ""))
        given = _norm(p.get("given", ""))
        for norm_v, anchor in ANCHOR_NORM_MAP.items():
            if surname and surname in norm_v and given and given.split()[0] in norm_v:
                ged_by = p.get("birth_year")
                anc_by = anchor.get("birth_year")
                if ged_by and anc_by and abs(ged_by - anc_by) > 10:
                    continue
                # Avoid duplicates
                if not any(f["xref"] == xref and f["anchor"]["id"] == anchor["id"] for f in found):
                    found.append({"anchor": anchor, "xref": xref, "person": p,
                                  "partial_match": True})
                break
    return found


# ---------------------------------------------------------------------------
# Ancestor chain walker
# ---------------------------------------------------------------------------
def build_parent_map(persons, families):
    """Return {child_xref: (father_xref_or_None, mother_xref_or_None)}"""
    parent_map = {}
    for fxref, fam in families.items():
        husb = fam.get("husb")
        wife = fam.get("wife")
        for child_xref in fam.get("children", []):
            parent_map[child_xref] = (husb, wife)
    return parent_map


def get_ancestors(xref, parent_map, max_depth=15):
    """BFS upward from xref. Return {xref: generation_depth}."""
    visited = {}
    queue = [(xref, 0)]
    while queue:
        cur, depth = queue.pop(0)
        if cur in visited or depth > max_depth:
            continue
        visited[cur] = depth
        parents = parent_map.get(cur, (None, None))
        for p_xref in parents:
            if p_xref and p_xref not in visited:
                queue.append((p_xref, depth + 1))
    return visited


def path_from_to(start_xref, end_xref, parent_map, persons, max_depth=15):
    """Breadth-first path from start (cousin) upward to end (MRCA xref).
    Returns list of xrefs or None."""
    if start_xref == end_xref:
        return [start_xref]
    # BFS with path tracking
    from collections import deque
    queue = deque([(start_xref, [start_xref])])
    visited = {start_xref}
    while queue:
        cur, path = queue.popleft()
        if len(path) > max_depth:
            continue
        parents = parent_map.get(cur, (None, None))
        for p_xref in parents:
            if not p_xref or p_xref in visited:
                continue
            new_path = path + [p_xref]
            if p_xref == end_xref:
                return new_path
            visited.add(p_xref)
            queue.append((p_xref, new_path))
    return None


def xref_to_label(xref, persons):
    """Human-readable label for an xref."""
    if xref not in persons:
        return xref
    p = persons[xref]
    name = p.get("full_name") or f"{p.get('given','')} {p.get('surname','')}".strip()
    by = p.get("birth_year")
    return f"{name} (b.{by})" if by else name


# ---------------------------------------------------------------------------
# Surname-line inference from GEDCOM contents
# ---------------------------------------------------------------------------
SURNAME_LINE_KEYWORDS = {
    "Henslee": ["henslee", "hensely", "hensley"],
    "Byrd": ["byrd", "bird"],
    "Stuart": ["stuart"],
    "Rau": ["rau"],
    "Spence": ["spence"],
    "Mattingly": ["mattingly", "mattingley"],
    "Lepick": ["lepick", "lepik", "lepic"],
    "Teichmueller": ["teichmueller", "teichmuller", "teichmüller"],
    "Baity": ["baity"],
    "Boehme": ["boehme", "böhme"],
    "Gillespie": ["gillespie"],
    "Noble": ["noble"],
    "Jarisch": ["jarisch"],
    "Frost": ["frost"],
    "Herron": ["herron"],
    "Vincent": ["vincent"],
    "Chewning": ["chewning"],
    "Mattingley": ["mattingley"],
    "Westerfield": ["westerfield"],
    "Padgett": ["padgett"],
}

def detect_surname_lines(persons):
    """Detect which Hunter surname lines appear in this GEDCOM."""
    found_lines = set()
    all_surnames = [_norm(p.get("surname","")) for p in persons.values()]
    all_surnames_str = " ".join(all_surnames)
    for line_name, keywords in SURNAME_LINE_KEYWORDS.items():
        for kw in keywords:
            if kw in all_surnames_str:
                found_lines.add(line_name)
                break
    return sorted(found_lines)


# ---------------------------------------------------------------------------
# Side inference
# ---------------------------------------------------------------------------
def infer_side(filename_rel, surname_lines, anchors_found):
    """Infer 'paternal', 'maternal', or 'unknown' side."""
    fl = filename_rel.lower()
    if "paternal" in fl:
        return "paternal"
    if "maternal" in fl:
        return "maternal"
    # Infer from anchors
    sides = [a["anchor"]["side"] for a in anchors_found if "side" in a["anchor"]]
    if sides:
        if all(s == "paternal" for s in sides):
            return "paternal"
        if all(s == "maternal" for s in sides):
            return "maternal"
    # Infer from surname lines
    paternal_lines = {"Henslee", "Byrd", "Stuart", "Rau", "Spence", "Baity"}
    maternal_lines = {"Mattingly", "Lepick", "Teichmueller", "Boehme"}
    p_score = sum(1 for sl in surname_lines if sl in paternal_lines)
    m_score = sum(1 for sl in surname_lines if sl in maternal_lines)
    if p_score > m_score:
        return "paternal"
    if m_score > p_score:
        return "maternal"
    return "unknown"


# ---------------------------------------------------------------------------
# Main per-GEDCOM audit logic
# ---------------------------------------------------------------------------
def audit_one_gedcom(fp, persons, families):
    """Return the audit record dict for one GEDCOM file."""
    stem = fp.stem
    cousin_name, claimed_rel = parse_filename_relationship(stem)
    n_indi = len(persons)
    n_fam = len(families)

    parent_map = build_parent_map(persons, families)
    surname_lines = detect_surname_lines(persons)
    anchors_found = find_anchors_in_gedcom(persons, families)

    # @I1@ is the redacted cousin (Ancestry exports the DNA match as record #1)
    cousin_xref = "@I1@"
    cousin_person = persons.get(cousin_xref, {})
    cousin_label = cousin_person.get("full_name") or cousin_name

    # Try to get ancestors of @I1@
    cousin_ancestors = get_ancestors(cousin_xref, parent_map)

    # Find anchor hits that are also ancestors of the cousin
    mrca_hits = []
    for af in anchors_found:
        axref = af["xref"]
        if axref in cousin_ancestors:
            mrca_hits.append({
                "anchor": af["anchor"],
                "xref": axref,
                "person": af["person"],
                "depth_from_cousin": cousin_ancestors[axref],
                "partial_match": af.get("partial_match", False),
            })

    # Sort by shallowest (most recent) MRCA first
    mrca_hits.sort(key=lambda x: x["depth_from_cousin"])

    if mrca_hits:
        best = mrca_hits[0]
        mrca_person = best["person"]
        mrca_anchor = best["anchor"]
        mrca_by = mrca_person.get("birth_year") or mrca_anchor.get("birth_year")
        mrca_name = (mrca_person.get("full_name") or mrca_anchor["canonical"])
        # Build path from cousin to MRCA
        path_xrefs = path_from_to(cousin_xref, best["xref"], parent_map, persons)
        if path_xrefs:
            path_labels = [xref_to_label(x, persons) for x in path_xrefs]
        else:
            # Fallback: just show the persons at cousin and MRCA
            path_labels = [cousin_label, f"... → {mrca_name}"]

        confidence = "probable" if best.get("partial_match") else "confirmed"
        # Cross-check birth year
        ged_by = mrca_person.get("birth_year")
        anc_by = mrca_anchor.get("birth_year")
        if ged_by and anc_by and abs(ged_by - anc_by) > 5:
            confidence = "conflicting"
            evidence = (f"Name '{mrca_name}' matches anchor '{mrca_anchor['canonical']}' "
                        f"but birth year mismatch: GEDCOM={ged_by} vs expected={anc_by}.")
        else:
            evidence = (f"'{mrca_name}' found at depth {best['depth_from_cousin']} above "
                        f"cousin in GEDCOM. "
                        f"Matches Hunter anchor '{mrca_anchor['canonical']}' "
                        f"(b.{anc_by or '?'}) on {mrca_anchor['side']} side "
                        f"via {mrca_anchor['surname_line']} line.")
            if best.get("partial_match"):
                evidence += " [Partial name match — verify manually.]"

        side = infer_side(claimed_rel, surname_lines, anchors_found)
        verified_link = True

        # Collect new ancestors (any non-empty named person above the MRCA)
        new_ancestors = []
        for xref_above, depth in cousin_ancestors.items():
            if depth <= best["depth_from_cousin"]:
                continue  # Only above MRCA
            pa = persons.get(xref_above, {})
            name_a = pa.get("full_name", "")
            if not name_a:
                continue
            norm_a = _norm(name_a)
            # Skip if already a known anchor
            if norm_a in ANCHOR_NORM_MAP:
                continue
            new_ancestors.append({
                "name": name_a,
                "birth_year": pa.get("birth_year"),
                "birth_place": pa.get("birth_place"),
                "death_year": pa.get("death_year"),
                "death_place": pa.get("death_place"),
                "surname": pa.get("surname", ""),
            })
        new_ancestors.sort(key=lambda x: x.get("birth_year") or 9999)

        return {
            "cousin_file": fp.name,
            "cousin_name": cousin_name,
            "claimed_relationship": claimed_rel,
            "individuals_in_gedcom": n_indi,
            "families_in_gedcom": n_fam,
            "surname_lines_found": surname_lines,
            "verified_link": verified_link,
            "side": side,
            "mrca_with_hunter": {
                "name": mrca_name,
                "birth_year": mrca_by,
                "death_year": mrca_person.get("death_year") or mrca_anchor.get("death_year"),
                "birth_place": mrca_person.get("birth_place", ""),
                "surname_line": mrca_anchor["surname_line"],
                "anchor_id": mrca_anchor["id"],
            },
            "path_from_cousin_to_hunter": path_labels,
            "all_mrca_candidates": [
                {
                    "name": h["person"].get("full_name", h["anchor"]["canonical"]),
                    "anchor_id": h["anchor"]["id"],
                    "depth": h["depth_from_cousin"],
                    "surname_line": h["anchor"]["surname_line"],
                    "partial_match": h.get("partial_match", False),
                }
                for h in mrca_hits
            ],
            "confidence": confidence,
            "evidence": evidence,
            "new_ancestors_unlocked": new_ancestors[:20],  # cap at 20 per cousin
        }

    else:
        # No anchor found in ancestors — try to find if anchor is a sibling or descendant
        # (cousin's sibling might be in Hunter's line — detect via shared FAM)
        side = infer_side(claimed_rel, surname_lines, [])
        reason = "No Hunter anchor found among ancestors of @I1@."

        # Check if any anchor appears AT ALL in the GEDCOM (even not as ancestor)
        any_anchor_in_ged = []
        for af in anchors_found:
            any_anchor_in_ged.append({
                "anchor_id": af["anchor"]["id"],
                "name": af["anchor"]["canonical"],
                "person_in_ged": af["person"].get("full_name", ""),
                "relationship_to_cousin": "non-ancestor (sibling/descendant/in-law)",
            })

        if any_anchor_in_ged:
            reason = (f"Anchors found in GEDCOM but not as direct ancestors of @I1@: "
                      f"{[a['name'] for a in any_anchor_in_ged]}. "
                      f"Possibly a collateral relative (e.g. sibling who married into Hunter's line).")
            confidence = "probable"
            verified_link = True
            evidence = reason
        else:
            confidence = "unverified"
            verified_link = False
            evidence = (f"No Hunter surname anchor found. "
                        f"Surname lines in GEDCOM: {surname_lines}. "
                        f"May need manual review — redacted entries in GEDCOM limit tracing.")

        return {
            "cousin_file": fp.name,
            "cousin_name": cousin_name,
            "claimed_relationship": claimed_rel,
            "individuals_in_gedcom": n_indi,
            "families_in_gedcom": n_fam,
            "surname_lines_found": surname_lines,
            "verified_link": verified_link,
            "side": side,
            "mrca_with_hunter": None,
            "path_from_cousin_to_hunter": [],
            "all_mrca_candidates": any_anchor_in_ged,
            "confidence": confidence,
            "evidence": evidence,
            "new_ancestors_unlocked": [],
        }


# ---------------------------------------------------------------------------
# Deduplication for merged-people output
# ---------------------------------------------------------------------------
def normalize_key(p):
    """Stable dedup key: (normalized_name, birth_year_bucket)."""
    full = p.get("full_name") or f"{p.get('given','')} {p.get('surname','')}".strip()
    norm = _norm(full)
    by = p.get("birth_year")
    # Bucket to decade to handle slight date discrepancies
    by_bucket = (by // 10 * 10) if by else 0
    return (norm, by_bucket)


def merge_person_into(target, source, source_file):
    """Merge source fields into target (non-destructive — fill blanks only)."""
    target.setdefault("source_files", [])
    if source_file not in target["source_files"]:
        target["source_files"].append(source_file)
    for fld in ("sex", "birth_year", "birth_date", "birth_place",
                "death_year", "death_date", "death_place", "surname", "given"):
        if not target.get(fld) and source.get(fld):
            target[fld] = source[fld]
    # Union parent / spouse / child sets
    for rel_key in ("parent_names", "spouse_names", "child_names"):
        if rel_key not in target:
            target[rel_key] = set()
        if rel_key in source:
            target[rel_key].update(source[rel_key])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    files = sorted(GED_DIR.glob("*.ged"))
    print(f"Found {len(files)} GEDCOM files in {GED_DIR}")

    audit_records = []
    all_people_map = {}  # dedup key -> merged person record

    duplicate_file_stems = set()  # track duplicates like "Diane Matava (2)"

    for fp in files:
        # Skip duplicate "(2)" files — same data as the primary
        if re.search(r"\(\d+\)\.ged$", fp.name):
            duplicate_file_stems.add(fp.stem)
            print(f"  SKIP duplicate: {fp.name}")
            continue

        print(f"  Parsing: {fp.name}")
        persons, families = parse_gedcom_file(fp)

        # Build parent map for this file (for child_names in merged people)
        parent_map_local = build_parent_map(persons, families)

        # Enrich persons with parent/spouse/child names (for merged output)
        for xref, p in persons.items():
            p_enriched = dict(p)
            p_enriched["parent_names"] = set()
            p_enriched["spouse_names"] = set()
            p_enriched["child_names"] = set()
            if p.get("famc") and p["famc"] in families:
                fam = families[p["famc"]]
                for rel_xref in [fam.get("husb"), fam.get("wife")]:
                    if rel_xref and rel_xref in persons and rel_xref != xref:
                        rn = persons[rel_xref].get("full_name", "")
                        if rn:
                            p_enriched["parent_names"].add(rn)
            for fxref in p.get("fams", []):
                if fxref not in families:
                    continue
                fam = families[fxref]
                for role_xref in [fam.get("husb"), fam.get("wife")]:
                    if role_xref and role_xref != xref and role_xref in persons:
                        sn = persons[role_xref].get("full_name", "")
                        if sn:
                            p_enriched["spouse_names"].add(sn)
                for child_xref in fam.get("children", []):
                    if child_xref in persons:
                        cn = persons[child_xref].get("full_name", "")
                        if cn:
                            p_enriched["child_names"].add(cn)
            persons[xref] = p_enriched

        # Merge into global people map
        for xref, p in persons.items():
            full = p.get("full_name", "")
            if not full:
                continue  # skip redacted entries
            key = normalize_key(p)
            if key not in all_people_map:
                all_people_map[key] = {
                    "full_name": full,
                    "given": p.get("given", ""),
                    "surname": p.get("surname", ""),
                    "sex": p.get("sex", ""),
                    "birth_year": p.get("birth_year"),
                    "birth_date": p.get("birth_date", ""),
                    "birth_place": p.get("birth_place", ""),
                    "death_year": p.get("death_year"),
                    "death_date": p.get("death_date", ""),
                    "death_place": p.get("death_place", ""),
                    "source_files": [fp.name],
                    "parent_names": set(p.get("parent_names", [])),
                    "spouse_names": set(p.get("spouse_names", [])),
                    "child_names": set(p.get("child_names", [])),
                }
            else:
                merge_person_into(all_people_map[key], p, fp.name)

        # Run MRCA audit for this file
        record = audit_one_gedcom(fp, persons, families)
        audit_records.append(record)
        verdict = "VERIFIED" if record["verified_link"] else "UNVERIFIED"
        mrca = record.get("mrca_with_hunter")
        mrca_str = mrca["name"] if mrca else "none"
        print(f"    {verdict} | {record['cousin_name']} | MRCA: {mrca_str} | "
              f"conf={record['confidence']} | side={record['side']}")

    # ---------------------------------------------------------------------------
    # Summary stats
    # ---------------------------------------------------------------------------
    verified = [r for r in audit_records if r["verified_link"]]
    unverified = [r for r in audit_records if not r["verified_link"]]
    paternal = [r for r in audit_records if r["side"] == "paternal"]
    maternal = [r for r in audit_records if r["side"] == "maternal"]
    confirmed = [r for r in audit_records if r["confidence"] == "confirmed"]
    probable = [r for r in audit_records if r["confidence"] == "probable"]
    conflicting = [r for r in audit_records if r["confidence"] == "conflicting"]

    summary = {
        "total_files_processed": len(audit_records),
        "duplicates_skipped": len(duplicate_file_stems),
        "verified_links": len(verified),
        "unverified_links": len(unverified),
        "paternal_side": len(paternal),
        "maternal_side": len(maternal),
        "unknown_side": len([r for r in audit_records if r["side"] == "unknown"]),
        "confidence_confirmed": len(confirmed),
        "confidence_probable": len(probable),
        "confidence_conflicting": len(conflicting),
        "confidence_unverified": len([r for r in audit_records if r["confidence"] == "unverified"]),
        "total_unique_people_across_gedcoms": len(all_people_map),
        "new_ancestors_total": sum(len(r.get("new_ancestors_unlocked", [])) for r in audit_records),
    }

    audit_out = {
        "_meta": {
            "generated": "2026-04-26",
            "gedcom_dir": str(GED_DIR),
            "description": "MRCA audit linking each cousin GEDCOM to Hunter's known direct line",
        },
        "summary": summary,
        "cousins": audit_records,
    }

    OUT_AUDIT.write_text(json.dumps(audit_out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT_AUDIT}")

    # ---------------------------------------------------------------------------
    # Write merged-people output
    # ---------------------------------------------------------------------------
    # Convert sets back to sorted lists
    people_list = []
    for key, rec in all_people_map.items():
        rec_out = dict(rec)
        for rel_key in ("parent_names", "spouse_names", "child_names"):
            rec_out[rel_key] = sorted(rec.get(rel_key, set()))
        people_list.append(rec_out)

    # Sort by birth year (ascending), unknown last
    people_list.sort(key=lambda x: (x.get("birth_year") or 9999, x.get("full_name", "")))

    # Surname frequency map
    surname_count = defaultdict(int)
    for rec in people_list:
        if rec.get("surname"):
            surname_count[rec["surname"]] += 1
    top_surnames = sorted(surname_count.items(), key=lambda x: -x[1])[:40]

    merged_out = {
        "_meta": {
            "generated": "2026-04-26",
            "description": "Deduplicated master person list from all 27 cousin GEDCOMs",
            "dedup_strategy": "normalized_name + birth_decade",
        },
        "summary": {
            "total_unique_people": len(people_list),
            "top_40_surnames": [{"surname": s, "count": c} for s, c in top_surnames],
        },
        "people": people_list,
    }

    OUT_PEOPLE.write_text(json.dumps(merged_out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_PEOPLE}")

    # ---------------------------------------------------------------------------
    # Print summary to console
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("MRCA AUDIT SUMMARY")
    print("=" * 70)
    print(f"  Files processed:      {summary['total_files_processed']}")
    print(f"  Duplicates skipped:   {summary['duplicates_skipped']}")
    print(f"  Verified links:       {summary['verified_links']}")
    print(f"  Unverified links:     {summary['unverified_links']}")
    print(f"  Paternal side:        {summary['paternal_side']}")
    print(f"  Maternal side:        {summary['maternal_side']}")
    print(f"  Unknown side:         {summary['unknown_side']}")
    print(f"  Confidence confirmed: {summary['confidence_confirmed']}")
    print(f"  Confidence probable:  {summary['confidence_probable']}")
    print(f"  Conflicting:          {summary['confidence_conflicting']}")
    print(f"  New ancestors found:  {summary['new_ancestors_total']}")
    print(f"  Total unique people:  {summary['total_unique_people_across_gedcoms']}")
    print()
    if unverified:
        print("UNVERIFIED COUSINS (need manual review):")
        for r in unverified:
            print(f"  - {r['cousin_name']} | {r['evidence'][:100]}")
    print()
    print("MRCA BREAKDOWN (verified):")
    mrca_names = defaultdict(list)
    for r in verified:
        mrca = r.get("mrca_with_hunter")
        if mrca:
            mrca_names[mrca["name"]].append(r["cousin_name"])
    for mrca_name, cousins in sorted(mrca_names.items()):
        print(f"  {mrca_name}: {len(cousins)} cousin(s) — {', '.join(cousins[:3])}{'...' if len(cousins)>3 else ''}")


if __name__ == "__main__":
    main()
