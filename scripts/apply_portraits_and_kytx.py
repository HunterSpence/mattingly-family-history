"""Apply agent 13 (portraits) + agent 10 (KY-TX gap) findings to entities.json."""
import json
from pathlib import Path

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENT = WS / "research" / "entities.json"
PORTRAITS = WS / "research" / "13-portraits-and-images.json"
KYTX = WS / "research" / "10-kentucky-to-texas.json"

entities = json.loads(ENT.read_text(encoding="utf-8"))
portraits = json.loads(PORTRAITS.read_text(encoding="utf-8"))
kytx = json.loads(KYTX.read_text(encoding="utf-8"))

# Map agent 13 entity_id → my entities.json id
PORTRAIT_ID_MAP = {
    "p_hans_teichmueller": "p003",
    "p_hugo_pohl": "p005",
    "p_minette_teichmueller": "p004",
    "p_claude_mattingly": "p011",
    "p_leroy_mattingly": "p002",
    "p_william_baity": "p010",
    "p_pearl_baity": "p006",
    "h_mark_twain": "hr001",
    "h_william_sherman": "hr002",
    "h_daniel_boone": "hr008",
    "h_sul_ross": "p034",
    "h_oliver_cromwell": "hr007",
    "h_cecilius_calvert": "p032",
}

count = 0
all_portraits = (portraits.get("person_portraits", []) +
                 portraits.get("historical_figure_images", []))

for p in all_portraits:
    src_id = p.get("entity_id")
    url = p.get("image_url")
    if not url or url.lower() in ("none", "(none)"):
        continue
    my_id = PORTRAIT_ID_MAP.get(src_id)
    if not my_id:
        print(f"  no map for {src_id}")
        continue
    # Find target in entities.people OR entities.historical_references
    target = None
    for arr_name in ("people", "historical_references"):
        for ent in entities.get(arr_name, []):
            if ent.get("id") == my_id:
                target = ent
                break
        if target:
            break
    if not target:
        print(f"  entity not found: {my_id}")
        continue
    target["portrait_url"] = url
    target["portrait_caption"] = p.get("image_caption", "")
    target["portrait_source"] = p.get("source", "")
    target["portrait_license"] = p.get("license", "")
    print(f"  Applied portrait: {my_id} ({src_id})")
    count += 1

# Apply agent 10 — Leonard Jr's children + George Thomas Mattingly candidate
# Agent 10 confirmed Leonard Jr. (p045) had 4 children: Mary Alvey (1798), Henry Martin Sr. (1799),
# William Cissell (1807), Leonard III (1828). George Thomas Mattingly (b.1830 Marion KY,
# WikiTree-695) is the strongest Texas-migrant candidate.

# Update Leonard Jr. with children list
for p in entities["people"]:
    if p.get("id") == "p045":
        p["children_named"] = [
            "Mary Alvey Mattingly (b. 1798)",
            "Henry Martin Mattingly Sr. (b. 1799)",
            "William Cissell Mattingly (b. 1807)",
            "Leonard Mattingly III (b. 1828)",
        ]
        p["enriched_context"] = (p.get("context") or "") + (
            " — Per Agent 10 KY-TX research: had exactly 4 children. "
            "Henry Martin Sr. had 9 children born 1828-1844 in Marion/Washington County, KY. "
            "Of Leonard Jr.'s grandchildren, **George Thomas Mattingly** (b. 1830 Marion KY, "
            "WikiTree-695) is the only one with NO Kentucky death record — strongest "
            "POSSIBLE candidate for the Texas-migrant ancestor who bridged to Edward Mattingly Sr."
        )
        print(f"  Applied: p045 enriched with KY-TX gap context")
        count += 1

# Add George Thomas Mattingly as POSSIBLE Texas migrant
if not any(p.get("id") == "p046" for p in entities["people"]):
    entities["people"].append({
        "id": "p046",
        "full_name": "George Thomas Mattingly",
        "given_name": "George",
        "surname": "Mattingly",
        "birth_year": 1830,
        "birth_place": "Marion County, Kentucky",
        "relation_to_shari": "POSSIBLE 4th-great-grandfather (Leonard Jr.'s grandson via Henry Martin Sr.; only sibling with no Kentucky death record — strongest Texas-migrant candidate)",
        "context": (
            "George Thomas Mattingly (b. 1830 Marion County KY). Per Agent 10 KY-TX research: "
            "the ONLY one of Leonard Jr.'s ~13 grandchildren with no documented Kentucky death record. "
            "All siblings died in KY. Strongest POSSIBLE Texas-migrant candidate. WikiTree Mattingly-695. "
            "If confirmed, he is the bridge between Leonard Jr. (1843 KY) and Edward Mattingly Sr. (TX 1934)."
        ),
        "fuzzy": True,
        "confidence": "POSSIBLE",
        "sources": ["https://www.wikitree.com/wiki/Mattingly-695"],
        "branch": "Mattingly paternal — KY→TX bridge candidate"
    })
    print(f"  Added p046 George Thomas Mattingly (POSSIBLE Texas migrant candidate)")
    count += 1

# Note: Agent 10 confirmed Leonard III (Nov 15 1828 - Sep 5 1914 Glen Dean KY) is NOT the centenarian
# — he died at 85 in Kentucky. So the "1828-1935 lived to 107" centenarian remains UNVERIFIED.
# Update p030 with this exclusion
for p in entities["people"]:
    if p.get("id") == "p030":
        p["context"] = (p.get("context") or "") + (
            " — Agent 10 ruled out the strongest birth-year-matching candidate: Leonard Mattingly III "
            "(b. Nov 15 1828) died Sep 5 1914 in Glen Dean, Breckinridge County, KY at age 85, NOT 107 in Texas. "
            "The centenarian (1828-1935, age 107) remains UNVERIFIED. Briscoe Center microfilm of Texas "
            "newspapers 1935 is the recommended next step."
        )
        print(f"  Applied: p030 centenarian exclusion note")
        count += 1

ENT.write_text(json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nTotal updates applied: {count}")
print(f"Total entities now: people={len(entities['people'])}, historical={len(entities.get('historical_references', []))}")
