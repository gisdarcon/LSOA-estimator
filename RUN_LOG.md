# Run Log

> **Prepend-only record of what happened and when.** New entries go on top; past
> entries are never rewritten or deleted.

## [2026-09-12 21:58] Hermes Agent | Static hosting requirement captured

- Captured user decision that the web app must be static and able to be served by GitHub Pages.
- Added ADR 0003 requiring browser-only/static v1 processing, GitHub Pages-safe routing/base paths, and no required backend/server upload handling.
- Updated plan, architecture, project state, and task list to treat static hosting as a hard constraint.

## [2026-09-12 21:55] Hermes Agent | Method decisions captured

- Captured user decisions: support both LSOA11 → LSOA21 and LSOA21 → LSOA11; start weights with postcode count; investigate household/residential count next.
- Captured requirement that the app must implement GIS tools/libraries, not just CSV processing.
- Added ADR 0002 for a bidirectional GIS-first method using boundary loading, point-in-polygon validation, and postcode-count shares.
- Updated plan, architecture, data-source investigation, project state, and task list to bring GIS/spatial-analysis risk forward.

## [2026-09-12 21:43] Hermes Agent | Project created and investigation started

- Scaffolded `/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator` from the web template, initialized git, and installed hooks.
- Created Hermes Desktop Project `LSOA11 to LSOA21 estimator` anchored to the project root.
- Created Discord project channel/session: `#p-lsoa11-to-lsoa21-estimator` / `D-LSOA11 to LSOA21 estimator`.
- Requested and then routed Telegram project group/session: `P - LSOA11 to LSOA21 estimator` / `T-LSOA11 to LSOA21 estimator`.
- Sent a starter message in Discord project channel with the first method questions.
- Framed the first method questions: NSPL/ONSPD vs published ONS LSOA lookup vs spatial overlay; weighting method; browser-only feasibility.
- Watch-outs: additive variables only for first pass; verify exact ONS field names before implementation.

## [2026-09-09] <you/agent> | Project initialized

- Scaffolded from the web template: README, PLAN, AGENTS, wiki, ADRs, architecture.
- Adopted ADR catalogue (see docs/adrs/0001).
- Next: define the project goal in PLAN.md and the first real task.
