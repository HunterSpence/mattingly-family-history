# UI Redesign Notes — Mattingly Family History

## Design Direction

The goal was to move from "functional engineer build" to something that reads like a
Pentagram-designed family history book: warm, archival, typographically intentional.

## Typography

Replaced Playfair Display with **Cormorant Garamond** as the display face. Cormorant
is free on Google Fonts and has true optical-weight italics, proper ligatures, and
an extremely high x-height that reads beautifully at large sizes. It feels like a
letterpress-era typeface without being pastiche. Lora stays as the reading body face
(excellent hinting at 18px, warm but not fussy). Source Code Pro remains for timestamps
and dates — the monospaced contrast reinforces the archival metadata role.

The transcript now has a proper **drop cap** on Shari's first word, CSS-only using
`::first-letter`. Pull-quote for the most memorable line ("She bought land in
Reeves County...") uses a Cormorant italic at 2rem with a large decorative curly quote.

## Color Palette

Kept the cream ground (`#f7f3ec`) but pushed the accent from a middling mid-brown to a
genuine deep **mahogany** (`#6b2d0e`) used sparingly — cover rule, section h2 underlines,
pull-quote text, entity link hover. A warm **antique gold** (`#b8934a`) handles decorative
elements and secondary accents. **Bottle green** (`#3a5c3a`) is available for confirmed
badges. The result is a three-note palette: cream + mahogany + gold.

## Hero Cover

The cover is now a full-bleed warm-linen block with a top gradient rule in gold-to-mahogany,
a faint inset frame (CSS `::after` pseudo-element), and an eyebrow line in small-caps italic.
The main title is `clamp(2.8rem, 6vw, 5rem)` Cormorant Garamond Bold Italic. A CSS noise
texture (inline SVG `feTurbulence`) adds a subtle paper grain without any external image.
The audio player is wrapped in a translucent pill container.

## Family Tree

Complete redesign of the D3 visualization:
- **14-color depth gradient** from espresso (`#3d1f0d`) at generation 1 down to near-white cream at
  generation 14 — makes descent visually readable at a glance.
- Per-depth **linear gradient fills** on each node card via SVG `defs`, giving a gentle top-to-bottom
  sheen.
- **Generation spine**: "G1"–"G14" labels run down the left margin alongside faint dashed separator
  lines at each generational band — an explicit timeline axis.
- **Diamond badges** (not circles) for generation numbers, rendered in SVG path for archival feel.
- **Cubic bezier links** (S-curve from parent bottom to child top) instead of the default D3
  elbow — softer, less mechanical.
- **Drop-shadow filter** on hover via SVG `feDropShadow`.
- CSS **`@keyframes nodeIn`** staggered by generation class (`.gen-0` through `.gen-13`) — nodes
  fade in generation by generation on page load. Respects `prefers-reduced-motion`.
- Sibling badges remain but now use gold fill with proper Cormorant text.
- Keyboard accessible: all named nodes have `tabindex="0"` and respond to Enter/Space.

## Transcript

Hunter's short interjections get a distinct visual treatment: indented, left-bordered, slightly
muted italic styling (`transcript-turn-hunter`). Shari's turns are the primary text. The speaker
label is now in an absolutely-positioned `speaker-line` flex container, making timestamp alignment
cleaner.

## Print Stylesheet

Substantially expanded: media query resets noise background, hides audio/map/timeline, forces all
`<details>` cards open via `display: block !important` on `.entity-body`, applies `break-inside:
avoid` on cards and callouts, sets 10.5pt body size, renders URLs after external links. The tree
SVG is given explicit print dimensions so it doesn't collapse.

## Tradeoffs

- The Leaflet map and vis-timeline are unchanged functionally — they are styled to match the new
  palette via CSS border/radius changes only.
- Cormorant Garamond adds ~45KB to the font payload (two weights + italics). Acceptable given the
  single-page, family-archive nature of the site.
- The CSS noise texture is a 200x200 inline SVG (~250 bytes gzipped) — negligible.
- No JavaScript was added outside of D3 tree changes. All animations are CSS or D3 transitions.
