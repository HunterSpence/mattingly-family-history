"""Build the self-contained HTML deliverable from transcript + entities + research.

Inputs:
  transcripts/final.md
  research/entities.json
  research/01-mattingly-lineage.md (if present)
  research/02-texas-places.md (if present)
  research/03-pohl-monette-art.md (if present)
  research/04-english-origins.md (if present)
  research/05-scandal-and-loose-ends.md (if present)
  research/13-portraits-and-images.json (if present — portrait URLs per person id)
  research/14-notable-deeds.json (if present — notable deeds per person/place)

Outputs:
  output/grandma-shari-family-history.html  (full version, family-only)
  output/grandma-shari-family-history-public.html  (redacted version, shareable)
  docs/family.html  (full GitHub Pages version)
  docs/index.html  (public GitHub Pages version)

The HTML is one file with inline CSS and inline JS. Uses CDN for D3 + vis-timeline.
Leaflet replaced with a custom cinematic SVG migration map (v3).
"""
import html
import json
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
TRANSCRIPT = WORKSPACE / "transcripts" / "final.md"
ENTITIES = WORKSPACE / "research" / "entities.json"
RESEARCH_DIR = WORKSPACE / "research"
PORTRAITS_JSON = WORKSPACE / "research" / "13-portraits-and-images.json"
DEEDS_JSON = WORKSPACE / "research" / "14-notable-deeds.json"
OUT_FAMILY = WORKSPACE / "output" / "grandma-shari-family-history.html"
OUT_PUBLIC = WORKSPACE / "output" / "grandma-shari-family-history-public.html"
DOCS_FAMILY = WORKSPACE / "docs" / "family.html"
DOCS_INDEX = WORKSPACE / "docs" / "index.html"
AUDIO_REL = "audio/source.m4a"

CSS = """
/* =========================================================
   MATTINGLY FAMILY HISTORY — Dark Archive Design System
   Mood: nighttime archive room, brass lamp warmth
   Typography: Cormorant Garamond (display) + Lora (body)
   ========================================================= */

:root {
  /* Palette — dark archive */
  --bg:           #0d0a08;         /* deep warm black — the floor */
  --bg-warm:      #110e0b;         /* slightly lighter warm black */
  --paper:        #161210;         /* card surface — warm charcoal */
  --paper-raised: #1e1916;         /* elevated surface (TOC, research) */
  --ink:          #e2d5c3;         /* warm parchment — primary text */
  --ink-mid:      #c8b89e;         /* mid-tone text */
  --ink-soft:     #9a8a78;         /* muted secondary text */
  --ink-ghost:    #665a4e;         /* barely-there metadata */
  --accent:       #d4a458;         /* antique gold — primary accent */
  --accent-warm:  #c8945a;         /* burnished copper — links */
  --accent-gold:  #d4a458;         /* gold for rules & decoration */
  --accent-gold-light: #a07840;    /* deeper gold for subtle rules */
  --accent-bronze: #b8826a;        /* warm bronze — secondary */
  --green:        #4a8a5a;         /* sage green — confirmed */
  --rule:         #2a2420;         /* near-invisible border */
  --rule-light:   #221e1a;         /* even quieter divider */
  --shari-color:  #e8c88a;         /* warm amber for Shari's label */
  --hunter-color: #8a9db5;         /* muted steel for Hunter's label */
  --confirmed:    #6aaa7a;         /* confirmed badge text */
  --probable:     #c8a050;         /* probable badge text */
  --possible:     #c87060;         /* possible badge text */
  --living:       #7a9ab8;         /* living badge text */

  /* Spacing scale */
  --sp-xs: 4px;
  --sp-sm: 8px;
  --sp-md: 16px;
  --sp-lg: 32px;
  --sp-xl: 64px;
  --sp-2xl: 96px;

  /* Type scale */
  --fs-xs:   0.75rem;
  --fs-sm:   0.875rem;
  --fs-base: 1rem;
  --fs-md:   1.0625rem;
  --fs-lg:   1.25rem;
  --fs-xl:   1.5rem;
  --fs-2xl:  2rem;
  --fs-3xl:  2.75rem;
  --fs-4xl:  3.75rem;
  --fs-hero: clamp(2.8rem, 6vw, 5rem);
}

/* ---- Reset & base ---- */

*, *::before, *::after { box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  scroll-padding-top: 24px;
  -webkit-text-size-adjust: 100%;
}

body {
  font-family: 'Lora', Georgia, 'Times New Roman', serif;
  font-size: 18px;
  line-height: 1.75;
  font-weight: 400;
  color: var(--ink);
  background-color: var(--bg);
  margin: 0;
  padding: 0;
  /* Subtle warm grain — dark version: lower opacity, sepia noise */
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
}

/* ---- Layout ---- */

.container {
  max-width: 780px;
  margin: 0 auto;
  padding: var(--sp-xl) var(--sp-lg);
}

/* ---- ARCHIVE MASTHEAD ---- */

header.cover {
  position: relative;
  text-align: center;
  padding: var(--sp-xl) var(--sp-lg) var(--sp-lg);
  margin: 0 calc(-1 * var(--sp-lg)) var(--sp-lg);
  background:
    linear-gradient(180deg, rgba(26, 20, 14, 0.96) 0%, rgba(15, 12, 9, 0.98) 100%),
    repeating-linear-gradient(90deg, transparent, transparent 31px, rgba(212, 164, 88, 0.025) 32px);
  border-bottom: 1px solid var(--rule);
  box-shadow:
    inset 0 -1px 0 rgba(212, 164, 88, 0.08),
    0 8px 28px rgba(0,0,0,0.32);
  overflow: hidden;
}

header.cover::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent 0%,
    #a07840 15%,
    var(--accent-gold) 40%,
    #e8c070 50%,
    var(--accent-gold) 60%,
    #a07840 85%,
    transparent 100%);
}

header.cover::after {
  content: '';
  position: absolute;
  inset: 16px;
  border: 1px solid rgba(212, 164, 88, 0.12);
  pointer-events: none;
}

.cover-eyebrow {
  font-family: 'Lora', Georgia, serif;
  font-size: var(--fs-sm);
  font-style: italic;
  letter-spacing: 0.18em;
  color: var(--ink-soft);
  text-transform: uppercase;
  margin: 0 0 var(--sp-md);
  opacity: 0.8;
}

header.cover h1 {
  font-family: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  font-weight: 700;
  font-size: clamp(2.4rem, 5vw, 3.8rem);
  line-height: 1.05;
  margin: 0 0 var(--sp-sm);
  color: #f0e6d2;
  letter-spacing: 0;
  text-wrap: balance;
  text-shadow: 0 2px 4px rgba(0,0,0,0.6);
}

header.cover h1 em {
  font-style: italic;
  color: var(--accent-gold);
}

.cover-ornament {
  display: block;
  text-align: center;
  font-size: 1.5em;
  color: var(--accent-gold);
  margin: var(--sp-md) 0;
  letter-spacing: 0.4em;
  opacity: 0.5;
  user-select: none;
}

header.cover .subtitle {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  color: var(--ink-mid);
  font-size: var(--fs-lg);
  margin: 0 0 var(--sp-sm);
  font-weight: 400;
  letter-spacing: 0.02em;
}

header.cover .cover-rule {
  width: 80px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
  margin: var(--sp-md) auto;
  border: none;
  opacity: 0.6;
}

header.cover .meta {
  color: var(--ink-ghost);
  font-size: var(--fs-sm);
  line-height: 1.9;
  margin-top: var(--sp-sm);
  letter-spacing: 0.01em;
}

header.cover .meta strong {
  color: var(--ink-soft);
}

/* Audio player — brass-trimmed tape control */
.audio-wrapper {
  margin: var(--sp-lg) auto 0;
  max-width: 520px;
  /* Warm metallic casing */
  background: linear-gradient(180deg,
    rgba(40, 32, 22, 0.92) 0%,
    rgba(28, 22, 14, 0.95) 100%
  );
  border: 1px solid rgba(180, 130, 70, 0.35);
  border-top: 1px solid rgba(212, 164, 88, 0.5);
  border-radius: 8px;
  padding: 10px 14px;
  box-shadow:
    0 4px 20px rgba(0,0,0,0.5),
    inset 0 1px 0 rgba(212, 164, 88, 0.15),
    inset 0 -1px 0 rgba(0,0,0,0.3);
}

.cover-particles,
header.cover .cover-glow {
  display: none;
}

audio {
  width: 100%;
  display: block;
  height: 40px;
  /* Tint the native controls to work on dark */
  filter: invert(0.85) sepia(0.3) hue-rotate(10deg) brightness(0.95);
}

/* Remove default audio styling where we can */
audio::-webkit-media-controls-panel {
  background: transparent;
}

/* ---- Table of Contents ---- */

nav.toc {
  background: var(--paper-raised);
  border: 1px solid var(--rule);
  border-top: 2px solid var(--accent-gold-light);
  border-radius: 0 0 6px 6px;
  padding: var(--sp-md) var(--sp-lg);
  margin-bottom: var(--sp-xl);
  box-shadow: 0 4px 16px rgba(0,0,0,0.35);
}

nav.toc strong {
  display: block;
  margin-bottom: var(--sp-sm);
  font-size: var(--fs-xs);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-ghost);
  font-family: 'Lora', Georgia, serif;
}

nav.toc ul {
  list-style: none;
  padding: 0;
  margin: 0;
  columns: 2;
  column-gap: var(--sp-lg);
}

nav.toc li {
  padding: 3px 0;
  break-inside: avoid;
}

nav.toc a {
  font-size: var(--fs-sm);
  color: var(--ink-soft);
  text-decoration: none;
  border-bottom: 1px dotted var(--rule);
  transition: color 0.15s, border-bottom-color 0.15s;
}

nav.toc a:hover {
  color: var(--accent-gold);
  border-bottom-color: var(--accent-gold);
}

/* ---- Section headings ---- */

h2 {
  font-family: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  font-weight: 600;
  font-size: var(--fs-3xl);
  margin: var(--sp-2xl) 0 var(--sp-lg);
  color: #f0e6d2;
  letter-spacing: 0;
  line-height: 1.1;
  position: relative;
  padding-bottom: var(--sp-md);
}

h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 48px;
  height: 1px;
  background: linear-gradient(90deg, var(--accent-gold), transparent);
}

h3 {
  font-family: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  font-weight: 600;
  font-size: var(--fs-xl);
  margin: var(--sp-lg) 0 var(--sp-sm);
  color: var(--ink-mid);
  letter-spacing: 0.01em;
}

p { margin: 0 0 1em; }

/* ---- Transcript ---- */

#transcript > p {
  font-style: italic;
  color: var(--ink-ghost);
  font-size: var(--fs-sm);
  margin-bottom: var(--sp-xl);
}

.transcript-turn {
  margin: 0;
  padding: var(--sp-md) 0;
  border-bottom: 1px solid var(--rule);
  position: relative;
}

.transcript-turn:last-child { border-bottom: none; }

.speaker-line {
  display: flex;
  align-items: baseline;
  gap: var(--sp-sm);
  margin-bottom: 6px;
}

.transcript-turn .speaker-shari {
  font-family: 'Lora', Georgia, serif;
  color: var(--shari-color);
  font-weight: 600;
  font-size: var(--fs-xs);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.transcript-turn .speaker-hunter {
  font-family: 'Lora', Georgia, serif;
  color: var(--hunter-color);
  font-weight: 600;
  font-size: var(--fs-xs);
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.transcript-turn .timestamp {
  color: var(--ink-ghost);
  font-size: var(--fs-xs);
  font-family: 'Source Code Pro', 'Courier New', monospace;
  opacity: 0.6;
}

.transcript-turn .text {
  color: var(--ink);
  font-size: var(--fs-md);
  line-height: 1.85;
}

/* Drop cap — illuminated manuscript style, gold on dark — v3: enlarged & more dramatic */
.transcript-turn:first-child .text p:first-child::first-letter {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 5.8em;
  font-weight: 700;
  float: left;
  line-height: 0.72;
  margin: 0.04em 0.12em 0 -0.06em;
  color: var(--accent-gold);
  text-shadow:
    0 0 30px rgba(212, 164, 88, 0.55),
    0 0 60px rgba(212, 164, 88, 0.2),
    2px 3px 8px rgba(0,0,0,0.7);
  /* Faint inner gold border effect via filter */
  filter: drop-shadow(0 0 2px rgba(212, 164, 88, 0.6));
}

/* Hunter's turns — recessed into background, interjection feel */
.transcript-turn-hunter {
  background: rgba(255, 255, 255, 0.015);
  padding-left: var(--sp-md);
  border-left: 2px solid var(--rule);
  border-bottom: 1px solid transparent;
}

.transcript-turn-hunter .text {
  color: var(--ink-soft);
  font-size: 0.95em;
  font-style: italic;
}

/* Pull-quote — the memorable moment glowing on dark */
.pull-quote {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: var(--fs-2xl);
  line-height: 1.35;
  color: var(--accent-gold);
  text-align: center;
  padding: var(--sp-xl) var(--sp-lg);
  margin: var(--sp-xl) 0;
  border-top: 1px solid rgba(212, 164, 88, 0.2);
  border-bottom: 1px solid rgba(212, 164, 88, 0.2);
  position: relative;
  /* Subtle warm glow around the pull-quote block */
  text-shadow: 0 0 40px rgba(212, 164, 88, 0.15);
}

.pull-quote::before {
  content: '\201C';
  position: absolute;
  top: -0.15em;
  left: var(--sp-md);
  font-size: 4em;
  color: var(--accent-gold-light);
  line-height: 1;
  font-family: 'Cormorant Garamond', Georgia, serif;
  opacity: 0.4;
}

/* ---- Entity links & cards ---- */

.entity-link {
  color: var(--accent-warm);
  text-decoration: none;
  border-bottom: 1px solid rgba(180, 120, 60, 0.4);
  cursor: help;
  white-space: nowrap;
  transition: color 0.15s, border-bottom-color 0.15s;
}

.entity-link:hover {
  color: var(--accent-gold);
  border-bottom-color: var(--accent-gold);
}

details.entity-card {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent-gold-light);
  border-radius: 0 4px 4px 0;
  padding: var(--sp-md) var(--sp-lg);
  margin: var(--sp-sm) 0;
  transition: border-left-color 0.2s, box-shadow 0.2s;
}

details.entity-card[open] {
  border-left-color: var(--accent-gold);
  box-shadow: -3px 0 12px rgba(212, 164, 88, 0.08), 0 4px 16px rgba(0,0,0,0.3);
}

details.entity-card summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--ink);
  font-size: 1.0em;
  padding: 2px 0;
  list-style: none;
  display: flex;
  align-items: center;
  gap: var(--sp-sm);
}

details.entity-card summary::-webkit-details-marker { display: none; }

details.entity-card summary::before {
  content: "";
  display: inline-block;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 5px 0 5px 8px;
  border-color: transparent transparent transparent var(--accent-gold-light);
  flex-shrink: 0;
  transition: transform 0.15s;
}

details.entity-card[open] summary::before {
  transform: rotate(90deg);
  border-color: transparent transparent transparent var(--accent-gold);
}

details.entity-card .entity-meta {
  font-size: var(--fs-sm);
  color: var(--ink-soft);
  margin-top: var(--sp-sm);
  font-style: italic;
}

details.entity-card .entity-body {
  margin-top: var(--sp-sm);
  font-size: 0.95em;
}

/* Confidence badges — dark mode versions */
.confidence {
  display: inline-block;
  font-size: var(--fs-xs);
  padding: 2px 7px;
  border-radius: 3px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-family: 'Lora', Georgia, serif;
  margin-left: var(--sp-sm);
}

.confidence-confirmed { background: rgba(74, 138, 90, 0.15); color: var(--confirmed); border: 1px solid rgba(74, 138, 90, 0.3); }
.confidence-probable  { background: rgba(200, 160, 80, 0.15); color: var(--probable); border: 1px solid rgba(200, 160, 80, 0.3); }
.confidence-possible  { background: rgba(200, 112, 96, 0.15); color: var(--possible); border: 1px solid rgba(200, 112, 96, 0.3); }
.confidence-living    { background: rgba(122, 154, 184, 0.15); color: var(--living); border: 1px solid rgba(122, 154, 184, 0.3); }

.entity-links {
  margin-top: var(--sp-sm);
  font-size: var(--fs-sm);
}

.entity-links a {
  color: var(--accent-warm);
  margin-right: var(--sp-md);
  text-decoration: none;
  border-bottom: 1px solid rgba(160, 100, 60, 0.35);
}

.entity-links a:hover {
  color: var(--accent-gold);
  border-bottom-color: var(--accent-gold);
}

/* ---- Callout / open questions ---- */

.callout {
  background: rgba(212, 164, 88, 0.06);
  border-left: 3px solid var(--accent-gold-light);
  padding: var(--sp-md) var(--sp-lg);
  margin: var(--sp-lg) 0;
  border-radius: 0 4px 4px 0;
}

.callout strong { color: var(--accent-gold); }
.callout ul { margin: var(--sp-sm) 0 0; padding-left: var(--sp-lg); }
.callout li { margin-bottom: var(--sp-xs); color: var(--ink-soft); }

/* ---- Research sections ---- */

.research-section {
  background: var(--paper-raised);
  border: 1px solid var(--rule);
  border-top: 1px solid rgba(212, 164, 88, 0.2);
  border-radius: 4px;
  margin: var(--sp-md) 0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  overflow: hidden;
}

.research-library {
  margin-top: var(--sp-lg);
}

.research-group-heading {
  margin: var(--sp-xl) 0 var(--sp-sm);
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: var(--fs-xl);
  font-weight: 700;
  color: var(--accent-gold);
}

.research-group-heading:first-child {
  margin-top: var(--sp-lg);
}

.research-section summary {
  cursor: pointer;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 6px var(--sp-md);
  align-items: baseline;
  padding: var(--sp-md) var(--sp-lg);
  list-style: none;
}

.research-section summary::-webkit-details-marker { display: none; }

.research-section summary::before {
  content: "";
  grid-row: 1 / span 2;
  width: 0;
  height: 0;
  margin-top: 0.45em;
  border-style: solid;
  border-width: 5px 0 5px 8px;
  border-color: transparent transparent transparent var(--accent-gold-light);
  transition: transform 0.15s;
}

.research-section[open] summary::before {
  transform: rotate(90deg);
  border-color: transparent transparent transparent var(--accent-gold);
}

.research-number {
  font-family: 'Source Code Pro', 'Courier New', monospace;
  font-size: var(--fs-xs);
  letter-spacing: 0.08em;
  color: var(--accent-gold-light);
}

.research-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: var(--fs-lg);
  font-weight: 700;
  color: #f0e6d2;
  line-height: 1.2;
}

.research-size {
  justify-self: end;
  font-family: 'Source Code Pro', 'Courier New', monospace;
  font-size: var(--fs-xs);
  color: var(--ink-ghost);
  white-space: nowrap;
}

.research-excerpt {
  grid-column: 2 / 4;
  margin: 0;
  color: var(--ink-soft);
  font-size: var(--fs-sm);
  line-height: 1.55;
}

.research-body {
  padding: 0 var(--sp-lg) var(--sp-lg);
  border-top: 1px solid rgba(212, 164, 88, 0.08);
}

.research-body h2:first-child,
.research-body h3:first-child {
  margin-top: var(--sp-md);
}

.research-section h3 { margin-top: var(--sp-lg); }
.research-section ul { padding-left: var(--sp-lg); }
.research-section li { margin-bottom: var(--sp-xs); }

/* ---- Timeline & Map ---- */

#timeline-container {
  height: 360px;
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 4px;
  margin: var(--sp-lg) 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

/* vis-timeline dark overrides */
#timeline-container .vis-timeline {
  background: var(--paper);
  border-color: var(--rule);
}

#timeline-container .vis-panel.vis-center,
#timeline-container .vis-panel.vis-left,
#timeline-container .vis-panel.vis-right,
#timeline-container .vis-panel.vis-top,
#timeline-container .vis-panel.vis-bottom {
  border-color: var(--rule);
}

#timeline-container .vis-time-axis .vis-text {
  color: var(--ink-ghost);
  font-family: 'Source Code Pro', monospace;
  font-size: 11px;
}

#timeline-container .vis-time-axis .vis-grid.vis-minor,
#timeline-container .vis-time-axis .vis-grid.vis-major {
  border-color: rgba(255,255,255,0.04);
}

#timeline-container .vis-label {
  background: var(--paper-raised);
  color: var(--ink-soft);
  font-size: 11px;
  border-color: var(--rule);
}

#timeline-container .vis-item {
  background: rgba(212, 164, 88, 0.18);
  border-color: var(--accent-gold-light);
  color: var(--ink);
  font-size: 11px;
  font-family: 'Lora', Georgia, serif;
  border-radius: 2px;
}

#timeline-container .vis-item.vis-selected {
  background: rgba(212, 164, 88, 0.35);
  border-color: var(--accent-gold);
}

#timeline-container .vis-current-time {
  background: var(--accent-gold);
  opacity: 0.4;
}

#map-container {
  height: 440px;
  background: #1a1814;
  border: 1px solid var(--rule);
  border-radius: 4px;
  margin: var(--sp-lg) 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

/* Leaflet dark popup */
#map-container .leaflet-popup-content-wrapper {
  background: var(--paper-raised);
  color: var(--ink);
  border: 1px solid var(--rule);
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

#map-container .leaflet-popup-tip {
  background: var(--paper-raised);
}

#map-container .leaflet-popup-content strong {
  color: var(--accent-gold);
}

#map-container .leaflet-control-zoom a {
  background: var(--paper-raised);
  color: var(--ink);
  border-color: var(--rule);
}

#map-container .leaflet-control-zoom a:hover {
  background: var(--paper);
  color: var(--accent-gold);
}

#map-container .leaflet-control-attribution {
  background: rgba(13, 10, 8, 0.8);
  color: var(--ink-ghost);
  font-size: 10px;
}

#map-container .leaflet-control-attribution a {
  color: var(--ink-ghost);
}

/* ---- D3 LINEAGE TREE ---- */

/* The tree gets a full-bleed dark background, wider than the text column */
#lineage-section {
  /* Break out of the .container max-width so the wide branching tree gets real estate.
     Span full viewport width using the negative-margin trick. */
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  padding: 0 max(var(--sp-lg), calc((100vw - 1600px) / 2));
}

#lineage-tree-container {
  position: relative;
  /* Dark starfield-like background — deep space for the family constellation */
  background:
    radial-gradient(ellipse 60% 40% at 50% 10%, rgba(212,164,88,0.04) 0%, transparent 70%),
    linear-gradient(175deg, #0f0c09 0%, #0c0a07 55%, #090705 100%);
  border: 1px solid var(--rule);
  border-top: 1px solid rgba(212, 164, 88, 0.15);
  border-radius: 6px;
  margin: var(--sp-lg) 0;
  overflow: hidden;
  box-shadow:
    0 8px 40px rgba(0,0,0,0.6),
    inset 0 1px 0 rgba(212, 164, 88, 0.08);
}

/* Faint horizontal grid lines — archival ledger feel */
#lineage-tree-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(
    0deg, transparent, transparent 59px,
    rgba(212, 164, 88, 0.04) 60px
  );
  pointer-events: none;
  z-index: 0;
}

#lineage-tree-svg {
  display: block;
  width: 100%;
  height: auto;
  min-height: 720px;
  cursor: grab;
  position: relative;
  z-index: 1;
}

#lineage-tree-svg:active { cursor: grabbing; }

/* ── Enhanced entity (cast) cards ────────────────────────────────── */

.entity-card {
  background: linear-gradient(170deg, rgba(20,16,11,0.55), rgba(15,12,9,0.7));
  border: 1px solid rgba(212, 164, 88, 0.10);
  border-left: 3px solid var(--gold);
  border-radius: 4px;
  margin: 16px 0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.25);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.entity-card[open] {
  border-left-color: #e8c280;
  box-shadow: 0 6px 24px rgba(0,0,0,0.4), 0 0 16px rgba(212, 164, 88, 0.04);
}

.entity-card summary {
  list-style: none;
  cursor: pointer;
  padding: 14px 22px;
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 8px 16px;
  border-bottom: 1px dashed rgba(212, 164, 88, 0.08);
}
.entity-card summary::-webkit-details-marker { display: none; }
.entity-card[open] summary { border-bottom-color: rgba(212, 164, 88, 0.18); }

.entity-summary-name {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-weight: 700;
  font-size: 1.3em;
  color: var(--ink-bright);
  letter-spacing: 0.005em;
  flex-grow: 1;
}
.entity-summary-meta {
  font-family: 'Source Code Pro', monospace;
  font-size: 0.78em;
  color: var(--gold-soft);
  letter-spacing: 0.05em;
  white-space: nowrap;
}
.entity-summary-sub {
  width: 100%;
  font-style: italic;
  font-size: 0.92em;
  color: var(--ink-soft);
  margin-top: 4px;
}

.entity-body {
  padding: 18px 22px 20px;
  position: relative;
}

.entity-portrait-wrap {
  float: right;
  margin: 0 0 16px 20px;
  text-align: center;
  max-width: 180px;
}
.entity-portrait {
  width: 160px;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid var(--gold-soft);
  box-shadow: 0 4px 16px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,0,0,0.4);
  background: #0a0805;
}
.portrait-caption {
  font-size: 0.72em;
  color: var(--ink-soft);
  font-style: italic;
  margin-top: 6px;
  line-height: 1.3;
}

table.vital-stats {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 14px;
  font-size: 0.95em;
}
table.vital-stats th {
  text-align: left;
  width: 28%;
  padding: 4px 12px 4px 0;
  font-family: 'Source Code Pro', monospace;
  font-size: 0.78em;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--gold-soft);
  vertical-align: top;
}
table.vital-stats td {
  padding: 4px 0;
  color: var(--ink);
  vertical-align: top;
}

p.entity-bio {
  line-height: 1.7;
  margin: 8px 0 12px;
  color: var(--ink);
}

.notable-deed-callout {
  background: linear-gradient(150deg, rgba(212,164,88,0.08), rgba(184,130,106,0.04));
  border-left: 2px solid var(--gold);
  border-radius: 0 4px 4px 0;
  padding: 14px 18px;
  margin: 16px 0;
  position: relative;
  clear: both;
}
.notable-deed-label {
  font-family: 'Source Code Pro', monospace;
  font-size: 0.72em;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 4px;
}
.notable-deed-headline {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 1.05em;
  color: var(--ink-bright);
  margin-bottom: 6px;
  line-height: 1.4;
}
.notable-deed-story {
  font-size: 0.95em;
  line-height: 1.65;
  margin: 0;
  color: var(--ink);
}

.entity-links-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  clear: both;
  padding-top: 14px;
  border-top: 1px dashed rgba(212, 164, 88, 0.08);
}
.ext-link {
  display: inline-block;
  padding: 5px 12px;
  background: rgba(212, 164, 88, 0.08);
  border: 1px solid rgba(212, 164, 88, 0.22);
  border-radius: 14px;
  color: var(--gold);
  font-family: 'Source Code Pro', monospace;
  font-size: 0.78em;
  letter-spacing: 0.04em;
  text-decoration: none;
  transition: background 0.15s, border-color 0.15s;
}
.ext-link:hover {
  background: rgba(212, 164, 88, 0.16);
  border-color: var(--gold);
}
.ext-link.wiki-link { background: rgba(212, 164, 88, 0.14); }

@media (max-width: 600px) {
  .entity-portrait-wrap { float: none; margin: 0 auto 16px; }
  .entity-portrait { width: 120px; height: 150px; }
  table.vital-stats th { width: 36%; font-size: 0.72em; }
}

/* ── Notable Stories cards ───────────────────────────────────────── */

.story-era-heading {
  font-family: 'Cormorant Garamond', 'Lora', Georgia, serif;
  font-style: italic;
  font-weight: 600;
  font-size: 1.4em;
  color: var(--gold);
  margin: 48px 0 16px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(212, 164, 88, 0.18);
  letter-spacing: 0.01em;
}

.story-era-heading:first-of-type { margin-top: 8px; }

.story-card {
  background: linear-gradient(170deg, rgba(20,16,11,0.55), rgba(15,12,9,0.7));
  border: 1px solid rgba(212, 164, 88, 0.12);
  border-left: 3px solid var(--gold);
  border-radius: 4px;
  padding: 22px 26px;
  margin: 18px 0;
  position: relative;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  transition: border-left-color 0.2s, box-shadow 0.2s;
}

.story-card:hover {
  border-left-color: #e8c280;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 24px rgba(212, 164, 88, 0.06);
}

.story-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px dashed rgba(212, 164, 88, 0.08);
}

.story-name {
  font-family: 'Cormorant Garamond', 'Lora', Georgia, serif;
  font-size: 1.45em;
  font-weight: 700;
  color: var(--ink-bright);
  letter-spacing: 0.01em;
}

.story-meta {
  font-family: 'Source Code Pro', monospace;
  font-size: 0.78em;
  color: var(--gold-soft);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  white-space: nowrap;
}

.story-headline {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-weight: 600;
  font-size: 1.1em;
  color: var(--gold);
  margin: 6px 0 10px;
  line-height: 1.4;
}

.story-body {
  color: var(--ink);
  font-size: 1em;
  line-height: 1.75;
  margin: 0;
}

.story-sources {
  margin-top: 14px;
  font-family: 'Source Code Pro', monospace;
  font-size: 0.78em;
  color: var(--gold-soft);
  letter-spacing: 0.04em;
}

.story-sources a {
  color: var(--gold);
  text-decoration: none;
  border-bottom: 1px dotted var(--gold-soft);
}

.story-sources a:hover { border-bottom-style: solid; }

#stories > p {
  font-style: italic;
  color: var(--ink-soft);
  margin-bottom: 32px;
}

/* Node animations — animate opacity ONLY because setting CSS `transform`
   on an SVG element overrides the SVG `transform="translate(x,y)"`
   attribute, which would slam every node to the same position. */
@keyframes nodeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.tree-node {
  animation: nodeIn 0.4s ease both;
}

/* Stagger by generation depth */
.tree-node.gen-0  { animation-delay: 0.0s; }
.tree-node.gen-1  { animation-delay: 0.06s; }
.tree-node.gen-2  { animation-delay: 0.12s; }
.tree-node.gen-3  { animation-delay: 0.18s; }
.tree-node.gen-4  { animation-delay: 0.24s; }
.tree-node.gen-5  { animation-delay: 0.30s; }
.tree-node.gen-6  { animation-delay: 0.36s; }
.tree-node.gen-7  { animation-delay: 0.42s; }
.tree-node.gen-8  { animation-delay: 0.48s; }
.tree-node.gen-9  { animation-delay: 0.54s; }
.tree-node.gen-10 { animation-delay: 0.60s; }
.tree-node.gen-11 { animation-delay: 0.66s; }
.tree-node.gen-12 { animation-delay: 0.72s; }
.tree-node.gen-13 { animation-delay: 0.78s; }

.tree-node text { user-select: none; pointer-events: none; }

.tree-node .node-card {
  transition: filter 0.2s, transform 0.2s;
  transform-origin: center;
}

.tree-node:hover .node-card {
  /* Gold halo on dark — the node illuminates */
  filter: drop-shadow(0 0 8px rgba(212, 164, 88, 0.35)) drop-shadow(0 4px 16px rgba(0,0,0,0.6));
  transform: scale(1.025);
}

.tree-node:focus-within .node-card,
.tree-node:focus .node-card {
  outline: 2px solid var(--accent-gold);
  outline-offset: 3px;
}

/* Secondary family-line visual trees */
#secondary-trees {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin: var(--sp-2xl) -50vw 0;
  padding: 0 max(var(--sp-lg), calc((100vw - 1500px) / 2));
}

#secondary-trees > h2,
#secondary-trees > p,
.secondary-line-tabs {
  max-width: 980px;
  margin-left: auto;
  margin-right: auto;
}

#secondary-trees > p {
  color: var(--ink-soft);
}

.secondary-line-tabs {
  display: flex;
  gap: var(--sp-sm);
  overflow-x: auto;
  padding: var(--sp-sm) 0 var(--sp-md);
  margin-top: var(--sp-md);
  margin-bottom: var(--sp-md);
  scrollbar-color: var(--accent-gold-light) transparent;
}

.secondary-line-tabs a {
  flex: 0 0 auto;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 12px;
  border: 1px solid rgba(212, 164, 88, 0.16);
  border-radius: 6px;
  background: rgba(22, 18, 14, 0.88);
  color: var(--ink-soft);
  font-size: var(--fs-xs);
  line-height: 1.25;
  text-decoration: none;
  white-space: nowrap;
}

.secondary-line-tabs a:hover {
  color: var(--accent-gold);
  border-color: rgba(212, 164, 88, 0.45);
  background: rgba(40, 31, 20, 0.88);
}

.secondary-line-tabs .line-number {
  font-family: 'Source Code Pro', 'Courier New', monospace;
  color: var(--accent-gold-light);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.secondary-tree-list {
  display: grid;
  gap: var(--sp-lg);
}

.secondary-tree-card {
  background:
    linear-gradient(180deg, rgba(25, 20, 15, 0.96), rgba(14, 11, 8, 0.98)),
    repeating-linear-gradient(0deg, transparent, transparent 55px, rgba(212,164,88,0.025) 56px);
  border: 1px solid rgba(212, 164, 88, 0.14);
  border-radius: 7px;
  box-shadow:
    0 10px 32px rgba(0,0,0,0.42),
    inset 0 1px 0 rgba(212, 164, 88, 0.08);
  overflow: hidden;
}

.secondary-tree-card:target {
  border-color: rgba(212, 164, 88, 0.42);
  box-shadow:
    0 14px 42px rgba(0,0,0,0.55),
    0 0 0 1px rgba(212, 164, 88, 0.18),
    inset 0 1px 0 rgba(212, 164, 88, 0.08);
}

.secondary-tree-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: var(--sp-md);
  align-items: start;
  padding: var(--sp-md) var(--sp-lg);
  border-bottom: 1px solid rgba(212, 164, 88, 0.10);
}

.secondary-tree-kicker {
  margin: 0 0 4px;
  font-family: 'Source Code Pro', 'Courier New', monospace;
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-gold-light);
}

.secondary-tree-card h3 {
  margin: 0;
  font-family: 'Cormorant Garamond', 'Lora', Georgia, serif;
  font-size: clamp(1.25rem, 2vw, 1.75rem);
  font-weight: 700;
  line-height: 1.16;
  color: #f0e6d2;
}

.secondary-tree-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
  min-width: 240px;
}

.secondary-tree-meta span {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 4px 8px;
  border: 1px solid rgba(212, 164, 88, 0.13);
  border-radius: 5px;
  background: rgba(0,0,0,0.18);
  color: var(--ink-ghost);
  font-family: 'Source Code Pro', 'Courier New', monospace;
  font-size: 0.68rem;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.secondary-tree-toolbar {
  padding: var(--sp-sm) var(--sp-lg);
  margin-bottom: 0;
  border-bottom: 1px solid rgba(212, 164, 88, 0.08);
  background: rgba(0,0,0,0.12);
}

.secondary-tree-container {
  position: relative;
  min-height: 430px;
  overflow: hidden;
  background:
    radial-gradient(ellipse 70% 50% at 50% 8%, rgba(212,164,88,0.035), transparent 70%),
    linear-gradient(180deg, rgba(12,10,8,0.55), rgba(8,7,6,0.8));
}

.secondary-tree-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 59px, rgba(212,164,88,0.035) 60px),
    repeating-linear-gradient(90deg, transparent, transparent 79px, rgba(212,164,88,0.02) 80px);
  pointer-events: none;
  z-index: 0;
}

.secondary-tree-svg {
  display: block;
  width: 100%;
  height: min(68vh, 680px);
  min-height: 430px;
  position: relative;
  z-index: 1;
  cursor: grab;
}

.secondary-tree-svg:active {
  cursor: grabbing;
}

.secondary-tree-card .tree-hint {
  margin: 0;
  padding: var(--sp-sm) var(--sp-lg) var(--sp-md);
  border-top: 1px solid rgba(212, 164, 88, 0.08);
  background: rgba(0,0,0,0.14);
}

/* Tree toolbar */
.tree-toolbar {
  display: flex;
  align-items: center;
  gap: var(--sp-sm);
  margin-bottom: var(--sp-sm);
  flex-wrap: wrap;
}

.tree-toolbar .btn-group {
  display: flex;
  gap: 1px;
  background: var(--rule);
  border-radius: 5px;
  overflow: hidden;
}

.tree-toolbar button {
  background: var(--paper-raised);
  color: var(--ink-soft);
  border: none;
  padding: 9px 14px;
  font-family: 'Lora', Georgia, serif;
  font-size: var(--fs-sm);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  line-height: 1;
  min-width: 44px;
  min-height: 44px;
}

.tree-toolbar button:hover {
  background: rgba(212, 164, 88, 0.2);
  color: var(--accent-gold);
}

.tree-toolbar button:first-child { border-radius: 5px 0 0 5px; }
.tree-toolbar button:last-child  { border-radius: 0 5px 5px 0; }

.tree-toolbar .tree-legend {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-md);
  margin-left: auto;
  font-size: var(--fs-xs);
  color: var(--ink-ghost);
  align-items: center;
}

.tree-toolbar .legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.tree-toolbar .swatch {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  border: 1.5px solid;
}

.tree-toolbar .swatch.confirmed { background: rgba(180, 130, 60, 0.4); border-color: var(--accent-gold); }
.tree-toolbar .swatch.probable  { background: rgba(160, 100, 60, 0.3); border-color: var(--accent-bronze); }
.tree-toolbar .swatch.unknown   { background: rgba(80, 70, 60, 0.3); border-color: var(--ink-ghost); border-style: dashed; }

.tree-hint {
  font-size: var(--fs-xs);
  color: var(--ink-ghost);
  font-style: italic;
  text-align: center;
  margin-top: var(--sp-sm);
  opacity: 0.7;
}

/* Respects prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .tree-node { animation: none; }
}

/* ---- Footer ---- */

footer.colophon {
  margin-top: var(--sp-2xl);
  padding: var(--sp-lg) 0 var(--sp-xl);
  border-top: 1px solid var(--rule);
  font-size: var(--fs-xs);
  color: var(--ink-ghost);
  text-align: center;
  line-height: 1.9;
  opacity: 0.7;
}

footer.colophon code {
  font-family: 'Source Code Pro', 'Courier New', monospace;
  font-size: 0.95em;
  background: var(--paper);
  color: var(--ink-soft);
  padding: 1px 5px;
  border-radius: 3px;
  border: 1px solid var(--rule);
}

/* ---- Utility ---- */

.redacted {
  background: var(--ink-ghost);
  color: var(--ink-ghost);
  border-radius: 2px;
  user-select: none;
}

/* =========================================================
   HERO CINEMATIC PARTICLES  (v3)
   Floating dust motes — CSS animation only, no JS
   ========================================================= */

.cover-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.cover-particles span {
  position: absolute;
  display: block;
  background: rgba(212, 164, 88, 0.55);
  border-radius: 50%;
  animation: particleDrift linear infinite;
}

/* 16 particles with staggered sizes, positions, durations */
.cover-particles span:nth-child(1)  { width: 2px; height: 2px; left: 10%; animation-duration: 18s; animation-delay:  0s; }
.cover-particles span:nth-child(2)  { width: 3px; height: 3px; left: 22%; animation-duration: 24s; animation-delay: -7s; opacity: 0.4; }
.cover-particles span:nth-child(3)  { width: 2px; height: 2px; left: 35%; animation-duration: 20s; animation-delay: -3s; opacity: 0.6; }
.cover-particles span:nth-child(4)  { width: 1px; height: 1px; left: 48%; animation-duration: 16s; animation-delay: -12s; }
.cover-particles span:nth-child(5)  { width: 3px; height: 3px; left: 58%; animation-duration: 22s; animation-delay:  -5s; opacity: 0.35; }
.cover-particles span:nth-child(6)  { width: 2px; height: 2px; left: 70%; animation-duration: 19s; animation-delay: -9s; }
.cover-particles span:nth-child(7)  { width: 1px; height: 1px; left: 82%; animation-duration: 25s; animation-delay: -2s; opacity: 0.5; }
.cover-particles span:nth-child(8)  { width: 4px; height: 4px; left: 92%; animation-duration: 28s; animation-delay: -14s; opacity: 0.25; }
.cover-particles span:nth-child(9)  { width: 2px; height: 2px; left: 15%; animation-duration: 21s; animation-delay: -6s; opacity: 0.7; }
.cover-particles span:nth-child(10) { width: 1px; height: 1px; left: 42%; animation-duration: 17s; animation-delay: -10s; }
.cover-particles span:nth-child(11) { width: 3px; height: 3px; left: 63%; animation-duration: 23s; animation-delay: -4s; opacity: 0.45; }
.cover-particles span:nth-child(12) { width: 2px; height: 2px; left: 77%; animation-duration: 20s; animation-delay: -8s; opacity: 0.6; }
.cover-particles span:nth-child(13) { width: 1px; height: 1px; left: 88%; animation-duration: 15s; animation-delay: -1s; }
.cover-particles span:nth-child(14) { width: 2px; height: 2px; left:  5%; animation-duration: 26s; animation-delay: -15s; opacity: 0.4; }
.cover-particles span:nth-child(15) { width: 3px; height: 3px; left: 30%; animation-duration: 30s; animation-delay: -11s; opacity: 0.3; }
.cover-particles span:nth-child(16) { width: 1px; height: 1px; left: 55%; animation-duration: 18s; animation-delay: -16s; opacity: 0.65; }

@keyframes particleDrift {
  0%   { transform: translateY(120%) translateX(0) scale(0.8); opacity: 0; }
  10%  { opacity: 1; }
  50%  { transform: translateY(40%) translateX(15px) scale(1); }
  90%  { opacity: 0.8; }
  100% { transform: translateY(-20%) translateX(-10px) scale(1.1); opacity: 0; }
}

/* Animated gradient shimmer behind the hero title */
@keyframes heroGlow {
  0%, 100% { opacity: 0.04; }
  50%       { opacity: 0.10; }
}

header.cover .cover-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 55% 60% at 50% 55%, #d4a458 0%, transparent 70%);
  animation: heroGlow 6s ease-in-out infinite;
  pointer-events: none;
  z-index: 0;
}

header.cover > *:not(.cover-particles):not(.cover-glow) {
  position: relative;
  z-index: 1;
}

/* =========================================================
   PORTRAIT CARDS IN ENTITY DETAILS  (v3)
   ========================================================= */

.entity-portrait-wrap {
  float: right;
  margin: 0 0 var(--sp-md) var(--sp-md);
  clear: right;
}

.entity-portrait {
  display: block;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 2px solid var(--accent-gold);
  box-shadow:
    0 0 0 4px rgba(212, 164, 88, 0.12),
    0 4px 20px rgba(0,0,0,0.6),
    inset 0 0 8px rgba(0,0,0,0.4);
  object-fit: cover;
  overflow: hidden;
  background: var(--paper-raised);
}

.entity-portrait-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 1px dashed rgba(212, 164, 88, 0.25);
  background: var(--paper-raised);
  color: var(--ink-ghost);
  font-size: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

/* Notable Achievements sub-section in entity cards */
.entity-deeds {
  margin-top: var(--sp-md);
  padding-top: var(--sp-sm);
  border-top: 1px solid var(--rule);
}

.entity-deeds-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: var(--fs-sm);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-gold-light);
  margin: 0 0 var(--sp-sm);
}

.entity-deeds ul {
  margin: 0;
  padding-left: var(--sp-lg);
  font-size: 0.9em;
}

.entity-deeds li {
  color: var(--ink-soft);
  margin-bottom: var(--sp-xs);
}

/* =========================================================
   CONFIDENCE BADGE "?" — POSSIBLE / UNVERIFIED  (v3)
   Visually impossible to miss
   ========================================================= */

/* Used in entity detail cards */
.confidence-question-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(200, 112, 96, 0.12);
  border: 1px solid rgba(200, 112, 96, 0.35);
  border-radius: 4px;
  padding: 4px 10px;
  margin: var(--sp-sm) 0;
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: var(--fs-sm);
  color: #d07868;
}

.confidence-question-badge .qmark {
  font-size: 1.3em;
  font-weight: 700;
  color: var(--accent-gold);
  text-shadow: 0 0 8px rgba(212, 164, 88, 0.5);
}

/* The UNVERIFIED banner that goes across entity summary */
.unverified-banner {
  display: inline-block;
  font-family: 'Lora', Georgia, serif;
  font-size: var(--fs-xs);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  background: rgba(200, 112, 96, 0.2);
  color: #e08a7a;
  border: 1px solid rgba(200, 112, 96, 0.4);
  border-radius: 3px;
  padding: 2px 8px;
  margin-left: var(--sp-sm);
  vertical-align: middle;
}

/* =========================================================
   CINEMATIC MIGRATION MAP  (v3)
   Full-bleed, 600px tall, custom SVG vintage cartography
   ========================================================= */

#map-section {
  margin-left: calc(-1 * var(--sp-lg));
  margin-right: calc(-1 * var(--sp-lg));
}

#map-section h2 {
  margin-left: var(--sp-lg);
  margin-right: var(--sp-lg);
}

#map-section > p {
  margin-left: var(--sp-lg);
  margin-right: var(--sp-lg);
}

#migration-map-container {
  position: relative;
  background: #0e0b08;
  border-top: 1px solid rgba(212, 164, 88, 0.18);
  border-bottom: 1px solid rgba(212, 164, 88, 0.18);
  overflow: hidden;
  /* No fixed height — the SVG viewBox drives height via aspect ratio */
}

#migration-map-svg {
  display: block;
  width: 100%;
  /* SVG viewBox 900x600 — 3:2 ratio; lets it scale responsively */
}

/* Map tooltip / hover card */
.map-tooltip {
  position: absolute;
  pointer-events: none;
  background: var(--paper-raised);
  border: 1px solid rgba(212, 164, 88, 0.5);
  border-top: 2px solid var(--accent-gold);
  border-radius: 0 6px 6px 6px;
  padding: 12px 16px;
  min-width: 220px;
  max-width: 300px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.7), 0 0 0 1px rgba(212,164,88,0.08);
  z-index: 20;
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.map-tooltip.visible {
  opacity: 1;
  transform: translateY(0);
}

.map-tooltip-name {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--accent-gold);
  margin-bottom: 3px;
}

.map-tooltip-year {
  font-family: 'Source Code Pro', monospace;
  font-size: 0.7rem;
  color: var(--ink-ghost);
  letter-spacing: 0.06em;
  margin-bottom: 6px;
}

.map-tooltip-body {
  font-family: 'Lora', Georgia, serif;
  font-size: 0.85rem;
  color: var(--ink-soft);
  line-height: 1.55;
}

/* Map animation — the polyline draws itself on load */
#migration-path {
  stroke-dasharray: 3000;
  stroke-dashoffset: 3000;
  animation: drawPath 3.5s ease-out 0.6s forwards;
}

@keyframes drawPath {
  to { stroke-dashoffset: 0; }
}

/* Location markers pulse on hover */
.map-location {
  cursor: pointer;
}

.map-marker-pulse {
  transform-origin: center;
  animation: markerPulse 2.8s ease-in-out infinite;
}

@keyframes markerPulse {
  0%, 100% { opacity: 0.15; transform: scale(1); }
  50%       { opacity: 0.4;  transform: scale(1.6); }
}

/* Stagger each location's pulse */
.map-location:nth-child(1)  .map-marker-pulse { animation-delay: 0.0s; }
.map-location:nth-child(2)  .map-marker-pulse { animation-delay: 0.3s; }
.map-location:nth-child(3)  .map-marker-pulse { animation-delay: 0.6s; }
.map-location:nth-child(4)  .map-marker-pulse { animation-delay: 0.9s; }
.map-location:nth-child(5)  .map-marker-pulse { animation-delay: 1.2s; }
.map-location:nth-child(6)  .map-marker-pulse { animation-delay: 1.5s; }
.map-location:nth-child(7)  .map-marker-pulse { animation-delay: 1.8s; }
.map-location:nth-child(8)  .map-marker-pulse { animation-delay: 2.1s; }
.map-location:nth-child(9)  .map-marker-pulse { animation-delay: 2.4s; }
.map-location:nth-child(10) .map-marker-pulse { animation-delay: 2.7s; }

/* Map legend */
.map-legend {
  position: absolute;
  bottom: 16px;
  right: 16px;
  background: rgba(14, 11, 8, 0.85);
  border: 1px solid rgba(212, 164, 88, 0.2);
  border-radius: 4px;
  padding: 10px 14px;
  font-size: 0.7rem;
  font-family: 'Lora', Georgia, serif;
  color: var(--ink-ghost);
  line-height: 1.8;
  backdrop-filter: blur(4px);
}

.map-legend strong {
  color: var(--accent-gold);
  display: block;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 0.65rem;
  margin-bottom: 4px;
}

@media (prefers-reduced-motion: reduce) {
  #migration-path { animation: none; stroke-dashoffset: 0; }
  .map-marker-pulse { animation: none; opacity: 0.2; }
  .cover-particles { display: none; }
  .cover-glow { animation: none; }
}

/* Print: hide the cinematic map entirely (too complex), keep simple text */
@media print {
  #migration-map-container { display: none !important; }
  .cover-particles { display: none !important; }
  .cover-glow { display: none !important; }
  .entity-portrait { display: none !important; }
  .entity-portrait-placeholder { display: none !important; }
}

/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 760px) {
  :root { font-size: 16px; }

  .container {
    padding: var(--sp-lg) var(--sp-md);
  }

  header.cover {
    margin: 0 calc(-1 * var(--sp-md)) var(--sp-xl);
    padding: var(--sp-xl) var(--sp-md) var(--sp-lg);
  }

  header.cover h1 {
    font-size: clamp(2rem, 8vw, 3rem);
  }

  header.cover::after {
    inset: 12px;
  }

  nav.toc ul { columns: 1; }

  h2 { font-size: var(--fs-2xl); }

  #lineage-section {
    margin-left: calc(-1 * var(--sp-md));
    margin-right: calc(-1 * var(--sp-md));
    padding: 0 var(--sp-md);
  }

  #secondary-trees {
    width: auto;
    left: auto;
    right: auto;
    margin-left: calc(-1 * var(--sp-md));
    margin-right: calc(-1 * var(--sp-md));
    padding: 0 var(--sp-md);
  }

  #secondary-trees > h2,
  #secondary-trees > p,
  .secondary-line-tabs {
    max-width: none;
  }

  .secondary-tree-header {
    grid-template-columns: 1fr;
    padding: var(--sp-md);
  }

  .secondary-tree-meta {
    justify-content: flex-start;
    min-width: 0;
  }

  .secondary-tree-toolbar {
    padding: var(--sp-sm) var(--sp-md);
  }

  .secondary-tree-container,
  .secondary-tree-svg {
    min-height: 420px;
  }

  .secondary-tree-svg {
    height: 520px;
  }

  #map-section {
    margin-left: calc(-1 * var(--sp-md));
    margin-right: calc(-1 * var(--sp-md));
  }

  #map-section h2,
  #map-section > p {
    margin-left: var(--sp-md);
    margin-right: var(--sp-md);
  }

  .map-tooltip {
    min-width: 180px;
    max-width: 240px;
    padding: 8px 12px;
  }

  .tree-toolbar .tree-legend { display: none; }

  .pull-quote {
    font-size: var(--fs-xl);
    padding: var(--sp-lg) var(--sp-md);
  }

  .research-section summary {
    grid-template-columns: auto minmax(0, 1fr);
    padding: var(--sp-md);
  }

  .research-size {
    justify-self: start;
  }

  .research-excerpt {
    grid-column: 2;
  }

  .research-body {
    padding: 0 var(--sp-md) var(--sp-md);
  }

  .entity-portrait-wrap {
    float: none;
    margin: 0 0 var(--sp-md) 0;
    display: flex;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  header.cover h1 { font-size: 2rem; }
  .transcript-turn:first-child .text p:first-child::first-letter {
    font-size: 3.2em;
  }
}

/* =========================================================
   PRINT
   ========================================================= */

@media print {
  /* Print = clean light mode — dark ink on white paper, no waste */
  :root {
    --bg: #ffffff !important;
    --bg-warm: #ffffff !important;
    --paper: #ffffff !important;
    --paper-raised: #f8f6f2 !important;
    --ink: #1a1614 !important;
    --ink-mid: #3a3028 !important;
    --ink-soft: #5a5048 !important;
    --ink-ghost: #7a7068 !important;
    --accent: #6b3010 !important;
    --accent-warm: #8b5030 !important;
    --accent-gold: #8a6a20 !important;
    --accent-gold-light: #a88030 !important;
    --rule: #d0c8bc !important;
    --rule-light: #e0d8cc !important;
    --shari-color: #4a2010 !important;
    --hunter-color: #3a4858 !important;
  }

  * { animation: none !important; transition: none !important; }

  body {
    background: white !important;
    background-image: none !important;
    color: #1a1614 !important;
    font-size: 10.5pt;
    line-height: 1.55;
  }

  .container {
    max-width: none;
    padding: 0;
  }

  header.cover {
    margin: 0 0 2cm;
    padding: 1.5cm 0;
    background: none !important;
    box-shadow: none;
    border-bottom: 2pt solid #6b3010;
  }

  header.cover h1 {
    color: #1a1614 !important;
    text-shadow: none !important;
  }

  header.cover h1 em {
    color: #6b3010 !important;
  }

  header.cover::before,
  header.cover::after { display: none; }

  header.cover h1 { font-size: 28pt; }

  .audio-wrapper,
  audio,
  #timeline-container,
  #map-container,
  .tree-toolbar,
  .tree-hint,
  nav.toc a[href^="#"]::after { display: none !important; }

  nav.toc {
    border: 1pt solid #ccc;
    background: #f8f6f2 !important;
    break-inside: avoid;
    page-break-after: always;
  }

  nav.toc ul { columns: 2; }

  h2 {
    font-size: 18pt;
    color: #1a1614 !important;
    page-break-after: avoid;
    margin-top: 1.5cm;
  }

  h2::after {
    background: #8a6a20 !important;
  }

  h3 { font-size: 13pt; page-break-after: avoid; }

  section { page-break-before: auto; }

  #lineage-tree-container {
    height: 280mm;
    width: 100%;
    background: white !important;
    border: 1pt solid #ccc;
    overflow: hidden;
    break-inside: avoid;
  }

  #lineage-tree-container::before { display: none; }

  details.entity-card {
    background: white !important;
    break-inside: avoid;
    border-left-width: 2pt;
    margin: 4pt 0;
  }

  details.entity-card[open] summary::before,
  details.entity-card summary::before { display: none; }

  /* Force all entity cards open for print */
  details.entity-card .entity-body { display: block !important; }

  .confidence-confirmed { background: #dff0e0 !important; color: #2d5a2d !important; border-color: #2d5a2d !important; }
  .confidence-probable  { background: #fef3cd !important; color: #7a5a00 !important; border-color: #7a5a00 !important; }
  .confidence-possible  { background: #fce8e8 !important; color: #8b2020 !important; border-color: #8b2020 !important; }
  .confidence-living    { background: #e8edf2 !important; color: #3d4d5e !important; border-color: #3d4d5e !important; }

  .research-section {
    background: #f8f6f2 !important;
    border: 1pt solid #ccc;
    break-inside: avoid;
    padding: 12pt;
    margin: 8pt 0;
    box-shadow: none !important;
  }

  .callout {
    border-left: 3pt solid #8a6a20;
    background: #fffdf4 !important;
    break-inside: avoid;
  }

  .pull-quote {
    font-size: 14pt;
    color: #6b3010 !important;
    text-shadow: none !important;
    break-inside: avoid;
    padding: 12pt 0;
    border-color: #c0a070 !important;
  }

  .pull-quote::before {
    color: #c0a070 !important;
  }

  .transcript-turn:first-child .text p:first-child::first-letter {
    color: #6b3010 !important;
    text-shadow: none !important;
  }

  .transcript-turn-hunter {
    background: #f4f0ec !important;
    border-left-color: #d0c8bc !important;
  }

  footer.colophon {
    margin-top: 1cm;
    font-size: 8pt;
    border-top: 1pt solid #ccc;
    opacity: 1 !important;
  }

  footer.colophon code {
    background: #f0ece8 !important;
    color: #5a5048 !important;
    border-color: #d0c8bc !important;
  }

  a { color: inherit; text-decoration: none; }

  /* Show URLs for external links */
  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666;
  }
}
"""

# ---------- Helpers ----------

def load_transcript():
    md = TRANSCRIPT.read_text(encoding="utf-8")
    parts = md.split("---", 1)
    body = parts[1] if len(parts) > 1 else md
    turns = []
    pattern = re.compile(
        r"\[(\d+:\d{2}(?::\d{2})?)\]\s*\*\*(\w+):\*\*\s*\n(.*?)(?=\n\[\d+:\d{2}|\Z)",
        re.DOTALL,
    )
    for m in pattern.finditer(body):
        turns.append({
            "ts": m.group(1),
            "speaker": m.group(2),
            "text": m.group(3).strip(),
        })
    return turns


def load_entities():
    return json.loads(ENTITIES.read_text(encoding="utf-8"))


def load_research():
    findings = {}
    research_files = [
        fn for fn in RESEARCH_DIR.glob("*.md")
        if re.match(r"^\d{2,}-", fn.name)
    ]
    research_files.sort(key=lambda p: (int(p.name.split("-", 1)[0]), p.name))
    for fn in research_files:
        findings[fn.stem] = fn.read_text(encoding="utf-8")
    return findings


def load_portraits():
    """Load portrait URL map from research/13-portraits-and-images.json if present.
    Returns dict: {person_id: portrait_url, ...}
    Also merges portrait_url from entities.json and lineage.json persons directly.
    """
    portrait_map = {}
    if PORTRAITS_JSON.exists():
        try:
            data = json.loads(PORTRAITS_JSON.read_text(encoding="utf-8"))
            # Agent 13 schema: top-level keys with arrays of {entity_id, image_url, ...}
            arrays = []
            if isinstance(data, dict):
                for k in ("person_portraits", "historical_figure_images",
                          "place_images", "artifact_images"):
                    v = data.get(k)
                    if isinstance(v, list):
                        arrays.append(v)
            elif isinstance(data, list):
                arrays.append(data)
            for arr in arrays:
                for item in arr:
                    if not isinstance(item, dict):
                        continue
                    pid = item.get("entity_id") or item.get("id") or item.get("person_id")
                    url = item.get("image_url") or item.get("portrait_url") or item.get("url")
                    if pid and url:
                        portrait_map[pid] = url
        except (json.JSONDecodeError, KeyError, AttributeError, TypeError):
            pass
    # Also pick up portrait_url embedded directly on person objects (future-proof)
    entities_data = json.loads(ENTITIES.read_text(encoding="utf-8"))
    for p in entities_data.get("people", []):
        if p.get("portrait_url") and p.get("id"):
            portrait_map[p["id"]] = p["portrait_url"]
    lineage_path = WORKSPACE / "research" / "06-full-mattingly-lineage.json"
    if lineage_path.exists():
        try:
            lineage_data = json.loads(lineage_path.read_text(encoding="utf-8"))
            for g in lineage_data.get("generations", []):
                per = g.get("person", {}) or {}
                if per.get("portrait_url") and per.get("id"):
                    portrait_map[per["id"]] = per["portrait_url"]
        except (json.JSONDecodeError, KeyError):
            pass
    return portrait_map


def render_notable_stories():
    """Render the Notable Stories section — beautiful narrative cards from
    research/14-notable-deeds.json. Replaces the verbatim-transcript section.
    """
    if not DEEDS_JSON.exists():
        return '<p><em>Notable stories pending — research/14-notable-deeds.json not found.</em></p>'
    try:
        raw = json.loads(DEEDS_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return '<p><em>Notable stories file is malformed.</em></p>'
    deeds = raw.get("notable_deeds", []) if isinstance(raw, dict) else raw
    if not isinstance(deeds, list) or not deeds:
        return '<p><em>No notable stories found.</em></p>'

    # Group by tag/era for sectioning
    sections = {
        "Medieval (1167–1249)": [],
        "Colonial Maryland (1666–1789)": [],
        "Kentucky frontier (1785–1843)": [],
        "Texas era (1837–1945)": [],
        "Twentieth century": [],
        "Other": [],
    }
    def classify(d):
        year_str = str(d.get("year", "") or "").strip()
        try:
            year = int(year_str[:4]) if year_str else 0
        except (ValueError, TypeError):
            year = 0
        if year and year < 1300: return "Medieval (1167–1249)"
        if year and year < 1790: return "Colonial Maryland (1666–1789)"
        if year and year < 1850: return "Kentucky frontier (1785–1843)"
        if year and year < 1946: return "Texas era (1837–1945)"
        if year >= 1946: return "Twentieth century"
        # Fallback: tag-based
        tag = (d.get("tag") or "").lower()
        if "medieval" in tag: return "Medieval (1167–1249)"
        if "civic" in tag and year > 1900: return "Twentieth century"
        return "Other"
    for d in deeds:
        if isinstance(d, dict):
            sections[classify(d)].append(d)

    cards_html = []
    for section_title, group in sections.items():
        if not group:
            continue
        cards_html.append(f'<h3 class="story-era-heading">{html.escape(section_title)}</h3>')
        for deed in group:
            name = deed.get("person_name") or "—"
            headline = deed.get("headline") or ""
            story = deed.get("story") or ""
            year = deed.get("year") or ""
            place = deed.get("place") or ""
            tag = deed.get("tag") or ""
            verifications = deed.get("verification") or []
            sources_html = ""
            if verifications:
                links = " · ".join(
                    f'<a href="{html.escape(v)}" target="_blank" rel="noopener">source</a>'
                    for v in verifications[:3] if isinstance(v, str) and v.startswith("http")
                )
                if links:
                    sources_html = f'<div class="story-sources">{links}</div>'
            meta = []
            if year: meta.append(html.escape(str(year)))
            if place: meta.append(html.escape(str(place)))
            meta_html = " · ".join(meta)
            cards_html.append(
                f'<article class="story-card">'
                f'<header class="story-header">'
                f'<div class="story-name">{html.escape(str(name))}</div>'
                f'{f"<div class=story-meta>{meta_html}</div>" if meta_html else ""}'
                f'</header>'
                f'<h4 class="story-headline">{html.escape(headline)}</h4>'
                f'<p class="story-body">{html.escape(story)}</p>'
                f'{sources_html}'
                f'</article>'
            )
    return "\n".join(cards_html) if cards_html else '<p><em>No stories rendered.</em></p>'


def load_deeds():
    """Load notable deeds map from research/14-notable-deeds.json if present.
    Returns dict: {person_id: [deed_headline_string, ...], ...}
    Handles multiple schema variants:
      - List of {entity_id, headline, story, ...}
      - List of {id/person_id, deeds/notable_deeds, ...}
      - Dict with 'notable_deeds' key (list)
    """
    if not DEEDS_JSON.exists():
        return {}
    try:
        raw = json.loads(DEEDS_JSON.read_text(encoding="utf-8"))
        # Unwrap dict container if needed
        if isinstance(raw, dict):
            # Try common wrapper keys
            for key in ("notable_deeds", "deeds", "people", "entries"):
                if isinstance(raw.get(key), list):
                    raw = raw[key]
                    break
            else:
                # Flat dict keyed by person_id?
                result = {}
                for pid, val in raw.items():
                    if isinstance(val, list):
                        result[pid] = [str(x) for x in val[:5]]
                    elif isinstance(val, str):
                        result[pid] = [val]
                return result

        deeds = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            # Support 'entity_id', 'id', 'person_id' as the key field
            pid = item.get("entity_id") or item.get("id") or item.get("person_id")
            # Support 'headline', 'title', 'deed' as a single deed string
            headline = item.get("headline") or item.get("title") or item.get("deed")
            # Support 'deeds', 'notable_deeds', 'achievements' as a list of deeds
            deed_list = item.get("deeds") or item.get("notable_deeds") or item.get("achievements") or []
            if pid:
                entries = []
                if headline:
                    entries.append(str(headline))
                for d in deed_list[:4]:
                    if isinstance(d, dict):
                        s = d.get("headline") or d.get("text") or d.get("description") or ""
                    else:
                        s = str(d)
                    if s:
                        entries.append(s)
                if entries:
                    if pid in deeds:
                        deeds[pid].extend(entries[:3])
                    else:
                        deeds[pid] = entries[:4]
        return deeds
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


def md_to_html(md: str) -> str:
    """Tiny markdown-to-HTML for research files (handles headings, lists, links, bold, italic)."""
    out = []
    in_list = False
    for line in md.split("\n"):
        s = line.rstrip()
        # Headings
        m = re.match(r"^(#+)\s+(.*)$", s)
        if m:
            if in_list:
                out.append("</ul>"); in_list = False
            level = min(len(m.group(1)) + 1, 6)
            out.append(f"<h{level}>{html.escape(m.group(2))}</h{level}>")
            continue
        # List
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{render_inline(m.group(1))}</li>")
            continue
        # Blank
        if not s:
            if in_list:
                out.append("</ul>"); in_list = False
            out.append("")
            continue
        # Paragraph
        if in_list:
            out.append("</ul>"); in_list = False
        out.append(f"<p>{render_inline(s)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def _research_number(stem):
    m = re.match(r"^(\d+)-", stem)
    return int(m.group(1)) if m else 9999


def _research_title(stem, content):
    for line in content.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
    title = re.sub(r"^\d+-", "", stem).replace("-", " ")
    return title.title()


def _research_excerpt(content, max_chars=220):
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"^[-*]\s+", "", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        s = re.sub(r"[*_`]+", "", s)
        if len(s) > max_chars:
            return s[:max_chars - 1].rstrip() + "…"
        return s
    return "Research memo."


def _research_group_label(number):
    if number <= 5:
        return "Foundational Research"
    if number <= 21:
        return "Lineage Build-Out"
    if number <= 35:
        return "Branch Deep Dives"
    return "Current Research Memos"


def _name_redaction_variants(name):
    if not name:
        return set()
    clean = re.sub(r"\s+", " ", str(name)).strip()
    if not clean or clean.startswith("[") or clean in {"?", "—"}:
        return set()

    variants = {clean}
    no_parens = re.sub(r"\s*\([^)]*\)", "", clean).strip()
    if no_parens and no_parens != clean:
        if " " in no_parens or no_parens.lower() not in {"rachel"}:
            variants.add(no_parens)
    variants.add(clean.replace("Jr.", "Jr"))
    variants.add(clean.replace("Sr.", "Sr"))
    if "Dale William Spence Jr" in clean:
        variants.update({"Dale Jr.", "Dale Jr"})
    if clean.startswith("Rachel "):
        variants.update({"Rachel Spence", "Rachel Trifon"})
    return {v for v in variants if len(v) >= 3}


def _collect_tree_living_terms(root, redaction_set):
    terms = set()
    if not isinstance(root, dict):
        return terms
    stack = [root]
    while stack:
        node = stack.pop()
        node_id = node.get("id")
        dates = str(node.get("dates") or "").lower()
        fact = str(node.get("fact") or "").lower()
        should_redact = (
            (node_id and node_id in redaction_set)
            or "living" in dates
            or "lives in" in fact
        )
        if should_redact:
            terms.update(_name_redaction_variants(node.get("name")))
        for child in node.get("children", []) or []:
            if isinstance(child, dict):
                stack.append(child)
    return terms


def collect_public_research_redaction_terms(entities, redaction_set):
    terms = set()
    for person in entities.get("people", []):
        pid = person.get("id")
        if pid not in redaction_set:
            continue
        for key in ("full_name", "full_name_redacted"):
            value = person.get(key)
            if value and " " in value:
                terms.update(_name_redaction_variants(value))

    multi_path = WORKSPACE / "research" / "lineage-tree-multi.json"
    if multi_path.exists():
        try:
            data = json.loads(multi_path.read_text(encoding="utf-8"))
            roots = [data.get("primary")]
            roots.extend(st.get("tree") for st in data.get("secondary_trees", []) or [])
            for root in roots:
                terms.update(_collect_tree_living_terms(root, redaction_set))
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    return terms


def redact_public_markdown(text, redaction_terms):
    if not redaction_terms:
        return text
    redacted = text
    for term in sorted(redaction_terms, key=len, reverse=True):
        redacted = re.sub(re.escape(term), "[living relative]", redacted, flags=re.IGNORECASE)
    return redacted


def render_research_sections(research, family_only=True, redaction_terms=None):
    if not research:
        return '<div class="research-section"><p><em>Research pending — files will appear when subagents complete.</em></p></div>'

    sections = []
    current_group = None
    for stem, content in sorted(research.items(), key=lambda item: (_research_number(item[0]), item[0])):
        display_content = content if family_only else redact_public_markdown(content, redaction_terms or set())
        number = _research_number(stem)
        group = _research_group_label(number)
        if group != current_group:
            sections.append(f'<h3 class="research-group-heading">{html.escape(group)}</h3>')
            current_group = group

        title = _research_title(stem, display_content)
        excerpt = _research_excerpt(display_content)
        size_kb = max(1, round(len(content.encode("utf-8")) / 1024))
        sections.append(f"""<details class="research-section" id="research-{html.escape(stem)}">
  <summary>
    <span class="research-number">{number:02d}</span>
    <span class="research-title">{html.escape(title)}</span>
    <span class="research-size">{size_kb} KB</span>
    <span class="research-excerpt">{html.escape(excerpt)}</span>
  </summary>
  <div class="research-body">
{md_to_html(display_content)}
  </div>
</details>""")

    return f'<div class="research-library">\n{"".join(sections)}\n</div>'


def render_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


# ---------- Entity annotation in transcript ----------

def build_entity_index(entities):
    """Return list of (search_string, entity_id, entity_type, display_name) sorted longest-first."""
    idx = []
    for p in entities.get("people", []):
        if p.get("redact_in_public") or p.get("research_priority") == "skip":
            continue
        for nm in [p.get("full_name"), p.get("given_name"), p.get("surname"), p.get("middle_name")] + p.get("alternate_spellings", []):
            if nm and len(nm) >= 3 and not nm.startswith("("):
                idx.append((nm, p["id"], "person", p.get("full_name") or nm))
    for pl in entities.get("places", []):
        nm = pl.get("name")
        if nm and len(nm) >= 3:
            idx.append((nm, pl["id"], "place", nm))
    for o in entities.get("organizations", []):
        nm = o.get("name")
        if nm and len(nm) >= 3:
            idx.append((nm, o["id"], "org", nm))
    for hr in entities.get("historical_references", []):
        nm = hr.get("subject")
        if nm and len(nm) >= 3:
            idx.append((nm, hr["id"], "historical", nm))
    seen = set()
    deduped = []
    for entry in sorted(idx, key=lambda x: -len(x[0])):
        if entry[0].lower() in seen:
            continue
        seen.add(entry[0].lower())
        deduped.append(entry)
    return deduped


def annotate_text(text: str, entity_index, redact_set=None):
    redact_set = redact_set or set()
    safe = html.escape(text)
    for nm, eid, etype, _disp in entity_index:
        if eid in redact_set:
            pattern = re.compile(r"\b" + re.escape(html.escape(nm)) + r"\b")
            safe = pattern.sub(f"<span class=\"redacted\">[redacted]</span>", safe, count=10)
            continue
        pattern = re.compile(r"(?<!>)\b(" + re.escape(html.escape(nm)) + r")\b(?![^<]*</a>)")
        safe = pattern.sub(
            lambda m, eid=eid, etype=etype: f'<a href="#{eid}" class="entity-link entity-{etype}">{m.group(1)}</a>',
            safe,
            count=2,
        )
    return safe


# ---------- HTML rendering ----------

def render_transcript(turns, entity_index, redact_set):
    out = []
    for t in turns:
        is_shari = t["speaker"].lower().startswith("shari")
        spk_class = "speaker-shari" if is_shari else "speaker-hunter"
        turn_class = "transcript-turn" if is_shari else "transcript-turn transcript-turn-hunter"
        annotated = annotate_text(t["text"], entity_index, redact_set)
        out.append(
            f'<div class="{turn_class}">'
            f'<div class="speaker-line">'
            f'<span class="{spk_class}">{html.escape(t["speaker"])}</span>'
            f'<span class="timestamp">{html.escape(t["ts"])}</span>'
            f'</div>'
            f'<div class="text"><p>{annotated}</p></div>'
            f'</div>'
        )
    return "\n".join(out)


def _matches_public_redaction_terms(value, redaction_terms):
    text = str(value or "")
    return any(re.search(re.escape(term), text, flags=re.IGNORECASE) for term in redaction_terms or set())


def _public_relation_label(relation, redaction_terms=None):
    relation = str(relation or "").strip()
    if not relation:
        return "living relative"
    if "(" in relation or _matches_public_redaction_terms(relation, redaction_terms or set()):
        generic = re.sub(r"\([^)]*\)", "", relation).strip(" ,;-")
        return generic or "living relative"
    return relation


def render_person_card(p, redact=False, portrait_map=None, deeds_map=None, public_redaction_terms=None):
    portrait_map = portrait_map or {}
    deeds_map = deeds_map or {}
    public_redaction_terms = public_redaction_terms or set()
    if p.get("redact_in_public") and redact:
        return ""
    name = p.get("full_name") or p.get("given_name") or "(unnamed)"
    pid = p["id"]
    relation = p.get("relation_to_shari", "")

    public_blob = " ".join(
        str(p.get(key) or "")
        for key in ("full_name", "given_name", "context", "relation_to_shari", "occupation")
    )
    public_redact_person = redact and (
        (p.get("living_flag") and pid not in {"p020", "p021"})
        or _matches_public_redaction_terms(public_blob, public_redaction_terms)
        or "lives in" in public_blob.lower()
    )
    if public_redact_person:
        redacted_name = f"[redacted, {_public_relation_label(relation, public_redaction_terms)}]"
        return f'''<details class="entity-card" id="{pid}">
  <summary>
    <div class="entity-summary-name">{html.escape(redacted_name)}</div>
    <div class="entity-summary-meta">{render_confidence("living")}</div>
  </summary>
  <div class="entity-body">
    <p class="entity-meta">Living-person details redacted in the public edition.</p>
  </div>
</details>'''

    b = p.get("birth_year")
    d = p.get("death_year")
    years = f" ({b}–{d})" if b and d else (f" (b. {b})" if b else (f" (d. {d})" if d else ""))
    living = " " + render_confidence("living") if p.get("living_flag") else ""
    occupation = p.get("occupation")
    enriched = p.get("enriched_context", "")
    context = p.get("context", "")
    bp = p.get("birth_place")
    dp = p.get("death_place")
    spouse = p.get("spouse")
    education = p.get("education")
    branch = p.get("branch", "")
    confidence = p.get("confidence", "") or ""
    sources = p.get("sources") or []
    wiki_url = p.get("wikipedia_url") or ""
    portrait_caption = p.get("portrait_caption", "")

    # Subtitle for collapsed summary view
    subtitle_bits = []
    if relation:
        subtitle_bits.append(relation)
    if occupation:
        subtitle_bits.append(occupation[:60])
    elif bp:
        subtitle_bits.append(f"of {bp}")
    subtitle = " · ".join(subtitle_bits)

    conf_upper = confidence.upper()
    summary_badge = ""
    if "UNVERIFIED" in conf_upper:
        summary_badge = ' <span class="unverified-banner">? UNVERIFIED</span>'
    elif "POSSIBLE" in conf_upper:
        summary_badge = ' <span class="unverified-banner">? POSSIBLE</span>'

    body_parts = []

    # Portrait (floated)
    portrait_url = portrait_map.get(pid) or p.get("portrait_url")
    if portrait_url:
        cap = f'<figcaption class="portrait-caption">{html.escape(portrait_caption)}</figcaption>' if portrait_caption else ''
        body_parts.append(
            f'<figure class="entity-portrait-wrap">'
            f'<img class="entity-portrait" src="{html.escape(portrait_url)}" '
            f'alt="Portrait of {html.escape(name)}" loading="lazy">'
            f'{cap}'
            f'</figure>'
        )

    # Vital stats — clean, scannable
    vital_rows = []
    if relation:
        vital_rows.append(("Relation", relation + (years if years else "") + living))
    if b and d:
        vital_rows.append(("Lifespan", f"{b}–{d} ({d-b} years)"))
    elif b or d:
        vital_rows.append(("Born/Died", years.strip().lstrip("(").rstrip(")")))
    if bp:
        vital_rows.append(("Birthplace", bp))
    if dp:
        vital_rows.append(("Died at", dp))
    if spouse:
        vital_rows.append(("Spouse", spouse))
    if occupation:
        vital_rows.append(("Occupation", occupation))
    if education:
        vital_rows.append(("Education", education))
    if branch:
        vital_rows.append(("Branch", branch))
    if vital_rows:
        rows_html = "\n".join(
            f'<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>'
            for k, v in vital_rows
        )
        body_parts.append(f'<table class="vital-stats">{rows_html}</table>')

    # Confidence note
    if "UNVERIFIED" in conf_upper:
        body_parts.append(
            '<div class="confidence-question-badge">'
            '<span class="qmark">?</span>'
            ' <span>UNVERIFIED — needs primary source research. Genealogical descent not yet confirmed.</span>'
            '</div>'
        )
    elif "POSSIBLE" in conf_upper:
        body_parts.append(
            '<div class="confidence-question-badge">'
            '<span class="qmark">?</span>'
            ' <span>POSSIBLE — only one source / circumstantial evidence. Treat as working hypothesis.</span>'
            '</div>'
        )

    # Rich biographical narrative (prefer enriched_context)
    bio = enriched or context
    if bio:
        body_parts.append(f'<p class="entity-bio">{html.escape(bio)}</p>')

    # Notable deed (rich version with story if available in entity.notable_deed)
    nd = p.get("notable_deed") or {}
    if isinstance(nd, dict) and nd.get("story"):
        headline = nd.get("headline", "")
        story = nd.get("story", "")
        body_parts.append(
            f'<aside class="notable-deed-callout">'
            f'<div class="notable-deed-label">Notable</div>'
            f'<div class="notable-deed-headline">{html.escape(headline)}</div>'
            f'<p class="notable-deed-story">{html.escape(story)}</p>'
            f'</aside>'
        )
    else:
        deeds = deeds_map.get(pid)
        if deeds:
            deeds_li = "\n".join(f"<li>{html.escape(d)}</li>" for d in deeds)
            body_parts.append(
                f'<div class="entity-deeds">'
                f'<p class="entity-deeds-title">Notable</p>'
                f'<ul>{deeds_li}</ul>'
                f'</div>'
            )

    # External links — Wikipedia, FamilySearch, WikiTree, etc.
    link_buttons = []
    if wiki_url:
        link_buttons.append(f'<a class="ext-link wiki-link" href="{html.escape(wiki_url)}" target="_blank" rel="noopener">📖 Wikipedia</a>')
    for src in sources:
        if not isinstance(src, str) or not src.startswith("http"):
            continue
        if "wikitree" in src:
            link_buttons.append(f'<a class="ext-link" href="{html.escape(src)}" target="_blank" rel="noopener">🌳 WikiTree</a>')
        elif "familysearch" in src:
            link_buttons.append(f'<a class="ext-link" href="{html.escape(src)}" target="_blank" rel="noopener">🔍 FamilySearch</a>')
        elif "findagrave" in src:
            link_buttons.append(f'<a class="ext-link" href="{html.escape(src)}" target="_blank" rel="noopener">🪦 Find a Grave</a>')
        elif "loc.gov" in src:
            link_buttons.append(f'<a class="ext-link" href="{html.escape(src)}" target="_blank" rel="noopener">📜 Library of Congress</a>')
        elif "archive.org" in src:
            link_buttons.append(f'<a class="ext-link" href="{html.escape(src)}" target="_blank" rel="noopener">📚 Internet Archive</a>')
        else:
            link_buttons.append(f'<a class="ext-link" href="{html.escape(src)}" target="_blank" rel="noopener">🔗 Source</a>')
    if link_buttons:
        body_parts.append(f'<div class="entity-links-row">{"".join(link_buttons[:6])}</div>')

    body = "\n".join(body_parts)

    # Direct-line ancestors should be open by default
    direct_line_ids = {"p070", "p071", "p072", "p073", "p062", "p060", "p028", "p039",
                      "p043", "p044", "p041", "p002", "p000", "p014", "p011"}
    open_attr = " open" if pid in direct_line_ids else ""

    summary_html = (
        f'<div class="entity-summary-name">{html.escape(name)}</div>'
        f'<div class="entity-summary-meta">{html.escape(years.strip())}{summary_badge}</div>'
    )
    if subtitle:
        summary_html += f'<div class="entity-summary-sub">{html.escape(subtitle)}</div>'

    return f'''<details class="entity-card" id="{pid}"{open_attr}>
  <summary>{summary_html}</summary>
  <div class="entity-body">
{body}
  </div>
</details>'''


def render_place_card(pl):
    name = pl.get("name", "(unnamed)")
    pid = pl["id"]
    typ = pl.get("type", "")
    modern = pl.get("modern_name")
    country = pl.get("country", "")
    context = pl.get("context", "")
    timestamps = pl.get("transcript_timestamps", []) or []
    body = []
    meta = f"{typ}"
    if country:
        meta += f", {country}"
    body.append(f'<p class="entity-meta">{html.escape(meta)}</p>')
    if modern:
        body.append(f"<p><strong>Modern equivalent:</strong> {html.escape(modern)}</p>")
    if context:
        body.append(f"<p>{html.escape(context)}</p>")
    if timestamps:
        body.append(f'<p class="entity-meta">Mentioned at: {", ".join(html.escape(t) for t in timestamps)}</p>')
    return f'''<details class="entity-card" id="{pid}">
  <summary>{html.escape(name)}</summary>
  <div class="entity-body">
{chr(10).join(body)}
  </div>
</details>'''


def render_event_card(e):
    desc = e.get("description", "")
    eid = e["id"]
    when = e.get("date_or_year") or "—"
    place = e.get("place") or ""
    context = e.get("context", "")
    body = [f'<p class="entity-meta"><strong>{html.escape(when)}</strong>{(" · " + html.escape(place)) if place else ""}</p>']
    if context:
        body.append(f"<p>{html.escape(context)}</p>")
    return f'''<details class="entity-card" id="{eid}">
  <summary>{html.escape(desc[:80])}</summary>
  <div class="entity-body">
{chr(10).join(body)}
  </div>
</details>'''


def render_confidence(level):
    cls = {
        "confirmed": "confidence-confirmed",
        "probable": "confidence-probable",
        "possible": "confidence-possible",
        "living": "confidence-living",
    }.get(level, "")
    label = level.upper()
    return f'<span class="confidence {cls}">{label}</span>'


# ---------- D3 lineage tree ----------

def build_lineage_tree_data(portrait_map=None):
    """Return nested dict for D3 tree.
    Preference order:
    1. research/lineage-tree.json — pre-shaped branching tree (CLASSIC family-tree structure)
    2. research/06-full-mattingly-lineage.json — linear generations array
    3. _placeholder_lineage_tree() — hardcoded fallback
    """
    portrait_map = portrait_map or {}

    # Prefer the classic branching tree if it exists
    classic_path = WORKSPACE / "research" / "lineage-tree.json"
    if classic_path.exists():
        try:
            tree = json.loads(classic_path.read_text(encoding="utf-8"))
            # Already in {name, dates, fact, id, children, ...} shape — just inject portraits
            _inject_portraits(tree, portrait_map)
            return tree
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    lineage_path = WORKSPACE / "research" / "06-full-mattingly-lineage.json"
    if lineage_path.exists():
        try:
            data = json.loads(lineage_path.read_text(encoding="utf-8"))
            return convert_lineage_research_to_tree(data, portrait_map)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
    return _placeholder_lineage_tree(portrait_map)


def _inject_portraits(node, portrait_map):
    """Recursively walk a tree and add portrait_url where ID matches."""
    if isinstance(node, dict):
        nid = node.get("id")
        if nid and nid in portrait_map:
            node["portrait_url"] = portrait_map[nid]
        for child in node.get("children", []) or []:
            _inject_portraits(child, portrait_map)


def convert_lineage_research_to_tree(lineage_data, portrait_map=None):
    """Convert the lineage agent's generations array to a nested tree."""
    portrait_map = portrait_map or {}
    gens = lineage_data.get("generations", [])
    if not gens:
        return _placeholder_lineage_tree(portrait_map)
    # Build linearly (one main descendant per generation; collateral siblings as branches)
    nodes = []
    for g in gens:
        p = g.get("person", {}) or {}
        pid = p.get("id") or None
        raw_conf = (p.get("confidence") or "unknown")
        conf_lower = raw_conf.lower()
        # Normalize: anything with POSSIBLE or UNVERIFIED gets flagged
        if "unverified" in conf_lower:
            conf_normalized = "unverified"
        elif "possible" in conf_lower:
            conf_normalized = "possible"
        elif "probable" in conf_lower:
            conf_normalized = "probable"
        elif "confirmed" in conf_lower:
            conf_normalized = "confirmed"
        else:
            conf_normalized = "unknown"
        nodes.append({
            "name": p.get("full_name") or g.get("label") or f"Generation {g.get('gen')}",
            "dates": _format_dates(p.get("birth_year"), p.get("death_year")),
            "fact": (p.get("key_facts") or [g.get("label", "")])[0] if p.get("key_facts") else g.get("label", ""),
            "id": pid,
            "generation": g.get("gen", 0),
            "century": _century_for_year(p.get("birth_year") or p.get("death_year")),
            "confidence": conf_normalized,
            "portrait_url": portrait_map.get(pid, "") if pid else "",
        })
    if not nodes:
        return _placeholder_lineage_tree(portrait_map)
    # Convert flat list to nested tree
    root = nodes[0]
    cursor = root
    cursor["children"] = []
    for n in nodes[1:]:
        n["children"] = []
        cursor["children"].append(n)
        cursor = n
    # Append modern descent (Leroy → Hunter) from entities
    return _attach_modern_descent(root)


def _attach_modern_descent(root):
    """Make sure the tree ends at Hunter."""
    leaf = root
    while leaf.get("children"):
        leaf = leaf["children"][-1]
    return root


def _format_dates(b, d):
    if b and d:
        return f"{b}–{d}"
    if b and not d:
        return f"b. {b}"
    if d and not b:
        return f"d. {d}"
    return "—"


def _century_for_year(year):
    if not year:
        return 0
    try:
        y = int(year)
        return (y // 100) + 1
    except (TypeError, ValueError):
        return 0


def _placeholder_lineage_tree(portrait_map=None):
    """Fallback tree using only confirmed-from-interview anchors."""
    portrait_map = portrait_map or {}

    def gen(name, dates, fact, eid, generation, century, confidence, children=None, siblings=None):
        node = {
            "name": name, "dates": dates, "fact": fact, "id": eid,
            "generation": generation, "century": century, "confidence": confidence,
            "children": children or [],
            "portrait_url": portrait_map.get(eid, "") if eid else "",
        }
        if siblings:
            node["siblings"] = siblings
        return node

    leroy_siblings = [
        {"name": "Claude Mattingly", "dates": "~1900–1934/35", "fact": "San Antonio physician; scandal", "id": "p011"},
        {"name": "Aunt Mamie", "dates": "b. ~1900–02", "fact": "Mother died at her birth", "id": "p013"},
    ]
    fathers_siblings = [
        {"name": "Uncle Zay", "dates": "?", "fact": "Stauffer Chemicals; MIT PhD", "id": None},
        {"name": "Uncle Billy", "dates": "?", "fact": "Stanford geologist", "id": "p019"},
        {"name": "Frost Bank uncle", "dates": "?", "fact": "Mother's brother; lawyer", "id": "p018"},
    ]
    shari_siblings = [
        {"name": "[brother]", "dates": "living", "fact": "Got the chair from Pearl's set", "id": "p022"},
        {"name": "[sister]", "dates": "living", "fact": "—", "id": "p023"},
    ]
    hunter_parent_siblings = [
        {"name": "Charmaine", "dates": "living", "fact": "Hunter's aunt; brought oil painting", "id": "p021"},
    ]

    return gen("Thomas Mattingly I", "~1623–~1665", "Catholic immigrant from England → Maryland 1663–64", "p028", 1, 17, "confirmed", [
        gen("Thomas Mattingly II", "?", "Co-recipient Mattingly's Hope land patent (Sept 4, 1666)", "p039", 2, 17, "confirmed", [
            gen("[Maryland Generation 3]", "~1690s", "Charles County, Maryland Catholic family", None, 3, 17, "unknown", [
                gen("[Maryland Generation 4]", "~1720s", "Pre-Revolution Maryland", None, 4, 18, "unknown", [
                    gen("[Maryland Generation 5]", "~1750s", "Around the Revolution era", None, 5, 18, "unknown", [
                        gen("[Generation 6]", "~1785", "Possible Bardstown, Kentucky migration", None, 6, 18, "unknown", [
                            gen("[Generation 7]", "~1810s", "Texas migration era", None, 7, 19, "unknown", [
                                gen("[The Centenarian]", "1828–1935", "Lived to 107 — Shari's gf's grandfather", "p030", 8, 19, "confirmed", [
                                    gen("[Texas Judge Mattingly]", "~1850s–~1920s", "Texas judge; married a Teichmueller", None, 9, 19, "probable", [
                                        gen("Leroy Teichmuller Mattingly", "1898–?", "U Texas engineer; Shari's grandfather", "p002", 10, 20, "confirmed", [
                                            gen("Shari's father", "1922–?", "Master's degree", "p015", 11, 20, "confirmed", [
                                                gen("Sharyn (\"Shari\")", "~1947–", "Family historian; Santa Monica; oil royalty owner", "p000", 12, 20, "confirmed", [
                                                    gen("[Hunter's parent]", "living", "Shari + David's child", None, 13, 20, "confirmed", [
                                                        gen("Hunter Spence", "living", "Recipient of this family history", "p001", 14, 21, "confirmed"),
                                                    ], siblings=hunter_parent_siblings),
                                                ], siblings=shari_siblings),
                                            ], siblings=fathers_siblings),
                                        ], siblings=leroy_siblings),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ])


def _normalize_tree_confidence(confidence):
    raw = str(confidence or "unknown").strip().lower()
    if "confirmed" in raw:
        return "confirmed"
    if "probable" in raw:
        return "probable"
    if "possible" in raw:
        return "possible"
    if "unverified" in raw:
        return "unverified"
    if "living" in raw:
        return "living"
    return "unknown"


def _walk_tree_nodes(root):
    if not isinstance(root, dict):
        return
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        yield node, depth
        children = node.get("children", []) or []
        for child in reversed(children):
            if isinstance(child, dict):
                stack.append((child, depth + 1))


def _tree_node_should_redact(node, redaction_set):
    node_id = node.get("id")
    if node_id and node_id in redaction_set:
        return True
    dates = str(node.get("dates") or "").lower()
    if "living" in dates:
        return True
    fact = str(node.get("fact") or "").lower()
    if "lives in" in fact:
        return True
    return False


def _prepare_tree_for_audience(node, family_only=True, redaction_set=None):
    """Copy a lineage tree and redact living-node details for public output."""
    redaction_set = redaction_set or set()
    if not isinstance(node, dict):
        return {}

    copied = {k: v for k, v in node.items() if k != "children"}
    copied["confidence"] = _normalize_tree_confidence(copied.get("confidence"))
    copied["children"] = [
        _prepare_tree_for_audience(child, family_only=family_only, redaction_set=redaction_set)
        for child in node.get("children", []) or []
        if isinstance(child, dict)
    ]

    if not family_only and _tree_node_should_redact(copied, redaction_set):
        copied["name"] = "[living relative]"
        copied["dates"] = "living"
        copied["fact"] = "Living-person details redacted in the public edition."
        copied["spouse"] = None
        copied["portrait_url"] = ""
    return copied


def _redact_tree_payload_text(node, redaction_terms):
    if not isinstance(node, dict) or not redaction_terms:
        return node
    for key in ("name", "dates", "fact", "spouse"):
        if isinstance(node.get(key), str):
            node[key] = redact_public_markdown(node[key], redaction_terms)
    for child in node.get("children", []) or []:
        _redact_tree_payload_text(child, redaction_terms)
    return node


def _tree_metrics(root):
    nodes = list(_walk_tree_nodes(root) or [])
    if not nodes:
        return {
            "node_count": 0,
            "generation_count": 0,
            "leaf_count": 0,
            "redacted_count": 0,
            "confidence_counts": {},
        }

    confidence_counts = {}
    leaf_count = 0
    redacted_count = 0
    max_depth = 0
    for node, depth in nodes:
        max_depth = max(max_depth, depth)
        conf = _normalize_tree_confidence(node.get("confidence"))
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
        if not (node.get("children") or []):
            leaf_count += 1
        if node.get("name") == "[living relative]":
            redacted_count += 1
    return {
        "node_count": len(nodes),
        "generation_count": max_depth + 1,
        "leaf_count": leaf_count,
        "redacted_count": redacted_count,
        "confidence_counts": confidence_counts,
    }


def _confidence_summary(metrics):
    counts = metrics.get("confidence_counts", {})
    labels = [
        ("confirmed", "confirmed"),
        ("probable", "probable"),
        ("possible", "possible"),
        ("unverified", "unverified"),
        ("unknown", "open"),
    ]
    parts = [f"{counts[k]} {label}" for k, label in labels if counts.get(k)]
    return " · ".join(parts) if parts else "confidence pending"


def _short_family_line_label(label):
    short = re.sub(r"^(PATERNAL|MATERNAL|DEBUNKED)(-[A-Z]+)?\s*[—-]\s*", "", str(label), flags=re.I)
    short = re.split(r"\s*\(", short, maxsplit=1)[0].strip()
    return short or "Family line"


def _family_line_slug(label, index):
    base = _short_family_line_label(label).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return f"family-line-{index + 1}-{base or 'line'}"


def render_secondary_trees_section(family_only=True, redaction_set=None, public_redaction_terms=None):
    """Render every secondary lineage tree as an interactive D3 tree card."""
    multi_path = WORKSPACE / "research" / "lineage-tree-multi.json"
    if not multi_path.exists():
        return ""
    try:
        data = json.loads(multi_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    secondaries = data.get("secondary_trees", []) or []
    if not secondaries:
        return ""

    cards = []
    tabs = []
    tree_payload = []
    for idx, st in enumerate(secondaries):
        label_raw = st.get("label", "Family line")
        tree = st.get("tree")
        if not tree:
            continue
        prepared_tree = _prepare_tree_for_audience(tree, family_only=family_only, redaction_set=redaction_set)
        if not family_only:
            _redact_tree_payload_text(prepared_tree, public_redaction_terms or set())
        metrics = _tree_metrics(prepared_tree)
        slug = _family_line_slug(label_raw, idx)
        short_label = _short_family_line_label(label_raw)
        tree_payload.append({
            "label": label_raw,
            "short_label": short_label,
            "slug": slug,
            "tree": prepared_tree,
            "metrics": metrics,
        })

        tabs.append(
            f'<a href="#{html.escape(slug)}">'
            f'<span class="line-number">Line {idx + 1}</span>'
            f'<span>{html.escape(short_label)}</span>'
            f'</a>'
        )

        privacy_note = ""
        if metrics["redacted_count"]:
            privacy_note = f'\n      <span>{metrics["redacted_count"]} private</span>'

        cards.append(f"""<article class="secondary-tree-card" id="{html.escape(slug)}" data-tree-index="{idx}">
  <header class="secondary-tree-header">
    <div>
      <p class="secondary-tree-kicker">Family line {idx + 1}</p>
      <h3>{html.escape(label_raw)}</h3>
    </div>
    <div class="secondary-tree-meta" aria-label="Tree summary">
      <span>{metrics["node_count"]} people</span>
      <span>{metrics["generation_count"]} generations</span>
      <span>{html.escape(_confidence_summary(metrics))}</span>{privacy_note}
    </div>
  </header>
  <div class="tree-toolbar secondary-tree-toolbar" role="toolbar" aria-label="{html.escape(short_label)} tree controls">
    <div class="btn-group">
      <button onclick="secondaryTreeZoomIn({idx})" aria-label="Zoom in {html.escape(short_label)}" title="Zoom in">+</button>
      <button onclick="secondaryTreeZoomOut({idx})" aria-label="Zoom out {html.escape(short_label)}" title="Zoom out">&#8722;</button>
      <button onclick="secondaryTreeZoomReset({idx})" aria-label="Reset {html.escape(short_label)} view" title="Reset zoom">Reset</button>
    </div>
    <div class="tree-legend" aria-label="Confidence level legend">
      <span class="legend-item"><span class="swatch confirmed" aria-hidden="true"></span>Confirmed</span>
      <span class="legend-item"><span class="swatch probable" aria-hidden="true"></span>Probable</span>
      <span class="legend-item"><span class="swatch unknown" aria-hidden="true"></span>Research pending</span>
    </div>
  </div>
  <div class="secondary-tree-container" role="img" aria-label="Interactive family tree for {html.escape(short_label)}">
    <svg id="secondary-tree-svg-{idx}" class="secondary-tree-svg" xmlns="http://www.w3.org/2000/svg"></svg>
  </div>
  <p class="tree-hint">Scroll or pinch to zoom &nbsp;&middot;&nbsp; Drag to pan &nbsp;&middot;&nbsp; Click linked nodes to open their detail card below</p>
</article>""")

    if not cards:
        return ""

    tree_payload_json = json.dumps(tree_payload)
    return f"""<section id="secondary-trees" aria-labelledby="secondary-heading">
  <h2 id="secondary-heading">Additional Family Lines</h2>
  <p>The Mattingly tree traces the central maternal line. These separate family-line trees show the connected Spence, Henslee, Teichmüller, Lepik, Boehme, Trifon, and ruled-out Frost lines as inspectable diagrams instead of nested text lists.</p>
  <nav class="secondary-line-tabs" aria-label="Jump to a family line">
    {"".join(tabs)}
  </nav>
  <div class="secondary-tree-list">
    {"".join(cards)}
  </div>
  <script id="secondary-lineage-data" type="application/json">{tree_payload_json}</script>
</section>"""


def render_lineage_tree_section(portrait_map=None, family_only=True, redaction_set=None, public_redaction_terms=None):
    """Generate the HTML+SVG+JS for the D3 family tree."""
    portrait_map = portrait_map or {}
    tree_data = _prepare_tree_for_audience(
        build_lineage_tree_data(portrait_map),
        family_only=family_only,
        redaction_set=redaction_set,
    )
    if not family_only:
        _redact_tree_payload_text(tree_data, public_redaction_terms or set())
    tree_data_json = json.dumps(tree_data)

    # Use lineage research file presence to decide caption
    has_research = (WORKSPACE / "research" / "06-full-mattingly-lineage.json").exists()
    note = (
        "Built from genealogical research (FamilySearch, WikiTree, Maryland State Archives)."
        if has_research
        else "Bracketed [Generation N] cards are placeholders awaiting genealogical research from FamilySearch / Maryland archives."
    )

    return f"""<section id="lineage" aria-labelledby="lineage-heading">
<h2 id="lineage-heading">The Mattingly Lineage</h2>
<p>From <strong>Thomas Mattingly I</strong> — Catholic immigrant to Maryland, 1663 — through fourteen generations to Hunter, four centuries later. <em>{html.escape(note)}</em></p>

<div id="lineage-section">
  <div class="tree-toolbar" role="toolbar" aria-label="Family tree controls">
    <div class="btn-group">
      <button onclick="treeZoomIn()" aria-label="Zoom in" title="Zoom in">+</button>
      <button onclick="treeZoomOut()" aria-label="Zoom out" title="Zoom out">&#8722;</button>
      <button onclick="treeZoomReset()" aria-label="Reset view" title="Reset zoom">Reset</button>
    </div>
    <div class="tree-legend" aria-label="Confidence level legend">
      <span class="legend-item"><span class="swatch confirmed" aria-hidden="true"></span>Confirmed</span>
      <span class="legend-item"><span class="swatch probable" aria-hidden="true"></span>Probable</span>
      <span class="legend-item"><span class="swatch unknown" aria-hidden="true"></span>Research pending</span>
      <span class="legend-item"><span style="font-family:'Cormorant Garamond',Georgia,serif;font-size:1.15em;font-weight:700;color:#d4a458;text-shadow:0 0 5px rgba(212,164,88,0.5)" aria-hidden="true">?</span>&#8201;Uncertain</span>
    </div>
  </div>

  <div id="lineage-tree-container" role="img" aria-label="Interactive family tree showing Mattingly lineage across fourteen generations">
    <svg id="lineage-tree-svg" xmlns="http://www.w3.org/2000/svg"></svg>
  </div>

  <p class="tree-hint">Scroll or pinch to zoom &nbsp;&middot;&nbsp; Drag to pan &nbsp;&middot;&nbsp; Click a named node to open its detail card below</p>
</div>

<script id="lineage-tree-data" type="application/json">{tree_data_json}</script>
</section>"""


def render_lineage_tree_js():
    """Return the D3 tree initialization JS — heritage editorial design v3.
    New: circular portrait frames, HUGE ? confidence badges,
    paper-texture fill for portrait-less uncertain nodes.
    """
    return r"""
// ── Mattingly Lineage Tree v3 ────────────────────────────────────
// Portrait frames, confidence ? badges, paper-texture,
// generation-spine labels, animated entry, zoom+pan.
// ────────────────────────────────────────────────────────────────

const lineageData = JSON.parse(document.getElementById('lineage-tree-data').textContent);

// Canvas dimensions — wider cards for portrait integration
const W = 3600;
const H = 3200;
const NW = 220;   // node width — compact so more nodes fit
const NH = 76;    // node height — compact so the tree breathes vertically
const SPINE = 68; // left margin for generation labels
const M = { top: 56, right: 36, bottom: 72, left: SPINE + 12 };

// Portrait layout constants
const PORT_R = 26;   // portrait circle radius
const PORT_X = -NW/2 + PORT_R + 8;  // portrait center x (left side of card)
const TEXT_X_PORT = PORT_X + PORT_R + 8;  // text start x when portrait present

const svg = d3.select("#lineage-tree-svg")
  .attr("viewBox", `0 0 ${W} ${H}`)
  .attr("preserveAspectRatio", "xMidYMid meet")
  .attr("width", "100%")
  .attr("height", "1040");

// ── Defs: gradients, filters ────────────────────────────────────
const defs = svg.append("defs");

// Glow filter for hovered nodes — gold halo on dark
const shadowFilter = defs.append("filter")
  .attr("id", "node-shadow")
  .attr("x", "-35%").attr("y", "-35%")
  .attr("width", "170%").attr("height", "170%");
shadowFilter.append("feGaussianBlur")
  .attr("in", "SourceGraphic")
  .attr("stdDeviation", 7)
  .attr("result", "blur");
shadowFilter.append("feFlood")
  .attr("flood-color", "#d4a458")
  .attr("flood-opacity", 0.5)
  .attr("result", "color");
shadowFilter.append("feComposite")
  .attr("in", "color").attr("in2", "blur")
  .attr("operator", "in")
  .attr("result", "glow");
const shadowMerge = shadowFilter.append("feMerge");
shadowMerge.append("feMergeNode").attr("in", "glow");
shadowMerge.append("feMergeNode").attr("in", "SourceGraphic");

// Glow filter for "?" confidence badge — amber glow
const qFilter = defs.append("filter")
  .attr("id", "q-badge-glow")
  .attr("x", "-80%").attr("y", "-80%")
  .attr("width", "360%").attr("height", "360%");
qFilter.append("feGaussianBlur")
  .attr("in", "SourceGraphic")
  .attr("stdDeviation", 3)
  .attr("result", "qblur");
qFilter.append("feFlood")
  .attr("flood-color", "#d4a458")
  .attr("flood-opacity", 0.8)
  .attr("result", "qcolor");
qFilter.append("feComposite")
  .attr("in", "qcolor").attr("in2", "qblur")
  .attr("operator", "in")
  .attr("result", "qglow");
const qMerge = qFilter.append("feMerge");
qMerge.append("feMergeNode").attr("in", "qglow");
qMerge.append("feMergeNode").attr("in", "SourceGraphic");

// Portrait drop shadow
const pFilter = defs.append("filter")
  .attr("id", "portrait-drop")
  .attr("x", "-30%").attr("y", "-30%")
  .attr("width", "160%").attr("height", "160%");
pFilter.append("feDropShadow")
  .attr("dx", 0).attr("dy", 2)
  .attr("stdDeviation", 2.5)
  .attr("flood-color", "rgba(0,0,0,0.6)");

// Gradient for each depth level (will create 14 gradients)
function makeGradient(id, topColor, botColor) {
  const g = defs.append("linearGradient")
    .attr("id", id)
    .attr("x1", "0%").attr("y1", "0%")
    .attr("x2", "0%").attr("y2", "100%");
  g.append("stop").attr("offset", "0%").attr("style", `stop-color:${topColor};stop-opacity:1`);
  g.append("stop").attr("offset", "100%").attr("style", `stop-color:${botColor};stop-opacity:1`);
  return id;
}

// Dark-on-dark tree gradient: ALL backgrounds are deep so white/cream text always reads.
// Earlier gens lean amber, later gens lean indigo — but luminance stays low everywhere
// so contrast against light text passes WCAG AA across all 14 generations.
const gradientPalette = [
  ['#3a2208', '#2a1804'],   // G1  — deep amber-black (1620s England)
  ['#46280a', '#341e06'],   // G2
  ['#52300e', '#3e2408'],   // G3
  ['#5e3810', '#48280a'],   // G4
  ['#6a4014', '#522e0e'],   // G5
  ['#724618', '#5a3412'],   // G6  — warm midpoint
  ['#6e4a20', '#583a18'],   // G7
  ['#5a4628', '#48381e'],   // G8  — transition zone
  ['#3e3a3a', '#2e2c30'],   // G9  — neutral charcoal
  ['#2e3242', '#222632'],   // G10 — dark slate
  ['#283044', '#1c2434'],   // G11 — deep navy-slate
  ['#243248', '#182238'],   // G12 — deep navy
  ['#1f3050', '#142042'],   // G13 (Hunter's parent) — rich indigo
  ['#1a2c54', '#0e1c44'],   // G14 (Hunter) — deepest indigo
];

gradientPalette.forEach((pair, i) => {
  makeGradient(`ng-${i}`, pair[0], pair[1]);
});

// Paper texture gradient — for nodes without portraits that are uncertain
makeGradient('ng-paper', '#1a1510', '#221c14');

function nodeFill(d) {
  const conf = d.data.confidence;
  // Uncertain nodes without portraits get a neutral parchment-paper feel
  if (!d.data.portrait_url && (conf === 'unknown' || conf === 'possible' || conf === 'unverified')) {
    return 'url(#ng-paper)';
  }
  const i = Math.min(d.depth, gradientPalette.length - 1);
  return `url(#ng-${i})`;
}

// All cards are dark — text is bright cream/gold across the board for max readability
function nodeTextColor(depth) {
  // Bright cream/white at AA-AAA contrast against the new deep gradient palette
  if (depth < 5) return '#fff3d8';   // bright warm cream on deep amber
  if (depth < 9) return '#fbeacc';   // creamy ivory on warm-mid
  return '#f5f7fc';                  // bright cool white on indigo (was #d8dde4 — too dim)
}
function nodeDateColor(depth) {
  if (depth < 5) return '#f0c060';   // bright gold dates on amber cards
  if (depth < 9) return '#e0b060';   // golden bronze on transition
  return '#a8c0e0';                  // bright cool blue on indigo cards
}
function nodeFactColor(depth) {
  if (depth < 5) return '#d89860';   // bright bronze on amber
  if (depth < 9) return '#c8a878';   // soft tan on transition
  return '#9aa8c8';                  // soft steel-blue on indigo (was #6878a0 — too dark)
}

function confidenceStroke(c) {
  if (c === 'confirmed') return '#d4a458';     // gold for confirmed
  if (c === 'probable')  return '#b8826a';     // bronze for probable
  if (c === 'possible')  return '#c07060';     // warm red for possible
  if (c === 'unverified') return '#a05040';    // deep red for unverified
  return '#4a4440';                            // dim for unknown
}
function confidenceStrokeWidth(c) {
  if (c === 'confirmed') return 2.0;
  if (c === 'possible' || c === 'unverified') return 1.8;
  return 1.5;
}
function confidenceDash(c) {
  if (c === 'unknown') return '4,3';
  if (c === 'possible') return '6,3';
  if (c === 'unverified') return '5,3,2,3';
  return 'none';
}

// ── Tree layout ─────────────────────────────────────────────────
const root = d3.hierarchy(lineageData);
const treeLayout = d3.tree()
  .size([W - M.left - M.right, H - M.top - M.bottom])
  .separation((a, b) => a.parent === b.parent ? 1.15 : 1.5);
treeLayout(root);

// Main transform group
const g = svg.append("g")
  .attr("class", "tree-root")
  .attr("transform", `translate(${M.left},${M.top})`);

// ── Generation spine — left margin labels ────────────────────────
// Map from depth → first y-position seen for that generation
const genYmap = new Map();
root.each(d => {
  if (!genYmap.has(d.depth)) genYmap.set(d.depth, d.y);
});

const spineG = svg.append("g")
  .attr("class", "gen-spine")
  .attr("transform", `translate(${M.left},${M.top})`);

// Horizontal separator lines — dark gold rules
root.each(d => {
  if (!genYmap.has(d.depth)) return; // deduped — only first time
  const y = genYmap.get(d.depth);
  // faint gold rule at each generation band
  spineG.append("line")
    .attr("x1", -M.left + SPINE).attr("x2", W - M.left - M.right)
    .attr("y1", y).attr("y2", y)
    .attr("stroke", "#d4a458")
    .attr("stroke-width", 0.4)
    .attr("stroke-dasharray", "3,8")
    .attr("opacity", 0.2);
  genYmap.set(d.depth, null); // mark used
});

// Re-build genYmap fresh for labels
const genYlabel = new Map();
root.each(d => {
  if (!genYlabel.has(d.depth)) genYlabel.set(d.depth, d.y);
});

genYlabel.forEach((y, depth) => {
  // Generation spine labels — gold italic serif on dark
  spineG.append("text")
    .attr("x", -M.left + SPINE - 8)
    .attr("y", y + 4)
    .attr("text-anchor", "end")
    .attr("font-family", "'Cormorant Garamond', Georgia, serif")
    .attr("font-size", "11px")
    .attr("font-weight", "600")
    .attr("font-style", "italic")
    .attr("letter-spacing", "0.02em")
    .attr("fill", "#a07840")
    .attr("opacity", "0.8")
    .text(`G${depth + 1}`);
});

// ── Links ───────────────────────────────────────────────────────
// Custom curved links: elbow (straight horizontal + straight vertical) for archival feel
// We use a custom path: from parent center-bottom to child center-top via cubic bezier
g.append("g")
  .attr("class", "links")
  .selectAll("path")
  .data(root.links())
  .enter()
  .append("path")
  .attr("fill", "none")
  .attr("stroke", d => {
    // Connection lines — warm gold for old gens, cooling to silver-blue for modern
    const depth = d.source.depth;
    if (depth < 4) return '#b08030';   // rich gold — ancient lineage
    if (depth < 8) return '#906820';   // darker gold — middle generations
    if (depth < 11) return '#705860';  // bronze-mauve — transition
    return '#506070';                  // steel — modern
  })
  .attr("stroke-width", d => d.source.depth < 5 ? 1.6 : 1.2)
  .attr("stroke-opacity", 0.45)
  .attr("d", d => {
    const sx = d.source.x, sy = d.source.y + NH/2;
    const tx = d.target.x, ty = d.target.y - NH/2;
    const midY = (sy + ty) / 2;
    return `M${sx},${sy} C${sx},${midY} ${tx},${midY} ${tx},${ty}`;
  });

// ── Nodes ───────────────────────────────────────────────────────
const nodeGroups = g.append("g")
  .attr("class", "nodes")
  .selectAll("g.tree-node")
  .data(root.descendants())
  .enter()
  .append("g")
  .attr("class", d => `tree-node gen-${d.depth}`)
  .attr("transform", d => `translate(${d.x},${d.y})`)
  .attr("role", "button")
  .attr("tabindex", d => d.data.id ? "0" : null)
  .attr("aria-label", d => `${d.data.name}, ${d.data.dates}`)
  .style("cursor", d => d.data.id ? "pointer" : "default")
  .on("click", (event, d) => {
    if (!d.data.id) return;
    const el = document.getElementById(d.data.id);
    if (!el) return;
    if (el.tagName === 'DETAILS') el.open = true;
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.style.transition = 'background-color 0.4s ease, box-shadow 0.4s ease';
    el.style.backgroundColor = 'rgba(212, 164, 88, 0.12)';
    el.style.boxShadow = '-3px 0 16px rgba(212, 164, 88, 0.15)';
    setTimeout(() => {
      el.style.backgroundColor = '';
      el.style.boxShadow = '';
    }, 1800);
  })
  .on("keydown", (event, d) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (!d.data.id) return;
      const el = document.getElementById(d.data.id);
      if (!el) return;
      if (el.tagName === 'DETAILS') el.open = true;
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });

// Group everything inside for the hover filter
const cardG = nodeGroups.append("g").attr("class", "node-card");

// Shadow rect — deep drop shadow for dark cards (lift effect)
cardG.append("rect")
  .attr("x", -NW/2 + 3).attr("y", -NH/2 + 4)
  .attr("width", NW).attr("height", NH)
  .attr("rx", 7).attr("ry", 7)
  .attr("fill", "rgba(0,0,0,0.5)");

// Main card rect with gradient fill
cardG.append("rect")
  .attr("x", -NW/2).attr("y", -NH/2)
  .attr("width", NW).attr("height", NH)
  .attr("rx", 7).attr("ry", 7)
  .attr("fill", d => nodeFill(d))
  .attr("stroke", d => confidenceStroke(d.data.confidence))
  .attr("stroke-width", d => confidenceStrokeWidth(d.data.confidence))
  .attr("stroke-dasharray", d => confidenceDash(d.data.confidence));

// Thin highlight line at top edge — gives dimension on dark surface
cardG.append("rect")
  .attr("x", -NW/2 + 2).attr("y", -NH/2 + 1)
  .attr("width", NW - 4).attr("height", 1)
  .attr("rx", 1)
  .attr("fill", "rgba(255,255,255,0.12)");

// ── PORTRAIT RENDERING ───────────────────────────────────────────
// Renders a circular framed portrait on the left side of the card
// for nodes that have portrait_url; otherwise the card stays text-only.
nodeGroups.filter(d => d.data.portrait_url)
  .each(function(d, nodeIdx) {
    const sg = d3.select(this).select('.node-card');
    const clipId = 'pc-' + nodeIdx;

    // Register circular clip path in defs
    defs.append('clipPath')
      .attr('id', clipId)
      .append('circle')
      .attr('cx', PORT_X).attr('cy', 0)
      .attr('r', PORT_R);

    // Outer glow halo
    sg.append('circle')
      .attr('cx', PORT_X).attr('cy', 0)
      .attr('r', PORT_R + 5)
      .attr('fill', 'none')
      .attr('stroke', 'rgba(212,164,88,0.12)')
      .attr('stroke-width', 2);

    // Gold frame ring
    sg.append('circle')
      .attr('cx', PORT_X).attr('cy', 0)
      .attr('r', PORT_R + 2)
      .attr('fill', 'none')
      .attr('stroke', '#d4a458')
      .attr('stroke-width', 1.8);

    // Portrait image clipped to circle
    sg.append('image')
      .attr('href', d.data.portrait_url)
      .attr('x', PORT_X - PORT_R)
      .attr('y', -PORT_R)
      .attr('width', PORT_R * 2)
      .attr('height', PORT_R * 2)
      .attr('clip-path', 'url(#' + clipId + ')')
      .attr('preserveAspectRatio', 'xMidYMid slice')
      .attr('filter', 'url(#portrait-drop)');

    // Inner shadow ring for depth
    sg.append('circle')
      .attr('cx', PORT_X).attr('cy', 0)
      .attr('r', PORT_R)
      .attr('fill', 'none')
      .attr('stroke', 'rgba(0,0,0,0.45)')
      .attr('stroke-width', 1.5);
  });

// ── HUGE ? CONFIDENCE BADGES ────────────────────────────────────
// UNVERIFIED: amber overlay strip + "UNVERIFIED" banner text + large "?"
nodeGroups.filter(d => d.data.confidence === 'unverified')
  .each(function(d) {
    const sg = d3.select(this).select('.node-card');

    // Red-amber full-card tint
    sg.append('rect')
      .attr('x', -NW/2).attr('y', -NH/2)
      .attr('width', NW).attr('height', NH)
      .attr('rx', 7).attr('ry', 7)
      .attr('fill', 'rgba(180,60,40,0.09)')
      .attr('pointer-events', 'none');

    // Top banner strip
    sg.append('rect')
      .attr('x', -NW/2).attr('y', -NH/2)
      .attr('width', NW).attr('height', 18)
      .attr('rx', 7).attr('ry', 0)
      .attr('fill', 'rgba(180,60,40,0.32)')
      .attr('pointer-events', 'none');
    sg.append('rect')
      .attr('x', -NW/2).attr('y', -NH/2 + 10)
      .attr('width', NW).attr('height', 8)
      .attr('fill', 'rgba(180,60,40,0.32)')
      .attr('pointer-events', 'none');

    sg.append('text')
      .attr('x', 0).attr('y', -NH/2 + 13)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Lora', Georgia, serif")
      .attr('font-size', '8px')
      .attr('font-weight', '700')
      .attr('letter-spacing', '0.16em')
      .attr('fill', '#e09888')
      .attr('pointer-events', 'none')
      .text('UNVERIFIED — NEEDS RESEARCH');

    // Large "?" bottom-right — 34px serif, gold glow
    sg.append('text')
      .attr('x', NW/2 - 16).attr('y', NH/2 - 5)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Cormorant Garamond', Georgia, serif")
      .attr('font-size', '34px')
      .attr('font-weight', '700')
      .attr('fill', '#d4a458')
      .attr('filter', 'url(#q-badge-glow)')
      .attr('opacity', '0.92')
      .attr('pointer-events', 'none')
      .text('?');

    sg.append('title')
      .text('Confidence: UNVERIFIED — genealogical descent not confirmed. Needs primary source research.');
  });

// POSSIBLE: amber card tint + large gold "?" with glow
nodeGroups.filter(d => d.data.confidence === 'possible')
  .each(function(d) {
    const sg = d3.select(this).select('.node-card');

    // Subtle amber tint
    sg.append('rect')
      .attr('x', -NW/2).attr('y', -NH/2)
      .attr('width', NW).attr('height', NH)
      .attr('rx', 7).attr('ry', 7)
      .attr('fill', 'rgba(200,130,40,0.06)')
      .attr('pointer-events', 'none');

    // Large "?" — 38px, gold, bottom-right, prominent glow
    sg.append('text')
      .attr('x', NW/2 - 16).attr('y', NH/2 - 4)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Cormorant Garamond', Georgia, serif")
      .attr('font-size', '38px')
      .attr('font-weight', '700')
      .attr('fill', '#d4a458')
      .attr('filter', 'url(#q-badge-glow)')
      .attr('opacity', '0.95')
      .attr('pointer-events', 'none')
      .text('?');

    sg.append('title')
      .text('Confidence: POSSIBLE — one source / circumstantial. Treat as working hypothesis.');
  });

// ── Node text ────────────────────────────────────────────────────
// Text shifts right when a portrait is present on the left

// Name line
cardG.append("text")
  .attr("x", d => d.data.portrait_url ? (TEXT_X_PORT - NW/2 + PORT_R) : 0)
  .attr("y", -16)
  .attr("text-anchor", d => d.data.portrait_url ? "start" : "middle")
  .attr("font-family", "'Cormorant Garamond', 'Lora', Georgia, serif")
  .attr("font-weight", "700")
  .attr("font-size", "13px")
  .attr("letter-spacing", "0.01em")
  .attr("fill", d => nodeTextColor(d.depth))
  .text(d => truncate(d.data.name, d.data.portrait_url ? 21 : 28));

// Dates — monospaced
cardG.append("text")
  .attr("x", d => d.data.portrait_url ? (TEXT_X_PORT - NW/2 + PORT_R) : 0)
  .attr("y", -1)
  .attr("text-anchor", d => d.data.portrait_url ? "start" : "middle")
  .attr("font-family", "'Source Code Pro', 'Courier New', monospace")
  .attr("font-size", "10.5px")
  .attr("letter-spacing", "0.02em")
  .attr("fill", d => nodeDateColor(d.depth))
  .text(d => d.data.dates);

// Fact line — italic
cardG.append("text")
  .attr("x", d => d.data.portrait_url ? (TEXT_X_PORT - NW/2 + PORT_R) : 0)
  .attr("y", 14)
  .attr("text-anchor", d => d.data.portrait_url ? "start" : "middle")
  .attr("font-family", "'Lora', Georgia, serif")
  .attr("font-style", "italic")
  .attr("font-size", "9.5px")
  .attr("fill", d => nodeFactColor(d.depth))
  .text(d => truncate(d.data.fact, d.data.portrait_url ? 28 : 38));

// Spouse line — when present
cardG.filter(d => d.data.spouse).append("text")
  .attr("x", d => d.data.portrait_url ? (TEXT_X_PORT - NW/2 + PORT_R) : 0)
  .attr("y", 28)
  .attr("text-anchor", d => d.data.portrait_url ? "start" : "middle")
  .attr("font-family", "'Lora', Georgia, serif")
  .attr("font-size", "9px")
  .attr("fill", d => nodeFactColor(d.depth))
  .text(d => "m. " + truncate(d.data.spouse, d.data.portrait_url ? 26 : 36));

// ── Generation badge (top-left diamond) ─────────────────────────
const badgeX = -NW/2 + 11;
const badgeY = -NH/2 + 11;

// Diamond shape — gold on dark
const DIAMOND = `M${badgeX},${badgeY - 9} L${badgeX + 9},${badgeY} L${badgeX},${badgeY + 9} L${badgeX - 9},${badgeY} Z`;
cardG.append("path")
  .attr("d", DIAMOND)
  .attr("fill", "rgba(0,0,0,0.4)")
  .attr("stroke", d => d.depth < 7 ? "rgba(212,164,88,0.5)" : "rgba(180,180,200,0.3)")
  .attr("stroke-width", 1.0);

cardG.append("text")
  .attr("x", badgeX).attr("y", badgeY + 3.5)
  .attr("text-anchor", "middle")
  .attr("font-family", "'Cormorant Garamond', Georgia, serif")
  .attr("font-size", "9px")
  .attr("font-weight", "600")
  .attr("fill", d => d.depth < 7 ? '#d4a458' : '#9aacbc')
  .text(d => (d.data.generation || d.depth + 1));

// ── Sibling badge (top-right) ────────────────────────────────────
nodeGroups.filter(d => d.data.siblings && d.data.siblings.length > 0)
  .each(function(d) {
    const sg = d3.select(this).select('.node-card');
    const bx = NW/2 - 11;
    const by = -NH/2 + 11;

    sg.append("circle")
      .attr("cx", bx).attr("cy", by)
      .attr("r", 10)
      .attr("fill", "rgba(212,164,88,0.25)")
      .attr("stroke", "#d4a458")
      .attr("stroke-width", 1.0);

    sg.append("text")
      .attr("x", bx).attr("y", by + 3.5)
      .attr("text-anchor", "middle")
      .attr("font-family", "'Cormorant Garamond', Georgia, serif")
      .attr("font-size", "9.5px")
      .attr("font-weight", "700")
      .attr("fill", "#e8c878")
      .text("+" + d.data.siblings.length);

    sg.append("title")
      .text("Siblings: " + d.data.siblings.map(s => `${s.name} (${s.dates})`).join(", "));
  });

// ── Hover: gold glow + scale ─────────────────────────────────────
nodeGroups.on("mouseenter", function(event, d) {
  d3.select(this).select(".node-card")
    .style("filter", "url(#node-shadow)")
    .attr("transform", "scale(1.04)");
}).on("mouseleave", function() {
  d3.select(this).select(".node-card")
    .style("filter", null)
    .attr("transform", null);
});

// ── Utility ─────────────────────────────────────────────────────
function truncate(s, n) {
  if (!s) return "";
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

// ── Zoom & Pan ───────────────────────────────────────────────────
const zoomBehavior = d3.zoom()
  .scaleExtent([0.3, 4])
  .on("zoom", event => {
    g.attr("transform",
      `translate(${M.left + event.transform.x},${M.top + event.transform.y}) scale(${event.transform.k})`);
    spineG.attr("transform",
      `translate(${M.left + event.transform.x},${M.top + event.transform.y}) scale(${event.transform.k})`);
  });

svg.call(zoomBehavior)
   .on("dblclick.zoom", null); // disable dblclick zoom (annoying on text)

window.treeZoomIn    = () => svg.transition().duration(280).call(zoomBehavior.scaleBy, 1.35);
window.treeZoomOut   = () => svg.transition().duration(280).call(zoomBehavior.scaleBy, 1/1.35);
window.treeZoomReset = () => svg.transition().duration(420).call(zoomBehavior.transform, d3.zoomIdentity);

// ── Auto-fit on load ─────────────────────────────────────────────
// Compute fit-scale in VIEWBOX coordinates (the SVG's preserveAspectRatio
// already handles the viewBox→screen mapping; the zoom transform multiplies
// on top of that, so we need to think in viewBox units here).
function autoFitTree() {
  const bbox = g.node().getBBox();
  const padding = 40;
  const scaleX = (W - 2 * padding) / bbox.width;
  const scaleY = (H - 2 * padding) / bbox.height;
  const scale = Math.min(scaleX, scaleY, 1.0);  // never zoom in past 1.0
  // Center the tree inside the viewBox
  const tx = (W - bbox.width * scale) / 2 - bbox.x * scale - M.left;
  const ty = (H - bbox.height * scale) / 2 - bbox.y * scale - M.top;
  svg.call(zoomBehavior.transform,
    d3.zoomIdentity.translate(tx, ty).scale(scale));
}

window.addEventListener('load', () => setTimeout(autoFitTree, 120));
"""


def render_secondary_trees_js():
    """Return D3 initialization JS for all secondary family-line tree cards."""
    return r"""
// ── Secondary Family-Line Trees ──────────────────────────────────
// Renders every non-primary lineage from research/lineage-tree-multi.json
// as an interactive SVG tree card with its own zoom controls.

(function renderSecondaryLineageTrees() {
  const dataEl = document.getElementById('secondary-lineage-data');
  if (!dataEl || typeof d3 === 'undefined') return;

  let familyLines = [];
  try {
    familyLines = JSON.parse(dataEl.textContent || '[]');
  } catch (err) {
    console.warn('Could not parse secondary lineage data', err);
    return;
  }

  const controllers = [];
  const CARD_W = 218;
  const CARD_H = 84;
  const palette = [
    ['#3a2208', '#281804'],
    ['#4a2b0c', '#332006'],
    ['#563512', '#3c280c'],
    ['#5a4222', '#413219'],
    ['#3f3a35', '#2e2a28'],
    ['#2e3442', '#222733'],
    ['#25354a', '#18263a'],
    ['#1c304e', '#10223c'],
  ];

  function truncate(value, max) {
    const s = value == null ? '' : String(value);
    return s.length > max ? s.slice(0, max - 1) + '…' : s;
  }

  function normalizeConfidence(value) {
    const s = String(value || 'unknown').toLowerCase();
    if (s.includes('confirmed')) return 'confirmed';
    if (s.includes('probable')) return 'probable';
    if (s.includes('possible')) return 'possible';
    if (s.includes('unverified')) return 'unverified';
    if (s.includes('living')) return 'living';
    return 'unknown';
  }

  function confidenceStroke(conf) {
    const c = normalizeConfidence(conf);
    if (c === 'confirmed') return '#d4a458';
    if (c === 'probable') return '#b8826a';
    if (c === 'possible') return '#c07060';
    if (c === 'unverified') return '#a05040';
    if (c === 'living') return '#7a9ab8';
    return '#5a5048';
  }

  function confidenceDash(conf) {
    const c = normalizeConfidence(conf);
    if (c === 'unknown') return '4,3';
    if (c === 'possible') return '6,3';
    if (c === 'unverified') return '5,3,2,3';
    return 'none';
  }

  function nodeFill(defs, prefix, d) {
    const c = normalizeConfidence(d.data.confidence);
    if (d.data.name === '[living relative]') return `url(#${prefix}-private)`;
    if (c === 'unknown' || c === 'possible' || c === 'unverified') return `url(#${prefix}-paper)`;
    const idx = Math.min(d.depth, palette.length - 1);
    return `url(#${prefix}-g-${idx})`;
  }

  function nodeTextColor(d) {
    if (d.data.name === '[living relative]') return '#d7e2ee';
    return d.depth < 4 ? '#fff3d8' : '#f5f7fc';
  }

  function nodeDateColor(d) {
    if (d.data.name === '[living relative]') return '#9fb8cf';
    return d.depth < 4 ? '#f0c060' : '#a8c0e0';
  }

  function nodeFactColor(d) {
    if (d.data.name === '[living relative]') return '#8da4ba';
    return d.depth < 4 ? '#d8a070' : '#9aa8c8';
  }

  function scrollToEntity(d) {
    if (!d.data.id) return;
    const el = document.getElementById(d.data.id);
    if (!el) return;
    if (el.tagName === 'DETAILS') el.open = true;
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.style.transition = 'background-color 0.4s ease, box-shadow 0.4s ease';
    el.style.backgroundColor = 'rgba(212, 164, 88, 0.12)';
    el.style.boxShadow = '0 0 0 1px rgba(212, 164, 88, 0.26), 0 0 16px rgba(212, 164, 88, 0.15)';
    setTimeout(() => {
      el.style.backgroundColor = '';
      el.style.boxShadow = '';
    }, 1800);
  }

  function appendDefs(svg, prefix) {
    const defs = svg.append('defs');

    const glow = defs.append('filter')
      .attr('id', `${prefix}-node-glow`)
      .attr('x', '-35%').attr('y', '-35%')
      .attr('width', '170%').attr('height', '170%');
    glow.append('feDropShadow')
      .attr('dx', 0).attr('dy', 0)
      .attr('stdDeviation', 5)
      .attr('flood-color', '#d4a458')
      .attr('flood-opacity', 0.42);

    const qGlow = defs.append('filter')
      .attr('id', `${prefix}-q-glow`)
      .attr('x', '-80%').attr('y', '-80%')
      .attr('width', '360%').attr('height', '360%');
    qGlow.append('feDropShadow')
      .attr('dx', 0).attr('dy', 0)
      .attr('stdDeviation', 2.8)
      .attr('flood-color', '#d4a458')
      .attr('flood-opacity', 0.72);

    function gradient(id, top, bottom) {
      const g = defs.append('linearGradient')
        .attr('id', id)
        .attr('x1', '0%').attr('y1', '0%')
        .attr('x2', '0%').attr('y2', '100%');
      g.append('stop').attr('offset', '0%').attr('stop-color', top);
      g.append('stop').attr('offset', '100%').attr('stop-color', bottom);
    }

    palette.forEach((pair, i) => gradient(`${prefix}-g-${i}`, pair[0], pair[1]));
    gradient(`${prefix}-paper`, '#1a1510', '#221c14');
    gradient(`${prefix}-private`, '#182432', '#101923');
    return defs;
  }

  function renderLine(line, index) {
    const svg = d3.select(`#secondary-tree-svg-${index}`);
    if (svg.empty() || !line.tree) return;
    svg.selectAll('*').remove();

    const root = d3.hierarchy(line.tree);
    const leaves = Math.max(root.leaves().length, 2);
    const levels = Math.max(root.height + 1, 2);
    const W = Math.max(900, leaves * 255 + 160);
    const H = Math.max(520, levels * 152 + 120);
    const margin = { top: 56, right: 56, bottom: 70, left: 84 };
    const prefix = `secondary-line-${index}`;

    svg.attr('viewBox', `0 0 ${W} ${H}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .attr('width', '100%');

    const defs = appendDefs(svg, prefix);
    const treeLayout = d3.tree()
      .size([W - margin.left - margin.right, H - margin.top - margin.bottom])
      .separation((a, b) => a.parent === b.parent ? 1.18 : 1.55);
    treeLayout(root);

    const g = svg.append('g')
      .attr('class', 'secondary-tree-root')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const bandG = svg.append('g')
      .attr('class', 'secondary-tree-bands')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    const depthY = new Map();
    root.each(d => {
      if (!depthY.has(d.depth)) depthY.set(d.depth, d.y);
    });
    depthY.forEach((y, depth) => {
      bandG.append('line')
        .attr('x1', -margin.left + 48)
        .attr('x2', W - margin.left - margin.right)
        .attr('y1', y)
        .attr('y2', y)
        .attr('stroke', '#d4a458')
        .attr('stroke-width', 0.35)
        .attr('stroke-dasharray', '3,8')
        .attr('opacity', 0.22);
      bandG.append('text')
        .attr('x', -margin.left + 42)
        .attr('y', y + 4)
        .attr('text-anchor', 'end')
        .attr('font-family', "'Cormorant Garamond', Georgia, serif")
        .attr('font-size', '11px')
        .attr('font-style', 'italic')
        .attr('font-weight', '600')
        .attr('fill', '#a07840')
        .attr('opacity', 0.8)
        .text(`G${depth + 1}`);
    });

    g.append('g')
      .attr('class', 'links')
      .selectAll('path')
      .data(root.links())
      .enter()
      .append('path')
      .attr('fill', 'none')
      .attr('stroke', d => d.source.depth < 4 ? '#a87830' : '#506070')
      .attr('stroke-width', d => d.source.depth < 4 ? 1.45 : 1.15)
      .attr('stroke-opacity', 0.48)
      .attr('d', d => {
        const sx = d.source.x;
        const sy = d.source.y + CARD_H / 2;
        const tx = d.target.x;
        const ty = d.target.y - CARD_H / 2;
        const midY = (sy + ty) / 2;
        return `M${sx},${sy} C${sx},${midY} ${tx},${midY} ${tx},${ty}`;
      });

    const nodeGroups = g.append('g')
      .attr('class', 'nodes')
      .selectAll('g.secondary-tree-node')
      .data(root.descendants())
      .enter()
      .append('g')
      .attr('class', d => `secondary-tree-node tree-node gen-${Math.min(d.depth, 13)}`)
      .attr('transform', d => `translate(${d.x},${d.y})`)
      .attr('role', d => d.data.id ? 'button' : 'img')
      .attr('tabindex', d => d.data.id ? '0' : null)
      .attr('aria-label', d => `${d.data.name || 'Unknown person'}, ${d.data.dates || 'dates unknown'}`)
      .style('cursor', d => d.data.id ? 'pointer' : 'default')
      .on('click', (event, d) => scrollToEntity(d))
      .on('keydown', (event, d) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          scrollToEntity(d);
        }
      });

    const card = nodeGroups.append('g').attr('class', 'node-card');
    card.append('rect')
      .attr('x', -CARD_W / 2 + 3)
      .attr('y', -CARD_H / 2 + 4)
      .attr('width', CARD_W)
      .attr('height', CARD_H)
      .attr('rx', 7).attr('ry', 7)
      .attr('fill', 'rgba(0,0,0,0.45)');

    card.append('rect')
      .attr('x', -CARD_W / 2)
      .attr('y', -CARD_H / 2)
      .attr('width', CARD_W)
      .attr('height', CARD_H)
      .attr('rx', 7).attr('ry', 7)
      .attr('fill', d => nodeFill(defs, prefix, d))
      .attr('stroke', d => confidenceStroke(d.data.confidence))
      .attr('stroke-width', d => normalizeConfidence(d.data.confidence) === 'confirmed' ? 1.9 : 1.55)
      .attr('stroke-dasharray', d => confidenceDash(d.data.confidence));

    card.append('rect')
      .attr('x', -CARD_W / 2 + 2)
      .attr('y', -CARD_H / 2 + 1)
      .attr('width', CARD_W - 4)
      .attr('height', 1)
      .attr('rx', 1)
      .attr('fill', 'rgba(255,255,255,0.12)');

    card.filter(d => ['possible', 'unverified'].includes(normalizeConfidence(d.data.confidence)))
      .append('text')
      .attr('x', CARD_W / 2 - 16)
      .attr('y', CARD_H / 2 - 5)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Cormorant Garamond', Georgia, serif")
      .attr('font-size', d => normalizeConfidence(d.data.confidence) === 'unverified' ? '31px' : '36px')
      .attr('font-weight', '700')
      .attr('fill', '#d4a458')
      .attr('filter', `url(#${prefix}-q-glow)`)
      .attr('pointer-events', 'none')
      .text('?');

    const badgeX = -CARD_W / 2 + 12;
    const badgeY = -CARD_H / 2 + 12;
    card.append('path')
      .attr('d', `M${badgeX},${badgeY - 9} L${badgeX + 9},${badgeY} L${badgeX},${badgeY + 9} L${badgeX - 9},${badgeY} Z`)
      .attr('fill', 'rgba(0,0,0,0.36)')
      .attr('stroke', d => d.depth < 5 ? 'rgba(212,164,88,0.5)' : 'rgba(180,180,200,0.3)')
      .attr('stroke-width', 1);
    card.append('text')
      .attr('x', badgeX)
      .attr('y', badgeY + 3.5)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Cormorant Garamond', Georgia, serif")
      .attr('font-size', '9px')
      .attr('font-weight', '600')
      .attr('fill', d => d.depth < 5 ? '#d4a458' : '#9aacbc')
      .text(d => d.data.generation || d.depth + 1);

    card.append('text')
      .attr('x', 0)
      .attr('y', -19)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Cormorant Garamond', 'Lora', Georgia, serif")
      .attr('font-weight', '700')
      .attr('font-size', '13px')
      .attr('letter-spacing', '0.01em')
      .attr('fill', d => nodeTextColor(d))
      .text(d => truncate(d.data.name, 29));

    card.append('text')
      .attr('x', 0)
      .attr('y', -3)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Source Code Pro', 'Courier New', monospace")
      .attr('font-size', '10px')
      .attr('letter-spacing', '0.02em')
      .attr('fill', d => nodeDateColor(d))
      .text(d => truncate(d.data.dates || 'dates pending', 30));

    card.append('text')
      .attr('x', 0)
      .attr('y', 13)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Lora', Georgia, serif")
      .attr('font-style', 'italic')
      .attr('font-size', '9.2px')
      .attr('fill', d => nodeFactColor(d))
      .text(d => truncate(d.data.fact, 42));

    card.filter(d => d.data.spouse)
      .append('text')
      .attr('x', 0)
      .attr('y', 29)
      .attr('text-anchor', 'middle')
      .attr('font-family', "'Lora', Georgia, serif")
      .attr('font-size', '8.8px')
      .attr('fill', d => nodeFactColor(d))
      .text(d => 'm. ' + truncate(d.data.spouse, 39));

    card.append('title')
      .text(d => {
        const bits = [
          d.data.name,
          d.data.dates,
          `Confidence: ${normalizeConfidence(d.data.confidence).toUpperCase()}`,
          d.data.spouse ? `Spouse: ${d.data.spouse}` : '',
          d.data.fact || '',
        ].filter(Boolean);
        return bits.join('\n');
      });

    nodeGroups.on('mouseenter', function() {
      d3.select(this).select('.node-card')
        .style('filter', `url(#${prefix}-node-glow)`)
        .attr('transform', 'scale(1.035)');
    }).on('mouseleave', function() {
      d3.select(this).select('.node-card')
        .style('filter', null)
        .attr('transform', null);
    });

    const zoomBehavior = d3.zoom()
      .scaleExtent([0.35, 4])
      .on('zoom', event => {
        g.attr('transform',
          `translate(${margin.left + event.transform.x},${margin.top + event.transform.y}) scale(${event.transform.k})`);
        bandG.attr('transform',
          `translate(${margin.left + event.transform.x},${margin.top + event.transform.y}) scale(${event.transform.k})`);
      });

    svg.call(zoomBehavior).on('dblclick.zoom', null);

    function fit() {
      const bbox = g.node().getBBox();
      const padding = 44;
      const scaleX = (W - 2 * padding) / Math.max(bbox.width, 1);
      const scaleY = (H - 2 * padding) / Math.max(bbox.height, 1);
      const scale = Math.min(scaleX, scaleY, 1);
      const tx = (W - bbox.width * scale) / 2 - bbox.x * scale - margin.left;
      const ty = (H - bbox.height * scale) / 2 - bbox.y * scale - margin.top;
      svg.transition().duration(260).call(
        zoomBehavior.transform,
        d3.zoomIdentity.translate(tx, ty).scale(scale)
      );
    }

    controllers[index] = {
      zoomIn: () => svg.transition().duration(240).call(zoomBehavior.scaleBy, 1.32),
      zoomOut: () => svg.transition().duration(240).call(zoomBehavior.scaleBy, 1 / 1.32),
      reset: fit,
    };

    setTimeout(fit, 100 + index * 40);
  }

  window.secondaryTreeZoomIn = index => controllers[index] && controllers[index].zoomIn();
  window.secondaryTreeZoomOut = index => controllers[index] && controllers[index].zoomOut();
  window.secondaryTreeZoomReset = index => controllers[index] && controllers[index].reset();

  familyLines.forEach(renderLine);
})();
"""


def build_html(family_only=True):
    turns = load_transcript()
    entities = load_entities()
    research = load_research()
    portrait_map = load_portraits()
    deeds_map = load_deeds()

    redact_set = set() if family_only else set(entities.get("audience_policy", {}).get("redaction_set", []))
    redact_living_names = not family_only
    public_redaction_terms = set() if family_only else collect_public_research_redaction_terms(entities, redact_set)

    entity_index = build_entity_index(entities)

    # People grouped by family layer
    people = entities.get("people", [])
    deceased = [p for p in people if not p.get("living_flag") and not p.get("redact_in_public")]
    living = [p for p in people if p.get("living_flag") and not p.get("redact_in_public")]

    people_html = []
    if deceased:
        people_html.append("<h3>Ancestors &amp; Historical Family</h3>")
        for p in sorted(deceased, key=lambda x: x.get("birth_year") or 9999):
            people_html.append(render_person_card(p, redact=redact_living_names,
                                                   portrait_map=portrait_map,
                                                   deeds_map=deeds_map,
                                                   public_redaction_terms=public_redaction_terms))
    if living and family_only:
        people_html.append("<h3>Living Family</h3>")
        for p in living:
            people_html.append(render_person_card(p, redact=False,
                                                   portrait_map=portrait_map,
                                                   deeds_map=deeds_map,
                                                   public_redaction_terms=public_redaction_terms))

    places_html = "\n".join(render_place_card(pl) for pl in entities.get("places", []))
    events_html = "\n".join(render_event_card(e) for e in sorted(
        entities.get("events", []),
        key=lambda e: re.search(r"(\d{4})", str(e.get("date_or_year") or "")).group(1) if re.search(r"\d{4}", str(e.get("date_or_year") or "")) else "9999"
    ))

    research_html = render_research_sections(
        research,
        family_only=family_only,
        redaction_terms=public_redaction_terms,
    )

    open_questions = entities.get("open_questions", [])
    oq_html = ""
    if open_questions:
        items = "\n".join(f"<li>{html.escape(q)}</li>" for q in open_questions)
        oq_html = f"""<div class="callout">
  <strong>Open questions for the family:</strong>
  <ul>{items}</ul>
</div>"""

    transcript_html = render_transcript(turns, entity_index, redact_set)  # legacy, unused now
    notable_stories_html = render_notable_stories()
    lineage_tree_html = render_lineage_tree_section(
        portrait_map=portrait_map,
        family_only=family_only,
        redaction_set=redact_set,
        public_redaction_terms=public_redaction_terms,
    )
    secondary_trees_html = render_secondary_trees_section(
        family_only=family_only,
        redaction_set=redact_set,
        public_redaction_terms=public_redaction_terms,
    )
    migration_map_html = render_migration_map_section(deeds_map=deeds_map)

    title = "Grandma Shari — The Mattingly Family History"
    if not family_only:
        title += " (Public Edition)"

    out = f"""<!DOCTYPE html>
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
  </style>
</head>
<body>
  <div class="container">

    <header class="cover">
      <!-- Cinematic dust particles — CSS animation, no JS -->
      <div class="cover-particles" aria-hidden="true">
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
      </div>
      <!-- Animated hero glow -->
      <div class="cover-glow" aria-hidden="true"></div>

      <p class="cover-eyebrow">The Mattingly Family History</p>
      <h1><em>Grandma Shari</em></h1>
      <span class="cover-ornament" aria-hidden="true">&#10022; &nbsp; &#10022; &nbsp; &#10022;</span>
      <hr class="cover-rule" aria-hidden="true">
      <div class="subtitle">A spoken record of fourteen generations.</div>
      <div class="meta">
        <strong>Subject:</strong> Shari (age 79) &ensp;&middot;&ensp;
        <strong>Interviewer:</strong> Hunter (grandson)<br>
        Recorded April 25, 2026 &ensp;&middot;&ensp; Santa Monica, California &ensp;&middot;&ensp; 46 minutes
      </div>
      <div class="audio-wrapper">
        <audio controls src="{AUDIO_REL}" aria-label="Family history interview audio recording"></audio>
      </div>
    </header>

    <nav class="toc">
      <strong>Contents</strong>
      <ul>
        <li><a href="#lineage">Family Tree</a></li>
        <li><a href="#secondary-trees">Family Lines</a></li>
        <li><a href="#timeline">Timeline</a></li>
        <li><a href="#map">Migration Map</a></li>
        <li><a href="#stories">Notable Stories</a></li>
        <li><a href="#cast">People</a></li>
        <li><a href="#places">Places</a></li>
        <li><a href="#events">Events</a></li>
        <li><a href="#research">Research</a></li>
      </ul>
    </nav>

    {lineage_tree_html}

    {secondary_trees_html}

    <section id="timeline">
      <h2>Timeline</h2>
      <p>Four centuries of family events alongside the broader sweep of history. Drag horizontally to explore.</p>
      <div id="timeline-container"></div>
    </section>

    {migration_map_html}

    <section id="stories">
      <h2>Notable Stories from the Family</h2>
      <p>Verifiable accounts of what your ancestors actually did — drawn from primary sources, county histories, newspaper archives, and genealogical records. Each story has at least one source URL you can verify yourself.</p>
      {notable_stories_html}
    </section>

    <section id="cast">
      <h2>People (Cast of Characters)</h2>
      {''.join(people_html)}
    </section>

    <section id="places">
      <h2>Places</h2>
      {places_html}
    </section>

    <section id="events">
      <h2>Events</h2>
      {events_html}
    </section>

    <section id="research">
      <h2>Research & Sources</h2>
      <p>Findings from web research, genealogical databases, newspaper archives, and historical records. Confidence levels: <span class="confidence confidence-confirmed">CONFIRMED</span> = 3+ sources, <span class="confidence confidence-probable">PROBABLE</span> = 2 sources, <span class="confidence confidence-possible">POSSIBLE</span> = 1 source.</p>
      {research_html}
    </section>

    {oq_html}

    <footer class="colophon">
      Built {datetime.now().strftime('%B %d, %Y')} from <code>Grandma Shari Family History.m4a</code> ·
      Transcribed via Deepgram Nova-3 (two-pass) ·
      Cleaned by Claude Haiku 4.5 ·
      Entities extracted by Claude Sonnet 4.6 ·
      Research by 5 parallel Sonnet subagents ·
      Built lovingly by Hunter Spence
    </footer>

  </div>

  <!-- D3 for the lineage tree and geo map -->
  <script src="https://unpkg.com/d3@7/dist/d3.min.js"></script>
  <!-- TopoJSON for world-atlas land shapes -->
  <script src="https://unpkg.com/topojson-client@3/dist/topojson-client.min.js"></script>

  <!-- vis-timeline for the timeline -->
  <link rel="stylesheet" href="https://unpkg.com/vis-timeline@7.7.3/styles/vis-timeline-graph2d.min.css">
  <script src="https://unpkg.com/vis-timeline@7.7.3/standalone/umd/vis-timeline-graph2d.min.js"></script>

  <script>
{render_lineage_tree_js()}
{render_secondary_trees_js()}
{render_timeline_js()}
  </script>
</body>
</html>"""
    return out


def render_timeline_js():
    items = [
        {"id": 1, "content": "Mattingly arrives England", "start": "1525-01-01", "group": "family"},
        {"id": 2, "content": "Thomas Mattingly → Maryland w/ Lord Baltimore", "start": "1660-01-01", "group": "family"},
        {"id": 3, "content": "Mattingly families → Kentucky w/ Daniel Boone", "start": "1780-01-01", "end": "1790-01-01", "group": "family"},
        {"id": 4, "content": "Norman Invasion · Domesday", "start": "1066-01-01", "group": "history"},
        {"id": 5, "content": "Cromwell era ends · Restoration", "start": "1660-05-29", "group": "history"},
        {"id": 6, "content": "Civil War · Sherman's march", "start": "1864-11-15", "end": "1865-04-01", "group": "history"},
        {"id": 7, "content": "Pearl Baity NC → Texas", "start": "1875-01-01", "group": "family"},
        {"id": 8, "content": "Aunt Monette born", "start": "1871-01-01", "group": "family"},
        {"id": 9, "content": "Monette meets Mark Twain (Louisiana)", "start": "1887-01-01", "group": "family"},
        {"id": 10, "content": "Spindletop spudded", "start": "1901-01-10", "group": "history"},
        {"id": 11, "content": "Pearl buys Reeves County land", "start": "1901-04-01", "group": "family"},
        {"id": 12, "content": "Leroy Mattingly born", "start": "1898-01-01", "group": "family"},
        {"id": 13, "content": "Aunt Mamie born · mother dies in childbirth", "start": "1901-01-01", "group": "family"},
        {"id": 14, "content": "211 Castile home built", "start": "1905-01-01", "group": "family"},
        {"id": 15, "content": "1904 St Louis World's Fair", "start": "1904-04-30", "end": "1904-12-01", "group": "history"},
        {"id": 16, "content": "Pearl buys Kaiser pavilion set", "start": "1904-01-01", "group": "family"},
        {"id": 17, "content": "Father born", "start": "1922-01-01", "group": "family"},
        {"id": 18, "content": "Mother born", "start": "1923-01-01", "group": "family"},
        {"id": 19, "content": "1929 Crash · family loses fortune", "start": "1929-10-29", "group": "history"},
        {"id": 20, "content": "Claude Mattingly hotel scandal", "start": "1934-01-01", "end": "1935-12-31", "group": "family"},
        {"id": 21, "content": "Great-great-great-grandfather dies at 107", "start": "1935-01-01", "group": "family"},
        {"id": 22, "content": "Pearl's husband dies", "start": "1945-01-01", "group": "family"},
        {"id": 23, "content": "Shari born", "start": "1947-01-01", "group": "family"},
        {"id": 24, "content": "Aunt Monette dies, age 99", "start": "1970-01-01", "group": "family"},
        {"id": 25, "content": "Pearl Baity dies", "start": "1971-01-01", "group": "family"},
        {"id": 26, "content": "Wolfcamp royalties begin", "start": "2010-01-01", "group": "family"},
        {"id": 27, "content": "Interview recorded", "start": "2026-04-25", "group": "family"},
    ]
    items_json = json.dumps(items)
    return f"""
const timelineItems = new vis.DataSet({items_json});
const timelineGroups = new vis.DataSet([
  {{id: 'family', content: 'Family', style: 'background-color: #161210; color: #e2d5c3;'}},
  {{id: 'history', content: 'History', style: 'background-color: #111010; color: #9a8a78;'}},
]);
const timelineContainer = document.getElementById('timeline-container');
if (timelineContainer && window.vis) {{
  new vis.Timeline(timelineContainer, timelineItems, timelineGroups, {{
    start: '1500-01-01',
    end:   '2030-01-01',
    min:   '1000-01-01',
    max:   '2050-01-01',
    stack: true,
    height: '360px',
    margin: {{ item: 8, axis: 12 }},
  }});
}}
"""


def render_migration_map_section(deeds_map=None):
    """Render the cinematic migration map — D3-geo NaturalEarth projection with real
    world-atlas TopoJSON coastlines. Waypoints placed via actual lat/lon.
    deeds_map: {person_id: [deed,...]} — used for popup enrichment (future).
    """
    deeds_map = deeds_map or {}

    # Waypoints: real geographic lat/lon coordinates
    # Order defines the US migration path polyline
    locations_data = [
        {
            "id": "hampshire",
            "name": "Mattingley, Hampshire",
            "country": "England",
            "year": "pre-1660",
            "lat": 51.27, "lon": -1.03,
            "atlantic_origin": True,  # departure point for ocean crossing arc
            "story": "The ancestral village. The Mattingley name derives from this Hampshire settlement, documented since 1167 AD. Thomas and his family departed for the New World c. 1663.",
            "label_anchor": "start",
            "label_dx": 8, "label_dy": -4,
        },
        {
            "id": "maryland",
            "name": "St. Mary's County, Maryland",
            "country": "Colony of Maryland",
            "year": "1663–1780s",
            "lat": 38.20, "lon": -76.65,
            "story": "Thomas Mattingly II arrived with the Catholic colonists under Lord Baltimore. The family received the ‘Mattingly’s Hope’ 300-acre land patent on September 4, 1666. They farmed Charles and St. Mary’s Counties for over a century.",
            "label_anchor": "end",
            "label_dx": -9, "label_dy": -6,
        },
        {
            "id": "kentucky",
            "name": "Bardstown, Kentucky",
            "country": "Kentucky Territory",
            "year": "1780s",
            "lat": 37.81, "lon": -85.47,
            "story": "With Daniel Boone’s trailblazers, Catholic Maryland families migrated south-west into the fertile Kentucky territory. Bardstown became a hub of Catholic settlement — the ‘Holy Land of the West.’ The Mattinglys were among dozens of Catholic families who made this journey.",
            "label_anchor": "start",
            "label_dx": 8, "label_dy": -5,
        },
        {
            "id": "northcarolina",
            "name": "North Carolina",
            "country": "North Carolina",
            "year": "1810–1875",
            "lat": 35.50, "lon": -79.50,
            "story": "Pearl Baity’s branch — the Johnson-Baity family — was rooted in North Carolina before the westward push to Texas. Pearl was born here circa 1860 before her family joined the post-Civil War migration.",
            "label_anchor": "start",
            "label_dx": 8, "label_dy": -4,
        },
        {
            "id": "stlouis",
            "name": "St. Louis, Missouri",
            "country": "Missouri",
            "year": "1904",
            "lat": 38.63, "lon": -90.20,
            "story": "The 1904 Louisiana Purchase Exposition (World’s Fair). Pearl attended and purchased the Kaiser salon furniture set — matching chairs, table, fainting couch — that remain family heirlooms today.",
            "label_anchor": "end",
            "label_dx": -9, "label_dy": -6,
        },
        {
            "id": "sanantonio",
            "name": "San Antonio, Texas",
            "country": "Texas",
            "year": "1875–present",
            "lat": 29.42, "lon": -98.49,
            "story": "The Mattingly and Baity families converged in San Antonio. Ed Mattingly married into the Texas gentry. The Baity family built their 211 Castile home here, the gathering place for generations of family. Leroy Mattingly was born here in 1898.",
            "label_anchor": "start",
            "label_dx": 9, "label_dy": -6,
        },
        {
            "id": "kerrville",
            "name": "Kerrville, Texas",
            "country": "Texas Hill Country",
            "year": "1900s",
            "lat": 30.05, "lon": -99.14,
            "story": "Pearl Baity’s summer retreat in the Hill Country. A cooler escape from San Antonio’s heat, where the family gathered and rested. Pearl maintained a beloved summer home here.",
            "label_anchor": "start",
            "label_dx": 8, "label_dy": 12,
        },
        {
            "id": "reeves",
            "name": "Reeves County, Texas",
            "country": "West Texas",
            "year": "1901–present",
            "lat": 31.40, "lon": -103.50,
            "story": "In April 1901 — the same year as Spindletop — Pearl Baity purchased land in Reeves County. That act of prescient land acquisition is the foundation of all subsequent oil royalties the family still receives today, over 120 years later.",
            "label_anchor": "start",
            "label_dx": 9, "label_dy": -6,
        },
        {
            "id": "santamonica",
            "name": "Santa Monica, California",
            "country": "California",
            "year": "2026",
            "lat": 34.02, "lon": -118.49,
            "story": "Where Shari lives today, age 79. The end of the migration arc — from Hampshire, England across five centuries and the entire American continent. She still owns the oil rights Pearl purchased in 1901.",
            "label_anchor": "end",
            "label_dx": -9, "label_dy": -8,
        },
    ]

    # Marker size per location id
    marker_sizes = {
        "sanantonio": 7, "reeves": 7, "santamonica": 9,
        "maryland": 7, "kentucky": 6, "hampshire": 5,
    }

    # Build JSON-safe location data for the inline JS
    locations_json_parts = []
    for loc in locations_data:
        escaped_story = loc["story"].replace('"', '\\"').replace("'", "\\'")
        escaped_name = loc["name"].replace('"', '\\"')
        locations_json_parts.append(
            f'{{"id":"{loc["id"]}",'
            f'"name":"{escaped_name}",'
            f'"country":"{loc["country"]}",'
            f'"year":"{loc["year"]}",'
            f'"lat":{loc["lat"]},'
            f'"lon":{loc["lon"]},'
            f'"r":{marker_sizes.get(loc["id"], 5)},'
            f'"atlantic":{str(loc.get("atlantic_origin", False)).lower()},'
            f'"labelAnchor":"{loc.get("label_anchor","start")}",'
            f'"labelDx":{loc.get("label_dx", 8)},'
            f'"labelDy":{loc.get("label_dy", -4)},'
            f'"story":"{escaped_story}"}}'
        )
    locations_json = "[" + ",\n".join(locations_json_parts) + "]"

    map_js = """
(function() {
  /* -------------------------------------------------------
     D3-geo NaturalEarth1 migration map
     Fetches world-atlas 110m TopoJSON from CDN, renders real
     coastlines, then places waypoints via lat/lon projection.
     ------------------------------------------------------- */

  const SVG_W = 900, SVG_H = 480;

  const LOCATIONS = """ + locations_json + """;

  // Migration path order (US legs only, excluding england)
  const PATH_ORDER = ["maryland","kentucky","northcarolina","stlouis","sanantonio","kerrville","reeves","santamonica"];

  // Label visibility (major stops only)
  const SHOW_LABEL = new Set(["hampshire","maryland","kentucky","stlouis","sanantonio","reeves","santamonica"]);

  // Year label visibility
  const SHOW_YEAR = new Set(["maryland","reeves","santamonica"]);

  const svg = d3.select("#migration-map-svg");
  if (svg.empty()) return;

  // ── Projection — Natural Earth 1, fitted to our viewport ──
  // We want to show: western Europe + all of North America
  // Manually tuned center and scale for a cinematic North Atlantic framing.
  const projection = d3.geoNaturalEarth1()
    .center([-40, 38])      // center lon/lat for North Atlantic
    .scale(520)             // zoom level — covers England to California
    .translate([SVG_W / 2, SVG_H / 2]);

  const pathGen = d3.geoPath().projection(projection);

  // Helper: project a lon/lat → [svgX, svgY]
  function project(lon, lat) {
    return projection([lon, lat]);
  }

  // ── Fetch TopoJSON world atlas ──
  d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json")
    .then(function(world) {
      const land = topojson.feature(world, world.objects.land);
      const countries = topojson.feature(world, world.objects.countries);
      const borders = topojson.mesh(world, world.objects.countries, (a, b) => a !== b);

      // -- Ocean background (already set by rect in SVG markup) --

      // -- Graticule (faint grid) --
      const graticule = d3.geoGraticule()();
      svg.select("#map-graticule-group").remove();
      const gGroup = svg.insert("g", "#map-geo-land")
        .attr("id","map-graticule-group")
        .attr("opacity","0.055")
        .attr("pointer-events","none");
      gGroup.append("path")
        .datum(graticule)
        .attr("d", pathGen)
        .attr("fill","none")
        .attr("stroke","#d4a458")
        .attr("stroke-width","0.45");

      // -- Land fill (before land group inserted, remove old one) --
      svg.select("#map-geo-land").remove();
      const landGroup = svg.insert("g", "#map-overlay-group")
        .attr("id","map-geo-land")
        .attr("pointer-events","none");

      // Ocean accent: subtle country fills
      landGroup.selectAll("path.country")
        .data(countries.features)
        .join("path")
        .attr("class","country")
        .attr("d", pathGen)
        .attr("fill","#231d14")
        .attr("stroke","none");

      // Main land silhouette on top — warmer tone
      landGroup.append("path")
        .datum(land)
        .attr("d", pathGen)
        .attr("fill","#2c2316")
        .attr("stroke","#4a3c28")
        .attr("stroke-width","0.7");

      // Country borders — very subtle
      landGroup.append("path")
        .datum(borders)
        .attr("d", pathGen)
        .attr("fill","none")
        .attr("stroke","#352a1a")
        .attr("stroke-width","0.45")
        .attr("opacity","0.7");

      // -- Insert ocean labels into overlay group, project their positions --
      // Atlantic Ocean label
      const atlPt = project(-30, 35);
      if (atlPt) {
        const atlG = svg.select("#map-overlay-group").append("g")
          .attr("pointer-events","none");
        atlG.append("text")
          .attr("x", atlPt[0]).attr("y", atlPt[1] - 6)
          .attr("text-anchor","middle")
          .attr("font-family","'Cormorant Garamond', Georgia, serif")
          .attr("font-size","10").attr("font-style","italic")
          .attr("fill","#4a3820").attr("opacity","0.55")
          .attr("letter-spacing","0.15em")
          .text("ATLANTIC");
        atlG.append("text")
          .attr("x", atlPt[0]).attr("y", atlPt[1] + 7)
          .attr("text-anchor","middle")
          .attr("font-family","'Cormorant Garamond', Georgia, serif")
          .attr("font-size","10").attr("font-style","italic")
          .attr("fill","#4a3820").attr("opacity","0.55")
          .attr("letter-spacing","0.15em")
          .text("OCEAN");
      }

      // Pacific Ocean label
      const pacPt = project(-140, 40);
      if (pacPt) {
        const pacG = svg.select("#map-overlay-group").append("g")
          .attr("pointer-events","none");
        pacG.append("text")
          .attr("x", pacPt[0]).attr("y", pacPt[1] - 6)
          .attr("text-anchor","middle")
          .attr("font-family","'Cormorant Garamond', Georgia, serif")
          .attr("font-size","10").attr("font-style","italic")
          .attr("fill","#4a3820").attr("opacity","0.45")
          .attr("letter-spacing","0.15em")
          .text("PACIFIC");
        pacG.append("text")
          .attr("x", pacPt[0]).attr("y", pacPt[1] + 7)
          .attr("text-anchor","middle")
          .attr("font-family","'Cormorant Garamond', Georgia, serif")
          .attr("font-size","10").attr("font-style","italic")
          .attr("fill","#4a3820").attr("opacity","0.45")
          .attr("letter-spacing","0.15em")
          .text("OCEAN");
      }

      // -- Project all waypoints --
      const projected = {};
      LOCATIONS.forEach(function(loc) {
        const pt = project(loc.lon, loc.lat);
        projected[loc.id] = pt;
      });

      const englandPt = projected["hampshire"];
      const marylandPt = projected["maryland"];

      // -- Atlantic crossing arc (dashed great-circle-like curve) --
      if (englandPt && marylandPt) {
        // Use d3 geoPath with a LineString for true great-circle arc
        const atlanticArc = {
          "type": "LineString",
          "coordinates": [
            [-1.03, 51.27],   // Hampshire
            [-76.65, 38.20]   // Maryland
          ]
        };
        const arcPathGen = d3.geoPath().projection(projection).pointRadius(0);
        svg.select("#map-overlay-group").append("path")
          .datum(atlanticArc)
          .attr("d", arcPathGen)
          .attr("fill","none")
          .attr("stroke","#d4a458")
          .attr("stroke-width","1.4")
          .attr("stroke-dasharray","5,7")
          .attr("opacity","0.38")
          .attr("pointer-events","none");

        // Arrowhead at Maryland end
        const arrowLen = 8;
        const dx = marylandPt[0] - englandPt[0];
        const dy = marylandPt[1] - englandPt[1];
        const angle = Math.atan2(dy, dx);
        const ax = marylandPt[0] - arrowLen * Math.cos(angle - 0.35);
        const ay = marylandPt[1] - arrowLen * Math.sin(angle - 0.35);
        const bx = marylandPt[0] - arrowLen * Math.cos(angle + 0.35);
        const by = marylandPt[1] - arrowLen * Math.sin(angle + 0.35);
        svg.select("#map-overlay-group").append("path")
          .attr("d", `M${ax},${ay} L${marylandPt[0]},${marylandPt[1]} L${bx},${by}`)
          .attr("fill","none")
          .attr("stroke","#d4a458")
          .attr("stroke-width","1.2")
          .attr("opacity","0.5")
          .attr("pointer-events","none");
      }

      // -- US migration polyline (projected) --
      const pathPts = PATH_ORDER
        .map(id => projected[id])
        .filter(Boolean);

      if (pathPts.length > 1) {
        const lineStr = pathPts.map(p => p.join(",")).join(" ");
        // Update the existing animated polyline with real projected coords
        const migPath = svg.select("#migration-path");
        migPath.attr("points", lineStr);
        // Reset dash animation length to match actual path length
        const pathNode = migPath.node();
        if (pathNode && pathNode.getTotalLength) {
          const len = pathNode.getTotalLength();
          migPath
            .attr("stroke-dasharray", len)
            .attr("stroke-dashoffset", len)
            .style("animation", `drawPath 3.5s ease-out 0.8s forwards`);
          // Update the keyframe dynamically
          const styleEl = document.getElementById("migration-path-style");
          if (styleEl) {
            styleEl.textContent = `@keyframes drawPath { to { stroke-dashoffset: 0; } } #migration-path { stroke-dasharray: ${len}; stroke-dashoffset: ${len}; animation: drawPath 3.5s ease-out 0.8s forwards; }`;
          }
        }
      }

      // -- Location markers --
      svg.select("#map-markers-group").remove();
      const markerGroup = svg.select("#map-overlay-group").append("g")
        .attr("id","map-markers-group");

      LOCATIONS.forEach(function(loc) {
        const pt = projected[loc.id];
        if (!pt || pt[0] < -10 || pt[0] > SVG_W + 10) return; // off-canvas skip
        const r = loc.r;
        const cx = pt[0], cy = pt[1];
        const isSantaMonica = loc.id === "santamonica";

        const g = markerGroup.append("g")
          .attr("class","map-location")
          .attr("data-id", loc.id)
          .attr("data-name", loc.name)
          .attr("data-year", loc.year)
          .attr("data-country", loc.country)
          .attr("data-story", loc.story);

        // Extra outer pulse ring for Santa Monica
        if (isSantaMonica) {
          g.append("circle")
            .attr("class","map-marker-pulse")
            .attr("cx",cx).attr("cy",cy)
            .attr("r", r + 12)
            .attr("fill","none")
            .attr("stroke","#d4a458")
            .attr("stroke-width","1.5");
        }

        // Pulse ring
        g.append("circle")
          .attr("class","map-marker-pulse")
          .attr("cx",cx).attr("cy",cy)
          .attr("r", r + 6)
          .attr("fill","none")
          .attr("stroke","#d4a458")
          .attr("stroke-width","1");

        // Marker fill
        g.append("circle")
          .attr("cx",cx).attr("cy",cy)
          .attr("r", r)
          .attr("fill", isSantaMonica ? "#e8c070" : "#d4a458")
          .attr("stroke","#7a5010")
          .attr("stroke-width","1.5")
          .attr("opacity","0.92");

        // Inner highlight
        g.append("circle")
          .attr("cx",cx).attr("cy",cy)
          .attr("r", Math.max(1, r - 2))
          .attr("fill","#f0c878")
          .attr("opacity","0.6");

        // Location label
        if (SHOW_LABEL.has(loc.id)) {
          const labelName = loc.name.split(",")[0];
          g.append("text")
            .attr("x", cx + loc.labelDx)
            .attr("y", cy + loc.labelDy)
            .attr("text-anchor", loc.labelAnchor)
            .attr("font-family","'Cormorant Garamond', Georgia, serif")
            .attr("font-size","8")
            .attr("font-style","italic")
            .attr("fill","#c8a870")
            .attr("opacity","0.88")
            .attr("pointer-events","none")
            .text(labelName);
        }

        // Year label
        if (SHOW_YEAR.has(loc.id)) {
          g.append("text")
            .attr("x", cx)
            .attr("y", cy + r + 11)
            .attr("text-anchor","middle")
            .attr("font-family","'Source Code Pro', monospace")
            .attr("font-size","6.5")
            .attr("fill","#806040")
            .attr("opacity","0.72")
            .attr("pointer-events","none")
            .text(loc.year);
        }
      });

      // ── Tooltip interaction ──
      const container = document.getElementById("migration-map-container");
      const tooltip  = document.getElementById("map-tooltip");
      const tName    = document.getElementById("map-tt-name");
      const tYear    = document.getElementById("map-tt-year");
      const tBody    = document.getElementById("map-tt-body");
      if (!container || !tooltip) return;

      function showTip(loc, e) {
        tName.textContent = loc.dataset.name + " — " + loc.dataset.country;
        tYear.textContent = loc.dataset.year;
        tBody.textContent = loc.dataset.story;
        tooltip.classList.add("visible");
        positionTooltip(e);
      }

      function positionTooltip(e) {
        const rect = container.getBoundingClientRect();
        let x = e.clientX - rect.left + 14;
        let y = e.clientY - rect.top - 10;
        const tw = tooltip.offsetWidth || 240;
        const th = tooltip.offsetHeight || 120;
        if (x + tw > rect.width - 10) x = e.clientX - rect.left - tw - 14;
        if (y + th > rect.height - 10) y = e.clientY - rect.top - th - 10;
        if (y < 8) y = 8;
        tooltip.style.left = x + "px";
        tooltip.style.top  = y + "px";
      }

      markerGroup.selectAll(".map-location").each(function() {
        const node = this;
        node.addEventListener("mouseenter", function(e) { showTip(node, e); });
        node.addEventListener("mousemove",  positionTooltip);
        node.addEventListener("mouseleave", function() { tooltip.classList.remove("visible"); });
        node.addEventListener("click", function(e) {
          showTip(node, e);
          e.stopPropagation();
        });
      });

      document.addEventListener("click", function() {
        tooltip.classList.remove("visible");
      });
    })
    .catch(function(err) {
      // If CDN fails, the map simply shows the fallback placeholder text
      console.warn("Migration map: could not load world atlas:", err);
      svg.append("text")
        .attr("x", SVG_W/2).attr("y", SVG_H/2)
        .attr("text-anchor","middle")
        .attr("fill","#806040")
        .attr("font-family","'Lora', Georgia, serif")
        .attr("font-size","13")
        .text("Map requires network access to load geographic data.");
    });
})();
"""

    return f"""<section id="map" aria-labelledby="map-heading">
<div id="map-section">
  <h2 id="map-heading">The Migration</h2>
  <p>Four centuries of purposeful motion. From <strong>Hampshire, England</strong> (1663) across the Atlantic to Maryland &mdash; south to Kentucky &mdash; through the Carolinas &mdash; into Texas &mdash; and finally to California. <em>Hover any marker to read what happened there.</em></p>

  <div id="migration-map-container" role="img" aria-label="Migration map showing Mattingly family movement from England to California">

    <!-- Dynamic path style override (updated by JS once path length is known) -->
    <style id="migration-path-style">
      #migration-path {{
        stroke-dasharray: 4000;
        stroke-dashoffset: 4000;
        animation: drawPath 3.5s ease-out 0.8s forwards;
      }}
    </style>

    <svg id="migration-map-svg" viewBox="0 0 900 480" xmlns="http://www.w3.org/2000/svg"
         preserveAspectRatio="xMidYMid meet">
      <defs>
        <!-- Vignette gradient -->
        <radialGradient id="map-vignette" cx="50%" cy="50%" r="70%">
          <stop offset="50%" stop-color="transparent"/>
          <stop offset="100%" stop-color="rgba(8,6,4,0.72)"/>
        </radialGradient>
        <!-- Vintage paper grain filter for land -->
        <filter id="map-land-grain" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3"
            seed="4" stitchTiles="stitch" result="noise"/>
          <feColorMatrix type="saturate" values="0" in="noise" result="grayNoise"/>
          <feBlend in="SourceGraphic" in2="grayNoise" mode="multiply" result="blended"/>
          <feComponentTransfer in="blended">
            <feFuncA type="linear" slope="1"/>
          </feComponentTransfer>
        </filter>
      </defs>

      <!-- ── Ocean background ── -->
      <rect width="900" height="480" fill="#090706"/>

      <!-- Ocean texture — very faint warm ripple -->
      <rect width="900" height="480" fill="none"
        stroke="#1e1810" stroke-width="0"
        style="background:repeating-linear-gradient(0deg,transparent,transparent 23px,rgba(212,164,88,0.012) 24px)"/>

      <!-- D3 inserts geo groups here (land before markers) -->
      <!-- geo land group placeholder — D3 inserts before this -->
      <g id="map-overlay-group">
        <!-- Atlantic arc and ocean labels inserted by D3 -->
      </g>

      <!-- MIGRATION POLYLINE — animated draw on load (coords updated by D3) -->
      <polyline id="migration-path"
        points="0,0"
        fill="none"
        stroke="#d4a458"
        stroke-width="2"
        stroke-dasharray="8,5"
        opacity="0.65"
        stroke-linejoin="round"
        pointer-events="none"/>

      <!-- MAP TITLE — engraved serif -->
      <text x="450" y="28" text-anchor="middle"
        font-family="'Cormorant Garamond', Georgia, serif"
        font-size="14" font-weight="700" letter-spacing="0.28em"
        fill="#c8a060" opacity="0.78">THE MATTINGLY MIGRATION</text>
      <line x1="270" y1="33" x2="630" y2="33"
        stroke="#d4a458" stroke-width="0.5" opacity="0.28"/>

      <!-- Compass rose — bottom right -->
      <g transform="translate(858, 435)" opacity="0.38">
        <circle cx="0" cy="0" r="20" fill="none" stroke="#d4a458" stroke-width="0.5"/>
        <line x1="0" y1="-19" x2="0" y2="19" stroke="#d4a458" stroke-width="1"/>
        <line x1="-19" y1="0" x2="19" y2="0" stroke="#d4a458" stroke-width="1"/>
        <line x1="-12" y1="-12" x2="12" y2="12" stroke="#d4a458" stroke-width="0.4"/>
        <line x1="12" y1="-12" x2="-12" y2="12" stroke="#d4a458" stroke-width="0.4"/>
        <polygon points="0,-19 3.5,-9 -3.5,-9" fill="#d4a458"/>
        <polygon points="0,19 3.5,9 -3.5,9" fill="#d4a458" opacity="0.4"/>
        <text x="0" y="-24" text-anchor="middle"
          font-family="'Cormorant Garamond', Georgia, serif"
          font-size="8" font-weight="700" fill="#d4a458">N</text>
      </g>

      <!-- Scale note -->
      <text x="30" y="470"
        font-family="'Lora', Georgia, serif"
        font-size="6.5" font-style="italic" fill="#504030" opacity="0.65">
        Natural Earth projection · World Atlas 110m coastlines
      </text>

      <!-- Vignette overlay -->
      <rect width="900" height="480" fill="url(#map-vignette)" pointer-events="none"/>
    </svg>

    <!-- Hover tooltip -->
    <div class="map-tooltip" id="map-tooltip" role="tooltip" aria-live="polite">
      <div class="map-tooltip-name" id="map-tt-name"></div>
      <div class="map-tooltip-year" id="map-tt-year"></div>
      <div class="map-tooltip-body" id="map-tt-body"></div>
    </div>

    <!-- Map legend -->
    <div class="map-legend">
      <strong>Legend</strong>
      <span>&#9679; Settlement waypoint</span><br>
      <span>&#8212;&#8212; Migration route</span><br>
      <span>- - - Atlantic crossing (1663)</span>
    </div>

  </div>
</div>
</section>

<script>
{map_js}
</script>"""


def main():
    OUT_FAMILY.parent.mkdir(parents=True, exist_ok=True)
    DOCS_FAMILY.parent.mkdir(parents=True, exist_ok=True)

    family_html = build_html(family_only=True)
    OUT_FAMILY.write_text(family_html, encoding="utf-8")
    print(f"Wrote {OUT_FAMILY} ({OUT_FAMILY.stat().st_size:,} bytes)")
    DOCS_FAMILY.write_text(family_html, encoding="utf-8")
    print(f"Wrote {DOCS_FAMILY} ({DOCS_FAMILY.stat().st_size:,} bytes)")

    public_html = build_html(family_only=False)
    OUT_PUBLIC.write_text(public_html, encoding="utf-8")
    print(f"Wrote {OUT_PUBLIC} ({OUT_PUBLIC.stat().st_size:,} bytes)")
    DOCS_INDEX.write_text(public_html, encoding="utf-8")
    print(f"Wrote {DOCS_INDEX} ({DOCS_INDEX.stat().st_size:,} bytes)")

    research_files = [
        fn for fn in RESEARCH_DIR.glob("*.md")
        if re.match(r"^\d{2,}-", fn.name)
    ]
    research_files.sort(key=lambda p: (int(p.name.split("-", 1)[0]), p.name))
    if research_files:
        print(f"\nResearch files included ({len(research_files)}):")
        for f in research_files:
            print(f"  {f.name}")
    else:
        print("\nNo research files yet — placeholders shown. Re-run after subagents complete.")


if __name__ == "__main__":
    main()
