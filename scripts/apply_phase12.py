"""Apply Phase 12 new entities (Henslee + Lepik + Boehme + Teichmüller deep + Dovie)."""
import json
from pathlib import Path

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENT = WS / "research" / "entities.json"
d = json.loads(ENT.read_text(encoding="utf-8"))
ids = {p["id"] for p in d["people"]}

new = [
    {"id": "p110", "full_name": "Frances Henslee", "given_name": "Frances", "surname": "Henslee",
     "birth_year": 1918, "birth_place": "Dallas, Texas", "death_year": 2008, "death_place": "Port Arthur, TX",
     "spouse": "Lee Stuart Henslee", "relation_to_shari": "Hunter's paternal great-grandmother",
     "context": "Frances Henslee — Hunter's paternal great-grandmother. Born ~1918 Dallas TX, died 19 Dec 2008 (age 90) at Gulf Health Care Port Arthur. Lived Beaumont 55 years (1938-1993) then Nederland TX. m. Lee Stuart Henslee (60-yr marriage). Member St. Charles Borromeo Catholic Church Nederland. Buried Forest Lawn Memorial Park Beaumont. Daughter Alice Marie Spence (predeceased) + son Don Henslee. CONFIRMED via Broussard's Mortuary obituary 2008.",
     "confidence": "CONFIRMED", "branch": "Henslee paternal-grandmother", "sources": ["Broussard's Mortuary obituary, December 2008"]},
    {"id": "p111", "full_name": "Lee Stuart Henslee", "given_name": "Lee Stuart", "surname": "Henslee",
     "spouse": "Frances Henslee", "relation_to_shari": "Hunter's paternal great-grandfather",
     "context": "Lee Stuart Henslee — m. Frances Henslee 60 years. Predeceased her (before 2008). Children: Alice Marie Spence + Don Henslee. Per Broussard's Mortuary obituary 2008.",
     "confidence": "CONFIRMED", "branch": "Henslee paternal"},
    {"id": "p112", "full_name": "Don Henslee", "given_name": "Don", "surname": "Henslee", "spouse": "Jo Ann",
     "relation_to_shari": "Hunter's paternal grand-uncle (Frances + Lee Stuart's son)",
     "context": "Don Henslee — Frances's son; Hunter's paternal grand-uncle. Lives in Nederland TX. m. Jo Ann. Children: Chad Henslee, Stacy (Henslee) George, Jennifer (Henslee) Tyler.",
     "confidence": "CONFIRMED", "branch": "Henslee paternal"},
    {"id": "p113", "full_name": "Rosalie (Henslee) Stephens", "given_name": "Rosalie", "surname": "Henslee",
     "married_name": "Stephens", "spouse": "Steve Stephens",
     "relation_to_shari": "Hunter's paternal great-grand-aunt",
     "context": "Frances's sister; lives Allen TX. m. Steve Stephens. Per obituary.",
     "confidence": "CONFIRMED", "branch": "Henslee paternal"},
    {"id": "p114", "full_name": "Dovie (?) Spence", "given_name": "Dovie", "surname": "Spence",
     "relation_to_shari": "Hunter's paternal great-grandmother (Dale Sr's mother)",
     "context": "Dovie Spence — mother of Dr. Dale William Spence Sr. (Rice U professor). Maiden name UNKNOWN — agent dispatched. Per Hunter 2026-04-26.",
     "confidence": "CONFIRMED", "branch": "Spence paternal", "open_question": "maiden name"},
    {"id": "p115", "full_name": "Frank Lepik (later Lepick)", "given_name": "Frank", "surname": "Lepik",
     "birth_year": 1862, "birth_place": "Bohemia (Austria-Hungary)", "spouse": "Mary Mikeska",
     "relation_to_shari": "Hunter's maternal 2x-great-grandfather",
     "context": "Frank Lepik — Bohemian immigrant 1881 to Brown County Kansas. Czech surname Lepik Americanized to Lepick by next generation. Father of Fred Charles Lepick Sr (1894-, Hunter's maternal great-grandfather). 9 children. WikiTree Lepik-8.",
     "confidence": "CONFIRMED", "branch": "Lepik/Lepick maternal — Bohemian immigrant"},
    {"id": "p116", "full_name": "Mary (Mikeska) Lepik", "given_name": "Mary", "surname": "Mikeska",
     "married_name": "Lepik", "birth_year": 1863, "birth_place": "Bohemia/Moravia",
     "spouse": "Frank Lepik", "relation_to_shari": "Hunter's maternal 2x-great-grandmother",
     "context": "Mary Mikeska — Czech/Moravian. Mikeska family arrived Kansas 1871 via NE Kansas Czech corridor. m. Frank Lepik. WikiTree Mikeska-77/78.",
     "confidence": "CONFIRMED", "branch": "Mikeska maternal"},
    {"id": "p117", "full_name": "Fred Charles Lepick Sr.", "given_name": "Fred Charles", "surname": "Lepick",
     "birth_year": 1894, "birth_place": "Brown County, Kansas", "spouse": "Hilda Boehme",
     "relation_to_shari": "Hunter's maternal great-grandfather (Jennive's father)",
     "context": "Fred Charles Lepick Sr. — born 8 Mar 1894 Brown Co KS. Moved to Wilson Co TX 1910-1920. m. Hilda Boehme ~1920. Lived San Antonio late 1930s+. Buried Floresville City Cemetery (Find a Grave 55217353). WikiTree Lepick-2. CORRECTS earlier Frederick Lepick placeholder.",
     "confidence": "CONFIRMED", "branch": "Lepick maternal",
     "sources": ["WikiTree Lepick-2", "Find a Grave 55217353", "1895 KS State Census, 1910 AR Census, 1930 Wilson Co TX Census"]},
    {"id": "p118", "full_name": "Herman F. Boehme", "given_name": "Herman", "surname": "Boehme",
     "birth_year": 1863, "birth_place": "Texas", "death_year": 1900, "death_place": "Shiner, Lavaca County TX",
     "relation_to_shari": "Hunter's maternal 2x-great-grandfather",
     "context": "Herman F. Boehme — Hilda Boehme's father. Born 9 Jun 1863 Texas, died 18 Jun 1900 Shiner Lavaca Co TX. Lutheran (buried Sons of Hermann Cemetery). German-Texan. Hilda's mother UNVERIFIED. Per agent 30.",
     "confidence": "CONFIRMED", "branch": "Boehme German-Texan maternal",
     "sources": ["PeopleLegacy via Wayback Machine", "agent 30 research"]},
    {"id": "p119", "full_name": "Hans / Johann Teichmüller", "given_name": "Hans", "surname": "Teichmüller",
     "birth_year": 1580, "death_year": 1638, "birth_place": "Southern Harz mountains, Germany",
     "relation_to_shari": "EARLIEST documented Teichmüller patrilineal ancestor",
     "context": "Hans / Johann Teichmüller (~1580-1638) — master miller (Mühlenmeister) in southern Harz mountains. Surname Teichmüller is occupational: pond miller. Earliest documented ancestor in the Teichmüller patrilineal chain. Per NDB 2016 vol 26 p.6.",
     "confidence": "CONFIRMED", "branch": "Teichmüller maternal-paternal — German",
     "sources": ["Neue Deutsche Biographie vol 26 (2016) p. 6"]},
    {"id": "p120", "full_name": "Joachim Andreas Teichmüller", "given_name": "Joachim Andreas",
     "surname": "Teichmüller", "birth_year": 1705, "death_year": 1778, "birth_place": "Goslar, Harz, Germany",
     "relation_to_shari": "Hunter's 6x-great-grandfather (Teichmüller line)",
     "context": "Joachim Andreas Teichmüller (1705-1778) — Oberfaktor (chief commercial agent) in Goslar at the foot of the Harz mountains. GND 1154326802. Per NDB 2016.",
     "confidence": "CONFIRMED", "branch": "Teichmüller maternal-paternal"},
    {"id": "p121", "full_name": "Wilhelm Ernst Conrad Teichmüller", "given_name": "Wilhelm Ernst Conrad",
     "surname": "Teichmüller", "birth_year": 1758, "death_year": 1835,
     "spouse": "Henriette Christiane Helene Schorkopf",
     "relation_to_shari": "Hunter's 5x-great-grandfather (Teichmüller line)",
     "context": "Oberhütteninspekteur at Karlshütte near Delligsen, Leinebergland. m. Henriette Schorkopf (1763-1818) of Uslar. GND 1154326616. Per NDB 2016.",
     "confidence": "CONFIRMED", "branch": "Teichmüller maternal-paternal"},
    {"id": "p122", "full_name": "August Wilhelm Teichmüller", "given_name": "August Wilhelm",
     "surname": "Teichmüller", "birth_year": 1795, "death_year": 1855,
     "spouse": "Charlotte Georgine Elisabeth von Girsewald",
     "relation_to_shari": "Hunter's 4x-great-grandfather",
     "context": "August Wilhelm Teichmüller (1795-1855) — Seconde-Lieutenant in the Schwarzen Corps des Majors Olfermann, Brunswick army (NOT Prussian). m. Charlotte Georgine Elisabeth von Girsewald (1799-1860). 5 children. Per NDB 2016. Father of both Hans + Gustav (sibling relationship NOW CONFIRMED).",
     "confidence": "CONFIRMED", "branch": "Teichmüller maternal-paternal"},
    {"id": "p123", "full_name": "Wilhelm Teichmüller", "given_name": "Wilhelm", "surname": "Teichmüller",
     "birth_year": 1834, "death_year": 1869, "spouse": "Bertha Kuntzen",
     "relation_to_shari": "Hans/Gustav's brother — Hunter's great-great-grand-uncle",
     "context": "Wilhelm Teichmüller (1834-1869) — Premier-Lieutenant + Schriftsteller. m. Bertha Kuntzen. POSSIBLE father of pianist Robert Teichmüller (1863-1939). Per NDB 2016.",
     "confidence": "CONFIRMED", "branch": "Teichmüller maternal-paternal"},
    {"id": "p124", "full_name": "Wilhelmina (Minette) Teichmüller", "given_name": "Wilhelmina",
     "surname": "Teichmüller", "birth_year": 1829, "death_year": 1886, "spouse": "Karl Mollenhauer",
     "relation_to_shari": "Hans/Gustav's sister — Hunter's great-great-grand-aunt (NOT to be confused with Hans's daughter Minette Pohl b.1871)",
     "context": "Wilhelmina Teichmüller (1829-1886) — m. Karl Mollenhauer (Protestant pastor + Superintendent at Bockenem, Niedersachsen). Per NDB 2016.",
     "confidence": "CONFIRMED", "branch": "Teichmüller maternal-paternal"},
]
added = 0
for p in new:
    if p["id"] not in ids:
        d["people"].append(p)
        ids.add(p["id"])
        added += 1
ENT.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Added {added} entities. Total people={len(d['people'])}")
