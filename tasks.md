# Tasks

> Dependency-ordered, checkable breakdown of the work. `PLAN.md` is the
> *why/what*; this file is the *how, in order, with a definition of done*.

## Definition of done (applies to every task)

- [x] Code works and checks pass
- [x] Docs updated as applicable (PLAN.md / architecture.md / ADRs / wiki)
- [x] No secrets committed; no `--no-verify`
- [x] ADR added in `docs/adrs/` if a non-trivial decision was made

## Completed

- [x] Confirm England-only LSOA 2011 and LSOA 2021 scope.
- [x] Verify NSPL fields needed for LSOA11 and LSOA21 correspondence.
- [x] Investigate household/residential count weighting sources and licensing.
- [x] Compare GIS implementation libraries and select Vite + TypeScript + Svelte, Turf.js, shpjs, and Leaflet.
- [x] Scaffold static GitHub Pages-compatible Vite + TypeScript + Svelte app tooling.
- [x] Configure GitHub Pages deployment workflow.
- [x] Build CSV parser for variable uploads.
- [x] Build boundary-loader and spatial-analysis spikes.
- [x] Implement share calculation logic using precomputed official weights.
- [x] Replace mock/50-50 shares with real ONS Exact Fit Lookup V3 + NSPL August 2024 active residential postcode-count weights.
- [x] Implement bidirectional estimation:
  - [x] `2011 → 2021` using forward `share`.
  - [x] `2021 → 2011` using `reverseShare`.
- [x] Implement automatic direction detection from uploaded code column/codes.
- [x] Implement conservation/audit cards and non-1 weight preview sorting.
- [x] Implement detailed export: `lsoa2011,lsoa2021,weight,<uploaded variable>`.
- [x] Generate full test CSVs:
  - [x] `assets/test-variable-lsoa11-full.csv` with 32,844 actual LSOA11 codes.
  - [x] `assets/test-variable-lsoa21-full.csv` with 33,755 actual LSOA21 codes.
- [x] Implement grey basemap using standard OpenStreetMap tiles with grayscale styling.
- [x] Implement direction-specific ONS Generalised Clipped polygon maps:
  - [x] 1,945 changed LSOA21 target/output polygons for `2011 → 2021`.
  - [x] 1,034 changed LSOA11 target/output polygons for `2021 → 2011`.
- [x] Update Methodology & Sources page with current crosswalk method, map behavior, and ONS links.
- [x] Verify boundary-change calculation and presentation in code, UI, methodology, and docs.

## Latest verification checklist

- [x] `npm run check` passes with 0 errors and 0 warnings.
- [x] `npm run build` passes.
- [x] Crosswalk has 33,856 exact-fit rows, 32,844 LSOA11 areas, and 33,755 LSOA21 areas.
- [x] Changed LSOA21 target codes = 1,945; bundled LSOA21 polygon features = 1,945; missing = 0.
- [x] Changed LSOA11 target/output codes = 1,034; bundled LSOA11 polygon features = 1,034; missing = 0.
- [x] Browser verification for `2011 → 2021` renders 1,945 SVG polygon paths.
- [x] Browser verification for `2021 → 2011` renders 1,034 SVG polygon paths.
- [x] Both full test workflows show conservation as `Perfect Match`.
- [x] No point/centroid map layer remains in the app.

## Backlog / optional next steps

- [ ] Lazy-load boundary polygon JSON after Step 3 to reduce first-load production bundle size.
- [ ] Add user-uploaded household/address-count weights as an advanced method.
- [ ] Add public deployment URL once GitHub repository/pages setup is confirmed.

## Converge check

Before calling a milestone done, re-scan the codebase against this task list and `PLAN.md`, run checks/build, and verify a browser workflow in both directions.
