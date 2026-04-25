"""Apply notable deeds from research/14-notable-deeds.json to entities.json.
Agent 14 used its own ID scheme — map by person_name to our entities.json IDs.
"""
import json
from pathlib import Path

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
DEEDS = WORKSPACE / "research" / "14-notable-deeds.json"
ENTITIES = WORKSPACE / "research" / "entities.json"

deeds_data = json.loads(DEEDS.read_text(encoding="utf-8"))
entities = json.loads(ENTITIES.read_text(encoding="utf-8"))

# Manual ID mapping based on agent 14's person_name → my entity IDs
# (Entity 14 used its own p001, p002... while my entities.json has different IDs)
NAME_TO_ENTITY_ID = {
    "Ellis of Mattingley": "p073",
    "Stephen de Mattingley": "p070",
    "Peter de Mattingley": "p072",
    "Thomas Mattingly II": "p039",
    "Cezar Mattingly": "p038",
    "Ignatius Mattingly": "p043",
    "Leonard Mattingly Jr.": "p045",
    "Hans Teichmueller": "p003",
    "Minette Teichmueller": "p004",
    "Hugo Pohl": "p005",
    "Pearl (Paralee) Johnson Baity": "p006",
    "William Alexander Baity": "p010",
    "Dr. Claude Mattingly": "p011",
    "The Centenarian": "p030",
    "Joseph Hardin Frost": "p018",
    # "Mattingly & Moore Distillery": Organization, not a person
}

count = 0
for deed in deeds_data.get("notable_deeds", []):
    name = (deed.get("person_name") or "").split(" (")[0].strip()  # strip "(fl. 1167)" suffix
    eid = NAME_TO_ENTITY_ID.get(name)
    if not eid:
        # Try variations
        for k, v in NAME_TO_ENTITY_ID.items():
            if k in name or name in k:
                eid = v
                break
    if not eid:
        print(f"  NO MATCH: {deed.get('person_name')}")
        continue
    target = next((p for p in entities["people"] if p.get("id") == eid), None)
    if not target:
        print(f"  ENTITY NOT FOUND: {eid} for {name}")
        continue
    target["notable_deed"] = {
        "headline": deed.get("headline", ""),
        "story": deed.get("story", ""),
        "year": deed.get("year"),
        "place": deed.get("place"),
        "tag": deed.get("tag", ""),
        "verification": deed.get("verification", []),
    }
    count += 1
    print(f"  Applied: {eid} | {deed.get('headline','')[:70]}")

ENTITIES.write_text(json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nTotal applied: {count} of {len(deeds_data.get('notable_deeds', []))}")
