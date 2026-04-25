# Mattingly Family History

> An interactive family-history archive built from a 46-minute audio interview with Shari ("Sharyn"), Hunter Spence's grandmother. Fourteen generations of Mattinglys, from a Catholic immigrant arriving in Maryland in 1663 down to today.

**🌐 Live site:** https://hunterspence.github.io/mattingly-family-history

---

## What's in here

- **The interview** — a verbatim transcript with speaker labels, timestamps, and inline links to every named person and place
- **An interactive family tree** — D3-driven, fourteen generations from Thomas Mattingly I (England → Maryland 1663) to Hunter
- **A cast of characters** — 38 people with biographical detail, cited sources, and confidence ratings
- **Migration map** — Leaflet, traces England → Maryland → Kentucky → North Carolina → Texas → California
- **Timeline** — vis-timeline showing family events overlaid with historical context (Civil War, Spindletop 1901, 1929 crash, World's Fairs, etc.)
- **Research findings** — six markdown files with verified facts, source URLs, and confidence levels
- **Embedded audio** — Shari's voice, the irreplaceable original
- **GEDCOM file** — `output/family-tree.ged`, importable into FamilyEcho, MyHeritage, Ancestry, WikiTree

## Notable Mattingly facts surfaced by the research

- **Thomas Mattingly I** (~1623–~1665) arrived in Maryland 1663–64 as a Catholic refugee. His sons received the **Mattingly's Hope** 300-acre land patent in Charles County, Maryland on **September 4, 1666**.
- **Mattingley village** in Hampshire, England (recorded in the Domesday Book of 1086 as *Matingelege* — "the woodland clearing of Matta's people") is the surname's etymological origin.
- The "Beringa tribe" of Shari's family lore is actually the **Basingas** — a Wessex Anglo-Saxon clan whose name survives in Old Basing and Basingstoke.
- Shari's great-great-aunt **Minette Teichmueller** (1871–1970) was a documented WPA muralist; her painting *The Law, Texas Rangers* still hangs in the Smithville, Texas post office.
- Her husband, **Hugo D. Pohl** (1878–1960), painted the 36×75-foot stage curtain for the San Antonio Municipal Auditorium (destroyed in a 1979 fire).
- Shari's great-grandmother **Pearl Baity** (b. 1870s NC, d. 1971) bought land in **Reeves County, Texas** in April 1901 — three months after Spindletop spudded — and kept the mineral rights when she sold. That land is now part of the **Wolfcamp Shale**, the largest USGS-assessed oil reserve in American history.
- The family home Pearl built in 1905 still stands at **211 Castillo Avenue, San Antonio, TX 78210**.
- An ancestor lived to **107 years old**, dying in 1935.

## The technical pipeline

```
Grandma Shari Family History.m4a   (46:11, 75 MB)
            │
            ▼
Pass 1 — Deepgram Nova-3 with seed keyterms
Pass 2 — Deepgram Nova-3 with 88-keyterm vocabulary
Pass 3 — Claude Haiku 4.5 cleanup, speaker labels, diacritic restoration
            │
            ▼
final.md  (verbatim transcript)
            │
            ▼
Claude Sonnet 4.6 entity extraction → entities.json
            │
            ▼
6 parallel Sonnet researcher subagents (FamilySearch, WikiTree, Wikipedia, LOC, Maryland State Archives, etc.)
            │
            ▼
Build script — single self-contained HTML with D3 + Leaflet + vis-timeline
            │
            ▼
GitHub Pages
```

Total cost end-to-end: **under $5** (Deepgram + Anthropic API).

## Running it yourself

```bash
# Install dependencies
pip install deepgram-sdk anthropic

# Set keys
export DEEPGRAM_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

# Run the pipeline
cd scripts
python pass1_transcribe.py
python pass2_transcribe.py
python pass3_cleanup.py
python extract_entities.py
python patch_entities.py        # apply Hunter's clarifications
python apply_research.py        # apply research findings
python build_html.py            # generate HTML
python build_gedcom.py          # generate GEDCOM
```

## Files

```
.
├── audio/source.m4a              ← the irreplaceable original (75 MB)
├── transcripts/final.md          ← verbatim transcript
├── research/
│   ├── entities.json             ← structured entities (38 people, 29 places, ...)
│   ├── 01-mattingly-lineage.md   ← deceased ancestor research
│   ├── 02-texas-places.md        ← 211 Castillo, Reeves County, Wolfcamp, Spindletop
│   ├── 03-pohl-monette-art.md    ← Hugo Pohl + Minette Teichmueller corrections
│   ├── 04-english-origins.md     ← Mattingley village, Basingas tribe, Domesday
│   ├── 05-scandal-and-loose-ends.md   ← Claude scandal, Ignatius, Sul Ross
│   ├── 06-full-mattingly-lineage.md   ← Thomas (1663) → Hunter
│   └── family-tree-extension-plan.md  ← roadmap for further research
├── scripts/                      ← Python pipeline
├── docs/                         ← GitHub Pages serves from here
│   ├── index.html                ← redacted public version
│   ├── family.html               ← full names version
│   ├── audio/source.m4a
│   └── family-tree.ged
└── output/                       ← local build artifacts (mirror of docs/)
```

## Confidence

Every fact in the research files is rated:

- **CONFIRMED** — three or more independent sources agree
- **PROBABLE** — two sources agree, no contradictions
- **POSSIBLE** — one source or strong circumstantial evidence
- **UNVERIFIED** — inference only, flagged

Where the historical record contradicts Shari's account, the discrepancy is preserved and noted (e.g., 1660 vs. 1663–64 arrival date, "Beringa" vs. Basingas, 1903 vs. 1904 World's Fair).

## Privacy

Two HTML versions are generated:

- **`index.html`** (default for the live site) — names of living relatives are redacted
- **`family.html`** — full names, intended for family viewing

The audio file is the original recording — please be respectful when sharing.

## Credits

- **Subject:** Sharyn Mattingly Spence ("Shari"), Hunter's grandmother
- **Interviewer:** Hunter Spence
- **Build pipeline:** Claude (Anthropic) — Deepgram + Sonnet + Haiku + parallel researcher subagents
- **Visualization:** D3.js v7, Leaflet, vis-timeline, all CDN-hosted
- **Typography:** Lora, Playfair Display, Source Code Pro (via Google Fonts)

## License

This archive is a personal family history. All content (audio, transcript, photos) © Hunter Spence 2026, all rights reserved. The build scripts in `scripts/` are released under MIT — feel free to adapt them for your own family-history projects.
