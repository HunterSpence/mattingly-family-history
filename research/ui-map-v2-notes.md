# Migration Map v2 — Design Notes

## What changed

The v1 map was a hand-drawn blob: a single `<polygon>` approximating the continental US outline with manually tuned SVG coordinates. It looked stylized but not credible as a map.

v2 replaces the static SVG continent with a runtime D3-geo render using real geographic data.

## Approach

**Projection:** `d3.geoNaturalEarth1()` centered at lon -40, lat 38 with scale 520. This frames the North Atlantic so both Hampshire (England) and Santa Monica (California) sit comfortably within the 900x480 viewport with room for ocean labels.

**Data source:** `world-atlas@2/countries-110m.json` via `cdn.jsdelivr.net` (TopoJSON, ~100KB gzipped). Parsed with `topojson-client@3` (unpkg CDN). Both are loaded in the HTML head after D3 v7.

**What D3 draws at runtime:**
- Country fill polygons (#231d14, very dark warm brown)
- Land silhouette over-layer (#2c2316 with #4a3c28 stroke)
- Country borders mesh (very subtle, #352a1a)
- Graticule (latitude/longitude grid, 5.5% opacity gold)

**Waypoints:** All 9 locations use actual lat/lon (e.g., Bardstown KY: 37.81, -85.47; Reeves County TX: 31.40, -103.50). D3's projection converts these to SVG pixel coordinates, so every marker sits on its real geographic position.

**Atlantic arc:** Drawn as a true great-circle `LineString` through D3's path generator, giving it the natural curved shape of an ocean crossing rather than a cubic bezier guess.

**Animated path:** The existing `stroke-dashoffset` draw animation is preserved. JS reads `getTotalLength()` on the real polyline and sets the dasharray dynamically, so the animation always draws the exact path length.

**Tooltip system:** Unchanged — same `mouseenter`/`mousemove`/`click` handlers, same HTML structure, same CSS. Marker data attached as `data-*` attributes on `<g>` elements.

## Preserved from v1

- Dark archive palette: ocean #090706, land ~#2c2316, accent gold #d4a458
- Vignette radial gradient overlay
- Compass rose (enhanced with outer circle)
- Pulse ring animations on markers
- Responsive SVG (viewBox 900x480, width:100%)
- Print media query hide, prefers-reduced-motion guard
- Tooltip card styling (Cormorant Garamond + Lora + Source Code Pro)

## Output

Build: `python scripts/build_html.py`
Output: `output/grandma-shari-family-history.html` (351KB)
