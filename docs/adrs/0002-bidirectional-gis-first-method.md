---
id: 0002
title: Bidirectional GIS-first method with postcode-count starting weights
status: Accepted
date: 2026-09-12
deciders: User, Hermes Agent
tags: [architecture, gis, methodology]
---

# ADR 0002 — Bidirectional GIS-first method with postcode-count starting weights

## Context

The project needs to estimate additive variables between LSOA11 and LSOA21 geographies. The user confirmed that the application must support both transformation directions, not just LSOA11 → LSOA21. The user also confirmed that the first weighting method should be postcode count, while household/residential count weighting remains a required investigation path.

The app must not be reduced to CSV-only processing. Users should be able to load GIS boundary files and the implementation should use GIS tools and spatial analysis, including point-in-polygon, to validate and derive relationships between postcode evidence and LSOA boundary geometries.

Initial library research suggests a browser-capable path is plausible:

- `shpjs` can parse zipped shapefiles to GeoJSON in browser contexts from a File API `ArrayBuffer`.
- Turf.js provides modular GeoJSON spatial analysis functions in browser and Node contexts.
- `polygon-clipping` or `martinez-polygon-clipping` can support polygon intersection/overlay spikes if Turf's higher-level operations are insufficient.

## Decision

Build the first implementation as a bidirectional GIS-first web app. The first crosswalk calculation will use postcode counts as weights, supported by point-in-polygon validation against uploaded LSOA11 and LSOA21 boundary geometries. The method model must represent source and target years generically so the same calculation path can run LSOA11 → LSOA21 and LSOA21 → LSOA11.

Keep household/residential count weighting as the next method investigation after postcode-count weighting works. Treat published ONS lookups as validation/baseline evidence, not as a replacement for GIS-capable processing.

## Consequences

- The MVP must include boundary loading and spatial analysis spikes before the method is considered viable.
- CSV tables remain useful for lookup and variable uploads, but they are not sufficient as the whole app.
- The app needs a clear internal model for `sourceYear`, `targetYear`, source code field, target code field, weight field, and share normalization direction.
- Browser performance risk is higher because LSOA boundaries and postcode-level records can be large; Web Workers and static-site-compatible chunking/progress strategies are required investigation areas. A required backend is not allowed for v1 by ADR 0003.
- Household/residential weighting needs data-source research, especially whether a suitable NSPL/ONSPD field, address count proxy, or separate residential delivery-point/address source is available and licensable.

## Alternatives considered

- **LSOA11 → LSOA21 only** — rejected because the user wants both directions.
- **CSV-only first prototype** — rejected because it would avoid the core GIS requirement and defer too much spatial risk.
- **Published ONS lookup as primary method** — useful as validation, but rejected as the primary method until it is proven to provide proportional shares and to satisfy the spatial-analysis requirement.
- **Area-only polygon overlay** — retained as a diagnostic/spike, but not accepted as the first weighting method because area share is a weak proxy for population/household distribution.
