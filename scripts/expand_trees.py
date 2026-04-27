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
                                                                                                                        "born 1876, England — immigrated to America ~1900",
                                                                                                                        "POSSIBLE. Hunter's paternal great-great-grandfather. "
                                                                                                                        "Born 1876 in England (most likely Co. Durham or North "
                                                                                                                        "Yorkshire based on surname density); immigrated ~1900. "
                                                                                                                        "Married Jeanne A. Meton (born 1883, France; immigrated "
                                                                                                                        "1898). Had three children: Mary L. Spence, William Spence "
                                                                                                                        "(Hunter's great-grandfather), and Joseph C. Spence Jr. "
                                                                                                                        "NOTE: family oral tradition only — parents' names and "
                                                                                                                        "exact birthplace unconfirmed. UNLOCK: FreeBMD births "
                                                                                                                        "search (free) + GRO birth cert (~£11) will name his "
                                                                                                                        "parents and confirm county.",
                                                                                                                        gen=27, century=19, confidence="possible",
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
                                                                                                                                            "Son of Dr. Dale William Spence Sr. and Alice Marie Henslee. "
                                                                                                                                            "Married and divorced Rachel Trifon.",
                                                                                                                                            gen=30, century=20, confidence="probable",
                                                                                                                                            spouse="Rachel Trifon (m. ~1990s, div.)",
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
                                                                                            "John Spence of Glasgow",
                                                                                            "b. ~1611, Glasgow, Scotland; d. 1704, Westmoreland County, Virginia",
                                                                                            "POSSIBLE bridge candidate (WikiTree Spence-2810). "
                                                                                            "Emigrated from Scotland to colonial Virginia. "
                                                                                            "Died 1704 Westmoreland County, Virginia. "
                                                                                            "Probable link between the confirmed Clan Spens chain "
                                                                                            "and Hunter's paternal Spence line. "
                                                                                            "Connection to Wormiston branch probable but not yet documented.",
                                                                                            gen=21, century=17, confidence="possible",
                                                                                            is_immigrant=True, country_flag="\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f",
                                                                                            children=[]
                                                                                        ),
                                                                                        N(
                                                                                            "David Spence of Dysart",
                                                                                            "b. 1639, Dysart, Fife, Scotland; d. 1679, Maryland",
                                                                                            "POSSIBLE bridge candidate (WikiTree Spence-1823; "
                                                                                            "FamilySearch christening confirmed). "
                                                                                            "Born Dysart, Fife — same county as Wormiston Castle. "
                                                                                            "Emigrated to Maryland colony; 1678 will on file. "
                                                                                            "Probable link between the confirmed Fife Spens gentry "
                                                                                            "and Hunter's paternal Spence line. "
                                                                                            "Dysart Fife origin makes Wormiston connection plausible.",
                                                                                            gen=21, century=17, confidence="possible",
                                                                                            is_immigrant=True, country_flag="\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f",
                                                                                            children=[]
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
    "PATERNAL — Spence line (Clan Spens surname heritage — direct link to Hunter UNCONFIRMED pending Joseph C. Spence Sr. birth cert)"
)
if not replaced:
    add_tree(
        "PATERNAL — Spence line (Clan Spens surname heritage — direct link to Hunter UNCONFIRMED pending Joseph C. Spence Sr. birth cert)",
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
if henslee_tree:
    _henslee_root_name = henslee_tree.get("name", "")
    if _henslee_root_name not in ("James Hensley II",):
        # Find the deepest existing tree starting point to avoid double-wrapping
        # If root is already "William Hensley (Henslee)", use its children (Maxfield onward)
        if _henslee_root_name == "William Hensley (Henslee)":
            _maxfield_children = henslee_tree.get("children", [])
        else:
            # Root is the raw original tree (e.g. Maxfield or earlier) — use its children
            _maxfield_children = henslee_tree.get("children", [])

        # Rebuild William Hensley node pointing at Maxfield's subtree
        _william_node = N(
            "William Hensley (Henslee)",
            "c. 1691–1693, Fluvanna / Goochland County, Virginia Colony; died c. 1770–1781, Virginia",
            "POSSIBLE. Father of Maxfield Henslee (b.1727 Goochland, VA). "
            "The Hensley/Henslee surname is a Devon, England habitational name from Hensley village, "
            "East Worlington parish, Devon, England — meaning 'Hēahmund's woodland clearing' in Old "
            "English (Oxford DAFN 2022). The 'Henslee' spelling is specific to the Macksfield line. "
            "NOTE: This parentage is asserted in WikiTree Hensley-196 and cousin GED (Jenniffer Henslee); "
            "NOT verified by primary source. Independent researcher martygrant.com explicitly disclaims "
            "knowledge of Macksfield's parents. Display as POSSIBLE/unconfirmed on website. "
            "Source: 61-cousin-merged-people.json; WikiTree Henslee-88; 79-henslee-extended-research.json.",
            gen=7, century=18, confidence="possible",
            spouse="Jane Snell (c. 1709–1796)",
            children=[
                N(
                    "Maxfield Henslee",
                    "1727 Goochland, VA – c. 1790",
                    "PROBABLE. Earliest traced Henslee ancestor in Hunter's direct line. "
                    "Virginia-born; likely moved to Caswell County, North Carolina per family pattern. "
                    "DAR records confirm a Macksfield/Maxfield Henslee in NC colonial-era records. "
                    "Source: 61-cousin-merged-people.json; 65-henslee-confirmed-trace.json.",
                    gen=8, century=18, confidence="probable",
                    spouse="Martha 'Patty' Sneed",
                    children=_maxfield_children
                )
            ]
        )

        # Top-level: add James Hensley II as possible ancestor above William
        _extended_henslee = N(
            "James Hensley II",
            "born 1642, Northampton County, Virginia; died 1705, Northampton County, Virginia",
            "POSSIBLE ancestor. Named in WikiTree Hensley-196 as the father of William Hensley (~1691) "
            "who is the probable father of Macksfield Henslee. Cited in multiple WikiTree profiles as "
            "common ancestor of the Maxfield Henslee (1810) line. "
            "CAUTION: This chain (James II → William → Macksfield) is user-asserted on WikiTree without "
            "primary source documentation. The independent researcher martygrant.com explicitly states "
            "'I have no clue who Mackfield's parents might be.' Mark as POSSIBLE — NOT confirmed. "
            "Source: WikiTree Hensley-196; research/79-henslee-extended-research.json.",
            gen=6, century=17, confidence="possible",
            spouse="Susanna (Newcomb) Hensley (born 1665, Henrico County, Virginia; died 1730, Henrico County, Virginia)",
            children=[_william_node]
        )
        replace_tree("Henslee line", _extended_henslee)

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
                "Hunter's father. Son of Dr. Dale William Spence Sr. and Alice Marie Henslee. "
                "Married and divorced Rachel Trifon.",
                gen=31, century=20, confidence="probable",
                spouse="Rachel Trifon (m. ~1990s, div.)",
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
# BYRD ANCESTORS — add Richard Bird (1750) and Rev William Byrd (1774)
# Source: research/78-byrd-extended-research.json (wave-1 research)
# Chain: Richard Bird (1750) → Rev William Byrd (1774) → [William Leander Byrd 1832]
# Guard: skip if Richard Bird (Byrd) already present in Byrd tree children
# ═══════════════════════════════════════════════════════════════════════════

def _byrd_ancestor_present(node, target="Richard Bird (Byrd)"):
    """Return True if target name exists anywhere in the tree."""
    if node.get("name") == target:
        return True
    return any(_byrd_ancestor_present(c, target) for c in node.get("children", []))

_byrd_root = get_tree("Byrd line")
if _byrd_root and not _byrd_ancestor_present(_byrd_root):
    # Build the new confirmed ancestor chain as a top-level sibling branch
    _richard_bird_node = N(
        "Richard Bird (Byrd)",
        "November 3, 1750, Albemarle Parish, Virginia — March 5, 1803, Hawkins County, Tennessee",
        "DAR patriot A133396; fought Battle of Point Pleasant 1774 (Lord Dunmore's War) under "
        "Capt. Daniel Smith. Will (Hawkins Co TN, 1803) names 11 children including Michael Byrd. "
        "Primary sources: Albemarle Parish Register, Spotsylvania deed 1763, Montgomery Co VA "
        "militia 1777-1790, Hawkins Co TN deed/will books. WikiTree Bird-3176. "
        "Moved Spotsylvania/Prince Edward Co VA → Fincastle/Botetourt Co VA → Hawkins Co TN. "
        "CONFIRMED as real historical person; PROBABLE as Hunter's ancestor (intermediate "
        "generations to William Leander Byrd 1832 still being confirmed). "
        "Source: research/78-byrd-extended-research.json.",
        gen=9, century=18, confidence="confirmed",
        is_notable=True,
        spouse="Elizabeth Woods (Buster) Byrd (born 1751 North Carolina; married 1774 Virginia)",
        children=[
            N(
                "Rev William Byrd",
                "circa 1774 — 1856",
                "Son of Richard Bird (Byrd, 1750-1803) and Elizabeth Woods Buster. "
                "Married Lydia Adair 1794. Find A Grave memorial 134708782. "
                "His son John Byrd (married Sara Fears) is a probable match to 'William John Byrd "
                "(1799-1855) + Sarah A Fears' in the GEDCOM chain — the Fears/Fear surname "
                "convergence strongly supports this link to William Leander Byrd (1832 AL). "
                "PROBABLE ancestor: Richard Bird (1750) → Rev William Byrd (1774) → "
                "John/William John Byrd (~1799) → William Leander Byrd (1832) chain. "
                "Source: Find A Grave #134708782; research/78-byrd-extended-research.json.",
                gen=8, century=18, confidence="probable",
                spouse="Lydia Adair (married 1794)",
            )
        ]
    )
    # Append to the Byrd / Bird Ancestry root's children list
    _byrd_root["children"].append(_richard_bird_node)


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
    "Arthur Beatty",
    "b. ~1673, Killeshandra, County Cavan, Ireland; d. after 1710",
    "POSSIBLE. Probable grandfather of George Baity Sr. via Francis Beaty Sr. "
    "Killeshandra, County Cavan, Ireland. Y-DNA R-BY1127 confirms Scots-Irish origin; "
    "family migrated Scotland → County Down/Cavan, Ulster ~1610s. "
    "Source: 88-baity-colonial-origins.json; sherrysharp.com genealogy.",
    gen=1, century=17, confidence="possible",
    children=[N(
        "Francis Beaty Sr. (Ensign)",
        "b. ~1707, Ireland (probable County Down); d. 1773, Mecklenburg County, North Carolina",
        "POSSIBLE. Ensign in colonial militia; emigrated from Ulster ~1729–1750 via Pennsylvania; "
        "died Mecklenburg County NC 1773; will may document parentage of Thomas Beaty and George Baity. "
        "Settled Rowan County NC area by 1759 (Rowan tax census) then Mecklenburg by 1768. "
        "NOTE: Baity is Scots-Irish (NOT German as sometimes assumed); from Old English 'Bat(t)' "
        "(pet form of Bartholomew), recorded as 'Batie' in Berwick-on-Tweed 1334; "
        "Y-DNA R-BY1127 characteristic of Ireland/Scotland. "
        "Source: 88-baity-colonial-origins.json; WikiTree Beaty-282.",
        gen=2, century=18, confidence="possible",
        is_immigrant=True, country_flag="🇮🇪",
        spouse="Martha Cairnes",
        children=[N(
            "Thomas Beaty",
            "b. ~1735; d. after 1765, Rowan/Anson County, North Carolina",
            "POSSIBLE. Appears in Rowan/Anson County deeds 1762–1765; probable father of George Baity Sr.; "
            "son of Francis Beaty Sr. Source: 88-baity-colonial-origins.json.",
            gen=3, century=18, confidence="possible",
            children=[N(
                "George Baity Sr.",
                "b. ~November 27, 1746, d. March 11, 1828, Rowan County, North Carolina",
                "CONFIRMED. Father of William Henry Baity (1771) and David Isom Baity (1782); "
                "WikiTree Baity-20; confirmed via FamilySearch PID L4SG-7MF for Rachel Allgood. "
                "George 'appears to have never lived anywhere other than Dutchman's Creek in Rowan County.' "
                "Paid Rowan County taxes 1787. Land on Chiquapin Creek purchased 1798. "
                "Source: 88-baity-colonial-origins.json; WikiTree Baity-20; FindAGrave #24992971.",
                gen=4, century=18, confidence="confirmed",
                spouse="Rachel Allgood (b. ~1754–1756, d. 1828; FamilySearch PID L4SG-7MF)",
                children=[N(
                    "David Isom Baity",
                    "1782, Rowan, NC – 1854, Davie County, NC",
                    "PROBABLE. Son of George Baity Sr., Rowan Co NC. "
                    "Confirmed in cousin GEDCOM (61-cousin-merged-people.json). "
                    "Source: FindAGrave #202953407.",
                    gen=5, century=18, confidence="probable",
                    children=[N(
                        "Isom 'Isham' Baity",
                        "1804, Surry / Yadkin, NC – 1892, Yadkin County, NC",
                        "CONFIRMED. Primary source: cemetery transcription at Courtney Baptist Church Cemetery "
                        "'Baity, Isham Isom (b. 19 Oct 1804 - d. 23 Dec 1892)'. "
                        "Wife Nancy Plowman confirmed by daughter Jennette C. Baity's cemetery entry. "
                        "Source: cemeterycensus.org/nc/yadk/cem049.htm.",
                        gen=6, century=19, confidence="confirmed",
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
                                                                "Sharyn 'Shari' Mattingly Trifon",
                                                                "born 1947, USA — living",
                                                                "CONFIRMED. Hunter's maternal grandmother. "
                                                                "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                                                                "Married David A. Trifon. "
                                                                "Recorded oral history for this family history project in 2025.",
                                                                gen=11, century=20, confidence="confirmed",
                                                                children=[
                                                                    N(
                                                                        "Rachel Trifon",
                                                                        "living, USA",
                                                                        "Hunter's mother. Daughter of Shari Mattingly Trifon. "
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
                    )]
                )]
            )]
        )]
    )]
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
        "CONFIRMED (Neue Deutsche Biographie). Seconde-Lieutenant in the Brunswick army's "
        "Schwarzen Corps des Majors Olfermann (the 'Brunswick Black Corps' — the famous "
        "all-black-uniformed Napoleonic War volunteers, NOT the Prussian army as sometimes stated). "
        "His death in 1855 left the family in financial hardship, causing sons Gustav (then 23) "
        "and Hans (then 18) to abandon planned university careers — Hans emigrated to Texas in 1856. "
        "Married Charlotte Georgine Elisabeth von Girsewald (1799–1860; correct spelling: 'Girsewald', "
        "NOT 'Gursewald' which is an OCR artifact from Lotto 1902). "
        "Their children include Gustav Teichmüller (philosopher, 1832–1888; died Dorpat/Estonia — "
        "Baltic German only by residence, Lower Saxon/Braunschweig by origin; his work influenced Nietzsche) "
        "and Hans Teichmüller (Hunter's direct ancestor). Source: NDB vol. 26, 2016, p. 6.",
        gen=5, century=19, confidence="confirmed",
        spouse="Charlotte Georgine Elisabeth von Girsewald (1799–1860)",
        children=[current_root]
    )
    # Prepend Wilhelm Ernst Conrad Teichmüller before August Wilhelm
    wec_node = N(
        "Wilhelm Ernst Conrad Teichmüller",
        "1758–1835, Delligsen / Lower Saxony, Germany",
        "CONFIRMED (NDB). Oberhütteninspekteur (chief inspector of smelting works) at "
        "Karlshütte near Delligsen, Leinebergland — a major ironworks south of Hanover. "
        "Married Henriette Christiane Helene Schorkopf (1763–1818, Uslar, Lower Saxony). "
        "Ancestor of both Hans Teichmüller (Hunter's direct ancestor) and "
        "Gustav Teichmüller (the philosopher). Source: NDB vol. 26, 2016, p. 6.",
        gen=4, century=18, confidence="confirmed",
        children=[aug_node]
    )
    joachim_node = N(
        "Joachim Andreas Teichmüller",
        "1705–1778, Rohrsheim near Halberstadt (Saxony-Anhalt) → Goslar, Germany",
        "CONFIRMED (NDB + GEDBAS). Born Rohrsheim near Halberstadt, Saxony-Anhalt (baptized 26 June 1705); "
        "worked as Oberfaktor (chief commercial agent) in Goslar — the ancient Harz silver-mining capital "
        "(Rammelsberg mine, UNESCO World Heritage). Died Goslar 31 January 1778. "
        "Rohrsheim Ortsfamilienbuch (OFB) covering 1673–1980 may name his parents. "
        "Source: NDB vol. 26, 2016, pp. 6*–7*; GEDBAS genealogy database (GND 1154326802).",
        gen=3, century=18, confidence="confirmed",
        children=[wec_node]
    )
    full_teich = N(
        "Hans / Johann Teichmüller",
        "~1580–1638, Harz Mountains, Germany",
        "CONFIRMED (NDB). Earliest documented Teichmüller ancestor — Mühlenmeister (master miller) "
        "in the southern Harz mountains. The surname is occupational: 'Teich' (pond) + "
        "'Müller' (miller) = 'pond miller'. The Harz was Germany's premier mining region; "
        "water mills powered the silver, iron, and copper mines. "
        "Source: Neue Deutsche Biographie (NDB) vol. 26, 2016, p. 6*: 'Aus seit Ende d. 16. Jh. "
        "mit d. Mühlenmeister Han(n)s (um 1580–1638) im südl. Harz nachweisbarer Fam.'",
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
            "Father of Sharyn 'Shari' Mattingly Trifon (b.1947). "
            "Source: 76-baity-to-hunter.json; Shari Mattingly oral history.",
            gen=10, century=20, confidence="confirmed",
            spouse="Jennive Imogene Lepick (b.1923-d.2008; see Lepik tree)",
            children=[N(
                "Sharyn 'Shari' Mattingly Trifon",
                "born 1947, USA — living",
                "CONFIRMED. Hunter's maternal grandmother. "
                "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                "Recorded oral history for this project in 2025.",
                gen=11, century=20, confidence="confirmed",
                children=[N(
                    "Rachel Trifon",
                    "living, USA",
                    "Hunter's mother. Daughter of Shari Mattingly Trifon. "
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
            "Father of Sharyn 'Shari' Mattingly Trifon (b.1947). "
            "Source: 76-baity-to-hunter.json; Shari Mattingly oral history.",
            gen=6, century=20, confidence="confirmed",
            spouse="Jennive Imogene Lepick (married ~1944)",
            children=[N(
                "Sharyn 'Shari' Mattingly Trifon",
                "born 1947, USA — living",
                "CONFIRMED. Hunter's maternal grandmother. "
                "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                "Recorded oral history for this project in 2025.",
                gen=7, century=20, confidence="confirmed",
                children=[N(
                    "Rachel Trifon",
                    "living, USA",
                    "Hunter's mother. Daughter of Shari Mattingly Trifon. "
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
if boehme_tree and boehme_tree.get("name") not in ("Böhme family, Prussian Silesia (Schlesien)", "Böhme family, Germany (possibly Saxony or Silesia)"):
    silesian_root = N(
        "Böhme family, Germany (possibly Saxony or Silesia)",
        "~1800–1855, Germany (Saxony or Prussian Silesia region)",
        "PROBABLE. The Böhme surname means 'the Bohemian' — an ethnic label for German Protestants "
        "who fled Bohemia into Saxony/Silesia during the Thirty Years' War (1618–1648). "
        "Surname today concentrated in Saxony (34%) and Saxony-Anhalt (11%) — statistically, "
        "Saxony is more likely than Silesia as the family origin. "
        "They arrived at Indianola TX between 1855 and 1862; Indianola's 1875 hurricane destroyed "
        "most passenger manifests. Parents of the Texan Böhme immigrants are unidentified — "
        "Hamburg Passenger Lists and 1870/1880 US Census are the primary research unlock. "
        "The Texas settlement at Breslau (Lavaca Co.) was named for Breslau (now Wrocław, Poland) "
        "by settlers who may have come via Silesia, but Saxony origin is statistically more probable. "
        "Source: 68-boehme-confirmed-trace.json; 87-boehme-silesia-ancestry.json.",
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
                "Mother of Sharyn 'Shari' Mattingly Trifon. "
                "Source: Shari Mattingly oral history.",
                gen=6, century=20, confidence="confirmed",
                spouse="Leroy Baity Mattingly (b.1922, San Antonio TX)",
                children=[N(
                    "Sharyn 'Shari' Mattingly Trifon",
                    "born 1947, USA — living",
                    "CONFIRMED. Hunter's maternal grandmother. "
                    "Daughter of Leroy Baity Mattingly and Jennive Imogene Lepick. "
                    "Recorded oral history for this project in 2025.",
                    gen=7, century=20, confidence="confirmed",
                    children=[N(
                        "Rachel Trifon",
                        "living, USA",
                        "Hunter's mother. Daughter of Shari Mattingly Trifon. "
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
    "Lubbert Van Westervelt",
    "died ~1619, Meppel, Drenthe, Netherlands",
    "POSSIBLE Dutch ancestor — father of the 1662 immigrant. Named in the Genealogical Society of Bergen "
    "County (GSBC) family files as the father of Lubbert Lubbertsen Van Westervelt (the immigrant). "
    "No birth date or spouse name documented. This is the practical limit of the genealogical record. "
    "Source: GSBC Family Files p817; dutchcousins.org Westerfield PDF; research/81-westerfield-extended-research.json.",
    gen=1, century=16, confidence="possible",
    children=[N(
        "Lubbert Lubbertsen Van Westervelt (THE IMMIGRANT)",
        "born ~1620–1626, Meppel, Drenthe, Netherlands; died before Sep 1, 1687, Hackensack, New Jersey",
        "CONFIRMED. First Westervelt in America. The name 'Westervelt' means 'of the western fields' in Dutch, "
        "referring to geographic area near Meppel on the east coast of the Zuider Zee. "
        "Emigrated from Meppel, Drenthe aboard the ship 'Hope' (de Hoop), departed Apr 8, 1662, "
        "arriving New Amsterdam (New York) Jun 29, 1662 — traveled with brother William Lubbertsen Van "
        "Westervelt and 4+ children. Settled 1662–1672 at Flatbush, Long Island (purchased farm, sold for "
        "4,000 guilders profit in 1672), then 1672–1687 Hackensack, New Jersey. Founding member of Dutch "
        "Reformed Church at Hackensack (Schaarlenburgh congregation) 1686. "
        "Married Geesje (Grace) Roelofse Van Houten (~1625, NL; died after Dec 27, 1696, Hackensack). "
        "Source: GSBC Family Files p817; WikiTree Lubbertz-1; dutchcousins.org Westerfield PDF; "
        "Genealogy of the Westervelt Family, Walter Tallman Westervelt (1905); research/81-westerfield-extended-research.json.",
        gen=2, century=17, confidence="confirmed",
        is_immigrant=True, country_flag="🇳🇱",
        spouse="Geesje (Grace) Roelofse Van Houten (~1625, Netherlands; died after Dec 27, 1696, Hackensack, NJ)",
        children=[N(
            "Lubbert Lubberts Jr. Westervelt",
            "born ~1658–1661, Meppel, Drenthe, Netherlands; died ~1694–1695, Hackensack, New Jersey",
            "CONFIRMED. Son of Lubbert Lubbertsen (the immigrant) and Geesje Van Houten. Likely born in Meppel "
            "before the 1662 emigration (one of the children on the ship 'Hope'). Died young in Hackensack "
            "before his son Jan was born — hence Jan was baptized 1686 under patronymic 'Lubbertsen' (son of Lubbert). "
            "Dutch Reformed Church records at Hackensack document this generation. "
            "Married Hilletje Poulouse / Hilletia Paulus (born before May 22, 1661, New Amsterdam; died 1764). "
            "Source: dutchcousins.org Westerfield PDF; GSBC p817; WikiTree Lubbertz-1; research/81-westerfield-extended-research.json.",
            gen=3, century=17, confidence="confirmed",
            is_immigrant=True, country_flag="🇳🇱",
            spouse="Hilletje Poulouse / Hilletia Paulus (born before May 22, 1661, New Amsterdam; died 1764)",
            children=[N(
                "Jan Westervelt (Jan Lubbertse Van Westervelt)",
                "born before Mar 27, 1686, Hackensack, Bergen County, New Jersey; died ~1730, Hackensack",
                "CONFIRMED. Son of Lubbert Lubberts Jr. and Hilletje Poulouse. "
                "Baptized 1686 in Dutch Reformed Church, Hackensack. "
                "Married Dirckje Huybertse Blauvelt (born before Apr 3, 1687, NY) on May 28, 1709, Hackensack (DRC). "
                "Children included: Jacobus Westervelt (b. Sep 7, 1712) — Hunter's direct line. "
                "Source: GSBC Family Files p1817; WikiTree Westervelt-41; research/81-westerfield-extended-research.json.",
                gen=4, century=17, confidence="confirmed",
                spouse="Dirckje Huybertse Blauvelt (born before Apr 3, 1687, New York; married May 28, 1709, Hackensack DRC)",
                children=[N(
                    "Jacobus Westervelt Sr.",
                    "born Sep 7, 1712, Hackensack, Bergen County, New Jersey; died Dec 6, 1743, Closter, Bergen County, New Jersey",
                    "CONFIRMED. Son of Jan Westervelt and Dirckje Blauvelt. Died young at age 31, leaving his son "
                    "Jacobus Jr. (future massacre victim) only ~6 years old. "
                    "Will (Dec 6, 1743, New York Wills Lib. D, p.108) left estate to wife Deborah and sons Jacobus and "
                    "Isaac; each son to pay £25 to sister Dirckje. Also recorded as 'James Westervelt' and 'Jacobus Van Westervelt Sr.' "
                    "Married Debora Van Schywen on Dec 28, 1733, Schraalenburgh, Bergen County, NJ. "
                    "Source: GSBC Family Files p1817; WikiTree Westervelt-41; research/81-westerfield-extended-research.json.",
                    gen=5, century=18, confidence="confirmed",
                    spouse="Debora Van Schywen (born ~Nov 10, 1717, Bergen County, NJ; married Dec 28, 1733, Schraalenburgh, NJ)",
                    children=[N(
                        "Jacobus (James) Westervelt / Westerfield",
                        "born Jul 1, 1737, Tappan, Bergen County, New Jersey; KILLED Jun 27, 1780, near Thixton, Jefferson County, Kentucky — WESTERFIELD MASSACRE",
                        "CONFIRMED. Hunter's 9th great-grandfather (maternal Westerfield line). "
                        "Killed in the Westerfield Massacre — one of the most documented Indian attacks on Dutch settlers in "
                        "Kentucky history (documented by Theodore Roosevelt in 'The Winning of the West, Vol.2'). "
                        "A Shawnee-allied party attacked a group of ~30 Dutch settlers traveling the Wilderness Road from "
                        "Louisville toward Harrodsburg. Jacobus was killed; his daughters Deborah and Polly were taken captive "
                        "(recovered via Fort Detroit/Quebec); his wife Maria survived by hiding in a sinkhole. "
                        "His son James Jr. (Hunter's ancestor) had stayed to serve in the Revolution and was NOT present. "
                        "Served in Revolution: Corporal, Col. John Freer's 4th & 5th Regiments, Dutchess County NY Militia; "
                        "likely present at Battle of Brooklyn Heights, Aug 27, 1776. "
                        "Married Maria DeMaree / Demarest (born Oct 19, 1735, Schraalenbergh, NJ; died Feb 1799, Jefferson Co., KY) "
                        "on Nov 5, 1754, Schraalenbergh, Bergen County, NJ. "
                        "Source: WikiTree Westervelt-42; dutchcousins.org Westerfield PDF; Bullitt County History; research/81-westerfield-extended-research.json.",
                        gen=6, century=18, confidence="confirmed",
                        is_notable=True,
                        spouse="Maria DeMaree / Demarest (born Oct 19, 1735, Schraalenbergh, NJ; died Feb 1799, Jefferson County, KY)",
                        children=[N(
                            "James Jacobus Westerfield Esq.",
                            "born Aug 15, 1755, Utrecht / New Utrecht, Long Island, New York; died Jun 1, 1826, Mercer County, Kentucky",
                            "Hunter's maternal great-great-great-great-great-great-great-grandfather. Dutch origin — the family "
                            "anglicized the surname Westervelt to Westerfield upon settling in Kentucky. "
                            "Survived his father's 1780 massacre because he was serving in the Revolution. "
                            "Served as Corporal, Dutchess County NY Militia; Battle of Brooklyn Heights, Aug 27, 1776 "
                            "(largest battle by troop count in the Revolutionary War). NSSAR Ancestor #P316901. "
                            "Married Phoebe Cozine (born Dec 9, 1759, Readington, Somerset County, NJ; died before Jun 19, 1846, "
                            "Harrodsburg, Mercer County, KY) — daughter of Rev. Cornelius Cozine (~1718–1786, Dutch Reformed "
                            "minister, Conewago Colony PA) and Antje (Anna) Staats (~1722–1775). "
                            "The Westervelt/Westerfield family is one of the oldest documented Dutch families in America, "
                            "arriving in New Amsterdam in 1662 — over 400 years ago. "
                            "Source: WikiTree Westerfield-59; dutchcousins.org; Walls Doris GEDCOM; research/81-westerfield-extended-research.json.",
                            gen=7, century=18, confidence="confirmed",
                            spouse="Phoebe Cozine (born Dec 9, 1759, Readington, Somerset County, New Jersey; died before Jun 19, 1846, Harrodsburg, Mercer County, Kentucky; "
                                   "parents: Rev. Cornelius Cozine ~1718–1786 + Antje (Anna) Staats ~1722–1775)",
                            children=[N(
        "Cornelius Westerfield",
        "born Feb 1, 1782, Harper's Ferry, Jefferson County, West Virginia; died Jul 30, 1852, Whitesville, Ohio County, Kentucky",
        "Son of James Jacobus Westerfield and Phoebe Cozine. Founded Westerfield Bourbon distillery in Daviess County, "
        "Kentucky ~1810 — one of the founders of Kentucky's bourbon whiskey industry. "
        "Married Elizabeth Bruce (born Oct 27, 1786, Coxes Creek, Nelson County, Kentucky; "
        "died Sep 6, 1852, Whitesville, Daviess County, Kentucky). "
        "Elizabeth's parents: James Bruce (born Apr 2, 1760, Brucetown, Frederick County, Virginia; died 1835, "
        "Corydon, Harrison County, Indiana) and Mary Polly Runyan (born May 27, 1761, Frederick County, Maryland; "
        "died Feb 4, 1836, Corydon, Harrison County, Indiana). Cornelius settled in Ohio County, Kentucky. "
        "Source: Walls Doris GEDCOM; research/81-westerfield-extended-research.json.",
        gen=8, century=18, confidence="confirmed",
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
                                                "Rachel Trifon",
                                                "living, USA",
                                                "Hunter's mother. Daughter of David A. Trifon. "
                                                "Source: Hunter Spence (direct family knowledge).",
                                                gen=8, century=20, confidence="confirmed",
                                                id_="p999",
                                                children=[N(
                                                    "Hunter Spence",
                                                    "living, USA",
                                                    "Subject of this family history. Son of Rachel Trifon (maternal) and Dale William Spence Jr. (paternal). "
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
        )]  # closes Joel Hayden Westerfield Sr. children / Cornelius children
    )]      # closes Cornelius Westerfield children / James Jacobus children
)]          # closes James Jacobus Westerfield Esq. children / Jacobus 1737 children
)]          # closes Jacobus (James) Westervelt 1737 children / Jacobus Sr. children
)]          # closes Jacobus Westervelt Sr. children / Jan Westervelt children
)]          # closes Jan Westervelt children / Lubbert Lubberts Jr. children
)]          # closes Lubbert Lubberts Jr. children / Lubbert immigrant children
)]          # closes Lubbert Lubbertsen (immigrant) children / root children
)           # closes WESTERFIELD_TREE = N(Lubbert Van Westervelt ...)
_wester_label = "MATERNAL — Westerfield/Trifon line (Lubbert Van Westervelt, Meppel NL ~1619 → Lubbert Lubbertsen 1662 immigrant New Amsterdam → Lubbert Jr. ~1658 → Jan ~1686 → Jacobus Sr. 1712 → Jacobus 1737 KILLED MASSACRE → James Jacobus 1755 Long Island NY → Cornelius 1782 WV → Joel Sr. 1811 KY → Joel Jr. 1853 KY → Iris 1919 AR → David Trifon → Rachel → Hunter)"
if not replace_tree("Westerfield/Trifon", WESTERFIELD_TREE, new_label=_wester_label):
    add_tree(_wester_label, WESTERFIELD_TREE)


# ═══════════════════════════════════════════════════════════════════════════
# PADGETT ANCESTORS — Bertie Jane Padgett's lineage (Jesse Westerfield's wife)
# Source: Frances Padgett GEDCOM, Walls Doris GEDCOM
# ═══════════════════════════════════════════════════════════════════════════

PADGETT_TREE = N(
    "Benjamin Padgett (Sr.)",
    "born ~1676, Calvert County, Maryland; died Jun 13, 1727, Charles County, Maryland",
    "CONFIRMED. Hunter's maternal 7x great-grandfather (Padgett line). "
    "Tobacco planter, Charles County, MD. Will (1727) left 'Wallnut Thicket' to son William and "
    "'Paggets Purches' to son Benjamin; wife Mary named executrix. Witnesses: Henry Acton Sr., "
    "Stephen Cawood Jr., Henry Acton Jr. (the Cawood witness confirms family connection to "
    "Elizabeth Cawood, first wife of his son John I). His father was William Padgett (~1656, Calvert Co MD). "
    "Source: Charles County MD will 1727; colonial-settlers-md-va.us; WikiTree Padgett-471; "
    "research/83-padgett-extended-research.json.",
    gen=1, century=17, confidence="confirmed",
    spouse="Mary Stevens/Stephens (~1680–~1740, Charles County, Maryland)",
    children=[N(
        "John I. Padgett",
        "born Sep 9, 1723, Charles County, Maryland; died Jun 2, 1811, Hope, Forsyth County, North Carolina",
        "CONFIRMED. Hunter's maternal 6x great-grandfather (Padgett line). "
        "Recorded his own birth date in a memoir (Moravian archives, 1811): 'was a little more than 3 years "
        "old when his father died' — confirms father Benjamin died 1727. "
        "Private in Captain Elias Delashmutt's Company, Maryland Militia (French & Indian War, Aug 1757). "
        "Leased 50 acres at Carroll's Manor, Frederick County MD, 1767–1774. Among first settlers from "
        "Frederick County MD to Hope community near Wachovia, NC (spring 1775) — Moravian church member. "
        "Had 12 children across two marriages. "
        "Source: John Padgett memoir 1811 (Moravian archives); colonial-settlers-md-va.us I54757; "
        "Marylanders to Carolina, Henry C. Peden Jr.; research/83-padgett-extended-research.json.",
        gen=2, century=18, confidence="confirmed",
        spouse="Elizabeth Cawood (~1730–~1756, Carrolls Manor, Prince George's County, Maryland; first wife, married ~1746); "
               "Mary Thrasher (1734–1787, NC; second wife, married Aug 25, 1759, Frederick County MD)",
        children=[N(
    "Benjamin Padgett",
    "born Sep 15, 1755, Frederick County, Maryland; died ~Aug 1794, Stokes County, North Carolina",
    "PROBABLE. Hunter's maternal 5x great-grandfather (Padgett line). Father of William Riley Padgett. "
    "WikiTree Padgett-1375 notes 'no PROOF of any of Benjamin Padgett's children, but circumstantial "
    "evidence suggests William' was his son; 1790 Stokes NC census corroborates family presence there. "
    "Benjamin's father died 1794; widow Mary Spruill moved family (incl. son William Riley ~age 16) to "
    "Madison County, KY ~1799. "
    "Source: WikiTree Padgett-1375; colonial-settlers-md-va.us; fmoran.com/padgett.html; "
    "research/83-padgett-extended-research.json.",
    gen=3, century=18, confidence="probable",
    spouse="Mary (Spruill) Padgett (~1755, North Carolina)",
    children=[N(
    "William Riley Padgett",
    "born ~1783, Stokes County, North Carolina; died Oct 20, 1824, Howard County, Missouri",
    "Hunter's maternal 5x great-grandfather (Padgett line). Father of John Jefferson Padgett. "
    "Correct birth: Stokes County, NC ~1783 (WikiTree Padgett-1375, citing 1790 Stokes NC census; "
    "prior record incorrectly said 'Virginia 1785'). "
    "Married Hannah Evans (~1776–1859, NC) on Feb 24, 1804, Madison County, Kentucky "
    "(FamilySearch ark:/61903/1:1:V5ZZ-3L8 — primary source KY county marriage record). "
    "The 'Anne Casey' wife in prior GEDCOM record is unverified and likely an error — "
    "Hannah Evans is documented by primary source. "
    "Died Howard County, Missouri Oct 20, 1824, aged ~41; buried Wesley Chapel Cemetery, "
    "Armstrong, Howard County, MO (Find a Grave #179637990; Howard County Probate Records 1821–1833). "
    "Source: WikiTree Padgett-1375; FamilySearch marriage record; research/83-padgett-extended-research.json.",
    gen=4, century=18, confidence="probable",
    spouse="Hannah Evans (~1776–1859, North Carolina; married Feb 24, 1804, Madison County, Kentucky)",
    children=[N(
        "John J. Padgett (Pagett)",
        "born ~1808, Madison County, Kentucky; died Aug 14, 1873, Independence County, Arkansas",
        "Hunter's maternal 4x great-grandfather (Padgett line). CORRECTED birthplace: Madison County, "
        "Kentucky (1850 census shows 'born KY', age 42; prior tree had 'Indiana' — Indiana is where "
        "he lived in 1850, not where he was born). Father William Riley died 1824 in Missouri; the "
        "family migrated KY→MO→Indiana. First wife: Mary Ann O'Connor (PA-born, seen in 1850 census). "
        "Second wife: Amanda Goad/Sleydan (married Sep 24, 1861, Independence County, AR). "
        "Died Aug 14, 1873, buried Hopewell Cemetery, Cord, Independence County, Arkansas. "
        "Source: WikiTree Padgett-3067; 1850 Jennings IN census; 1860 Independence AR census; "
        "Frances Padgett GEDCOM; research/83-padgett-extended-research.json.",
        gen=5, century=19, confidence="confirmed",
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
)]  # closes William Riley Padgett children / Benjamin Padgett children
)]  # closes Benjamin Padgett children / John I. Padgett children
)]  # closes John I. Padgett children / Benjamin Padgett Sr. children
)
_padgett_label = "MATERNAL — Padgett ancestors (Benjamin Padgett Sr. ~1676 Calvert MD → John I. Padgett 1723 Charles MD → Benjamin 1755 Frederick MD → William Riley Padgett ~1783 Stokes NC → John J. Padgett 1808 Madison KY → William Miller 1862 AR → Bertie Jane 1888 AR)"
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
                        "Rachel Trifon",
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
    "George Ballentine Sr.",
    "born ~1635–1636, Selkirkshire, Scotland; died ~May 1702, Norfolk County, Colony of Virginia",
    "PROBABLE Scottish immigrant ancestor of the Ballentine line. The Ballantyne/Ballentine surname is "
    "definitively Scottish, from the lands of Bellenden in Selkirkshire/Roxburghshire (Gaelic: 'baile an "
    "deadhain' — 'the dean's farmstead'). First confirmed American Ballentine: arrived as indentured servant, "
    "recorded in Lower Norfolk County, Virginia court records Feb 4, 1652/53 ('George Valentine servant of "
    "Christopher Burrow deceased, having three more years to serve'). By June 1662 he married Frances Yates "
    "in Lower Norfolk County, VA. Had 11 children including George Jr., Thomas, William, John, Alexander, "
    "Richard, Daniel, David, Frances, Mary, Dorothy. The Norfolk Virginia Ballentine dynasty is documented "
    "through the late 1700s. Connection to Hunter's John Ballentine (~1800, VA/NC) is probable but unproven — "
    "specific bridging generation (~1760–1780) not yet identified. "
    "The Ballantyne surname appears in the Ragman Rolls of 1296 as 'Ballendyn' — swearing fealty to Edward I. "
    "Source: WikiTree Ballentine-40; Geni.com George Ballentine Sr.; momslookups.com/generations/ballentine.html; "
    "research/82-ballentine-extended-research.json.",
    gen=1, century=17, confidence="probable",
    is_immigrant=True, country_flag="🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    spouse="Frances Yates (married June 1662, Lower Norfolk County, Virginia)",
    children=[N(
    "John Ballentine",
    "born ~1770–1800, likely Virginia or North Carolina",
    "Earliest confirmed Ballentine ancestor in Hunter's direct line. Married Betty Ducatt (NOT Sallie "
    "Culbertson — that is a later generation). Sallie Culbertson married David Wyle Ballentine, two "
    "generations below. Parents unknown as of 2026-04-27 research. Most probable origin: Norfolk County, "
    "Virginia Ballentine line descending from George Ballentine Sr. (Scottish immigrant, ~1636–1702). "
    "Source: M.P. GEDCOM (1st cousin 2x removed or half great-grandaunt, maternal side).",
    gen=2, century=18, confidence="probable",
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
)]  # closes John Ballentine children / George Ballentine Sr. children
)
_ballentine_label = "MATERNAL — Ballentine ancestors (George Ballentine Sr. ~1636 Selkirkshire Scotland → Norfolk VA → John Ballentine ~1800 VA → David d.1838 Gibson TN → John Wallace 1826 NC → David Wyle 1856 Ozark AR → Harold Ballentine → David Trifon)"
if not replace_tree("Ballentine ancestors", BALLENTINE_TREE, new_label=_ballentine_label):
    add_tree(_ballentine_label, BALLENTINE_TREE)

# Descent chain: David A. Trifon → Rachel → Hunter (for Ballentine tree)
def _add_hunter_to_ballentine(node):
    """Find David A. Trifon with no children, add Rachel → Hunter chain."""
    if "David A. Trifon" in node.get("name", "") and not node.get("children"):
        node["children"] = [N(
            "Rachel Trifon",
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
    "Unnamed Covenanter Culbertson",
    "b. ~1640, Morebattle, Roxburghshire, Scotland; fl. ~1665–1690",
    "POSSIBLE. One of three Covenanter brothers who fled Scotland to Ulster ~1665–1690 "
    "during persecution under James II; settled Ballygan, County Antrim, founding 'Culbertson Row'; "
    "defended Londonderry 1689; surname Culbertson from Morebattle, Roxburghshire — "
    "family documented there since ~1400; 'John de Culbertson' in Ragman Rolls 1296. "
    "Source: Lewis R. Culbertson 1923 genealogy; 92-culbertson-scots-irish.json.",
    gen=1, century=17, confidence="possible",
    is_immigrant=True, country_flag="🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    children=[N(
        "Joseph Culbertson of Ballygan",
        "b. ~1689, Ballygan near Ballymoney, County Antrim, Ireland; d. ~1726, Ireland",
        "POSSIBLE. Patriarch of Ballygan/Ballymoney Culbertson Row; probable father of "
        "Capt. Alexander 'Irish' Culbertson; Lewis Culbertson 1923 genealogy documents "
        "Burke County NC as Irish Culbertson line. "
        "Source: culbertsonmansion.us; RootsWeb Culbertson families; 92-culbertson-scots-irish.json.",
        gen=2, century=17, confidence="possible",
        children=[N(
    "Capt. Alexander 'Irish' Culbertson",
    "born ~1748, County Antrim or County Tyrone, Ireland (Scots-Irish); emigrated to Burke County, North Carolina ~1773",
    "PROBABLE. Scots-Irish; emigrated ~1773 to Burke County NC where Jeremiah Culbertson (b.1782) was born; "
    "probable father of Jeremiah; parallel: William Cuthbertson Sr. (b.1740 County Tyrone, d.1838 Burke Co NC) "
    "confirms Irish Culbertsons in Burke County this exact era. "
    "NOTE: NOT the Capt. Alexander Culbertson (1714–1756) who died at Sideling Hill, PA — "
    "that man died before Jeremiah's birth. They are likely cousins from the same Ballygan community. "
    "Source: Culbertson family genealogy; 92-culbertson-scots-irish.json.",
    gen=3, century=18, confidence="probable",
    is_immigrant=True, country_flag="🇮🇪",
    children=[N(
        "Jeremiah Culbertson",
        "born 1782, Burke County, North Carolina",
        "Son of Capt. Alexander Culbertson. Born NC after family emigrated from Ireland. "
        "WikiTree Culberson genealogy confirms 'Jeremiah Culberson born 17 Dec 1782 in Burke County, NC.' "
        "Source: web research, Culbertson family records; 92-culbertson-scots-irish.json.",
        gen=4, century=18, confidence="probable",
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
    )]
    )]
)
if not replace_tree("Culbertson ancestors", CULBERTSON_TREE):
    add_tree(
        "MATERNAL — Culbertson ancestors (Covenanter ~1640 Morebattle Scotland → Joseph of Ballygan ~1689 County Antrim → Capt. Alexander 'Irish' Culbertson ~1748 → Jeremiah 1782 NC → Allen Turner 1820 GA → Sallie Culbertson 1864 AL → Ballentine line)",
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
                        "Rachel Trifon",
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
    "Richard Goad (Goard / Gorde / Goade)",
    "born ~1617–1618, England (possibly Lancashire or Cornwall); died Sep 27, 1683, Roxbury, Suffolk, Massachusetts Bay Colony",
    "CONFIRMED. Hunter's earliest confirmed Goad ancestor — IMMIGRANT. Sailed Apr 29 / May 6, 1635 "
    "on the ship Elizabeth and Ann from London to New England during the Puritan Great Migration "
    "(age listed as 17 on passenger manifest). Settled Roxbury, Suffolk, Massachusetts. "
    "Married Phoebe Hewes on Nov 30, 1639 in Roxbury (Phoebe died Feb 28, 1678/9, 'of the pox'). "
    "Children: Hannah (1641), John (1643) — Hunter's direct ancestor, Mary (1644), Phoebe (1646), "
    "Joseph (1647), Lydia (1652), Benjamin (1654). Later relocated from Massachusetts to Virginia "
    "(Lancaster County area). Will (Sep 18, 1683) left everything to son Joseph with small legacies "
    "to daughters Phoebe Andrews and Lydia Twitchell. Name spelled variously: Goard, Gorde, Goade, Goode, Goad. "
    "English origins listed as 'unknown' by Robert Charles Anderson's Great Migration Directory p.132. "
    "Source: WikiTree Goard-80; Anderson, Great Migration Series 2 vol.3 p.78; Roxbury church records; "
    "Elizabeth and Ann passenger manifest 1635; research/84-goad-extended-research.json.",
    gen=1, century=17, confidence="confirmed",
    is_immigrant=True, country_flag="🇬🇧",
    spouse="Phoebe Hewes (~1620, England; died Feb 28, 1678/9, Roxbury, Massachusetts, of smallpox)",
    children=[N(
        "John Goad",
        "born 1643, Lancaster County, Virginia (or Massachusetts Bay Colony); died June 1666, Virginia",
        "PROBABLE. Son of Richard Goad (the immigrant) and Phoebe Hewes. "
        "Died young at ~age 23, leaving son Abraham as infant. "
        "Some sources list him as born in Massachusetts Bay Colony before the family relocated to Virginia. "
        "Married Ann [Unknown] — name beyond 'Ann' is not recorded. "
        "Source: millerdotson.tripod.com Goad Family Connections; joepayne.org/aol/phillips/goad1.htm; "
        "research/84-goad-extended-research.json.",
        gen=2, century=17, confidence="probable",
        spouse="Ann [Unknown]",
        children=[N(
            "Abraham Goad Sr.",
            "born ~1665, Lancaster County, Virginia; died Apr 11, 1734, North Farnham Parish, Richmond County, Virginia",
            "CONFIRMED. Hunter's maternal 7x great-grandfather (Goad line). Tobacco planter, Richmond County, VA. "
            "In Lancaster County by 1682; settled Moratico Creek, north bank Rappahannock River after marriage. "
            "Will (March 7, 1733; proved July 1, 1734) names wife Catherine and children. "
            "Name commonly recorded as 'Goard' in contemporary records. "
            "NOTABLE CONNECTION: Abraham Goad Sr. was great-grandfather of John Sevier (1745–1815), "
            "first governor of Tennessee, through his daughter Hannah Goad who married [Sevier]. "
            "Married Katherine Williams (~1668–1674, North Farnham Parish, Richmond County, VA; died May 23, 1741) ~1692. "
            "Source: FamilySearch LY74-D3G; WikiTree Goad-21; Abraham Goad will 1734; Haas (1983) 'The Goads'; "
            "Lancaster County VA tithable records 1687; research/84-goad-extended-research.json.",
            gen=3, century=17, confidence="confirmed",
            spouse="Katherine Williams (born ~1668–1674, North Farnham Parish, Richmond County, Virginia; died May 23, 1741; "
                   "parents: John Williams (died ~1681) and Eve [Unknown] Smyth)",
            children=[N(
    "John Goad Sr.",
    "born Nov 27, 1700, North Farnham Parish, Richmond County, Virginia; died after 1771, Bedford County, Virginia",
    "Hunter's maternal 6x great-grandfather (Goad line). Early Virginia colonist, North Farnham Parish, Richmond County. "
    "TWO marriages: (1) Katherine Jennings (married 1722) — children Joannah, Elizabeth, John Jr. (1729), Hannah, William, Ann. "
    "(2) Ann Isham (married Aug 11, 1734, Brunswick County, VA — SECOND wife, NOT Katherine Jennings). "
    "CORRECTION: The prior tree listed 'Hannah Ann Isham' as spouse — all primary sources record her as "
    "'Ann Isham' or 'Anne Isham' (born ~1699, Farnham, Richmond, VA; died 1771, Bedford County, VA). "
    "The 'Hannah Ann' formulation was a data corruption in the source GEDCOM. "
    "John Goad Jr. (1729) was the son of the FIRST wife, Katherine Jennings — NOT Ann Isham. "
    "Source: Haas (1983) 'The Goads - A Pioneer Family' pp.008-009; FamilySearch LC5N-Q8V; "
    "John Goad Sr. will (1771, Bedford County VA, Will Book 1 p.132); research/84-goad-extended-research.json.",
    gen=4, century=17, confidence="probable",
    spouse="Katherine Jennings (first wife, married 1722, died before 1741); "
           "Ann Isham (second wife, born ~1699, Farnham, Richmond County, VA; married Aug 11, 1734, Brunswick County, VA; died 1771, Bedford County, VA)",
    children=[N(
        "John Goad Jr.",
        "born Jul 1, 1729, North Farnham Parish, Richmond County, Virginia; died ~1792–1795, Sullivan County, Virginia",
        "Son of John Goad Sr. and his FIRST wife Katherine Jennings (NOT Ann Isham). "
        "Born before his father's second marriage (1734) — confirmed as Katherine Jennings' son. "
        "Married Margaret Chiles approximately 1748. Margaret is the daughter of Henry Chiles II "
        "(1698–1746, New Kent VA) and Anna Harrelson; and granddaughter of Captain John Henry Chiles Sr. "
        "(1671–1719, Jamestown VA) and great-granddaughter of Walter Chiles I (English immigrant to "
        "Jamestown, arrived before 1638 — Jamestown Society qualifying ancestor). "
        "Source: genealogy.com Goad forum; MontyHistNotes family group sheet F80; research/84-goad-extended-research.json.",
        gen=5, century=18, confidence="probable",
        spouse="Margaret Chiles (born ~1730, Virginia; daughter of Henry Chiles II (1698–1746 New Kent VA) + Anna Harrelson; "
               "granddaughter of Capt. John Henry Chiles Sr. (1671–1719 Jamestown); great-granddaughter of Walter Chiles I, English immigrant to Jamestown pre-1638)",
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
)]  # closes John Goad Jr. children / John Goad Sr. children
)]  # closes John Goad Sr. children / Abraham Goad Sr. children
)]  # closes Abraham Goad Sr. children / John Goad (1643) children
)
_goad_label = "MATERNAL — Goad ancestors (Richard Goad immigrant 1635 New England → John Goad 1643 VA → Abraham Goad Sr. 1665 Richmond VA → John Goad Sr. 1700 North Farnham VA → John Jr. 1729 VA → Thomas 1770 Bedford VA → Caleb Goad 1792 VA → Amanda Goad 1830 Graves KY)"
if not replace_tree("Goad ancestors", GOAD_TREE, new_label=_goad_label):
    add_tree(_goad_label, GOAD_TREE)

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
                                "Rachel Trifon",
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
    "James Ward",
    "ca. 1650 — after 1696, Chowan County, North Carolina",
    "PROBABLE. Earliest documented Ward ancestor in Hunter's maternal line. "
    "Documented in Chowan County, NC records 1694–1696: administered estate of Richard Stibell (with wife Hannah, "
    "1694/95 probate). On Grand Jury 1696. Land grant on Yeopim River Bridge area. "
    "Children Michael Ward and Thomas Ward documented in Chowan County probate records. "
    "The Ward surname is English occupational (warden/guardian), originating primarily from Yorkshire/Derbyshire. "
    "Probable origin: arrived Virginia ~1640s–1650s; family migrated VA→NC. "
    "Source: Chowan County probate abstracts; NC Historical and Genealogical Register; "
    "sallysfamilyplace.com/maple-lawn/james-ward-first-wife/; research/85-ward-extended-research.json.",
    gen=1, century=17, confidence="probable",
    spouse="Hannah [Unknown] (documented 1694/95 Chowan County probate — administered Richard Stibell estate with James Ward)",
    children=[N(
        "Michael Ward Sr.",
        "born before 1674; died ~1757–1758, Chowan/Bertie County, North Carolina",
        "PROBABLE. Son of James Ward (ca.1650). Documented in Chowan Indian land conveyances 1733–1735: "
        "received 300 acres on Katharine Creek (1733) and 600 acres near new Poly Bridge (1734). "
        "In 1714: Michael, Ann, and Hannah Ward witnessed a Norfolk County VA will. "
        "Children include: Michael Ward Jr. (Hertford Co), James Ward (Bertie Co), Richard Ward (Carteret Co). "
        "WikiTree (Ward-1068) shows Michael Ward Sr. bef.1674–1758 as grandfather of James Ward (1770, Bertie Co). "
        "Source: NC Native Heritage Project (Chowan Indian Land Conveyances); Sally's Family Place; "
        "WikiTree Ward-1068; research/85-ward-extended-research.json.",
        gen=2, century=17, confidence="probable",
        children=[N(
            "John Ward Sr. (Tyrrell County)",
            "born ~1705–1715, Tyrrell County, North Carolina; died ~1750, Tyrrell County, NC",
            "PROBABLE. Son of Michael Ward Sr. Will of John Ward, Tyrrell County, NC, dated Mar 5, 1748/9, "
            "proved September 1750. Named children in will: Michael Ward (son), John Ward (son — received "
            "'negro Tom' + cattle), David Ward (son — received 180-acre plantation), Elizabeth Noble (daughter "
            "— received 140-acre plantation), Dorcas Overstreet (daughter — received 100 acres on Catankne). "
            "Tyrrell County was formed from the Chowan County area — consistent with family's Chowan roots. "
            "Source: NC GenWeb Tyrrell County — Will of John Ward (ncgenweb.us/tyrrell/WARD1749.HTM); "
            "research/85-ward-extended-research.json.",
            gen=3, century=18, confidence="probable",
            children=[N(
    "John Ward",
    "born ~1748, Chowan/Tyrrell County area, North Carolina",
    "Hunter's maternal 5x great-grandfather (Ward line). Born colonial North Carolina, Chowan/Tyrrell County area. "
    "May be the son 'John Ward' named in the Tyrrell County will of John Ward Sr. (1748/9) who received "
    "'a negro man named Tom' and cattle. His birth year ~1748 matches the will date exactly. "
    "Migrated south into South Carolina — family migration pattern consistent with post-Revolution land opening. "
    "Source: web research, colonial North Carolina records; research/85-ward-extended-research.json.",
    gen=4, century=18, confidence="probable",
    spouse="Catherine Ward (born ~1750, North Carolina, estimated)",
    children=[N(
        "Thomas S. Ward",
        "born ~1775–1785, Darlington/Pendleton area, South Carolina (date uncertain — Darlington records burned 1785–1806)",
        "Son of John Ward and Catherine Ward. CORRECTED birth year: cannot be born 1760 if father John Ward "
        "was born ~1748 (he would be only ~12). Birth more likely ~1775–1785. Darlington District records "
        "were burned making verification very difficult. Migrated to Pendleton, Anderson County SC. "
        "Source: web research, South Carolina census records; research/85-ward-extended-research.json.",
        gen=5, century=18, confidence="probable",
        spouse="Nancy Crompton (born ~1775, estimated; possibly NC Compton family)",
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
)]  # closes John Ward (1748) children / John Ward Sr. (Tyrrell) children
)]  # closes John Ward Sr. (Tyrrell) children / Michael Ward Sr. children
)]  # closes Michael Ward Sr. children / James Ward (ca.1650) children
)
_ward_label = "MATERNAL — Ward ancestors (James Ward ca.1650 Chowan NC → Michael Ward Sr. bef.1674 → John Ward Sr. Tyrrell NC ~1705 → John Ward ~1748 → Thomas ~1775 SC → John Robert 1804 Pendleton SC → Joseph 1833 TN → Frances Ward 1868 Strawberry AR)"
if not replace_tree("Ward ancestors", WARD_TREE, new_label=_ward_label):
    add_tree(_ward_label, WARD_TREE)

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
                            "Rachel Trifon",
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
# UPDATE RAU TREE — Frances Virginia (Rau) Henslee confirmed dates & burial
# Source: research/80-rau-extended-research.json (wave-1 research)
# ═══════════════════════════════════════════════════════════════════════════

def _update_frances_rau(node):
    """Walk Rau tree; update Frances Virginia node with confirmed facts."""
    if "Frances Virginia" in node.get("name", "") and "Henslee" in node.get("name", ""):
        node["dates"] = "January 1, 1918 – December 19, 2008"
        node["fact"] = (
            "born Texas; died Nederland, Jefferson County TX; "
            "buried Forest Lawn Memorial Park, Beaumont TX; "
            "Catholic parishioner St. Charles Borromeo, Nederland; "
            "parents unidentified — Texas Death Certificate DSHS order required to unlock "
            "this line. Maiden name RAU confirmed via cousin GEDCOM. "
            "m. Lee Stuart Henslee (1908-10-02 – 1994-08-31), also buried Forest Lawn. "
            "Source: research/80-rau-extended-research.json; PeopleLegacy; Find A Grave #39700994."
        )
        return True
    return any(_update_frances_rau(c) for c in node.get("children", []))

_rau_root = get_tree("Rau line")
if _rau_root:
    _update_frances_rau(_rau_root)


# ═══════════════════════════════════════════════════════════════════════════
# MATTINGLY PRIMARY TREE — Wave-2 corrections
# Source: research/91-mattingly-english-origins.json
# ═══════════════════════════════════════════════════════════════════════════

def _insert_william_mattyngle(node):
    """Insert William Mattyngle (~1480) between the documentary gap and Henry MATYNGLE."""
    if "[~250-year documentary gap]" in node.get("name", ""):
        children = node.get("children", [])
        # Check if William is already present (idempotency guard)
        for c in children:
            if "William Mattyngle" in c.get("name", ""):
                return True
        # Find Henry MATYNGLE among the gap's children
        henry_idx = None
        for i, c in enumerate(children):
            if "Henry MATYNGLE" in c.get("name", ""):
                henry_idx = i
                break
        if henry_idx is not None:
            henry_node = children[henry_idx]
            william_node = {
                "name": "William Mattyngle",
                "dates": "b. ~1480, Mattingley village, Hampshire, England; fl. 1483",
                "fact": (
                    "POSSIBLE. Named in a 1483 mortgage document (HRO 19M61/153) "
                    "for land in Mattingley, Hampshire — the earliest surviving record "
                    "of the Mattingly surname. Probable father of Henry Matyngle "
                    "(who married Heckfield Hampshire 1548 and left will 1566). "
                    "The Mattingley estate/village in Hampshire is the origin point "
                    "of the entire Mattingly surname. "
                    "Source: research/91-mattingly-english-origins.json."
                ),
                "id": None,
                "generation": 8,
                "century": 15,
                "confidence": "possible",
                "spouse": None,
                "children": [henry_node],
                "country_flag": "\U0001f1ec\U0001f1e7",
            }
            children[henry_idx] = william_node
            node["children"] = children
            return True
    return any(_insert_william_mattyngle(c) for c in node.get("children", []))


def _fix_thomas_mattingly_birthplace(node):
    """Correct Thomas Mattingly I birthplace from Sussex to Hampshire."""
    if "Thomas Mattingly I" in node.get("name", ""):
        fact = node.get("fact", "")
        if "Sussex" in fact:
            node["fact"] = fact.replace(
                "Born Sussex England",
                "Born Hampshire, England (exact parish unknown — data artifact corrected)"
            )
            return True
    return any(_fix_thomas_mattingly_birthplace(c) for c in node.get("children", []))


_primary = multi.get("primary")
if _primary:
    _insert_william_mattyngle(_primary)
    _fix_thomas_mattingly_birthplace(_primary)


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
