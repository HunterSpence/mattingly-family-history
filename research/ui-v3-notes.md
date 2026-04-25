# UI v3 Notes — Mattingly Family History

**Built:** April 25, 2026  
**Builder:** ui-designer specialist

## What Changed in v3

### 1. Portrait Images on Tree Nodes
- Each D3 tree node now checks `d.data.portrait_url` (propagated from `portrait_url` field on lineage person objects, entities.json, and research/13-portraits-and-images.json)
- If present: renders a 52×52px circular portrait on the LEFT side of the card, clipped with a unique `<clipPath id="pc-N">` per node, gold ring frame (2px stroke #d4a458), outer glow ring, inner shadow for depth
- If absent AND confidence is uncertain (unknown/possible/unverified): card fills with a neutral parchment paper gradient (`ng-paper`) instead of the depth-graduated gradient — visually distinguishes "we know what they looked like" from "we just have a name"
- Portrait URLs also render in entity detail cards as 96×96px circular `<img>` elements with a gold border and box-shadow, floated right inside the card body
- When 13-portraits-and-images.json becomes available, the next `python3 scripts/build_html.py` automatically picks it up

### 2. The Huge "?" Badge
- For nodes with `confidence: "POSSIBLE"`: a **38px serif "?" in #d4a458** with `q-badge-glow` SVG filter glow, positioned bottom-right of the card; subtle amber tint overlay on the whole card; dashed border (6,3 pattern); SVG `<title>` tooltip on hover explains "POSSIBLE — one source / circumstantial"
- For nodes with `confidence: "UNVERIFIED"`: more aggressive — a **34px "?"** plus a full-width amber/red banner strip across the TOP of the card reading "UNVERIFIED — NEEDS RESEARCH" in 8px tracked uppercase; deep red tint overlay; irregular dash pattern (5,3,2,3)
- In entity detail cards: `confidence-question-badge` div with a large "?" and explanatory text; UNVERIFIED also gets an `unverified-banner` pill in the summary line
- Legend updated: "?" swatch added to the tree toolbar legend

### 3. Cinematic Migration Map
- Replaced Leaflet+Dark Matter tiles with a **fully custom vintage SVG map** — no external tile dependency
- 900×480 viewBox, dark parchment palette, faux Mercator projection hand-tuned for aesthetics
- England appears in a **framed inset panel** (top-left), connected to Maryland via a dashed "Atlantic crossing" arc
- Animated **migration polyline** (`stroke-dasharray: 3000; animation: drawPath 3.5s ease-out`) draws itself on page load
- 9 locations from Hampshire to Santa Monica, each with a pulsing ring animation (staggered delays)
- **Hover tooltip** with location name, year range, and a multi-sentence narrative story for each waypoint — includes the 1901 Reeves County oil land purchase, 1904 World's Fair, Boonesborough migration, etc.
- Compass rose (bottom-right), vintage grid overlay, sepia tint filter, vignette gradient overlay
- Leaflet CSS/JS removed from the HTML head

### 4. Hero Cover Enhancements
- **16 CSS-animated floating particles** — amber gold dust motes (`particleDrift` keyframe, 15–30s durations, staggered delays, no JS)
- **Animated radial glow** behind the title (`heroGlow` keyframe, 6s ease-in-out, opacity pulses 0.04→0.10)
- All particle elements are `aria-hidden` and `prefers-reduced-motion` respected (particles + glow hidden)
- Drop cap enlarged: 4.2em → 5.8em; stronger text-shadow triple layer + drop-shadow filter for "illuminated manuscript" effect

### 5. Notable Achievements Section
- Entity detail cards now pull from `research/14-notable-deeds.json` when it exists
- `load_deeds()` handles schema variants: list of `{entity_id, headline, story}` entries (the actual format), as well as `{id/person_id, deeds/notable_deeds}` variants for future-proofing
- Headlines from the deeds file appear in a "Notable Achievements" subsection at the bottom of each person's card

## Data Wiring — New Files Consumed
| File | Status | Field used |
|------|--------|-----------|
| `research/13-portraits-and-images.json` | Not yet created | `{id, portrait_url}` per entry |
| `research/14-notable-deeds.json` | Exists (created by research agent) | `{entity_id, headline}` per entry |
| `research/06-full-mattingly-lineage.json` | Exists | `person.confidence` now normalized to confirmed/probable/possible/unverified/unknown |

## File Sizes (v3)
- Full version: ~305 KB
- Public version: ~302 KB

## Technical Constraints Preserved
- Single self-contained HTML file (no external map tiles)
- D3 v7, vis-timeline CDN retained
- Leaflet removed (no longer needed)
- Both output files regenerate cleanly from one `python3 scripts/build_html.py` run
- All animations guarded by `prefers-reduced-motion: reduce`
- WCAG: all interactive elements have aria-labels; SVG titles on confidence badges; map has role="img" aria-label
