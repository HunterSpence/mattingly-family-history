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

# Hunter's mother — Rachel (per Hunter, 2026-04-26)
rachel = n("Rachel", "living", "Hunter's mother; daughter of Shari + David Spence", None, 17, 21, "confirmed", [hunter])
charmaine = n("Charmaine", "living", "Shari + David's daughter; Hunter's aunt", "p021", 17, 21, "confirmed")

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
    n("Joseph Mattingly", "?", "Mattingly-339; son of Leonard Sr.", None, 11, 18, "probable"),
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
    n("Ignatius Mattingly", "b. 1766", "Mattingly-53; son of Leonard Sr.", None, 11, 18, "probable"),
    n("Susannah (Mattingly) Ray", "b. 1766", "Mattingly-208; m. Ray", None, 11, 18, "probable"),
    n("Basil Mattingly", "b. 1772", "Mattingly-207", None, 11, 18, "probable"),
    n("Susan (Mattingly) Barron", "b. 1775", "Mattingly-78; m. Barron", None, 11, 18, "probable"),
    n("Mary (Mattingly) Buckman", "b. 1777", "Mattingly-205; m. Buckman", None, 11, 18, "probable"),
    n("William Mattingly", "b. 1777", "Mattingly-204", None, 11, 18, "probable"),
    n("Sister Margaret Mattingly", "fl. 1812 KY", "Founding member of the Sisters of Loretto (1812) — the first women's religious order founded west of the Allegheny Mountains. Per Webb 1884.", "p056", 11, 19, "confirmed"),
]
leonard_sr = n("Leonard Mattingly Sr.", "1739–1829 Washington Co KY", "Mattingly-62. 'Old Leonard'; m1. Mary Hayden; m2. Margaret Monarch; m3. Dorothy Hardesty; 10+ named children. SIBLING of Ignatius Jr (NOT direct ancestor of Hunter)", "p044", 10, 18, "confirmed",
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

# Ellis — earliest documented Mattingley individual (root)
ellis = n("Ellis (lord of Mattingley)", "fl. 1167", "First named lord of Mattingley village; recorded in Pipe Roll 13 Henry II", "p073", -3, 12, "possible",
         [revelendus])

# ── Lepick maternal subtree (agent 25 finding — DEFINITIVE) ───────
# Per Leroy Baity Mattingly obituary (Gazette, 24 Mar 2013): Shari's mother is Jennive Lepick.
# Per Jennive's 2008 obituary (Gazette/PPLD): Jennive Imogene Lepick, b. 2 Feb 1923 Floresville TX,
# parents Frederick + Hilda (Boehme) Lepick; one of three children. Dietician degree, Our Lady of the Lake.
# Brother Fred Charles Lepick Jr (1925-2016) was a NAVAL AVIATOR — NOT a banker. The Frost-Bank "uncle"
# claim from Shari's oral history is UNVERIFIED — likely a transmission error.

shari_mother = n("Jennive Imogene Lepick", "2 Feb 1923 Floresville TX – 2008 Colorado Springs", "Shari's mother. m. Leroy Baity Mattingly 18 Dec 1943 at Fort Sill OK. Dietician degree from Our Lady of the Lake College, San Antonio. Find a Grave 36080759.", None, 15, 20, "confirmed",
                 [], spouse="Leroy Baity Mattingly")

# Jennive's siblings (per agent 25)
gertrude_lepick = n("Gertrude (Lepick) Hurlburt", "1920–2000", "Jennive's older sister", None, 15, 20, "confirmed")
fred_lepick_jr = n("Fred Charles Lepick Jr.", "1925–2016", "Jennive's younger brother. Naval Aviator (NOT a banker — Frost Bank 'uncle' oral tradition is debunked).", None, 15, 20, "confirmed")

# Jennive's parents
hilda_boehme = n("Hilda (Boehme) Lepick", "?", "Jennive's mother. Maiden name Boehme.", None, 14, 20, "confirmed")
frederick_lepick = n("Frederick Lepick", "?", "Jennive's father. Lepick family of Wilson County TX.", None, 14, 20, "confirmed",
                    [shari_mother, gertrude_lepick, fred_lepick_jr], spouse="Hilda Boehme")
lepick_root = frederick_lepick

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

# ── Teichmueller maternal-paternal subtree (agent 24 finding) ────────────────────
# Hunter ← Shari (p000) ← Leroy Teichmuller Mattingly (p002) ← May Teichmueller (Edward Sr's wife)
# ← Hans Teichmueller (1837-1901, p003) ← August Teichmueller + Charlotte von Girsewaldt (Brunswick)
# Per agent 24: Gustav Teichmüller (philosopher, 0.82) is PROBABLE brother of Hans (matching parents)

anna_teichmueller = n("Anna Teichmüller", "1861–1940", "German Lieder composer; daughter of Gustav. Wikipedia article. PROBABLE first cousin twice removed of Hans's children.", "p061", 14, 19, "probable")
gustav_teichmueller = n("Gustav Teichmüller", "1832 Brunswick – 1888 Tartu", "German philosopher who influenced Friedrich Nietzsche directly; professor at Dorpat (Tartu) University. PROBABLE 0.82 brother of Hans (matching Brunswick parents per Wikipedia).", "p060", 13, 19, "probable",
                       [anna_teichmueller])

minette = n("Minette Teichmueller (Pohl)", "1871–1970", "WPA muralist — painted 'The Law, Texas Rangers' for Smithville TX post office. Hans's daughter; CONFIRMED great-great-grandaunt of Hunter.", "p004", 14, 19, "confirmed")
may_teichmueller = n("May Teichmueller", "1872 – 28 Aug 1900", "m. Edward Mattingly Sr. 1 Sept 1894; mother of Leroy Teichmuller Mattingly (Hunter's great-grandfather); Hans's other daughter", None, 14, 19, "confirmed")
unknown_5th_child = n("[5th child of Hans]", "?", "Lotto 1902 confirms 5 children but 5th not in TX vital records (pre-1903 records sparse) — UNVERIFIED", None, 14, 19, "possible")

hans = n("Hans Teichmueller", "1837 Brunswick – 1901 La Grange TX", "Hunter's confirmed great-great-grandfather; emigrated to TX 1854; Civil War CSA artillery officer; named for father August. m. Anna Lemke", "p003", 13, 19, "confirmed",
        [may_teichmueller, minette, unknown_5th_child], spouse="Anna Lemke")

august = n("August Teichmüller", "fl. 1820–1860 Brunswick", "Officer in the Brunswick army; per Wikipedia matched both Gustav (Wiki) and Hans (Lotto 1902 KY history). Father of both.", None, 12, 19, "probable",
           [hans, gustav_teichmueller], spouse="Charlotte von Girsewaldt")

teichmueller_root = august

# ── Spence paternal subtree (David Spence, Hunter's paternal grandfather) ─────
# Surname Spence = small clan; Sir Basil Spence (Coventry Cathedral architect) is POSSIBLE distant cousin
sir_basil_spence = n("Sir Basil Spence", "1907–1976", "British architect; rebuilt Coventry Cathedral after WWII bombing. POSSIBLE distant Spence relative of David.", "hr024", 16, 20, "possible")
david_spence = n("David Spence", "Hunter's paternal grandfather", "Shari's first husband; UNVERIFIED specific Spence-line origin. Possible distant connection to James Monroe (5th US President) via Patrick Spence migrant ancestor.", "p020", 16, 20, "confirmed",
                 [sir_basil_spence])
spence_root = david_spence

# Save the main Mattingly tree (Ellis as root)
OUT.parent.mkdir(parents=True, exist_ok=True)
output_data = {
    "_root_kind": "multi",
    "primary": ellis,
    "secondary_trees": [
        {"label": "Maternal Lepick line (Shari's mother's family — Jennive Lepick of Floresville TX)", "tree": lepick_root},
        {"label": "Maternal-paternal Teichmüller line (Brunswick → Texas)", "tree": teichmueller_root},
        {"label": "Paternal Spence clan (David's surname)", "tree": spence_root},
        {"label": "Frost dynasty (PRIOR THEORY — DISPROVEN per agent 25; Frost Bank 'uncle' is unverified oral tradition)", "tree": frost_root}
    ]
}
# For backward compat, write the primary tree at top-level
OUT.write_text(json.dumps(ellis, indent=2, ensure_ascii=False), encoding="utf-8")
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
print(f"Total nodes: {count(ellis)}")
print(f"Tree depth: {depth(ellis)}")
print(f"Root: {ellis['name']} ({ellis['dates']})")
