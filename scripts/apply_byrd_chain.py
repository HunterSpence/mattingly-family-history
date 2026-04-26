"""Apply the Byrd patrilineal chain (Dovie Spence's family) — found in 4 cousin GEDCOMs.

Chain (multi-tree converged):
- Dovie BYRD (Hunter's paternal great-grandmother, Dale Sr's mother) — PROBABLE
- John Archie Asner Byrd (1868 Birmingham AL - 1928) + Martha Alice Bedford — PROBABLE parents
- Pvt William Leander Byrd (1832 Frankfort AL - 1889) + Margarete Rhetta Peradeau
- Benjamin Franklin Byrd (1798) + Melissa Colbert
- John Howard Byrd + Mary B. Moore
- Michael Byrd + Sally Logan
- Rev. William M. Byrd + Lydia Adair
- Richard George Byrd + Elizabeth Buster
- John Henry Bird/Byrd + Sarah Carter (~early 1700s Westmoreland VA — colonial Virginia origin)

Convergent across: KcaMarco, L.B., B.G., Frances Padgett (all paternal-side cousins).
"""
import json
from pathlib import Path

ENT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history\research\entities.json")

d = json.loads(ENT.read_text(encoding="utf-8"))
ids = {p["id"] for p in d["people"]}

new = [
    # ── Update Dovie's entity with maiden name = BYRD ──
    # (we update p114 in place below)

    # John Archie Asner Byrd + Martha Alice Bedford (PROBABLE parents of Dovie)
    {"id": "p150", "full_name": "John Archie Asner Byrd", "given_name": "John Archie Asner",
     "surname": "Byrd", "birth_year": 1868, "death_year": 1928,
     "birth_place": "Birmingham, Jefferson County, Alabama",
     "spouse": "Martha Alice Bedford",
     "relation_to_shari": "Hunter's paternal great-great-grandfather (PROBABLE — Dovie Byrd's father)",
     "context": ("John Archie Asner Byrd (1868 Birmingham AL – 1928) — likely father of Dovie Byrd. "
                 "Per cousin KcaMarco GEDCOM (paternal side, 1st cousin 2x removed). m. Martha Alice "
                 "Bedford. Their son Otha Lee 'Othar' Byrd (1902-1989) settled in Milam County, TX — "
                 "the same region as Dale Spence Sr's Beaumont/SE Texas family. Ancestral chain "
                 "extends back through Pvt William Leander Byrd (1832 AL CSA Civil War) to colonial "
                 "Virginia (Westmoreland Co). Cross-confirmed in 2 cousin GEDCOMs."),
     "confidence": "PROBABLE", "branch": "Byrd paternal — colonial Virginia → Alabama → Texas",
     "sources": ["KcaMarco cousin GEDCOM", "L.B. cousin GEDCOM", "B.G. cousin GEDCOM"]},

    {"id": "p151", "full_name": "Martha Alice (Bedford) Byrd", "given_name": "Martha Alice",
     "surname": "Bedford", "married_name": "Byrd", "spouse": "John Archie Asner Byrd",
     "relation_to_shari": "Hunter's paternal great-great-grandmother (PROBABLE — Dovie's mother)",
     "context": ("Martha Alice Bedford (Byrd) — Dovie Byrd's mother (PROBABLE). m. John Archie Asner "
                 "Byrd. Per cousin KcaMarco GEDCOM."),
     "confidence": "PROBABLE", "branch": "Bedford"},

    # Otha Lee Byrd (1902-1989) — Hunter's paternal grand-uncle if Dovie is his sister
    {"id": "p152", "full_name": "Otha Lee 'Othar' Byrd", "given_name": "Otha Lee", "surname": "Byrd",
     "birth_year": 1902, "death_year": 1989, "birth_place": "Milam County, Texas",
     "spouse": "Mattie Doris Curlee",
     "relation_to_shari": "Hunter's paternal grand-uncle (PROBABLE — Dovie's brother)",
     "context": ("Otha Lee Byrd (1902 Milam Co TX – 1989) — likely Dovie Byrd's brother (Hunter's "
                 "paternal grand-uncle). m. Mattie Doris Curlee; daughter Sharon Kay Byrd "
                 "(1944 Velasco TX – 2020). Per cousin KcaMarco GEDCOM."),
     "confidence": "PROBABLE", "branch": "Byrd paternal collateral"},

    # Pvt William Leander Byrd (1832-1889) — Hunter's paternal 3x-great-grandfather
    {"id": "p153", "full_name": "Pvt William Leander Byrd", "given_name": "William Leander",
     "surname": "Byrd", "birth_year": 1832, "death_year": 1889,
     "birth_place": "Frankfort, Franklin County, Alabama",
     "spouse": "Margarete Rhetta (Perideaux) Peradeau",
     "relation_to_shari": "Hunter's paternal 3x-great-grandfather (PROBABLE)",
     "context": ("Private William Leander Byrd (1832-1889) — Confederate States Army soldier per "
                 "rank prefix. Born Frankfort, Franklin Co, Alabama. m. Margarete Rhetta Peradeau "
                 "(1829 Alabama – 1925). Father of John Archie Asner Byrd. Cross-confirmed in 3 "
                 "cousin GEDCOMs (KcaMarco, L.B., B.G.)."),
     "confidence": "PROBABLE", "branch": "Byrd paternal",
     "sources": ["3 cousin GEDCOMs"]},

    {"id": "p154", "full_name": "Margarete Rhetta (Peradeau) Byrd", "given_name": "Margarete Rhetta",
     "surname": "Peradeau", "married_name": "Byrd", "birth_year": 1829, "death_year": 1925,
     "birth_place": "Alabama", "spouse": "Pvt William Leander Byrd",
     "relation_to_shari": "Hunter's paternal 3x-great-grandmother (PROBABLE)",
     "context": ("Margarete Rhetta Perrydore Peradeau (1829-1925) — French/Huguenot surname "
                 "Peradeau/Perrydore/Perideaux. Parents: Paul Perridaux Peradore + Lauretta Peradore. "
                 "m. Pvt William Leander Byrd. Lived to age 96."),
     "confidence": "PROBABLE", "branch": "Peradeau (French Huguenot)"},

    # Benjamin Franklin Byrd (1798) — Hunter's paternal 4x-great-grandfather
    {"id": "p155", "full_name": "Benjamin Franklin Byrd", "given_name": "Benjamin Franklin",
     "surname": "Byrd", "birth_year": 1798, "spouse": "Melissa Colbert",
     "relation_to_shari": "Hunter's paternal 4x-great-grandfather (POSSIBLE)",
     "context": ("Benjamin Franklin Byrd (b. 1798) — father of Pvt William Leander Byrd. m. Melissa "
                 "Colbert. Parents: John Howard Byrd + Mary B. Moore."),
     "confidence": "POSSIBLE", "branch": "Byrd paternal"},

    {"id": "p156", "full_name": "John Howard Byrd", "given_name": "John Howard",
     "surname": "Byrd", "spouse": "Mary B. Moore",
     "relation_to_shari": "Hunter's paternal 5x-great-grandfather (POSSIBLE)",
     "context": "John Howard Byrd. Parents: Michael Byrd + Sally Logan.",
     "confidence": "POSSIBLE", "branch": "Byrd paternal"},

    {"id": "p157", "full_name": "Michael Byrd", "given_name": "Michael", "surname": "Byrd",
     "spouse": "Sally Logan",
     "relation_to_shari": "Hunter's paternal 6x-great-grandfather (POSSIBLE)",
     "context": "Michael Byrd. Parents: Rev. William M. Byrd + Lydia Adair.",
     "confidence": "POSSIBLE", "branch": "Byrd paternal"},

    {"id": "p158", "full_name": "Rev. William M. Byrd", "given_name": "Rev. William M.",
     "surname": "Byrd", "spouse": "Lydia Adair",
     "relation_to_shari": "Hunter's paternal 7x-great-grandfather (POSSIBLE)",
     "context": ("Rev. William M. Byrd — colonial-era Reverend in the Byrd family. m. Lydia Adair. "
                 "Parents: Richard George Byrd + Elizabeth Buster."),
     "confidence": "POSSIBLE", "branch": "Byrd paternal"},

    {"id": "p159", "full_name": "Richard George Byrd", "given_name": "Richard George",
     "surname": "Byrd", "spouse": "Elizabeth Buster",
     "relation_to_shari": "Hunter's paternal 8x-great-grandfather (POSSIBLE)",
     "context": ("Richard George Byrd — colonial Virginia. Parents: John Henry Bird (Byrd) + "
                 "Sarah Carter."),
     "confidence": "POSSIBLE", "branch": "Byrd paternal — colonial Virginia"},

    {"id": "p160", "full_name": "John Henry Bird (Byrd)", "given_name": "John Henry",
     "surname": "Bird (Byrd)", "spouse": "Sarah Carter",
     "relation_to_shari": "Hunter's paternal 9x-great-grandfather (EARLIEST documented Byrd ancestor — POSSIBLE)",
     "context": ("John Henry Bird (Byrd) — earliest documented Byrd patrilineal ancestor in cousin "
                 "GEDCOMs. m. Sarah Carter. Likely colonial Virginia (Westmoreland County region — "
                 "the same area as the famous Byrd family of Westover, founders of Richmond VA, "
                 "though direct connection to William Byrd I/II/III not yet established)."),
     "confidence": "POSSIBLE", "branch": "Byrd paternal — colonial Virginia"},

    # The L.B. tree's parallel chain (Richard Byrd 1717 Westmoreland VA - 1808)
    {"id": "p161", "full_name": "Richard Byrd of Westmoreland", "given_name": "Richard",
     "surname": "Byrd", "birth_year": 1717, "death_year": 1808,
     "birth_place": "Westmoreland, Virginia, United States",
     "spouse": "Sarah Jane Jones",
     "relation_to_shari": "Hunter's paternal 7x-great-grandfather (POSSIBLE — alternate Byrd chain)",
     "context": ("Richard Byrd of Westmoreland VA (1717-1808) — alternate Byrd chain per L.B. cousin "
                 "GEDCOM. Westmoreland County, Virginia is the historical seat of the prominent Byrd "
                 "family (William Byrd I founded Westover plantation; William Byrd II founded "
                 "Richmond VA in 1737). Direct ancestral relationship to that line not yet established "
                 "but geographic/temporal overlap is suggestive."),
     "confidence": "POSSIBLE", "branch": "Byrd paternal — Westmoreland VA"},
]

added = 0
for p in new:
    if p["id"] not in ids:
        d["people"].append(p); ids.add(p["id"])
        added += 1

# Update Dovie (p114) with maiden name = Byrd + parents
for p in d["people"]:
    if p.get("id") == "p114":
        p["full_name"] = "Dovie (Byrd) Spence"
        p["maiden_name"] = "Byrd"
        p["surname"] = "Byrd"
        p["married_name"] = "Spence"
        p["context"] = (
            "Dovie Byrd Spence — Hunter's paternal great-grandmother (Dale William Spence Sr's mother). "
            "Maiden name BYRD (per Hunter family knowledge 2026-04-26). PROBABLE parents: John Archie "
            "Asner Byrd (1868 Birmingham AL – 1928) + Martha Alice Bedford. PROBABLE brother: Otha Lee "
            "Byrd (1902-1989, Milam County TX). The Byrd patrilineal line traces back through "
            "Pvt William Leander Byrd (1832 Alabama, CSA private) and continues to colonial Virginia "
            "(Westmoreland Co region). Multi-tree confirmation from KcaMarco + L.B. + B.G. + "
            "Frances Padgett cousin GEDCOMs (all paternal side)."
        )
        p["confidence"] = "PROBABLE"
        p["sources"] = ["Hunter family knowledge", "4 cousin GEDCOMs (KcaMarco, L.B., B.G., Frances Padgett)"]

ENT.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Added {added} Byrd-line entities. Total people: {len(d['people'])}")
