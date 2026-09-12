# Architecture — LSOA11 to LSOA21 Estimator

> Living map of how the project is built now. Update when structure or method changes.

Last updated: 2026-09-12

## System overview

Planned static, GitHub Pages-compatible browser GIS estimator for translating additive variables in both directions between LSOA11 and LSOA21 geographies. The first accepted method is a bidirectional, GIS-first workflow using postcode-count weights, point-in-polygon validation against uploaded boundaries, and later investigation of household/residential count weights. All core v1 processing runs client-side and uses the client machine's browser resources for difficult computations.

## Proposed module map

| Module / package | Responsibility | Key files | Depends on |
|---|---|---|---|
| Static app shell | GitHub Pages-compatible Svelte app bundle and route handling | `src/` TBD | Vite, TypeScript, Svelte |
| Input loader | Load boundaries, postcode lookup tables, and variable CSVs from local files | `src/` TBD | Browser File API, CSV parser, shapefile/GeoJSON parser |
| Worker spatial engine | Use client processing resources to build spatial indexes and run point-in-polygon/overlay checks without blocking UI | `src/` TBD | Web Workers, input loader, Turf.js |
| Geography validator | Check LSOA codes, required columns, and spatial/code mismatches | `src/` TBD | Input loader, spatial engine |
| Crosswalk builder | Convert lookup records into bidirectional LSOA11↔LSOA21 shares | `src/` TBD | Geography validator |
| Estimator | Apply shares to additive variables and aggregate target values | `src/` TBD | Crosswalk builder |
| Diagnostics | Report unmatched rows, many-to-many mappings, share totals, warnings | `src/` TBD | Crosswalk builder, estimator |
| Map/export UI | Preview source/target boundaries, postcode diagnostics, and export outputs | `src/` TBD | Estimator, boundary loader |

## Initial data flow hypothesis

1. User loads LSOA11 boundaries.
2. User loads LSOA21 boundaries.
3. User selects transformation direction: LSOA11 → LSOA21 or LSOA21 → LSOA11.
4. User loads NSPL/ONSPD-style postcode lookup with postcode point/grid reference evidence and old/new LSOA fields where available.
5. User loads variable CSV keyed by selected source geography.
6. App validates required columns, geography code coverage, and point-in-polygon consistency.
7. App builds source-target shares from postcode counts.
8. App multiplies source variable values by shares and aggregates to target geography.
9. App shows diagnostics, map preview, and exportable tables.

## Data model draft

| Entity | Key fields | Notes |
|---|---|---|
| `BoundaryFeature` | `code`, `name`, `geometry`, `year` | LSOA11/LSOA21 features from uploaded boundaries |
| `LookupRecord` | `postcode`, `point`, `lsoa11cd`, `lsoa21cd`, optional weight fields | Exact fields depend on selected NSPL/ONSPD/lookup source |
| `SpatialAssignment` | `postcode`, `boundary_year`, `lsoa_code_from_point`, `lsoa_code_from_lookup`, `status` | Captures point-in-polygon validation/derivation results |
| `CrosswalkPair` | `source_lsoa`, `target_lsoa`, `postcode_count`, `share`, `direction` | Share sums checked per selected source geography |
| `VariableRecord` | `source_lsoa`, `value`, optional metadata | Additive count variables first |
| `EstimateRecord` | `target_lsoa`, `estimated_value`, diagnostics | Output table and map join target |

## External systems & data sources under investigation

| System/source | Role | Notes |
|---|---|---|
| NSPL / ONSPD | Postcode-to-geography lookup evidence | Need to verify exact fields and whether both LSOA11 and LSOA21 are present in chosen release |
| ONS Geography/data.gov.uk LSOA boundaries | LSOA11 and LSOA21 geometry | Need final download URLs and preferred format |
| ONS LSOA11 to LSOA21 lookup | Possible baseline crosswalk | Search result indicates an LSOA 2011 to LSOA 2021 best-fit lookup exists for England and Wales |
| `shpjs` | Candidate browser shapefile parser | Research indicates it can parse zipped shapefiles from File API `ArrayBuffer` to GeoJSON |
| Turf.js | Candidate browser/Node spatial analysis toolkit | Research indicates modular GeoJSON spatial analysis functions usable without sending data to a server |
| `polygon-clipping` / `martinez-polygon-clipping` | Candidate polygon overlay engine | For intersection/overlay spikes if higher-level Turf operations are insufficient |

Selected first stack: Vite + TypeScript + Svelte for the app framework, Turf.js for point-in-polygon/GeoJSON analysis, and `shpjs` for browser ZIP shapefile parsing. See [ADR 0004](adrs/0004-static-client-library-stack.md).

Library choices are not automatic: before adding GIS, UI, build, mapping, CSV, or deployment libraries to the project, present the viable options with trade-offs and ask the user to select the preferred option.

## Architectural decisions pending

| Decision | Status | ADR |
|---|---|---|
| Browser-only/static vs backend-assisted processing | accepted: static/browser-only v1 | [0003](adrs/0003-static-github-pages-deployment.md) |
| Canonical first-pass crosswalk method | accepted | [0002](adrs/0002-bidirectional-gis-first-method.md) |
| Static client library stack | accepted | [0004](adrs/0004-static-client-library-stack.md) |
| Supported first input formats | pending | TBD |
| Major app/library choices | pending user selection | TBD |

## Performance & constraints

- Large boundary and postcode lookup files may exceed comfortable browser memory limits.
- Zipped shapefile parsing in-browser needs validation before committing to browser-only processing.
- Point-in-polygon for postcode points and other difficult computations should use client browser processing resources and run in a Web Worker if datasets are large enough to block the UI.
- GitHub Pages hosting means no required backend, server-side secrets, upload storage, database, or server-side GIS processing in v1.
- The built app must work from a repository subpath, so route handling/base paths must be GitHub Pages-safe.
- Polygon overlay/area calculations require careful projection choices; do not compute areas on raw WGS84 coordinates without validating the method.
- Additive variables are safer for share-based apportionment than rates, medians, or percentages.
- ONS geography codes and lookup columns must be treated exactly; do not guess field names in code.
