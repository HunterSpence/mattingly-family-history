"""Build EXTENSIVE family trees from the parsed GEDCOM merge — including ALL siblings,
spouses, cousins, descendants — for each surname spine. Output:
research/lineage-tree-multi-extensive.json (consumed by build_pages.py).

Strategy:
1. Load 55-gedcom-merge.json (8,756 unique persons)
2. Build a graph: name -> {parents, spouses, children}
3. For each surname spine starting at an anchor ancestor (e.g., Maxfield Henslee 1727),
   recursively expand DOWN to current generation, including every descendant found
   in any cousin GEDCOM, plus their spouses and (where the spouse is named) the
   marriage relationship displayed inline.
4. Cap descent depth so the tree doesn't explode (cousin-trees usually go 6-8 gens deep).
"""
import json
import sys
import unicodedata
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
MERGE = json.loads((ROOT / "research" / "55-gedcom-merge.json").read_text(encoding="utf-8"))


def norm(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^\w\s]", "", s).lower().strip()


# Build name index — multiple entries may map to same person across files
people_by_name = {}
for p in MERGE["all_unique_persons"]:
    key = (norm(p.get("full_name", "")), p.get("birth_year") or 0)
    if key in people_by_name:
        # merge children/spouses/parents
        existing = people_by_name[key]
        existing["child_names"] = sorted(set(existing.get("child_names", []) + p.get("child_names", [])))
        existing["spouse_names"] = sorted(set(existing.get("spouse_names", []) + p.get("spouse_names", [])))
        existing["parent_names"] = sorted(set(existing.get("parent_names", []) + p.get("parent_names", [])))
    else:
        people_by_name[key] = dict(p)

# Also build simpler name-only index for fuzzy lookup
name_only_index = defaultdict(list)
for k, p in people_by_name.items():
    name_only_index[k[0]].append(p)

# Build REVERSE-parent index: norm(parent_name) -> [children]
# This finds children even when parent's child_names list is incomplete
children_by_parent = defaultdict(list)
for p in people_by_name.values():
    for parent_name in p.get("parent_names", []):
        children_by_parent[norm(parent_name)].append(p)


def find_person(name_with_dates, fuzzy=True):
    """Find a person by name; supports 'Name (1900-1980)' or 'Name b. 1900' or just 'Name'."""
    # Strip date hints
    n = re.sub(r"\([^)]*\)", "", name_with_dates)
    n = re.sub(r"\s*b\.\s*\d{4}.*", "", n)
    n = re.sub(r"\s*[\d\?]+[\s\-–]+[\d\?]+", "", n)
    nk = norm(n)
    matches = name_only_index.get(nk, [])
    if matches:
        return matches[0]
    if fuzzy:
        for k, lst in name_only_index.items():
            if nk and (nk in k or k in nk):
                return lst[0]
    return None


def make_node(p, generation=10, century=20, marker_id=None):
    """Convert a merged-person record to a tree-node dict."""
    name = p.get("full_name", "?")
    by = p.get("birth_year")
    dy = p.get("death_year")
    bp = p.get("birth_place", "") or ""
    dp = p.get("death_place", "") or ""
    if by and dy:
        dates = f"{by}–{dy}"
    elif by:
        dates = f"b. {by}"
    elif dy:
        dates = f"d. {dy}"
    else:
        dates = ""
    if bp:
        dates = f"{dates} {bp[:30]}".strip()
    spouse = ", ".join(p.get("spouse_names", [])[:2]) if p.get("spouse_names") else None
    return {
        "name": name,
        "dates": dates,
        "fact": "",
        "id": marker_id,
        "generation": generation,
        "century": century,
        "confidence": "probable",
        "spouse": spouse,
        "children": [],
    }


def expand_descendants(person, generation, century, max_depth=7, _visited=None):
    """Recursively build a full descendant tree from a person.

    Returns a tree-node dict with all GEDCOM-known descendants + their spouses inline.
    """
    if _visited is None:
        _visited = set()
    key = (norm(person.get("full_name", "")), person.get("birth_year") or 0)
    if key in _visited or max_depth <= 0:
        return make_node(person, generation, century)
    _visited.add(key)

    node = make_node(person, generation, century)
    seen_children = set()
    child_nodes = []
    # Source 1: the person's recorded child_names list
    for child_name in person.get("child_names", []):
        if not child_name or not child_name.strip():
            continue
        ck = norm(child_name)
        if ck in seen_children:
            continue
        seen_children.add(ck)
        candidates = name_only_index.get(ck, [])
        if candidates:
            child_p = candidates[0]
            child_node = expand_descendants(
                child_p, generation + 1, century, max_depth - 1, _visited
            )
            child_nodes.append(child_node)
        else:
            child_nodes.append({
                "name": child_name.strip(),
                "dates": "",
                "fact": "",
                "id": None,
                "generation": generation + 1,
                "century": century,
                "confidence": "possible",
                "spouse": None,
                "children": [],
            })
    # Source 2: REVERSE LOOKUP — anyone whose parent_names includes this person
    # (catches children scattered across multiple cousin GEDCOMs)
    person_norm = norm(person.get("full_name", ""))
    for variant_key in [person_norm,
                        norm(re.sub(r"\b(pvt|sgt|capt|rev|dr|mr|mrs)\b", "", person.get("full_name", "").lower())),
                        norm(re.sub(r"\([^)]*\)", "", person.get("full_name", "")))]:
        for child_p in children_by_parent.get(variant_key, []):
            ck = norm(child_p.get("full_name", ""))
            if ck in seen_children or not ck:
                continue
            seen_children.add(ck)
            child_node = expand_descendants(
                child_p, generation + 1, century, max_depth - 1, _visited
            )
            child_nodes.append(child_node)
    node["children"] = child_nodes
    return node


# ── Build extensive subtrees per surname ──
# For each, find the deepest known ancestor in our spine, then expand down.

SPINES = [
    # (label, ancestor_lookup, fallback_full_name, base_gen, century)
    ("byrd_oldest", "John Henry Bird (Byrd)", "John Henry Bird", 8, 18),
    ("byrd_richard_1717", "Richard Byrd", "Richard Byrd", 8, 18),
    ("byrd_william_leander", "William Leander Byrd", "Pvt William Leander Byrd", 14, 19),
    ("byrd_john_archie", "John Archie Asner Byrd", "John Archie Asner Byrd", 15, 19),
    ("henslee_maxfield_1727", "Maxfield Henslee", "Maxfield Henslee", 8, 18),
    ("henslee_pappy", "James Ernest Henslee", "James Ernest (Pappy) Henslee", 14, 20),
    ("rau_frank", "Frank H. Rau", "Frank H. Rau", 14, 20),
    ("stuart_lewis", "Lewis Lunsford Stuart", "Lewis Stuart", 13, 19),
    ("mattingly_thomas_jefferson", "Thomas Jefferson Mattingly", "Thomas Jefferson Mattingly", 12, 19),
    ("mattingly_edward_sr", "Edward D Mattingly", "Edward Mattingly", 13, 20),
    ("baity_george_1774", "George Baity", "George Baity", 8, 18),
    ("baity_isham", "Isome Isham Baity", "Isham Baity", 10, 19),
    ("teichmueller_hans", "Hans Teichmueller", "Hans Teichmueller", 13, 19),
    ("lepick_frank", "Frank Lepik", "Frank Lepik", 13, 19),
    ("boehme_herman", "Herman F. Boehme", "Herman Boehme", 13, 19),
]

extensive = {}
for label, lookup, fallback, base_gen, base_cent in SPINES:
    p = find_person(lookup)
    if not p:
        p = find_person(fallback)
    if p:
        tree = expand_descendants(p, base_gen, base_cent, max_depth=8)
        extensive[label] = tree
        # Count nodes
        def count_nodes(t):
            return 1 + sum(count_nodes(c) for c in t.get("children", []))
        print(f"{label}: {p.get('full_name')} -> {count_nodes(tree)} descendants")
    else:
        print(f"{label}: NO MATCH for '{lookup}'")


OUT = ROOT / "research" / "extensive-subtrees.json"
OUT.write_text(json.dumps(extensive, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nWrote {OUT}")
print(f"Total subtrees built: {len(extensive)}")
