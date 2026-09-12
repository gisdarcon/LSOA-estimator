# Tasks

> Dependency-ordered, checkable breakdown of the work. `PLAN.md` is the
> *why/what*; this file is the *how, in order, with a definition of done*.

## Definition of done (applies to every task)

- [ ] Code works and tests pass
- [ ] Docs updated as applicable (PLAN.md / architecture.md / ADRs / wiki)
- [ ] No secrets committed; no `--no-verify`
- [ ] ADR added in `docs/adrs/` if a non-trivial decision was made

## Backlog

- [ ] Confirm target variable format and first example variable, e.g. 2021 estimated population.
- [ ] Verify NSPL/ONSPD fields needed for LSOA11 and LSOA21 correspondence.
- [ ] Investigate household/residential count weighting sources and licensing.
- [ ] Compare GIS implementation libraries for shapefile parsing, point-in-polygon, and polygon overlay.
- [ ] Scaffold static GitHub Pages-compatible web app tooling (`package.json`, build/test stack, static output config).
- [ ] Add GitHub Pages deployment notes/workflow once repository hosting details are known.
- [ ] Build CSV parser spike for lookup and variable tables.
- [ ] Build boundary loader spike for zipped shapefile and/or GeoJSON.
- [ ] Build point-in-polygon spike for postcode points against LSOA11 and LSOA21 boundaries.
- [ ] Implement share calculation and diagnostics table.
- [ ] Implement export of crosswalk and estimated target geography table.
- [ ] Add map preview of source/target boundaries and estimated values.

## In progress

- [ ] Initial project framing and data-source investigation.
- [ ] GIS library and household/residential weighting investigation.
- [ ] Static GitHub Pages deployment constraints investigation.

## Done

- [x] 2026-09-12 — Project scaffolded from the web template under `/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator`.
- [x] 2026-09-12 — Discord project channel/session created and Telegram project group routed.
- [x] 2026-09-12 — User confirmed bidirectional workflow, postcode-count first weighting, household/residential follow-up, and GIS/spatial analysis requirement.
- [x] 2026-09-12 — ADR 0002 accepted for bidirectional GIS-first method.
- [x] 2026-09-12 — User confirmed the app must be static and GitHub Pages-compatible.
- [x] 2026-09-12 — ADR 0003 accepted for static GitHub Pages deployment.

## Converge check

Before calling a milestone done, re-scan the codebase against this task list and `PLAN.md`, then append any remaining work as tasks.
