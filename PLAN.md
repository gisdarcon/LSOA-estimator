# Plan — LSOA11 to LSOA21 Estimator

> Source of truth for what this project is building and why.

## Goal

Build a static web application, deployable on GitHub Pages, that estimates additive variables in both directions between England LSOA 2011 and LSOA 2021 geographies using an official precomputed crosswalk and auditable proportional weights.

The current version lets a user upload a variable CSV only, auto-detects whether the source geography is LSOA 2011 or LSOA 2021, applies the correct directional weights, displays conservation/audit checks, maps changed boundary polygons, and exports detailed relationship-level rows.

## Scope

**In scope**

- England-only LSOA 2011 and LSOA 2021 workflows (`E01...`, `ctry = E92000001`).
- Static GitHub Pages-compatible deployment: no required backend, database, API keys, or server-side upload handling.
- User upload of additive variable CSVs keyed by LSOA 2011 or LSOA 2021.
- Automatic direction detection from column names and uploaded LSOA code membership.
- ONS Exact Fit Lookup V3 as the relationship authority for LSOA11↔LSOA21 pairs.
- NSPL 2011 Census August 2024 and NSPL 2021 Census August 2024 as postcode evidence for weights.
- Active residential England postcode weighting: `usertype = 0`, empty `doterm`, `ctry = E92000001`.
- Bidirectional calculation:
  - `2011 → 2021`: forward `share`, normalised within LSOA 2011.
  - `2021 → 2011`: `reverseShare`, normalised within LSOA 2021.
- Conservation diagnostics and warnings for additive-variable assumptions.
- Relationship-level CSV export with `lsoa2011,lsoa2021,weight,<variable>`.
- Direction-specific map QA using ONS Generalised Clipped polygon boundaries:
  - changed LSOA 2021 target/output polygons for `2011 → 2021`;
  - changed LSOA 2011 target/output polygons for `2021 → 2011`.

**Out of scope for the current static version**

- Scotland, Wales, and Northern Ireland transformations unless explicitly added later.
- Direct apportionment of rates, percentages, medians, or ranks without a defined numerator/denominator method.
- Required server-side GIS processing.
- Replacing agreed polygon map outputs with points/centroids without explicit user approval.

## Current method

1. Load the bundled Exact Fit + NSPL-derived crosswalk from `src/assets/data/lsoa11-to-lsoa21-crosswalk.json`.
2. Parse the uploaded CSV and detect code/value columns.
3. Auto-select direction from the code column name or by matching uploaded codes against the official 2011/2021 code sets.
4. For `2011 → 2021`, multiply each LSOA 2011 value by each relationship `share` and emit detailed LSOA11→LSOA21 rows.
5. For `2021 → 2011`, multiply each LSOA 2021 value by each relationship `reverseShare` and emit detailed LSOA11←LSOA21 rows.
6. Sum input and output values and report conservation difference.
7. Load direction-specific bundled ONS Generalised Clipped changed-boundary polygons for map QA.
8. Export detailed relationship-level CSV.

## Milestones

| # | Milestone | Status | Notes |
|---|-----------|--------|-------|
| 1 | Project scaffold, contact sessions, and initial investigation started | ☑ | 2026-09-12 |
| 2 | Data-source and method decision: bidirectional GIS-first workflow, postcode-count first | ☑ | ADR 0002 |
| 3 | Static Vite + TypeScript + Svelte app scaffold and build checks | ☑ | GitHub Pages-compatible Vite app |
| 4 | Real Exact Fit + NSPL-derived crosswalk | ☑ | ONS Exact Fit V3 + NSPL August 2024 active residential postcodes |
| 5 | Bidirectional variable estimation and export | ☑ | Auto-direction, conservation, relationship-level CSV |
| 6 | Direction-specific ONS polygon map preview | ☑ | Generalised Clipped LSOA21 and LSOA11 changed polygons |
| 7 | Methodology and source documentation | ☑ | In-app methodology page and project docs updated |

Status: ☐ not started · ◐ in progress · ☑ done · ✕ dropped

## Open questions

- Should the public build lazy-load boundary polygon JSON to reduce first-load bundle size?
- Should a household/address-count weighting option be added as an advanced mode?
- What GitHub repository URL should receive the final pushed deployment branch?

## Status log

- **2026-09-13:** Reinstated polygon maps after rejecting point substitutes; forward uses changed LSOA21 Generalised Clipped polygons and reverse uses changed LSOA11 Generalised Clipped polygons.
- **2026-09-13:** Methodology and docs updated to reflect actual Exact Fit + NSPL August 2024 method and boundary sources.
- **2026-09-13:** Browser verified both directions with full test CSVs and conservation checks.
- **2026-09-12:** User confirmed the app must be static and GitHub Pages-compatible; ADR 0003 added.
- **2026-09-12:** User selected Vite + TypeScript + Svelte, Turf.js, and shpjs; ADR 0004 added.
- **2026-09-12:** User confirmed both directions, postcode-count first, household/residential count as follow-up, and GIS/spatial analysis as required; ADR 0002 added.
