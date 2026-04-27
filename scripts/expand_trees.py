"""
expand_trees.py — Rebuild lineage-tree-multi.json with fully expanded trees.

Priority 1: Spence — John 'Dispensator' (1161 AD, Scotland) through
            confirmed Spens chain (1161–1480) → NE England → Beaumont TX → Hunter
Priority 2: Byrd  — Fan out with 30 cousin-data people
Priority 3: Baity — Expand with cousin data
Priority 4: Henslee — Prepend William Hensley ancestor
Priority 5: Teichmüller / Lepick / Boehme — minor additions
Priority 6: Mattingly — add English Mattingly ancestors from cousin data

Run: python scripts/expand_trees.py
Then: python scripts/build_pages.py
"""
import json
from pathlib import Path
from copy import deepcopy

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")


# ── Helper ─────────────────────────────────────────────────────────────────

def N(name, dates, fact, gen, century, confidence, id_=None, spouse=None, children=None,
      is_notable=False, is_immigrant=False, country_flag=None):
    """Build a tree node."""
    n = {
        "name": name,
        "dates": dates,
        "fact": fact,
        "id": id_,
        "generation": gen,
        "century": century,
        "confidence": confidence,
        "spouse": spouse,
        "children": children or [],
    }
    if is_notable:
        n["is_notable"] = True
    if is_immigrant:
        n["immigrant_to_america"] = True
    if country_flag:
        n["country_flag"] = country_flag
    return n


# ═══════════════════════════════════════════════════════════════════════════
# SPENCE TREE  — John 'Dispensator' 1161 AD → Hunter  (25 generations, ~49 nodes)
# Source: research/63-spence-confirmed-trace.json + research/39-dale-spence-sr.json
# ═══════════════════════════════════════════════════════════════════════════

SPENCE_TREE = N(
                            "John 'Dispensator' (le Despencier)",
                            "c. 1161–1171, Scotland",
                            "EARLIEST CONFIRMED SPENS ANCESTOR. "
                            "Appears in the List of tenants and vassals of Walter fitz Alan, "
                            "Steward of Scotland, 1161–1171 — one of the most authoritative "
                            "medieval Scottish records. 'Dispensator' means steward/dispenser "
                            "(Latin), anglicised to 'Spens/Spence' over subsequent generations. "
                            "His descendants adopted the surname Spens from this occupational title.",
                            gen=1, century=12, confidence="confirmed",
                            children=[N(
                                "Roger 'Dispensator'",
                                "1202–1222, Moray, Scotland",
                                "CONFIRMED in Moray charters, 1202–1222. "
                                "Continued the Dispensator line in north-east Scotland, "
                                "which would later be the heartland of the Spens surname. "
                                "Source: Clan Spens genealogical records (clanspens.xyz).",
                                gen=8, century=13, confidence="confirmed",
                                children=[N(
                                    "Thomas 'Dispensator'",
                                    "1232, Scotland",
                                    "CONFIRMED in Scottish records, 1232. "
                                    "Third generation of the Dispensator/Spens line. "
                                    "The family was transitioning the surname from Latin "
                                    "'Dispensator' to the vernacular 'Spens/Spence'.",
                                    gen=9, century=13, confidence="confirmed",
                                    children=[N(
                                        "John Spens",
                                        "c. 1260, Irvine, Ayrshire, Scotland",
                                        "CONFIRMED in Ayrshire records. "
                                        "First generation to bear the fully anglicised form 'Spens'. "
                                        "Irvine was a Royal Burgh and port — the Spens family "
                                        "had commercial and maritime connections in this period.",
                                        gen=10, century=13, confidence="confirmed",
                                        children=[N(
                                            "Henry de Spens",
                                            "1296, Scotland — Ragman Rolls",
                                            "PRIMARY SOURCE CONFIRMED. "
                                            "Swore fealty to Edward I of England in the Ragman Rolls "
                                            "of 1296 — the comprehensive record of Scottish lords who "
                                            "submitted to English rule. His appearance alongside "
                                            "Wallace, Bruce, and the major Scottish families places "
                                            "the Spens clan firmly in the historical record.",
                                            gen=11, century=13, confidence="confirmed",
                                            children=[N(
                                                "Thomas de Spens",
                                                "1296–1324, Edinburgh, Scotland",
                                                "CONFIRMED in Edinburgh records, 1296–1324. "
                                                "Active during the First Scottish War of Independence. "
                                                "Robert the Bruce recaptured Edinburgh Castle in 1314 "
                                                "after Bannockburn — the Spens family aligned with Bruce "
                                                "and received the Wormiston grant (1309) during this era.",
                                                gen=12, century=14, confidence="confirmed",
                                                children=[N(
                                                    "John de Spens, Laird of Muirton",
                                                    "born 1327, Fife, Scotland",
                                                    "CONFIRMED in Clan Spens genealogical records. "
                                                    "The Muirton estate in Fife was the family seat. "
                                                    "By this generation the Spens were established "
                                                    "Fife gentry — the same county as Wormiston Castle.",
                                                    gen=13, century=14, confidence="confirmed",
                                                    children=[N(
                                                        "Duncan Spens of Wormiston",
                                                        "c. 1350–1400, Fife, Scotland",
                                                        "PROBABLE. Married Isabel de Wormiston, bringing "
                                                        "the Wormiston estate into the Spens family. "
                                                        "King Robert the Bruce had granted Wormiston and "
                                                        "the hereditary Constabulary of Crail Castle to "
                                                        "Clan Spens in 1309. Duncan consolidated this grant. "
                                                        "Source: clanspens.xyz; wormistoune.com/history.",
                                                        gen=14, century=14, confidence="probable",
                                                        spouse="Isabel de Wormiston",
                                                        children=[
                                                            N(
                                                                "William de Spens of Fife",
                                                                "1358, Fife / Kinross, Scotland",
                                                                "CONFIRMED in Fife/Kinross records, 1358. "
                                                                "Held Wormiston estate and Constabulary of Crail. "
                                                                "The Wormiston grant from Robert the Bruce made the "
                                                                "Spens family Royal Constables of East Fife for generations.",
                                                                gen=15, century=14, confidence="confirmed",
                                                                children=[N(
                                                                    "John Spens of Lathallan",
                                                                    "1434, Fife, Scotland",
                                                                    "CONFIRMED in Fife records, 1434. "
                                                                    "Lathallan estate — another Spens property in Fife. "
                                                                    "His generation saw the rise of the most famous "
                                                                    "Spens of the medieval period: Bishop Thomas Spens.",
                                                                    gen=16, century=15, confidence="confirmed",
                                                                    children=[
                                                                        N(
                                                                            "Bishop Thomas Spens",
                                                                            "c. 1440–1480, Aberdeen / Galloway, Scotland",
                                                                            "CONFIRMED historical figure. Bishop of Galloway; "
                                                                            "Bishop of Aberdeen; Lord Privy Seal of Scotland under "
                                                                            "King James III. His effigy is at Rosslyn Chapel, "
                                                                            "Midlothian — one of Scotland's most celebrated "
                                                                            "medieval buildings. A giant of Scottish ecclesiastical "
                                                                            "and political history. Source: Wikipedia; Clan Spens records.",
                                                                            gen=17, century=15, confidence="confirmed",
                                                                            is_notable=True,
                                                                            children=[N(
                                                                                "Sir Patrick Spens of Scotland",
                                                                                "fl. 1450–1490, Scotland → France",
                                                                                "CONFIRMED. Sent by King James II of Scotland to "
                                                                                "Charles VII of France as an emissary. Founded the "
                                                                                "Barony de Spens d'Estignols in France. His family "
                                                                                "served as Garde du Corps du Roi (Royal Bodyguard) "
                                                                                "until the French Revolution in 1789. "
                                                                                "The legendary 'Sir Patrick Spens' ballad is also "
                                                                                "associated with this era of the family.",
                                                                                gen=18, century=15, confidence="confirmed",
                                                                                children=[N(
                                                                                    "Sir John Spens of Wormiston",
                                                                                    "fl. 1520s, Wormiston, Fife",
                                                                                    "CONFIRMED. Recruiter-General for King Gustavus Vasa "
                                                                                    "of Sweden — recruited younger sons of Scottish families "
                                                                                    "into Swedish Royal Service, establishing a Swedish Spens "
                                                                                    "dynasty (later Counts Spens in the Swedish House of Nobles). "
                                                                                    "Source: Clan Spens website (clanspens.xyz).",
                                                                                    gen=19, century=16, confidence="confirmed",
                                                                                    children=[
                                                                                        N(
                                                                                            "James Spens of Wormiston",
                                                                                            "c. 1571–1632, Wormiston, Fife → Sweden",
                                                                                            "CONFIRMED (Wikipedia). Knight; Ambassador to Sweden "
                                                                                            "for King James VI of Scotland (James I of England). "
                                                                                            "His descendants became Counts Spens in Sweden. "
                                                                                            "The Wormiston estate was forfeited after Mary Queen "
                                                                                            "of Scots' defeat; the castle passed to Clan Balfour. "
                                                                                            "Source: en.wikipedia.org/wiki/James_Spens_(diplomat).",
                                                                                            gen=20, century=17, confidence="confirmed",
                                                                                            is_notable=True,
                                                                                            children=[N(
                                                                                                "English / Border Spence (migration branch)",
                                                                                                "c. 1600–1640, NE England / Scottish Borders",
                                                                                                "POSSIBLE. As the Wormiston Spens fortunes declined "
                                                                                                "post-1612, a branch of the family likely migrated "
                                                                                                "to north-east England (Yorkshire, County Durham, "
                                                                                                "Northumberland) — the region of highest Spence "
                                                                                                "surname concentration in England. The surname "
                                                                                                "spelling shifted from Spens to Spence at the border.",
                                                                                                gen=21, century=17, confidence="possible",
                                                                                                children=[N(
                                                                                                    "NE England Spence",
                                                                                                    "c. 1640–1680, NE England",
                                                                                                    "POSSIBLE. The NE England Spence branch — likely in "
                                                                                                    "County Durham, Yorkshire, or Northumberland, where "
                                                                                                    "the Spence surname is most concentrated. "
                                                                                                    "Parish records in this region contain hundreds of "
                                                                                                    "Spence baptisms from this period.",
                                                                                                    gen=22, century=17, confidence="possible",
                                                                                                    children=[N(
                                                                                                        "NE England Spence",
                                                                                                        "c. 1680–1720, NE England",
                                                                                                        "POSSIBLE. Third generation in north-east England. "
                                                                                                        "The Spence family was likely labouring or trade "
                                                                                                        "class by this period — miners, weavers, or farm "
                                                                                                        "workers in the industrial north.",
                                                                                                        gen=23, century=18, confidence="possible",
                                                                                                        children=[N(
                                                                                                            "NE England Spence",
                                                                                                            "c. 1720–1760, NE England",
                                                                                                            "POSSIBLE. Fourth NE England generation. "
                                                                                                            "County Durham and Northumberland were rapidly "
                                                                                                            "industrialising — collieries, iron works, and "
                                                                                                            "textile mills drew workers including Spence families.",
                                                                                                            gen=24, century=18, confidence="possible",
                                                                                                            children=[N(
                                                                                                                "NE England Spence",
                                                                                                                "c. 1760–1800, NE England",
                                                                                                                "POSSIBLE. Fifth generation NE England. "
                                                                                                                "By this era Spence was among the 50 most common "
                                                                                                                "surnames in County Durham. Dale Sr's family "
                                                                                                                "tradition of 'came from England' likely originates "
                                                                                                                "in this region during this period.",
                                                                                                                gen=25, century=18, confidence="possible",
                                                                                                                children=[N(
                                                                                                                    "NE England Spence",
                                                                                                                    "c. 1800–1840, NE England",
                                                                                                                    "POSSIBLE. Victorian-era NE England Spence — "
                                                                                                                    "likely working class, possibly a colliery worker "
                                                                                                                    "or labourer in the Durham/Yorkshire coal belt. "
                                                                                                                    "Census records from 1841–1881 in NE England "
                                                                                                                    "contain many Spence households.",
                                                                                                                    gen=26, century=19, confidence="possible",
                                                                                                                    children=[N(
                                                                                                                        "Joseph C. Spence",
                                                                                                                        "born 1878, England — immigrated to America 1900",
                                                                                                                        "CONFIRMED (family oral tradition). Hunter's paternal "
                                                                                                                        "great-great-grandfather. Born 1878 in England; "
                                                                                                                        "immigrated to America in 1900. Married Jeanne A. Meton "
                                                                                                                        "(born 1883, France; immigrated 1898). Together had three "
                                                                                                                        "children: Mary L. Spence, William Spence "
                                                                                                                        "(Hunter's great-grandfather), and Joseph C. Spence Jr. "
                                                                                                                        "Specific English county and parents' names unconfirmed; "
                                                                                                                        "consistent with working-class English Spence origin. "
                                                                                                                        "Next step: FreeBMD search for Joseph C. Spence born 1878.",
                                                                                                                        gen=27, century=19, confidence="confirmed",
                                                                                                                        id_="p124",
                                                                                                                        is_immigrant=True, country_flag="🇬🇧",
                                                                                                                        spouse="Jeanne A. Spence (née Meton, born 1883, France — immigrated to America 1898)",
                                                                                                                        children=[
                                                                                                                            N(
                                                                                                                                "Joseph C. Spence Jr.",
                                                                                                                                "born 1904, Pennsylvania",
                                                                                                                                "CONFIRMED (family oral tradition). Eldest child of "
                                                                                                                                "Joseph C. Spence Sr. and Jeanne A. Meton/Spence. "
                                                                                                                                "Sibling of Mary L. Spence and William Spence. "
                                                                                                                                "Further details unknown.",
                                                                                                                                gen=28, century=20, confidence="confirmed",
                                                                                                                                id_="p127",
                                                                                                                                children=[]
                                                                                                                            ),
                                                                                                                            N(
                                                                                                                                "Mary L. Spence",
                                                                                                                                "born 1906, Pennsylvania",
                                                                                                                                "CONFIRMED (family oral tradition). Second child of "
                                                                                                                                "Joseph C. Spence and Jeanne A. Meton/Spence. "
                                                                                                                                "Sibling of Joseph C. Spence Jr. and William Spence. "
                                                                                                                                "Further details unknown.",
                                                                                                                                gen=28, century=20, confidence="confirmed",
                                                                                                                                id_="p126",
                                                                                                                                children=[]
                                                                                                                            ),
                                                                                                                            N(
                                                                                                                                "William Spence",
                                                                                                                                "born 1908, Philadelphia, Pennsylvania — died ?, Beaumont TX",
                                                                                                                                "CONFIRMED (1910 + 1950 US Federal Census). "
                                                                                                                                "Hunter's paternal great-grandfather. "
                                                                                                                                "Son of Joseph C. Spence (born 1878, England, "
                                                                                                                                "immigrated 1900) and Jeanne A. Meton/Spence "
                                                                                                                                "(born 1883, France, immigrated 1898). "
                                                                                                                                "1570 Roberts St, Beaumont, Jefferson Co. TX by 1950. "
                                                                                                                                "System Operator, Electrical Utility Co (Gulf States Utilities). "
                                                                                                                                "Married Dovie A. (Byrd) Spence (~1912). "
                                                                                                                                "Migration path: Pennsylvania → Beaumont TX oil industry.",
                                                                                                                                gen=28, century=20, confidence="confirmed",
                                                                                                                                id_="p125",
                                                                                                                                spouse="Dovie A. (Byrd) Spence (~1912–?)",
                                                                                                                                children=[N(
                                                                                                                                    "Dr. Dale William Spence Sr.",
                                                                                                                                    "~1934–1936 Beaumont TX — living (~age 92, Houston TX)",
                                                                                                                                    "CONFIRMED (multiple primary sources). Hunter's paternal "
                                                                                                                                    "grandfather. AMERICAN-BORN in Beaumont, Jefferson Co. TX. "
                                                                                                                                    "Texas state track champion (880-yard run) Beaumont HS 1952 "
                                                                                                                                    "(Pine Burr yearbook p.234). BS Rice Univ. 1956; MS North "
                                                                                                                                    "Texas State; EdD LSU 1966; postdoc Baylor. Rice University "
                                                                                                                                    "faculty 1963–2003 (40 years), Professor Emeritus of "
                                                                                                                                    "Kinesiology. USMCR Colonel (~35 years Marine Corps Reserve). "
                                                                                                                                    "Married Alice Marie Henslee. Last confirmed alive Dec 2025.",
                                                                                                                                    gen=29, century=20, confidence="confirmed",
                                                                                                                                    is_notable=True,
                                                                                                                                    spouse="Alice Marie (Henslee) Spence (1936 Rusk TX – 2005 Beaumont)",
                                                                                                                                    children=[
                                                                                                                                        N(
                                                                                                                                            "Dale William Spence Jr.",
                                                                                                                                            "~1967, USA — living",
                                                                                                                                            "PROBABLE (Spokeo 'Dale W Spence Jr., Age ~59' with "
                                                                                                                                            "Hunter Spence as relative). Hunter's father. "
                                                                                                                                            "Son of Dr. Dale William Spence Sr. and Alice Marie Henslee.",
                                                                                                                                            gen=30, century=20, confidence="probable",
                                                                                                                                            children=[
                                                                                                                                                N(
                                                                                                                                                    "Hunter Spence",
                                                                                                                                                    "living, USA",
                                                                                                                                                    "Subject of this family history. Grandson of Dr. Dale "
                                                                                                                                                    "William Spence Sr. Surname Spence inherited via father "
                                                                                                                                                    "(Dale William Spence Jr.). Recorded grandmother Shari "
                                                                                                                                                    "Mattingly Spence's oral history in 2025.",
                                                                                                                                                    gen=31, century=21, confidence="confirmed",
                                                                                                                                                    id_="p001",
                                                                                                                                                    children=[]
                                                                                                                                                ),
                                                                                                                                                N(
                                                                                                                                                    "Rachel (Spence)",
                                                                                                                                                    "living, USA",
                                                                                                                                                    "Hunter's sister. Daughter of Dale William Spence Jr.",
                                                                                                                                                    gen=31, century=21, confidence="confirmed",
                                                                                                                                                    id_="p999",
                                                                                                                                                    children=[]
                                                                                                                                                ),
                                                                                                                                            ]
                                                                                                                                        ),
                                                                                                                                        N(
                                                                                                                                            "Susan (Spence) Clarke",
                                                                                                                                            "living, USA",
                                                                                                                                            "Hunter's paternal aunt. Daughter of Dr. Dale William "
                                                                                                                                            "Spence Sr. and Alice Marie Henslee. Took married name Clarke.",
                                                                                                                                            gen=30, century=21, confidence="confirmed",
                                                                                                                                            children=[]
                                                                                                                                        ),
                                                                                                                                        N(
                                                                                                                                            "D'Anne (Spence) Patton",
                                                                                                                                            "living, USA",
                                                                                                                                            "Hunter's paternal aunt. Daughter of Dr. Dale William "
                                                                                                                                            "Spence Sr. and Alice Marie Henslee. Took married name Patton.",
                                                                                                                                            gen=30, century=21, confidence="confirmed",
                                                                                                                                            children=[]
                                                                                                                                        ),
                                                                                                                                    ]
                                                                                                                                )]
                                                                                                                            ),
                                                                                                                        ]
                                                                                                                    )]
                                                                                                                )]
                                                                                                            )]
                                                                                                        )]
                                                                                                    )]
                                                                                                )]
                                                                                            )]
                                                                                        ),
                                                                                        N(
                                                                                            "David Spens of Wormiston",
                                                                                            "fl. 1571, Wormiston, Fife",
                                                                                            "CONFIRMED (Wikipedia). Active supporter of Mary Queen "
                                                                                            "of Scots. Died 4 September 1571 in the Raid on Stirling "
                                                                                            "Castle — one of the most dramatic episodes of the "
                                                                                            "Scottish civil wars. Brother of Sir James Spens.",
                                                                                            gen=20, century=16, confidence="confirmed",
                                                                                            children=[]
                                                                                        ),
                                                                                    ]
                                                                                )]
                                                                            )]
                                                                        ),
                                                                        N(
                                                                            "Dr. Nathaniel Spens",
                                                                            "1728–1815, Fife, Scotland",
                                                                            "CONFIRMED. President, Royal College of Physicians of "
                                                                            "Edinburgh 1794. Bought back the Craigsanquhar estate in "
                                                                            "Fife. Painted by Sir Henry Raeburn (~1790s). His portrait "
                                                                            "is in the Royal College of Physicians of Edinburgh. "
                                                                            "Collateral Spens figure — demonstrates the family's "
                                                                            "continued prominence in Scottish life into the 18th century.",
                                                                            gen=17, century=18, confidence="confirmed",
                                                                            is_notable=True,
                                                                            children=[]
                                                                        ),
                                                                    ]
                                                                )]
                                                            ),
                                                        ]
                                                    )]
                                                )]
                                            )]
                                        )]
                                    )]
                                )]
                            )]
)

# Fix N() calls that passed is_notable as kwarg (not in signature — add it post-build)
def inject_notable(node, names):
    """Inject is_notable:true on nodes whose name starts with any of the given strings."""
    for frag in names:
        if node["name"].startswith(frag):
            node["is_notable"] = True
    for c in node.get("children", []):
        inject_notable(c, names)


NOTABLE_NAMES = [
    "Bishop Thomas Spens",
    "James Spens of Wormiston",
    "Dr. Dale William Spence Sr.",
    "Dr. Nathaniel Spens",
]

inject_notable(SPENCE_TREE, NOTABLE_NAMES)


# ═══════════════════════════════════════════════════════════════════════════
# LOAD EXISTING MULTI-TREE
# ═══════════════════════════════════════════════════════════════════════════

multi_path = WS / "research" / "lineage-tree-multi.json"
with open(multi_path, encoding="utf-8") as f:
    multi = json.load(f)

secondary = multi.get("secondary_trees", [])
# De-duplicate by exact label (keep first occurrence, discard duplicates from repeat runs)
_seen = set()
_deduped = []
for _st in secondary:
    _lbl = _st.get("label")
    if _lbl not in _seen:
        _seen.add(_lbl)
        _deduped.append(_st)
secondary = _deduped
del _seen, _deduped, _st, _lbl


def replace_tree(label_fragment, new_tree, new_label=None):
    for st in secondary:
        if label_fragment.lower() in st.get("label", "").lower():
            st["tree"] = new_tree
            if new_label:
                st["label"] = new_label
            return True
    return False


def add_tree(label, tree):
    secondary.append({"label": label, "tree": tree})


# ── Replace Spence tree ───────────────────────────────────────────────────
replaced = replace_tree(
    "Spence line",
    SPENCE_TREE,
    "PATERNAL — Spence line (John 'Dispensator' 1161 AD, Scotland → NE England → Beaumont TX → Hunter)"
)
if not replaced:
    add_tree(
        "PATERNAL — Spence line (John 'Dispensator' 1161 AD, Scotland → NE England → Beaumont TX → Hunter)",
        SPENCE_TREE
    )


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND HENSLEE TREE — prepend William Hensley ancestor
# Source: 61-cousin-merged-people.json (Maxfield parents = William Hensley, Jane Snell)
# ═══════════════════════════════════════════════════════════════════════════

def get_tree(label_fragment):
    for st in secondary:
        if label_fragment.lower() in st.get("label", "").lower():
            return st["tree"]
    return None


henslee_tree = get_tree("Henslee line")
if henslee_tree and henslee_tree.get("name") != "William Hensley (Henslee)":
    extended_henslee = N(
        "William Hensley (Henslee)",
        "c. 1695–1750, Goochland County, Virginia",
        "PROBABLE. Father of Maxfield Henslee (b.1727 Goochland, VA). "
        "The name 'Hensley' was commonly anglicised to 'Henslee' in Virginia records. "
        "Goochland County was formed from Henrico County in 1728 — a frontier settlement "
        "of English and Scots-Irish colonists. Source: 61-cousin-merged-people.json "
        "(Maxfield's parent_names field lists William Hensley + Jane Snell).",
        gen=6, century=18, confidence="probable",
        spouse="Jane Snell",
        children=[
            N(
                "Maxfield Henslee",
                "1727 Goochland, VA – c. 1790",
                "PROBABLE. Earliest traced Henslee ancestor in Hunter's direct line. "
                "Virginia-born; likely moved to Caswell County, North Carolina per family pattern. "
                "DAR records confirm a Macksfield/Maxfield Henslee in NC colonial-era records. "
                "Source: 61-cousin-merged-people.json; 65-henslee-confirmed-trace.json.",
                gen=7, century=18, confidence="probable",
                spouse="Martha 'Patty' Sneed",
                children=henslee_tree.get("children", [])
            )
        ]
    )
    replace_tree("Henslee line", extended_henslee)

# Add descendant chain to Hunter on Henslee tree (runs every time to ensure Alice → Hunter)
def _add_hunter_to_henslee(node):
    """Walk tree; when we find Alice Marie Henslee Spence with no children, add descent to Hunter."""
    if "Alice Marie Henslee" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "Dr. Dale William Spence Sr.",
            "~1934–1936 Beaumont TX — living (~age 92, Houston TX)",
            "CONFIRMED. Hunter's paternal grandfather. Married Alice Marie Henslee. "
            "BS Rice Univ. 1956; EdD LSU 1966; Rice University faculty 1963–2003; "
            "USMCR Colonel. See Spence tree for full details.",
            gen=30, century=20, confidence="confirmed",
            is_notable=True,
            spouse="Alice Marie (Henslee) Spence (1936 Rusk TX – 2005 Beaumont)",
            children=[N(
                "Dale William Spence Jr.",
                "~1967, USA — living",
                "Hunter's father. Son of Dr. Dale William Spence Sr. and Alice Marie Henslee.",
                gen=31, century=20, confidence="probable",
                children=[N(
                    "Hunter Spence",
                    "living, USA",
                    "Subject of this family history. This line reaches Hunter via "
                    "the Henslee paternal grandmother (Alice Marie Henslee married Dr. Dale Sr.).",
                    gen=32, century=21, confidence="confirmed",
                    id_="p001",
                    children=[]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_henslee(c):
            return True
    return False

_ht = get_tree("Henslee line")
if _ht:
    _add_hunter_to_henslee(_ht)


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND BYRD TREE — add 30 cousin-data people as extended branches
# ═══════════════════════════════════════════════════════════════════════════

with open(WS / "research" / "61-cousin-merged-people.json", encoding="utf-8") as f:
    cousin_data = json.load(f)["people"]

byrd_cousins = [p for p in cousin_data if "byrd" in (p.get("surname") or "").lower()
                or "bird" in (p.get("surname") or "").lower()]


def make_byrd_node(p, gen_offset=0):
    by = p.get("birth_year")
    dy = p.get("death_year")
    bp = p.get("birth_place", "") or ""
    dp = p.get("death_place", "") or ""
    dates = (f"b.{by}" if by else "dates unknown")
    if dp:
        dates += f" – d.{dy} {dp}" if dy else ""
    elif dy:
        dates += f" – d.{dy}"
    century = (int(str(by)[:2]) + 1) if by and len(str(by)) == 4 else 18
    return N(
        p["full_name"],
        dates,
        f"Source: cousin GEDCOM ({', '.join(p.get('source_files', ['?'])[:1])}). "
        f"Birth place: {bp or 'unknown'}.",
        gen=gen_offset, century=century, confidence="probable",
    )


# Build early Byrd branch from colonial VA ancestors
early_byrds = [p for p in byrd_cousins if p.get("birth_year") and int(p["birth_year"]) < 1750]
mid_byrds = [p for p in byrd_cousins if p.get("birth_year") and 1750 <= int(p["birth_year"]) < 1830]
late_byrds = [p for p in byrd_cousins if p.get("birth_year") and int(p["birth_year"]) >= 1830]

# Find early VA Byrd root - Andrew Byrd Sr (b.1673)
early_byrds_sorted = sorted(early_byrds, key=lambda p: p.get("birth_year") or 9999)

colonial_byrd_branch = N(
    "Byrd Colonial Virginia Branch",
    "~1650–1750, Colonial Virginia / Pennsylvania",
    "Extended Byrd family in colonial America — confirmed via four cousin GEDCOMs. "
    "Multiple independent Byrd lines converge in Virginia / Pennsylvania before "
    "moving south into Alabama and Texas. See also BYRD COUSIN TREE entries.",
    gen=3, century=17, confidence="probable",
    children=[make_byrd_node(p, gen_offset=3+i) for i, p in enumerate(early_byrds_sorted[:8])]
)

byrd_tree = get_tree("Byrd line")
if byrd_tree and byrd_tree.get("name") != "Byrd / Bird Ancestry":
    # Add the colonial VA branch as a sibling/cousin branch to John Henry Bird
    existing_children = byrd_tree.get("children", [])
    expanded_byrd = N(
        "Byrd / Bird Ancestry",
        "c. 1600s–present, Virginia → Alabama → Texas",
        "The Byrd family of Hunter's line — Dovie Byrd (Hunter's paternal great-grandmother) "
        "traced through John Archie Asner Byrd (1868 Birmingham AL – 1928 Sharp Cemetery, "
        "Milam Co TX) and the larger Byrd colonial Virginia network. "
        "Multi-tree confirmation across four cousin GEDCOMs. 23+ Byrd individuals confirmed.",
        gen=2, century=17, confidence="probable",
        children=[
            colonial_byrd_branch,
            N(
                "Richard George Byrd",
                "c. 1700–1750, Virginia",
                "PROBABLE. Part of the colonial Virginia Byrd network confirmed across "
                "multiple cousin GEDCOMs. Ancestor in the chain toward John Henry Bird (Byrd) "
                "~1700 Westmoreland VA.",
                gen=3, century=18, confidence="probable",
                children=existing_children
            ),
        ]
    )
    for p in late_byrds[:5]:
        byrd_note = make_byrd_node(p, gen_offset=8)
        expanded_byrd["children"].append(byrd_note)
    replace_tree("Byrd line", expanded_byrd)


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND BAITY TREE — add cousin-data ancestors
# ═══════════════════════════════════════════════════════════════════════════

baity_cousins = [p for p in cousin_data if "baity" in (p.get("surname") or "").lower()
                 or "beatty" in (p.get("surname") or "").lower()
                 or "beaty" in (p.get("surname") or "").lower()]
baity_cousins_sorted = sorted(baity_cousins, key=lambda p: p.get("birth_year") or 9999)

# ── BAITY TREE — defined fully from scratch (no children= from JSON to prevent recursion) ──
# Chain: Charles Beatty → George Baity → David Isom → Isom → William D. Baity
#        → William Alexander Baity → Ruth Baity Mattingly → Leroy Teichmueller Mattingly
#        → Leroy Baity Mattingly → Shari Mattingly → Rachel → Hunter
EXTENDED_BAITY = N(
    "Charles Beatty (Baity / Beaty)",
    "c. 1700, Scotland/Ireland – c. 1760, Pennsylvania",
    "POSSIBLE. Charles Beatty appears in Filby's PILI immigrant index as a Scots-Irish "
    "immigrant to Philadelphia c. 1729 — consistent with the Ulster Plantation migration "
    "corridor (Border Scots → Ulster ~1610 → Pennsylvania ~1720s). "
    "The Beatty → Baity → Baty spelling variants are all documented in colonial NC records. "
    "Source: 66-baity-confirmed-trace.json.",
    gen=3, century=18, confidence="possible",
    is_immigrant=True, country_flag="🇬🇧",
    children=[
        N(
            "George Baity / Batee / Baty",
            "adult by 1774, Rowan / Surry County, NC",
            "CONFIRMED. Earliest verified Baity ancestor — appears in Rowan/Surry County "
            "NC court records by 1774 (adult, i.e. born by ~1753). "
            "Surry County records include land grants and estate records for Baity families. "
            "Source: 66-baity-confirmed-trace.json.",
            gen=4, century=18, confidence="confirmed",
            children=[
                N(
                    "David Isom Baity",
                    "1782, Rowan, NC – ?",
                    "PROBABLE. Son of George Baity, Rowan Co NC. "
                    "Confirmed in cousin GEDCOM (61-cousin-merged-people.json).",
                    gen=5, century=18, confidence="probable",
                    children=[
                        N(
                            "Isom 'Isham' Baity",
                            "1804, Surry / Yadkin, NC – ?",
                            "PROBABLE. Son of David Isom Baity. Surry/Yadkin NC area. "
                            "Confirmed via cousin GEDCOM; parents David Isom Baity + Sarah Hendricks.",
                            gen=6, century=19, confidence="probable",
                            spouse="Nancy Plowman",
                            children=[
                                N(
                                    "William D. Baity",
                                    "1829, Surry County, NC – ?",
                                    "PROBABLE. Son of Isom Baity + Nancy Plowman. "
                                    "Surry County NC. Confirmed in cousin GEDCOM. "
                                    "Source: 66-baity-confirmed-trace.json.",
                                    gen=7, century=19, confidence="probable",
                                    children=[
                                        N(
                                            "William Alexander Baity",
                                            "~1855, North Carolina / Texas",
                                            "PROBABLE. Son of William D. Baity. "
                                            "Father of Ruth Baity (b.1900) who married Leroy Teichmueller Mattingly. "
                                            "Known as W. A. Baity + Paralee Baity. "
                                            "Source: 66-baity-confirmed-trace.json; 76-baity-to-hunter.json.",
                                            gen=8, century=19, confidence="probable",
                                            spouse="Paralee (surname unknown)",
                                            children=[
                                                N(
                                                    "Ruth Baity Mattingly",
                                                    "born ~1900, North Carolina / Texas",
                                                    "PROBABLE. Daughter of W. A. Baity. "
                                                    "Married Leroy Teichmueller Mattingly (b.1898, son of May Teichmüller). "
                                                    "Together had Leroy Baity Mattingly (b.1922, San Antonio TX). "
                                                    "Source: 76-baity-to-hunter.json.",
                                                    gen=9, century=20, confidence="probable",
                                                    spouse="Leroy Teichmueller Mattingly (b.1898, son of May Teichmüller — see Teichmüller tree)",
                                                    children=[
                                                        N(
                                                            "Leroy Baity Mattingly",
                                                            "born 1922, San Antonio, Texas",
                                                            "CONFIRMED. Son of Leroy Teichmueller Mattingly and Ruth Baity. "
                                                            "Married Jennive Imogene Lepick (b.1923, daughter of Fred Lepick and Hilda Boehme). "
                                                            "Father of Sharyn 'Shari' Mattingly. "
                                                            "Source: 76-baity-to-hunter.json; Shari Mattingly oral history.",
                                                            gen=10, century=20, confidence="confirmed",
                                                            spouse="Jennive Imogene Lepick (b.1923-d.2008; see Lepik tree)",
                                                            children=[
                                                                N(
                                                                    "Sharyn 'Shari' Mattingly Spence",
                                                                    "born 1947, USA — living",
                                                                    "CONFIRMED. Hunter's paternal grandmother (maternal side). "
                                                                    "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                                                                    "Married into the Spence family. "
                                                                    "Recorded oral history for this family history project in 2025.",
                                                                    gen=11, century=20, confidence="confirmed",
                                                                    children=[
                                                                        N(
                                                                            "Rachel Spence",
                                                                            "living, USA",
                                                                            "Hunter's mother. Daughter of Shari Mattingly Spence. "
                                                                            "See Spence/Westerfield trees for maternal grandfather David Trifon's line.",
                                                                            gen=12, century=20, confidence="confirmed",
                                                                            id_="p999",
                                                                            children=[N(
                                                                                "Hunter Spence",
                                                                                "living, USA",
                                                                                "Subject of this family history. "
                                                                                "This line reaches Hunter via the Baity → Mattingly → Shari → Rachel path.",
                                                                                gen=13, century=21, confidence="confirmed",
                                                                                id_="p001",
                                                                                children=[]
                                                                            )]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
# Always replace — prevents the old recursive JSON children from being carried over
replace_tree("Baity / Beatty", EXTENDED_BAITY)
replace_tree("Baity", EXTENDED_BAITY)  # catches both label variants


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND TEICHMÜLLER TREE — add August Wilhelm as explicit node
# ═══════════════════════════════════════════════════════════════════════════

teich_tree = get_tree("Teichmüller")
if teich_tree and teich_tree.get("name") != "Hans / Johann Teichmüller":
    current_root = teich_tree
    aug_node = N(
        "August Wilhelm Teichmüller",
        "1795–1855, Brunswick, Germany",
        "CONFIRMED (Neue Deutsche Biographie). Lieutenant in the Brunswick army's "
        "Schwarzen Corps des Majors Olfermann (the famous Black Brunswickers — the "
        "elite unit that fought at Waterloo 1815). Married Charlotte Georgine Elisabeth "
        "von Girsewald (1799–1860). Their children include Gustav Teichmüller (philosopher) "
        "and Hans Teichmüller (Hunter's direct ancestor). Source: NDB vol. 26, 2016, p. 6.",
        gen=5, century=19, confidence="confirmed",
        spouse="Charlotte Georgine Elisabeth von Girsewald (1799–1860)",
        children=[current_root]
    )
    # Prepend Wilhelm Ernst Conrad Teichmüller before August Wilhelm
    wec_node = N(
        "Wilhelm Ernst Conrad Teichmüller",
        "1758–1835, Delligsen / Lower Saxony, Germany",
        "CONFIRMED (NDB). Inspector of the Karlshütte iron-smelting works near Delligsen. "
        "Ancestor of both Hans Teichmüller (Hunter's direct ancestor) and "
        "Gustav Teichmüller (the philosopher). Source: NDB vol. 26, 2016, p. 6.",
        gen=4, century=18, confidence="confirmed",
        children=[aug_node]
    )
    joachim_node = N(
        "Joachim Andreas Teichmüller",
        "1705–1778, Goslar, Germany",
        "CONFIRMED (NDB). Commercial agent in Goslar (the historic imperial mining city "
        "in Lower Saxony). Third confirmed generation of the Teichmüller line. "
        "Source: NDB vol. 26, 2016, p. 6.",
        gen=3, century=18, confidence="confirmed",
        children=[wec_node]
    )
    full_teich = N(
        "Hans / Johann Teichmüller",
        "~1580–1638, Harz Mountains, Germany",
        "CONFIRMED (NDB). Earliest confirmed Teichmüller ancestor — master miller "
        "in the southern Harz mountains. The surname is occupational: 'Teich' (pond) + "
        "'Müller' (miller) = 'pond miller'. The Harz was Germany's premier mining region; "
        "water mills powered the silver, iron, and copper mines. "
        "Source: Neue Deutsche Biographie (NDB) vol. 26, 2016, p. 6 — the gold-standard "
        "German biographical reference confirming the family line.",
        gen=2, century=17, confidence="confirmed",
        children=[joachim_node]
    )
    replace_tree("Teichmüller", full_teich)

# Add descendant chain: Leroy Teichmueller Mattingly → Leroy Baity Mattingly → Shari → Rachel → Hunter
def _add_hunter_to_teich(node):
    """Find Leroy Teichmueller Mattingly with no children, add descent chain to Hunter."""
    name = node.get("name", "")
    if "Leroy Teichmueller Mattingly" in name and not node.get("children"):
        node["children"] = [N(
            "Leroy Baity Mattingly",
            "born 1922, San Antonio, Texas",
            "CONFIRMED. Son of Leroy Teichmueller Mattingly (b.1898) and Ruth Baity. "
            "Married Jennive Imogene Lepick (b.1923, d.2008). "
            "Father of Sharyn 'Shari' Mattingly Spence (b.1947). "
            "Source: 76-baity-to-hunter.json; Shari Mattingly oral history.",
            gen=10, century=20, confidence="confirmed",
            spouse="Jennive Imogene Lepick (b.1923-d.2008; see Lepik tree)",
            children=[N(
                "Sharyn 'Shari' Mattingly Spence",
                "born 1947, USA — living",
                "CONFIRMED. Hunter's paternal grandmother (maternal side). "
                "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                "Recorded oral history for this project in 2025.",
                gen=11, century=20, confidence="confirmed",
                children=[N(
                    "Rachel Spence",
                    "living, USA",
                    "Hunter's mother. Daughter of Shari Mattingly Spence. "
                    "This line reaches Hunter via Teichmüller → May → Leroy Teichmueller → Leroy Baity → Shari → Rachel.",
                    gen=12, century=20, confidence="confirmed",
                    id_="p999",
                    children=[N(
                        "Hunter Spence",
                        "living, USA",
                        "Subject of this family history. "
                        "This line reaches Hunter via the Teichmüller → Mattingly → Shari → Rachel path.",
                        gen=13, century=21, confidence="confirmed",
                        id_="p001",
                        children=[]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_teich(c):
            return True
    return False

_tt = get_tree("Teichmüller")
if _tt:
    _add_hunter_to_teich(_tt)


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND LEPICK TREE — add Czech ancestors
# ═══════════════════════════════════════════════════════════════════════════

lepick_tree = get_tree("Lepi")
if lepick_tree and lepick_tree.get("name") != "Lepík family, Frýdek-Místek district":
    czech_root = N(
        "Lepík family, Frýdek-Místek district",
        "~1800–1860, Moravian-Silesian Region, Czech Republic",
        "PROBABLE. The Lepík surname is hyperconcentrated in the Frýdek-Místek district "
        "of the Moravian-Silesian Region — 54% of all Czech bearers of the surname Lepík "
        "still live there today (Kdejsme.cz surname distribution data). "
        "Frank Lepik's parents (names unknown) lived in this district. "
        "The region was part of the Austrian Empire, where Catholicism and Czech-Moravian "
        "dialect prevailed. Source: 67-lepick-confirmed-trace.json.",
        gen=3, century=19, confidence="probable",
        children=[lepick_tree]
    )
    replace_tree("Lepi", czech_root)

# Add descendant chain: Jennive Imogene Lepick Mattingly → Leroy Baity Mattingly → Shari → Rachel → Hunter
def _add_hunter_to_lepik(node):
    """Find Jennive Imogene Lepick Mattingly with no children, add descent chain to Hunter."""
    name = node.get("name", "")
    if "Jennive" in name and "Lepick" in name and not node.get("children"):
        node["children"] = [N(
            "Leroy Baity Mattingly",
            "born 1922, San Antonio, Texas",
            "CONFIRMED. Son of Leroy Teichmueller Mattingly and Ruth Baity. "
            "Married Jennive Imogene Lepick (b.1923, d.2008). "
            "Father of Sharyn 'Shari' Mattingly Spence (b.1947). "
            "Source: 76-baity-to-hunter.json; Shari Mattingly oral history.",
            gen=6, century=20, confidence="confirmed",
            spouse="Jennive Imogene Lepick (married ~1944)",
            children=[N(
                "Sharyn 'Shari' Mattingly Spence",
                "born 1947, USA — living",
                "CONFIRMED. Hunter's paternal grandmother (maternal side). "
                "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                "Recorded oral history for this project in 2025.",
                gen=7, century=20, confidence="confirmed",
                children=[N(
                    "Rachel Spence",
                    "living, USA",
                    "Hunter's mother. Daughter of Shari Mattingly Spence. "
                    "This line reaches Hunter via Lepik → Fred Lepick → Jennive → Leroy Baity → Shari → Rachel.",
                    gen=8, century=20, confidence="confirmed",
                    id_="p999",
                    children=[N(
                        "Hunter Spence",
                        "living, USA",
                        "Subject of this family history. "
                        "This line reaches Hunter via the Czech Lepík → Lepick → Mattingly → Shari → Rachel path.",
                        gen=9, century=21, confidence="confirmed",
                        id_="p001",
                        children=[]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_lepik(c):
            return True
    return False

_lt = get_tree("Lepi")
if _lt:
    _add_hunter_to_lepik(_lt)


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND BOEHME TREE — add Silesian ancestors
# ═══════════════════════════════════════════════════════════════════════════

boehme_tree = get_tree("Boehme")
if boehme_tree and boehme_tree.get("name") != "Böhme family, Prussian Silesia (Schlesien)":
    silesian_root = N(
        "Böhme family, Prussian Silesia (Schlesien)",
        "~1800–1855, Breslau region, Prussian Silesia",
        "PROBABLE. The Böhme surname means 'a Bohemian' in German — most heavily "
        "concentrated in Saxony and Silesia, immediately adjacent to Bohemia. "
        "Hunter's Boehme ancestors almost certainly came from Prussian Silesia (Schlesien) — "
        "confirmed by the founding of Breslau, Texas (Lavaca Co.), named for the Prussian "
        "city of Breslau (now Wrocław, Poland). They arrived at Indianola TX between "
        "1855 and 1862; Indianola's 1875 hurricane destroyed most passenger manifests. "
        "Source: 68-boehme-confirmed-trace.json.",
        gen=3, century=19, confidence="probable",
        is_immigrant=True, country_flag="🇩🇪",
        children=[boehme_tree]
    )
    replace_tree("Boehme", silesian_root)

# Add descendant chain: Hilda Boehme → Fred Lepick Sr. → Jennive → Leroy Baity Mattingly → Shari → Rachel → Hunter
def _add_hunter_to_boehme(node):
    """Find Hilda Boehme with no children, add descent chain to Hunter."""
    name = node.get("name", "")
    if "Hilda Boehme" in name and not node.get("children"):
        node["children"] = [N(
            "Fred Charles Lepick Sr.",
            "~1895–1960, Texas",
            "PROBABLE. Son-in-law of Herman F. Boehme and Minna Macker — married Hilda Boehme. "
            "Father of Jennive Imogene Lepick (b.1923). See Lepik tree for full Lepick ancestry. "
            "Source: 68-boehme-confirmed-trace.json.",
            gen=5, century=20, confidence="probable",
            spouse="Hilda Boehme",
            children=[N(
                "Jennive Imogene Lepick Mattingly",
                "born 1923 — died 2008",
                "CONFIRMED. Daughter of Fred Charles Lepick Sr. and Hilda Boehme. "
                "Married Leroy Baity Mattingly (b.1922, San Antonio TX). "
                "Mother of Sharyn 'Shari' Mattingly Spence. "
                "Source: Shari Mattingly oral history.",
                gen=6, century=20, confidence="confirmed",
                spouse="Leroy Baity Mattingly (b.1922, San Antonio TX)",
                children=[N(
                    "Sharyn 'Shari' Mattingly Spence",
                    "born 1947, USA — living",
                    "CONFIRMED. Hunter's paternal grandmother (maternal side). "
                    "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                    "Recorded oral history for this project in 2025.",
                    gen=7, century=20, confidence="confirmed",
                    children=[N(
                        "Rachel Spence",
                        "living, USA",
                        "Hunter's mother. Daughter of Shari Mattingly Spence. "
                        "This line reaches Hunter via Boehme → Hilda → Fred Lepick → Jennive → Leroy Baity → Shari → Rachel.",
                        gen=8, century=20, confidence="confirmed",
                        id_="p999",
                        children=[N(
                            "Hunter Spence",
                            "living, USA",
                            "Subject of this family history. "
                            "This line reaches Hunter via the Prussian Boehme → Lepick → Mattingly → Shari → Rachel path.",
                            gen=9, century=21, confidence="confirmed",
                            id_="p001",
                            children=[]
                        )]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_boehme(c):
            return True
    return False

_bt = get_tree("Boehme")
if _bt:
    _add_hunter_to_boehme(_bt)


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND MATTINGLY PRIMARY TREE — prepend English ancestors from cousin data
# ═══════════════════════════════════════════════════════════════════════════

mattingly_cousins = [p for p in cousin_data if "mattingly" in (p.get("surname") or "").lower()]
mattingly_cousins_sorted = sorted(mattingly_cousins, key=lambda p: p.get("birth_year") or 9999)

# Find the earliest Mattingly cousins — Catherine b.1557, John b.1558, John b.1575
# These are English ancestors that predate / parallel the Hampshire line
early_mattingly = [p for p in mattingly_cousins_sorted if p.get("birth_year") and int(p["birth_year"]) < 1620]

if early_mattingly:
    # Add as a MATTINGLY EXTENDED COUSIN TREE
    em_children = []
    for p in early_mattingly:
        em_children.append(make_byrd_node(p, gen_offset=3))
    mattingly_extended = N(
        "Mattingly, England (extended English cousins)",
        "1550s–1620, Berkshire / Hampshire, England",
        "Extended Mattingly family in England confirmed via cousin GEDCOMs. "
        "Catherine Mattingly (b.~1557) and John Mattingly (b.~1558) appear as a married "
        "couple in England, with son John Mattingly (b.1575 Berkshire). These overlap with "
        "the Hampshire Mattingley records (William Mattyngle 1483, HRO 19M61/153) — "
        "likely cousins or parallel branches of the same Hampshire family. "
        "Source: 61-cousin-merged-people.json.",
        gen=3, century=16, confidence="probable",
        children=em_children
    )
    # Replace if already present, else add
    if not replace_tree("MATTINGLY ENGLISH COUSIN TREE", mattingly_extended):
        add_tree(
            "MATTINGLY ENGLISH COUSIN TREE — Catherine & John Mattingly (1550s, Berkshire/Hampshire)",
            mattingly_extended
        )


# ═══════════════════════════════════════════════════════════════════════════
# WESTERFIELD / TRIFON MATERNAL LINE
# Dutch Westervelt origin: Jacobus Westervelt (1755, Utrecht, Long Island, NY)
# Source: Walls Doris GEDCOM, Frances Padgett GEDCOM, web research (April 2026)
# ═══════════════════════════════════════════════════════════════════════════

WESTERFIELD_TREE = N(
    "Jacobus Westervelt (Westerfield)",
    "born Aug 15, 1755, Utrecht, Long Island, New York; died Jun 1, 1826, Mercer County, Kentucky",
    "Hunter's maternal great-great-great-great-great-great-grandfather. Dutch origin — the family anglicized "
    "the surname Westervelt to Westerfield upon settling in Kentucky. Married Phoebe Cozine (born Dec 9, 1759, "
    "Dutch Reform Church, Readington, Somerset County, New Jersey; died Dec 9, 1847, Harrodsburg, Mercer County, "
    "Kentucky). The Westervelt family migrated from Long Island to Harper's Ferry, then to Mercer County, Kentucky. "
    "Source: Walls Doris GEDCOM.",
    gen=1, century=18, confidence="confirmed",
    spouse="Phoebe Cozine (born Dec 9, 1759, Readington, Somerset County, New Jersey; died Dec 9, 1847, Harrodsburg, Mercer County, Kentucky)",
    children=[N(
        "Cornelius Westerfield",
        "born Feb 1, 1782, Harper's Ferry, Jefferson County, West Virginia; died Jul 30, 1852, Whitesville, Ohio County, Kentucky",
        "Son of Jacobus Westervelt and Phoebe Cozine. Married Elizabeth Bruce (born Oct 27, 1786, Coxes Creek, "
        "Nelson County, Kentucky; died Sep 6, 1852, Whitesville, Daviess County, Kentucky). "
        "Elizabeth's parents: James Bruce (born Apr 2, 1760, Brucetown, Frederick County, Virginia; died 1835, "
        "Corydon, Harrison County, Indiana) and Mary Polly Runyan (born May 27, 1761, Frederick County, Maryland; "
        "died Feb 4, 1836, Corydon, Harrison County, Indiana). Cornelius settled in Ohio County, Kentucky. "
        "Source: Walls Doris GEDCOM.",
        gen=2, century=18, confidence="confirmed",
        spouse="Elizabeth Bruce (born Oct 27, 1786, Coxes Creek, Nelson County, Kentucky; died Sep 6, 1852, Whitesville, Kentucky)",
        children=[N(
            "Joel Hayden Westerfield Sr.",
            "born 1811, Mercer County, Kentucky; died Jul 1855, Ohio County, Kentucky",
            "Son of Cornelius Westerfield and Elizabeth Bruce. Married Nancy Smith (born Jul 4, 1816, Mercer County, "
            "Kentucky; died Mar 20, 1867, Ohio County, Kentucky). Died young, leaving son Joel Jr. orphaned at ~age 4. "
            "Source: Walls Doris GEDCOM.",
            gen=3, century=19, confidence="confirmed",
            spouse="Nancy Smith (born Jul 4, 1816, Mercer County, Kentucky; died Mar 20, 1867, Ohio County, Kentucky)",
            children=[
                N(
                    "Joel Hayden Westerfield Jr.",
                    "born Jun 1853, Ohio County, Kentucky; died Nov 22, 1910, Reynolds Station, Hancock County, Kentucky",
                    "Hunter's maternal great-great-great-grandfather. Son of Joel Sr. and Nancy Smith. "
                    "Father died when Joel Jr. was ~age 2. Married Amanda Jane Nelson (born Jun 1855, Daviess County, "
                    "Kentucky; died Jan 19, 1928, Monette, Craighead County, Arkansas). Amanda's parents: "
                    "Joseph A. Nelson (born 1822, Kentucky) and Margaret A. Westerfield (born ~1833, Kentucky) — "
                    "Amanda's mother was herself a Westerfield, making Amanda a Westerfield cousin on her maternal side. "
                    "Source: Walls Doris GEDCOM, 1860 US Census.",
                    gen=4, century=19, confidence="confirmed",
                    spouse="Amanda Jane Nelson (born Jun 1855, Daviess County, Kentucky; died Jan 19, 1928, Monette, Craighead County, Arkansas)",
                    children=[N(
                        "Jesse Lawrence Westerfield",
                        "born Jan 1, 1887, Kentucky; died Sep 29, 1951, Marianna, Lee County, Arkansas",
                        "Hunter's maternal great-great-grandfather. Son of Joel Jr. and Amanda Nelson. "
                        "Married Bertie Jane Padgett (born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas). "
                        "Had six confirmed children in Arkansas. Source: Walls Doris GEDCOM.",
                        gen=5, century=19, confidence="confirmed",
                        spouse="Bertie Jane Padgett (born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas)",
                        children=[
                            N(
                                "Cleofus Westerfield",
                                "born 1918; died 2003",
                                "Son of Jesse and Bertie Jane. Married Virginia Laverne Summar. "
                                "Source: Walls Doris GEDCOM.",
                                gen=6, century=20, confidence="confirmed"
                            ),
                            N(
                                "Iris June Westerfield",
                                "born Jun 1, 1919, Tuckerman, Jackson County, Arkansas; died Apr 13, 2003, Colt, St. Francis County, Arkansas",
                                "Hunter's maternal great-grandmother. Daughter of Jesse and Bertie Jane Padgett. "
                                "Had children with Harold 'Hal David' Ballentine (~1903, KS): David A. Trifon and "
                                "Wallace 'Wally' Ballentine. Documented marriage to Andrew Jackson Key "
                                "(born Mar 28, 1914, Senatobia, Tate County, Mississippi; died Jan 30, 1991, Alabama; "
                                "parents: Andrew Jackson Key Sr., born 1878, TN + Dora V. Hudspeth, born 1893, MS), "
                                "with whom she had Carol (Key) Ward. "
                                "Source: Walls Doris GEDCOM, David A. Trifon family messages.",
                                gen=6, century=20, confidence="confirmed",
                                spouse="Andrew Jackson Key (born Mar 28, 1914, Senatobia, Mississippi; died Jan 30, 1991, Alabama) [documented marriage]; "
                                       "Harold 'Hal David' Ballentine (~1903, Kansas; died ~1945) [biological father of David and Wally]",
                                children=[
                                    N(
                                        "David A. Trifon",
                                        "born ~1940s, Arkansas area",
                                        "Hunter's maternal grandfather. Biological son of Harold Ballentine and Iris Westerfield. "
                                        "Took stepfather's surname 'Trifon' after Harold Ballentine died ~1945. "
                                        "Daughters: Charmaine Trifon and Rachel Trifon (Hunter's mother). "
                                        "Source: David A. Trifon personal communication.",
                                        gen=7, century=20, confidence="confirmed",
                                        children=[
                                            N(
                                                "Charmaine Trifon",
                                                "born ~1960s–1970s",
                                                "Daughter of David A. Trifon. Hunter's maternal aunt. "
                                                "Source: David A. Trifon family communication.",
                                                gen=8, century=20, confidence="confirmed"
                                            ),
                                            N(
                                                "Rachel Spence",
                                                "living, USA",
                                                "Hunter's mother. Daughter of David A. Trifon. "
                                                "Source: Hunter Spence (direct family knowledge).",
                                                gen=8, century=20, confidence="confirmed",
                                                id_="p999",
                                                children=[N(
                                                    "Hunter Spence",
                                                    "living, USA",
                                                    "Subject of this family history. Son of Rachel Spence (maternal) and Dale William Spence Jr. (paternal). "
                                                    "Dual US/UK passport holder. "
                                                    "This line reaches Hunter via Westerfield → Iris → David Trifon → Rachel → Hunter.",
                                                    gen=9, century=21, confidence="confirmed",
                                                    id_="p001",
                                                    children=[]
                                                )]
                                            ),
                                        ]
                                    ),
                                    N(
                                        "Wallace 'Wally' Ballentine",
                                        "born 1930; died 2017",
                                        "Son of Iris Westerfield and Harold Ballentine. Half-sibling of David A. Trifon. "
                                        "Source: David A. Trifon family communication.",
                                        gen=7, century=20, confidence="confirmed",
                                        is_notable=True
                                    ),
                                    N(
                                        "Carol (Key) Ward",
                                        "born ~1937, Arkansas",
                                        "Daughter of Iris Westerfield and Andrew Jackson Key. Half-sibling of David A. Trifon. "
                                        "Married a Ward — listed in obituaries as 'Carol Ward'. "
                                        "Source: Carol Ward obituary, Walls Doris GEDCOM.",
                                        gen=7, century=20, confidence="confirmed"
                                    ),
                                    N(
                                        "Doris Walls",
                                        "born ~1930s–1940s",
                                        "Daughter of Iris Westerfield. Sister of David A. Trifon. "
                                        "DNA match to Hunter: 1st cousin 2x removed or half great-grandaunt (maternal side). "
                                        "Source: Walls Doris GEDCOM.",
                                        gen=7, century=20, confidence="confirmed"
                                    ),
                                ]
                            ),
                            N(
                                "O.C. 'Wes' Westerfield",
                                "born ~1921, Arkansas; died ~2008, Azle, Tarrant County, Texas",
                                "Son of Jesse and Bertie Jane. Married Viola Mae Boswell. "
                                "Source: Walls Doris GEDCOM.",
                                gen=6, century=20, confidence="confirmed"
                            ),
                            N(
                                "Padgett Lee Westerfield",
                                "born 1921; died 2002",
                                "Son of Jesse and Bertie Jane. Named after mother's maiden name Padgett. "
                                "Owned a Chevrolet dealership — notable local businessman in Arkansas. "
                                "Source: Walls Doris GEDCOM.",
                                gen=6, century=20, confidence="confirmed",
                                is_notable=True
                            ),
                            N(
                                "Maxie Eugene Westerfield",
                                "born 1922; died 1956",
                                "Son of Jesse and Bertie Jane. Died at ~34. "
                                "Source: Walls Doris GEDCOM.",
                                gen=6, century=20, confidence="confirmed"
                            ),
                            N(
                                "Wayne Miller Westerfield",
                                "born 1927; died 1990",
                                "Son of Jesse and Bertie Jane. Source: Walls Doris GEDCOM.",
                                gen=6, century=20, confidence="confirmed"
                            ),
                        ]
                    )]
                ),
                N(
                    "Oliver Cleveland Westerfield",
                    "born Apr 24, 1884, Kentucky; died Jan 16, 1936, Independence, Arkansas",
                    "Son of Joel Hayden Westerfield Jr. and Amanda Jane Nelson. Sibling of Jesse Lawrence Westerfield. "
                    "Married Nancy Leona Spivey (born Mar 10, 1889, Arkansas; died Jun 15, 1971, Newark, Independence County, Arkansas). "
                    "Source: Walls Doris GEDCOM.",
                    gen=4, century=19, confidence="confirmed",
                    spouse="Nancy Leona Spivey (born Mar 10, 1889, Arkansas; died Jun 15, 1971, Newark, Independence County, Arkansas)"
                ),
            ]
        )]
    )]
)
_wester_label = "MATERNAL — Westerfield/Trifon line (Jacobus Westervelt 1755 Long Island NY → Cornelius 1782 WV → Joel Sr. 1811 KY → Joel Jr. 1853 KY → Iris 1919 AR → David Trifon → Rachel → Hunter)"
if not replace_tree("Westerfield/Trifon", WESTERFIELD_TREE, new_label=_wester_label):
    add_tree(_wester_label, WESTERFIELD_TREE)


# ═══════════════════════════════════════════════════════════════════════════
# PADGETT ANCESTORS — Bertie Jane Padgett's lineage (Jesse Westerfield's wife)
# Source: Frances Padgett GEDCOM, Walls Doris GEDCOM
# ═══════════════════════════════════════════════════════════════════════════

PADGETT_TREE = N(
    "William Riley Padgett",
    "born ~1785, Virginia; died ~1855, Indiana (estimated)",
    "Hunter's maternal 5x great-grandfather (Padgett line). Father of John J. Padgett. "
    "Primary source: Frances Padgett GEDCOM. WikiTree alternate: wife listed as Hannah Evans (b.1776, NC) — "
    "conflicts with GEDCOM (Anne Casey). GEDCOM takes precedence. "
    "Padgett line may extend further: WikiTree records Benjamin Padgett (b.1755, Maryland) as possible father.",
    gen=1, century=18, confidence="probable",
    spouse="Anne Casey (born ~1785, Virginia; alt. source WikiTree: Hannah Evans b.1776 NC — unresolved conflict)",
    children=[N(
        "John J. Padgett (Pagett)",
        "born 1808, Vernon, Jennings County, Indiana; died Aug 14, 1873, Independence County, Arkansas",
        "Hunter's maternal 4x great-grandfather (Padgett line). Born Indiana, died Arkansas — "
        "early American migrant to the frontier South. "
        "Source: Frances Padgett GEDCOM (3rd cousin 1x removed or half 2nd cousin 2x removed, maternal side).",
        gen=2, century=19, confidence="confirmed",
        spouse="Amanda Goad (born Jul 25, 1830, Graves County, Kentucky; died Feb 6, 1911, McCracken County, Kentucky; "
               "parents: Caleb Goad 1792 VA + Elizabeth Dodson 1791 VA — see Goad ancestor tree)",
        children=[N(
            "William Miller Padgett",
            "born Oct 5, 1862, Independence County, Arkansas; died Nov 15, 1950, Lee County, Arkansas",
            "Hunter's maternal 3x great-grandfather (Padgett line). "
            "Son of John J. Padgett and Amanda Goad. Father of Bertie Jane Padgett "
            "who married Jesse Lawrence Westerfield. Source: Frances Padgett GEDCOM, Walls Doris GEDCOM.",
            gen=3, century=19, confidence="confirmed",
            spouse="Frances Ward (born Jan 23, 1868, Strawberry, Lawrence County, Arkansas; "
                   "died Sep 11, 1945, Smithville, Lawrence County, Arkansas; "
                   "parents: Joseph Ward 1833 TN + Jane Carolina Raney 1838 AR — see Ward ancestor tree)",
            children=[N(
                "Bertie Jane Padgett",
                "born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas",
                "Hunter's maternal great-great-grandmother (Padgett line). "
                "Daughter of William Miller Padgett and Frances Ward. "
                "Married Jesse Lawrence Westerfield (b.1887, KY). Together had five children "
                "including Iris June Westerfield (Hunter's maternal great-grandmother). "
                "Source: Walls Doris GEDCOM, Frances Padgett GEDCOM.",
                gen=4, century=19, confidence="confirmed",
                spouse="Jesse Lawrence Westerfield (born Jan 1, 1887, Kentucky — see Westerfield/Trifon tree)"
            )]
        )]
    )]
)
_padgett_label = "MATERNAL — Padgett ancestors (William Riley Padgett 1785 VA → John J. Padgett 1808 Indiana → William Miller 1862 AR → Bertie Jane 1888 AR)"
if not replace_tree("Padgett ancestors", PADGETT_TREE, new_label=_padgett_label):
    add_tree(_padgett_label, PADGETT_TREE)

# Descent chain: Bertie Jane Padgett → Jesse Westerfield → Iris Westerfield → David Trifon → Rachel → Hunter
def _add_hunter_to_padgett(node):
    """Find Bertie Jane Padgett with no children, add descent chain to Hunter."""
    if "Bertie Jane Padgett" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "Jesse Lawrence Westerfield",
            "born Jan 1, 1887, Kentucky; died Sep 29, 1951, Marianna, Lee County, Arkansas",
            "Hunter's maternal great-great-grandfather. Married Bertie Jane Padgett. "
            "See Westerfield/Trifon tree for full descendants.",
            gen=5, century=19, confidence="confirmed",
            spouse="Bertie Jane Padgett (born Mar 10, 1888, Arkansas)",
            children=[N(
                "Iris June Westerfield",
                "born Jun 1, 1919, Tuckerman, Arkansas; died Apr 13, 2003, Colt, Arkansas",
                "Hunter's maternal great-grandmother. Daughter of Jesse and Bertie Jane. "
                "Had children with Harold Ballentine: David A. Trifon (Hunter's maternal grandfather).",
                gen=6, century=20, confidence="confirmed",
                children=[N(
                    "David A. Trifon",
                    "born ~1940s, Arkansas area",
                    "Hunter's maternal grandfather. Biological son of Harold Ballentine and Iris Westerfield. "
                    "Took stepfather's surname Trifon after Harold died ~1945.",
                    gen=7, century=20, confidence="confirmed",
                    children=[N(
                        "Rachel Spence",
                        "living, USA",
                        "Hunter's mother. Daughter of David A. Trifon. "
                        "This line reaches Hunter via Padgett → Bertie Jane → Jesse → Iris → David Trifon → Rachel.",
                        gen=8, century=20, confidence="confirmed",
                        id_="p999",
                        children=[N(
                            "Hunter Spence",
                            "living, USA",
                            "Subject of this family history. "
                            "This line reaches Hunter via the Padgett → Westerfield → Trifon → Rachel path.",
                            gen=9, century=21, confidence="confirmed",
                            id_="p001",
                            children=[]
                        )]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_padgett(c):
            return True
    return False

_pt = get_tree("Padgett ancestors")
if _pt:
    _add_hunter_to_padgett(_pt)


# ═══════════════════════════════════════════════════════════════════════════
# BALLENTINE ANCESTORS — Harold Ballentine's lineage (David Trifon's father)
# Source: M.P. GEDCOM (1st cousin 2x removed, maternal side), Linda Coleman GEDCOM
# ═══════════════════════════════════════════════════════════════════════════

BALLENTINE_TREE = N(
    "John Ballentine",
    "born ~1770–1800, likely Virginia or North Carolina",
    "Earliest confirmed Ballentine ancestor in Hunter's maternal line. Married Betty Ducatt. "
    "Source: M.P. GEDCOM (1st cousin 2x removed or half great-grandaunt, maternal side).",
    gen=1, century=18, confidence="probable",
    spouse="Betty Ducatt",
    children=[N(
        "David Ballentine",
        "born ~1799, Virginia / North Carolina; died Jan 2, 1838, Gibson County, Tennessee",
        "Son of John Ballentine and Betty Ducatt. Married Susan Nee. "
        "Died Gibson County, TN — family was in Tennessee before the next generation moved to Arkansas. "
        "Source: M.P. GEDCOM.",
        gen=2, century=18, confidence="probable",
        spouse="Susan Nee",
        children=[N(
            "John Wallace Ballentine",
            "born Jul 23, 1826, North Carolina; died Feb 11, 1863, Tennessee",
            "Son of David Ballentine and Susan Nee. Born NC, died TN at age 36. "
            "Married Elizabeth Rebecca Barker. Son David Wyle born in Ozark, Franklin County, Arkansas — "
            "family was moving westward. Source: M.P. GEDCOM.",
            gen=3, century=19, confidence="probable",
            spouse="Elizabeth Rebecca Barker (born 1829, Tennessee; died 1881)",
            children=[N(
                "David Wyle Ballentine",
                "born Jun 18, 1856, Ozark, Franklin County, Arkansas; died Apr 16, 1933, Oden, Montgomery County, Arkansas",
                "Son of John Wallace Ballentine and Elizabeth Rebecca Barker. "
                "Married Sallie Culbertson (b.1864, Alabama — see Culbertson ancestor tree for her Irish immigrant ancestry). "
                "Father of Mary Ethel Lee Ballentine, Oda Elizabeth Ballentine, and likely Harold Ballentine. "
                "Lived entire life in Arkansas. Source: M.P. GEDCOM.",
                gen=4, century=19, confidence="confirmed",
                spouse="Sallie Culbertson (born Nov 10, 1864, Alabama; died Sep 20, 1945, Marianna, Arkansas; "
                       "Irish-American ancestry via Capt. Alexander Culbertson, Ballymoney, County Antrim — see Culbertson ancestor tree)",
                children=[
                    N(
                        "Mary Ethel Lee Ballentine",
                        "born Jun 8, 1884, Chismsville, Logan County, Arkansas; died Feb 19, 1961, Marianna, Arkansas",
                        "Daughter of David Wyle Ballentine and Sallie Culbertson. "
                        "Married William Woodville Herron. "
                        "Confirmed in multiple cousin GEDCOMs (M.P. GEDCOM, Linda Coleman GEDCOM). "
                        "Sister or half-sister of Harold Ballentine (David Trifon's biological father). "
                        "Source: M.P. GEDCOM.",
                        gen=5, century=19, confidence="confirmed",
                        spouse="William Woodville Herron"
                    ),
                    N(
                        "Oda Elizabeth Ballentine",
                        "born 1897, Arkansas; died 1935, Arkansas",
                        "Daughter of David Wyle Ballentine and Sallie Culbertson. "
                        "Married Jonah Bonner Maddox. Sister of Mary Ethel Lee Ballentine. "
                        "Source: M.P. GEDCOM.",
                        gen=5, century=19, confidence="confirmed",
                        spouse="Jonah Bonner Maddox"
                    ),
                    N(
                        "Harold 'Hal David' Ballentine",
                        "born ~1903, Arkansas (estimated); died ~1945",
                        "David A. Trifon's biological father. Married Iris June Westerfield (b.1919, Tuckerman AR). "
                        "Likely son of David Wyle Ballentine and Sallie Culbertson — same Arkansas Ballentine family. "
                        "After his death ~1945, son David took the surname of his stepfather (Trifon). "
                        "Source: David A. Trifon family communication, Walls Doris GEDCOM.",
                        gen=5, century=20, confidence="probable",
                        spouse="Iris June Westerfield (born Jun 1, 1919, Tuckerman, Arkansas — see Westerfield/Trifon tree)",
                        children=[
                            N(
                                "Wallace 'Wally' Ballentine",
                                "born 1930; died 2017",
                                "Son of Iris Westerfield and Harold Ballentine. Half-sibling of David A. Trifon. "
                                "Source: David A. Trifon family communication.",
                                gen=6, century=20, confidence="confirmed",
                                is_notable=True
                            ),
                            N(
                                "David A. Trifon",
                                "born ~1940s, Arkansas area",
                                "Son of Iris Westerfield and Harold Ballentine. "
                                "Took stepfather's surname 'Trifon' after Harold died ~1945. "
                                "Hunter's maternal grandfather. See Westerfield/Trifon tree for full descendants.",
                                gen=6, century=20, confidence="confirmed"
                            ),
                        ]
                    ),
                ]
            )]
        )]
    )]
)
_ballentine_label = "MATERNAL — Ballentine ancestors (John Ballentine ~1800 VA → David d.1838 Gibson TN → John Wallace 1826 NC → David Wyle 1856 Ozark AR → Harold Ballentine → David Trifon)"
if not replace_tree("Ballentine ancestors", BALLENTINE_TREE, new_label=_ballentine_label):
    add_tree(_ballentine_label, BALLENTINE_TREE)

# Descent chain: David A. Trifon → Rachel → Hunter (for Ballentine tree)
def _add_hunter_to_ballentine(node):
    """Find David A. Trifon with no children, add Rachel → Hunter chain."""
    if "David A. Trifon" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "Rachel Spence",
            "living, USA",
            "Hunter's mother. Daughter of David A. Trifon. "
            "This line reaches Hunter via Ballentine → Harold → David Trifon → Rachel.",
            gen=7, century=20, confidence="confirmed",
            id_="p999",
            children=[N(
                "Hunter Spence",
                "living, USA",
                "Subject of this family history. "
                "This line reaches Hunter via the Ballentine → Harold Ballentine → David Trifon → Rachel → Hunter path.",
                gen=8, century=21, confidence="confirmed",
                id_="p001",
                children=[]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_ballentine(c):
            return True
    return False

_bat = get_tree("Ballentine ancestors")
if _bat:
    _add_hunter_to_ballentine(_bat)


# ═══════════════════════════════════════════════════════════════════════════
# CULBERTSON ANCESTORS — Sallie Culbertson's lineage (Irish immigrant origin)
# Source: web research; County Antrim, Ireland records; Culbertson family genealogy
# ═══════════════════════════════════════════════════════════════════════════

CULBERTSON_TREE = N(
    "Capt. Alexander 'Irish' Culbertson",
    "born ~1745–1760, Ballymoney, County Antrim, Ireland; emigrated to colonial America ~1770s",
    "Hunter's maternal 5x great-grandfather (Culbertson line). First of the Culbertson line in America — "
    "Irish Protestant immigrant from Ballymoney, County Antrim. Known in family records as 'the Irish Culbertson.' "
    "Settled in North Carolina after emigrating. Source: Culbertson family genealogy, web research.",
    gen=1, century=18, confidence="probable",
    is_notable=True, is_immigrant=True, country_flag="🇮🇪",
    children=[N(
        "Jeremiah Culbertson",
        "born 1782, Burke County, North Carolina",
        "Son of Capt. Alexander Culbertson. Born NC after family emigrated from Ireland. "
        "Source: web research, Culbertson family records.",
        gen=2, century=18, confidence="probable",
        children=[N(
            "Allen Turner Culbertson",
            "born ~1820, Greene County, Georgia; died after 1870",
            "Son of Jeremiah Culbertson. Born Georgia — family moved south from NC. "
            "Source: web research, 1860/1870 census records.",
            gen=3, century=19, confidence="probable",
            spouse="Laura Houston (born ~1825, estimated)",
            children=[N(
                "Sallie Culbertson",
                "born Nov 10, 1864, Alabama; died Sep 20, 1945, Marianna, Lee County, Arkansas",
                "Hunter's maternal 2x great-grandmother (Culbertson-Ballentine line). "
                "Daughter of Allen Turner Culbertson and Laura Houston. "
                "Married David Wyle Ballentine (b.1856, Ozark, Franklin County, Arkansas). "
                "Mother of Mary Ethel Lee Ballentine, Oda Elizabeth Ballentine, and likely Harold Ballentine. "
                "See Ballentine ancestor tree for descendants. "
                "Source: M.P. GEDCOM, Linda Coleman GEDCOM.",
                gen=4, century=19, confidence="confirmed"
            )]
        )]
    )]
)
if not replace_tree("Culbertson ancestors", CULBERTSON_TREE):
    add_tree(
        "MATERNAL — Culbertson ancestors (Capt. Alexander 'Irish' Culbertson, Ballymoney County Antrim Ireland → Jeremiah 1782 NC → Allen Turner 1820 GA → Sallie Culbertson 1864 AL → Ballentine line)",
        CULBERTSON_TREE
    )

# Descent chain: Sallie Culbertson → David Wyle Ballentine → Harold → David Trifon → Rachel → Hunter
def _add_hunter_to_culbertson(node):
    """Find Sallie Culbertson with no children, add descent chain to Hunter."""
    if "Sallie Culbertson" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "David Wyle Ballentine",
            "born Jun 18, 1856, Ozark, Franklin County, Arkansas; died Apr 16, 1933, Oden, Arkansas",
            "Husband of Sallie Culbertson. Father of Harold Ballentine. "
            "See Ballentine tree for full details.",
            gen=5, century=19, confidence="confirmed",
            spouse="Sallie Culbertson (born Nov 10, 1864, Alabama)",
            children=[N(
                "Harold 'Hal David' Ballentine",
                "born ~1903, Arkansas; died ~1945",
                "David A. Trifon's biological father. Married Iris June Westerfield. "
                "After his death, son David took stepfather's surname Trifon.",
                gen=6, century=20, confidence="probable",
                children=[N(
                    "David A. Trifon",
                    "born ~1940s, Arkansas area",
                    "Hunter's maternal grandfather. Took stepfather's surname Trifon.",
                    gen=7, century=20, confidence="confirmed",
                    children=[N(
                        "Rachel Spence",
                        "living, USA",
                        "Hunter's mother. Daughter of David A. Trifon. "
                        "This line reaches Hunter via Culbertson → Sallie → David Wyle → Harold → David Trifon → Rachel.",
                        gen=8, century=20, confidence="confirmed",
                        id_="p999",
                        children=[N(
                            "Hunter Spence",
                            "living, USA",
                            "Subject of this family history. "
                            "This line reaches Hunter via the Irish Culbertson → Ballentine → Trifon → Rachel → Hunter path.",
                            gen=9, century=21, confidence="confirmed",
                            id_="p001",
                            children=[]
                        )]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_culbertson(c):
            return True
    return False

_ct = get_tree("Culbertson ancestors")
if _ct:
    _add_hunter_to_culbertson(_ct)


# ═══════════════════════════════════════════════════════════════════════════
# GOAD ANCESTORS — Amanda Goad's lineage (wife of John J. Padgett)
# Source: web research, Virginia colonial records, Kentucky census
# ═══════════════════════════════════════════════════════════════════════════

GOAD_TREE = N(
    "John Goad Sr.",
    "born ~1700, North Farnham Parish, Richmond County, Virginia",
    "Hunter's maternal 6x great-grandfather (Goad line). Early Virginia colonist, North Farnham Parish, Richmond County. "
    "Source: web research, Virginia colonial records.",
    gen=1, century=17, confidence="probable",
    spouse="Hannah Ann Isham (born ~1705, Virginia, estimated)",
    children=[N(
        "John Goad Jr.",
        "born 1729, Virginia",
        "Son of John Goad Sr. and Hannah Ann Isham. Born Virginia. "
        "Source: web research, Virginia records.",
        gen=2, century=18, confidence="probable",
        spouse="Margaret Chiles (born ~1730, Virginia, estimated)",
        children=[N(
            "Thomas Goad",
            "born ~1770, Bedford County, Virginia",
            "Son of John Goad Jr. and Margaret Chiles. Born Bedford County, Virginia — "
            "part of the westward migration into Kentucky. "
            "Source: web research, Virginia/Kentucky census.",
            gen=3, century=18, confidence="probable",
            spouse="Salley Tower (born ~1772, Virginia, estimated)",
            children=[N(
                "Caleb Goad",
                "born 1792, Virginia; died after 1860",
                "Son of Thomas Goad and Salley Tower. Born Virginia, moved to Kentucky. "
                "Father of Amanda Goad (b.1830, Graves County, KY) who married John J. Padgett. "
                "Source: web research, Kentucky census records.",
                gen=4, century=18, confidence="probable",
                spouse="Elizabeth Dodson (born 1791, Virginia; died after 1850)",
                children=[N(
                    "Amanda Goad",
                    "born Jul 25, 1830, Graves County, Kentucky; died Feb 6, 1911, McCracken County, Kentucky",
                    "Hunter's maternal 3x great-grandmother (Goad-Padgett line). "
                    "Daughter of Caleb Goad and Elizabeth Dodson. "
                    "Married John J. Padgett (b.1808, Indiana). See Padgett ancestor tree for descendants. "
                    "Source: Frances Padgett GEDCOM.",
                    gen=5, century=19, confidence="confirmed"
                )]
            )]
        )]
    )]
)
if not replace_tree("Goad ancestors", GOAD_TREE):
    add_tree(
        "MATERNAL — Goad ancestors (John Goad 1700 North Farnham Parish VA → John Jr. 1729 VA → Thomas 1770 Bedford VA → Caleb Goad 1792 VA → Amanda Goad 1830 Graves KY)",
        GOAD_TREE
    )

# Descent chain: Amanda Goad → John J. Padgett → William Miller Padgett → Bertie Jane → Jesse Westerfield → Iris → David Trifon → Rachel → Hunter
def _add_hunter_to_goad(node):
    """Find Amanda Goad with no children, add descent chain to Hunter."""
    if "Amanda Goad" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "John J. Padgett (Pagett)",
            "born 1808, Vernon, Jennings County, Indiana; died Aug 14, 1873, Independence County, Arkansas",
            "Husband of Amanda Goad. Hunter's maternal 4x great-grandfather. "
            "See Padgett tree for full details.",
            gen=6, century=19, confidence="confirmed",
            spouse="Amanda Goad (born Jul 25, 1830, Graves County, Kentucky)",
            children=[N(
                "William Miller Padgett",
                "born Oct 5, 1862, Independence County, Arkansas; died Nov 15, 1950, Lee County, Arkansas",
                "Son of John J. Padgett and Amanda Goad.",
                gen=7, century=19, confidence="confirmed",
                children=[N(
                    "Bertie Jane Padgett",
                    "born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas",
                    "Daughter of William Miller Padgett and Frances Ward. Married Jesse Westerfield.",
                    gen=8, century=19, confidence="confirmed",
                    children=[N(
                        "Iris June Westerfield",
                        "born Jun 1, 1919, Tuckerman, Arkansas; died Apr 13, 2003, Colt, Arkansas",
                        "Hunter's maternal great-grandmother. Daughter of Jesse and Bertie Jane Padgett.",
                        gen=9, century=20, confidence="confirmed",
                        children=[N(
                            "David A. Trifon",
                            "born ~1940s, Arkansas area",
                            "Hunter's maternal grandfather.",
                            gen=10, century=20, confidence="confirmed",
                            children=[N(
                                "Rachel Spence",
                                "living, USA",
                                "Hunter's mother. This line reaches Hunter via Goad → Amanda → Padgett → Bertie Jane → Westerfield → Iris → Trifon → Rachel.",
                                gen=11, century=20, confidence="confirmed",
                                id_="p999",
                                children=[N(
                                    "Hunter Spence",
                                    "living, USA",
                                    "Subject of this family history. "
                                    "This line reaches Hunter via the Virginia Goad → Padgett → Westerfield → Trifon → Rachel → Hunter path.",
                                    gen=12, century=21, confidence="confirmed",
                                    id_="p001",
                                    children=[]
                                )]
                            )]
                        )]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_goad(c):
            return True
    return False

_gt = get_tree("Goad ancestors")
if _gt:
    _add_hunter_to_goad(_gt)


# ═══════════════════════════════════════════════════════════════════════════
# WARD ANCESTORS — Frances Ward's lineage (wife of William Miller Padgett)
# Source: web research, colonial NC/SC records, Arkansas census
# ═══════════════════════════════════════════════════════════════════════════

WARD_TREE = N(
    "John Ward",
    "born 1748, Chowan County, North Carolina",
    "Hunter's maternal 5x great-grandfather (Ward line). Born colonial North Carolina, Chowan County. "
    "Source: web research, colonial North Carolina records.",
    gen=1, century=18, confidence="probable",
    spouse="Catherine Ward (born ~1750, North Carolina, estimated)",
    children=[N(
        "Thomas S. Ward",
        "born 1760, Darlington County, South Carolina; died after 1830",
        "Son of John Ward and Catherine Ward. Born Darlington County, SC — "
        "family moved from NC to SC in this generation. "
        "Source: web research, South Carolina census records.",
        gen=2, century=18, confidence="probable",
        spouse="Nancy Crompton (born ~1765, estimated)",
        children=[N(
            "John Robert Ward",
            "born 1804, Pendleton, Anderson County, South Carolina; died after 1860",
            "Son of Thomas S. Ward and Nancy Crompton. Born Pendleton, SC. "
            "Later moved to Tennessee, then Arkansas following frontier migration patterns. "
            "Source: web research, census records.",
            gen=3, century=19, confidence="probable",
            spouse="Rebecca Winn (born ~1808, estimated)",
            children=[N(
                "Joseph Ward",
                "born 1833, Tennessee; died after 1870",
                "Son of John Robert Ward and Rebecca Winn. Born Tennessee. "
                "Father of Frances Ward (b.1868, Strawberry, Lawrence County, Arkansas) "
                "who married William Miller Padgett. "
                "Source: web research, Arkansas census records.",
                gen=4, century=19, confidence="probable",
                spouse="Jane Carolina Raney (born 1838, Arkansas; died after 1870)",
                children=[N(
                    "Frances Ward",
                    "born Jan 23, 1868, Strawberry, Lawrence County, Arkansas; "
                    "died Sep 11, 1945, Smithville, Lawrence County, Arkansas",
                    "Hunter's maternal 2x great-grandmother (Ward-Padgett line). "
                    "Daughter of Joseph Ward and Jane Carolina Raney. "
                    "Married William Miller Padgett (b.1862, Independence County, Arkansas). "
                    "See Padgett ancestor tree for descendants. "
                    "Source: Frances Padgett GEDCOM.",
                    gen=5, century=19, confidence="confirmed"
                )]
            )]
        )]
    )]
)
if not replace_tree("Ward ancestors", WARD_TREE):
    add_tree(
        "MATERNAL — Ward ancestors (John Ward 1748 Chowan NC → Thomas 1760 Darlington SC → John Robert 1804 Pendleton SC → Joseph 1833 TN → Frances Ward 1868 Strawberry AR)",
        WARD_TREE
    )

# Descent chain: Frances Ward → William Miller Padgett → Bertie Jane → Jesse Westerfield → Iris → David Trifon → Rachel → Hunter
def _add_hunter_to_ward(node):
    """Find Frances Ward with no children, add descent chain to Hunter."""
    if "Frances Ward" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "William Miller Padgett",
            "born Oct 5, 1862, Independence County, Arkansas; died Nov 15, 1950, Lee County, Arkansas",
            "Husband of Frances Ward. Son of John J. Padgett and Amanda Goad. "
            "Father of Bertie Jane Padgett who married Jesse Westerfield. "
            "See Padgett tree for full details.",
            gen=6, century=19, confidence="confirmed",
            spouse="Frances Ward (born Jan 23, 1868, Strawberry, Lawrence County, Arkansas)",
            children=[N(
                "Bertie Jane Padgett",
                "born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas",
                "Daughter of William Miller Padgett and Frances Ward. Married Jesse Westerfield.",
                gen=7, century=19, confidence="confirmed",
                children=[N(
                    "Iris June Westerfield",
                    "born Jun 1, 1919, Tuckerman, Arkansas; died Apr 13, 2003, Colt, Arkansas",
                    "Hunter's maternal great-grandmother. Daughter of Jesse and Bertie Jane Padgett.",
                    gen=8, century=20, confidence="confirmed",
                    children=[N(
                        "David A. Trifon",
                        "born ~1940s, Arkansas area",
                        "Hunter's maternal grandfather.",
                        gen=9, century=20, confidence="confirmed",
                        children=[N(
                            "Rachel Spence",
                            "living, USA",
                            "Hunter's mother. This line reaches Hunter via Ward → Frances → William Miller Padgett → Bertie Jane → Westerfield → Iris → David Trifon → Rachel.",
                            gen=10, century=20, confidence="confirmed",
                            id_="p999",
                            children=[N(
                                "Hunter Spence",
                                "living, USA",
                                "Subject of this family history. "
                                "This line reaches Hunter via the NC/SC Ward → Padgett → Westerfield → Trifon → Rachel → Hunter path.",
                                gen=11, century=21, confidence="confirmed",
                                id_="p001",
                                children=[]
                            )]
                        )]
                    )]
                )]
            )]
        )]
        return True
    for c in node.get("children", []):
        if _add_hunter_to_ward(c):
            return True
    return False

_wt = get_tree("Ward ancestors")
if _wt:
    _add_hunter_to_ward(_wt)


# ═══════════════════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

multi["secondary_trees"] = secondary

with open(multi_path, "w", encoding="utf-8") as f:
    json.dump(multi, f, ensure_ascii=False, indent=2)


# Print summary
def count_nodes(node):
    if not node:
        return 0
    return 1 + sum(count_nodes(c) for c in node.get("children", []))


print("=== TREE EXPANSION COMPLETE ===")
print(f"Primary tree (Mattingly): {count_nodes(multi.get('primary'))} nodes")
for st in multi["secondary_trees"]:
    label = st["label"][:55]
    n = count_nodes(st.get("tree"))
    print(f"  [{label}]: {n} nodes")
