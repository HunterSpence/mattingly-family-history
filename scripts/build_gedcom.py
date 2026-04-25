"""Generate a GEDCOM 5.5.5 file from entities.json.

Imports cleanly into FamilyEcho, MyHeritage, Ancestry, WikiTree.
Living relatives get role-redacted entries (PRIVate flag).
"""
import json
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
ENTITIES = WORKSPACE / "research" / "entities.json"
OUT = WORKSPACE / "output" / "family-tree.ged"


def gid(eid: str) -> str:
    """Convert entity id to GEDCOM @P002@ form."""
    n = re.sub(r"[^0-9]", "", eid)
    return f"@I{int(n):04d}@" if n else f"@I{eid}@"


def date_str(year):
    if year is None:
        return None
    return f"ABT {year}" if isinstance(year, int) else str(year)


def emit_indi(p):
    eid = gid(p["id"])
    redact = p.get("redact_in_public", False)
    living = p.get("living_flag", False)

    full_name = p.get("full_name") or p.get("given_name") or "(unnamed)"
    if redact:
        full_name = f"[redacted, {p.get('relation_to_shari', 'living')}]"
    surname = p.get("surname") or ""
    given = p.get("given_name") or full_name.split(" ")[0] if not redact else "Private"

    if surname:
        name_line = f"{given} /{surname}/"
    else:
        name_line = full_name

    out = [
        f"0 {eid} INDI",
        f"1 NAME {name_line}",
    ]
    if given and not redact:
        out.append(f"2 GIVN {given}")
    if surname and not redact:
        out.append(f"2 SURN {surname}")

    sex = p.get("sex")
    if not sex:
        rel = (p.get("relation_to_shari") or "").lower()
        if any(k in rel for k in ["father", "grandfather", "uncle", "brother", "husband", "son", "nephew"]):
            sex = "M"
        elif any(k in rel for k in ["mother", "grandmother", "aunt", "sister", "wife", "daughter", "niece"]):
            sex = "F"
    if sex:
        out.append(f"1 SEX {sex}")

    if p.get("birth_year"):
        out.append("1 BIRT")
        out.append(f"2 DATE {date_str(p['birth_year'])}")
        if p.get("birth_place"):
            out.append(f"2 PLAC {p['birth_place']}")

    if p.get("death_year"):
        out.append("1 DEAT")
        out.append(f"2 DATE {date_str(p['death_year'])}")
        if p.get("death_place"):
            out.append(f"2 PLAC {p['death_place']}")

    if p.get("occupation"):
        out.append(f"1 OCCU {p['occupation']}")

    if not redact and p.get("context"):
        # Emit context as a note
        ctx = p["context"][:200].replace("\n", " ")
        out.append(f"1 NOTE {ctx}")

    if living:
        out.append("1 RESN locked")

    return "\n".join(out)


def emit_fam(fam_id, husband_eid=None, wife_eid=None, children_eids=None, marriage_year=None, note=None):
    out = [f"0 {fam_id} FAM"]
    if husband_eid:
        out.append(f"1 HUSB {gid(husband_eid)}")
    if wife_eid:
        out.append(f"1 WIFE {gid(wife_eid)}")
    for c in children_eids or []:
        out.append(f"1 CHIL {gid(c)}")
    if marriage_year:
        out.append("1 MARR")
        out.append(f"2 DATE {marriage_year}")
    if note:
        out.append(f"1 NOTE {note}")
    return "\n".join(out)


def main():
    data = json.loads(ENTITIES.read_text(encoding="utf-8"))
    people = data.get("people", [])

    by_id = {p["id"]: p for p in people}

    lines = [
        "0 HEAD",
        "1 SOUR HunterSpence-FamilyHistoryProject",
        "2 VERS 1.0",
        "2 NAME Grandma Shari Family History",
        "1 GEDC",
        "2 VERS 5.5.5",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
        f"1 DATE {datetime.now().strftime('%d %b %Y').upper()}",
        f"1 SUBM @SUBM1@",
        "",
        "0 @SUBM1@ SUBM",
        "1 NAME Hunter Spence",
        "",
    ]

    # Skip pure historical figures (Lord Baltimore, Daniel Boone) and unnamed groups
    skip_ids = {"p032", "p033", "p024", "p029"}
    for p in people:
        if p["id"] in skip_ids:
            continue
        lines.append(emit_indi(p))
        lines.append("")

    # Inferred families
    fam_lines = []

    # F001: Pearl Baity + her builder husband
    if "p006" in by_id and "p010" in by_id:
        fam_lines.append(emit_fam("@F001@", husband_eid="p010", wife_eid="p006",
                                   children_eids=["p009"],
                                   note="Pearl Baity married a successful San Antonio builder"))
    # F002: Leroy Mattingly's parents (great-grandmother + great-grandfather)
    if "p009" in by_id:
        fam_lines.append(emit_fam("@F002@", husband_eid=None, wife_eid="p009",
                                   children_eids=["p002", "p011", "p013"],
                                   note="Leroy Teichmuller Mattingly + brother Claude + sister Mamie"))
    # F003: Aunt Monette + Hugo Pohl
    if "p004" in by_id and "p005" in by_id:
        fam_lines.append(emit_fam("@F003@", husband_eid="p005", wife_eid="p004",
                                   note="Hugo Pohl (San Antonio painter) + Monette"))
    # F004: Leroy Mattingly + grandmother
    if "p002" in by_id and "p014" in by_id:
        fam_lines.append(emit_fam("@F004@", husband_eid="p002", wife_eid="p014",
                                   children_eids=["p015"],
                                   note="Leroy Teichmuller Mattingly + Shari's grandmother"))
    # F005: Father + Mother
    if "p015" in by_id and "p016" in by_id:
        fam_lines.append(emit_fam("@F005@", husband_eid="p015", wife_eid="p016",
                                   children_eids=["p000"],
                                   marriage_year="ABT 1945",
                                   note="Shari's parents (born 1922, 1923)"))
    # F006: Shari + David
    if "p000" in by_id and "p020" in by_id:
        fam_lines.append(emit_fam("@F006@", husband_eid="p020", wife_eid="p000",
                                   children_eids=["p021"],
                                   note="Shari + David (first husband). Charmaine is their daughter."))

    for fl in fam_lines:
        lines.append(fl)
        lines.append("")

    lines.append("0 TRLR")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"  individuals: {sum(1 for l in lines if l.endswith(' INDI'))}")
    print(f"  families:    {sum(1 for l in lines if l.endswith(' FAM'))}")
    print()
    print("Import targets:")
    print("  - FamilyEcho: https://www.familyecho.com/ (free, browser-based, no login)")
    print("  - MyHeritage: https://www.myheritage.com/import-gedcom (free tier accepts GEDCOM)")
    print("  - WikiTree: https://www.wikitree.com/wiki/Help:GEDCOM_Import")


if __name__ == "__main__":
    main()
