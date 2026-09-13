# Project State — LSOA11 to LSOA21 Estimator

Last updated: 2026-09-13 02:31 BST | Updated by: Hermes Agent

## Current focus

Static GitHub Pages-compatible estimator for additive variables between England LSOA 2011 and LSOA 2021 geographies. The app now uses a bundled official Exact Fit + NSPL-derived crosswalk and direction-specific ONS Generalised Clipped polygon map layers.

## Working state

- Branch: `main`
- Main development mirror: `/home/kd/projects/lsoa-estimator`
- Project/tracking repo: `/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator`
- Preview URL: `http://localhost:4173/`
- App stack: Vite + TypeScript + Svelte + Tailwind + Leaflet
- Tests/checks: `npm run check`, `npm run build`, browser workflow checks, boundary/crosswalk verification script
- Blockers: none known for the current static app workflow

## Implemented app behavior

- User uploads only a variable CSV; no boundary upload is required for the standard workflow.
- Direction is auto-selected from the uploaded LSOA code column/codes:
  - LSOA 2011 input → `2011 → 2021`
  - LSOA 2021 input → `2021 → 2011`
- Relationship-level export uses columns: `lsoa2011,lsoa2021,weight,<uploaded variable>`.
- Conservation totals are shown for input and estimated output geographies.
- Preview table sorts non-1 weights first so changed-boundary rows are visible immediately.
- Methodology & Sources page documents the Exact Fit + NSPL August 2024 method, boundary map, and official source links.
- Map uses grey OpenStreetMap basemap plus ONS Generalised Clipped LSOA polygon overlays.

## Current data assets

- Crosswalk: `src/assets/data/lsoa11-to-lsoa21-crosswalk.json`
  - 33,856 official exact-fit relationship rows
  - 32,844 LSOA 2011 source areas
  - 33,755 LSOA 2021 target areas
  - 1,415,849 active residential England postcode records used as weighting evidence
- Forward map polygons: `src/assets/data/changed-lsoa21-polygons.json`
  - 1,945 changed LSOA 2021 target/output polygons
  - Source: ONS LSOA 2021 Boundaries EW BGC V5, Generalised Clipped
- Reverse map polygons: `src/assets/data/changed-lsoa11-polygons.json`
  - 1,034 changed LSOA 2011 target/output polygons
  - Source: ONS LSOA 2011 Boundaries EW BGC V3, Generalised Clipped

## Latest verification

- `npm run check` passed with 0 errors and 0 warnings.
- `npm run build` passed.
- Browser verification:
  - `2011 → 2021` loaded 1,945 SVG polygon paths and reported 1,848 non-1 output weights.
  - `2021 → 2011` loaded 1,034 SVG polygon paths and reported 200 non-1 output weights.
  - Both directions reported conservation as `Perfect Match` with the generated full test CSVs.
- Boundary asset verification:
  - changed LSOA21 target code count = 1,945; polygon features = 1,945; missing = 0.
  - changed LSOA11 target/output code count = 1,034; polygon features = 1,034; missing = 0.
  - reverse weight sums pass exactly; forward sums differ only at around 1e-8 due stored decimal rounding.

## Next actions

1. Optionally reduce production JS size by lazy-loading boundary polygon JSON only after Step 3.
2. If a public deployment is needed, push the committed repo to GitHub and enable GitHub Pages from the workflow.
3. If higher-accuracy weighting is required, add a user-provided household/address-count weighting option.

## Pointers

- Intent & roadmap: `PLAN.md`
- Architecture: `docs/architecture.md`
- Data sources/method: `docs/data-sources.md`
- Decisions: `docs/adrs/`
- App source: `src/`
- Crosswalk build script: `scripts/build_real_crosswalk.py`
