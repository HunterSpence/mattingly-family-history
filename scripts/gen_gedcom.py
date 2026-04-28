import json, re

data = json.load(open('C:/Users/hspen/.openclaw/workspace/family-history/research/lineage-tree-multi.json', encoding='utf-8'))

FEMALE_NAMES = {
    'alice','ann','anne','mary','jane','grace','dinah','hannah','frances',
    'isabella','elizabeth','margaret','sarah','catherine','emily','helen',
    'edith','martha','ruth','dorothy','virginia','patricia','betty',
    'jeanne','minna','carol','linda','donna','judith','teresa','eleanor',
    'mabel','ida','lena','rosa','anna','clara','emma','flora','harriet',
    'josephine','laura','louisa','lydia','maud','nora','phoebe','phebe',
    'priscilla','rachel','rebecca','sophia','susannah','winifred','hester',
    'honor','bridget','constance','lettice','lucy','matilda','cecily',
    'agatha','adeliza','sybil','rohaise','egidia','scholastica',
    "d'anne",'shari','dovie','jean','marie','phyllis','maxine','lois',
    'alice marie','rosa','minnie','ida','bertha','gertrude','wilhelmina',
    'friederike','friedrike','helene','mary alice','alice','leona','alma',
    'lucille','thelma','vera','irene','pearl','opal','ruby','myrtle',
    'daisy','violet','hazel','ethel','gladys','blanche','nell','nellie',
    'minnie','belle','ora','ola','etta','lula','cora','nora','dora',
    'zora','rena','lena','vena','alena','elena','magdalena'
}

def infer_sex(name, spouse_str):
    first = name.split()[0].lower().rstrip('.')
    if first in FEMALE_NAMES:
        return 'F'
    if spouse_str:
        sl = spouse_str.lower()
        if 'wife of' in sl or 'his wife' in sl:
            return 'M'
        if 'husband of' in sl:
            return 'F'
    return 'M'

def extract_year(text):
    """Return earliest 4-digit year found in text, or None."""
    if not text:
        return None
    text = text.replace('–','-').replace('—','-')
    # fl. YYYY or c.YYYY or ~YYYY or YYYY
    m = re.search(r'\b(\d{4})\b', text)
    return int(m.group(1)) if m else None

def should_include(node):
    """Include only if we can't find a year < 1500, or no year at all."""
    if node.get('confidence') == 'debunked':
        return False
    dates = node.get('dates', '') or ''
    yr = extract_year(dates)
    if yr is not None and yr < 1500:
        return False
    return True

def parse_date_str(text):
    """Return (gedcom_date_str, death_year_str_or_None)."""
    if not text:
        return None, None
    text = text.replace('–','-').replace('—','-').replace('~','').strip()
    m = re.search(r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{4})', text, re.I)
    if m:
        return f"{m.group(1)} {m.group(2).upper()[:3]} {m.group(3)}", None
    m = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{4})', text, re.I)
    if m:
        return f"{m.group(1).upper()[:3]} {m.group(2)}", None
    m = re.search(r'(?:abt\.?|about|circa|c\.)\s*(\d{4})', text, re.I)
    if m:
        return f"ABT {m.group(1)}", None
    m = re.search(r'\bborn\s+(\d{4})\b', text, re.I)
    if m:
        return m.group(1), None
    m = re.search(r'\bb\.\s*(\d{4})\b', text, re.I)
    if m:
        return m.group(1), None
    m = re.search(r'\b(\d{4})\s*[-–]\s*(\d{4})\b', text)
    if m:
        return m.group(1), m.group(2)
    m = re.search(r'\b(\d{4})\b', text)
    if m:
        return m.group(1), None
    return None, None

def parse_place(text):
    if not text:
        return None
    m = re.search(r'(?:born|b\.)\s+(?:(?:abt\.?\s+)?(?:\d{1,2}\s+\w+\s+)?\d{4}),?\s+(.+?)(?:\s*[-—]|$)', text, re.I)
    if m:
        p = m.group(1).strip().rstrip('.,')
        if 0 < len(p) < 120:
            return p
    m = re.search(r'\d{4},\s+(.+?)(?:\s*[-—(]|$)', text)
    if m:
        p = m.group(1).strip().rstrip('.,')
        if p and len(p) < 120:
            return p
    return None

def parse_death(text):
    if not text:
        return None, None
    m = re.search(r'(?:d\.|died|death)\s+(?:(\d{1,2})\s+(\w+)\s+)?(\d{4})(?:,\s*([^;)—]+?))?(?:\s*[-;)—]|$)', text, re.I)
    if m:
        day, mon, yr, plac = m.groups()
        date = yr
        if day and mon:
            try:
                date = f"{day} {mon[:3].upper()} {yr}"
            except Exception:
                date = yr
        return date, (plac.strip() if plac else None)
    return None, None

def parse_spouse(spouse_str):
    if not spouse_str:
        return None
    sp = {}
    m = re.match(r'^([^(;,]+?)(?:\s*\(|,\s*(?:born|b\.|n[e\xe9]{2}|\d{4}))', spouse_str)
    if m:
        sp['name'] = m.group(1).strip()
    else:
        sp['name'] = spouse_str.split(';')[0].split('(')[0].strip()
    sp['name'] = re.sub(r'\s+', ' ', sp['name']).strip()[:80]
    if not sp['name'] or len(sp['name']) < 2:
        return None
    m = re.search(r'born\s+(?:(\d{1,2})\s+(\w+)\s+)?(\d{4})(?:,\s*([^;)—-]+?))?(?:[;)—-]|$)', spouse_str, re.I)
    if m:
        day, mon, yr, plac = m.groups()
        sp['birth_date'] = yr if not day else f"{day} {mon[:3].upper()} {yr}"
        sp['birth_place'] = plac.strip().rstrip('.,') if plac else None
    if 'birth_date' not in sp:
        m = re.search(r'~(\d{4})', spouse_str)
        if m:
            sp['birth_date'] = f"ABT {m.group(1)}"
    m = re.search(r'married\s+(?:(\d{1,2})\s+(\w+)\s+)?(\d{4})(?:,\s*([^;)—]+?))?(?:[;)—]|$)', spouse_str, re.I)
    if m:
        day, mon, yr, plac = m.groups()
        sp['marr_date'] = yr if not day else f"{day} {mon[:3].upper()} {yr}"
        sp['marr_place'] = plac.strip().rstrip('.,') if plac else None
    m = re.search(r'n[e\xe9]{2}\s+(\w+)', spouse_str, re.I)
    if m:
        sp['maiden'] = m.group(1)
    return sp

def format_name(name):
    # Remove problematic chars from surname slot
    parts = name.rsplit(' ', 1)
    if len(parts) == 2:
        given, surname = parts
        # Don't put descriptors in surname slot
        if any(c in surname for c in ['(', ')', '.']) or surname.lower() in {'unknown','of','the','son','jr','sr'}:
            return f"{name} /Unknown/"
        return f"{given} /{surname}/"
    return f"{name} /Unknown/"

def gedcom_line(level, tag, value):
    """Return list of GEDCOM lines, wrapping at 248 chars."""
    if value is None:
        return []
    # Sanitize: remove chars that break GEDCOM parsers
    value = str(value).replace('\r', ' ').replace('\n', ' ')
    # Replace unicode dash variants
    value = value.replace('–', '-').replace('—', '-').replace('’', "'")
    first_line = f"{level} {tag} {value}"
    if len(first_line) <= 248:
        return [first_line]
    # Split into CONT/CONC chunks
    lines = []
    max_first = 248
    lines.append(first_line[:max_first])
    remainder = first_line[max_first:]
    while remainder:
        chunk = remainder[:245]
        lines.append(f"{level+1} CONC {chunk}")
        remainder = remainder[245:]
    return lines

# ── Build individuals and families ──────────────────────────────────────────
counter = [0]
id_map = {}
fam_counter = [0]
individuals = []
families = []

def get_id(node):
    k = id(node)
    if k not in id_map:
        counter[0] += 1
        id_map[k] = f"I{counter[0]:04d}"
    return id_map[k]

def new_fam():
    fam_counter[0] += 1
    return f"F{fam_counter[0]:04d}"

def process_node(node, parent_fam_id=None):
    if not should_include(node):
        # Still process children in case they're post-1500
        for child in node.get('children', []):
            process_node(child, parent_fam_id=None)
        return None

    nid = get_id(node)
    name = node.get('name', 'Unknown')
    dates = node.get('dates', '') or ''
    fact = node.get('fact', '') or ''
    spouse_str = node.get('spouse') or ''
    confidence = node.get('confidence', '?')
    gen = node.get('generation', 0)
    children = node.get('children', [])

    birt_date, deat_from_range = parse_date_str(dates)
    birt_place = parse_place(dates)
    if not birt_place and birt_date:
        birt_place = parse_place(fact[:300])

    deat_date = deat_from_range
    deat_place = None
    if not deat_date:
        deat_date, deat_place = parse_death(dates)
    if not deat_date:
        deat_date, deat_place = parse_death(fact[:400])

    sex = infer_sex(name, spouse_str)
    gedcom_name = format_name(name)

    # Short note — keep under 200 chars to stay safe
    short_fact = fact.replace('\n', ' ').strip()[:150]
    note = f"Confidence: {confidence}. Gen {gen}. {short_fact}"

    indi = {
        'id': nid, 'name': gedcom_name, 'sex': sex,
        'birt_date': birt_date, 'birt_place': birt_place,
        'deat_date': deat_date, 'deat_place': deat_place,
        'note': note, 'famc': parent_fam_id, 'fams': [],
    }
    individuals.append(indi)

    fam_id = None

    if spouse_str and spouse_str.strip() and children:
        sp = parse_spouse(spouse_str)
        if sp and sp.get('name'):
            counter[0] += 1
            sid = f"I{counter[0]:04d}"
            sp_name = sp['name']
            sp_ged = format_name(sp_name)
            if sp.get('maiden'):
                parts = sp_name.rsplit(' ', 1)
                sp_ged = f"{parts[0]} /{sp['maiden']}/"
            spouse_sex = 'F' if sex == 'M' else 'M'
            sp_note = f"Spouse of {name}. {spouse_str[:120]}"
            spouse_indi = {
                'id': sid, 'name': sp_ged, 'sex': spouse_sex,
                'birt_date': sp.get('birth_date'), 'birt_place': sp.get('birth_place'),
                'deat_date': None, 'deat_place': None,
                'note': sp_note, 'famc': None, 'fams': [],
            }
            individuals.append(spouse_indi)
            fam_id = new_fam()
            husb = nid if sex == 'M' else sid
            wife = sid if sex == 'M' else nid
            fam = {
                'id': fam_id, 'husb': husb, 'wife': wife,
                'marr_date': sp.get('marr_date'), 'marr_place': sp.get('marr_place'),
                'children': [],
            }
            families.append(fam)
            indi['fams'].append(fam_id)
            spouse_indi['fams'].append(fam_id)
        else:
            fam_id = new_fam()
            fam = {'id': fam_id, 'husb': nid if sex=='M' else None,
                   'wife': nid if sex=='F' else None,
                   'marr_date': None, 'marr_place': None, 'children': []}
            families.append(fam)
            indi['fams'].append(fam_id)
    elif children:
        fam_id = new_fam()
        fam = {'id': fam_id,
               'husb': nid if sex == 'M' else None,
               'wife': nid if sex == 'F' else None,
               'marr_date': None, 'marr_place': None, 'children': []}
        families.append(fam)
        indi['fams'].append(fam_id)

    for child in children:
        child_id = process_node(child, parent_fam_id=fam_id)
        if child_id and fam_id:
            for f in families:
                if f['id'] == fam_id:
                    f['children'].append(child_id)
                    break

    return nid

process_node(data['primary'])
for tree in data.get('secondary_trees', []):
    process_node(tree)

print(f"Individuals: {len(individuals)}, Families: {len(families)}")

# ── Write GEDCOM ─────────────────────────────────────────────────────────────
out = []
out.append("0 HEAD")
out.append("1 SOUR Clawrence Research")
out.append("2 VERS 1.0")
out.append("1 GEDC")
out.append("2 VERS 5.5.1")
out.append("2 FORM LINEAGE-LINKED")
out.append("1 CHAR UTF-8")
out.append("1 NOTE Full family history 1500+. Sources: FamilySearch, England Census, FreeBMD, AncestryDNA.")
out.append("")

for indi in individuals:
    out.append(f"0 @{indi['id']}@ INDI")
    out += gedcom_line(1, "NAME", indi['name'])
    out.append(f"1 SEX {indi['sex']}")
    if indi.get('birt_date') or indi.get('birt_place'):
        out.append("1 BIRT")
        if indi.get('birt_date'):
            out += gedcom_line(2, "DATE", indi['birt_date'])
        if indi.get('birt_place'):
            out += gedcom_line(2, "PLAC", indi['birt_place'])
    if indi.get('deat_date') or indi.get('deat_place'):
        out.append("1 DEAT")
        if indi.get('deat_date'):
            out += gedcom_line(2, "DATE", indi['deat_date'])
        if indi.get('deat_place'):
            out += gedcom_line(2, "PLAC", indi['deat_place'])
    if indi.get('famc'):
        out.append(f"1 FAMC @{indi['famc']}@")
    for fams in indi.get('fams', []):
        out.append(f"1 FAMS @{fams}@")
    if indi.get('note'):
        out += gedcom_line(1, "NOTE", indi['note'])
    out.append("")

for fam in families:
    out.append(f"0 @{fam['id']}@ FAM")
    if fam.get('husb'):
        out.append(f"1 HUSB @{fam['husb']}@")
    if fam.get('wife'):
        out.append(f"1 WIFE @{fam['wife']}@")
    if fam.get('marr_date') or fam.get('marr_place'):
        out.append("1 MARR")
        if fam.get('marr_date'):
            out += gedcom_line(2, "DATE", fam['marr_date'])
        if fam.get('marr_place'):
            out += gedcom_line(2, "PLAC", fam['marr_place'])
    for chil in fam.get('children', []):
        out.append(f"1 CHIL @{chil}@")
    out.append("")

out.append("0 TRLR")

# Verify no lines over 255
long_lines = [l for l in out if len(l) > 255]
print(f"Lines over 255 chars: {len(long_lines)}")
if long_lines:
    for l in long_lines[:3]:
        print(f"  ({len(l)}) {l[:80]}")

path = 'C:/Users/hspen/.openclaw/workspace/family-history/research/full-family-history.ged'
with open(path, 'w', encoding='utf-8') as f:
    f.write('\r\n'.join(out))  # CRLF as GEDCOM spec requires
print(f"Written: {path} ({len(out)} lines)")
