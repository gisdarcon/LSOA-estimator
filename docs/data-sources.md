# Data Sources Investigation — LSOA11 to LSOA21 Estimator

Last updated: 2026-09-12

## Purpose

Track candidate data sources for deriving or validating shares between LSOA11 and LSOA21. This is investigation material, not yet an architectural decision.

## User requirement

The app should allow users to load LSOA11 boundaries and LSOA21 boundaries, use an NSPL/ONSPD-style postcode lookup to identify shares between boundary changes, and estimate additive variables such as 2021 estimated population. The workflow must support both LSOA11 → LSOA21 and LSOA21 → LSOA11.

## Sources found so far

### ONSPD / postcode-to-geography lookups

Search result found a data.gov.uk page for “Postcode to OA (2021) to LSOA to MSOA to LAD (February 2025) Best Fit Lookup in the UK”. The result description says it contains fields including `PCD7`, `PCD8`, `PCDS`, `OA21CD`, `LSOA21CD`, `MSOA21CD`, `LADCD`, and names. This looks useful for postcodes to 2021 geography, but does not by itself prove that LSOA11 is present.

Search result also found “ONS Postcode Directory (November 2025) for the UK (Hosted Table)”. The result description says ONSPD relates current and terminated postcodes to a range of geographies and includes 2021 Census OA hierarchy for England, Wales, and Northern Ireland. Need to verify whether the selected release includes 2011 LSOA fields in the same table, or whether a separate historical lookup is needed.

### LSOA11 to LSOA21 lookup

Search result text from data.gov.uk indicates an “LSOA 2011 to LSOA 2021 to Local Authority District (2022) Best Fit Lookup” exists for England and Wales. This may be the safest first baseline crosswalk, but “best fit” is not necessarily a proportional share table. Need metadata.

### Boundary files

Search result text indicates ONS Geography/data.gov.uk has “Lower layer Super Output Areas (December 2021) Boundaries EW” datasets in multiple formats including GeoJSON, ZIP, GPKG, and GDB. Need exact pages for:

- LSOA 2011 boundaries, England and Wales
- LSOA 2021 boundaries, England and Wales
- preferred resolution: full, generalised, or clipped

### Browser GIS libraries

Initial web research found candidate libraries for a GIS-first implementation:

- `shpjs`: parses zipped shapefiles to GeoJSON in pure JavaScript, including browser File API `ArrayBuffer` inputs.
- Turf.js: modular GeoJSON spatial-analysis toolkit for browser and Node contexts; candidate for point-in-polygon, measurement, and other analysis functions.
- `polygon-clipping` / `martinez-polygon-clipping`: candidate polygon boolean/intersection libraries for overlay spikes if needed.

## Candidate methods

### Method A — Published ONS LSOA11→LSOA21 lookup first

Use the published ONS LSOA11-to-LSOA21 lookup as the initial crosswalk source. If it is best-fit only, use it for code correspondence and validation, not proportional shares unless metadata supports that.

Pros:
- likely easiest and most authoritative first pass
- avoids browser-heavy geometry overlay
- good for validating user-uploaded codes

Cons:
- may not provide proportional shares
- may hide many-to-many boundary-change detail

### Method B — Postcode-weighted lookup shares

Use NSPL/ONSPD records as evidence. Count or weight postcodes by source-target LSOA pairs, then calculate shares. This is the accepted first method, starting with postcode count and supporting both directions by swapping source and target.

Pros:
- aligns with user’s requested NSPL-based approach
- can produce proportional shares if suitable weights exist
- transparent and reproducible

Cons:
- postcode count is not population count
- terminated/current postcode handling matters
- needs verified old and new LSOA fields

Follow-up:
- investigate a household/residential count weight, preferably based on a defensible delivery-point, residential-address, or household proxy rather than raw postcode count

### Method C — Spatial overlay of boundaries

Intersect LSOA11 and LSOA21 geometries and use area shares.

Pros:
- independent of postcode lookup availability
- directly reflects geometry changes

Cons:
- area is often a poor population/share proxy
- computationally heavier in browser
- requires robust projection and geometry handling

## Early recommendation

Superseded by ADR 0002. Do **not** start with a CSV-only prototype. Start with a GIS parser/spatial-analysis spike:

1. Load LSOA11 and LSOA21 boundaries from zipped shapefile and/or GeoJSON.
2. Load postcode lookup data with point/grid-reference fields and LSOA11/LSOA21 fields where available.
3. Run point-in-polygon validation or derivation for postcode points against both boundary sets.
4. Calculate bidirectional postcode-count shares.
5. Apply shares to an additive variable table keyed by the selected source geography.

This brings the core GIS risk forward instead of hiding it behind a CSV-only prototype.

## Questions to resolve with user

- Should user-uploaded data include the variable on LSOA11 or LSOA21?
- Should the app ship with known ONS lookup downloads, or only accept user-uploaded files?
- Is browser-only processing required?
- Which household/residential count source can be used after postcode-count weighting?
