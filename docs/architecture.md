# Architecture — LSOA11 to LSOA21 Estimator

> Living map of how the project is built now. Update when structure or method changes.

Last updated: 2026-09-13

## System overview

Static, GitHub Pages-compatible browser app for translating additive variables between England LSOA 2011 and LSOA 2021 geographies. The production path uses a bundled ONS Exact Fit + NSPL-derived crosswalk and bundled changed-boundary polygon layers; users upload only their variable CSV.

## Runtime architecture

| Area | Responsibility | Key files |
|---|---|---|
| App shell | Wizard, theme, status, methodology, upload/run/export flow | `src/App.svelte` |
| CSV parser | Parse generic LSOA/value CSVs and detect code/value columns | `src/lib/simple-parser.ts` |
| Crosswalk asset | Static relationship table with forward and reverse weights | `src/assets/data/lsoa11-to-lsoa21-crosswalk.json` |
| Estimation engine | Apply directional weights and emit detailed relationship rows | `src/lib/estimation-engine.ts` |
| Exporter | Write `lsoa2011,lsoa2021,weight,<variable>` CSV | `src/lib/exporter.ts` |
| Boundary service | Select direction-specific bundled ONS changed-polygon layer | `src/lib/boundary-service.ts` |
| Map UI | Leaflet map with grey OSM basemap and ONS polygon overlays | `src/lib/MapPreview.svelte` |
| Methodology UI | In-app method/source documentation | `src/lib/MethodologyModal.svelte` |
| Crosswalk builder | Rebuild real weights from raw ONS Exact Fit + NSPL files | `scripts/build_real_crosswalk.py` |

## Data flow

1. Load bundled crosswalk metadata in the browser.
2. User uploads a CSV containing LSOA codes and one additive numeric variable.
3. App detects whether input codes are LSOA 2011 or LSOA 2021.
4. User runs national estimation.
5. Engine applies:
   - `share` for `2011 → 2021`, normalised within each LSOA11;
   - `reverseShare` for `2021 → 2011`, normalised within each LSOA21.
6. App reports input/output totals and conservation difference.
7. App loads the matching changed-boundary polygon layer:
   - `changed-lsoa21-polygons.json` for `2011 → 2021`;
   - `changed-lsoa11-polygons.json` for `2021 → 2011`.
8. App renders map, split statistics, preview rows, and CSV export.

## Core data model

| Entity | Key fields | Notes |
|---|---|---|
| `ShareResult` | `source_lsoa`, `target_lsoa`, `share`, `reverseShare` | `source_lsoa` is LSOA11; `target_lsoa` is LSOA21 |
| `VariableRow` | `code`, `value` | Parsed user variable input |
| `DetailedEstimateRow` | `lsoa2011`, `lsoa2021`, `ratio`, `value` | Exporter writes `ratio` as `weight` |
| Boundary FeatureCollection | `LSOA11CD` or `LSOA21CD`, name, polygon geometry | ONS Generalised Clipped changed polygons |

## Static assets

| Asset | Purpose | Size/coverage |
|---|---|---|
| `src/assets/data/lsoa11-to-lsoa21-crosswalk.json` | Relationship weights | 33,856 rows |
| `src/assets/data/changed-lsoa21-polygons.json` | Forward map polygons | 1,945 changed LSOA21 target/output polygons |
| `src/assets/data/changed-lsoa11-polygons.json` | Reverse map polygons | 1,034 changed LSOA11 target/output polygons |

## External source data

- ONS LSOA 2011 to LSOA 2021 Exact Fit Lookup V3.
- National Statistics Postcode Lookup - 2011 Census (August 2024) for the UK.
- National Statistics Postcode Lookup - 2021 Census (August 2024) for the UK.
- Lower Layer Super Output Areas (December 2011) Boundaries EW BGC V3, Generalised Clipped.
- Lower Layer Super Output Areas (December 2021) Boundaries EW BGC V5, Generalised Clipped.

## Performance constraints

- The static app should not require server-side GIS or credentials.
- Full national polygon rendering is avoided in the standard map because it is too heavy for the browser UI. The app maps changed polygons only, preserving polygon representation without loading all LSOAs.
- Current production bundle is large because changed polygon JSON is bundled into the main build. A future optimization is to lazy-load these JSON assets only after Step 3.
- Rates, percentages, medians, and ranks are not directly safe for proportional apportionment.

## Accepted architectural decisions

| Decision | Status | ADR |
|---|---|---|
| Bidirectional GIS-first method | accepted | [0002](adrs/0002-bidirectional-gis-first-method.md) |
| Static GitHub Pages deployment | accepted | [0003](adrs/0003-static-github-pages-deployment.md) |
| Static client library stack | accepted | [0004](adrs/0004-static-client-library-stack.md) |
| Official Exact Fit + NSPL static crosswalk and ONS polygon map layers | accepted | [0005](adrs/0005-official-crosswalk-and-boundary-map-assets.md) |
