# Plan — LSOA11 to LSOA21 Estimator

> Source of truth for what this project is building and why.

## Goal

Build a web application that helps users estimate a variable between 2011 and 2021 LSOA geographies by combining uploaded LSOA boundary files with postcode/geography lookup evidence, starting with an LSOA11 → LSOA21 workflow.

A useful first version lets a user load LSOA11 boundaries, LSOA21 boundaries, a lookup/crosswalk table, and a variable table, then inspect and export estimated values on the target geography.

## Scope

**In scope**

- England and Wales LSOA11 and LSOA21 boundary workflows first.
- Browser-based loading of zipped shapefiles or GeoJSON where feasible.
- Lookup-table based crosswalk construction using NSPL/ONSPD-style postcode geography fields.
- Optional use of published ONS LSOA11-to-LSOA21 best-fit/exact-fit lookup as baseline or validation source.
- Variable estimation by source-target shares, initially for additive variables such as population counts.
- Diagnostics: unmatched areas, many-to-many changes, share totals, and warnings when a variable is not safely additive.
- Export of estimated table, crosswalk table, and possibly mapped GeoJSON.

**Out of scope for the first pass**

- Scotland and Northern Ireland equivalents unless explicitly added later.
- Non-additive variable transformations without a defined method.
- Server-side processing, unless browser limits make large files unusable.
- A polished public deployment before method and data-source choices are agreed.

## Method hypothesis

1. Parse LSOA11 and LSOA21 boundaries for geometry display and code validation.
2. Parse a lookup table containing postcodes and both old/new output geographies, or use an ONS-published LSOA11-to-LSOA21 lookup where available.
3. Build a pair table: `LSOA11CD`, `LSOA21CD`, `weight`, `share_from_lsoa11`, `share_to_lsoa21`.
4. Join an uploaded variable table to the source geography.
5. Multiply values by shares and aggregate to the target geography.
6. Report diagnostics for missing geography codes, share totals not summing to 1, and many-to-many relationships.

## Milestones

| # | Milestone | Status | Notes |
|---|-----------|--------|-------|
| 1 | Project scaffold, contact sessions, and initial investigation started | ☑ | 2026-09-12 |
| 2 | Data-source decision: NSPL/ONSPD vs published LSOA11→LSOA21 lookup vs spatial overlay | ◐ | Needs confirmation |
| 3 | Minimal file parser spike for boundary + CSV lookup files | ☐ | Browser feasibility test |
| 4 | Crosswalk/share calculation prototype | ☐ | Start with postcode count or supplied weight |
| 5 | Variable estimation and diagnostics table | ☐ | Population/count variables first |
| 6 | Map preview and export flow | ☐ | Target LSOA geometry colored by estimate |
| 7 | UX walkthrough and method documentation | ☐ | Explain assumptions and limitations |

Status: ☐ not started · ◐ in progress · ☑ done · ✕ dropped

## Open questions

- Should the main workflow estimate **LSOA11 → LSOA21**, **LSOA21 → LSOA11**, or support both directions?
- Which variable table shape should be supported first: one CSV with `LSOA11CD,value`, or arbitrary named variable columns?
- Which weighting should be default: postcode count, address count, population, or a user-selected numeric field?
- Does the user expect fully local/browser processing only, or is a backend acceptable for large shapefiles/lookups?
- Should the first proof-of-concept rely on a published ONS best-fit lookup to avoid over-engineering spatial overlay?
- What is the target audience: analyst internal tool, public-facing teaching app, or production-grade estimator?

## Status log

- **2026-09-12:** Project scaffolded from the web template; Discord project channel/session created; Telegram project group requested; initial data-source investigation started.
