"""Build the self-contained HTML deliverable from transcript + entities + research.

Inputs:
  transcripts/final.md
  research/entities.json
  research/01-mattingly-lineage.md (if present)
  research/02-texas-places.md (if present)
  research/03-pohl-monette-art.md (if present)
  research/04-english-origins.md (if present)
  research/05-scandal-and-loose-ends.md (if present)

Outputs:
  output/grandma-shari-family-history.html  (full version, family-only)
  output/grandma-shari-family-history-public.html  (redacted version, shareable)

The HTML is one file with inline CSS and inline JS. Uses CDN for Leaflet + vis-timeline.
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
OUT_FAMILY = WORKSPACE / "output" / "grandma-shari-family-history.html"
OUT_PUBLIC = WORKSPACE / "output" / "grandma-shari-family-history-public.html"
AUDIO_REL = "../audio/source.m4a"

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

/* ---- HERO / COVER ---- */

header.cover {
  position: relative;
  text-align: center;
  padding: var(--sp-2xl) var(--sp-lg) var(--sp-xl);
  margin: 0 calc(-1 * var(--sp-lg)) var(--sp-xl);
  /* Dark leather-bound book foreword — warm black with vignette */
  background: radial-gradient(
    ellipse 80% 90% at 50% 40%,
    #1c1510 0%,
    #130f0c 45%,
    #0a0806 100%
  );
  border-bottom: 1px solid var(--rule);
  /* Brass lamp vignette — warmth pulls toward center */
  box-shadow:
    inset 0 -12px 40px rgba(5, 3, 2, 0.7),
    inset 0 60px 120px rgba(212, 164, 88, 0.04);
  overflow: hidden;
}

/* Top gold rule — brass trim */
header.cover::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg,
    transparent 0%,
    #a07840 15%,
    var(--accent-gold) 40%,
    #e8c070 50%,
    var(--accent-gold) 60%,
    #a07840 85%,
    transparent 100%);
}

/* Inset frame — aged gilt border */
header.cover::after {
  content: '';
  position: absolute;
  inset: 28px;
  border: 1px solid rgba(212, 164, 88, 0.18);
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
  font-size: var(--fs-hero);
  line-height: 1.05;
  margin: 0 0 var(--sp-md);
  color: #f0e6d2;
  letter-spacing: -0.02em;
  text-wrap: balance;
  /* Subtle text glow — brass lamp light on the title */
  text-shadow: 0 0 60px rgba(212, 164, 88, 0.2), 0 2px 4px rgba(0,0,0,0.6);
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
  font-size: var(--fs-xl);
  margin: 0 0 var(--sp-md);
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
  margin-top: var(--sp-md);
  letter-spacing: 0.01em;
}

header.cover .meta strong {
  color: var(--ink-soft);
}

/* Audio player — brass-trimmed tape control */
.audio-wrapper {
  margin: var(--sp-xl) auto 0;
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
  letter-spacing: -0.01em;
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

/* Drop cap — illuminated manuscript style, gold on dark */
.transcript-turn:first-child .text p:first-child::first-letter {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 4.2em;
  font-weight: 700;
  float: left;
  line-height: 0.78;
  margin: 0.04em var(--sp-sm) 0 -0.04em;
  color: var(--accent-gold);
  text-shadow: 0 0 20px rgba(212, 164, 88, 0.4);
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
  padding: var(--sp-lg) var(--sp-xl);
  margin: var(--sp-lg) 0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

.research-section h3 { margin-top: 0; }
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
  margin-left: calc(-1 * var(--sp-lg));
  margin-right: calc(-1 * var(--sp-lg));
  padding: 0 var(--sp-lg);
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
  cursor: grab;
  position: relative;
  z-index: 1;
}

#lineage-tree-svg:active { cursor: grabbing; }

/* Node animations */
@keyframes nodeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
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
  padding: 7px 14px;
  font-family: 'Lora', Georgia, serif;
  font-size: var(--fs-sm);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  line-height: 1;
  min-width: 40px;
  min-height: 36px;
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

  .tree-toolbar .tree-legend { display: none; }

  .pull-quote {
    font-size: var(--fs-xl);
    padding: var(--sp-lg) var(--sp-md);
  }

  .research-section { padding: var(--sp-md); }
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
    for fn in sorted(RESEARCH_DIR.glob("0*-*.md")):
        findings[fn.stem] = fn.read_text(encoding="utf-8")
    return findings


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


def render_person_card(p, redact=False):
    if p.get("redact_in_public") and redact:
        return ""
    name = p.get("full_name") or p.get("given_name") or "(unnamed)"
    if redact and p.get("living_flag") and p.get("id") not in {"p020", "p021"}:
        name = f"[redacted, {p.get('relation_to_shari', 'living relative')}]"
    pid = p["id"]
    relation = p.get("relation_to_shari", "")
    b = p.get("birth_year")
    d = p.get("death_year")
    years = f" ({b}–{d})" if b and d else (f" (b. {b})" if b else (f" (d. {d})" if d else ""))
    living = " " + render_confidence("living") if p.get("living_flag") else ""
    occupation = p.get("occupation")
    context = p.get("context", "")
    bp = p.get("birth_place")
    notes = p.get("notes") or p.get("notes_from_hunter") or ""
    timestamps = p.get("transcript_timestamps", []) or []
    body_parts = []
    if relation:
        body_parts.append(f'<p class="entity-meta">{html.escape(relation)}{years}{living}</p>')
    if occupation:
        body_parts.append(f"<p><strong>Occupation:</strong> {html.escape(occupation)}</p>")
    if bp:
        body_parts.append(f"<p><strong>Born:</strong> {html.escape(bp)}</p>")
    if context:
        body_parts.append(f"<p>{html.escape(context)}</p>")
    if notes and notes != context:
        body_parts.append(f"<p><em>{html.escape(notes)}</em></p>")
    if timestamps:
        ts_str = ", ".join(timestamps)
        body_parts.append(f'<p class="entity-meta">Mentioned at: {html.escape(ts_str)}</p>')
    body = "\n".join(body_parts)
    return f'''<details class="entity-card" id="{pid}">
  <summary>{html.escape(name)}{years}</summary>
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

def build_lineage_tree_data():
    """Return nested dict for D3 tree.
    Reads research/06-full-mattingly-lineage.json if present, otherwise falls back to a
    structured placeholder showing known generations + 'unknown' middle generations.
    """
    lineage_path = WORKSPACE / "research" / "06-full-mattingly-lineage.json"
    if lineage_path.exists():
        try:
            data = json.loads(lineage_path.read_text(encoding="utf-8"))
            return convert_lineage_research_to_tree(data)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
    return _placeholder_lineage_tree()


def convert_lineage_research_to_tree(lineage_data):
    """Convert the lineage agent's generations array to a nested tree."""
    gens = lineage_data.get("generations", [])
    if not gens:
        return _placeholder_lineage_tree()
    # Build linearly (one main descendant per generation; collateral siblings as branches)
    nodes = []
    for g in gens:
        p = g.get("person", {}) or {}
        nodes.append({
            "name": p.get("full_name") or g.get("label") or f"Generation {g.get('gen')}",
            "dates": _format_dates(p.get("birth_year"), p.get("death_year")),
            "fact": (p.get("key_facts") or [g.get("label", "")])[0] if p.get("key_facts") else g.get("label", ""),
            "id": p.get("id") or None,
            "generation": g.get("gen", 0),
            "century": _century_for_year(p.get("birth_year") or p.get("death_year")),
            "confidence": (p.get("confidence") or "unknown").lower(),
        })
    if not nodes:
        return _placeholder_lineage_tree()
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


def _placeholder_lineage_tree():
    """Fallback tree using only confirmed-from-interview anchors."""
    def gen(name, dates, fact, eid, generation, century, confidence, children=None, siblings=None):
        node = {
            "name": name, "dates": dates, "fact": fact, "id": eid,
            "generation": generation, "century": century, "confidence": confidence,
            "children": children or [],
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


def render_lineage_tree_section():
    """Generate the HTML+SVG+JS for the D3 family tree."""
    tree_data = build_lineage_tree_data()
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
    """Return the D3 tree initialization JS — heritage editorial design."""
    return r"""
// ── Mattingly Lineage Tree ──────────────────────────────────────
// Vertical descent layout with generation-spine labels,
// warm-brown depth gradient, confidence-coded borders,
// sibling badges, animated entry, zoom+pan.
// ────────────────────────────────────────────────────────────────

const lineageData = JSON.parse(document.getElementById('lineage-tree-data').textContent);

// Canvas dimensions
const W = 1320;
const H = 1800;
const NW = 210;   // node width
const NH = 76;    // node height
const SPINE = 68; // left margin for generation labels
const M = { top: 56, right: 36, bottom: 72, left: SPINE + 12 };

const svg = d3.select("#lineage-tree-svg")
  .attr("viewBox", `0 0 ${W} ${H}`)
  .attr("preserveAspectRatio", "xMidYMid meet")
  .attr("width", "100%")
  .attr("height", "1020");

// ── Defs: gradients, filters ────────────────────────────────────
const defs = svg.append("defs");

// Glow filter for hovered nodes — gold halo on dark
const shadowFilter = defs.append("filter")
  .attr("id", "node-shadow")
  .attr("x", "-35%").attr("y", "-35%")
  .attr("width", "170%").attr("height", "170%");
// Outer warm glow
const feMerge = shadowFilter.append("feComposite").attr("in", "SourceGraphic");
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
const merge = shadowFilter.append("feMerge");
merge.append("feMergeNode").attr("in", "glow");
merge.append("feMergeNode").attr("in", "SourceGraphic");

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

// Dark mode tree gradient: G1 (oldest) = deep amber-brown, G14 (newest) = pale silver-rose
// Direction: ancient warmth → modern coolness, all on dark backgrounds
const gradientPalette = [
  ['#4a2c0a', '#3a2208'],   // G1  — deep amber-brown (1620s England)
  ['#5e3810', '#4e2e0c'],   // G2
  ['#744618', '#603a14'],   // G3
  ['#8a5820', '#784c1c'],   // G4
  ['#a06c2a', '#8e5e24'],   // G5
  ['#b48035', '#a0722e'],   // G6  — warm gold midpoint
  ['#c09040', '#b0823a'],   // G7
  ['#b89858', '#a88a4e'],   // G8  — transition zone
  ['#a89070', '#988264'],   // G9  — cooling down
  ['#8a8878', '#7c7a6c'],   // G10 — muted warm-grey
  ['#787c80', '#6c7074'],   // G11 — silver-grey
  ['#6a7480', '#5e6872'],   // G12 — cool silver
  ['#607080', '#545e6e'],   // G13 (Hunter's parent)
  ['#586878', '#4c5c6a'],   // G14 (Hunter) — silver-blue
];

gradientPalette.forEach((pair, i) => {
  makeGradient(`ng-${i}`, pair[0], pair[1]);
});

function nodeFill(depth) {
  const i = Math.min(depth, gradientPalette.length - 1);
  return `url(#ng-${i})`;
}

// On dark cards, all text needs to be warm-light; earlier gens get warmer gold tones
function nodeTextColor(depth) {
  // All cards are dark; earlier gens (amber) get cream text, later (grey-blue) get pale silver
  if (depth < 5) return '#f0e0c0';   // warm cream on amber-brown
  if (depth < 9) return '#ede0cc';   // warm off-white on gold-grey
  return '#d8dde4';                  // cool silver-white on slate
}
function nodeDateColor(depth) {
  if (depth < 5) return '#d4a040';   // gold dates on amber cards
  if (depth < 9) return '#b89858';   // muted gold on transition
  return '#8090a0';                  // cool grey on slate cards
}
function nodeFactColor(depth) {
  if (depth < 5) return '#b07030';   // burnished bronze on amber
  if (depth < 9) return '#9a8060';   // warm taupe on transition
  return '#6878a0';                  // steel-blue on slate
}

function confidenceStroke(c) {
  if (c === 'confirmed') return '#d4a458';   // gold for confirmed
  if (c === 'probable')  return '#b8826a';   // bronze for probable
  return '#4a4440';                          // dim for unknown
}
function confidenceStrokeWidth(c) {
  return c === 'confirmed' ? 2.0 : 1.5;
}
function confidenceDash(c) {
  return c === 'unknown' ? '4,3' : 'none';
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
  .attr("fill", d => nodeFill(d.depth))
  .attr("stroke", d => confidenceStroke(d.data.confidence))
  .attr("stroke-width", d => confidenceStrokeWidth(d.data.confidence))
  .attr("stroke-dasharray", d => confidenceDash(d.data.confidence));

// Thin highlight line at top edge — gives dimension on dark surface
cardG.append("rect")
  .attr("x", -NW/2 + 2).attr("y", -NH/2 + 1)
  .attr("width", NW - 4).attr("height", 1)
  .attr("rx", 1)
  .attr("fill", "rgba(255,255,255,0.12)");

// ── Node text ────────────────────────────────────────────────────

// Name line
cardG.append("text")
  .attr("y", -16)
  .attr("text-anchor", "middle")
  .attr("font-family", "'Cormorant Garamond', 'Lora', Georgia, serif")
  .attr("font-weight", "700")
  .attr("font-size", "13.5px")
  .attr("letter-spacing", "0.01em")
  .attr("fill", d => nodeTextColor(d.depth))
  .text(d => truncate(d.data.name, 28));

// Dates — monospaced, smaller
cardG.append("text")
  .attr("y", -1)
  .attr("text-anchor", "middle")
  .attr("font-family", "'Source Code Pro', 'Courier New', monospace")
  .attr("font-size", "10.5px")
  .attr("letter-spacing", "0.02em")
  .attr("fill", d => nodeDateColor(d.depth))
  .text(d => d.data.dates);

// Fact line — italic, smallest
cardG.append("text")
  .attr("y", 17)
  .attr("text-anchor", "middle")
  .attr("font-family", "'Lora', Georgia, serif")
  .attr("font-style", "italic")
  .attr("font-size", "10px")
  .attr("fill", d => nodeFactColor(d.depth))
  .text(d => truncate(d.data.fact, 34));

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
function autoFitTree() {
  const bbox = g.node().getBBox();
  const containerW = svg.node().getBoundingClientRect().width || W;
  const containerH = parseFloat(svg.attr("height")) || 1020;
  const scaleX = containerW / (bbox.width + M.left + M.right + 40);
  const scaleY = containerH / (bbox.height + M.top + M.bottom + 40);
  const scale = Math.min(scaleX, scaleY, 0.95);
  const tx = (containerW - (bbox.width + 40) * scale) / 2 - bbox.x * scale + 20 * scale;
  const ty = M.top;
  svg.call(zoomBehavior.transform,
    d3.zoomIdentity.translate(tx - M.left * scale, ty - M.top * scale).scale(scale));
}

window.addEventListener('load', () => setTimeout(autoFitTree, 120));
"""


def build_html(family_only=True):
    turns = load_transcript()
    entities = load_entities()
    research = load_research()

    redact_set = set() if family_only else set(entities.get("audience_policy", {}).get("redaction_set", []))
    redact_living_names = not family_only

    entity_index = build_entity_index(entities)

    # People grouped by family layer
    people = entities.get("people", [])
    deceased = [p for p in people if not p.get("living_flag") and not p.get("redact_in_public")]
    living = [p for p in people if p.get("living_flag") and not p.get("redact_in_public")]

    people_html = []
    if deceased:
        people_html.append("<h3>Ancestors & Historical Family</h3>")
        for p in sorted(deceased, key=lambda x: x.get("birth_year") or 9999):
            people_html.append(render_person_card(p, redact=redact_living_names))
    if living and family_only:
        people_html.append("<h3>Living Family</h3>")
        for p in living:
            people_html.append(render_person_card(p, redact=False))

    places_html = "\n".join(render_place_card(pl) for pl in entities.get("places", []))
    events_html = "\n".join(render_event_card(e) for e in sorted(
        entities.get("events", []),
        key=lambda e: re.search(r"(\d{4})", str(e.get("date_or_year") or "")).group(1) if re.search(r"\d{4}", str(e.get("date_or_year") or "")) else "9999"
    ))

    research_html = []
    titles = {
        "01-mattingly-lineage": "Mattingly Direct Lineage",
        "02-texas-places": "Texas Places & Properties",
        "03-pohl-monette-art": "Pohl, Monette & Texas Art",
        "04-english-origins": "English Origins & Etymology",
        "05-scandal-and-loose-ends": "Loose Ends & Mysteries",
    }
    for stem, title in titles.items():
        content = research.get(stem)
        if content:
            research_html.append(f'<div class="research-section">{md_to_html(content)}</div>')
        else:
            research_html.append(f'<div class="research-section"><h3>{html.escape(title)}</h3><p><em>Research pending — file will appear when subagent completes.</em></p></div>')

    open_questions = entities.get("open_questions", [])
    oq_html = ""
    if open_questions:
        items = "\n".join(f"<li>{html.escape(q)}</li>" for q in open_questions)
        oq_html = f"""<div class="callout">
  <strong>Open questions for the family:</strong>
  <ul>{items}</ul>
</div>"""

    transcript_html = render_transcript(turns, entity_index, redact_set)
    lineage_tree_html = render_lineage_tree_section()

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
        <li><a href="#timeline">Timeline</a></li>
        <li><a href="#map">Migration Map</a></li>
        <li><a href="#transcript">The Interview</a></li>
        <li><a href="#cast">People</a></li>
        <li><a href="#places">Places</a></li>
        <li><a href="#events">Events</a></li>
        <li><a href="#research">Research</a></li>
      </ul>
    </nav>

    {lineage_tree_html}

    <section id="timeline">
      <h2>Timeline</h2>
      <p>Four centuries of family events alongside the broader sweep of history. Drag horizontally to explore.</p>
      <div id="timeline-container"></div>
    </section>

    <section id="map">
      <h2>Migration Map</h2>
      <p>England to Maryland (1663) &rarr; Kentucky (1780s) &rarr; North Carolina &rarr; Texas (1870s) &rarr; California. A family in constant, purposeful motion.</p>
      <div id="map-container"></div>
    </section>

    <section id="transcript">
      <h2>The Interview</h2>
      <p><em>Tap or click any underlined name to jump to its entry below.</em></p>
      <blockquote class="pull-quote">
        She bought land in Reeves County, Texas in April 1901. That is a source for all the wells that we have now.
      </blockquote>
      {transcript_html}
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
      {''.join(research_html)}
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

  <!-- D3 for the lineage tree -->
  <script src="https://unpkg.com/d3@7/dist/d3.min.js"></script>

  <!-- Leaflet for the map -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin></script>

  <!-- vis-timeline for the timeline -->
  <link rel="stylesheet" href="https://unpkg.com/vis-timeline@7.7.3/styles/vis-timeline-graph2d.min.css">
  <script src="https://unpkg.com/vis-timeline@7.7.3/standalone/umd/vis-timeline-graph2d.min.js"></script>

  <script>
{render_lineage_tree_js()}
{render_timeline_js()}
{render_map_js()}
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


def render_map_js():
    points = [
        {"name": "Mattingley, Hampshire (origin village)", "lat": 51.2855, "lng": -0.9550, "year": "pre-1660"},
        {"name": "St Mary's City, Maryland (1660 arrival)", "lat": 38.1893, "lng": -76.4316, "year": "1660"},
        {"name": "Boonesborough, Kentucky", "lat": 37.8884, "lng": -84.2697, "year": "1780s"},
        {"name": "North Carolina (Pearl Baity)", "lat": 35.7596, "lng": -79.0193, "year": "1810–1875"},
        {"name": "San Antonio, Texas (Mattingly + Baity)", "lat": 29.4241, "lng": -98.4936, "year": "1875–today"},
        {"name": "Kerrville, Texas (Pearl's summer home)", "lat": 30.0474, "lng": -99.1403, "year": "1900s"},
        {"name": "Reeves County, TX (1901 oil land)", "lat": 31.4237, "lng": -103.4828, "year": "1901–today"},
        {"name": "Galveston, Texas (1880 immigration port)", "lat": 29.3013, "lng": -94.7977, "year": "1880"},
        {"name": "St Louis, Missouri (1904 World's Fair)", "lat": 38.6356, "lng": -90.2842, "year": "1904"},
        {"name": "Santa Monica, CA (Shari today)", "lat": 34.0195, "lng": -118.4912, "year": "2026"},
    ]
    points_json = json.dumps(points)
    return f"""
const mapContainer = document.getElementById('map-container');
if (mapContainer && window.L) {{
  const map = L.map('map-container').setView([39.5, -90], 3);
  // CartoDB Dark Matter — dark base tiles that match the archive aesthetic
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" style="color:#665a4e">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions" style="color:#665a4e">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
  }}).addTo(map);
  const points = {points_json};
  const route = points.map(p => [p.lat, p.lng]);
  // Gold migration route — illuminated manuscript line
  L.polyline(route, {{
    color: '#d4a458',
    weight: 2,
    dashArray: '6, 10',
    opacity: 0.65
  }}).addTo(map);
  points.forEach((p, i) => {{
    const m = L.circleMarker([p.lat, p.lng], {{
      radius: 7,
      fillColor: '#d4a458',
      color: '#a07030',
      fillOpacity: 0.8,
      weight: 2
    }}).addTo(map);
    m.bindPopup(
      `<strong style="color:#d4a458">${{p.name}}</strong><br><em style="color:#9a8a78">${{p.year}}</em>`,
      {{className: 'dark-popup'}}
    );
  }});
  map.fitBounds(L.polyline(route).getBounds().pad(0.15));
}}
"""


def main():
    OUT_FAMILY.parent.mkdir(parents=True, exist_ok=True)
    family_html = build_html(family_only=True)
    OUT_FAMILY.write_text(family_html, encoding="utf-8")
    print(f"Wrote {OUT_FAMILY} ({OUT_FAMILY.stat().st_size:,} bytes)")

    public_html = build_html(family_only=False)
    OUT_PUBLIC.write_text(public_html, encoding="utf-8")
    print(f"Wrote {OUT_PUBLIC} ({OUT_PUBLIC.stat().st_size:,} bytes)")

    research_files = list(RESEARCH_DIR.glob("0*-*.md"))
    if research_files:
        print(f"\nResearch files included ({len(research_files)}):")
        for f in research_files:
            print(f"  {f.name}")
    else:
        print("\nNo research files yet — placeholders shown. Re-run after subagents complete.")


if __name__ == "__main__":
    main()
