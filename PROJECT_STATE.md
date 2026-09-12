# Project State — LSOA11 to LSOA21 Estimator

Last updated: 2026-09-12 21:43 BST | Updated by: Hermes Agent

## Current focus

Define the first viable method and UX for a web app that estimates variables between LSOA11 and LSOA21 geographies using uploaded boundaries and lookup/crosswalk evidence.

## Working state

- Branch: `main`
- Tests: not run — scaffold/documentation only so far
- Build: not configured beyond web template placeholders
- Blockers: need method decisions before implementation starts

## What changed since last session

- Created project under `/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator` from the web template.
- Created Hermes Desktop Project anchored to the project root.
- Created Discord channel/session: `#p-lsoa11-to-lsoa21-estimator` / `D-LSOA11 to LSOA21 estimator`.
- Routed Telegram group/session: `P - LSOA11 to LSOA21 estimator` / `T-LSOA11 to LSOA21 estimator`.
- Started investigation of ONS postcode/geography lookups and LSOA boundary sources.

## Next actions (ordered)

1. Confirm the intended transformation direction: LSOA11 → LSOA21 only, or both directions.
2. Decide the first weighting method: postcode count, address/delivery point count, population/household weight, or user-provided weight column.
3. Verify exact fields available in the chosen NSPL/ONSPD or ONS lookup table.
4. Decide whether the first MVP uses a published LSOA11↔LSOA21 lookup, lookup-derived shares, or spatial overlay.
5. Build a minimal parser spike for CSV lookup + variable table before adding shapefile rendering.

## Open threads

- Data source pending: NSPL vs ONSPD vs published LSOA11-to-LSOA21 lookup.
- Architecture pending: browser-only vs backend-assisted processing.
- Method details pending: transformation direction, weighting basis, and first input file format.

## Pointers

- Intent & roadmap: `PLAN.md`
- Agent context & guardrails: `AGENTS.md`
- Architecture: `docs/architecture.md`
- Decisions: `docs/adrs/`
- Knowledge base: `/home/kd/NAS_Hermes/wiki/`
