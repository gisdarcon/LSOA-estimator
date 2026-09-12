# Project State — LSOA11 to LSOA21 Estimator

Last updated: 2026-09-12 21:55 BST | Updated by: Hermes Agent

## Current focus

Define and spike a bidirectional GIS-first web app that estimates variables between LSOA11 and LSOA21 geographies using uploaded boundaries, postcode lookup evidence, and spatial analysis.

## Working state

- Branch: `main`
- Tests: `python3 scripts/doc_lint.py` OK; `python3 scripts/secret_scan.py` OK
- Build: not configured beyond web template placeholders
- Blockers: need exact NSPL/ONSPD fields and GIS library feasibility before implementation starts

## What changed since last session

- Created project under `/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator` from the web template.
- Created Hermes Desktop Project anchored to the project root.
- Created Discord channel/session: `#p-lsoa11-to-lsoa21-estimator` / `D-LSOA11 to LSOA21 estimator`.
- Routed Telegram group/session: `P - LSOA11 to LSOA21 estimator` / `T-LSOA11 to LSOA21 estimator`.
- Started investigation of ONS postcode/geography lookups and LSOA boundary sources.
- User confirmed both LSOA11 → LSOA21 and LSOA21 → LSOA11 are required.
- User confirmed postcode count is the first weighting method, with household/residential count to investigate next.
- User confirmed GIS tooling is required: boundary loading, point-in-polygon, and other spatial analysis, not CSV-only processing.
- Added ADR 0002 for the accepted bidirectional GIS-first method.

## Next actions (ordered)

1. Verify exact fields available in the chosen NSPL/ONSPD or ONS lookup table, especially postcode point/grid references and LSOA11/LSOA21 fields.
2. Investigate household/residential count weighting sources and licensing.
3. Compare browser GIS libraries for zipped shapefile parsing, point-in-polygon, and polygon overlay.
4. Build a boundary-loader and point-in-polygon spike before committing to the implementation stack.
5. Design the generic source/target model for both transformation directions.

## Open threads

- Data source pending: exact NSPL/ONSPD fields, household/residential count source, and published lookup validation role.
- Architecture pending: browser-only vs backend-assisted processing.
- Method accepted: bidirectional GIS-first, postcode-count first; details pending for input field mapping and performance strategy.

## Pointers

- Intent & roadmap: `PLAN.md`
- Agent context & guardrails: `AGENTS.md`
- Architecture: `docs/architecture.md`
- Decisions: `docs/adrs/`
- Knowledge base: `/home/kd/NAS_Hermes/wiki/`
