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
    'alice marie','carol','rosa','minnie','ida','bertha','gertrude',
    'wilhelmina','friederike','friedrike','helene'
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

def parse_date(text):
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
    m = re.search(r'(?:born|b\.)\s+(?:\d{1,2}\s+\w+\s+)?\d{4},?\s+(.+?)(?:\s*[-—]|$)', text, re.I)
    if m:
        place = m.group(1).strip().rstrip('.')
        if 0 < len(place) < 120:
            return place
    m = re.search(r'\d{4},\s+(.+?)(?:\s*[-—(]|$)', text)
    if m:
        place = m.group(1).strip().rstrip('.')
        if place and len(place) < 120:
            return place
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
    m = re.match(r'^([^(;,]+?)(?:\s*\(|,\s*(?:born|b\.|n[eé]{2}|née|\d{4}))', spouse_str)
    if m:
        sp['name'] = m.group(1).strip()
    else:
        sp['name'] = spouse_str.split(';')[0].split('(')[0].strip()
    sp['name'] = re.sub(r'\s+', ' ', sp['name']).strip()[:80]
    m = re.search(r'born\s+(?:(\d{1,2})\s+(\w+)\s+)?(\d{4})(?:,\s*([^;)—-]+?))?(?:[;)—-]|$)', spouse_str, re.I)
    if m:
        day, mon, yr, plac = m.groups()
        sp['birth_date'] = yr if not day else f"{day} {mon[:3].upper()} {yr}"
        sp['birth_place'] = plac.strip().rstrip('.') if plac else None
    if 'birth_date' not in sp:
        m = re.search(r'~(\d{4})', spouse_str)
        if m:
            sp['birth_date'] = f"ABT {m.group(1)}"
    m = re.search(r'married\s+(?:(\d{1,2})\s+(\w+)\s+)?(\d{4})(?:,\s*([^;)—]+?))?(?:[;)—]|$)', spouse_str, re.I)
    if m:
        day, mon, yr, plac = m.groups()
        sp['marr_date'] = yr if not day else f"{day} {mon[:3].upper()} {yr}"
        sp['marr_place'] = plac.strip().rstrip('.') if plac else None
    m = re.search(r'n[eé]{2}\s+(\w+)', spouse_str, re.I)
    if m:
        sp['maiden'] = m.group(1)
    return sp

counter = [0]
id_map = {}
fam_id_counter = [0]
individuals = []
families = []

def node_key(node):
    return id(node)

def gedcom_id(node):
    k = node_key(node)
    if k not in id_map:
        counter[0] += 1
        id_map[k] = f"I{counter[0]:04d}"
    return id_map[k]

def new_fam_id():
    fam_id_counter[0] += 1
    return f"F{fam_id_counter[0]:04d}"

def format_name(name):
    skip_words = {'of','the','son','daughter','lord','sir','de','van','von',
                  'le','la','du','des','al','ibn','bint'}
    parts = name.rsplit(' ', 1)
    if len(parts) == 2:
        given, surname = parts
        words = surname.lower().split()
        if all(w in skip_words or '(' in surname or len(words) > 2 for w in words):
            return f"{name} /Unknown/"
        return f"{given} /{surname}/"
    return f"{name} /Unknown/"

def process_node(node, parent_fam_id=None):
    if node.get('confidence') == 'debunked':
        return None

    nid = gedcom_id(node)
    name = node.get('name', 'Unknown')
    dates = node.get('dates', '') or ''
    fact = node.get('fact', '') or ''
    spouse_str = node.get('spouse') or ''
    confidence = node.get('confidence', '?')
    gen = node.get('generation', 0)
    children = node.get('children', [])

    birt_date, deat_date_from_range = parse_date(dates)
    birt_place = parse_place(dates)
    if not birt_place and birt_date:
        birt_place = parse_place(fact[:250])

    deat_date = deat_date_from_range
    deat_place = None
    if not deat_date:
        deat_date, deat_place = parse_death(dates)
    if not deat_date:
        deat_date, deat_place = parse_death(fact[:400])

    sex = infer_sex(name, spouse_str)
    gedcom_name = format_name(name)

    note_text = f"Confidence: {confidence}. Generation: {gen}. {fact[:500].strip()}"
    note_text = note_text.replace('\n', ' ')

    indi = {
        'id': nid,
        'name': gedcom_name,
        'sex': sex,
        'birt_date': birt_date,
        'birt_place': birt_place,
        'deat_date': deat_date,
        'deat_place': deat_place,
        'note': note_text,
        'famc': parent_fam_id,
        'fams': [],
    }
    individuals.append(indi)

    spouse_indi = None
    fam_id = None

    if spouse_str and spouse_str.strip() and children:
        sp = parse_spouse(spouse_str)
        if sp and sp.get('name') and len(sp['name']) > 1:
            counter[0] += 1
            spouse_id = f"I{counter[0]:04d}"
            sp_name = sp['name']
            sp_gedcom_name = format_name(sp_name)
            if sp.get('maiden'):
                sp_parts = sp_name.rsplit(' ', 1)
                sp_gedcom_name = f"{sp_parts[0]} /{sp['maiden']}/"
            spouse_sex = 'F' if sex == 'M' else 'M'
            spouse_indi = {
                'id': spouse_id,
                'name': sp_gedcom_name,
                'sex': spouse_sex,
                'birt_date': sp.get('birth_date'),
                'birt_place': sp.get('birth_place'),
                'deat_date': None,
                'deat_place': None,
                'note': f"Spouse of {name}. {spouse_str[:400]}",
                'famc': None,
                'fams': [],
            }
            individuals.append(spouse_indi)
            fam_id = new_fam_id()
            husb_id = nid if sex == 'M' else spouse_id
            wife_id = spouse_id if sex == 'M' else nid
            fam = {
                'id': fam_id,
                'husb': husb_id,
                'wife': wife_id,
                'marr_date': sp.get('marr_date'),
                'marr_place': sp.get('marr_place'),
                'children': [],
            }
            families.append(fam)
            indi['fams'].append(fam_id)
            spouse_indi['fams'].append(fam_id)
    elif children:
        fam_id = new_fam_id()
        if sex == 'M':
            fam = {'id': fam_id, 'husb': nid, 'wife': None, 'marr_date': None, 'marr_place': None, 'children': []}
        else:
            fam = {'id': fam_id, 'husb': None, 'wife': nid, 'marr_date': None, 'marr_place': None, 'children': []}
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

lines = []
lines.append("0 HEAD")
lines.append("1 SOUR Clawrence Genealogy Research")
lines.append("2 VERS 1.0")
lines.append("1 GEDC")
lines.append("2 VERS 5.5.1")
lines.append("2 FORM LINEAGE-LINKED")
lines.append("1 CHAR UTF-8")
lines.append("1 NOTE Full family history — all confirmed and probable lines. Sources: FamilySearch England Births/Christenings/Marriages 1538-1975; 1841/1851/1881 England Census; 1910 US Census; FreeBMD; AncestryDNA matches. Confidence level noted per individual.")
lines.append("")

for indi in individuals:
    lines.append(f"0 @{indi['id']}@ INDI")
    lines.append(f"1 NAME {indi['name']}")
    lines.append(f"1 SEX {indi['sex']}")
    if indi.get('birt_date') or indi.get('birt_place'):
        lines.append("1 BIRT")
        if indi.get('birt_date'):
            lines.append(f"2 DATE {indi['birt_date']}")
        if indi.get('birt_place'):
            lines.append(f"2 PLAC {indi['birt_place']}")
    if indi.get('deat_date') or indi.get('deat_place'):
        lines.append("1 DEAT")
        if indi.get('deat_date'):
            lines.append(f"2 DATE {indi['deat_date']}")
        if indi.get('deat_place'):
            lines.append(f"2 PLAC {indi['deat_place']}")
    if indi.get('famc'):
        lines.append(f"1 FAMC @{indi['famc']}@")
    for fams in indi.get('fams', []):
        lines.append(f"1 FAMS @{fams}@")
    if indi.get('note'):
        lines.append(f"1 NOTE {indi['note'][:500]}")
    lines.append("")

for fam in families:
    lines.append(f"0 @{fam['id']}@ FAM")
    if fam.get('husb'):
        lines.append(f"1 HUSB @{fam['husb']}@")
    if fam.get('wife'):
        lines.append(f"1 WIFE @{fam['wife']}@")
    if fam.get('marr_date') or fam.get('marr_place'):
        lines.append("1 MARR")
        if fam.get('marr_date'):
            lines.append(f"2 DATE {fam['marr_date']}")
        if fam.get('marr_place'):
            lines.append(f"2 PLAC {fam['marr_place']}")
    for chil in fam.get('children', []):
        lines.append(f"1 CHIL @{chil}@")
    lines.append("")

lines.append("0 TRLR")

out_path = 'C:/Users/hspen/.openclaw/workspace/family-history/research/full-family-history.ged'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Written: {out_path}")
print(f"Lines: {len(lines)}")
