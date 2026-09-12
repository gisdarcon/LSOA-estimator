# LSOA11 to LSOA21 Estimator

Web application for estimating variables from 2011 Lower Layer Super Output Areas (LSOA11) onto 2021 Lower Layer Super Output Areas (LSOA21), using boundary files and postcode/lookup evidence to estimate shares where geographies changed.

## Working idea

A user loads:

- LSOA11 boundaries, ideally shapefile/zip or GeoJSON
- LSOA21 boundaries, ideally shapefile/zip or GeoJSON
- an NSPL/ONSPD-style postcode lookup table containing postcode-to-geography fields
- a variable attached to LSOA11 or LSOA21, for example 2021 estimated population

The app calculates or previews a crosswalk between LSOA11 and LSOA21 and applies shares to estimate the variable on the target geography.

## Early method hypothesis

1. Use postcode lookup records as weighted evidence for correspondence between LSOA11 and LSOA21.
2. Group records by source and target LSOA pair.
3. Estimate shares using a selected weighting field:
   - postcode count as a first pass
   - population/household/address count if available or provided
   - optional externally supplied variable weights
4. Join shares to the uploaded variable table and aggregate to the target geography.
5. Map and export the resulting estimates plus diagnostics.

## Key research questions

- Which lookup table should be canonical: NSPL, ONSPD, or ONS-published LSOA11-to-LSOA21 best-fit/exact-fit lookup?
- Do we need exact spatial overlay of shapefiles, or is lookup-table weighting good enough for the first MVP?
- Should variables be transformed LSOA11 → LSOA21, LSOA21 → LSOA11, or both?
- What weight should define “share”: postcodes, residential delivery points, population, households, or user-provided weights?
- What file formats should the first version support in-browser?

## Layout

- `src/` — frontend source
- `tests/` — component / e2e tests
- `docs/` — design notes, ADRs, runbooks
- `assets/` — static assets
- `/home/kd/NAS_Hermes/wiki/` — shared knowledge base

## Setup

```bash
npm install
```

## Run

```bash
npm run dev
npm test
npm run build
npm run preview
```
