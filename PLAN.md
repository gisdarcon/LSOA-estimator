# Plan — LSOA11 to LSOA21 Estimator

> Source of truth for what this project is building and why.

## Goal

Build a static web application, deployable on GitHub Pages, that helps users estimate additive variables in both directions between 2011 and 2021 LSOA geographies by combining uploaded LSOA boundary files with postcode/geography lookup evidence and GIS spatial analysis.

A useful first version lets a user load LSOA11 boundaries, LSOA21 boundaries, an NSPL/ONSPD-style postcode lookup, and a variable table, then choose LSOA11 → LSOA21 or LSOA21 → LSOA11, inspect spatial diagnostics, and export estimated values on the target geography.

## Scope

**In scope**

- England and Wales LSOA11 and LSOA21 boundary workflows first, in both directions.
- Browser-based loading of zipped shapefiles or GeoJSON where feasible.
- Static GitHub Pages-compatible deployment: all v1 processing runs client-side with no required backend.
- GIS-first processing: point-in-polygon checks, spatial validation, and later polygon overlay/area-share diagnostics where useful.
- Lookup-table based crosswalk construction using NSPL/ONSPD-style postcode geography fields.
- Optional use of published ONS LSOA11-to-LSOA21 best-fit/exact-fit lookup as baseline or validation source.
- Variable estimation by source-target shares, initially for additive variables such as population counts.
- First weighting method: postcode count by source-target LSOA pair.
- Follow-up weighting investigation: household/residential count or delivery-point/address-count proxy where a suitable source exists.
- Diagnostics: unmatched areas, many-to-many changes, share totals, and warnings when a variable is not safely additive.
- Export of estimated table, crosswalk table, and possibly mapped GeoJSON.

**Out of scope for the first pass**

- Scotland and Northern Ireland equivalents unless explicitly added later.
- Non-additive variable transformations without a defined method.
- Required server-side processing for v1; if browser limits are hit, reduce scope, use Web Workers/chunking, or record a separate optional-backend decision later.
- A polished public deployment before method and data-source choices are agreed.

## Method hypothesis

1. Parse LSOA11 and LSOA21 boundaries for geometry display, code validation, and spatial indexing.
2. Parse a postcode lookup table containing postcode point/grid references and old/new LSOA geography fields where available.
3. Use point-in-polygon checks to validate or derive each postcode's LSOA11 and LSOA21 relationship against the uploaded boundaries.
4. Build a generic source-target pair table from the selected direction: `source_lsoa`, `target_lsoa`, `postcode_count`, `share`.
5. Join an uploaded variable table to the selected source geography.
6. Multiply values by shares and aggregate to the selected target geography.
7. Report diagnostics for missing geography codes, point-in-polygon mismatches, share totals not summing to 1, and many-to-many relationships.

## Milestones

| # | Milestone | Status | Notes |
|---|-----------|--------|-------|
| 1 | Project scaffold, contact sessions, and initial investigation started | ☑ | 2026-09-12 |
| 2 | Data-source and method decision: bidirectional GIS-first workflow, postcode-count first | ☑ | ADR 0002 |
| 3 | Minimal static GIS parser spike for zipped shapefile/GeoJSON + postcode lookup files | ☐ | Browser + Web Worker feasibility test; GitHub Pages-compatible build |
| 4 | Crosswalk/share calculation prototype | ☐ | Start with postcode count, support both directions |
| 5 | Variable estimation and diagnostics table | ☐ | Population/count variables first |
| 6 | Map preview and export flow | ☐ | Target LSOA geometry colored by estimate |
| 7 | UX walkthrough and method documentation | ☐ | Explain assumptions and limitations |

Status: ☐ not started · ◐ in progress · ☑ done · ✕ dropped

## Open questions

- Which variable table shape should be supported first: one CSV with `LSOA11CD,value`, or arbitrary named variable columns?
- Which household/residential-count source is usable for the second weighting method?
- What maximum upload sizes should the GitHub Pages/browser-only MVP support comfortably?
- What is the target audience: analyst internal tool, public-facing teaching app, or production-grade estimator?

## Status log

- **2026-09-12:** User confirmed the app must be static and GitHub Pages-compatible; ADR 0003 added.
- **2026-09-12:** User confirmed both directions, postcode-count first, household/residential count as follow-up, and GIS/spatial analysis as required; ADR 0002 added.
- **2026-09-12:** Project scaffolded from the web template; Discord project channel/session created; Telegram project group requested; initial data-source investigation started.
