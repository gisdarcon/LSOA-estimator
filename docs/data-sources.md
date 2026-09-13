# Data Sources — LSOA11 to LSOA21 Estimator

Last updated: 2026-09-13

## Purpose

Document the official data sources used to derive and verify the static LSOA 2011 ↔ LSOA 2021 estimator.

## Geographic scope

The estimator is scoped to **England**.

- Country filter: `ctry = E92000001`.
- LSOA 2011 codes: `E01...`, 32,844 areas.
- LSOA 2021 codes: `E01...`, 33,755 areas.
- Wales, Scotland, and Northern Ireland are excluded from the current app.

## Crosswalk relationship authority

The valid relationship set comes from:

- **LSOA (2011) to LSOA (2021) to Local Authority District (2022) Exact Fit Lookup for EW (V3)**
- ONS Open Geography Portal: <https://geoportal.statistics.gov.uk/datasets/ons::lsoa-2011-to-lsoa-2021-to-local-authority-district-2022-exact-fit-lookup-for-ew-v3/about>

This lookup defines the official LSOA11→LSOA21 relationships used by the app. It is used as the authority for relationship membership; the app does not invent target codes.

## Weighting evidence

Weights are derived from two NSPL August 2024 releases joined by normalised postcode:

1. **National Statistics Postcode Lookup - 2011 Census (August 2024) for the UK**
   - ONS Open Geography Portal: <https://geoportal.statistics.gov.uk/datasets/c5afedb9204a47e99559a4880feddcb1/about>
   - Used for LSOA 2011 membership.
2. **National Statistics Postcode Lookup - 2021 Census (August 2024) for the UK**
   - ONS Open Geography Portal: <https://geoportal.statistics.gov.uk/datasets/73ce619853044aaaa6f7fa5b90765b85/about>
   - Used for LSOA 2021 membership.

### Filters

Only active residential England postcode records are used:

| Field | Required value | Reason |
|---|---|---|
| `ctry` | `E92000001` | England-only scope |
| `doterm` | empty | active postcodes only |
| `usertype` | `0` | small-user/residential weighting proxy |

### Weight formula

Forward `2011 → 2021` weight:

```text
share(lsoa11,lsoa21) = postcode_count(lsoa11,lsoa21) / sum(postcode_count(lsoa11,*))
```

Reverse `2021 → 2011` weight:

```text
reverseShare(lsoa21,lsoa11) = postcode_count(lsoa11,lsoa21) / sum(postcode_count(*,lsoa21))
```

The exported column is named `weight` in both directions.

## Current crosswalk asset

Bundled file:

```text
src/assets/data/lsoa11-to-lsoa21-crosswalk.json
```

Verified coverage:

- 33,856 official exact-fit relationship rows.
- 32,844 LSOA 2011 source areas.
- 33,755 LSOA 2021 target areas.
- 1,415,849 active residential England postcode records used.
- Forward weights sum to 1 within each LSOA 2011 to stored-decimal rounding tolerance.
- Reverse weights sum to 1 within each LSOA 2021.

## Boundary map sources

The map uses real ONS **Generalised Clipped polygon boundaries**. It does not use point or centroid replacements.

| Direction | Polygons shown | Bundled asset | Source |
|---|---|---|---|
| `2011 → 2021` | changed LSOA 2021 target/output polygons | `src/assets/data/changed-lsoa21-polygons.json` | Lower Layer Super Output Areas (December 2021) Boundaries EW BGC V5 |
| `2021 → 2011` | changed LSOA 2011 target/output polygons | `src/assets/data/changed-lsoa11-polygons.json` | Lower Layer Super Output Areas (December 2011) Boundaries EW BGC V3 |

Source references:

- **Lower Layer Super Output Areas (December 2011) Boundaries EW BGC (V3)**: <https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2011-boundaries-ew-bgc-v3/about>
- **Lower Layer Super Output Areas (December 2021) Boundaries Generalised Clipped EW BGC**: <https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-generalised-clipped-ew-bgc/about>

Verified bundled map coverage:

- Forward map: 1,945 changed LSOA21 codes and 1,945 polygon features; no missing changed codes.
- Reverse map: 1,034 changed LSOA11 codes and 1,034 polygon features; no missing changed codes.

## Limitations

- Postcode count is a proxy, not a direct household or population count.
- Direct apportionment is appropriate for additive variables only.
- Browser upload processing uses a precomputed static crosswalk; the full postcode-level precompute is run offline when the source data or method changes.
- Full all-LSOA national boundary rendering is avoided for performance; the app maps changed polygons only.
