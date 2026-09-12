# Data Sources Investigation — LSOA11 to LSOA21 Estimator

Last updated: 2026-09-12

## Purpose

Track candidate data sources for deriving or validating shares between LSOA11 and LSOA21. This is investigation material, not yet an architectural decision.

## User requirement

The app should allow users to load LSOA11 boundaries and LSOA21 boundaries, and use an NSPL lookup table to identify shares between boundary changes for a variable such as 2021 estimated population.

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

Use NSPL/ONSPD records as evidence. Count or weight postcodes by source-target LSOA pairs, then calculate shares.

Pros:
- aligns with user’s requested NSPL-based approach
- can produce proportional shares if suitable weights exist
- transparent and reproducible

Cons:
- postcode count is not population count
- terminated/current postcode handling matters
- needs verified old and new LSOA fields

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

Start with a simple CSV-based prototype before full boundary rendering:

1. Accept a prepared crosswalk table with `LSOA11CD`, `LSOA21CD`, and `weight`.
2. Calculate source-to-target shares.
3. Apply shares to an additive variable table keyed by `LSOA11CD`.
4. Add boundary display only after the crosswalk/estimation math is agreed.

This keeps the first investigation focused on method correctness rather than shapefile parsing complexity.

## Questions to resolve with user

- Is postcode count acceptable as a first weight, or must weights represent population/households/addresses?
- Is the first direction LSOA11 → LSOA21 only?
- Should user-uploaded data include the variable on LSOA11 or LSOA21?
- Should the app ship with known ONS lookup downloads, or only accept user-uploaded files?
- Is browser-only processing required?
