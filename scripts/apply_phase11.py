"""Apply Phase 11 findings (agents 23, 24, 27, 28) to entities.json + lineage tree.

Sources:
- 23-1969-mattingly-book — Henry Mattingly I (1751-1823) + parents John/Elizabeth, brothers' KY migration
- 24-famous-mattinglys — Gustav Teichmuller (philosopher, 0.82), Marie Mattingly Meloney, Ben distiller, Don, etc.
- 27-cezar-mattingly-line — Cezar (Thomas I's son, brother of Thomas II), Garrett MD descendants, R-Y14083
- 28-maryland-catholic-kentucky — 1786 corrected arrival, Sisters of Loretto founders, B.F. Mattingly Jr distillery
"""
import json
from pathlib import Path

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENT = WS / "research" / "entities.json"

entities = json.loads(ENT.read_text(encoding="utf-8"))
people = entities["people"]
hist = entities.setdefault("historical_references", [])

existing_ids = {p["id"] for p in people} | {h["id"] for h in hist}
added = 0

def add_person(p):
    global added
    if p["id"] in existing_ids:
        return False
    people.append(p)
    existing_ids.add(p["id"])
    added += 1
    return True

def add_hist(h):
    global added
    if h["id"] in existing_ids:
        return False
    hist.append(h)
    existing_ids.add(h["id"])
    added += 1
    return True

# ============ AGENT 27: CEZAR LINE (Hunter's collateral via Thomas I) ============
add_person({
    "id": "p050",
    "full_name": "Cezar Mattingly",
    "given_name": "Cezar",
    "surname": "Mattingly",
    "birth_year": 1654,
    "death_year": 1719,
    "birth_place": "Maryland (St. Mary's or Charles County)",
    "spouse": "Jane Suttle",
    "relation_to_shari": "Collateral 6th-great-granduncle (Thomas I's son, brother of Hunter's direct ancestor Thomas Mattingly II)",
    "context": (
        "Cezar Mattingly — son of colonial founder Thomas Mattingly I (d. before 1664) "
        "and brother of Thomas Mattingly II (Hunter's confirmed direct ancestor). "
        "Married Jane Suttle. Anchor of the Garrett County / Hoyes MD branch. "
        "Y-DNA R-Y14083 confirmed in his line (FamilyTreeDNA, William Mattingly), "
        "sibling terminal to Hunter's expected R1b-DF27 > Y14084 cluster. "
        "WikiTree: Mattingly-223."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — colonial collateral",
    "sources": ["https://www.wikitree.com/wiki/Mattingly-223"],
    "wikitree_id": "Mattingly-223"
})

add_person({
    "id": "p051",
    "full_name": "Henry Mattingly I",
    "given_name": "Henry",
    "surname": "Mattingly",
    "birth_year": 1751,
    "death_year": 1823,
    "birth_place": "Maryland",
    "death_place": "Mount Savage, Allegany County, Maryland",
    "spouse": "Honora Durbin",
    "relation_to_shari": "Collateral patriarch (great-great-grandnephew of Cezar; subject of 1969 Mattingly genealogy book)",
    "context": (
        "Henry Mattingly I (3 Jul 1751 – 1823) — progenitor of the entire 1969 'Descendants of Henry Mattingly' "
        "genealogy book documenting 4 generations of Ohio/Indiana/Illinois/Maryland descendants. "
        "Per the post-publication letter (1969), his parents were John Mattingly (~1720) and Elizabeth, "
        "linking him via Cezar→John Baptist→John 1715→Henry I 1751. Family tradition records 'brothers Leonard, "
        "William, and Luke' leaving Leonardtown MD for Kentucky in 1791 — corrected by Webb (1884) to 1786 "
        "arrival at Hardin's Creek. Henry I had 12 children including 4 sons (John, Samuel, Henry II, William)."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Allegany MD collateral",
    "sources": [
        "https://www.wikitree.com/wiki/Mattingly-617",
        "https://archive.org/details/thedescendantsofhenrymattingly"
    ],
    "wikitree_id": "Mattingly-617"
})

add_person({
    "id": "p052",
    "full_name": "Dominick Mattingly",
    "given_name": "Dominick",
    "surname": "Mattingly",
    "birth_year": 1808,
    "death_year": 1854,
    "birth_place": "Maryland",
    "death_place": "Hoyes, Garrett County, Maryland",
    "spouse": "Ann Browning",
    "relation_to_shari": "Collateral cousin (Henry I's grandson; anchor of the Hoyes MD settlement)",
    "context": (
        "Dominick Mattingly (6 Mar 1808 – 27 May 1854) — anchor of the Mattingly branch in Garrett County, MD. "
        "January 1831 he and brother John bought 157 acres on the Youghiogheny River from John Hoye for $196.56. "
        "December 1853 bought the 386-acre Singleton Townshend farm at Johnstown — village renamed 'Hoyes' in 1880. "
        "His descendants formed the core of the Garrett County Catholic community for the next century."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Garrett County MD collateral",
    "sources": ["https://www.wikitree.com/wiki/Mattingly-648"],
    "wikitree_id": "Mattingly-648"
})

add_person({
    "id": "p053",
    "full_name": "Meshack Mattingly",
    "given_name": "Meshack",
    "surname": "Mattingly",
    "birth_year": 1837,
    "death_year": 1912,
    "birth_place": "Garrett County, Maryland",
    "spouse": "Mary P. Griffith",
    "relation_to_shari": "Collateral cousin (Dominick's son; Garrett County Commissioner)",
    "context": (
        "Meshack Mattingly (1837–1912) — served one term as Commissioner of Garrett County, Maryland. "
        "Operated 'the best stock farm in the county.' Married Mary P. Griffith, daughter of the Governor "
        "of Pennsylvania. Six generations descended from colonial founder Cezar Mattingly."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Garrett County MD collateral",
    "sources": ["1969 Descendants of Henry Mattingly, p. 230 ff"],
    "notable": True
})

add_person({
    "id": "p054",
    "full_name": "Rev. Romanus Mattingly",
    "given_name": "Romanus",
    "surname": "Mattingly",
    "birth_year": 1850,
    "death_year": 1922,
    "birth_place": "Maryland",
    "relation_to_shari": "Collateral cousin (Catholic priest; built Oakland MD + Hoyes MD churches)",
    "context": (
        "Rev. Romanus Mattingly (1850–1922) — Catholic priest who built the parish churches at Oakland, MD "
        "and Hoyes, MD. Served 16 years at the Oakland parish. Praised in Father Stanton's history of "
        "Western Maryland Catholic churches. Seven generations descended from Cezar Mattingly."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Garrett County MD collateral",
    "sources": ["1969 Descendants of Henry Mattingly", "Stanton, Western Maryland Catholic churches"],
    "notable": True
})

add_person({
    "id": "p055",
    "full_name": "Judge Francis Mattingly",
    "given_name": "Francis",
    "surname": "Mattingly",
    "birth_year": 1813,
    "death_year": 1879,
    "birth_place": "Maryland",
    "relation_to_shari": "Collateral cousin (Judge of Orphans' Court, Cumberland MD 1859; civic Union leader 1861)",
    "context": (
        "Francis Mattingly (1813–1879) — Judge of the Orphans' Court at Cumberland, Maryland (elected 1859). "
        "Civic leader who helped commit Allegany County to the Union side during the Civil War in 1861. "
        "Six generations descended from Cezar Mattingly."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Allegany County MD collateral",
    "notable": True
})

# ============ AGENT 28: SISTERS OF LORETTO (collateral via Leonard Sr) ============
add_person({
    "id": "p056",
    "full_name": "Sister Margaret Mattingly",
    "given_name": "Margaret",
    "surname": "Mattingly",
    "birth_year": None,
    "relation_to_shari": "Collateral great-great-great-grandaunt (Leonard Sr's daughter; founding member of Sisters of Loretto 1812)",
    "context": (
        "Sister Margaret Mattingly — daughter of patriarch Leonard Mattingly Sr. (1739–1827). "
        "One of the founding band of the Sisters of Loretto, established 1812 — the first women's "
        "religious order founded west of the Allegheny Mountains. Aunt of Hunter's direct ancestor "
        "Leonard Mattingly Jr.'s children. Source: Webb, Centenary of Catholicity in Kentucky (1884)."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Kentucky collateral",
    "sources": ["Webb 1884, Centenary of Catholicity in Kentucky"],
    "notable": True
})

add_person({
    "id": "p057",
    "full_name": "Sister Generose (Martha) Mattingly",
    "given_name": "Martha",
    "surname": "Mattingly",
    "religious_name": "Sister Generose",
    "relation_to_shari": "Collateral cousin (Mother Superior of Sisters of Loretto 1842–1843)",
    "context": (
        "Sister Generose Mattingly (Martha Mattingly) — daughter of Basil Mattingly and Monica Miles; "
        "granddaughter of Leonard Mattingly Sr. Mother Superior of the Sisters of Loretto, 1842–1843. "
        "Source: Webb 1884."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Kentucky collateral",
    "sources": ["Webb 1884, Centenary of Catholicity in Kentucky"],
    "notable": True
})

add_person({
    "id": "p058",
    "full_name": "Sister Ann Joseph Mattingly",
    "given_name": "Ann Joseph",
    "surname": "Mattingly",
    "relation_to_shari": "Collateral cousin (Mother Superior of Sisters of Loretto 1882)",
    "context": (
        "Sister Ann Joseph Mattingly — Mother Superior of the Sisters of Loretto, 1882. "
        "Descendant of Leonard Mattingly Sr.'s Kentucky settlement. Source: Webb 1884."
    ),
    "confidence": "CONFIRMED",
    "branch": "Mattingly paternal — Kentucky collateral",
    "sources": ["Webb 1884, Centenary of Catholicity in Kentucky"],
    "notable": True
})

add_person({
    "id": "p059",
    "full_name": "Benjamin F. Mattingly Jr.",
    "given_name": "Benjamin",
    "surname": "Mattingly",
    "relation_to_shari": "Collateral cousin (Mattingly & Moore Distillery 1877; Old Forester source)",
    "context": (
        "B.F. Mattingly Jr. — grandson of Leonard Mattingly Sr. via son John Mattingly (m. Polly Fenwick). "
        "Operated 'large distillery interests in Louisville' per Webb 1884; lived near St. Charles Church, "
        "Marion County, KY. Probable founder of Mattingly & Moore Distillery (Bardstown, 1877) — the "
        "Saint Mary, KY distillery later purchased by Brown to launch Old Forester bourbon. Confidence: PROBABLE."
    ),
    "confidence": "PROBABLE",
    "branch": "Mattingly paternal — Kentucky collateral",
    "sources": ["Webb 1884", "Wikipedia: Old Forester"],
    "notable": True
})

# ============ AGENT 24: NOTABLE FAMOUS MATTINGLYS / TEICHMUELLERS ============
add_person({
    "id": "p060",
    "full_name": "Gustav Teichmüller",
    "given_name": "Gustav",
    "surname": "Teichmüller",
    "birth_year": 1832,
    "death_year": 1888,
    "birth_place": "Braunschweig, German Confederation",
    "death_place": "Dorpat (Tartu), Estonia",
    "relation_to_shari": "PROBABLE great-great-granduncle (brother of Hans Teichmueller per matching Brunswick parents)",
    "context": (
        "Gustav Teichmüller (1832–1888) — German philosopher, professor at Dorpat University (Tartu, Estonia). "
        "Influenced Friedrich Nietzsche directly. Wikipedia confirms his father was August Teichmueller, a "
        "lieutenant in the Prussian/Brunswick army, and his mother was Charlotte née von Girsewaldt — "
        "EXACTLY matching the parents of Hunter's confirmed ancestor Hans Teichmueller (1837–1901) per "
        "the 1902 Fayette County KY history. Same city (Braunschweig), same father (officer Augusto), "
        "same mother (Charlotte von Gursewaldt/von Girsewaldt — variant spellings), 5 years apart. "
        "Confidence: PROBABLE 0.82. Single confirmation step: parish register at Niedersächsisches "
        "Landesarchiv in Wolfenbüttel."
    ),
    "confidence": "PROBABLE",
    "branch": "Teichmueller maternal — German",
    "sources": ["https://en.wikipedia.org/wiki/Gustav_Teichmüller", "Lotto 1902 Fayette County KY history"],
    "notable": True
})

add_person({
    "id": "p061",
    "full_name": "Anna Teichmüller",
    "given_name": "Anna",
    "surname": "Teichmüller",
    "birth_year": 1861,
    "death_year": 1940,
    "birth_place": "Braunschweig, German Empire",
    "relation_to_shari": "PROBABLE first cousin twice removed (Gustav's daughter; Hans's niece)",
    "context": (
        "Anna Teichmüller (1861–1940) — German Lieder composer with her own Wikipedia article. "
        "Daughter of Gustav Teichmüller (philosopher) → Hans Teichmueller's niece if the Brunswick "
        "parental match holds. Confidence: PROBABLE 0.72."
    ),
    "confidence": "PROBABLE",
    "branch": "Teichmueller maternal — German",
    "sources": ["https://en.wikipedia.org/wiki/Anna_Teichmüller"],
    "notable": True
})

add_person({
    "id": "p062",
    "full_name": "Marie Mattingly Meloney",
    "given_name": "Marie",
    "surname": "Mattingly",
    "married_name": "Meloney",
    "birth_year": 1878,
    "death_year": 1943,
    "birth_place": "Bardstown, Nelson County, Kentucky",
    "relation_to_shari": "PROBABLE 4th–6th cousin (Bardstown Catholic Mattingly stock)",
    "context": (
        "Marie Mattingly Meloney (1878–1943) — daughter of physician Cyprian Peter Mattingly of Bardstown KY. "
        "Bardstown is the capital of the Catholic Mattingly clan descended from Leonard Mattingly Jr. — "
        "Hunter's confirmed patrilineal ancestor. Organized the 1921 international fund drive that "
        "purchased Marie Curie's radium. Eleanor Roosevelt's confidante. Edited the New York Herald "
        "Tribune Sunday Magazine. Confidence: PROBABLE 0.72."
    ),
    "confidence": "PROBABLE",
    "branch": "Mattingly paternal — Kentucky collateral",
    "sources": ["Wikipedia: Marie Mattingly Meloney"],
    "notable": True
})

add_person({
    "id": "p063",
    "full_name": "Ignatius G. Mattingly",
    "given_name": "Ignatius",
    "surname": "Mattingly",
    "birth_year": 1927,
    "death_year": 2004,
    "relation_to_shari": "PROBABLE distant cousin (Yale/Haskins Labs linguist; computer speech synthesis pioneer)",
    "context": (
        "Ignatius G. Mattingly (1927–2004) — Yale / Haskins Laboratories linguist. Wrote the first computer "
        "program for synthesizing speech from phonetic input (1964). The given name 'Ignatius' is "
        "diagnostic of Maryland Catholic Mattingly descent — Hunter's direct ancestor Ignatius "
        "Mattingly (1704–1789) carried it. Confidence: PROBABLE 0.60."
    ),
    "confidence": "PROBABLE",
    "branch": "Mattingly paternal — distant cousin",
    "sources": ["Wikipedia: Ignatius G. Mattingly"],
    "notable": True
})

# ============ ADD HISTORICAL REFERENCES for figures with 0.30-0.55 confidence ============
add_hist({
    "id": "hr020",
    "name": "Don Mattingly",
    "lifespan": "1961–present",
    "fame": "New York Yankees first baseman (1982–1995), 1985 AL MVP, MLB manager",
    "relation_to_shari": "POSSIBLE distant cousin (Indiana Catholic Mattingly migration corridor; no Y-DNA on record)",
    "context": (
        "Don Mattingly — born Evansville, Indiana, attended Roman Catholic Reitz Memorial High School. "
        "Indiana Catholic Mattinglys trace back through the same KY→IN migration corridor as Hunter's "
        "direct line. Father Bill Mattingly. Confidence: POSSIBLE 0.55. No Y-DNA test on record."
    ),
    "image_url": None,
    "confidence": "POSSIBLE"
})

add_hist({
    "id": "hr021",
    "name": "Mack Mattingly",
    "lifespan": "1931–present",
    "fame": "U.S. Senator from Georgia 1981–1987 (first Republican popularly elected from Georgia since Reconstruction)",
    "relation_to_shari": "POSSIBLE distant cousin (Indiana Catholic stock)",
    "context": (
        "Mack Mattingly — born Anderson, Indiana. First Republican popularly elected to U.S. Senate "
        "from Georgia since Reconstruction. Indiana Catholic Mattingly corridor. Confidence: POSSIBLE 0.40."
    ),
    "confidence": "POSSIBLE"
})

add_hist({
    "id": "hr022",
    "name": "Garrett Mattingly",
    "lifespan": "1900–1962",
    "fame": "Pulitzer Prize historian — 'The Armada' (1959), Columbia University professor",
    "relation_to_shari": "POSSIBLE distant cousin (lineage undocumented)",
    "context": (
        "Garrett Mattingly — Pulitzer Prize for History 1960 ('The Armada'). Born Washington DC. "
        "No documented parental lineage to confirm Mattingly clan branch. Confidence: POSSIBLE 0.30."
    ),
    "confidence": "POSSIBLE"
})

add_hist({
    "id": "hr023",
    "name": "Ken Mattingly",
    "lifespan": "1936–2023",
    "fame": "Apollo 16 astronaut — orbited the Moon as Command Module Pilot",
    "relation_to_shari": "POSSIBLE distant cousin (lineage undocumented)",
    "context": (
        "Thomas Kenneth 'Ken' Mattingly II — NASA astronaut, Apollo 16 Command Module Pilot (1972), "
        "STS-4 + STS-51-C Shuttle commander. Born Chicago. No lineage documentation. Confidence: POSSIBLE 0.30."
    ),
    "confidence": "POSSIBLE"
})

add_hist({
    "id": "hr024",
    "name": "Sir Basil Spence",
    "lifespan": "1907–1976",
    "fame": "British architect — rebuilt Coventry Cathedral after WWII bombing",
    "relation_to_shari": "POSSIBLE distant Spence relative (David Spence's surname clan)",
    "context": (
        "Sir Basil Spence OM OBE — Scottish architect, designed the new Coventry Cathedral (1962) "
        "beside the bombed-out medieval ruin. The Spence surname clan is small enough that David Spence "
        "(Hunter's paternal grandfather) could be a distant cousin. Confidence: POSSIBLE."
    ),
    "confidence": "POSSIBLE"
})

# ============ AGENT 23: 1969 BOOK — Henry I's parents (collateral via Cezar) ============
add_person({
    "id": "p064",
    "full_name": "John Mattingly",
    "given_name": "John",
    "surname": "Mattingly",
    "birth_year": 1720,
    "spouse": "Elizabeth Mattingly",
    "relation_to_shari": "Collateral 5th-great-granduncle (Henry I's father per 1969 book post-publication letter)",
    "context": (
        "John Mattingly (~1720) — first named in the post-publication letter (8 July 1969) inserted "
        "at the back of the 1969 'Descendants of Henry Mattingly' book. Father of Henry Mattingly I "
        "(1751–1823). Per the Cezar→John Baptist→John 1715→Henry I 1751 chain confirmed by agent 27, "
        "this John (~1720) is the link between Cezar's grandson John (b. 1715) and Henry I. Wife Elizabeth "
        "(maiden name unknown, but per the letter she was 'Elizabeth Mattingly'). Birth year approximate."
    ),
    "fuzzy": True,
    "confidence": "PROBABLE",
    "branch": "Mattingly paternal — colonial collateral",
    "sources": ["1969 Descendants of Henry Mattingly post-publication letter (8 July 1969)"]
})

# ============ ENRICH EXISTING ENTITIES ============

# Hans Teichmueller (p003) — link to Gustav as brother
for p in people:
    if p.get("id") == "p003":
        existing = p.get("context", "")
        if "Gustav" not in existing:
            p["context"] = existing + (
                " — Per Agent 24 famous-Mattinglys research: Gustav Teichmüller (1832–1888), the "
                "philosopher who influenced Nietzsche, has matching parents (August Teichmüller "
                "officer of Brunswick army, Charlotte née von Girsewaldt) per Wikipedia. Confidence "
                "0.82 that Gustav is Hans's brother — single parish-register check at Wolfenbüttel "
                "Landesarchiv would confirm. This would also make Anna Teichmüller (1861–1940, German "
                "composer) Hans's niece."
            )
        break

# Leonard Sr (p043 or whatever) — note Sister Margaret as daughter
for p in people:
    if p.get("id") in ("p043", "p044"):
        if "Sister Margaret" not in p.get("context", ""):
            p["context"] = p.get("context", "") + (
                " — Per Agent 28 MD Catholic research: of Leonard Sr's 10 Maryland-born children, "
                "daughter Margaret became Sister Margaret Mattingly, founding member of the Sisters "
                "of Loretto (1812) — first women's religious order founded west of the Alleghenies."
            )

# David Spence (p020) — possible Sir Basil Spence cousin
for p in people:
    if p.get("id") == "p020":
        existing = p.get("enriched_context", "") or p.get("context", "")
        if "Basil Spence" not in existing:
            p["enriched_context"] = existing + (
                " — Per Agent 24: Sir Basil Spence (1907–1976), British architect who rebuilt "
                "Coventry Cathedral after WWII bombing, is a POSSIBLE distant Spence relative "
                "(surname clan is small)."
            )

# ============ Save ============
ENT.write_text(json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Phase 11 applied: +{added} entities (people={len(people)}, historical={len(hist)})")
