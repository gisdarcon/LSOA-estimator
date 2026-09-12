# Architecture — LSOA11 to LSOA21 Estimator

> Living map of how the project is built now. Update when structure or method changes.

Last updated: 2026-09-12

## System overview

Planned browser-based geospatial estimator for translating additive variables between LSOA11 and LSOA21 geographies. The first architecture is still investigative: define the method, validate input file formats, then build the smallest working parser/calculation path.

## Proposed module map

| Module / package | Responsibility | Key files | Depends on |
|---|---|---|---|
| Input loader | Load boundaries, lookup tables, and variable CSVs | `src/` TBD | Browser File API, CSV parser, geospatial parser |
| Geography validator | Check LSOA codes and required columns | `src/` TBD | Input loader |
| Crosswalk builder | Convert lookup records into LSOA11↔LSOA21 shares | `src/` TBD | Geography validator |
| Estimator | Apply shares to additive variables and aggregate target values | `src/` TBD | Crosswalk builder |
| Diagnostics | Report unmatched rows, many-to-many mappings, share totals, warnings | `src/` TBD | Crosswalk builder, estimator |
| Map/export UI | Preview target boundaries and export outputs | `src/` TBD | Estimator, boundary loader |

## Initial data flow hypothesis

1. User loads LSOA11 boundaries.
2. User loads LSOA21 boundaries.
3. User loads NSPL/ONSPD-style lookup or published LSOA11-to-LSOA21 lookup.
4. User loads variable CSV keyed by source geography.
5. App validates required columns and geography code coverage.
6. App builds source-target shares.
7. App multiplies source variable values by shares and aggregates to target geography.
8. App shows diagnostics, map preview, and exportable tables.

## Data model draft

| Entity | Key fields | Notes |
|---|---|---|
| `BoundaryFeature` | `code`, `name`, `geometry`, `year` | LSOA11/LSOA21 features from uploaded boundaries |
| `LookupRecord` | `postcode`, `lsoa11cd`, `lsoa21cd`, optional weight fields | Exact fields depend on selected NSPL/ONSPD/lookup source |
| `CrosswalkPair` | `source_lsoa`, `target_lsoa`, `weight`, `share` | Share sums should be checked per source and/or target |
| `VariableRecord` | `source_lsoa`, `value`, optional metadata | Additive count variables first |
| `EstimateRecord` | `target_lsoa`, `estimated_value`, diagnostics | Output table and map join target |

## External systems & data sources under investigation

| System/source | Role | Notes |
|---|---|---|
| NSPL / ONSPD | Postcode-to-geography lookup evidence | Need to verify exact fields and whether both LSOA11 and LSOA21 are present in chosen release |
| ONS Geography/data.gov.uk LSOA boundaries | LSOA11 and LSOA21 geometry | Need final download URLs and preferred format |
| ONS LSOA11 to LSOA21 lookup | Possible baseline crosswalk | Search result indicates an LSOA 2011 to LSOA 2021 best-fit lookup exists for England and Wales |

## Architectural decisions pending

| Decision | Status | ADR |
|---|---|---|
| Browser-only vs backend-assisted processing | pending | TBD |
| Canonical crosswalk method | pending | TBD |
| Supported first input formats | pending | TBD |

## Performance & constraints

- Large boundary and postcode lookup files may exceed comfortable browser memory limits.
- Zipped shapefile parsing in-browser needs validation before committing to browser-only processing.
- Additive variables are safer for share-based apportionment than rates, medians, or percentages.
- ONS geography codes and lookup columns must be treated exactly; do not guess field names in code.
