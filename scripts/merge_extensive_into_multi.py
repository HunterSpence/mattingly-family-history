"""Merge the extensive subtrees from cousin GEDCOMs into lineage-tree-multi.json
so the D3 visual tree on each surname page shows the wider extended family."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
MULTI_FILE = ROOT / "research" / "lineage-tree-multi.json"
EXT_FILE = ROOT / "research" / "extensive-subtrees.json"

multi = json.loads(MULTI_FILE.read_text(encoding="utf-8"))
ext = json.loads(EXT_FILE.read_text(encoding="utf-8"))

# Build label -> tree mapping for new extensive trees
extensive_secondaries = [
    {"label": "BYRD COUSIN TREE — Richard Byrd of Westmoreland VA (1717-1808) full descent (cousin GEDCOM source)",
     "tree": ext.get("byrd_richard_1717")} if ext.get("byrd_richard_1717") else None,
    {"label": "BYRD COUSIN TREE — Pvt William Leander Byrd (1832-1889 AL) full descent",
     "tree": ext.get("byrd_william_leander")} if ext.get("byrd_william_leander") else None,
    {"label": "HENSLEE COUSIN TREE — Maxfield Henslee (1727-1801) full descent",
     "tree": ext.get("henslee_maxfield_1727")} if ext.get("henslee_maxfield_1727") else None,
    {"label": "HENSLEE COUSIN TREE — James Ernest 'Pappy' Henslee (1885-1948) descent",
     "tree": ext.get("henslee_pappy")} if ext.get("henslee_pappy") else None,
    {"label": "STUART COUSIN TREE — Lewis Lunsford Stuart full descent",
     "tree": ext.get("stuart_lewis")} if ext.get("stuart_lewis") else None,
    {"label": "MATTINGLY COUSIN TREE — Thomas Jefferson Mattingly (1828 KY-1883 MO) descent",
     "tree": ext.get("mattingly_thomas_jefferson")} if ext.get("mattingly_thomas_jefferson") else None,
    {"label": "BAITY COUSIN TREE — Isham 'Isom' Baity (1804-1892 Yadkin NC) full descent",
     "tree": ext.get("baity_isham")} if ext.get("baity_isham") else None,
    {"label": "TEICHMUELLER COUSIN TREE — Hans Teichmueller (1837 Brunswick - 1901 La Grange TX) descent",
     "tree": ext.get("teichmueller_hans")} if ext.get("teichmueller_hans") else None,
]
extensive_secondaries = [s for s in extensive_secondaries if s]

# Append to existing secondary_trees
existing = multi.get("secondary_trees", [])
multi["secondary_trees"] = existing + extensive_secondaries

MULTI_FILE.write_text(json.dumps(multi, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Merged {len(extensive_secondaries)} extensive subtrees into lineage-tree-multi.json")
print(f"Total secondary_trees now: {len(multi['secondary_trees'])}")
