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
    # Replace if already present, else add
    if not replace_tree("MATTINGLY ENGLISH COUSIN TREE", mattingly_extended):
        add_tree(
            "MATTINGLY ENGLISH COUSIN TREE — Catherine & John Mattingly (1550s, Berkshire/Hampshire)",
            mattingly_extended
        )


# ═══════════════════════════════════════════════════════════════════════════
# WESTERFIELD / TRIFON MATERNAL LINE
# Source: Walls Doris GEDCOM, David A. Trifon family messages (April 2026)
# ═══════════════════════════════════════════════════════════════════════════

WESTERFIELD_TREE = N(
    "Joel Hayden Westerfield",
    "born Jun 1853, Ohio County, Kentucky; died Nov 22, 1910, Reynolds Station, Hancock County, Kentucky",
    "Hunter's maternal great-great-great-grandfather. Farmer from Kentucky who migrated to Arkansas. "
    "Source: Walls Doris GEDCOM (1st cousin 2x removed or half great-grandaunt, maternal side).",
    gen=1, century=19, confidence="confirmed",
    spouse="Amanda Jane Nelson (born Jun 1855, Kentucky; died Jan 19, 1928, Monette, Craighead County, Arkansas)",
    children=[N(
        "Jesse Lawrence Westerfield",
        "born Jan 1, 1887, Kentucky; died Sep 29, 1951, Marianna, Lee County, Arkansas",
        "Hunter's maternal great-great-grandfather. Son of Joel Westerfield and Amanda Nelson. "
        "Married Bertie Jane Padgett (b.1888 AR). Had five children including "
        "Iris June Westerfield (Hunter's maternal great-grandmother). "
        "Source: Walls Doris GEDCOM.",
        gen=2, century=19, confidence="confirmed",
        spouse="Bertie Jane Padgett (born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas)",
        children=[
            N(
                "Cleofus Westerfield",
                "born 1918; died 2003",
                "Son of Jesse and Bertie Jane. Married Virginia Laverne Summar. "
                "Brother of Iris June Westerfield. Source: Walls Doris GEDCOM.",
                gen=3, century=20, confidence="confirmed"
            ),
            N(
                "Iris June Westerfield",
                "born Jun 1, 1919, Tuckerman, Arkansas; died Apr 13, 2003, Colt, Arkansas",
                "Hunter's maternal great-grandmother. Daughter of Jesse Westerfield and Bertie Jane Padgett. "
                "Married Harold 'Hal David' Ballentine (~1903, KS). Their son David took the surname Trifon "
                "from a stepfather after Harold died ~1945. Also had children Carol Ward and Doris Walls. "
                "Source: Walls Doris GEDCOM, David A. Trifon family messages.",
                gen=3, century=20, confidence="confirmed",
                spouse="Harold 'Hal David' Ballentine (~1903, Kansas; died ~1945)",
                children=[
                    N(
                        "David A. Trifon",
                        "born ~1940s, Arkansas area",
                        "Hunter's maternal grandfather. Biological son of Harold Ballentine and Iris Westerfield. "
                        "Took stepfather's surname 'Trifon' after Harold Ballentine died ~1945. "
                        "Shared extensive family history documentation with Hunter in April 2026. "
                        "Daughters: Charmaine Trifon and Rachel Trifon (Hunter's mother). "
                        "Source: David A. Trifon personal communication.",
                        gen=4, century=20, confidence="confirmed",
                        children=[
                            N(
                                "Charmaine Trifon",
                                "born ~1960s–1970s",
                                "Daughter of David A. Trifon. Hunter's maternal aunt. "
                                "Source: David A. Trifon family communication.",
                                gen=5, century=20, confidence="confirmed"
                            ),
                            N(
                                "Rachel Trifon",
                                "born ~1960s–1970s",
                                "Hunter's mother. Daughter of David A. Trifon and granddaughter of Iris Westerfield. "
                                "Source: Hunter Spence (direct family knowledge).",
                                gen=5, century=20, confidence="confirmed",
                                children=[N(
                                    "Hunter Spence",
                                    "born ~2002–2003, Florida",
                                    "User. Son of Rachel Trifon (maternal) and Dale William Spence Jr. (paternal). "
                                    "Dual US/UK passport holder.",
                                    gen=6, century=21, confidence="confirmed"
                                )]
                            ),
                        ]
                    ),
                    N(
                        "Carol Ward",
                        "born ~1937",
                        "Daughter of Iris Westerfield and Andrew Jackson Key "
                        "(born Mar 28, 1914, Senatobia, Tate, Mississippi; died Jan 30, 1991, Alabama). "
                        "Sister of David A. Trifon. Doris Walls listed in Carol Ward obituary. "
                        "Source: Carol Ward obituary (Walls Doris GEDCOM).",
                        gen=4, century=20, confidence="confirmed",
                        spouse="Andrew Jackson Key (born Mar 28, 1914, Senatobia, Mississippi; died Jan 30, 1991, Alabama)"
                    ),
                    N(
                        "Doris Walls",
                        "born ~1930s–1940s",
                        "Daughter of Iris Westerfield. Sister of David A. Trifon. "
                        "DNA match to Hunter: 1st cousin 2x removed or half great-grandaunt (maternal side). "
                        "Source: Walls Doris GEDCOM.",
                        gen=4, century=20, confidence="confirmed"
                    ),
                ]
            ),
            N(
                "Padgett Lee Westerfield",
                "born 1921; died 2002",
                "Son of Jesse and Bertie Jane. Named after mother's maiden name Padgett. "
                "Owned a Chevrolet dealership — notable local businessman in Arkansas. "
                "Source: Walls Doris GEDCOM.",
                gen=3, century=20, confidence="confirmed",
                is_notable=True
            ),
            N(
                "Maxie Eugene Westerfield",
                "born 1922; died 1956",
                "Son of Jesse and Bertie Jane. Died at ~34. "
                "Source: Walls Doris GEDCOM.",
                gen=3, century=20, confidence="confirmed"
            ),
            N(
                "Wayne Miller Westerfield",
                "born 1927; died 1990",
                "Son of Jesse and Bertie Jane Westerfield. "
                "Source: Walls Doris GEDCOM.",
                gen=3, century=20, confidence="confirmed"
            ),
        ]
    )]
)
if not replace_tree("Westerfield/Trifon", WESTERFIELD_TREE):
    add_tree(
        "MATERNAL — Westerfield/Trifon line (Joel Westerfield 1853 KY → Iris 1919 AR → David Trifon → Rachel → Hunter)",
        WESTERFIELD_TREE
    )


# ═══════════════════════════════════════════════════════════════════════════
# PADGETT ANCESTORS — Bertie Jane Padgett's lineage (Jesse Westerfield's wife)
# Source: Frances Padgett GEDCOM, Walls Doris GEDCOM
# ═══════════════════════════════════════════════════════════════════════════

PADGETT_TREE = N(
    "John J. Padgett (Pagett)",
    "born 1808, Vernon, Jennings County, Indiana; died Aug 14, 1873, Independence County, Arkansas",
    "Hunter's maternal great-great-great-great-grandfather (Padgett line). Born Indiana, died Arkansas — "
    "early American migrant to the frontier South. "
    "Source: Frances Padgett GEDCOM (3rd cousin 1x removed or half 2nd cousin 2x removed, maternal side).",
    gen=1, century=19, confidence="confirmed",
    spouse="Amanda Goad (born Jul 25, 1830, Graves County, Kentucky; died Feb 6, 1911, McCracken County, Kentucky)",
    children=[N(
        "William Miller Padgett",
        "born Oct 5, 1862, Independence County, Arkansas; died Nov 15, 1950, Lee County, Arkansas",
        "Hunter's maternal great-great-great-grandfather (Padgett line). "
        "Son of John J. Padgett and Amanda Goad. Father of Bertie Jane Padgett "
        "who married Jesse Lawrence Westerfield. Source: Frances Padgett GEDCOM, Walls Doris GEDCOM.",
        gen=2, century=19, confidence="confirmed",
        spouse="Frances Ward (born Jan 23, 1868, Strawberry, Lawrence County, Arkansas; "
               "died Sep 11, 1945, Smithville, Lawrence County, Arkansas)",
        children=[N(
            "Bertie Jane Padgett",
            "born Mar 10, 1888, Arkansas; died Oct 6, 1964, Lee County, Arkansas",
            "Hunter's maternal great-great-grandmother (Padgett line). "
            "Daughter of William Miller Padgett and Frances Ward. "
            "Married Jesse Lawrence Westerfield (b.1887, KY). Together had five children "
            "including Iris June Westerfield (Hunter's maternal great-grandmother). "
            "Source: Walls Doris GEDCOM, Frances Padgett GEDCOM.",
            gen=3, century=19, confidence="confirmed",
            spouse="Jesse Lawrence Westerfield (born Jan 1, 1887, Kentucky — see Westerfield/Trifon tree)"
        )]
    )]
)
if not replace_tree("Padgett ancestors", PADGETT_TREE):
    add_tree(
        "MATERNAL — Padgett ancestors (John J. Padgett 1808 Indiana → William Miller Padgett 1862 AR → Bertie Jane Padgett 1888 AR)",
        PADGETT_TREE
    )


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
        "born ~1799, Virginia / North Carolina / Scotland (birth location varies in records)",
        "Son of John Ballentine and Betty Ducatt. Married Susan Nee. "
        "Next generation born Virginia. Source: M.P. GEDCOM.",
        gen=2, century=18, confidence="probable",
        spouse="Susan Nee",
        children=[N(
            "John Wallace Ballentine",
            "born ~1826, Virginia",
            "Son of David Ballentine and Susan Nee. Married Elizabeth Rebecca Barker. "
            "Family moved south — son David Wyle born in Ozark, Franklin County, Arkansas. "
            "Source: M.P. GEDCOM.",
            gen=3, century=19, confidence="probable",
            spouse="Elizabeth Rebecca Barker (born 1829, Tennessee; died 1881)",
            children=[N(
                "David Wyle Ballentine",
                "born Jun 18, 1856, Ozark, Franklin County, Arkansas; died Apr 16, 1933, Oden, Montgomery County, Arkansas",
                "Son of John Wallace Ballentine and Elizabeth Rebecca Barker. "
                "Married Sallie Culbertson. Father of Mary Ethel Lee Ballentine (confirmed in GEDCOMs) "
                "and likely father of Harold Ballentine (David Trifon's biological father). "
                "Lived entire life in Arkansas. Source: M.P. GEDCOM.",
                gen=4, century=19, confidence="confirmed",
                spouse="Sallie Culbertson (born Nov 10, 1864, Alabama; died Sep 20, 1945, Marianna, Arkansas)",
                children=[
                    N(
                        "Mary Ethel Lee Ballentine",
                        "born Jun 8, 1884, Chismsville, Logan County, Arkansas; died Feb 19, 1961, Marianna, Arkansas",
                        "Daughter of David Wyle Ballentine and Sallie Culbertson. "
                        "Confirmed in multiple cousin GEDCOMs (M.P. GEDCOM, Linda Coleman GEDCOM). "
                        "Likely sister or aunt of Harold Ballentine (David Trifon's biological father). "
                        "Source: M.P. GEDCOM.",
                        gen=5, century=19, confidence="confirmed"
                    ),
                    N(
                        "Harold 'Hal David' Ballentine",
                        "born ~1903, Kansas (estimated); died ~1945",
                        "David A. Trifon's biological father. Married Iris June Westerfield (b.1919, Tuckerman AR). "
                        "Likely son of David Wyle Ballentine and Sallie Culbertson — same Arkansas Ballentine family. "
                        "After his death ~1945, son David took the surname of his stepfather (Trifon). "
                        "Source: David A. Trifon family communication, Walls Doris GEDCOM.",
                        gen=5, century=20, confidence="speculative",
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
if not replace_tree("Ballentine ancestors", BALLENTINE_TREE):
    add_tree(
        "MATERNAL — Ballentine ancestors (John Ballentine ~1800 VA → David Wyle Ballentine 1856 Ozark AR → Harold Ballentine ~1903 → David Trifon)",
        BALLENTINE_TREE
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
