"""Enrich entities.json + lineage trees with immigrant + origin-country metadata.

Adds these fields to each entity (and matching tree node by id):
  immigrant_to_america: bool   — first-American ancestor in Hunter's direct line for that surname
  origin_country: str          — country of birth or earliest known origin
  country_flag: str            — emoji flag for the country (used in headers + node badges)
  country_code: str            — ISO 3166 hint (GB-ENG, GB-SCT, US, DE, CZ, etc.)
  is_notable: bool             — flag for star badge on the tree

Detection strategy:
  1. CANONICAL_IMMIGRANTS — known direct-line immigrants per surname (filled as research confirms)
  2. Heuristic detection from fact text + relation_to_shari (looks for "IMMIGRANT", "emigrated", "sailed", "first to America")
  3. Country detection from birth_place + fact text (England/Scotland/Germany/Bohemia/France/etc.)

Run: python scripts/enrich_immigrants_and_origins.py
"""
import json
import re
from pathlib import Path

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENT = WS / "research" / "entities.json"
TREE = WS / "research" / "lineage-tree.json"
MULTI = WS / "research" / "lineage-tree-multi.json"

# ── COUNTRY → FLAG MAP ──────────────────────────────────────────────────────
COUNTRY_FLAGS = {
    "USA": "🇺🇸",
    "United States": "🇺🇸",
    "England": "🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f",
    "Scotland": "🏴\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f",
    "Wales": "🏴\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f",
    "United Kingdom": "🇬🇧",
    "UK": "🇬🇧",
    "Britain": "🇬🇧",
    "Ireland": "🇮🇪",
    "Northern Ireland": "🇬🇧",
    "Germany": "🇩🇪",
    "Prussia": "🇩🇪",
    "Saxony": "🇩🇪",
    "Bavaria": "🇩🇪",
    "Hesse": "🇩🇪",
    "Hessen": "🇩🇪",
    "Württemberg": "🇩🇪",
    "Bohemia": "🇨🇿",
    "Czech Republic": "🇨🇿",
    "Czechia": "🇨🇿",
    "Moravia": "🇨🇿",
    "France": "🇫🇷",
    "Italy": "🇮🇹",
    "Spain": "🇪🇸",
    "Portugal": "🇵🇹",
    "Netherlands": "🇳🇱",
    "Holland": "🇳🇱",
    "Belgium": "🇧🇪",
    "Norway": "🇳🇴",
    "Sweden": "🇸🇪",
    "Denmark": "🇩🇰",
    "Poland": "🇵🇱",
    "Russia": "🇷🇺",
    "Switzerland": "🇨🇭",
    "Austria": "🇦🇹",
    "Hungary": "🇭🇺",
    "Romania": "🇷🇴",
    "Greece": "🇬🇷",
    "Mexico": "🇲🇽",
    "Canada": "🇨🇦",
}

COUNTRY_CODES = {
    "USA": "US", "United States": "US",
    "England": "GB-ENG", "Scotland": "GB-SCT", "Wales": "GB-WLS",
    "United Kingdom": "GB", "UK": "GB", "Britain": "GB",
    "Ireland": "IE", "Northern Ireland": "GB-NIR",
    "Germany": "DE", "Prussia": "DE", "Saxony": "DE", "Bavaria": "DE",
    "Hesse": "DE", "Hessen": "DE", "Württemberg": "DE",
    "Bohemia": "CZ", "Czech Republic": "CZ", "Czechia": "CZ", "Moravia": "CZ",
    "France": "FR", "Italy": "IT", "Spain": "ES", "Portugal": "PT",
    "Netherlands": "NL", "Holland": "NL", "Belgium": "BE",
    "Norway": "NO", "Sweden": "SE", "Denmark": "DK",
    "Poland": "PL", "Russia": "RU",
    "Switzerland": "CH", "Austria": "AT", "Hungary": "HU",
    "Romania": "RO", "Greece": "GR",
    "Mexico": "MX", "Canada": "CA",
}

# ── CANONICAL DIRECT-LINE IMMIGRANTS ────────────────────────────────────────
# These are confirmed (by entity ID) ancestors of Hunter who FIRST set foot in America
# for their respective surname lines. To be expanded as background research agents land.
CANONICAL_IMMIGRANTS = {
    # Mattingly: Thomas Mattingly II — pre-1665, Maryland
    "p039": {
        "surname_line": "Mattingly",
        "departure_country": "England",
        "arrival_year": "pre-1665",
        "arrival_place": "St. Mary's County, Maryland",
        "primary_source": "Mattingly's Hope land patent Sept 4 1666 — Maryland Land Office",
    },
    # Teichmueller: Hans Teichmüller — emigrated 1856, Braunschweig → Fayette County TX
    "p003": {
        "surname_line": "Teichmueller",
        "departure_country": "Germany",
        "departure_place": "Braunschweig (Brunswick), Duchy of Brunswick",
        "arrival_year": "1856",
        "arrival_place": "Fayette County, Texas (via cousin Arthur Meerscheidt)",
        "primary_source": "Neue Deutsche Biographie (NDB) vol. 26, 2016, p. 6",
        "context": "Emigrated 1856 after father August Wilhelm Teichmüller died 1855, leaving family in financial hardship. Became District Judge of the 22nd Judicial District (1884-1901).",
    },
    # Lepick: Frank Lepik (František Lepík) — emigrated 1881, Bohemia → Brown County KS
    "p115": {
        "surname_line": "Lepick",
        "departure_country": "Czech Republic",
        "departure_place": "Frýdek-Místek area, Moravian-Silesian Region (Bohemia/Czech lands of Austria-Hungary, working hypothesis POSSIBLE)",
        "arrival_year": "1881",
        "arrival_place": "Brown County, Kansas (Everest, then Horton)",
        "primary_source": "WikiTree Lepik-8; Forebears.io Lepík surname distribution; KdeJsme.cz village mapping; St. Joseph Catholic Church Everest KS marriage register 13 Jan 1885",
        "context": "Arrived USA alone, age ~19. Shoemaker/boot-maker. Catholic. m. Mary Mikeska 1885. Buried Kennekuk Cemetery, Horton KS. Hunter's maternal 3rd-great-grandfather.",
    },
    # Spence: TBD — Dale Sr's father (the Scottish/MacDuff immigrant) name UNKNOWN.
    #   Best paths: ask Dale Jr OR Texas DSHS birth cert for Dale Sr ($22) OR 1930 Census Jefferson Co TX
    # Byrd: TBD — direct chain back to colonial Virginia immigrant POSSIBLE only; no specific person yet
    # Henslee: TBD — Macksfield Henslee (~1725 VA Colony) is American-born; immigrant is one gen earlier (~1640-1700)
    # Baity: TBD — Charles Beatty (PA 1729 via Filby PILI) is candidate but link to George Baity Sr POSSIBLE only
    # Boehme: TBD — G6 Unknown Boehme (Herman F. Boehme's father) — name unknown, immigration window c.1855-1862
}

# ── EARLIEST-CONFIRMED ORIGIN PER SURNAME LINE (for heritage panel) ─────────
# Filled as research agents confirm primary sources.
LINE_ORIGINS = {
    "Mattingly": {
        "earliest_confirmed_year": 1483,
        "earliest_confirmed_person": "William Mattyngle (Hampshire 1483 — mortgage for 'Rychars land' in Mattingley village)",
        "country": "England",
        "country_subregion": "Hampshire (Mattingley village — the toponym source of the surname)",
        "country_confidence": "confirmed",
        "evidence": "Hampshire Record Office HRO 19M61/153 — mortgage dated 24 March 1483. Pushes confirmed surname presence in the Hampshire village back 65 years from prior research. Y-DNA haplogroup R-Y14084 (unique to all American Mattingly descendants of Thomas I) includes multiple Hampshire, England-origin YFull samples — genetically confirming Hampshire origin.",
        "earliest_probable_year": 1548,
        "earliest_probable_person": "Henry MATYNGLE (m. Heckfield St Michael Hampshire 30 Sept 1548 — Phillimore's Transcript)",
        "immigrant_in_line": "Thomas Mattingly II (received Mattingly's Hope land patent 4 Sept 1666, Charles Co Maryland — Patent Book Liber 10, Maryland State Archives SM2). His father Thomas Mattingly I died shortly after arrival in Maryland, 24 July 1664.",
        "ydna_haplogroup": "R-Y14084 (confirmed Hampshire English origin via YFull)",
        "color_hex": "#dc1d3a",
    },
    "Spence": {
        "earliest_confirmed_year": 1934,
        "earliest_confirmed_person": "Dr. Dale W. Spence Sr. (b. 1934 Beaumont, TX) — direct documentary line. Pre-Dale-Sr generations require finding Dale Sr's father.",
        "country": "Scotland",
        "country_confidence": "confirmed_clan_affiliation",
        "evidence": "Spence/Spens CONFIRMED as a sept of Clan MacDuff in every major Scottish clan register (Electric Scotland, tartans.com, Wikipedia). Clan Spens has its own Lord Lyon King of Arms registration; the 4th Baron Spens (b. 1968) holds 'of Blairsanquhar, County of Fife'. King Robert the Bruce granted the Wormiston estate (Fife) to Clan Spens in 1309 — 'Royal Constables of the Kingdom of East Fife'. Direct genealogical chain to Hunter pending: Dale Sr's father (the immigrant) name still UNKNOWN — best paths: ask Dale Jr OR Texas DSHS birth certificate for Dale Sr ($22) OR 1930 US Census Jefferson Co TX.",
        "clan_affiliation": "Clan MacDuff (Spens sept) — Lowland Scottish",
        "clan_motto": "Si Deus Quis Contra",
        "clan_arms": "Hart's head erased proper (Spens crest); demi-lion Gules holding broadsword (MacDuff crest)",
        "notable_in_line": "Bishop Thomas Spens of Aberdeen (c.1400-1480, Lord Privy Seal of Scotland under James III, effigy at Rosslyn Chapel); Sir James Spens of Wormiston (c.1571-1632, Ambassador to Sweden, descendants became Swedish counts)",
        "color_hex": "#0065bd",  # Scottish blue
    },
    "Byrd": {
        "earliest_confirmed_year": 1832,
        "earliest_confirmed_person": "William Leander Byrd (b. 1832 Frankfort, Franklin Co AL – d. 1889; Confederate Army private; m. Margarete Rhetta Peradeau)",
        "earliest_confirmed_year_status": "PROBABLE — confirmed via burial at Sharp Cemetery Milam Co TX (PeopleLegacy) for his son John A Byrd 1868-1928; parent link probable via cousin GEDCOMs",
        "country": "England",
        "country_confidence": "probable",
        "evidence": "Virginia colonial chain back to 'John Henry Bird fl. ~1700 Westmoreland VA' is POSSIBLE only (cousin GEDCOM, WikiTree profiles flagged as conflations). Hunter's line is NOT the Westover Byrd line (William Byrd of Westover 1652-1704 is from a Cheshire English gentry family, Charles City Co tidewater — confirmed distinct). Hunter's probable Virginia Byrd ancestors are a Spotsylvania/Piedmont cluster.",
        "huguenot_thread": "Margarete Rhetta Peradeau bears a French-Huguenot surname — possible Huguenot ancestry on the maternal Byrd side.",
        "open_questions": "Dovie Byrd's parentage still POSSIBLE only. Top records to unlock: 1910 Milam Co census, Texas death certificate for Dovie Spence, 1850-1860 Franklin Co AL census for William Leander Byrd.",
        "color_hex": "#dc1d3a",
    },
    "Henslee": {
        "earliest_confirmed_year": 1725,
        "earliest_confirmed_person": "Macksfield Henslee (b. ~1725 Hanover Co VA — d. bef. Aug 1801 Caswell Co NC). DAR/SAR qualifying Rev War ancestor.",
        "country": "England",
        "country_confidence": "confirmed",
        "evidence": "Caswell Co NC Will Book D p.70 (will dated 31 Dec 1794, proved Oct Court 1801) names sons John + David. Surname etymologically from Hensley village, East Worlington, Devon. First English record: John de Henselay, Yorkshire Subsidy Rolls 1297.",
        "color_hex": "#dc1d3a",
        "ydna_haplogroup": "I-M253 (FamilyTreeDNA kit #213697)",
    },
    "Baity": {
        "earliest_confirmed_year": 1746,
        "earliest_confirmed_person": "George Baity Sr. (b. 27 Nov 1746 Rowan/Surry Co NC, d. 11 Mar 1828; m. Rachel Allgood)",
        "country": "Ireland",
        "country_subregion": "Ulster Plantation (Counties Down, Tyrone, Cavan) — Scots-Irish ethnic origin",
        "country_confidence": "confirmed_ethnic_origin",
        "evidence": "Scots-Irish ethnic origin — Borders Scottish settlers (Northumberland, Dumfriesshire) moved to Ulster during the Plantation of Ulster (1610-1640), then emigrated to Pennsylvania in the 1720s-30s. Surname evolution in NC records: Batee (1774) → Baty (1785) → Batey (1787) → Beaty (1800) → Baity (standard by 1830). Sources: WikiTree Baity-117, NC Land Grants database, Filby PILI.",
        "immigrant_candidate": "Charles Beatty — arrived Pennsylvania 1729 (Filby PILI); 800-acre joint land grant Rowan County NC 1753. Link to George Baity Sr. is geographically/temporally coherent but POSSIBLE not proved.",
        "color_hex": "#ff883e",  # Ulster orange
    },
    "Lepick": {
        "earliest_confirmed_year": 1862,
        "earliest_confirmed_person": "Frank Lepik / František Lepík (b. ~1862 Czech lands of Austria-Hungary — d. 1939 Horton, Brown Co Kansas; m. Mary Mikeska 1885)",
        "country": "Czech Republic",
        "country_subregion": "Frýdek-Místek area, Moravian-Silesian Region (working hypothesis POSSIBLE — surname clusters 100% in Czech Republic, 82% in Frýdek-Místek/Ostrava corridor)",
        "country_confidence": "confirmed",
        "evidence": "Forebears.io: Lepík has 88 bearers worldwide, 100% in Czech Republic. KdeJsme.cz: 54.5% in Frýdek-Místek, 12.5% in Frýdlant nad Ostravicí, 14.8% in Ostrava. Catholic. WikiTree Lepik-8.",
        "immigrant_in_line": "Frank Lepik arrived USA 1881 at age ~19, alone. Shoemaker. Settled Brown Co Kansas. Buried Kennekuk Cemetery.",
        "notable_relative": "Fred Charles Lepick Jr. (1925-2016) — Naval Aviator, UT Law JD 1950, President of Frost National Bank San Antonio 1981-1988. Hunter's great-great-uncle.",
        "color_hex": "#11457e",  # Czech blue
    },
    "Boehme": {
        "earliest_confirmed_year": 1863,
        "earliest_confirmed_person": "Herman F. Boehme (1863 TX – 1900 Shiner, Lavaca Co TX). Buried Sons of Hermann Cemetery. Probable wife: Minna Marie Macker.",
        "country": "Germany",
        "country_subregion": "Kingdom of Saxony (PROBABLE)",
        "country_confidence": "probable",
        "evidence": "Böhme surname concentrates 34% in Saxony (Forebears.io — highest of any German state). Confirmed collateral immigrant Dr. Friedrich August Boehme (b. 1809 Waldenburg, Landkreis Zwickau, Saxony) emigrated to Castroville, Medina Co TX. Surname etymology: Böhme = ethnic Germans resettled from Bohemia into Saxony post-Thirty Years War. Texas holds 15% of all US Boehme bearers.",
        "immigrant_in_line": "G6 Unknown Boehme (Herman's father) — name unknown, immigration window c.1855-1862, probable entry port Indianola TX, departure Hamburg or Bremen. Path to identify: 1870 Lavaca Co census (NARA M593 roll 1595) for Boehme household with Herman age ~7.",
        "color_hex": "#000000",  # German tricolor — black/red/gold
    },
    "Teichmueller": {
        "earliest_confirmed_year": 1580,
        "earliest_confirmed_person": "Hans/Johann Teichmüller (master miller, c.1580–1638, southern Harz mountains)",
        "country": "Germany",
        "country_region": "Lower Saxony / Saxony-Anhalt borderlands (Harz mining corridor — Goslar, Halberstadt, Rohrsheim, Braunschweig)",
        "country_confidence": "confirmed",
        "evidence": "Neue Deutsche Biographie (NDB) vol. 26, 2016, p. 6 — peer-reviewed German biographical dictionary. Surname is occupational: Teichmüller = 'pond miller'.",
        "immigrant_in_line": "Hans Teichmüller (1837 Braunschweig → 1856 Fayette Co TX)",
        "notable_relative": "Gustav Teichmüller (1832-1888) — Hans's older brother, German philosopher whose perspectivism doctrine directly influenced Nietzsche. Hunter's 3x great-granduncle.",
        "color_hex": "#000000",
    },
    "Rau": {
        "earliest_confirmed_year": None,
        "earliest_confirmed_person": "Frances Virginia Rau (Lee Stuart Henslee's wife)",
        "country": "Germany",
        "country_confidence": "probable",
        "evidence": "Rau is German surname.",
        "color_hex": "#000000",
    },
}


# ── DETECTORS ───────────────────────────────────────────────────────────────
IMMIGRANT_PATTERNS = [
    re.compile(r"\bTHE\s+\w+\s+IMMIGRANT\b", re.I),
    re.compile(r"\bTHE\s+IMMIGRANT\b", re.I),
    re.compile(r"\bMARYLAND\s+IMMIGRANT\b", re.I),
    re.compile(r"\bfirst\s+(?:to\s+)?America\b", re.I),
    re.compile(r"\bemigrated\s+to\s+America\b", re.I),
    re.compile(r"\bemigrated\s+to\s+the\s+(?:colonies|US|United\s+States)\b", re.I),
    re.compile(r"\barrived\s+in\s+(?:Maryland|Virginia|Pennsylvania|New\s+York|Philadelphia|Charleston|Boston|Baltimore|Galveston|New\s+Orleans|Castle\s+Garden|Ellis\s+Island)\b", re.I),
]

# Strong NEGATIVE — record refers to OTHERS as the immigrant, not self
NEGATIVE_IMMIGRANT_PATTERNS = [
    re.compile(r"\bSTAYED\s+in\b", re.I),
    re.compile(r"\bhis\s+son\s+\w*\s*(?:was|is)\s+the\s+(?:actual\s+)?immigrant\b", re.I),
    re.compile(r"\bson\s+\w+\s+was\s+the\s+actual\s+immigrant\b", re.I),
    re.compile(r"\bhis\s+father\s+(?:was|is)\s+the\s+\w*\s*immigrant\b", re.I),
    re.compile(r"\bfather\s+(?:was|is)\s+the\s+(?:English|Scottish|Irish|German|Czech|Bohemian|French|Italian)\s+immigrant\b", re.I),
    re.compile(r"\bgrandson\s+of\s+(?:the\s+)?immigrant\b", re.I),
    re.compile(r"\bdied\s+(?:in|there)\s+\d{4}\s+BEFORE\s+emigrating\b", re.I),
    re.compile(r"\bdied\s+in\s+(?:England|Scotland|Wales|Ireland|Germany|France|Italy|Bohemia)\b", re.I),
    re.compile(r"\bnever\s+came\s+to\s+America\b", re.I),
    # Parenthetical form: "Father (the English immigrant) NAME UNKNOWN"
    re.compile(r"\bFather\s*\(\s*the\s+\w+\s+immigrant\s*\)", re.I),
    re.compile(r"\bMother\s*\(\s*the\s+\w+\s+immigrant\s*\)", re.I),
    # AMERICAN-BORN means NOT an immigrant
    re.compile(r"\bAMERICAN[- ]BORN\b", re.I),
]

COUNTRY_HINT_RE = re.compile(
    r"\b(England|Scotland|Wales|Ireland|Northern\s+Ireland|Germany|Bohemia|Czech\s+Republic|Czechia|Moravia|"
    r"France|Italy|Spain|Portugal|Netherlands|Holland|Belgium|Norway|Sweden|Denmark|Poland|Russia|"
    r"Switzerland|Austria|Hungary|Mexico|Canada|Prussia|Saxony|Bavaria|Hesse|Hessen|Württemberg|Wurttemberg|"
    r"USA|United\s+States|US\b|U\.S\.A\.)\b",
    re.I,
)


def detect_immigrant(person):
    """Return True if entity record looks like a direct-line immigrant to America."""
    text = " ".join([
        person.get("context") or "",
        person.get("relation_to_shari") or "",
        person.get("enriched_context") or "",
        person.get("notes_from_hunter") or "",
    ])
    if any(p.search(text) for p in NEGATIVE_IMMIGRANT_PATTERNS):
        return False
    return any(p.search(text) for p in IMMIGRANT_PATTERNS)


def detect_country(person):
    """Best-guess origin country from birth_place + fact text. Returns canonical key or None."""
    candidates = []
    for fld in ("birth_place", "death_place", "context", "enriched_context", "relation_to_shari", "notes_from_hunter"):
        v = person.get(fld)
        if v:
            candidates.append(v)
    blob = " ".join(candidates)
    m = COUNTRY_HINT_RE.search(blob)
    if not m:
        return None
    raw = m.group(1).strip()
    # Normalize
    upper = raw.upper().replace(".", "").strip()
    if upper in ("US", "USA", "UNITED STATES", "U.S.A.", "U.S."):
        return "USA"
    if upper in ("CZECH REPUBLIC", "CZECHIA"):
        return "Czech Republic"
    if upper.lower() in ("northern ireland",):
        return "Northern Ireland"
    if upper in ("WURTTEMBERG", "WÜRTTEMBERG"):
        return "Germany"
    if upper in ("PRUSSIA", "SAXONY", "BAVARIA", "HESSE", "HESSEN", "BOHEMIA", "MORAVIA"):
        # Sub-region — record under canonical Germany/Czechia for flag, but keep regional name in note
        return upper.title()
    return raw.title()


def main():
    entities = json.loads(ENT.read_text(encoding="utf-8"))

    auto_immigrant_ids = []
    canonical_immigrant_ids = []
    country_assignments = []

    for p in entities.get("people", []):
        pid = p.get("id")

        # IDEMPOTENCE: clear any previously-set immigrant flags so re-running
        # the script always re-derives from current rules.
        p.pop("immigrant_to_america", None)
        p.pop("immigrant_metadata", None)
        p.pop("immigrant_detected_via", None)

        # CANONICAL immigrants — authoritative
        if pid in CANONICAL_IMMIGRANTS:
            cm = CANONICAL_IMMIGRANTS[pid]
            p["immigrant_to_america"] = True
            p["immigrant_metadata"] = cm
            country = cm["departure_country"]
            p["origin_country"] = country
            p["country_flag"] = COUNTRY_FLAGS.get(country, "")
            p["country_code"] = COUNTRY_CODES.get(country, "")
            canonical_immigrant_ids.append(pid)
        else:
            # Heuristic fallback
            if detect_immigrant(p):
                p["immigrant_to_america"] = True
                p["immigrant_detected_via"] = "text_heuristic"
                auto_immigrant_ids.append(pid)
                # Try to fill country if not already set
                country = detect_country(p)
                if country:
                    p["origin_country"] = country
                    p["country_flag"] = COUNTRY_FLAGS.get(country, "")
                    p["country_code"] = COUNTRY_CODES.get(country, "")
            else:
                # Just add origin_country if detectable from birth_place
                country = detect_country(p)
                if country and country != "USA":  # USA-born not "origin" for our purposes
                    p["origin_country"] = country
                    p["country_flag"] = COUNTRY_FLAGS.get(country, "")
                    p["country_code"] = COUNTRY_CODES.get(country, "")
                    country_assignments.append((pid, country))

    # Persist enriched entities
    ENT.write_text(json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[entities] Canonical immigrants tagged: {len(canonical_immigrant_ids)}")
    print(f"  IDs: {canonical_immigrant_ids}")
    print(f"[entities] Auto-detected immigrants: {len(auto_immigrant_ids)}")
    print(f"  IDs: {auto_immigrant_ids[:20]}{'...' if len(auto_immigrant_ids) > 20 else ''}")
    print(f"[entities] Country assignments (non-immigrant origin): {len(country_assignments)}")

    # Build id → fields map for tree injection
    id_meta = {}
    for p in entities.get("people", []):
        if p.get("id"):
            md = {}
            for k in ("immigrant_to_america", "origin_country", "country_flag", "country_code"):
                if p.get(k):
                    md[k] = p[k]
            if md:
                id_meta[p["id"]] = md

    # Inject into trees
    def inject(node):
        if isinstance(node, dict):
            nid = node.get("id")
            if nid and nid in id_meta:
                for k, v in id_meta[nid].items():
                    node[k] = v
            for c in node.get("children", []):
                inject(c)

    if TREE.exists():
        tree_data = json.loads(TREE.read_text(encoding="utf-8"))
        inject(tree_data)
        TREE.write_text(json.dumps(tree_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[tree] Injected immigrant/country metadata into {TREE.name}")

    if MULTI.exists():
        multi_data = json.loads(MULTI.read_text(encoding="utf-8"))
        # multi could be either dict-of-trees or list-of-trees
        if isinstance(multi_data, dict):
            for v in multi_data.values():
                inject(v)
        elif isinstance(multi_data, list):
            for t in multi_data:
                inject(t)
        MULTI.write_text(json.dumps(multi_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[tree] Injected metadata into {MULTI.name}")

    # Write LINE_ORIGINS as a separate JSON for heritage panel + page headers
    origins_out = WS / "research" / "line-origins.json"
    origins_out.write_text(json.dumps({
        "lines": LINE_ORIGINS,
        "country_flags": COUNTRY_FLAGS,
        "country_codes": COUNTRY_CODES,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[origins] Wrote {origins_out.name}")


if __name__ == "__main__":
    main()
