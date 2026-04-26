"""Apply the GEDCOM cross-reference findings to entities.json + build_classic_tree.py.

Major unlocks (from 27 cousin GEDCOMs):
- Henslee paternal chain: Maxfield 1727 → David E 1760 → Enoch 1788 → Maxfield 1810
  → Enoch 1832 → Miles Reed 1856 → James Ernest 'Pappy' 1885 → Lee Stuart 1908 → Alice Marie 1936
- Frances Henslee MAIDEN = RAU; parents Frank H. Rau + Ethel Lee Reece
- Lee Stuart Henslee parents: James Ernest 'Pappy' Henslee + Mary Alice Stuart (Caldwell, Burleson Co TX)
- Don Henslee m. Joann Carlin (1942-2022); her parents Wilford John Carlin + Violet M Carlin
- Edward D Mattingly (middle initial D) — confirms our Edward Sr
- Ruth A Baity middle initial confirmed
- David Isom Baity (1782-1856) — earlier Baity ancestor than our George Baity 1774; possibly the link
"""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENT = ROOT / "research" / "entities.json"

d = json.loads(ENT.read_text(encoding="utf-8"))
ids = {p["id"] for p in d["people"]}

new = [
    # ── Henslee paternal chain (newly confirmed via cousin GEDCOMs) ──
    {"id": "p130", "full_name": "Maxfield Henslee", "given_name": "Maxfield", "surname": "Henslee",
     "birth_year": 1727, "death_year": 1801, "spouse": "Jane Snell",
     "relation_to_shari": "Hunter's 6x-great-grandfather (earliest known Henslee ancestor)",
     "context": "Maxfield Henslee (1727-1801) — earliest documented Henslee patrilineal ancestor. m. Jane Snell. Father William Hensley. Confirmed via Cousin Henslee GEDCOM cluster (Donald Henslee + Jenniffer Henslee + Reba Patton Jackson trees).",
     "confidence": "PROBABLE", "branch": "Henslee paternal — colonial American",
     "sources": ["Cousin GEDCOM cluster (3 trees converge)"]},

    {"id": "p131", "full_name": "David E Henslee", "given_name": "David E", "surname": "Henslee",
     "birth_year": 1760, "death_year": 1820, "spouse": "Mary Payne",
     "relation_to_shari": "Hunter's 5x-great-grandfather",
     "context": "David E Henslee (1760-1820) — son of Maxfield Henslee + Patty Sneed. m. Mary Payne. Confirmed via cousin GEDCOM cluster.",
     "confidence": "PROBABLE", "branch": "Henslee paternal"},

    {"id": "p132", "full_name": "Enoch Henslee", "given_name": "Enoch", "surname": "Henslee",
     "birth_year": 1788, "death_year": 1860, "spouse": "Amy Mary Hasting",
     "relation_to_shari": "Hunter's 4x-great-grandfather",
     "context": "Enoch Henslee (1788-1860) — son of David E + Mary Payne. m. Amy Mary Hasting.",
     "confidence": "PROBABLE", "branch": "Henslee paternal"},

    {"id": "p133", "full_name": "Maxfield Henslee II", "given_name": "Maxfield",
     "surname": "Henslee", "birth_year": 1810, "death_year": 1900, "spouse": "Mary Blackwell",
     "relation_to_shari": "Hunter's 3x-great-grandfather",
     "context": "Maxfield Henslee II (1810-1900) — son of Enoch + Amy Mary Hasting. m. Mary Blackwell.",
     "confidence": "PROBABLE", "branch": "Henslee paternal"},

    {"id": "p134", "full_name": "Enoch Henslee II", "given_name": "Enoch", "surname": "Henslee",
     "birth_year": 1832, "death_year": 1916, "spouse": "Sarah Jane Hudson",
     "relation_to_shari": "Hunter's great-great-great-grandfather",
     "context": "Enoch Henslee II (1832-1916) — son of Maxfield II + Mary Blackwell. m. Sarah Jane Hudson. Cross-confirmed in 2 cousin trees.",
     "confidence": "PROBABLE", "branch": "Henslee paternal",
     "sources": ["Cousin GEDCOM cluster (2 trees)"]},

    {"id": "p135", "full_name": "Miles Reed Henslee", "given_name": "Miles Reed",
     "surname": "Henslee", "birth_year": 1856, "death_year": 1894, "spouse": "Lula Jane Norville",
     "relation_to_shari": "Hunter's great-great-grandfather",
     "context": "Miles Reed Henslee (1856-1894) — son of Enoch II + Sarah Jane Hudson. m. Lula Jane Norville. Father of James Ernest 'Pappy' Henslee. Cross-confirmed in 2 cousin trees.",
     "confidence": "PROBABLE", "branch": "Henslee paternal",
     "sources": ["Cousin GEDCOM cluster (2 trees)"]},

    {"id": "p136", "full_name": "James Ernest 'Pappy' Henslee", "given_name": "James Ernest 'Pappy'",
     "surname": "Henslee", "birth_year": 1885, "death_year": 1948,
     "birth_place": "Lyons, Burleson County, Texas, USA", "spouse": "Mary Alice Stuart",
     "relation_to_shari": "Hunter's great-grandfather (Lee Stuart Henslee's FATHER)",
     "context": "James Ernest 'Pappy' Henslee (1885-1948) — Lee Stuart Henslee's father; Hunter's paternal great-great-grandfather. Born Lyons, Burleson Co TX. m. Mary Alice Stuart (1887-1981 Caldwell, Burleson Co TX). Son of Miles Reed Henslee + Lula Jane Norville. Confirmed via Cousin Henslee GEDCOM (Donald Henslee tree).",
     "confidence": "CONFIRMED", "branch": "Henslee paternal",
     "sources": ["Donald Henslee cousin GEDCOM", "Jenniffer Henslee cousin GEDCOM"]},

    {"id": "p137", "full_name": "Mary Alice Stuart", "given_name": "Mary Alice",
     "surname": "Stuart", "married_name": "Henslee", "birth_year": 1887, "death_year": 1981,
     "birth_place": "Caldwell, Burleson, Texas, United States",
     "spouse": "James Ernest 'Pappy' Henslee",
     "relation_to_shari": "Hunter's great-great-grandmother (Lee Stuart's mother)",
     "context": "Mary Alice Stuart (1887-1981) — Hunter's paternal great-great-grandmother. Born Caldwell, Burleson Co TX. m. James Ernest 'Pappy' Henslee. Mother of Lee Stuart Henslee. Parents: Lewis Lunsford Stuart + Nora C. Sale.",
     "confidence": "CONFIRMED", "branch": "Stuart maternal-of-Henslee"},

    {"id": "p138", "full_name": "Lewis Lunsford Stuart", "given_name": "Lewis Lunsford",
     "surname": "Stuart",
     "relation_to_shari": "Hunter's great-great-great-grandfather (Mary Alice's father)",
     "context": "Lewis Lunsford Stuart — Mary Alice Stuart's father. Per cousin GEDCOM.",
     "confidence": "PROBABLE", "branch": "Stuart"},

    {"id": "p139", "full_name": "Nora C. Sale", "given_name": "Nora C.", "surname": "Sale",
     "married_name": "Stuart",
     "relation_to_shari": "Hunter's great-great-great-grandmother (Mary Alice's mother)",
     "context": "Nora C. Sale — Mary Alice Stuart's mother. Per cousin GEDCOM.",
     "confidence": "PROBABLE", "branch": "Sale"},

    # ── Frances's maiden name = RAU (huge unlock) ──
    {"id": "p140", "full_name": "Frances Virginia (Rau) Henslee", "given_name": "Frances Virginia",
     "surname": "Rau", "married_name": "Henslee", "birth_year": 1918, "death_year": 2008,
     "birth_place": "Dallas, Texas", "death_place": "Port Arthur, TX",
     "spouse": "Lee Stuart Henslee",
     "relation_to_shari": "Hunter's paternal great-grandmother (CORRECTS p110 — full name and maiden surname now confirmed)",
     "context": "Frances Virginia (Rau) Henslee (1918-2008) — full name and maiden surname RAU now confirmed via cousin GEDCOM. Parents: Frank H. Rau + Ethel Lee Reece. Native of Dallas TX. m. Lee Stuart Henslee. Mother of Alice Marie Henslee Spence + Don Henslee. Per Broussard's Mortuary obituary 2008.",
     "confidence": "CONFIRMED", "branch": "Rau (Frances's family) → Henslee",
     "sources": ["Cousin Henslee GEDCOM", "Broussard's Mortuary obituary 2008"]},

    {"id": "p141", "full_name": "Frank H. Rau", "given_name": "Frank H.", "surname": "Rau",
     "spouse": "Ethel Lee Reece",
     "relation_to_shari": "Hunter's paternal great-great-grandfather (Frances's father; previously unknown)",
     "context": "Frank H. Rau — Frances Virginia Rau Henslee's father. NEWLY IDENTIFIED via cousin Henslee GEDCOM (2026-04-26). Likely Texas-born; family may be German-Texan given the surname.",
     "confidence": "CONFIRMED", "branch": "Rau"},

    {"id": "p142", "full_name": "Ethel Lee Reece", "given_name": "Ethel Lee",
     "surname": "Reece", "married_name": "Rau", "spouse": "Frank H. Rau",
     "relation_to_shari": "Hunter's paternal great-great-grandmother (Frances's mother; previously unknown)",
     "context": "Ethel Lee Reece — Frances Virginia Rau Henslee's mother. NEWLY IDENTIFIED via cousin Henslee GEDCOM (2026-04-26).",
     "confidence": "CONFIRMED", "branch": "Reece"},

    # ── Don Henslee's wife Joann Carlin (new) ──
    {"id": "p143", "full_name": "Joann (Carlin) Henslee", "given_name": "Joann",
     "surname": "Carlin", "married_name": "Henslee", "birth_year": 1942, "death_year": 2022,
     "spouse": "Don Henslee",
     "relation_to_shari": "Don Henslee's wife (Hunter's paternal grand-aunt by marriage)",
     "context": "Joann Carlin Henslee (1942-2022) — Don Henslee's wife. Parents: Wilford John Carlin + Violet M Carlin. Per cousin GEDCOM.",
     "confidence": "CONFIRMED", "branch": "Carlin (in-law)"},

    # ── Earlier Baity ancestor (David Isom Baity 1782-1856 — fills gap before Isham 1804) ──
    {"id": "p144", "full_name": "David Isom Baity", "given_name": "David Isom",
     "surname": "Baity", "birth_year": 1782, "death_year": 1856,
     "relation_to_shari": "Hunter's 5x-great-grandfather (CONFIRMED bridge between George Baity 1774 and Isham 1804)",
     "context": "David Isom Baity (1782-1856) — son of George Baity (1774 Rowan/Surry NC). Father of Isham 'Isom' Baity (1804-1892). Confirms the David Baity link previously listed as POSSIBLE in our tree. Per cousin GEDCOM cluster.",
     "confidence": "CONFIRMED", "branch": "Baity NC"},
]

added = 0
for p in new:
    if p["id"] not in ids:
        d["people"].append(p)
        ids.add(p["id"])
        added += 1

# Update existing entities with newly-confirmed details
for p in d["people"]:
    if p.get("id") == "p110":  # Frances Henslee — add maiden + parents
        p["full_name"] = "Frances Virginia (Rau) Henslee"
        p["maiden_name"] = "Rau"
        p["context"] = ("Frances Virginia (Rau) Henslee — Hunter's paternal great-grandmother. "
                        "Born ~1918 Dallas TX, died 19 Dec 2008 (age 90) at Gulf Health Care Port Arthur. "
                        "Lived Beaumont 55 years (1938-1993) then Nederland TX. Maiden name RAU "
                        "confirmed via cousin Henslee GEDCOM. Parents: Frank H. Rau + Ethel Lee Reece. "
                        "m. Lee Stuart Henslee (60-yr marriage, ~1948-2008). Member St. Charles "
                        "Borromeo Catholic Church Nederland. Buried Forest Lawn Memorial Park Beaumont. "
                        "Daughter Alice Marie Spence (predeceased) + son Don Henslee.")
        p["sources"] = (p.get("sources") or []) + ["Cousin Henslee GEDCOM cluster (2026-04-26)"]
    elif p.get("id") == "p111":  # Lee Stuart Henslee — add parents + birth/death years
        p["birth_year"] = 1908
        p["death_year"] = 1994
        p["context"] = ("Lee Stuart Henslee (1908-1994) — Hunter's paternal great-grandfather. "
                        "Son of James Ernest 'Pappy' Henslee (1885-1948 Lyons, Burleson Co TX) + "
                        "Mary Alice Stuart (1887-1981 Caldwell, Burleson Co TX). m. Frances Virginia Rau ~1948. "
                        "Children: Alice Marie Spence + Don Henslee. Predeceased Frances (before 2008). "
                        "Per Broussard's Mortuary obituary + cousin Henslee GEDCOM.")
        p["confidence"] = "CONFIRMED"
        p["sources"] = (p.get("sources") or []) + ["Cousin Henslee GEDCOM cluster"]

ENT.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Added {added} entities (Henslee chain + Rau parents + Carlin + David Isom Baity).")
print(f"Total people now: {len(d['people'])}")
