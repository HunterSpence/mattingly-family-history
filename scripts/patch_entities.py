"""Apply Hunter's clarifications to entities.json.

Updates:
- David (p020): Shari's first husband + Hunter's grandfather (LIVING, ~80)
- Charmaine (p021): Shari's daughter + Hunter's aunt (LIVING)
- Stephanie: Shari's sister or niece (LIVING, uncertain)
- Hunter (p001), brother (p022), sister (p023), cousins (p024): redact names
- Add audience policy (family-with-redactions)
- Add Sharyn as formal-name alternate for Shari

Saves entities.json in place (backup to entities.original.json).
"""
import json
import shutil
from pathlib import Path

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENTITIES = WORKSPACE / "research" / "entities.json"
BACKUP = WORKSPACE / "research" / "entities.original.json"

if not BACKUP.exists():
    shutil.copy(ENTITIES, BACKUP)
    print(f"Backed up to: {BACKUP.name}")

data = json.loads(ENTITIES.read_text(encoding="utf-8"))

# Add audience + redaction policy
data["audience_policy"] = {
    "primary_audience": "family",
    "redaction_rule": "Living relatives' names redacted in the public/shareable HTML version. Full names shown in the family-only version.",
    "redaction_set": ["p001", "p022", "p023", "p024"],
    "show_living_with_role": ["p020", "p021"],
    "notes_from_hunter": [
        "David is Shari's first husband and Hunter's paternal grandfather, age ~80, living.",
        "Charmaine is Shari's daughter and Hunter's aunt, living.",
        "Stephanie is uncertain — possibly Shari's sister or niece, living.",
        "Hunter's siblings and three cousins to be redacted (no names known/given).",
        "Aunt Monette is Shari's great-great-aunt per transcript ('my great great aunt')."
    ]
}

# Add formal-name note to subject
for p in data.get("people", []):
    if p.get("id") == "p000":
        p["alternate_spellings"] = list(set(p.get("alternate_spellings", []) + ["Sharyn"]))
        p["notes_from_hunter"] = "Hunter's grandmother. Spelled 'Sharyn' formally; goes by 'Shari'."
    elif p.get("id") == "p001":
        p["full_name_redacted"] = "Hunter [redacted in public version]"
        p["context"] = "The interviewer (grandson). Surname Spence. Redacted in shareable version."
    elif p.get("id") == "p020":  # David
        p["full_name"] = "David"
        p["relation_to_shari"] = "first husband"
        p["relation_to_hunter"] = "paternal grandfather"
        p["context"] = "Shari's first husband, Hunter's paternal grandfather. Walked with Shari at Texas A&M when she recognized Hugo Pohl's paintings. Currently ~80 years old, living, healthy (no dementia)."
        p["living_flag"] = True
        p["fuzzy"] = False
        p["research_priority"] = "low"
    elif p.get("id") == "p021":  # Charmaine
        p["full_name"] = "Charmaine"
        p["relation_to_shari"] = "daughter"
        p["relation_to_hunter"] = "aunt"
        p["context"] = "Shari's daughter, Hunter's aunt. Brought a family oil painting to Shari from Hunter's parents. O-negative blood type (per Shari)."
        p["living_flag"] = True
        p["fuzzy"] = False
        p["research_priority"] = "low"
    elif p.get("id") in ["p022", "p023", "p024"]:  # brother, sister, cousins
        p["redact_in_public"] = True
        p["research_priority"] = "skip"
    elif p.get("id") == "p035":  # doctor
        p["redact_in_public"] = True

# Add Stephanie if not already
people_names = [p.get("full_name", "") for p in data["people"]]
if "Stephanie" not in people_names:
    data["people"].append({
        "id": "p037",
        "full_name": "Stephanie",
        "given_name": "Stephanie",
        "relation_to_shari": "possibly sister or niece (per Hunter)",
        "relation_to_hunter": "great-aunt or first cousin once removed (uncertain)",
        "context": "Shari started to say 'He was born in Stephanie' then corrected to Charmaine — likely a slip of the tongue but Stephanie may be a real living relative. Per Hunter: possibly Shari's sister or niece.",
        "living_flag": True,
        "fuzzy": True,
        "research_priority": "skip",
        "redact_in_public": True,
        "transcript_timestamps": ["20:42"]
    })

ENTITIES.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated: {ENTITIES.name}")
print(f"  audience: {data['audience_policy']['primary_audience']}")
print(f"  redaction set: {data['audience_policy']['redaction_set']}")
print(f"  show with role: {data['audience_policy']['show_living_with_role']}")
print(f"  total people: {len(data['people'])}")
