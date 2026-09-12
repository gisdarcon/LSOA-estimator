# Tasks

> Dependency-ordered, checkable breakdown of the work. `PLAN.md` is the
> *why/what*; this file is the *how, in order, with a definition of done*.

## Definition of done (applies to every task)

- [ ] Code works and tests pass
- [ ] Docs updated as applicable (PLAN.md / architecture.md / ADRs / wiki)
- [ ] No secrets committed; no `--no-verify`
- [ ] ADR added in `docs/adrs/` if a non-trivial decision was made

## Backlog

- [ ] Confirm transformation direction: LSOA11 → LSOA21 only, reverse, or both.
- [ ] Confirm target variable format and first example variable, e.g. 2021 estimated population.
- [ ] Verify NSPL/ONSPD fields needed for LSOA11 and LSOA21 correspondence.
- [ ] Compare three crosswalk methods: published ONS lookup, postcode-weighted lookup, spatial overlay.
- [ ] Add an ADR for chosen first-pass method.
- [ ] Scaffold web app tooling (`package.json`, build/test stack) after method decision.
- [ ] Build CSV parser spike for lookup and variable tables.
- [ ] Build boundary loader spike for zipped shapefile and/or GeoJSON.
- [ ] Implement share calculation and diagnostics table.
- [ ] Implement export of crosswalk and estimated target geography table.
- [ ] Add map preview of source/target boundaries and estimated values.

## In progress

- [ ] Initial project framing and data-source investigation.

## Done

- [x] 2026-09-12 — Project scaffolded from the web template under `/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator`.
- [x] 2026-09-12 — Discord project channel/session created and Telegram project group requested.

## Converge check

Before calling a milestone done, re-scan the codebase against this task list and `PLAN.md`, then append any remaining work as tasks.
