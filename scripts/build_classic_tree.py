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

# Shari's father generation (Leroy + Ruth's children)
shari_father = n("[Shari's father]", "b. 1922", "Master's degree", "p015", 15, 20, "confirmed", [shari, shari_brother, shari_sister])

# Leroy Teichmuller Mattingly + Ruth Baity (and Leroy's siblings)
# CORRECTION (agent 16): Leroy born 31 Aug 1896, died 1968 SA. Ruth Baity 4 Apr 1900 - 1982 Houston.
leroy = n("Leroy Teichmuller Mattingly", "1896–1968", "Born La Grange TX; died San Antonio. U Texas engineer; named for German maternal grandfather Hans", "p002", 14, 20, "confirmed",
          [shari_father], spouse="Ruth (Baity) Mattingly (4 Apr 1900 – 1982 Houston)")
claude = n("Dr. Claude Mattingly", "1898–1934", "Pediatrician; Marine WWI; suicide pact at Texan Hotel Austin Jan 31 1934", "p011", 14, 20, "confirmed")
mamie = n("Aunt Mamie", "b. ~1900", "Mother died at her birth", "p013", 14, 20, "confirmed")
edward_jr = n("Edward Mattingly Jr.", "b. ~1915 La Grange", "Half-sibling — son of Edward Sr. + 2nd wife Blanche Schroeder", None, 14, 20, "probable")

# Edward Mattingly Sr + May Teichmueller — CORRECTED: born 1868 Missouri, died 1945 La Grange
edward_sr = n("Edward Mattingly Sr.", "1868 MO – 1945 La Grange TX", "Born Missouri; migrated to TX by 1894; m. May Teichmueller 1 Sept 1894 (May d. 28 Aug 1900); m2. Blanche Schroeder", "p041", 13, 20, "confirmed",
              [leroy, claude, mamie, edward_jr], spouse="m1. May Teichmueller (1894–1900); m2. Blanche D. Schroeder (b. 1886 MO)")

# Thomas Jefferson Mattingly — Edward Sr's father, born KY 1828, died Pattonsburg MO 1883
thomas_jefferson = n("Thomas Jefferson Mattingly", "1828 KY – 1883 MO", "Born Kentucky; family moved to Missouri (Pattonsburg, Daviess Co) before death", None, 12, 19, "confirmed",
                     [edward_sr], spouse="Elizabeth Christie (b. 2 Dec 1833 Christianburg, Shelby KY)")

# Ignatius Mattingly (b. 1781 MD, d. 1833 KY) — the KY-migration generation
ignatius_1781 = n("Ignatius Mattingly", "1781 MD – 1833 KY", "Born Maryland; family moved to Kentucky (Marion/Washington Co); died there 1833", None, 11, 19, "confirmed",
                  [thomas_jefferson])

# Ignatius Jr. (b. 1750) — the NEW intermediate generation (per agent 16)
ignatius_jr = n("Ignatius Mattingly Jr.", "b. 1750", "Son of Leonard Sr.; the actual direct ancestor (NOT Leonard Jr. who is collateral)", None, 10, 18, "confirmed",
                [ignatius_1781])

# Leonard Jr. (now COLLATERAL — Y-DNA project anchor for KY descendants)
leonard_jr_children = [
    n("Mary Alvey Mattingly", "b. 1798", "Eldest of Leonard Jr.'s 4 children", None, 11, 19, "probable"),
    n("Henry Martin Mattingly Sr.", "1799–1858", "Had 9 children 1828-1844 in Marion/Washington Co KY; m. Helen Thompson", None, 11, 19, "confirmed",
      [n("George Thomas Mattingly", "b. 1830 Marion KY", "Y-DNA project participant; cousin of the Texas line", "p046", 12, 19, "possible")]),
    n("William Cissell Mattingly", "b. 1807", "Leonard Jr's third child", None, 11, 19, "probable"),
    n("Leonard Mattingly III", "1828–1914 Glen Dean KY", "Died KY at 85; ruled out as centenarian", None, 11, 19, "confirmed"),
]
leonard_jr = n("Leonard Mattingly Jr.", "1764–1843 Marion KY", "1785 Catholic migration to KY; Y-DNA project anchor — but COLLATERAL to Hunter, not direct line", "p045", 10, 18, "confirmed",
               leonard_jr_children, spouse="Ann Cissell (m. 7 Jan 1788, Nelson Co KY)")

# Leonard Sr. — CORRECTED: 14 children via 3 marriages
leonard_sr_other = [
    n("[+12 other children of Leonard Sr.]", "1760s-1810s", "Leonard Sr. had ~14 children across 3 marriages", None, 10, 18, "probable")
]
leonard_sr = n("Leonard Mattingly Sr.", "1739–1829 Leonardtown MD", "'Old Leonard'; m1. Mary Hayden; m2. Margaret Monarch; m3. Dorothy Hardesty; ~14 children", "p044", 9, 18, "confirmed",
               [ignatius_jr, leonard_jr] + leonard_sr_other,
               spouse="m1. Mary Hayden; m2. Margaret Monica Monarch; m3. Dorothy Hardesty")

# Ignatius (1704) — CORRECTED: m. Sarah Catherine Fowler; 7 children
ignatius_other_children = [
    n("Lucas Mattingly", "?", "Son of Ignatius (per Sarah Catherine Fowler line)", None, 9, 18, "probable"),
    n("William Mattingly", "?", "Son of Ignatius", None, 9, 18, "probable"),
    n("Elizabeth (Mattingly) Thompson", "?", "Daughter of Ignatius", None, 9, 18, "probable"),
    n("Sarah (Mattingly) Walker", "?", "Daughter of Ignatius", None, 9, 18, "probable"),
    n("Susanna Mattingly", "?", "Daughter of Ignatius", None, 9, 18, "probable"),
]
ignatius = n("Ignatius Mattingly", "1704–1789 St Mary's MD", "Catholic Jesuit naming tradition; 'We're from Ignatius'; m. Sarah Catherine Fowler; 7 children", "p043", 8, 18, "confirmed",
             [leonard_sr] + ignatius_other_children,
             spouse="Sarah Catherine (Fowler) Mattingly")

# Thomas III's other named sons (Edward, John Baptist, Clement)
thomas_iii_son_leonard = n("Leonard (son of Thomas III)", "?", "Named in 1774 will of Thomas III", None, 7, 18, "probable")
thomas_iii_son_edward = n("Edward (son of Thomas III)", "?", "Named in 1774 will of Thomas III", None, 7, 18, "probable")
thomas_iii_son_jbaptist = n("John Baptist Mattingly", "?", "Named in 1774 will of Thomas III", None, 7, 18, "probable")
thomas_iii_son_clement = n("Clement Mattingly", "?", "Named in 1774 will of Thomas III", None, 7, 18, "probable")

# Thomas III (Mount Misery plantation; will primary source)
thomas_iii = n("Thomas Mattingly III", "1688–1774", "Inherited Mount Misery plantation; will April 1774", "p090", 6, 18, "confirmed",
               [thomas_iii_son_leonard, thomas_iii_son_edward, thomas_iii_son_jbaptist, thomas_iii_son_clement])

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

# 300-year gap placeholder
gap = n("[~300-year documentary gap]", "1240s–1560", "Family likely yeoman farmers in southern England", None, 1, 14, "unknown",
        [john])

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
