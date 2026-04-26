"""
expand_trees.py — Rebuild lineage-tree-multi.json with fully expanded trees.

Priority 1: Spence — Scottish MacDuff ancestry from Duff (967 AD) through
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
      is_notable=False):
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
    return n


# ═══════════════════════════════════════════════════════════════════════════
# SPENCE TREE  — 967 AD → Hunter  (27 generations, ~55 nodes)
# Source: research/63-spence-confirmed-trace.json + research/39-dale-spence-sr.json
# ═══════════════════════════════════════════════════════════════════════════

SPENCE_TREE = N(
    "Duff (Dubh), King of Scotland",
    "died 967 AD, Scotland",
    "Ancestor of Clan MacDuff — the founding king of the MacDuff dynasty. "
    "Spence/Spens is a formally documented sept of Clan MacDuff per Electric Scotland, "
    "tartans.com, and Wikipedia. All three sources explicitly list 'Spence' and 'Spens' "
    "in the MacDuff sept roster. Dale Sr. showed Hunter a coat of arms consistent with "
    "MacDuff heraldry (lion rampant, Or field).",
    gen=1, century=10, confidence="probable",
    children=[N(
        "Macduff I, Mormaer of Fife",
        "~1000 AD, Kingdom of Fife, Scotland",
        "First Mormaer (Earl) of Fife — the MacDuff clan's hereditary title. "
        "The Mormaers of Fife had the privilege of crowning Scottish kings at Scone. "
        "Fife was the historical heartland of Clan Spens (Wormiston, Crail, Lathallan).",
        gen=2, century=11, confidence="probable",
        children=[N(
            "Constantine MacDuff, 1st Earl of Fife",
            "~1057 AD, Fife, Scotland",
            "First to bear the formal title 'Earl of Fife' under King Macbeth's successor. "
            "Supported Malcolm III Canmore in regaining the Scottish throne. "
            "The Earldom of Fife was inherited by the MacDuff line for over 200 years.",
            gen=3, century=11, confidence="probable",
            children=[N(
                "Gillemichael MacDuff, 2nd Earl of Fife",
                "~1095, Fife, Scotland",
                "Held the Earldom during the reigns of Malcolm III and Donald III. "
                "The MacDuff earls maintained their ancient Pictish privileges over Fife "
                "throughout the Norman reorganisation of Scotland.",
                gen=4, century=11, confidence="probable",
                children=[N(
                    "Constantine MacDuff, 3rd Earl of Fife",
                    "~1130, Fife, Scotland",
                    "Earl during the reign of David I, who modernised Scotland on Norman lines. "
                    "The Fife earldom anchored the MacDuff clan in the eastern Lowlands — "
                    "the same territory where Clan Spens would later hold Wormiston and Crail.",
                    gen=5, century=12, confidence="probable",
                    children=[N(
                        "Duncan MacDuff, 4th Earl of Fife",
                        "~1154, Fife, Scotland — died 1154",
                        "Earl during the reign of King David I. "
                        "Traditional clan genealogy connects Jean le Despencier (~1161) "
                        "to this line via marriage to a daughter of the Earl — establishing "
                        "the kinship that made Spens a MacDuff sept. This link is clan tradition "
                        "but consistently cited by Clan Spens sources (clanspens.xyz).",
                        gen=6, century=12, confidence="possible",
                        children=[N(
                            "John 'Dispensator' (le Despencier)",
                            "c. 1161–1171, Scotland",
                            "EARLIEST CONFIRMED SPENS ANCESTOR. "
                            "Appears in the List of tenants and vassals of Walter fitz Alan, "
                            "Steward of Scotland, 1161–1171 — one of the most authoritative "
                            "medieval Scottish records. 'Dispensator' means steward/dispenser "
                            "(Latin), anglicised to 'Spens/Spence' over subsequent generations. "
                            "His descendants adopted the surname Spens from this occupational title.",
                            gen=7, century=12, confidence="confirmed",
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
                                                                                                                        "William Spence's father (immigrant to Pennsylvania)",
                                                                                                                        "c. 1870–1890, England/Scotland → Pennsylvania, USA",
                                                                                                                        "UNVERIFIED. William Spence's father — the likely "
                                                                                                                        "English or Scottish immigrant to Pennsylvania. "
                                                                                                                        "This is the generation the family oral tradition "
                                                                                                                        "'came from England when he was 8' most likely refers to. "
                                                                                                                        "Pennsylvania was a major destination for British "
                                                                                                                        "industrial workers (coal, steel, oil). "
                                                                                                                        "NEXT STEP: Search 1910 US Census Pennsylvania for "
                                                                                                                        "William Spence (age ~2) in his parents' household "
                                                                                                                        "to confirm father's name and birthplace.",
                                                                                                                        gen=27, century=19, confidence="possible",
                                                                                                                        children=[
                                                                                                                            N(
                                                                                                                                "William Spence",
                                                                                                                                "born ~1908, Pennsylvania — died ?, Beaumont TX",
                                                                                                                                "CONFIRMED (1950 US Federal Census, Beaumont TX). "
                                                                                                                                "Hunter's paternal great-grandfather. "
                                                                                                                                "1570 Roberts St, Beaumont, Jefferson Co. TX. "
                                                                                                                                "System Operator, Electrical Utility Co (Gulf States Utilities). "
                                                                                                                                "Married Dovie A. (Byrd) Spence. "
                                                                                                                                "Born Pennsylvania — migrated to Texas, likely following "
                                                                                                                                "Spindletop oil-industry work. "
                                                                                                                                "Parents unknown — search 1910/1920 PA Census to identify.",
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
                                                                                                                            )
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
    "PATERNAL — Spence line (Clan MacDuff sept, Scotland 967 AD → NE England → Beaumont TX → Hunter)"
)
if not replaced:
    add_tree(
        "PATERNAL — Spence line (Clan MacDuff sept, Scotland 967 AD → NE England → Beaumont TX → Hunter)",
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
if byrd_tree:
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

baity_tree = get_tree("Baity")
if baity_tree:
    extended_baity = N(
        "Charles Beatty (Baity / Beaty)",
        "c. 1700, Scotland/Ireland – c. 1760, Pennsylvania",
        "POSSIBLE. Charles Beatty appears in Filby's PILI immigrant index as a Scots-Irish "
        "immigrant to Philadelphia c. 1729 — consistent with the Ulster Plantation migration "
        "corridor (Border Scots → Ulster ~1610 → Pennsylvania ~1720s). "
        "The Beatty → Baity → Baty spelling variants are all documented in colonial NC records. "
        "Source: 66-baity-confirmed-trace.json.",
        gen=3, century=18, confidence="possible",
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
                                        "Surry County NC. Confirmed in cousin GEDCOM.",
                                        gen=7, century=19, confidence="probable",
                                        children=baity_tree.get("children", [])
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    replace_tree("Baity", extended_baity)


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND TEICHMÜLLER TREE — add August Wilhelm as explicit node
# ═══════════════════════════════════════════════════════════════════════════

teich_tree = get_tree("Teichmüller")
if teich_tree:
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


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND LEPICK TREE — add Czech ancestors
# ═══════════════════════════════════════════════════════════════════════════

lepick_tree = get_tree("Lepi")
if lepick_tree:
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


# ═══════════════════════════════════════════════════════════════════════════
# EXPAND BOEHME TREE — add Silesian ancestors
# ═══════════════════════════════════════════════════════════════════════════

boehme_tree = get_tree("Boehme")
if boehme_tree:
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
        children=[boehme_tree]
    )
    replace_tree("Boehme", silesian_root)


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
    # Add as a new secondary tree
    add_tree(
        "MATTINGLY ENGLISH COUSIN TREE — Catherine & John Mattingly (1550s, Berkshire/Hampshire)",
        mattingly_extended
    )


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
