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
hunter = n("Hunter Spence", "living", "Recipient of this family history; recorded grandma's interview. Surname Spence inherited via FATHER (Dale William Spence Jr.), NOT via maternal grandfather David Trifon (whose Trifon surname was adopted, biological line untraceable).", "p001", 18, 21, "confirmed")

# Hunter's mother — Rachel (per Hunter, 2026-04-26)
rachel = n("Rachel (née Trifon→Spence)", "living", "Hunter's mother; daughter of Shari Mattingly + David Trifon (adopted-name Trifon). Married Dale William Spence Jr. — Hunter's surname comes via this marriage line, from Dale Sr's English Spence family.", None, 17, 21, "confirmed", [hunter],
              spouse="Dale William Spence Jr.")
charmaine = n("Charmaine", "living", "Shari + David Trifon's daughter; Hunter's aunt (maternal)", "p021", 17, 21, "confirmed")

# Shari + David
shari = n('Sharyn ("Shari") Mattingly', "b. 1947", "Family historian; Santa Monica; oil royalty owner", "p000", 16, 20, "confirmed",
          [rachel, charmaine], spouse="David Spence (1st husband)")

# Shari's siblings (redacted) + her father
shari_brother = n("[brother]", "living", "Got the chair from Pearl's set", "p022", 16, 20, "confirmed")
shari_sister = n("[sister]", "living", "—", "p023", 16, 20, "confirmed")

# Shari's father — agent 18 finding: STRONG candidate Leroy Baity Mattingly (b. 17 May 1922 SA, d. 2013 Colorado Springs)
shari_father = n("Leroy Baity Mattingly", "1922–2013", "Born 17 May 1922 San Antonio; died Colorado Springs CO 2013. WikiTree Mattingly-1178. m. Jennive Imogene Lepick (1923-2008) at Fort Sill OK on 18 Dec 1943.", "p015", 15, 20, "confirmed", [shari, shari_brother, shari_sister],
                 spouse="Jennive Imogene Lepick (2 Feb 1923 Floresville TX – 2008 Colorado Springs)")

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

# Leonard Mattingly Sr (Mattingly-62, 1739-1829) — COLLATERAL, NOT direct line
# Per WikiTree mass crawl (agent 22): his father is Ignatius Sr (Mattingly-60), making Leonard
# a SIBLING of Ignatius Jr (Mattingly-141), not parent. 10 named children:
leonard_sr_children = [
    n("Joseph Mattingly", "?", "Mattingly-339; son of Leonard Sr. Webb says Joseph Mattingly of Long Lick helped build the first Hardinsburg chapel by preparing heavy timbers and hand-sawing planks.", None, 11, 18, "probable"),
    n("Jane Mattingly", "b. 1760", "Mattingly-211", None, 11, 18, "probable"),
    n("John Baptist Mattingly", "b. 1762", "Mattingly-59", None, 11, 18, "probable"),
    n("Leonard Mattingly Jr.", "1764–1843 Marion KY", "Mattingly-210; 1785 Catholic migrant to KY; Y-DNA project anchor for KY descendants. m. Ann Cissell.", "p045", 11, 18, "confirmed",
      [
        n("Mary Alvey Mattingly", "b. 1798", "Eldest of Leonard Jr.'s 4 children", None, 12, 19, "probable"),
        n("Henry Martin Mattingly Sr.", "1799–1858 Marion KY", "9 children 1828-1844; m. Helen Thompson; collateral KY Y-DNA branch",
          None, 12, 19, "confirmed",
          [
            n("George Thomas Mattingly", "b. 1830 Marion KY", "Mattingly-695; Y-DNA project participant", "p046", 13, 19, "possible"),
            n("[+8 other children of Henry Martin Sr.]", "1828–1844", "Per agent 16 research", None, 13, 19, "probable"),
          ],
          spouse="Helen Thompson (b. ~1800)"),
        n("William Cissell Mattingly", "b. 1807", "Leonard Jr's third child", None, 12, 19, "probable"),
        n("Leonard Mattingly III", "1828–1914 Glen Dean KY", "Died KY at 85; ruled out as centenarian", None, 12, 19, "confirmed"),
      ],
      spouse="Ann Cissell (m. 7 Jan 1788, Nelson Co KY)"),
    n("Ignatius Mattingly", "b. 1766", "Mattingly-53; son of Leonard Sr. Webb says Ignatius Mattingly of Long Lick helped build the first Hardinsburg chapel by preparing heavy timbers and hand-sawing planks.", None, 11, 18, "probable"),
    n("Susannah (Mattingly) Ray", "b. 1766", "Mattingly-208; m. Ray", None, 11, 18, "probable"),
    n("Basil Mattingly", "b. 1772", "Mattingly-207", None, 11, 18, "probable",
      [n("Martha 'Mother Generose' Mattingly", "fl. 1842–1844 KY", "Webb identifies Martha as Basil Mattingly's daughter; as Mother Generose Mattingly she led the Loretto community from 1842 to 1844.", None, 12, 19, "confirmed")]),
    n("Susan (Mattingly) Barron", "b. 1775", "Mattingly-78; m. Barron", None, 11, 18, "probable"),
    n("Mary (Mattingly) Buckman", "b. 1777", "Mattingly-205; m. Buckman", None, 11, 18, "probable"),
    n("William Mattingly", "b. 1777", "Mattingly-204", None, 11, 18, "probable"),
    n("Sister Margaret Mattingly", "fl. 1812 KY", "Founding member of the Sisters of Loretto (1812) — the first women's religious order founded west of the Allegheny Mountains. Per Webb 1884.", "p056", 11, 19, "confirmed"),
    n("[Bardstown Mattingly bridge incomplete]", "19th c. KY", "Placeholder for a later Bardstown collateral line. Exact bridge from this Kentucky Mattingly cluster to Cyprian Peter Mattingly is still incomplete.", None, 11, 19, "possible",
      [n("Marie Mattingly Meloney", "1878–1943", "Major American journalist and editor, born Bardstown KY to physician Cyprian Peter Mattingly. Included only as a POSSIBLE Kentucky collateral until the branch bridge is documented.", None, 12, 20, "possible")]),
]
leonard_sr = n("Leonard Mattingly Sr.", "1739–1829 Washington Co KY", "Mattingly-62. 'Old Leonard'; one of the William/Leonard/Lucas brothers Webb places at Hardin's Creek in early 1786. m1. Mary Hayden; m2. Margaret Monarch; m3. Dorothy Hardesty; 10+ named children. SIBLING of Ignatius Jr (NOT direct ancestor of Hunter)", "p044", 10, 18, "confirmed",
               leonard_sr_children,
               spouse="m1. Mary Hayden; m2. Margaret Monarch; m3. Dorothy Hardesty")

# Ignatius Sr (1704) — m. Sarah Catherine Fowler; 7 children
# Direct line goes through Ignatius Jr (1750), NOT Leonard Sr (1739)
ignatius_other_children = [
    n("Leonard Mattingly Sr.", "(see collateral subtree)", "Mattingly-62 — moved to direct ignatius_jr branch", None, 10, 18, "confirmed", []),  # placeholder, real is leonard_sr below
    n("William Mattingly", "1741–1817 Washington KY", "Mattingly-213; m1. Mary Catherine Spalding; m2. Nancy Elizabeth Clark", None, 9, 18, "probable"),
    n("Lucas Mattingly", "1743–1830 KY", "Mattingly-214; m. Sue Ellen Hagan, Elizabeth Eleanor Thompson, Elizabeth Cambron", None, 9, 18, "probable"),
    n("Elizabeth (Mattingly) Thompson", "b. 1745", "Mattingly-1901; m. Thompson", None, 9, 18, "probable"),
    n("Sarah Ann (Mattingly) Walker", "b. 1747", "Mattingly-1312; m. Walker", None, 9, 18, "probable"),
    n("Susanna Mattingly", "b. 1749", "Mattingly-1900", None, 9, 18, "probable"),
]
# Replace first item (placeholder) with actual leonard_sr subtree
ignatius_other_children[0] = leonard_sr

ignatius = n("Ignatius Mattingly Sr.", "1704–1789 St Mary's MD", "Mattingly-60. Catholic Jesuit naming; 'We're from Ignatius'; m. Sarah Catherine Fowler. 7 children — direct line via Ignatius Jr (1750, Mattingly-141), NOT Leonard Sr.", "p043", 8, 18, "confirmed",
             [ignatius_jr] + ignatius_other_children,  # ignatius_jr is the direct-line child; rest are collateral
             spouse="Sarah Catherine (Fowler) Mattingly")

# Thomas III's 9 children (per agent 16 — 2 wives Elizabeth Warren + Ruth Cole)
thomas_iii_children = [
    n("Edward Mattingly", "~1710", "Son of Thomas III + Elizabeth Warren; Edward Mattingly is publicly documented as captain in the Upper Battalion of Militia in Saint Mary's County in 1779. The public role is confirmed; this exact placement in the Mount Misery branch remains probable.", None, 7, 18, "probable"),
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

# Thomas I's other 3 children — Cezar's line now expanded with Garrett MD descent (agent 27)
# Cezar (1654-1719) m. Jane Suttle → John Baptist (1690) m. Grace Brewer → John (1715) m. Elizabeth Brewer
# → Henry Mattingly I (1751-1823) [1969 book progenitor] → Henry II (1782-1846 MO) → Dominick (1808-1854 Hoyes MD)
# → Meshack (1837-1912 Garrett Co Commissioner), Rev. Romanus (1850-1922 priest), Judge Francis (1813-1879)

meshack = n("Meshack Mattingly", "1837–1912", "Garrett County (MD) Commissioner; operated 'best stock farm in the county'; m. Mary P. Griffith (daughter of Pennsylvania Governor)", "p053", 8, 19, "confirmed")
rev_romanus = n("Rev. Romanus Mattingly", "1850–1922", "Catholic priest; built parish churches at Oakland MD + Hoyes MD; 16-year pastor at Oakland", "p054", 8, 19, "confirmed")
judge_francis = n("Judge Francis Mattingly", "1813–1879", "Judge of the Orphans' Court at Cumberland MD (elected 1859); helped commit Allegany County to Union side 1861", "p055", 8, 19, "confirmed")

dominick = n("Dominick Mattingly", "1808 MD – 1854 Hoyes MD", "Anchor of Garrett County Mattingly settlement; bought 157 acres on Youghiogheny River from John Hoye 1831; the village was renamed 'Hoyes' in 1880", "p052", 7, 19, "confirmed",
             [meshack, rev_romanus], spouse="Ann Browning")
henry_ii = n("Henry Mattingly II", "1782 MD – 1846 MO", "Son of Henry I; m. Nancy Ann Durbin; migrated to Missouri", None, 6, 19, "confirmed",
             [dominick], spouse="Nancy Ann Durbin")
henry_i = n("Henry Mattingly I", "1751 MD – 1823 Mt Savage MD", "Mattingly-617. Patriarch / progenitor of the entire 1969 'Descendants of Henry Mattingly' genealogy book; m. Honora Durbin; 12 children", "p051", 5, 18, "confirmed",
            [henry_ii, judge_francis], spouse="Honora Durbin")
john_1715 = n("John Mattingly", "1715–1759", "Mattingly-258; m. Elizabeth Brewer; father of Henry I", None, 4, 18, "probable",
              [henry_i], spouse="Elizabeth Brewer")
john_baptist_1690 = n("John Baptist Mattingly", "1690–1744", "Mattingly-225; m. Grace Brewer; Cezar's son; great-grandfather of Henry I", None, 3, 17, "probable",
                     [john_1715, n("Lucius Mattingly", "1730–1826 Washington Co KY", "Mattingly-318; separate KY branch", None, 4, 18, "probable")],
                     spouse="Grace Brewer")

cezar = n("Cezar Mattingly", "1654–1719", "Mattingly-223. Co-recipient of Mattingly's Hope land patent 1666; m. Jane Suttle; brother of Hunter's direct ancestor Thomas II; Y-DNA R-Y14083 confirmed in his line (sibling terminal to Hunter's expected R-Y14084 cluster); ancestor of the Garrett County Hoyes settlement.", "p050", 5, 17, "confirmed",
          [john_baptist_1690], spouse="Jane Suttle")
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

# Ellis — first MATTINGLEY-named lord (the surname is taken FROM the village)
ellis = n("Ellis (lord of Mattingley)", "fl. 1167", "First named lord of Mattingley village; recorded in Pipe Roll 13 Henry II (Pipe R. Soc. xi, 189)", "p073", -3, 12, "possible",
         [revelendus])

# Pre-Ellis MATTINGLEY MANOR lords — VCH Hampshire vol 4 + Domesday Book
# These predated the "de Mattingley" surname tradition: surnames came AFTER 1086.
# They are POSSIBLE social/cultural ancestors of the de Mattingley family (whose surname
# came from this place), not provable biological ancestors.
alsi = n("Alsi son of Brixi", "fl. 1086", "Norman-era Domesday tenant of Mattingley manor (TRW). Held under royal demesne. 8 villagers, 3 smallholders, 3 ploughlands, 1 mill (5s), fishery (100 eels). VCH Hants i, 505a. POSSIBLE social-line ancestor of the de Mattingley family.", "p074", -4, 11, "possible",
          [ellis])

alric = n("Alric (Anglo-Saxon)", "fl. before 1066", "Held Mattingley as alod (free tenure, no feudal lord but the king) of King Edward the Confessor. Anglo-Saxon noble. VCH Hants i, 505a. The earliest named individual associated with the place from which the Mattingley surname later derived. POSSIBLE distant social-line ancestor.", "p075", -5, 11, "possible",
          [alsi])

# ── Lepick / LEPIK / Mikeska maternal subtree — agents 25 + 29 + 30 confirmed ──
# Bohemian-Czech immigrant chain: Frank LEPIK (b. ~1862 Bohemia, immigrated 1881 to Brown Co Kansas)
# m. Mary Mikeska (b. ~1863 Bohemia/Moravia, Mikeska family arrived 1871). 9 children, all in Kansas
# or Arkansas except Fred Sr who went to Texas. Migration: Bohemia → Brown Co KS (1881) → Hazen AR
# (1901-1920) → Wilson County TX (~1920s) → San Antonio (~1930s).

# Boehme line (Hilda's father per agent 30): Herman F. Boehme (b. 9 Jun 1863 TX, d. 18 Jun 1900 Shiner,
# Lavaca County TX). Lutheran. Buried Sons of Hermann Cemetery. Hilda's mother UNVERIFIED.

shari_mother = n("Jennive Imogene Lepick", "2 Feb 1923 Floresville TX – 2008 Colorado Springs", "Shari's mother (Hunter's maternal great-grandmother). m. Leroy Baity Mattingly 18 Dec 1943 at Fort Sill OK. Dietician degree from Our Lady of the Lake College, San Antonio. Find a Grave 36080759. WikiTree Lepick-1.", None, 15, 20, "confirmed",
                 [], spouse="Leroy Baity Mattingly")

# Jennive's siblings
gertrude_lepick = n("Gertrude (Lepick) Hurlburt", "1920–2000", "Jennive's older sister", None, 15, 20, "confirmed")
fred_lepick_jr = n("Fred Charles Lepick Jr.", "1925–2016", "Jennive's younger brother. Naval Aviator (NOT a banker — Frost Bank 'uncle' oral tradition is debunked).", None, 15, 20, "confirmed")

# Jennive's mother — Hilda (Boehme) Lepick
# Per agent 45: Hilda's mother = Minna Marie MACKER (PROBABLE); Boehme origin = PROBABLE Prussian Silesia (Schlesien),
# entered via Indianola TX (pre-1875 manifests lost in 1875 hurricane); Lutheran (likely LCMS Missouri Synod).
# Convergent evidence: Breslau TX (7 mi NW Hallettsville) named for Prussian Breslau (Wrocław) = Silesian settlers.

hilda_boehme = n("Hilda (Boehme) Lepick", "~1900 TX – ~1945", "Jennive's mother. Maiden name Boehme. Daughter of Herman F. Boehme + Minna Marie Macker. Texas-born; German-Lutheran community. FamilySearch PID LKM6-W7J.", None, 14, 20, "confirmed", spouse="Fred Charles Lepick Sr.")

# Half-siblings of Hilda via Minna's 2nd marriage to John W. Luedecke
luedecke_2 = n("Herbert John Luedecke", "?", "Half-sibling of Hilda Boehme (via mother Minna's 2nd marriage to John W. Luedecke). Per PeopleLegacy.", None, 14, 20, "probable")
luedecke_3 = n("William Luedecke", "?", "Half-sibling of Hilda Boehme. Per PeopleLegacy.", None, 14, 20, "probable")

# Minna Marie Macker — Hilda's mother (Herman's wife; outlived him 47 years; remarried Luedecke)
minna_macker = n("Minna Marie (Macker) Boehme→Luedecke", "? – 29 May 1947 Floresville TX", "Hunter's maternal 2x-great-grandmother (PROBABLE per agent 45 / PeopleLegacy). Hilda Boehme's mother. Outlived Herman by 47 years; remarried John W. Luedecke; had 2 more children (Herbert + William Luedecke).", None, 13, 19, "probable",
                 [hilda_boehme, luedecke_2, luedecke_3], spouse="m1. Herman F. Boehme; m2. John W. Luedecke")

herman_boehme = n("Herman F. Boehme", "9 Jun 1863 TX – 18 Jun 1900 Shiner, Lavaca Co TX", "Hilda Boehme's father (Hunter's maternal 2x-great-grandfather). Lutheran (likely LCMS Missouri Synod). Buried Sons of Hermann Cemetery. m. Minna Marie Macker. Parents (3x-great-grandparents) UNVERIFIED — they immigrated ~1855-1862, PROBABLE origin Prussian Silesia (Schlesien) per agent 45.", None, 13, 19, "confirmed", spouse="Minna Marie Macker")
boehme_root = minna_macker  # anchored at Minna since she bridges both marriages

# Fred Charles Lepick Sr. — CORRECTED from "Frederick" (per agent 29)
fred_lepick_sr = n("Fred Charles Lepick Sr.", "8 Mar 1894 Brown Co KS – ?", "Jennive's father. Born Brown County, Kansas to Bohemian immigrant Frank Lepik + Mary Mikeska. Moved to Wilson Co TX 1910-1920; m. Hilda Boehme ~1920. Lived San Antonio late 1930s+. Buried Floresville City Cemetery (Find a Grave 55217353). WikiTree Lepick-2.", None, 14, 20, "confirmed",
                    [shari_mother, gertrude_lepick, fred_lepick_jr], spouse="Hilda Boehme")

# Fred Sr's siblings (Frank Lepik + Mary Mikeska's other 8 children — agent 29)
fred_siblings = [
    n("Mary A. (Lepick) Blacketer", "fl. 1908 KS", "Fred Sr.'s sister; m. Blacketer 1908 Kansas", None, 14, 20, "confirmed"),
    n("Frank T. Lepick", "?", "Fred Sr.'s sibling (Kansas/Arkansas)", None, 14, 20, "confirmed"),
    n("Tilford Anthony Lepick", "?", "Fred Sr.'s sibling", None, 14, 20, "confirmed"),
    n("Edward Lepick", "?", "Fred Sr.'s sibling", None, 14, 20, "confirmed"),
    n("William Henry Lepick", "?", "Fred Sr.'s sibling", None, 14, 20, "confirmed"),
    n("Joseph Lepick", "?", "Fred Sr.'s sibling", None, 14, 20, "confirmed"),
    n("Jennie Lepick", "?", "Fred Sr.'s sibling", None, 14, 20, "confirmed"),
    n("Katherine 'Kate' Lepick", "?", "Fred Sr.'s sibling", None, 14, 20, "confirmed"),
]

# Frank LEPIK (Bohemian immigrant 1881) + Mary Mikeska
mary_mikeska = n("Mary (Mikeska) Lepik", "~1863 Bohemia/Moravia – ?", "Hunter's maternal 2x-great-grandmother. Czech/Moravian. Mikeska family arrived 1871 northeastern Kansas Czech corridor. WikiTree Mikeska-77 or 78.", None, 13, 19, "confirmed", spouse="Frank Lepik")

frank_lepik = n("Frank Lepik (later 'Lepick')", "~1862 Frýdek-Místek region, Moravia – 1939 Brown Co KS", "Hunter's maternal 2x-great-grandfather. EMIGRATED 1881 from the Frýdek-Místek District (Moravian-Silesian Region — 54% of all Czech Lepík surname-bearers concentrated there per agent 44 deep-dive). Settled Brown County Kansas; shoemaker; I.O.O.F. Lodge No. 331 Horton KS. m. Mary Mikeska 13 Jan 1885 St Joseph Catholic Church Everest KS. Roman Catholic. 9 children. Buried Kennekuk Cemetery Horton (Find a Grave 140131220). WikiTree Lepik-8.", None, 13, 19, "confirmed",
                 [fred_lepick_sr] + fred_siblings, spouse="Mary Mikeska")

lepick_root = frank_lepik

# ── BAITY / Beatty / Beatie line (agent 36 deep-dive) ─────────────
# Hunter ← Shari ← Leroy Baity Mattingly Sr ← Leroy Teichmuller Mattingly + Ruth Baity ← W.A. Baity + Pearl
# Patrilineal Baity chain: Pearl Mae Baity ← W.A. Baity ← William D Baity (1829-1894 Yadkin NC, Courtney
# Baptist Cemetery) ← Isham/Isom Baity (19 Oct 1804 - 23 Dec 1892 Yadkin NC) ← David Baity ← George Baity
# (adult by 1774 Rowan/Surry NC). Surname = Scots-Irish Beatty/Beattie via Border Scots → Plantation of
# Ulster (1610-1640) → Pennsylvania 1720s-30s → Great Wagon Road → NC by 1750s.

baity_george = n("George Baity / Batee / Baty", "fl. 1774 Rowan/Surry Co NC", "Earliest documented Baity ancestor. Adult by 1774 Rowan/Surry County NC court records. Scots-Irish/Plantation-of-Ulster origin via PA 1720s-30s.", None, 8, 18, "possible")
baity_david = n("David Baity", "fl. ~1830 Surry Co NC", "PROBABLE link between George (1774) and Isham (1804) — adult by 1830 Surry Co.", None, 9, 19, "possible", [baity_george])
baity_isham = n("Isham 'Isom' Baity", "19 Oct 1804 – 23 Dec 1892 Yadkin Co NC", "CONFIRMED documented person; PROBABLE direct ancestor of William D. Baity. Yadkin Co NC.", None, 10, 19, "probable", [baity_david])
baity_william_d = n("William D. Baity", "1829/1830 – 1894 Yadkin Co NC", "Buried Courtney Baptist Church Cemetery, Yadkin Co NC. Probable son of Isham + father of William Alexander Baity.", None, 11, 19, "probable", [baity_isham])
ruth_baity = n("Ruth (Baity) Mattingly", "4 Apr 1900 – 1982 Houston", "Hunter's maternal great-grandmother. Daughter of W.A. Baity + Pearl Mae 'Paralee' Johnson. m. Leroy Teichmuller Mattingly. Mother of Leroy Baity Mattingly Sr (Shari's father).", None, 14, 20, "confirmed")
baity_william_a = n("William Alexander 'W.A.' Baity", "~1850s NC – ?", "Hunter's maternal great-great-grandfather. NC-born; San Antonio builder/developer. 211 Castillo Ave (1925). Bexar County deed conveyances 1910. m. Pearl Mae 'Paralee' Johnson (26 Jul 1878 NC – 26 Dec 1969 Bexar Co TX, came NC→TX as child, bought Reeves Co TX land 1901 Wolfcamp/Spraberry oil play USGS 2016). Daughter Ruth Baity.", None, 12, 19, "confirmed",
                    [ruth_baity], spouse="Pearl Mae 'Paralee' Johnson")
# Re-parent: William D's child is William A
baity_william_d["children"] = [baity_william_a]
baity_root = baity_george

# Tom Frost Jr — bank president 1963-1997, possibly Shari's uncle
tom_frost_jr = n("Tom Frost Jr.", "1927–2018", "Frost Bank president 1963-1997. Probable 'Shari's uncle' from Hunter's interview.", None, 15, 20, "probable")
ita_frost = n("Ilse 'Ita' Herff Frost McNeel", "b. 1930", "Daughter of T.C. Frost III + Florence Herff", None, 15, 20, "probable")

tc_frost_iii = n("Thomas Claiborne Frost III", "1903–1971", "Grandson of bank founder. m. Florence Ilse Herff (1906-1984)", None, 14, 20, "confirmed",
                 [tom_frost_jr, ita_frost], spouse="Florence Ilse Herff (1906-1984)")

joseph_h_frost = n("Joseph H. Frost", "1881–1956", "Brother of T.C. Frost II; ran Frost Bank. Confirmed Frost-family lineage.", None, 13, 20, "confirmed")
tc_frost_ii = n("T.C. Frost II", "?", "Son of bank founder T.C. Frost I; Frost Bank president gen 2.", None, 13, 20, "confirmed",
                [tc_frost_iii])

tc_frost_i = n("Thomas Claiborne Frost I", "1833–1903", "FOUNDER of Frost Bank San Antonio (1868). Former Confederate Army Lt Col. Bank still Frost-controlled today.", None, 12, 19, "confirmed",
               [tc_frost_ii, joseph_h_frost])

# Attach Frost subtree as a SECOND ROOT — render alongside Mattingly tree as collateral marriage line
# (since lineage-tree.json is single-rooted, embed as a child of Hunter's parent placeholder for now —
# the visualization will show it as one of the maternal-side branches)
# Better approach: nest under shari_mother who is a sibling of shari (in-law to Mattingly direct line)
# Simplest for now: render as separate top-level "Maternal Frost line" — store as alt-root

frost_root = tc_frost_i

# ── Baity branch — tree-ready anchors from 2026-04-26 Baity integration pass ──
# The direct William Alexander / Pearl-Paralee / Reeves County mineral bridge remains below tree-ready.
# This visual tree keeps only source-backed anchors and explicitly labels unresolved bridge work.

isham_baity = n("Isham \"Isom\" Baity", "19 Oct 1804 – 23 Dec 1892", "Courtney Baptist Church Cemetery, Yadkin County NC, gives exact dates. Strong Yadkin/Surry Baity anchor; direct bridge to W. A. Baity still needs census/probate/vital proof.", None, 12, 19, "confirmed")

baity_surry_cluster = n("Surry County Baity household cluster", "1830", "1830 Surry County census transcription lists David Baity, George Baity, Isam Baity, and Pleasant Baity as separate heads of household. Regional presence note only; not a proved parent-child chain.", None, 11, 19, "confirmed",
                        [isham_baity])

wa_paralee_baity = n("W. A. Baity + Paralee Baity", "fl. 1909–1925 San Antonio TX", "Bexar County records and San Antonio newspapers document W. A. + Paralee as a real-estate couple by 1910; W. A. was a builder/developer and was listed at 211 Castillo Ave by 1925. Expanding W. A. to William Alexander and Pearl to Paralee remains research-note-only until direct records are cited.", None, 14, 20, "confirmed")

baity_root = n("Baity line research anchors", "NC by 1830; San Antonio by 1910", "Visual tree of source-backed Baity anchors only. It does not claim a completed direct lineage, immigrant arrival, or the unproved April 1901 Reeves County purchase.", None, 10, 19, "confirmed",
               [baity_surry_cluster, wa_paralee_baity])

# ── Teichmueller maternal-paternal subtree (agent 24 finding) ────────────────────
# Hunter ← Shari (p000) ← Leroy Teichmuller Mattingly (p002) ← May Teichmueller (Edward Sr's wife)
# ← Hans Teichmueller (1837-1901, p003) ← August Teichmueller + Charlotte von Girsewaldt (Brunswick)
# Per agent 24: Gustav Teichmüller (philosopher, 0.82) is PROBABLE brother of Hans (matching parents)

anna_teichmueller = n("Anna Teichmüller", "1861–1940", "Composer, pianist, and music teacher; NDB identifies her as Gustav Teichmüller's daughter.", "p061", 14, 19, "confirmed")
gustav_teichmueller = n("Gustav Teichmüller", "1832 Brunswick – 1888 Tartu", "German philosopher and historian of philosophy; professor at Dorpat (Tartu). NDB confirms he was Hans Teichmueller's brother.", "p060", 13, 19, "confirmed",
                       [anna_teichmueller])

minette = n("Minette Teichmueller (Pohl)", "1871–1970", "Texas muralist; New Deal Art Registry confirms she painted 'The Law--Texas Rangers' for the Smithville post office in 1940. Often identified as Hans and Augusta's daughter, but that parent-child link still needs a direct census, cemetery, or vital-record citation.", "p004", 14, 19, "possible")
may_teichmueller = n("May Teichmueller", "1872 – 28 Aug 1900", "m. Edward Mattingly Sr. 1 Sept 1894; mother of Leroy Teichmuller Mattingly (Hunter's great-grandfather); Hans's other daughter", None, 14, 19, "confirmed")
unknown_5th_child = n("[5th child of Hans]", "?", "Lotto 1902 confirms 5 children but 5th not in TX vital records (pre-1903 records sparse) — UNVERIFIED", None, 14, 19, "possible")

# Hans's other CONFIRMED siblings (per agent 34 NDB 2016 vol 26 p.6):
wilhelm_teichmueller = n("Wilhelm Teichmüller", "1834–1869", "Hans/Gustav's brother. Premier-Lieutenant + Schriftsteller (writer). m. Bertha Kuntzen. Per NDB 2016. POSSIBLE father of pianist Robert Teichmüller (1863-1939).", None, 13, 19, "confirmed")
wilhelmina_teichmueller = n("Wilhelmina (Minette) Teichmüller", "1829–1886", "Hans/Gustav's surviving sister (NOT to be confused with Hans's daughter Minette 1871). m. Karl Mollenhauer (Protestant pastor + Superintendent at Bockenem). Per NDB 2016.", None, 13, 19, "confirmed", spouse="Karl Mollenhauer")

hans = n("Hans Teichmueller", "7 Mar 1837 Braunschweig – 17 Feb 1901 La Grange TX", "Hunter's confirmed great-great-grandfather. TSHA confirms his Braunschweig birth, post-1855 migration to Texas, 1858 Fayette County marriage to Augusta Kellner, five children, and later legal/judicial career in Fayette County. This pass does not extend Kellner parentage beyond Augusta.", "p003", 13, 19, "confirmed",
        [may_teichmueller, minette, unknown_5th_child], spouse="Auguste Kellner")

# August Wilhelm Teichmüller — CONFIRMED via NDB (corrected dates)
august = n("August Wilhelm Teichmüller", "1795–1855", "Seconde-Lieutenant in Schwarzen Corps des Majors Olfermann, Brunswick (NOT Prussian) army. m. Charlotte Georgine Elisabeth von Girsewald (1799-1860). 5 children: Wilhelmina, Wilhelm, Hans, Gustav, +1 died young. Per NDB 2016.", None, 12, 19, "confirmed",
           [wilhelmina_teichmueller, wilhelm_teichmueller, hans, gustav_teichmueller],
           spouse="Charlotte Georgine Elisabeth von Girsewald (1799–1860)")

# Charlotte's parents (per NDB)
charlotte_parents = n("Georg von Girsewald + Christine Elisabeth Boyer", "Georg b. 1735 – 1816", "Charlotte's parents. Georg = Oberstallmeister and Hauptmann in Brunswick. Per NDB 2016.", None, 11, 19, "confirmed", [august])

# 6-generation Teichmüller patrilineal chain per NDB 2016
wilhelm_ernst = n("Wilhelm Ernst Conrad Teichmüller", "1758–1835", "Oberhütteninspekteur (chief smelting works inspector) at Karlshütte near Delligsen, Leinebergland. m. Henriette Christiane Helene Schorkopf (1763-1818) of Uslar. GND 1154326616. August's father.",
                  None, 11, 18, "confirmed", [august], spouse="Henriette Christiane Helene Schorkopf (1763–1818)")

joachim_andreas = n("Joachim Andreas Teichmüller", "1705–1778", "Oberfaktor (chief commercial agent) in Goslar at the foot of the Harz mountains. GND 1154326802. Earliest documented patrilineal Teichmüller before mining-clan generations.",
                    None, 10, 18, "confirmed", [wilhelm_ernst])

# Pre-Joachim gap (~1640-1700, ~2 unnamed generations per NDB)
gap_pre_joachim = n("[~2 unnamed Teichmüller generations]", "fl. 1640–1700", "NDB notes a gap between earliest Hans/Johann (~1580) and Joachim Andreas (1705). Likely millers / minor Harz officials.",
                    None, 9, 17, "unknown", [joachim_andreas])

hans_johann = n("Hans / Johann Teichmüller", "~1580–1638", "EARLIEST documented Teichmüller patrilineal ancestor. Master miller (Mühlenmeister) in the southern Harz mountains. Surname Teichmüller is occupational: 'pond miller'. Per NDB 2016.",
                None, 8, 16, "confirmed", [gap_pre_joachim])

teichmueller_root = hans_johann

# ── HUNTER'S ACTUAL PATERNAL SPENCE LINE (confirmed by Hunter 2026-04-26) ──
# Hunter's surname Spence comes from his FATHER Dale William Spence Jr.,
# NOT from David Trifon (Shari's first husband — adopted name, biological line untraceable).
# Dale William Spence Sr. = Rice University professor, English immigrant.
# Alice (maiden unknown) = Hunter's paternal grandmother. Family lived in Beaumont TX.

hunter_dad = n("Dale William Spence Jr.", "living", "Hunter Spence's father. m. Rachel.", None, 17, 21, "confirmed",
                [hunter])

aunt_susan = n("Susan (Spence) Clarke", "living", "Hunter's paternal aunt. Daughter of Dr. Dale William Spence Sr. + Alice Marie Henslee. Took married name Clarke.", None, 17, 21, "confirmed")
aunt_deanne = n("D'Anne (Spence) Patton", "living", "Hunter's paternal aunt. Daughter of Dr. Dale William Spence Sr. + Alice Marie Henslee. Took married name Patton.", None, 17, 21, "confirmed")

dale_sr = n("Dr. Dale William Spence Sr.", "~1934–1936 Beaumont TX – living (~age 92, Houston TX, per Spokeo + Rice emeritus directory Dec 2025)", "Hunter's paternal grandfather. AMERICAN-BORN. Beaumont HS class of 1952 (TX state track championship). BS Rice 1956 → MS North Texas State → EdD Louisiana State University 1966 → postdoc Baylor. Rice University faculty 1963-2003 (40 yrs); Professor Emeritus of Kinesiology (Department of Human Performance and Health Sciences); office Tudor Field House. Also Colonel USMCR (Retired) — ~35 years US Marine Corps Reserve service. m. Alice Marie Henslee. Per agent 39 deep-dive (CONFIRMED via 1990 PubMed + 2019 Rice references).", None, 16, 20, "confirmed",
            [hunter_dad, aunt_susan, aunt_deanne], spouse="Alice Marie (Henslee) Spence (13 Jan 1936 Rusk TX – 3 Dec 2005 Beaumont)")

# ── BYRD patrilineal chain (Dovie Byrd Spence's ancestors, multi-tree confirmed) ──
# Dovie's maiden name = Byrd (per Hunter 2026-04-26). PROBABLE daughter of John Archie Asner
# Byrd + Martha Alice Bedford. Multi-tree confirmed across KcaMarco/L.B./B.G./Frances Padgett.
# Chain extends from Hunter back ~10 generations to colonial Westmoreland Co VA.

# Build chain children-up so each node already has its descendant when defined
sharon_byrd = n("Sharon Kay Byrd", "1944 Velasco TX – 2020", "Daughter of Otha + Mattie. Hunter's 1st cousin 2x removed.", None, 17, 20, "probable")
otha_byrd = n("Otha Lee 'Othar' Byrd", "1902 Milam Co TX – 1989", "Hunter's paternal grand-uncle (PROBABLE — Dovie's brother). m. Mattie Doris Curlee. Per cousin KcaMarco GEDCOM.", "p152", 16, 20, "probable", [sharon_byrd], spouse="Mattie Doris Curlee")

dovie_spence = n("Dovie (Byrd) Spence", "fl. ~1905–1980 Texas", "Hunter's paternal great-grandmother. MAIDEN NAME BYRD (per Hunter 2026-04-26). PROBABLE daughter of John Archie Asner Byrd (1868 Birmingham AL – 1928) + Martha Alice Bedford. Brother: Otha Lee Byrd. m. unnamed English Spence immigrant. Mother of Dale William Spence Sr.", "p114", 16, 20, "probable",
                 [dale_sr], spouse="Mr. Spence (English immigrant)")

byrd_john_archie = n("John Archie Asner Byrd", "1868 Birmingham AL – 1928", "Hunter's paternal great-great-grandfather (PROBABLE). m. Martha Alice Bedford. Family settled Milam County, Texas. Per cousin KcaMarco GEDCOM (4-tree convergence).", "p150", 15, 19, "probable",
                    [otha_byrd, dovie_spence], spouse="Martha Alice (Bedford) Byrd")

byrd_william_leander = n("Pvt William Leander Byrd", "1832 Frankfort AL – 1889", "Confederate States Army Private (CSA). Son of Benjamin Franklin Byrd + Melissa Colbert. m. Margarete Rhetta Peradeau (1829-1925, French-Huguenot surname). Cross-confirmed 3 cousin GEDCOMs.", "p153", 14, 19, "probable",
                        [byrd_john_archie], spouse="Margarete Rhetta (Peradeau) Byrd (1829–1925)")

byrd_benjamin = n("Benjamin Franklin Byrd", "b. 1798", "Son of John Howard Byrd + Mary B. Moore. m. Melissa Colbert.", "p155", 13, 19, "possible",
                  [byrd_william_leander], spouse="Melissa Colbert")
byrd_john_howard = n("John Howard Byrd", "?", "Son of Michael Byrd + Sally Logan. m. Mary B. Moore.", "p156", 12, 18, "possible",
                    [byrd_benjamin], spouse="Mary B. Moore")
byrd_michael = n("Michael Byrd", "?", "Son of Rev. William M. Byrd + Lydia Adair. m. Sally Logan.", "p157", 11, 18, "possible",
                [byrd_john_howard], spouse="Sally Logan")
byrd_rev_william = n("Rev. William M. Byrd", "?", "Reverend in colonial Byrd family. Son of Richard George + Elizabeth Buster. m. Lydia Adair.", "p158", 10, 18, "possible",
                    [byrd_michael], spouse="Lydia Adair")
byrd_richard_george = n("Richard George Byrd", "?", "Son of John Henry Bird/Byrd + Sarah Carter. m. Elizabeth Buster.", "p159", 9, 18, "possible",
                       [byrd_rev_william], spouse="Elizabeth Buster")
byrd_john_henry = n("John Henry Bird (Byrd)", "fl. ~1700 Westmoreland VA", "EARLIEST documented Byrd patrilineal ancestor (POSSIBLE). m. Sarah Carter. Westmoreland County, Virginia — historical seat of the famous William Byrd dynasty (Westover plantation, founders of Richmond VA 1737); direct relationship to that line unverified but geographically/temporally suggestive.", "p160", 8, 18, "possible",
                   [byrd_richard_george], spouse="Sarah Carter")

# Dale Sr's FATHER — separate node (English immigrant, NAME UNKNOWN)
spence_immigrant = n("Mr. Spence (English immigrant)", "~1900–1915 NE England – ?", "Hunter's paternal great-grandfather (Dale Sr's father). NAME UNKNOWN — top research target. Per agent 41 deep-dive: PROBABLE NE England (Yorkshire/Durham/Northumberland). Arrived Beaumont TX via Galveston ~1920-1935 post-Spindletop oil boom. m. Dovie Byrd.", "p125", 15, 20, "probable")

# Spence root = deepest Byrd ancestor (the long visual chain users will see)
spence_root = byrd_john_henry

# ── HENSLEE branch — deceased anchors tightened from 2026-04-26 public burial/death indexes ──
# Alice Marie Henslee Spence, Lee S. Henslee, and Frances Virginia Henslee now carry sourced dates/places.
# The parent-child bridge between Alice and Lee/Frances remains explicit MEDIUM-confidence pending a direct obituary or vital record.

# Alice Marie Henslee — paternal grandmother — full descent through her 3 children to Hunter
alice_henslee = n("Alice Marie (Henslee) Spence", "13 Jan 1936 Rusk TX – 3 Dec 2005 Beaumont", "Hunter's paternal grandmother. Born Rusk TX; died 3 Dec 2005, buried Forest Lawn Memorial Park Beaumont (Garden of Hope). Daughter of Lee Stuart Henslee + Frances Virginia Rau (CONFIRMED via cousin Henslee GEDCOM). m. Dr. Dale William Spence Sr. (1934- ). Three children: D'Anne (Spence) Patton, Susan (Spence) Clarke, and Dale William Spence Jr. (Hunter's father).", None, 16, 20, "confirmed",
                  [aunt_deanne, aunt_susan, hunter_dad], spouse="Dr. Dale William Spence Sr.")

# Don Henslee + his children
chad_henslee = n("Chad Henslee", "living", "Hunter's first cousin once removed (Don's son)", None, 17, 21, "confirmed")
stacy_george = n("Stacy (Henslee) George", "living", "Hunter's first cousin once removed (Don's daughter)", None, 17, 21, "confirmed")
jennifer_tyler = n("Jennifer (Henslee) Tyler", "living", "Hunter's first cousin once removed (Don's daughter)", None, 17, 21, "confirmed")

don_henslee = n("Don Henslee", "living", "Frances + Lee Stuart's son; Hunter's paternal grand-uncle. m. Joann Carlin (1942-2022). Lives Nederland TX.",
                "p112", 16, 20, "confirmed",
                [chad_henslee, stacy_george, jennifer_tyler], spouse="Joann (Carlin) Henslee")

# Frances Virginia (Rau) Henslee — maiden name confirmed via cousin GEDCOM
frances_rau_henslee = n("Frances Virginia (Rau) Henslee", "1918 Dallas TX – 19 Dec 2008 Nederland TX", "Hunter's paternal great-grandmother. Maiden name RAU confirmed via cousin GEDCOM. Native of Dallas; lived Beaumont 55 yrs (1938-1993) then Nederland. Catholic. Buried Forest Lawn Memorial Park Beaumont. m. Lee Stuart Henslee 60 yrs.", "p140", 15, 20, "confirmed",
                       [alice_henslee, don_henslee], spouse="Lee Stuart Henslee")

rosalie_stephens = n("Rosalie (Henslee) Stephens", "living (2008)", "Frances's sister; m. Steve Stephens; lives Allen TX.", None, 15, 20, "confirmed", spouse="Steve Stephens")

# Frances's parents — RAU + REECE (newly identified via cousin GEDCOM)
frank_rau = n("Frank H. Rau", "?", "Frances Virginia Rau Henslee's father. Hunter's paternal great-great-grandfather. NEWLY identified via cousin Henslee GEDCOM 2026-04-26. Likely German-Texan given surname.", "p141", 14, 20, "confirmed",
              [frances_rau_henslee, rosalie_stephens], spouse="Ethel Lee Reece")

# Lee Stuart Henslee + parents (full Henslee patrilineal chain back to 1727 — multi-tree confirmed)
lee_stuart_henslee = n("Lee Stuart Henslee", "2 Oct 1908 – 31 Aug 1994", "Hunter's paternal great-grandfather. Son of James Ernest 'Pappy' Henslee + Mary Alice Stuart. m. Frances Virginia Rau ~1948 (60-yr marriage). Buried Forest Lawn Memorial Park Beaumont. Per Broussard's Mortuary obituary 2008 + cousin Henslee GEDCOM.", "p111", 15, 20, "confirmed",
                       [alice_henslee, don_henslee], spouse="Frances Virginia (Rau) Henslee")

mary_alice_stuart = n("Mary Alice (Stuart) Henslee", "1887 Caldwell TX – 1981", "Hunter's paternal great-great-grandmother. Born Caldwell, Burleson Co TX. Parents: Lewis Lunsford Stuart + Nora C. Sale.", "p137", 14, 20, "confirmed", spouse="James Ernest 'Pappy' Henslee")

pappy_henslee = n("James Ernest 'Pappy' Henslee", "1885 Lyons, Burleson Co TX – 1948", "Hunter's paternal great-great-grandfather. Son of Miles Reed Henslee + Lula Jane Norville. m. Mary Alice Stuart. Confirmed via cousin GEDCOM (2 trees).", "p136", 14, 20, "confirmed",
                  [lee_stuart_henslee], spouse="Mary Alice Stuart")

miles_reed = n("Miles Reed Henslee", "1856–1894", "m. Lula Jane Norville. Father of James Ernest 'Pappy' Henslee. Cross-confirmed 2 cousin GEDCOMs.", "p135", 13, 19, "probable",
              [pappy_henslee], spouse="Lula Jane Norville")
enoch_2 = n("Enoch Henslee II", "1832–1916", "m. Sarah Jane Hudson. Cross-confirmed 2 cousin GEDCOMs.", "p134", 12, 19, "probable",
           [miles_reed], spouse="Sarah Jane Hudson")
maxfield_2 = n("Maxfield Henslee II", "1810–1900", "m. Mary Blackwell.", "p133", 11, 19, "probable",
              [enoch_2], spouse="Mary Blackwell")
enoch_1 = n("Enoch Henslee", "1788–1860", "m. Amy Mary Hasting.", "p132", 10, 19, "probable",
           [maxfield_2], spouse="Amy Mary Hasting")
david_e_henslee = n("David E Henslee", "1760–1820", "Son of Maxfield + Patty Sneed. m. Mary Payne.", "p131", 9, 18, "probable",
                   [enoch_1], spouse="Mary Payne")
maxfield_1 = n("Maxfield Henslee", "1727–1801", "EARLIEST documented Henslee patrilineal ancestor. m. Jane Snell. Father William Hensley. Cross-confirmed via 3 converging cousin GEDCOMs.", "p130", 8, 18, "probable",
              [david_e_henslee], spouse="Jane Snell")

# Henslee root = deepest Henslee ancestor (Maxfield 1727, ~280 yrs of named ancestors)
henslee_root = maxfield_1
# Rau line as separate sub-anchor (Frances's family — independent of Henslee patrilineal)
rau_root = frank_rau

# Sir Basil Spence — possible distant collateral via the broader Spence surname
sir_basil_spence = n("Sir Basil Spence", "1907–1976", "Scottish architect; rebuilt Coventry Cathedral after WWII bombing. POSSIBLE very distant collateral Spence relative.", "hr024", 16, 20, "possible")

# David Trifon (Shari's first husband, adopted name; biological line untraceable per Hunter)
david_trifon = n("David Trifon", "Shari's first husband", "Sharyn Mattingly's first husband (m. ~1968); biological father of Rachel. Surname Trifon is an ADOPTED name — his biological lineage is untraceable. Per Hunter 2026-04-26: 'don't trace that one back.'", "p020", 16, 20, "confirmed")

# Save the main Mattingly tree (Ellis as root)
OUT.parent.mkdir(parents=True, exist_ok=True)
output_data = {
    "_root_kind": "multi",
    "primary": alric,
    "secondary_trees": [
        {"label": "PATERNAL — Byrd line (Dovie's family: colonial Westmoreland VA ~1700 → Alabama → Milam Co TX → Dale Sr → Hunter)", "tree": spence_root},
        {"label": "PATERNAL — Henslee line (Maxfield 1727 → 7 generations → Lee Stuart 1908 → Alice Marie 1936 → Hunter)", "tree": henslee_root},
        {"label": "PATERNAL — Rau line (Frances Henslee's family: Frank H. Rau + Ethel Lee Reece → Hunter)", "tree": rau_root},
        {"label": "PATERNAL — Spence patrilineal (unnamed English immigrant — name UNKNOWN, top research target)", "tree": spence_immigrant},
        {"label": "MATERNAL-PATERNAL — Teichmüller line (Hans/Johann ~1580 Harz miller → Brunswick → La Grange TX, 6 gens NDB-confirmed)", "tree": teichmueller_root},
        {"label": "MATERNAL — Lepik / Lepick / Mikeska line (Frýdek-Místek Moravia 1862 → Brown Co KS 1881 → Floresville TX; Roman Catholic)", "tree": lepick_root},
        {"label": "MATERNAL — Baity / Beatty line (Scots-Irish: Border Scots → Ulster 1610-40 → PA → NC by 1750s → SA TX; documented to George Baity 1774 Rowan/Surry NC)", "tree": baity_root},
        {"label": "MATERNAL — Boehme/Macker line (Herman F. Boehme + Minna Macker; PROBABLE Prussian Silesia origin → Indianola TX → Lavaca Co)", "tree": boehme_root},
        {"label": "MATERNAL-PATERNAL — Baity line research anchors (North Carolina by 1830 → San Antonio builders by 1910)", "tree": baity_root},
        {"label": "MATERNAL grandfather — David Trifon (adopted-name; biological line untraceable per Hunter)", "tree": david_trifon},
        {"label": "DEBUNKED — Frost dynasty (was UNVERIFIED, agent 25 confirmed Lepick line is the actual maternal line)", "tree": frost_root}
    ]
}
# For backward compat, write the primary tree at top-level (root is now Alric, fl. pre-1066)
OUT.write_text(json.dumps(alric, indent=2, ensure_ascii=False), encoding="utf-8")
# Write the multi-tree variant alongside
MULTI_OUT = OUT.parent / "lineage-tree-multi.json"
MULTI_OUT.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")

# Tree stats
def count(node):
    return 1 + sum(count(c) for c in node.get("children", []))

def depth(node):
    if not node.get("children"):
        return 1
    return 1 + max(depth(c) for c in node["children"])

print(f"Wrote {OUT}")
print(f"Total nodes: {count(alric)}")
print(f"Tree depth: {depth(alric)}")
print(f"Root: {alric['name']} ({alric['dates']})")
