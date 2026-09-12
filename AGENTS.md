# AGENTS.md — context for AI coding agents

> Read this file first when working in this repository. It exists so an agent can get productive in one pass without re-deriving context from scratch. Keep it current — if it stops matching reality, it is wrong by design. This file is canonical; `CLAUDE.md` and `.github/copilot-instructions.md` are portability shims that point back here.

## What this project is

A web application for estimating additive variables between 2011 and 2021 Lower Layer Super Output Area geographies, starting with LSOA11 → LSOA21. The app should let users load LSOA11/LSOA21 boundaries, a postcode/geography lookup or crosswalk table, and a variable table, then calculate shares, diagnostics, maps, and exports. Full intent lives in `PLAN.md` and `README.md`.

## Where things live (docs map — read in this order)

1. `PROJECT_STATE.md` — current focus and next actions.
2. `PLAN.md` — goal, scope, milestones, open questions.
3. `tasks.md` — ordered, checkable work breakdown.
4. `docs/architecture.md` — current technical map and data flow.
5. `docs/data-sources.md` — live investigation notes for ONS/NSPL/ONSPD/boundary data.
6. `docs/adrs/` — architectural decisions and rationale.
7. `/home/kd/NAS_Hermes/wiki/` — shared durable knowledge base.
8. `RUN_LOG.md` — prepend-only journal of completed work.
9. `CONTRIBUTING.md` — repo rules for humans and agents.
10. `scripts/` — enforcement: hooks, doc lint, secret scan.
11. `src/` — future web app source.
12. `tests/` — future component/e2e tests.
13. `assets/` — static assets and examples.

## Session loop

**On session start:** read `PROJECT_STATE.md` → `PLAN.md` → recent `RUN_LOG.md` → `docs/architecture.md` → `docs/data-sources.md` → relevant `/home/kd/NAS_Hermes/wiki/` pages. Only then start the task.

**On session end:** update `PROJECT_STATE.md`, update `tasks.md`, prepend a `RUN_LOG.md` entry, and add/supersede an ADR if a non-trivial method or architecture decision was made.

## Commands

```bash
npm install
npm run dev       # dev server, once web tooling is added
npm test          # must pass before committing once tests exist
npm run build
npm run preview
python3 scripts/doc_lint.py
python3 scripts/secret_scan.py
```

## Domain conventions

- Preserve ONS geography codes exactly. Do not normalize or “fix” codes unless validation explicitly rejects them.
- Treat share-based apportionment as safe only for additive variables unless an ADR defines another method.
- Verify exact NSPL/ONSPD/lookup field names from source documentation before coding them.
- Keep method assumptions visible in the UI and docs: weight basis, unmatched records, share totals, and many-to-many mappings.
- Prefer a simple CSV lookup + variable-table proof of concept before implementing full shapefile rendering.

## Guardrails

- **Confirm before executing** destructive or high-impact actions.
- **Never publish/deploy/merge without approval.**
- **When the user says STOP, stop.**
- **Simpler path first:** use a published crosswalk or CSV spike before overbuilding spatial overlay.
- **Tests green before committing** once code exists.
- **No secrets in the repo.**
- **Check `docs/adrs/` before any architectural choice** and add/supersede ADRs for method decisions.
- **Keep docs current** when assumptions, data sources, or architecture change.
- **Do not use `git commit --no-verify`.** Fix hook failures.
- **Keep `tasks.md` current**; check a box only when done and verified.

## Gotchas / do-nots

- Do not assume NSPL/ONSPD contains every old/new geography field needed until verified for the selected release.
- Do not use postcode count as a population proxy without labeling the limitation.
- Do not apportion rates/percentages using the additive-variable method.
- Do not treat ONS “best fit” lookup as exact area/population share without verifying the metadata.

## Current state

See `PROJECT_STATE.md`.
