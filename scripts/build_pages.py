"""Build Hunter's Roots — multi-page hub-and-spoke site.

One page per surname tree. Reuses CSS from build_html.py so Codex's visual work transfers.
Output: docs/index.html, docs/mattingly.html, docs/spence.html, docs/henslee.html,
        docs/baity.html, docs/lepick.html, docs/boehme.html, docs/teichmueller.html
"""
import html
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
sys.path.insert(0, str(WS / "scripts"))

# Reuse Codex's curated CSS + D3 tree renderer
import build_html as bh  # noqa: E402
from build_html import CSS  # noqa: E402

DOCS = WS / "docs"
ENT = json.loads((WS / "research" / "entities.json").read_text(encoding="utf-8"))
MULTI = json.loads((WS / "research" / "lineage-tree-multi.json").read_text(encoding="utf-8"))

# Surname → metadata: page filename, title, label-prefix-to-match in lineage-tree-multi
SURNAMES = [
    {
        "id": "mattingly",
        "title": "The Mattingly Line",
        "subtitle": "Hampshire England → Maryland 1666 → Kentucky 1786 → Texas 1894 → Hunter",
        "tree_label_substring": None,  # Mattingly is the PRIMARY tree (root: Alric pre-1066)
        "use_primary_tree": True,
        "extra_tree_labels": ["MATTINGLY COUSIN TREE"],
        "summary": (
            "The deepest documented line in the family — over 1,000 years from Anglo-Saxon "
            "Hampshire (Alric, fl. before 1066, holder of Mattingley manor under Edward the "
            "Confessor) through medieval England, then by Thomas Mattingly II to colonial "
            "Maryland in 1666, on to Marion County, Kentucky with the 1786 Catholic migration, "
            "and finally to Texas in 1894 when Edward Mattingly Sr. married May Teichmüller in "
            "La Grange. Hunter inherits this line via his grandmother Sharyn (Shari) Mattingly "
            "Spence, recorded interviewing her grandson in 2025. Y-DNA cluster R-DF27 > Y14084 "
            "confirms unbroken patrilineal descent from Thomas Mattingly I (~1676 CE)."
        ),
        "include_audio": True,
        "branch_match": ["mattingly"],
    },
    {
        "id": "spence",
        "title": "The Spence Line",
        "subtitle": "Scotland (Clan MacDuff sept) → Beaumont, Texas → Hunter (the line he carries his surname from)",
        "tree_label_substring": "PATERNAL — Spence",
        "summary": (
            "Hunter's surname comes from this line — a still-unnamed English immigrant from "
            "north-east England (probably Yorkshire, Durham, or Northumberland) who arrived "
            "Beaumont, Texas through Galveston in the post-Spindletop oil-boom labour wave of "
            "the 1920s-30s. He married American-born Dovie. Their son Dr. Dale William Spence "
            "Sr. (b. ~1934-36 Beaumont) was a Beaumont High School state-track champion, Rice "
            "University track athlete, and 40-year Rice faculty member retiring as Professor "
            "Emeritus of Kinesiology in 2003. Dale Sr. also served ~35 years as a Colonel in "
            "the US Marine Corps Reserve. He married Alice Marie Henslee. Their son Dale "
            "William Spence Jr. is Hunter's father."
        ),
        "branch_match": ["spence paternal"],
    },
    {
        "id": "byrd",
        "title": "The Byrd Line",
        "subtitle": "Colonial Westmoreland VA ~1700 → Alabama → Milam Co TX → Dovie → Dale Sr → Hunter",
        "tree_label_substring": "PATERNAL — Byrd",
        "extra_tree_labels": ["BYRD COUSIN TREE"],
        "summary": (
            "Hunter's paternal grandfather Dale W. Spence Sr.'s mother was <strong>Dovie Byrd</strong>. "
            "The Byrd line traces back through Texas, Alabama, and ultimately to colonial Westmoreland County, "
            "Virginia — the same region as the famous William Byrd dynasty (Westover plantation, founders of "
            "Richmond VA). Multi-tree confirmation across four cousin GEDCOMs. The chain: <strong>John Henry "
            "Bird (Byrd)</strong> ~1700 Westmoreland VA → Richard George → Rev. William M. (m. Lydia Adair) → "
            "Michael → John Howard → Benjamin Franklin (1798) → <strong>Pvt William Leander Byrd</strong> "
            "(1832 Frankfort AL CSA, 1889) → <strong>John Archie Asner Byrd</strong> (1868 Birmingham AL – 1928 "
            "Sharp Cemetery, Milam County TX) m. Martha Alice Bedford → <strong>Dovie Byrd</strong> + brother "
            "Otha Lee Byrd (1902-1989) → <strong>Dale W. Spence Sr.</strong> → Dale Jr. → Hunter."
        ),
        "branch_match": ["byrd"],
    },
    {
        "id": "henslee",
        "title": "The Henslee Line",
        "subtitle": "Dallas → Beaumont → Nederland, Texas — Hunter's paternal grandmother's people",
        "tree_label_substring": "PATERNAL — Henslee",
        "extra_tree_labels": ["HENSLEE COUSIN TREE", "STUART COUSIN TREE", "PATERNAL — Rau"],
        "summary": (
            "Lee Stuart Henslee married Frances of Dallas around 1948. They lived 55 years in "
            "Beaumont, Texas before retiring to Nederland in 1993. They were practising "
            "Catholics at St. Charles Borromeo, and both are buried at Forest Lawn Memorial "
            "Park, Beaumont. Frances passed in December 2008 at age 90. Their daughter Alice "
            "Marie Henslee (1936 Rusk, TX – 2005 Beaumont) married Dr. Dale William Spence Sr., "
            "becoming Hunter's paternal grandmother. Their son Don Henslee, his wife Jo Ann, and "
            "Don's children Chad, Stacy, and Jennifer represent the line that stayed in "
            "Nederland."
        ),
        "branch_match": ["henslee"],
    },
    {
        "id": "baity",
        "title": "The Baity Line",
        "subtitle": "Border Scots → Ulster 1610 → Pennsylvania → North Carolina → San Antonio",
        "tree_label_substring": "MATERNAL — Baity",
        "extra_tree_labels": ["BAITY COUSIN TREE"],
        "summary": (
            "A classic Scots-Irish migration corridor. The surname was \"Beatty\" or \"Beattie\" "
            "in the Scottish Borders — a diminutive of Bartholomew (Bate-y). The family moved "
            "with the 1610-1640 Plantation of Ulster (Counties Down, Tyrone, Antrim, Fermanagh), "
            "then sailed to Philadelphia c. 1729 (Charles Beatty in the Filby PILI immigrant "
            "index), down the Great Wagon Road to Lancaster County PA, the Shenandoah Valley, "
            "and into Rowan County, North Carolina by 1753. The earliest verified ancestor is "
            "George Baity / Batee / Baty (adult by 1774, Rowan/Surry County NC court records). "
            "Five generations later, Pearl Mae 'Paralee' Johnson Baity (b. 26 July 1878 NC) came "
            "to Texas as a child, married San Antonio builder W.A. Baity, and bought land in "
            "Reeves County in 1901 retaining the mineral rights — the same Wolfcamp/Spraberry "
            "geology USGS would assess as one of the largest US oil reserves in 2016."
        ),
        "branch_match": ["baity"],
    },
    {
        "id": "lepick",
        "title": "The Lepik / Lepick Line",
        "subtitle": "Frýdek-Místek, Moravia 1862 → Bohemia → Brown County, Kansas 1881 → Floresville, Texas",
        "tree_label_substring": "MATERNAL — Lepi",
        "summary": (
            "Frank Lepik was born around 1862 in the Frýdek-Místek district of the Moravian-"
            "Silesian region — where 54% of all Czech bearers of the surname Lepík still live "
            "today. He emigrated in 1881 to Brown County, Kansas, where on 13 January 1885 he "
            "married Mary Mikeska (also Czech-Moravian) at Saint Joseph Catholic Church in "
            "Everest, KS. Frank was a shoemaker, a member of I.O.O.F. Lodge No. 331 in Horton, "
            "Kansas, and a practising Roman Catholic. He and Mary had nine children. The family "
            "moved to Hazen, Arkansas around 1900 and then to Wilson County, Texas in the early "
            "1920s. Their son Fred Charles Lepick Sr. (b. 8 March 1894 Brown Co. KS) married "
            "Hilda Boehme around 1920; their daughter Jennive Imogene Lepick (1923 Floresville "
            "TX – 2008 Colorado Springs) is Hunter's maternal great-grandmother and the wife of "
            "Leroy Baity Mattingly."
        ),
        "branch_match": ["lepi", "mikeska"],
    },
    {
        "id": "boehme",
        "title": "The Boehme / Macker Line",
        "subtitle": "Prussian Silesia → Indianola, Texas → Lavaca County (Lutheran German-Texan)",
        "tree_label_substring": "MATERNAL — Boehme",
        "summary": (
            "The surname Böhme literally means \"a Bohemian\" — most heavily concentrated in "
            "Saxony and Silesia, the German-speaking zones immediately adjacent to Bohemia. "
            "Hunter's Boehme ancestors arrived at the now-vanished Texas port of Indianola "
            "between 1855 and 1862 (its 1875 hurricane destroyed most of the passenger "
            "manifests). They came almost certainly from Prussian Silesia (Schlesien) — the "
            "convergent toponym evidence is Breslau, Texas, a Lavaca County community 7 miles "
            "north-west of Hallettsville, named for the Prussian city of Breslau (now Wrocław). "
            "Their grandson Herman F. Boehme (b. 9 June 1863 Texas – d. 18 June 1900 Shiner, "
            "Lavaca Co.) married Minna Marie Macker. Hilda Boehme, their daughter, was Hunter's "
            "maternal great-great-grandmother. Minna outlived Herman by 47 years, remarried "
            "John W. Luedecke, and died in Floresville on 29 May 1947."
        ),
        "branch_match": ["boehme", "macker"],
    },
    {
        "id": "teichmueller",
        "title": "The Teichmüller Line",
        "subtitle": "Harz mountains 1580 → Brunswick → La Grange, Texas (six confirmed German generations)",
        "tree_label_substring": "Teichmüller",
        "extra_tree_labels": ["TEICHMUELLER COUSIN TREE"],
        "summary": (
            "The deepest German line in Hunter's family — confirmed by the Neue Deutsche "
            "Biographie (vol. 26, 2016, p. 6). Six documented patrilineal generations: "
            "<strong>Hans / Johann Teichmüller</strong> (~1580–1638), master miller in the "
            "southern Harz mountains — the surname is occupational, \"pond miller\". Then "
            "<strong>Joachim Andreas Teichmüller</strong> (1705–1778), commercial agent in "
            "Goslar; <strong>Wilhelm Ernst Conrad Teichmüller</strong> (1758–1835), inspector of "
            "the Karlshütte iron-smelting works near Delligsen; <strong>August Wilhelm "
            "Teichmüller</strong> (1795–1855), lieutenant in the Brunswick army's Schwarzen "
            "Corps des Majors Olfermann (the famous Black Brunswickers), who married Charlotte "
            "Georgine Elisabeth von Girsewald (1799–1860). Their five children include "
            "<strong>Gustav Teichmüller</strong> (1832–1888), the philosopher who personally "
            "influenced Friedrich Nietzsche, and Hunter's direct ancestor <strong>Hans "
            "Teichmueller</strong> (1837 Brunswick – 1901 La Grange TX), who emigrated to Texas "
            "in 1854, served as a Confederate artillery officer, and finished his career as a "
            "justice of the peace. His daughter May Teichmueller married Edward Mattingly Sr. "
            "in 1894."
        ),
        "branch_match": ["teichm"],
    },
    {
        "id": "westerfield",
        "title": "The Westerfield / Trifon Line",
        "subtitle": "Ohio County, Kentucky 1853 → Arkansas → Hunter's maternal grandfather David A. Trifon",
        "tree_label_substring": "Westerfield/Trifon",
        "extra_tree_labels": ["Padgett ancestors", "Ballentine ancestors"],
        "summary": (
            "Hunter's maternal grandfather is <strong>David A. Trifon</strong>, whose biological father "
            "was Harold 'Hal David' Ballentine and whose mother was <strong>Iris June Westerfield</strong> "
            "(1919 Tuckerman, Arkansas – 2003 Colt, Arkansas). David took the surname Trifon from his "
            "stepfather after Harold Ballentine died around 1945. The Westerfield line traces back to "
            "<strong>Joel Hayden Westerfield</strong> (born June 1853, Ohio County, Kentucky), who moved "
            "the family to Arkansas. Joel's son <strong>Jesse Lawrence Westerfield</strong> (1887–1951) "
            "married <strong>Bertie Jane Padgett</strong> (1888–1964), daughter of Arkansas settler "
            "William Miller Padgett (whose own father John J. Padgett came from Indiana). Jesse and "
            "Bertie had five children: Cleofus, Iris, Padgett Lee (Chevy dealer), Maxie Eugene, and "
            "Wayne Miller. Iris married Harold Ballentine and had David (Trifon), Carol Ward, and "
            "Doris Walls. David's daughters are Charmaine and Rachel — Rachel is Hunter's mother. "
            "The Ballentine line runs back through David Wyle Ballentine (1856, Ozark, Franklin County "
            "Arkansas) and John Wallace Ballentine (born ~1826, Virginia) to John Ballentine (~1800, "
            "Virginia/North Carolina), the earliest confirmed Ballentine ancestor."
        ),
        "branch_match": ["westerfield", "trifon", "ballentine", "padgett"],
    },
]


# ── Helpers ─────────────────────────────────────────────────────

def find_tree(label_substring):
    """Find the secondary tree whose label contains the given substring (case-insensitive)."""
    if label_substring is None:
        return None
    sub = label_substring.lower()
    for st in MULTI.get("secondary_trees", []) or []:
        if sub in (st.get("label", "") or "").lower():
            return st["tree"]
    return None


def get_primary_tree():
    return MULTI.get("primary")


def render_d3_tree_section(tree_root):
    """Render Codex's D3 tree HTML for a given subtree (not from lineage-tree.json).
    Monkey-patches build_lineage_tree_data temporarily so render_lineage_tree_section
    receives the right subtree. Returns the inner SVG + tree-data <script> only —
    skips the Mattingly-specific header so it works on any surname page.
    """
    import json as _json
    if not tree_root:
        return '<p style="color:var(--ink-soft);font-style:italic">(no tree data wired for this surname yet)</p>'
    # Inject portraits if entity has portrait_url
    portrait_map = {p["id"]: p["portrait_url"]
                    for p in ENT.get("people", [])
                    if p.get("id") and p.get("portrait_url")}

    # Deep clone so monkey-patch doesn't affect other pages
    import copy
    subtree = copy.deepcopy(tree_root)
    bh._inject_portraits(subtree, portrait_map)
    tree_data_json = _json.dumps(subtree)

    return f"""<div id="lineage-section">
  <div class="tree-toolbar" role="toolbar" aria-label="Family tree controls">
    <div class="btn-group">
      <button onclick="treeZoomIn()" aria-label="Zoom in" title="Zoom in">+</button>
      <button onclick="treeZoomOut()" aria-label="Zoom out" title="Zoom out">&#8722;</button>
      <button onclick="treeZoomReset()" aria-label="Reset view" title="Reset zoom">Reset</button>
    </div>
    <div class="tree-legend" aria-label="Confidence level legend">
      <span class="legend-item"><span class="swatch confirmed"></span>Confirmed</span>
      <span class="legend-item"><span class="swatch probable"></span>Probable</span>
      <span class="legend-item"><span class="swatch unknown"></span>Research pending</span>
      <span class="legend-item"><span style="font-family:'Cormorant Garamond',serif;font-size:1.15em;font-weight:700;color:#d4a458">?</span>&#8201;Uncertain</span>
    </div>
  </div>
  <div id="lineage-tree-container" role="img" aria-label="Interactive family tree">
    <svg id="lineage-tree-svg" xmlns="http://www.w3.org/2000/svg"></svg>
  </div>
  <p class="tree-hint">Scroll or pinch to zoom &nbsp;&middot;&nbsp; Drag to pan &nbsp;&middot;&nbsp; Click a named node for details</p>
</div>
<script id="lineage-tree-data" type="application/json">{tree_data_json}</script>"""


def render_node_ul(node, depth=0):
    """Render a tree as a nested HTML list."""
    if not isinstance(node, dict):
        return ""
    name = html.escape(node.get("name", "?"))
    dates = html.escape(node.get("dates", "") or "")
    fact = html.escape(node.get("fact", "") or "")
    spouse = html.escape(node.get("spouse", "") or "")
    conf = node.get("confidence", "unknown")
    children = node.get("children", []) or []
    spouse_html = f' <span class="subtree-spouse">m. {spouse}</span>' if spouse else ""
    dates_html = f' <span class="subtree-dates">({dates})</span>' if dates else ""
    fact_html = f' <span class="subtree-fact">— {fact}</span>' if fact else ""
    item = f'<li class="subtree-li conf-{conf}"><span class="subtree-name">{name}</span>{dates_html}{spouse_html}{fact_html}'
    if children:
        item += "<ul>" + "".join(render_node_ul(c, depth + 1) for c in children) + "</ul>"
    item += "</li>"
    return item


def render_entity_cards(branch_keywords):
    """Render entity cards filtered by branch-keyword match."""
    keywords = [k.lower() for k in branch_keywords]
    cards = []
    for p in ENT.get("people", []):
        branch = (p.get("branch", "") or "").lower()
        if not any(k in branch for k in keywords):
            continue
        name = html.escape(p.get("full_name", "?"))
        dates = []
        if p.get("birth_year"):
            dates.append(f"b. {p['birth_year']}")
        if p.get("death_year"):
            dates.append(f"d. {p['death_year']}")
        date_str = " – ".join(dates) if dates else (p.get("relation_to_shari") or "")
        ctx = html.escape(p.get("context", "") or p.get("enriched_context", "") or "")
        conf = (p.get("confidence", "") or "").lower()
        portrait = p.get("portrait_url")
        portrait_html = (f'<img class="card-portrait" src="{html.escape(portrait)}" alt="{name}">'
                         if portrait else "")
        cards.append(f"""
<article class="person-card conf-{conf}">
  {portrait_html}
  <h4>{name}</h4>
  <p class="card-dates">{html.escape(date_str)}</p>
  <p class="card-ctx">{ctx}</p>
</article>""")
    return "\n".join(cards) if cards else ""


def common_nav():
    """Top-of-page navigation linking back to home + each surname."""
    items = ['<a href="index.html">Home</a>']
    for s in SURNAMES:
        items.append(f'<a href="{s["id"]}.html">{html.escape(s["title"].replace("The ", "").replace(" Line", ""))}</a>')
    return f'<nav class="surname-nav">{"".join(items)}</nav>'


# ── Page generators ─────────────────────────────────────────────

def html_shell(title, body, include_tree_js=False):
    tree_js_block = ""
    if include_tree_js:
        d3_js = bh.render_lineage_tree_js()
        tree_js_block = f"""
<script src="https://unpkg.com/d3@7/dist/d3.min.js"></script>
<script>
{d3_js}
</script>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,700&family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Source+Code+Pro:wght@400&display=swap" rel="stylesheet">
  <style>
{CSS}

/* Multi-page additions */
.surname-nav {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px 20px;
  padding: 14px 24px;
  border-bottom: 1px solid var(--rule);
  background: linear-gradient(180deg, #18130d 0%, #120e08 100%);
  font-family: 'Lora', Georgia, serif;
  font-size: var(--fs-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}}
.surname-nav a {{
  color: var(--ink-soft);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  padding: 4px 6px;
  transition: color 0.15s, border-color 0.15s;
}}
.surname-nav a:hover {{
  color: var(--accent-gold);
  border-bottom-color: var(--accent-gold);
}}

.hub-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 18px;
  margin: var(--sp-lg) 0;
}}
.hub-card {{
  background: linear-gradient(180deg, #1a1610 0%, #14110c 100%);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent-gold);
  border-radius: 6px;
  padding: var(--sp-md) var(--sp-lg);
  transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s;
}}
.hub-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.55);
  border-left-color: #e8c878;
}}
.hub-card a {{
  text-decoration: none;
  color: inherit;
  display: block;
}}
.hub-card h2 {{
  margin: 0 0 6px;
  font-family: 'Cormorant Garamond', serif;
  color: var(--accent-gold);
  font-size: 1.45rem;
}}
.hub-card .sub {{
  color: var(--ink-soft);
  font-size: 0.92rem;
  margin: 0 0 var(--sp-sm);
  font-style: italic;
}}
.hub-card .body {{
  color: var(--ink-bright);
  font-size: 0.94rem;
  line-height: 1.55;
}}

.hero-mini {{
  padding: var(--sp-xl) 0 var(--sp-lg);
  text-align: center;
  border-bottom: 1px solid var(--rule);
}}
.hero-mini h1 {{
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 5vw, 3.8rem);
  letter-spacing: 0.02em;
  color: var(--accent-gold);
  margin: 0 0 14px;
  font-weight: 600;
}}
.hero-mini .tagline {{
  color: var(--ink-soft);
  font-style: italic;
  font-size: 1.08rem;
  max-width: 720px;
  margin: 0 auto;
}}

.surname-page main {{
  max-width: 1100px;
  margin: 0 auto;
  padding: var(--sp-md) var(--sp-lg) var(--sp-xl);
}}

.surname-summary {{
  font-family: 'Lora', Georgia, serif;
  font-size: 1.06rem;
  line-height: 1.7;
  color: var(--ink-bright);
  margin: var(--sp-lg) 0;
  border-left: 3px solid var(--accent-gold);
  padding: var(--sp-sm) var(--sp-lg);
  background: rgba(212, 164, 88, 0.04);
}}

.section-break {{
  margin: var(--sp-xl) 0 var(--sp-md);
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.65rem;
  color: var(--accent-gold);
  border-bottom: 1px solid var(--rule);
  padding-bottom: 10px;
}}

.person-cards-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}}
.person-card {{
  background: linear-gradient(180deg, #1a1610 0%, #14110c 100%);
  border: 1px solid var(--rule);
  border-radius: 5px;
  padding: var(--sp-sm) var(--sp-md);
  font-family: 'Lora', Georgia, serif;
  font-size: 0.92rem;
  line-height: 1.55;
}}
.person-card.conf-confirmed {{ border-left: 2px solid var(--accent-gold); }}
.person-card.conf-probable {{ border-left: 2px solid var(--accent-bronze); }}
.person-card.conf-possible {{ border-left: 2px dashed var(--accent-bronze); }}
.person-card h4 {{
  margin: 0 0 4px;
  color: var(--ink-bright);
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.1rem;
}}
.person-card .card-dates {{
  margin: 0 0 6px;
  font-family: 'Source Code Pro', monospace;
  font-size: 0.82rem;
  color: var(--accent-gold);
}}
.person-card .card-ctx {{
  color: var(--ink-soft);
  margin: 0;
}}
.card-portrait {{
  float: right;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0 0 6px 8px;
  border: 1.5px solid var(--accent-gold);
  object-fit: cover;
}}

.audio-section {{
  background: linear-gradient(180deg, #221b14 0%, #1a1410 100%);
  border: 1px solid var(--rule);
  border-radius: 6px;
  padding: var(--sp-lg);
  margin: var(--sp-lg) 0;
}}
.audio-section h3 {{
  margin: 0 0 6px;
  color: var(--accent-gold);
  font-family: 'Cormorant Garamond', serif;
}}
.audio-section audio {{
  width: 100%;
  margin-top: var(--sp-sm);
}}

footer.site-footer {{
  margin-top: var(--sp-xl);
  padding: var(--sp-md) var(--sp-lg);
  border-top: 1px solid var(--rule);
  font-size: 0.82rem;
  color: var(--ink-ghost);
  text-align: center;
}}
  </style>
</head>
<body class="surname-page">
  {body}
  <footer class="site-footer">
    Hunter's Roots — assembled from primary sources, oral history, DNA, and parish records.
    Last updated 2026. Source files live in <a href="https://github.com/HunterSpence/mattingly-family-history">github.com/HunterSpence/mattingly-family-history</a>.
  </footer>
{tree_js_block}
</body>
</html>"""


def _line_origin_for(line_name):
    """Look up a single surname-line origin record from research/line-origins.json."""
    origins_path = WS / "research" / "line-origins.json"
    if not origins_path.exists():
        return None, None
    data = json.loads(origins_path.read_text(encoding="utf-8"))
    return data.get("lines", {}).get(line_name), data.get("country_flags", {})


def render_surname_heritage_card(line_name):
    """Compact heritage card for the top of a surname page — shows the country flag,
    earliest CONFIRMED ancestor, and the immigrant who first set foot in America for this line.
    Pulls from research/line-origins.json (produced by enrich_immigrants_and_origins.py)."""
    info, flags = _line_origin_for(line_name)
    if not info:
        return ""
    country = info.get("country", "?")
    flag = (flags or {}).get(country, "")
    year = info.get("earliest_confirmed_year") or "?"
    person = info.get("earliest_confirmed_person") or "Earliest confirmed: pending research"
    immigrant = info.get("immigrant_in_line") or info.get("immigrant_candidate") or "(immigrant identification pending — see Research notes)"
    clan = info.get("clan_affiliation", "")
    clan_motto = info.get("clan_motto", "")
    notable = info.get("notable_relative") or info.get("notable_in_line") or ""
    ydna = info.get("ydna_haplogroup", "")
    subregion = info.get("country_subregion") or info.get("country_region", "")
    evidence = info.get("evidence", "")

    clan_block = ""
    if clan:
        motto_str = f' &nbsp;·&nbsp; <em>"{html.escape(clan_motto)}"</em>' if clan_motto else ""
        clan_block = f'<div class="hcard-clan">⚔ <strong>{html.escape(clan)}</strong>{motto_str}</div>'
    notable_block = f'<div class="hcard-notable">⭐ <strong>Notable in line:</strong> {html.escape(notable)}</div>' if notable else ""
    ydna_block = f'<div class="hcard-ydna">🧬 <strong>Y-DNA:</strong> {html.escape(ydna)}</div>' if ydna else ""
    subregion_str = f' <span class="hcard-subregion">— {html.escape(subregion)}</span>' if subregion else ""

    return f"""
<aside class="surname-heritage-card" aria-label="Heritage origin for the {html.escape(line_name)} line">
  <div class="hcard-flag-block">
    <div class="hcard-flag" aria-hidden="true">{flag}</div>
    <div class="hcard-country">
      <strong>{html.escape(country)}</strong>{subregion_str}
    </div>
  </div>
  <div class="hcard-body">
    <div class="hcard-row"><span class="hcard-label">Earliest confirmed</span><span class="hcard-value">{html.escape(str(year))} — {html.escape(person)}</span></div>
    <div class="hcard-row"><span class="hcard-label">★ Immigrant to America</span><span class="hcard-value">{html.escape(immigrant)}</span></div>
    {clan_block}
    {notable_block}
    {ydna_block}
    <details class="hcard-evidence"><summary>Evidence &amp; sources</summary><p>{html.escape(evidence)}</p></details>
  </div>
</aside>"""


def render_full_heritage_panel():
    """Full heritage panel for the index page — covers all surname lines + breakdown chart."""
    origins_path = WS / "research" / "line-origins.json"
    if not origins_path.exists():
        return ""
    data = json.loads(origins_path.read_text(encoding="utf-8"))
    lines = data.get("lines", {})
    flags = data.get("country_flags", {})

    PATERNAL = ["Spence", "Henslee", "Byrd", "Baity", "Rau"]
    MATERNAL = ["Mattingly", "Teichmueller", "Lepick", "Boehme"]

    def _card(name, info):
        if not info:
            return ""
        country = info.get("country", "?")
        flag = flags.get(country, "")
        year = info.get("earliest_confirmed_year") or "?"
        person = info.get("earliest_confirmed_person") or "Earliest confirmed: pending"
        immigrant = info.get("immigrant_in_line") or info.get("immigrant_candidate") or "(immigrant identification pending)"
        clan = info.get("clan_affiliation", "")
        notable = info.get("notable_relative") or info.get("notable_in_line") or ""
        evidence = info.get("evidence", "")
        subregion = info.get("country_subregion") or info.get("country_region", "")
        subregion_str = f' <span class="hcard-subregion">— {html.escape(subregion)}</span>' if subregion else ""
        clan_block = f'<div class="hcard-clan">⚔ <strong>{html.escape(clan)}</strong></div>' if clan else ""
        notable_block = f'<div class="hcard-notable">⭐ {html.escape(notable)}</div>' if notable else ""
        return f"""
        <article class="heritage-card">
          <header class="heritage-header">
            <span class="heritage-flag" aria-hidden="true">{flag}</span>
            <div>
              <h3 class="heritage-surname">{html.escape(name)}</h3>
              <div class="heritage-country"><strong>{html.escape(country)}</strong>{subregion_str}</div>
            </div>
          </header>
          <div class="heritage-body">
            <div class="heritage-row">
              <span class="heritage-label">Earliest confirmed</span>
              <span class="heritage-value">{html.escape(str(year))} — {html.escape(person)}</span>
            </div>
            <div class="heritage-row">
              <span class="heritage-label">★ Immigrant to America</span>
              <span class="heritage-value">{html.escape(immigrant)}</span>
            </div>
            {clan_block}
            {notable_block}
            <details class="heritage-evidence"><summary>Evidence &amp; sources</summary><p>{html.escape(evidence)}</p></details>
            <a class="heritage-deep-link" href="{name.lower()}.html">Full {html.escape(name)} tree →</a>
          </div>
        </article>"""

    pat_cards = "\n".join(_card(n, lines.get(n)) for n in PATERNAL if lines.get(n))
    mat_cards = "\n".join(_card(n, lines.get(n)) for n in MATERNAL if lines.get(n))

    # Heritage breakdown bar chart
    country_count = {}
    for info in lines.values():
        c = info.get("country")
        if c:
            country_count[c] = country_count.get(c, 0) + 1
    total = sum(country_count.values()) or 1
    rows = ""
    for c, ct in sorted(country_count.items(), key=lambda x: -x[1]):
        pct = round(ct / total * 100)
        flag = flags.get(c, "")
        rows += f"""
        <div class="heritage-bar-row">
          <span class="heritage-bar-flag">{flag}</span>
          <span class="heritage-bar-country">{html.escape(c)}</span>
          <div class="heritage-bar-track"><div class="heritage-bar-fill" style="width:{pct}%"></div></div>
          <span class="heritage-bar-pct">{pct}%</span>
          <span class="heritage-bar-count">({ct} {'line' if ct == 1 else 'lines'})</span>
        </div>"""

    return f"""
<section id="heritage" class="heritage-section">
  <h2>Heritage &amp; Origins</h2>
  <p class="heritage-intro">
    Each surname line traced back to its earliest <strong>confirmed</strong> ancestor (primary-source verified)
    with the country of origin and — where identified — the direct ancestor who <strong>first set foot in America</strong>
    for that line. On every family-tree page, immigrant ancestors are marked with a <span class="heritage-green">green border</span>
    and the country flag of where they came from.
  </p>
  <div class="heritage-breakdown">
    <h3>Heritage by surname line</h3>
    {rows}
  </div>
  <h3 class="heritage-subhead">Paternal Lines (via Dale W. Spence Sr.)</h3>
  <div class="heritage-grid">{pat_cards}</div>
  <h3 class="heritage-subhead">Maternal Lines (via Sharyn Mattingly)</h3>
  <div class="heritage-grid">{mat_cards}</div>
</section>
"""


def build_index():
    cards = []
    for s in SURNAMES:
        cards.append(f'''<div class="hub-card">
  <a href="{s["id"]}.html">
    <h2>{html.escape(s["title"])}</h2>
    <p class="sub">{html.escape(s["subtitle"])}</p>
    <p class="body">{s["summary"][:240]}…</p>
  </a>
</div>''')
    heritage_html = render_full_heritage_panel()
    body = f"""
{common_nav()}
<div class="hero-mini">
  <h1>Hunter's Roots</h1>
  <p class="tagline">A family archive, branch by branch — every named ancestor traced to a primary source.</p>
</div>
<main>
  <section class="surname-summary">
    These are the lines that converged to make me. Each surname below is its own page —
    its own tree, its own people, its own migration story. Some go back a thousand years,
    others one hundred. They start everywhere from Anglo-Saxon Hampshire to Bohemian Moravia
    to the Beaumont, Texas oil boom.
  </section>
  {heritage_html}
  <h2 class="section-break">The Lines</h2>
  <div class="hub-grid">
    {"".join(cards)}
  </div>
</main>
"""
    return html_shell("Hunter's Roots — Family Archive", body)


def find_all_trees_matching(label_substrings):
    """Find ALL secondary trees whose labels contain any of the given substrings."""
    found = []
    subs = [s.lower() for s in label_substrings]
    for st in MULTI.get("secondary_trees", []) or []:
        label = (st.get("label", "") or "").lower()
        for sub in subs:
            if sub in label:
                found.append({"label": st.get("label", ""), "tree": st["tree"]})
                break
    return found


def build_surname_page(s):
    if s.get("use_primary_tree"):
        primary_tree = get_primary_tree()
        primary_label = "Primary spine (Hunter's direct line)"
    else:
        primary_tree = find_tree(s.get("tree_label_substring") or s["title"])
        primary_label = "Hunter's direct line"
    d3_tree_html = render_d3_tree_section(primary_tree)
    list_tree_html = render_node_ul(primary_tree) if primary_tree else ""

    # Render extra cousin-GEDCOM trees
    extra_trees_html = ""
    extra_labels = s.get("extra_tree_labels") or []
    if extra_labels:
        extras = find_all_trees_matching(extra_labels)
        if extras:
            blocks = []
            for ex in extras:
                blocks.append(f"""
<details class="extra-tree-card" open>
  <summary><strong>{html.escape(ex["label"])}</strong></summary>
  <article class="subtree-card">
    <ul class="subtree-tree">{render_node_ul(ex["tree"])}</ul>
  </article>
</details>""")
            extra_trees_html = (
                '<h2 class="section-break">Extended Cousin Trees</h2>'
                '<p style="color:var(--ink-soft);font-style:italic;margin-bottom:var(--sp-md);">'
                "These wider trees are pulled directly from your DNA matches' "
                "Ancestry GEDCOMs — every documented cousin, sibling, and descendant "
                "shared in their family tree."
                "</p>"
                + "".join(blocks)
            )
    cards = render_entity_cards(s.get("branch_match") or [s["id"]])
    cards_section = (f'<h2 class="section-break">People</h2><div class="person-cards-grid">{cards}</div>'
                     if cards else "")

    audio_section = ""
    if s.get("include_audio"):
        audio_section = """
<div class="audio-section">
  <h3>Grandma Shari's Interview (the seed of this archive)</h3>
  <p>The recording that started everything — Sharyn (Shari) Mattingly Spence sitting down with
  her grandson Hunter in 2025, retelling the family stories she has been carrying for seventy
  years. The Mattingly tree above is largely the verified backbone of what she remembered.</p>
  <audio controls preload="metadata">
    <source src="audio/source.m4a" type="audio/mp4">
  </audio>
</div>"""

    list_block = ""
    if list_tree_html:
        list_block = f"""<details class="subtree-details">
  <summary>Show as nested list</summary>
  <article class="subtree-card">
    <ul class="subtree-tree">{list_tree_html}</ul>
  </article>
</details>"""

    # LINE_ORIGINS uses TitleCase keys (Mattingly, Spence, etc.); SURNAMES["id"] is lowercase
    line_name = s["id"].title() if s["id"] != "teichmueller" else "Teichmueller"
    heritage_card_html = render_surname_heritage_card(line_name)

    body = f"""
{common_nav()}
<div class="hero-mini">
  <h1>{html.escape(s["title"])}</h1>
  <p class="tagline">{html.escape(s["subtitle"])}</p>
</div>
<main>
  <section class="surname-summary">{s["summary"]}</section>
  {heritage_card_html}
  {audio_section}
  <h2 class="section-break">Family Tree</h2>
  {d3_tree_html}
  {list_block}
  {extra_trees_html}
  {cards_section}
</main>
"""
    return html_shell(f"Hunter's Roots — {s['title']}", body, include_tree_js=True)


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(build_index(), encoding="utf-8")
    print(f"Wrote docs/index.html")
    for s in SURNAMES:
        out = DOCS / f"{s['id']}.html"
        out.write_text(build_surname_page(s), encoding="utf-8")
        print(f"Wrote docs/{s['id']}.html")


if __name__ == "__main__":
    main()
