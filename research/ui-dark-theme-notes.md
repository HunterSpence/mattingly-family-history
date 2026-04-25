# UI Dark Theme Notes — Mattingly Family History

## Design Concept

The brief was "nighttime in an archive room." A single brass desk lamp. Aged paper warmth
showing through black ink. Not VS Code dark — editorial dark mode with genuine character.

## Palette

- Background: `#0d0a08` (deep warm black — no blue cast)
- Card surface: `#161210` (warm charcoal)
- Elevated surfaces: `#1e1916` (TOC, research blocks)
- Body text: `#e2d5c3` (warm parchment — AAA contrast against background)
- Display headings: `#f0e6d2` (brighter cream — draws the eye)
- Primary accent: `#d4a458` (antique brass gold — used for headlines, rules, tree)
- Secondary accent: `#b8826a` (burnished copper — confidence probable, secondary uses)
- Shari's label: `#e8c88a` (warm amber — warm and readable)
- Hunter's label: `#8a9db5` (muted steel — recessive, interjection feel)

## Hero Cover

Radial gradient dark vignette (`1c1510` at center, `0a0806` at edges) with a 3-axis brass
top rule (transparent → gold → bright → gold → transparent). The title gets a very subtle
gold text-shadow glow. Audio player is restyled as a brass-trimmed metallic control with
a warm gradient housing and `filter: invert(0.85) sepia(0.3)` on the native `<audio>` element.

## Family Tree

Gradient direction inverted from light version: generation 1 (oldest) = deep amber-brown
(`#4a2c0a`), descending to silver-steel (`#4c5c6a`) for Hunter's generation. This creates
visual narrative — warmth = deep history, coolness = present. All text is cream/gold on
dark cards. The connection lines graduate from rich gold (ancient) through bronze to steel.
The glow filter on hover produces a genuine gold halo using `feGaussianBlur + feFlood +
feComposite` — a proper illumination effect, not just a drop shadow. Spine labels use
Cormorant Garamond italic in amber.

## Map

Switched from OpenStreetMap to CartoDB Dark Matter tiles
(`basemaps.cartocdn.com/dark_all`). Migration route polyline in antique gold (`#d4a458`)
dashed. Markers gold-filled with darker gold stroke. Popups styled to match dark palette.

## vis-timeline

CSS overrides applied in-stylesheet targeting `.vis-*` classes within `#timeline-container`.
Group rows styled dark. Item backgrounds use gold with low opacity. Time axis text in monospace.

## Print Stylesheet

Complete light-mode inversion via `!important` overrides: white background, `#1a1614`
ink, warm mahogany accents. Confidence badges revert to their light-mode colours.
All glows and text-shadows stripped. The design prints cleanly without wasting ink.

## Typography on Dark

Reduced `font-weight` from 700 to 600 on `h2` (dark backgrounds make type read heavier).
Increased `letter-spacing` on speaker labels and TOC labels for small-caps legibility.
Drop cap on Shari's first word uses gold with a radial text-shadow glow — the illuminated
manuscript moment the design was built around.
