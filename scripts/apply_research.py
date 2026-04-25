"""Apply confirmed research findings back to entities.json.

This is run after research subagents complete to enrich the structured data
with verified facts, corrected names, and source URLs.

Currently applies:
- Pohl/Monette/Texas Art research (03-pohl-monette-art.md)
  → Minette Teichmueller correction (was "Monette")
  → Hugo Pohl 1878-1960 confirmation
  → 1904 World's Fair correction (was "1903")
  → La Grange, TX birthplace (was "Louisiana")

Future passes will add: Mattingly lineage, Texas places, English origins, scandal/loose ends, full pedigree.
"""
import json
from pathlib import Path

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENTITIES = WORKSPACE / "research" / "entities.json"

data = json.loads(ENTITIES.read_text(encoding="utf-8"))

confirmed_research = {}

# p004: Monette → Minette Teichmueller (CONFIRMED)
for p in data["people"]:
    if p.get("id") == "p004":
        p["full_name"] = "Minette Teichmueller (Pohl)"
        p["given_name"] = "Minette"
        p["surname"] = "Pohl"
        p["maiden_name"] = "Teichmueller"
        p["alternate_spellings"] = list(set(p.get("alternate_spellings", []) + ["Monette", "Minette Pohl"]))
        p["birth_year"] = 1871
        p["birth_place"] = "La Grange, Texas"
        p["death_year"] = 1970
        p["death_place"] = "Nacogdoches, Texas"
        p["occupation"] = "Muralist (WPA Treasury Section); painted 'The Law, Texas Rangers' for Smithville TX post office, 1940"
        p["fuzzy"] = False
        p["sources"] = [
            "https://en.wikipedia.org/wiki/Minette_Teichmueller",
        ]
        p["enriched_context"] = (
            "Minette Teichmueller (called 'Monette' by Shari) was herself a documented WPA muralist. "
            "Born in La Grange, Texas (not Louisiana as Shari recalled). Studied at Chicago Academy of Fine Arts "
            "and the San Antonio Academy of Art. Her 1940 mural 'The Law, Texas Rangers' still hangs in the "
            "Smithville, Texas post office. Maiden name Teichmueller — same German-Texan family that gave "
            "Leroy Teichmuller Mattingly his middle name."
        )
        p["wikipedia_url"] = "https://en.wikipedia.org/wiki/Minette_Teichmueller"
        confirmed_research["p004"] = "CONFIRMED via Wikipedia"

    elif p.get("id") == "p005":  # Hugo Pohl
        p["full_name"] = "Hugo D. Pohl"
        p["given_name"] = "Hugo"
        p["surname"] = "Pohl"
        p["birth_year"] = 1878
        p["death_year"] = 1960
        p["death_place"] = "San Antonio, Texas (assumed)"
        p["occupation"] = "Painter and art teacher; San Antonio Municipal Auditorium stage curtain (1926, destroyed 1979)"
        p["fuzzy"] = False
        p["sources"] = [
            "https://en.wikipedia.org/wiki/Minette_Teichmueller",
            "https://en.wikipedia.org/wiki/San_Antonio_Municipal_Auditorium",
        ]
        p["enriched_context"] = (
            "Hugo D. Pohl (1878–1960) — San Antonio painter. His most famous work was the 36×75-foot, "
            "5,600-pound asbestos stage curtain at the San Antonio Municipal Auditorium (1926), depicting "
            "the 1718 founding of San Antonio with portraits of Bowie, Crockett, Travis, and Bonham. "
            "Curtain destroyed in 1979 fire. Also taught at the Hungarian Academy of Arts (Pál Fried was a student). "
            "Reference: Dictionary of Texas Artists, 1800–1945 (Grauer & Grauer); Art for History's Sake (Steinfeldt / Witte Museum)."
        )
        p["wikipedia_url"] = "https://en.wikipedia.org/wiki/San_Antonio_Municipal_Auditorium"
        confirmed_research["p005"] = "CONFIRMED via Wikipedia"

# Add Hans Teichmueller relationship hint
for p in data["people"]:
    if p.get("id") == "p003":  # Hans Teichmueller
        p["enriched_context"] = (
            "Hans Teichmueller — likely a brother or close relative of Minette Teichmueller (1871–1970). "
            "The family photo Shari mentioned ('on the internet under Hans Teichmueller') is likely from this German-Texan family. "
            "Surname connects to Leroy Teichmuller Mattingly's middle name — Leroy's mother was almost certainly a Teichmueller."
        )
        confirmed_research["p003"] = "PROBABLE — German-Texan family, related to Minette"

# Update event e003 — Mark Twain encounter (location correction)
for e in data.get("events", []):
    if e.get("id") == "e003":
        e["enriched_context"] = (
            "Mark Twain conducted the 'Twins of Genius' reading tour with George Washington Cable in 1884–85, "
            "which did include Southern cities like New Orleans. If Minette was 16 when she snuck out, that would be "
            "1887 — two years after the documented tour. Either Shari's age estimate is approximate (Minette was likely "
            "13–14 in 1884–85), OR Twain made a later Southern appearance not in the standard timeline. "
            "Verification target: Mark Twain Project (marktwainproject.org)."
        )
        e["place"] = "Louisiana (per Shari) — though Minette was born/raised in La Grange, Texas. Family may have been visiting."

# Update event e004 — World's Fair (1904 not 1903)
for e in data.get("events", []):
    if e.get("id") == "e004":
        e["date_or_year"] = "1904 (NOT 1903 — Shari's recollection was off; the Louisiana Purchase Exposition ran April 30 – December 1, 1904)"
        e["enriched_context"] = (
            "The St. Louis World's Fair (Louisiana Purchase Exposition) was originally planned for 1903 (the centennial) "
            "but delayed to 1904 for full international participation. The 1944 film 'Meet Me in St. Louis' is set "
            "during 1903–04 anticipating the fair, which is why Shari said '1903.' Pearl Baity attended in 1904. "
            "$5,000 then ≈ $180,000 in 2025 dollars."
        )
        e["sources"] = ["https://en.wikipedia.org/wiki/Louisiana_Purchase_Exposition"]

# --- Findings from 05-scandal-and-loose-ends.md ---
# Ignatius is likely an ancestor's name (Catholic naming tradition)
oq = data.get("open_questions", [])
new_oq = []
for q in oq:
    if "WORLD'S FAIR DATE" in q:
        continue
    if "IGNATIUS" in q:
        new_oq.append(
            "IGNATIUS [0:00]: Most likely a Mattingly ancestor named Ignatius (Catholic naming tradition — "
            "Maryland Catholic Mattinglys routinely used Ignatian names). A real Ignatius G. Mattingly (1927–2004), "
            "Yale/Harvard linguist, exists. Recommend asking Shari directly: 'Who was Ignatius in your family?'"
        )
        continue
    new_oq.append(q)
data["open_questions"] = new_oq

# Add scientific corrections
for hr in data.get("historical_references", []):
    if hr.get("id") == "hr014":  # Mitochondrial Eve
        hr["correction"] = "Mitochondrial Eve is ~155,000 years old (range 130,000–200,000 BP), NOT 240,000 as Shari recalled. Source: Wikipedia, current consensus."
    if hr.get("id") == "hr010":  # Basque O-negative
        hr["correction"] = "Basques have ~47% Rh-negative overall (world's highest, confirmed) but only ~24-25% O-negative specifically (not ~30% as Shari said). Underlying claim about uniquely high Basque Rh-negativity is correct."

# Texas governor: Sul Ross identified as strongest candidate
for p in data.get("people", []):
    if p.get("id") == "p034":  # Texas governor (unnamed)
        p["full_name"] = "Lawrence Sullivan Ross (PROBABLE)"
        p["enriched_context"] = (
            "Strongest candidate: Sul Ross (governor 1887–1891). His family settled Milam County in central Texas in 1839 — "
            "exactly the corridor where 1880 immigrants via Galveston settled. Pat Neff (gov. 1921–25) is a weaker alternative. "
            "Confirmation needed: which central Texas county did the great-aunt's family settle in?"
        )
        p["wikipedia_url"] = "https://en.wikipedia.org/wiki/Sul_Ross"
        confirmed_research[p["id"]] = "PROBABLE — Sul Ross"

# Frost Bank uncle: probably Frost by blood
for p in data.get("people", []):
    if p.get("id") == "p018":  # Mother's brother (Frost Bank president)
        p["enriched_context"] = (
            "Probable Frost family member by blood. Frost Bank (founded 1868 by Thomas Claiborne Frost) has been "
            "exclusively Frost-family-controlled since founding. For Shari's maternal uncle to be president, he was "
            "almost certainly a Frost — meaning Shari's grandmother (her mother's mother) was a Frost. Tom Frost III "
            "(1929–2018) led the bank through the 1977 Cullen merger and is the era-fitting candidate. "
            "Verification: Shari's mother's maiden name."
        )
        confirmed_research[p["id"]] = "PROBABLE — Frost family by blood"

# Add Ignatius G. Mattingly as a possible historical reference
hist_refs = data.get("historical_references", [])
if not any(h.get("id") == "hr018" for h in hist_refs):
    hist_refs.append({
        "id": "hr018",
        "subject": "Ignatius G. Mattingly (1927–2004)",
        "type": "person",
        "shari_claim": "Possibly the 'Ignatius' Shari mentioned at 0:00. American linguist, Yale/Harvard, NSA analyst, professor at UConn, researcher at Haskins Laboratories. The Maryland Catholic Mattingly family commonly used the name Ignatius (after St Ignatius of Loyola).",
        "verifiable": True,
        "wikipedia_url": "https://en.wikipedia.org/wiki/Ignatius_Mattingly",
        "transcript_timestamps": ["0:00"]
    })
    confirmed_research["hr018"] = "Added Ignatius G. Mattingly as possible referent"

# --- Findings from 02-texas-places.md ---
# 211 Castillo Avenue (NOT Castile)
for pl in data.get("places", []):
    if pl.get("id") == "pl004":
        pl["name"] = "211 Castillo Avenue, San Antonio, TX 78210"
        pl["type"] = "street_address"
        pl["country"] = "USA"
        pl["coordinates"] = {"lat": 29.3969, "lng": -98.4829}
        pl["enriched_context"] = (
            "211 Castillo Avenue (Spanish for 'castle' or 'fortress'), San Antonio, TX 78210, "
            "in the Lavaca/Southtown district south of downtown. Built ~1905 by Pearl Baity's husband "
            "(a successful San Antonio builder). Pearl lived there until her death in 1971; sold in the 1980s. "
            "Shari heard 'Castile' but the actual spelling is the Spanish 'Castillo.'"
        )
        pl["sources"] = ["https://www.google.com/maps/place/211+Castillo+Ave,+San+Antonio,+TX+78210"]
        pl["fuzzy"] = False
        confirmed_research["pl004"] = "CONFIRMED — 211 Castillo Avenue"

for pl in data.get("places", []):
    if pl.get("id") == "pl005":  # Reeves County
        pl["enriched_context"] = (
            "1900 population: 1,847 (Shari's '2 people in Reeves County' quip is well-grounded). "
            "2020 census: 14,748 (Shari said 18,000; 1960 peak was 17,644). The 1901–1905 Texas "
            "school-land law made cheap purchase possible at the exact moment Pearl bought."
        )
    if pl.get("id") == "pl006":  # Wolfcamp Shale
        pl["enriched_context"] = (
            "USGS November 2016 assessment: 20 billion barrels of oil technically recoverable — "
            "the LARGEST USGS oil estimate ever announced at that time. Royalties beginning ~2010 "
            "for mineral-rights holders is consistent with when fracking unlocked this formation."
        )
        pl["sources"] = ["https://pubs.usgs.gov/fs/2016/3092/fs20163092.pdf"]
    if pl.get("id") == "pl027":  # Spindletop
        pl["enriched_context"] = (
            "Spindletop, Beaumont TX. The famous 'Lucas Gusher' on January 10, 1901 produced "
            "100,000 barrels per day, launching the Texas oil age. Pearl Baity bought her Reeves "
            "County land roughly 3 months later."
        )

# --- Findings from 04-english-origins.md ---
# Thomas Mattingly: arrived 1663-64 (not 1660), Mattingly's Hope patent 1666
for p in data.get("people", []):
    if p.get("id") == "p028":  # Thomas Mattingly
        p["full_name"] = "Thomas Mattingly I"
        p["birth_year"] = 1623
        p["death_year"] = 1665
        p["birth_place"] = "England (likely Hampshire — near Mattingley village)"
        p["death_place"] = "Charles County, Maryland"
        p["enriched_context"] = (
            "Thomas Mattingly I (~1623–~1665), the immigrant ancestor. First Maryland records appear "
            "1663–1664 (NOT 1660 as family tradition holds). King at the time was Charles II (Restoration 1660), "
            "not James (James II reigned 1685–88). Came as Catholic refugee following Cromwell's interregnum and "
            "the Restoration. His sons Thomas II and Cezar received the 'Mattingly's Hope' 300-acre land patent "
            "in Charles County, Maryland on September 4, 1666 — likely after Thomas I had died."
        )
        p["sources"] = [
            "https://msa.maryland.gov/",  # Maryland State Archives
        ]
        p["fuzzy"] = False
        confirmed_research["p028"] = "CONFIRMED — Thomas Mattingly I, b.~1623, came 1663-64, d.~1665"

# Update Mattingly's Hope place
for pl in data.get("places", []):
    if pl.get("id") == "pl018":  # Mattingly's Hope
        pl["enriched_context"] = (
            "Mattingly's Hope: 300-acre land patent in Charles County, Maryland, issued September 4, 1666 "
            "to Thomas Mattingly II and Cezar Mattingly (sons of immigrant Thomas I, who had died). "
            "It was a LAND PATENT, not a village (Shari called it 'a little village type thing'). "
            "Charles County is in southern Maryland on the Potomac, the original Catholic settlement region."
        )
        pl["country"] = "USA (Maryland)"
        pl["sources"] = ["https://msa.maryland.gov/"]

# Update Mattingley village
for pl in data.get("places", []):
    if pl.get("id") == "pl015":  # Mattingly village in England
        pl["name"] = "Mattingley, Hampshire"
        pl["country"] = "England"
        pl["enriched_context"] = (
            "Mattingley village is in HAMPSHIRE (between Hook and Reading), NOT near Cambridge as Shari recalled. "
            "It's about 75 miles from Cambridge. Domesday Book (1086) records it as 'Matingelege' with "
            "8 villagers, 3 smallholders, and a mill worth 5 shillings. Etymology: Old English 'Matta' "
            "(personal name) + 'inga' (people of) + 'leah' (clearing/woodland) = 'woodland clearing of the people of Matta.' "
            "Founding dates to the 5th–6th century (post-Roman Anglo-Saxon era), not strictly the 8th as Shari said."
        )
        pl["coordinates"] = {"lat": 51.2855, "lng": -0.9550}
        pl["sources"] = ["https://opendomesday.org/place/SU7357/mattingley/"]
        pl["fuzzy"] = False

# Mattingly Row doesn't exist
for pl in data.get("places", []):
    if pl.get("id") == "pl016":  # Mattingly Row
        pl["enriched_context"] = (
            "No 'Mattingly Row' street exists in England (verified). Shari may have confused this detail. "
            "She is correct that Mattingley village exists — but it's in Hampshire, not Cambridge."
        )
        pl["fuzzy"] = True
        pl["confidence"] = "DOES NOT EXIST"

# Update Beringa tribe -> Basingas
for hr in data.get("historical_references", []):
    if hr.get("id") == "hr012":  # Beringa tribe
        hr["subject"] = "Basingas (Wessex tribe, NOT 'Beringa')"
        hr["correction"] = (
            "The tribe Shari called 'Beringa' was actually the BASINGAS — a documented Wessex Anglo-Saxon "
            "tribe led by Basa, whose name survives in Old Basing and Basingstoke (22 km from Mattingley). "
            "Matta was a member or chief of a Basingas clan. 'Beringa' is a phonetic corruption of 'Basingas' "
            "passed down through generations of oral family tradition."
        )
        hr["wikipedia_url"] = "https://en.wikipedia.org/wiki/Basingstoke"

# Update Daniel Boone / Boonesborough
for hr in data.get("historical_references", []):
    if hr.get("id") == "hr008":  # Daniel Boone
        hr["correction"] = (
            "Two corrections to the family story: (1) Boonesborough was founded in 1775, not the 1780s. "
            "(2) The Maryland Catholic Mattinglys actually migrated to Nelson County / Bardstown KY in 1785 — "
            "a SEPARATE stream from Boone's settlement. The Mattingly & Moore Distillery (Bardstown, 1877) "
            "and the earlier J. Mattingly 1845 distillery confirm the Kentucky distilling lineage is real."
        )

# Add Cezar Mattingly as new person
people = data.get("people", [])
if not any(p.get("id") == "p038" for p in people):
    people.append({
        "id": "p038",
        "full_name": "Cezar Mattingly",
        "given_name": "Cezar",
        "surname": "Mattingly",
        "relation_to_shari": "ancestor (uncertain whether direct or collateral; son of immigrant Thomas I)",
        "context": "Son of Thomas Mattingly I; co-recipient of the Mattingly's Hope land patent September 4, 1666 with brother Thomas II.",
        "research_priority": "high",
        "transcript_timestamps": [],
        "fuzzy": True
    })
    confirmed_research["p038"] = "Added Cezar Mattingly (son of Thomas I)"

if not any(p.get("id") == "p039" for p in people):
    people.append({
        "id": "p039",
        "full_name": "Thomas Mattingly II",
        "given_name": "Thomas",
        "surname": "Mattingly",
        "relation_to_shari": "ancestor (uncertain whether direct or collateral; son of immigrant Thomas I)",
        "context": "Son of Thomas Mattingly I; co-recipient of the Mattingly's Hope land patent September 4, 1666 with brother Cezar. Possibly the direct ancestor of the Texas/Kentucky Mattingly lines.",
        "research_priority": "high",
        "transcript_timestamps": [],
        "fuzzy": True
    })
    confirmed_research["p039"] = "Added Thomas Mattingly II (son of Thomas I)"
data["people"] = people

# --- Findings from 01-mattingly-lineage.md ---
# Hans Teichmueller is the "judge in Texas" (CONFIRMED) — Leroy's maternal grandfather
for p in data["people"]:
    if p.get("id") == "p003":  # Hans Teichmueller
        p["full_name"] = "Hans Teichmueller"
        p["given_name"] = "Hans"
        p["surname"] = "Teichmueller"
        p["birth_year"] = 1837
        p["birth_place"] = "Brunswick, Germany"
        p["death_year"] = 1901
        p["death_place"] = "La Grange, Fayette County, Texas"
        p["occupation"] = "District Judge, 22nd Judicial District of Texas (1884–1901), based in La Grange"
        p["relation_to_shari"] = "great-great-grandfather (maternal-paternal — Leroy Mattingly's mother's father)"
        p["fuzzy"] = False
        p["enriched_context"] = (
            "Hans Teichmueller (1837–1901) — born March 7, 1837 in Brunswick, Germany; died February 17, 1901 "
            "in La Grange, Texas. District Judge of the 22nd Judicial District of Texas (Fayette County) "
            "from 1884 to 1901. **HE IS THE 'judge in Texas' Shari mentioned**, but Shari slightly compressed "
            "the genealogy: he was Leroy's MATERNAL GRANDFATHER, not paternal grandfather. Hans's daughter "
            "May Teichmueller married Ed Mattingly — that union produced Leroy Teichmuller Mattingly "
            "(named for his German maternal grandfather), Claude, and Aunt Mamie. The 1902 Fayette County "
            "history book at the Library of Congress contains his full biography and portrait — that's "
            "the photo Shari said is 'on the Internet under Hans Teichmueller.'"
        )
        p["sources"] = ["https://www.loc.gov/item/02023423/"]
        p["wikipedia_url"] = ""
        confirmed_research["p003"] = "CONFIRMED — Hans Teichmueller, German judge of Fayette County 1884-1901"

# Add May Teichmueller Mattingly (Leroy's mother)
if not any(p.get("id") == "p040" for p in data["people"]):
    data["people"].append({
        "id": "p040",
        "full_name": "May Teichmueller Mattingly",
        "given_name": "May",
        "maiden_name": "Teichmueller",
        "surname": "Mattingly",
        "relation_to_shari": "great-grandmother (paternal — Leroy's mother)",
        "birth_year": None,
        "birth_place": "La Grange, Fayette County, Texas (likely)",
        "death_year": 1900,  # approximate
        "death_place": "Texas",
        "occupation": "(unknown)",
        "context": "Daughter of Judge Hans Teichmueller (German immigrant). Married Ed Mattingly. Mother of Leroy Teichmuller Mattingly (1898), Claude Mattingly (~1899), and Aunt Mamie (1900-02). Per Shari, she 'died at childbirth giving birth to Aunt Mamie' around 1900-02.",
        "fuzzy": True,
        "research_priority": "high",
        "sources": ["https://www.loc.gov/item/02023423/"]
    })
    confirmed_research["p040"] = "Added May Teichmueller Mattingly (Leroy's mother)"

# Add Ed Mattingly (Leroy's father)
if not any(p.get("id") == "p041" for p in data["people"]):
    data["people"].append({
        "id": "p041",
        "full_name": "Ed Mattingly",
        "given_name": "Ed",
        "surname": "Mattingly",
        "relation_to_shari": "great-grandfather (paternal — Leroy's father)",
        "birth_year": None,
        "death_year": None,
        "birth_place": None,
        "death_place": None,
        "occupation": "(possibly judge — Shari said 'his father was a judge in Texas'; could conflict with Hans T being the documented judge)",
        "context": "Father of Leroy Teichmuller Mattingly, Claude Mattingly, and Aunt Mamie. Married May Teichmueller. Lived in La Grange, Fayette County, Texas. Confirmed alive in 1934 when Claude died (his body was returned to Ed in La Grange). The Mattingly half of the Texas family, descending from the Maryland Catholic Mattinglys.",
        "fuzzy": True,
        "research_priority": "high",
        "sources": []
    })
    confirmed_research["p041"] = "Added Ed Mattingly (Leroy's father, in La Grange)"

# Update Claude Mattingly with full scandal details
for p in data["people"]:
    if p.get("id") == "p011":  # Claude Mattingly
        p["full_name"] = "Dr. Claude Mattingly"
        p["given_name"] = "Claude"
        p["surname"] = "Mattingly"
        p["birth_year"] = 1898  # estimate — was 35 at death in Jan 1934
        p["death_year"] = 1934
        p["death_place"] = "Texan Hotel, Austin, Texas"
        p["occupation"] = "Pediatrician (specialist in children's diseases); practiced in Austin TX. WWI Marine Corps veteran. UT Medical Branch Galveston graduate."
        p["fuzzy"] = False
        p["enriched_context"] = (
            "Dr. Claude Mattingly died January 31, 1934 at the Texan Hotel in **Austin** (NOT San Antonio "
            "as Shari recalled). It was a confirmed suicide pact with **Mrs. Rhea B. Perrin** — the wife "
            "of a University of Texas psychology professor. The pair died of a narcotic injection. "
            "AP and INS wire-service articles ran February 1–6, 1934 in Texas newspapers. Claude was 35, "
            "a pediatrician practicing in Austin for six years, trained at UT Medical Branch Galveston, "
            "and had served in the Marine Corps in World War I. His body was returned to La Grange, where "
            "his father Ed Mattingly was still living. The family's 'we don't talk about him' silence and "
            "Shari's recollection of 'probably overdose' are confirmed — though it was specifically a "
            "double suicide by narcotic injection with a married woman, openly covered by the press at the time."
        )
        p["sources"] = [
            "AP wire articles, Texas newspapers, February 1-6, 1934 (Newspapers.com or Briscoe Center microfilm)",
        ]
        confirmed_research["p011"] = "CONFIRMED — Dr. Claude Mattingly, suicide pact at Texan Hotel Austin Jan 31 1934"

# Resolve open question about Claude scandal
oq = data.get("open_questions", [])
data["open_questions"] = [q for q in oq if "CLAUDE MATTINGLY DEATH YEAR" not in q and "HANS TEICHMULLER RELATIONSHIP" not in q]

# Update event e009 (Claude's death)
for e in data.get("events", []):
    if e.get("id") == "e009":
        e["date_or_year"] = "January 31, 1934"
        e["place"] = "Texan Hotel, Austin, Texas (NOT San Antonio)"
        e["enriched_context"] = (
            "Confirmed via AP/INS wire coverage Feb 1-6, 1934. Suicide pact with Mrs. Rhea B. Perrin "
            "(wife of UT psychology professor). Method: narcotic injection. Claude was 35, a pediatrician."
        )

# Audit log for what's been applied
data.setdefault("research_applied", {})
for k, v in confirmed_research.items():
    data["research_applied"][k] = v

ENTITIES.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Applied research to entities.json")
for k, v in confirmed_research.items():
    print(f"  {k}: {v}")
print()
print(f"Open questions remaining: {len(data.get('open_questions', []))}")
