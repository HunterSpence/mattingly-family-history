"""Build a CLASSIC branching family-tree JSON: descendants of Ellis (1167).

Produces research/lineage-tree.json — a single-rooted tree with `children` arrays
at every level, including known siblings (collateral) at each generation.

build_html.py reads this file in preference to the linear 06-full-mattingly-lineage.json.
"""
import json
from pathlib import Path

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
OUT = WS / "research" / "lineage-tree.json"


def n(name, dates="", fact="", id=None, gen=0, century=0, conf="confirmed", children=None, spouse=None):
    return {
        "name": name,
        "dates": dates,
        "fact": fact,
        "id": id,
        "generation": gen,
        "century": century,
        "confidence": conf,
        "spouse": spouse,
        "children": children or [],
    }


# ── Build the tree from Ellis (1167) → Hunter, with collateral siblings at every known generation ──

# Hunter and his generation (deepest descendants — at the leaves)
hunter = n("Hunter Spence", "living", "Recipient of this family history; recorded grandma's interview", "p001", 18, 21, "confirmed")

# Hunter's parent + Charmaine (Shari's children)
hunters_parent = n("[Hunter's parent]", "living", "Shari + David's child", None, 17, 21, "confirmed", [hunter])
charmaine = n("Charmaine", "living", "Shari + David's daughter; Hunter's aunt", "p021", 17, 21, "confirmed")

# Shari + David
shari = n('Sharyn ("Shari") Mattingly', "b. 1947", "Family historian; Santa Monica; oil royalty owner", "p000", 16, 20, "confirmed",
          [hunters_parent, charmaine], spouse="David (1st husband)")

# Shari's siblings (redacted) + her father
shari_brother = n("[brother]", "living", "Got the chair from Pearl's set", "p022", 16, 20, "confirmed")
shari_sister = n("[sister]", "living", "—", "p023", 16, 20, "confirmed")

# Shari's father — agent 18 finding: STRONG candidate Leroy Baity Mattingly (b. 17 May 1922 SA, d. 2013 Colorado Springs)
shari_father = n("Leroy Baity Mattingly", "1922–2013", "Born 17 May 1922 San Antonio; died Colorado Springs CO 2013. WikiTree Mattingly-1178. m. Jennive Lepick.", "p015", 15, 20, "probable", [shari, shari_brother, shari_sister],
                 spouse="Jennive Lepick")

# Leroy Teichmuller Mattingly + Ruth Baity (and Leroy's siblings)
# CORRECTION (agent 16): Leroy born 31 Aug 1896, died 1968 SA. Ruth Baity 4 Apr 1900 - 1982 Houston.
leroy = n("Leroy Teichmuller Mattingly", "31 Aug 1896 – 1968", "Born La Grange TX; died San Antonio. U Texas engineer; named for German maternal grandfather Hans Teichmueller. m. Ruth Baity 4 Apr 1900–1982. WikiTree Mattingly-1127.", "p002", 14, 20, "confirmed",
          [shari_father], spouse="Ruth (Baity) Mattingly (4 Apr 1900 – 1982 Houston)")
claude = n("Dr. Claude Mattingly", "1898–1934", "Pediatrician; Marine WWI; suicide pact at Texan Hotel Austin Jan 31 1934", "p011", 14, 20, "confirmed")
mamie = n("Aunt Mamie", "b. ~1900", "Mother died at her birth", "p013", 14, 20, "confirmed")
edward_jr = n("Edward Mattingly Jr.", "b. ~1915 La Grange", "Half-sibling — son of Edward Sr. + 2nd wife Blanche Schroeder", None, 14, 20, "probable")

# Edward Mattingly Sr + May Teichmueller — CORRECTED: born 1868 Missouri, died 1945 La Grange
edward_sr = n("Edward Mattingly Sr.", "1868 MO – 1945 La Grange TX", "Born Missouri; migrated to TX by 1894; m. May Teichmueller 1 Sept 1894 (May d. 28 Aug 1900); m2. Blanche Schroeder", "p041", 13, 20, "confirmed",
              [leroy, claude, mamie, edward_jr], spouse="m1. May Teichmueller (1894–1900); m2. Blanche D. Schroeder (b. 1886 MO)")

# Thomas Jefferson Mattingly — Edward Sr's father; agent 18: 8 children across 2 wives
# m1. Catherine Woodward: John T. Mattingly + Sarah Alice Embree
# m2. Elizabeth Christie (1833-): Anna Bell, Noble N., Francis Ellsworth (Frank), Edward Sr., Florence, Ida
tj_children = [
    n("John T. Mattingly", "?", "Half-sibling of Edward Sr. (mother Catherine Woodward)", None, 13, 19, "probable"),
    n("Sarah Alice (Mattingly) Embree", "?", "Half-sibling of Edward Sr.; m. Embree", None, 13, 19, "probable"),
    n("Anna Bell (Mattingly) Powell", "?", "Daughter of TJ + Elizabeth Christie; m. Ezra Doty Powell 1874", None, 13, 19, "probable"),
    n("Noble N. Mattingly", "?", "Son of TJ + Elizabeth Christie", None, 13, 19, "probable"),
    n("Francis Ellsworth 'Frank' Mattingly", "?", "Son of TJ + Elizabeth Christie", None, 13, 19, "probable"),
    edward_sr,  # Direct line — already defined
    n("Florence Mattingly", "?", "Daughter of TJ + Elizabeth Christie", None, 13, 19, "probable"),
    n("Ida Mattingly", "?", "Daughter of TJ + Elizabeth Christie", None, 13, 19, "probable"),
]
thomas_jefferson = n("Thomas Jefferson Mattingly", "1828 KY – 1883 MO", "WikiTree Mattingly-591; m1. Catherine Woodward (2 kids); m2. Elizabeth Christie (6 kids); KY→MO migration", None, 12, 19, "confirmed",
                     tj_children, spouse="m1. Catherine Woodward; m2. Elizabeth Christie (b. 2 Dec 1833 Christianburg, Shelby KY)")

# Ignatius Mattingly (b. 1781 MD, d. 1833 KY) — agent 18: had 2 confirmed sons
# Sibling of TJ: Ignatius Mattingly (b. 6 Mar 1811) m. Rachel F. Barnes
ignatius_1811 = n("Ignatius Mattingly", "b. 6 Mar 1811", "Sibling of Thomas Jefferson; m. Rachel F. Barnes (WikiTree Mattingly-139)", None, 12, 19, "probable")

ignatius_1781 = n("Ignatius Mattingly", "1781 MD – 1833 KY", "Born Maryland; MD→KY migration; died there 1833. WikiTree Mattingly-140.", None, 11, 19, "confirmed",
                  [thomas_jefferson, ignatius_1811])

# Ignatius Jr. (b. 1750) m. Eleanor Shircliffe; 3 confirmed children
# Children: George, Zachariah Sr (bef.1771-abt.1823), Ignatius (1781) [half-line]
zachariah_sr = n("Zachariah Mattingly Sr.", "bef. 1771 – abt. 1823", "WikiTree Mattingly-188. Sibling of Ignatius (1781). Children: Mary, Zachariah Jr.", None, 11, 19, "confirmed",
                 [n("Mary Mattingly", "?", "Daughter of Zachariah Sr.", None, 12, 19, "probable"),
                  n("Zachariah Mattingly Jr.", "?", "Son of Zachariah Sr.", None, 12, 19, "probable")])
george_son_ig_jr = n("George Mattingly", "?", "Son of Ignatius Jr. (named on WikiTree)", None, 11, 19, "probable")

ignatius_jr = n("Ignatius Mattingly Jr.", "b. 1750", "Son of Leonard Sr.; m. Eleanor Shircliffe; direct line via Ignatius (1781) — NOT Leonard Jr.", None, 10, 18, "confirmed",
                [george_son_ig_jr, zachariah_sr, ignatius_1781],
                spouse="Eleanor Shircliffe")

# Leonard Jr. (now COLLATERAL — Y-DNA project anchor for KY descendants)
leonard_jr_children = [
    n("Mary Alvey Mattingly", "b. 1798", "Eldest of Leonard Jr.'s 4 children", None, 11, 19, "probable"),
    n("Henry Martin Mattingly Sr.", "1799–1858 Marion KY", "9 children 1828-1844; m. Helen Thompson; collateral Mattingly/Y-DNA branch", None, 11, 19, "confirmed",
      [
        n("George Thomas Mattingly", "b. 1830 Marion KY", "Y-DNA project participant; not direct Texas-line ancestor", "p046", 12, 19, "possible"),
        n("[+8 other children of Henry Martin Sr.]", "1828–1844", "Per agent 16 research", None, 12, 19, "probable"),
      ],
      spouse="Helen Thompson (b. ~1800)"),
    n("William Cissell Mattingly", "b. 1807", "Leonard Jr's third child", None, 11, 19, "probable"),
    n("Leonard Mattingly III", "1828–1914 Glen Dean KY", "Died KY at 85; ruled out as centenarian", None, 11, 19, "confirmed"),
]
leonard_jr = n("Leonard Mattingly Jr.", "1764–1843 Marion KY", "1785 Catholic migration to KY; Y-DNA project anchor — but COLLATERAL to Hunter, not direct line", "p045", 10, 18, "confirmed",
               leonard_jr_children, spouse="Ann Cissell (m. 7 Jan 1788, Nelson Co KY)")

# Leonard Sr. — 14 children across 3 marriages (only Ignatius Jr. + Leonard Jr. known by name; rest abstracted)
leonard_sr_other = [
    n("[+ ~12 other children]", "1760s–1810s", "Leonard Sr. had ~14 children across 3 marriages (names being researched)", None, 10, 18, "probable")
]
leonard_sr = n("Leonard Mattingly Sr.", "1739–1829 Leonardtown MD", "'Old Leonard'; m1. Mary Hayden; m2. Margaret Monarch; m3. Dorothy Hardesty; ~14 children", "p044", 9, 18, "confirmed",
               [ignatius_jr, leonard_jr] + leonard_sr_other,
               spouse="m1. Mary Hayden; m2. Margaret Monica Monarch; m3. Dorothy Hardesty")

# Ignatius (1704) — m. Sarah Catherine Fowler; 7 children total (5 collateral + 2 direct lines)
ignatius_other_children = [
    n("Lucas Mattingly", "?", "Son of Ignatius (per Sarah Catherine Fowler line)", None, 9, 18, "probable"),
    n("William Mattingly", "?", "Son of Ignatius", None, 9, 18, "probable"),
    n("Elizabeth (Mattingly) Thompson", "?", "Daughter of Ignatius; m. Thompson", None, 9, 18, "probable"),
    n("Sarah (Mattingly) Walker", "?", "Daughter of Ignatius; m. Walker", None, 9, 18, "probable"),
    n("Susanna Mattingly", "?", "Daughter of Ignatius", None, 9, 18, "probable"),
]
ignatius = n("Ignatius Mattingly", "1704–1789 St Mary's MD", "Catholic Jesuit naming tradition; 'We're from Ignatius'; m. Sarah Catherine Fowler; 7 children", "p043", 8, 18, "confirmed",
             [leonard_sr] + ignatius_other_children,
             spouse="Sarah Catherine (Fowler) Mattingly")

# Thomas III's 9 children (per agent 16 — 2 wives Elizabeth Warren + Ruth Cole)
thomas_iii_children = [
    n("Edward Mattingly", "~1710", "Son of Thomas III + Elizabeth Warren", None, 7, 18, "probable"),
    n("Clement Mattingly", "~1715", "Son of Thomas III", None, 7, 18, "probable"),
    n("Thomas Mattingly IV", "~1716", "Son of Thomas III", None, 7, 18, "probable"),
    n("Mary (Mattingly) Millard", "~1719", "Daughter of Thomas III", None, 7, 18, "probable"),
    n("James Mattingly", "~1725", "Son of Thomas III", None, 7, 18, "probable"),
    n("Elizabeth (Mattingly) Ford", "~1726", "Daughter of Thomas III", None, 7, 18, "probable"),
    n("John Baptist Mattingly", "~1736", "Son of Thomas III + Ruth Cole; named in 1774 will", None, 7, 18, "confirmed"),
    n("Clement Matney Mattingly", "~1740", "Son of Thomas III + Ruth Cole", None, 7, 18, "probable"),
    n("Dorothy Mattingly", "~1740", "Daughter of Thomas III", None, 7, 18, "probable"),
]

# Thomas III (Mount Misery plantation; will primary source; 2 wives, 9 children)
thomas_iii = n("Thomas Mattingly III", "1688–1774", "Inherited Mount Misery plantation; will April 1774; m1. Elizabeth Warren, m2. Ruth Cole; 9 children", "p090", 6, 18, "confirmed",
               thomas_iii_children, spouse="m1. Elizabeth Warren; m2. Ruth Cole")

# Thomas II's other 8 children (per 1714 will)
thomas_ii_elizabeth = n("Elizabeth Mattingly", "b. 1681", "Thomas II's first daughter", None, 6, 17, "confirmed")
thomas_ii_judith = n("Judith Mattingly", "b. 1683", "Thomas II's second daughter", None, 6, 17, "confirmed")
thomas_ii_james = n("James Mattingly", "b. 1696", "Named in Thomas II's 1714 will", None, 6, 17, "confirmed")
thomas_ii_charles = n("Charles Mattingly", "b. 1698", "Named in Thomas II's 1714 will", None, 6, 17, "confirmed")
thomas_ii_william = n("William Mattingly", "b. 1700", "Named in Thomas II's 1714 will", None, 6, 17, "confirmed")
thomas_ii_luke = n("Luke Mattingly", "b. 1702", "Named in Thomas II's 1714 will", None, 6, 17, "confirmed")
thomas_ii_ann = n("Ann Mattingly", "b. 1706", "Named in Thomas II's 1714 will", None, 6, 17, "confirmed")

# Thomas Mattingly II — THE IMMIGRANT (children: Thomas III, Ignatius/Leonard Ignatius, plus 7 others)
thomas_ii = n("Thomas Mattingly II", "1650–1715", "THE MARYLAND IMMIGRANT — pre-1665; Mattingly's Hope land patent Sept 4 1666", "p039", 5, 17, "confirmed",
              [thomas_ii_elizabeth, thomas_ii_judith, thomas_iii, thomas_ii_james, thomas_ii_charles,
               thomas_ii_william, thomas_ii_luke, ignatius, thomas_ii_ann],
              spouse="m1. Mary Elizabeth Suttle (~1675); m2. Elizabeth Cole (~1690)")

# Thomas I's other 3 children
cezar = n("Cezar Mattingly", "1654–1719", "Co-recipient of Mattingly's Hope land patent 1666", "p038", 5, 17, "confirmed")
judith_turner = n("Judith (Mattingly) Turner", "1645–1744", "Lived to ~99", "p080", 5, 17, "probable")
elizabeth_dorcas = n("Elizabeth Dorcas Mattingly", "1656–1749", "Lived to ~93", "p081", 5, 17, "probable")

# Thomas Mattingly I (stayed in England)
thomas_i = n("Thomas Mattingly I", "1624–1664", "Born Sussex England; died there 1664 BEFORE emigrating; widow brought children to MD", "p028", 4, 17, "probable",
             [thomas_ii, cezar, judith_turner, elizabeth_dorcas],
             spouse="Elizabeth McWilliams (~1626 - aft. 1669)")

# Charles Mattingly + Judith Bugbee
charles = n("Charles Mattingly", "1600–1642", "Father of Thomas I; Sussex England", "p060", 3, 17, "probable",
            [thomas_i], spouse="Judith Bugbee (~1602)")

# John Mattingly (1560-1641 London) — primary-source-confirmed via burial register
john = n("John Mattingly", "1560–1641", "Buried 17 Dec 1641 St Mary Colechurch London — primary source", "p062", 2, 16, "confirmed",
         [charles])

# Henry MATYNGLE — agent 17 finding from FreeREG / Phillimore's Transcripts
# Married 30 Sept 1548 at Heckfield St Michael, Hampshire — same parish that covered Mattingley tithing.
# Born approximately 1518–1528. PROBABLE father of John Mattingly (~1560).
# Spelling "Matyngle" matches 15th-century BHO VCH variant "Martyngle".
# Plus collateral Hampshire Mattinglys: Agnes MATTYNGLY (m. 1571), Anne MATTINGLY (m. 1596).
agnes = n("Agnes Mattyngly", "fl. 1571", "Married Harry Cawte 10 Sept 1571 Heckfield (Phillimore's Transcript line 109)", None, 2, 16, "probable")
anne = n("Anne Mattingly", "fl. 1596", "Married John Ayer 17 Oct 1596 Heckfield (Phillimore line 230)", None, 2, 16, "probable")

henry_matyngle = n("Henry MATYNGLE", "~1520 – ?", "Married 30 Sept 1548 Heckfield St Michael Hampshire (Phillimore's Transcript line 48); probable father of John Mattingly", None, 1, 16, "probable",
                    [john, agnes, anne])

# Reduced ~250-year gap (down from ~300) — Peter de Mattingley (1240s) → Henry MATYNGLE (1548)
gap = n("[~250-year documentary gap]", "1240s–1548", "Family likely yeoman farmers in Hampshire/Surrey/southern England — TNA subsidy rolls + Hampshire Record Office unindexed", None, 1, 14, "unknown",
        [henry_matyngle])

# London-area cluster (collateral, not direct line) — agent 17 finding
# Thomas MOTTINGLEY baptised Wimbledon St Mary 16 Jan 1542/43, son of Henry MOTTINGLEY and Joan
thomas_wimbledon = n("Thomas MOTTINGLEY", "b. 16 Jan 1542/43 Wimbledon", "Son of Henry MOTTINGLEY + Joan; Wimbledon St Mary baptism (FreeREG)", None, 1, 16, "probable")
henry_wimbledon = n("Henry MOTTINGLEY", "fl. 1542", "Of Wimbledon St Mary Surrey; possibly same as Henry MATYNGLE of Heckfield 25 mi away (UNCONFIRMED)", None, 0, 16, "possible",
                    [thomas_wimbledon])

# Peter de Mattingley (last lord, sold the manor)
peter = n("Peter de Mattingley", "fl. 1236–1249", "Last lord; sold Mattingley manor to Geoffrey de Arundel", "p072", 0, 13, "possible",
          [gap])

# Stephen de Mattingley (Curia Regis Rolls 1206)
stephen = n("Stephen de Mattingley", "fl. 1206", "Earliest dated bearer of the Mattingley surname; granted mill to Prior of Merton", "p070", -1, 13, "possible",
            [peter])

# Revelendus (succeeded Ellis)
revelendus = n("Revelendus of Mattingley", "fl. late 12th c.", "Succeeded Ellis; had 3 sons including Stephen", "p071", -2, 12, "possible",
               [stephen])

# Ellis — earliest documented Mattingley individual (root)
ellis = n("Ellis (lord of Mattingley)", "fl. 1167", "First named lord of Mattingley village; recorded in Pipe Roll 13 Henry II", "p073", -3, 12, "possible",
         [revelendus])

# Save
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(ellis, indent=2, ensure_ascii=False), encoding="utf-8")

# Tree stats
def count(node):
    return 1 + sum(count(c) for c in node.get("children", []))

def depth(node):
    if not node.get("children"):
        return 1
    return 1 + max(depth(c) for c in node["children"])

print(f"Wrote {OUT}")
print(f"Total nodes: {count(ellis)}")
print(f"Tree depth: {depth(ellis)}")
print(f"Root: {ellis['name']} ({ellis['dates']})")
