"""Pull high-value targets from the parsed GEDCOM merge:
1. People with our key surnames (Spence, Henslee, Mattingly, Lepick/Lepik, Boehme, Teichmuller, Baity, Mikeska, Macker)
2. The specific unknowns we want to fill (Dale Sr's father, Dovie maiden, Frances Henslee maiden, etc.)
3. Notable historical figures (presidents, generals, etc. by name)
"""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history\research")
MERGE = json.loads((ROOT / "55-gedcom-merge.json").read_text(encoding="utf-8"))
persons = MERGE["all_unique_persons"]

KEY_SURNAMES = {
    "spence", "henslee", "henslee", "mattingly", "lepick", "lepik", "boehme", "böhme",
    "teichmueller", "teichmüller", "baity", "beatty", "beatie", "mikeska", "macker",
    "trifon", "schroeder", "luedecke", "matava", "patton", "clarke", "bradford"
}

NOTABLE_NAMES = [
    # US Presidents
    "Washington", "Adams", "Jefferson", "Madison", "Monroe", "Jackson",
    "Van Buren", "Harrison", "Tyler", "Polk", "Taylor", "Fillmore",
    "Pierce", "Buchanan", "Lincoln", "Johnson", "Grant", "Hayes",
    "Garfield", "Arthur", "Cleveland", "McKinley", "Roosevelt",
    "Taft", "Wilson", "Harding", "Coolidge", "Hoover", "Truman",
    "Eisenhower", "Kennedy", "Nixon", "Ford", "Carter", "Reagan",
    # Famous Mattinglys
    "Don Mattingly", "Mack Mattingly", "Garrett Mattingly", "Ken Mattingly",
    "Marie Mattingly Meloney", "Ignatius Mattingly", "Ben Mattingly",
    # Famous Spences
    "Sir Basil Spence", "Lewis Spence", "Catherine Spence",
    # Famous Teichmüllers
    "Gustav Teichmüller", "Anna Teichmüller", "Robert Teichmüller", "Minette Teichmueller",
    # Notable colonial Americans
    "Daniel Boone", "Davy Crockett", "Sam Houston", "Stephen Austin",
    # Famous Boehmes
    "Jakob Boehme",
]


# 1. PEOPLE WITH KEY SURNAMES
key_surname_hits = []
for p in persons:
    sn = (p.get("surname") or "").lower().strip()
    if sn in KEY_SURNAMES:
        key_surname_hits.append(p)

# Deduplicate by full_name + birth_year
seen = set()
key_unique = []
for p in key_surname_hits:
    k = (p.get("full_name", "").lower(), p.get("birth_year") or 0)
    if k not in seen:
        seen.add(k)
        key_unique.append(p)

# Sort by surname then birth year
key_unique.sort(key=lambda x: (x.get("surname", ""), x.get("birth_year") or 0))


# 2. SPECIFIC UNKNOWNS WE WANT TO FILL
# Dale William Spence Sr's father (Hunter's English-immigrant great-grandfather)
# We know Dovie was his mother. Search for any Spence whose spouse is Dovie.
dale_father_candidates = []
for p in persons:
    if (p.get("surname") or "").lower() == "spence":
        spouses = [s.lower() for s in p.get("spouse_names", [])]
        children = [c.lower() for c in p.get("child_names", [])]
        # Looking for Spence male whose wife was Dovie OR who has child named "Dale"
        if any("dovie" in s for s in spouses) or any("dale" in c and "spence" in c for c in children):
            dale_father_candidates.append(p)

# Frances Henslee's maiden name + parents
frances_parents = []
for p in persons:
    if (p.get("given") or "").lower().startswith("frances"):
        children = [c.lower() for c in p.get("child_names", [])]
        if any("henslee" in c or "spence" in c for c in children):
            frances_parents.append(p)

# Lee Stuart Henslee's parents
lee_stuart_parents = []
for p in persons:
    children = [c.lower() for c in p.get("child_names", [])]
    if any("lee stuart henslee" in c or "lee s henslee" in c or "leestuart" in c for c in children):
        lee_stuart_parents.append(p)

# Dovie Spence's parents (maiden name unknown)
dovie_parents = []
for p in persons:
    children = [c.lower() for c in p.get("child_names", [])]
    if any("dovie" in c for c in children):
        dovie_parents.append(p)


# 3. NOTABLE HISTORICAL FIGURES BY NAME MATCH
notable_hits = []
for p in persons:
    full = p.get("full_name", "")
    for notable in NOTABLE_NAMES:
        if notable.lower() in full.lower():
            notable_hits.append({"matched": notable, "person": p})
            break


# 4. PEOPLE APPEARING IN 3+ COUSIN TREES (high cross-confirmation)
multi_tree = [p for p in persons if p.get("n_files_appears_in", 0) >= 3]
multi_tree.sort(key=lambda x: (-x.get("n_files_appears_in", 0), -(x.get("birth_year") or 0)))


report = {
    "key_surname_hits": {
        "total": len(key_unique),
        "by_surname": {},
        "people": key_unique[:200],
    },
    "specific_unknowns": {
        "dale_sr_father_candidates": dale_father_candidates,
        "frances_henslee_parents_candidates": frances_parents,
        "lee_stuart_henslee_parents_candidates": lee_stuart_parents,
        "dovie_spence_parents_candidates": dovie_parents,
    },
    "notable_historical_hits": notable_hits[:50],
    "high_confidence_multi_tree": [{
        "name": p["full_name"],
        "surname": p.get("surname"),
        "birth_year": p.get("birth_year"),
        "death_year": p.get("death_year"),
        "n_trees": p.get("n_files_appears_in"),
        "appears_in": list(set(p.get("appears_in", []))),
        "parent_names": p.get("parent_names", []),
        "spouse_names": p.get("spouse_names", []),
        "child_names": p.get("child_names", []),
    } for p in multi_tree[:100]],
}

# Group key surname hits by surname
from collections import defaultdict
grp = defaultdict(list)
for p in key_unique:
    grp[p.get("surname", "?")].append({
        "name": p["full_name"],
        "birth_year": p.get("birth_year"),
        "death_year": p.get("death_year"),
        "birth_place": p.get("birth_place"),
        "death_place": p.get("death_place"),
        "n_trees": p.get("n_files_appears_in"),
        "appears_in": p.get("appears_in", []),
        "parents": p.get("parent_names", []),
        "spouses": p.get("spouse_names", []),
        "children": p.get("child_names", []),
    })
report["key_surname_hits"]["by_surname"] = {sn: lst for sn, lst in sorted(grp.items())}

OUT = ROOT / "55-gedcom-targets.json"
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"\nKey surname hits ({len(key_unique)}):")
for sn, lst in sorted(grp.items()):
    print(f"  {sn}: {len(lst)}")
print(f"\nSpecific unknowns:")
print(f"  Dale Sr father candidates: {len(dale_father_candidates)}")
print(f"  Frances Henslee parents candidates: {len(frances_parents)}")
print(f"  Lee Stuart Henslee parents candidates: {len(lee_stuart_parents)}")
print(f"  Dovie Spence parents candidates: {len(dovie_parents)}")
print(f"\nNotable historical name hits: {len(notable_hits)}")
print(f"\nHigh-confidence multi-tree (3+): {len(multi_tree)}")
