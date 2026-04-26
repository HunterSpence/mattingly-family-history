"""Parse all Ancestry GEDCOM files Hunter dropped, cross-reference against entities.json,
output a unified merge candidate list at research/55-gedcom-merge.json.

GEDCOM format primer (5.5.5):
  0 @I123@ INDI            ← person record start, xref id @I123@
  1 NAME John /Smith/      ← name; surname between slashes
  1 SEX M / F
  1 BIRT
  2 DATE 1 JAN 1900
  2 PLAC Beaumont, Texas, USA
  1 DEAT
  2 DATE 1 JAN 1980
  2 PLAC Houston, Texas
  1 FAMC @F45@             ← family this person is a child in
  1 FAMS @F46@             ← family this person is a spouse/parent in
  0 @F45@ FAM              ← family record
  1 HUSB @I100@
  1 WIFE @I101@
  1 CHIL @I123@
  1 CHIL @I124@
  1 MARR
  2 DATE 1 JAN 1898
  2 PLAC ...
"""
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

GED_DIR = Path(r"C:\Users\hspen\OneDrive\Desktop\Ancestry Gedcoms")
OUT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history\research\55-gedcom-merge.json")
ENT = Path(r"C:\Users\hspen\.openclaw\workspace\family-history\research\entities.json")


def parse_gedcom_file(path):
    """Return (persons_dict, families_dict, header_meta).

    persons_dict: {xref_id: {given, surname, full_name, sex, birth_year, birth_date, birth_place,
                              death_year, death_date, death_place, famc, fams[]}}
    families_dict: {xref_id: {husb, wife, children[], marr_year, marr_place}}
    """
    persons = {}
    families = {}
    cur = None  # current record (person or family) being filled
    cur_kind = None  # 'INDI' or 'FAM'
    cur_event = None  # 'BIRT' / 'DEAT' / 'MARR' to attach DATE/PLAC

    text = path.read_text(encoding="utf-8", errors="replace")
    for raw in text.splitlines():
        line = raw.rstrip("\r\n")
        if not line:
            continue
        # Parse "level [xref] tag [value]"
        m = re.match(r"^(\d+)\s+(@[^@]+@)?\s*(\S+)\s*(.*)$", line)
        if not m:
            continue
        level, xref, tag, value = m.group(1), m.group(2), m.group(3), m.group(4)
        level = int(level)
        if level == 0:
            cur_event = None
            if tag == "INDI":
                cur = {"xref": xref, "given": "", "surname": "", "full_name": "", "sex": "",
                       "birth_year": None, "birth_date": "", "birth_place": "",
                       "death_year": None, "death_date": "", "death_place": "",
                       "famc": None, "fams": []}
                persons[xref] = cur
                cur_kind = "INDI"
            elif tag == "FAM":
                cur = {"xref": xref, "husb": None, "wife": None, "children": [],
                       "marr_year": None, "marr_date": "", "marr_place": ""}
                families[xref] = cur
                cur_kind = "FAM"
            else:
                cur = None
                cur_kind = None
            continue
        if cur is None:
            continue
        if cur_kind == "INDI":
            if level == 1:
                cur_event = None
                if tag == "NAME":
                    cur["full_name"] = value.replace("/", "").strip()
                    sm = re.match(r"^(.*?)/(.+?)/", value)
                    if sm:
                        cur["given"] = sm.group(1).strip()
                        cur["surname"] = sm.group(2).strip()
                elif tag == "SEX":
                    cur["sex"] = value.strip()
                elif tag == "BIRT":
                    cur_event = "BIRT"
                elif tag == "DEAT":
                    cur_event = "DEAT"
                elif tag == "FAMC":
                    cur["famc"] = value.strip()
                elif tag == "FAMS":
                    cur["fams"].append(value.strip())
            elif level == 2:
                if cur_event == "BIRT":
                    if tag == "DATE":
                        cur["birth_date"] = value.strip()
                        ym = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", value)
                        if ym:
                            cur["birth_year"] = int(ym.group(1))
                    elif tag == "PLAC":
                        cur["birth_place"] = value.strip()
                elif cur_event == "DEAT":
                    if tag == "DATE":
                        cur["death_date"] = value.strip()
                        ym = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", value)
                        if ym:
                            cur["death_year"] = int(ym.group(1))
                    elif tag == "PLAC":
                        cur["death_place"] = value.strip()
        elif cur_kind == "FAM":
            if level == 1:
                cur_event = None
                if tag == "HUSB":
                    cur["husb"] = value.strip()
                elif tag == "WIFE":
                    cur["wife"] = value.strip()
                elif tag == "CHIL":
                    cur["children"].append(value.strip())
                elif tag == "MARR":
                    cur_event = "MARR"
            elif level == 2 and cur_event == "MARR":
                if tag == "DATE":
                    cur["marr_date"] = value.strip()
                    ym = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", value)
                    if ym:
                        cur["marr_year"] = int(ym.group(1))
                elif tag == "PLAC":
                    cur["marr_place"] = value.strip()
    return persons, families


def normalize_name(name):
    """For dedupe: strip accents, lowercase, collapse whitespace, remove punctuation."""
    if not name:
        return ""
    nfkd = unicodedata.normalize("NFKD", name)
    only_ascii = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^\w\s]", "", only_ascii).lower()
    return re.sub(r"\s+", " ", cleaned).strip()


def person_key(p):
    """Dedupe key: normalized full name + birth year (if known) + surname."""
    name = normalize_name(p.get("full_name") or f"{p.get('given','')} {p.get('surname','')}")
    by = p.get("birth_year") or 0
    return (name, by)


def main():
    files = sorted(GED_DIR.glob("*.ged"))
    print(f"Found {len(files)} GEDCOM files")

    # cousin label = filename stem (descriptive)
    all_persons = {}  # key -> aggregated person record across files
    file_meta = []
    for fp in files:
        persons, families = parse_gedcom_file(fp)
        cousin_label = fp.stem
        file_meta.append({"file": fp.name, "cousin": cousin_label,
                          "n_persons": len(persons), "n_families": len(families)})
        # Build parent lookup using families
        child_of_fam = {}  # fam_xref -> (husb_xref, wife_xref)
        for fxref, f in families.items():
            child_of_fam[fxref] = (f.get("husb"), f.get("wife"))

        for xref, p in persons.items():
            k = person_key(p)
            if not p.get("full_name"):
                continue
            agg = all_persons.setdefault(k, {
                "full_name": p["full_name"],
                "given": p["given"],
                "surname": p["surname"],
                "sex": p.get("sex", ""),
                "birth_year": p.get("birth_year"),
                "birth_place": p.get("birth_place", ""),
                "death_year": p.get("death_year"),
                "death_place": p.get("death_place", ""),
                "appears_in": [],
                "parent_names": set(),
                "spouse_names": set(),
                "child_names": set(),
            })
            agg["appears_in"].append(cousin_label)
            # Merge missing fields (overwrite if existing is empty)
            for fld in ("sex", "birth_year", "birth_place", "death_year", "death_place"):
                if not agg.get(fld) and p.get(fld):
                    agg[fld] = p[fld]
            # UNION parents/spouses/children across all file occurrences (NEVER overwrite)
            if p.get("famc") and p["famc"] in families:
                hxref, wxref = child_of_fam.get(p["famc"], (None, None))
                if hxref and hxref in persons:
                    agg["parent_names"].add(persons[hxref]["full_name"])
                if wxref and wxref in persons:
                    agg["parent_names"].add(persons[wxref]["full_name"])
            for fxref in p.get("fams", []):
                if fxref in families:
                    fam = families[fxref]
                    if fam.get("husb") == xref and fam.get("wife") in persons:
                        agg["spouse_names"].add(persons[fam["wife"]]["full_name"])
                    elif fam.get("wife") == xref and fam.get("husb") in persons:
                        agg["spouse_names"].add(persons[fam["husb"]]["full_name"])
                    for cxref in fam.get("children", []):
                        if cxref in persons:
                            agg["child_names"].add(persons[cxref]["full_name"])

    # Convert sets to lists for JSON
    for agg in all_persons.values():
        agg["parent_names"] = sorted(agg["parent_names"])
        agg["spouse_names"] = sorted(agg["spouse_names"])
        agg["child_names"] = sorted(agg["child_names"])
        agg["n_files_appears_in"] = len(set(agg["appears_in"]))

    # Cross-reference against existing entities.json
    existing = json.loads(ENT.read_text(encoding="utf-8"))
    existing_keys = {}
    for e in existing.get("people", []):
        nm = normalize_name(e.get("full_name", ""))
        by = e.get("birth_year") or 0
        existing_keys[(nm, by)] = e

    matched_existing = 0
    new_candidates = []
    for k, agg in all_persons.items():
        if k in existing_keys:
            agg["matches_existing_id"] = existing_keys[k].get("id")
            matched_existing += 1
        else:
            new_candidates.append(agg)

    # Sort new candidates by frequency-of-appearance (descending) — high-confidence first
    new_candidates.sort(key=lambda x: (-x["n_files_appears_in"], -(x.get("birth_year") or 0)))

    # Surnames by frequency — for Hunter's "main last names" focus
    surname_count = defaultdict(int)
    for agg in all_persons.values():
        if agg.get("surname"):
            surname_count[agg["surname"]] += 1
    top_surnames = sorted(surname_count.items(), key=lambda x: -x[1])[:30]

    out = {
        "summary": {
            "total_files": len(files),
            "total_unique_persons": len(all_persons),
            "matched_existing_entities": matched_existing,
            "new_candidates": len(new_candidates),
            "top_30_surnames_by_count": [{"surname": s, "count": c} for s, c in top_surnames],
        },
        "files": file_meta,
        "new_candidates": new_candidates[:500],  # cap at top 500 for sanity
        "all_unique_persons": list(all_persons.values()),
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Total unique persons across {len(files)} files: {len(all_persons)}")
    print(f"  Already in entities.json: {matched_existing}")
    print(f"  New candidates: {len(new_candidates)}")
    print(f"\nTop 15 surnames by frequency:")
    for s, c in top_surnames[:15]:
        print(f"  {s}: {c}")


if __name__ == "__main__":
    main()
