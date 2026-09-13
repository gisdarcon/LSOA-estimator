---
id: 0005
title: Official Exact Fit + NSPL static crosswalk and ONS polygon map assets
status: Accepted
date: 2026-09-13
deciders: User, Hermes Agent
tags: [architecture, data, gis, static-site]
---

# ADR 0005 — Official Exact Fit + NSPL static crosswalk and ONS polygon map assets

## Context

The app must be static and GitHub Pages-compatible, but the national LSOA 2011 ↔ LSOA 2021 method needs official relationship coverage, proportional weights, and map evidence of changed boundary areas.

Earlier mock data produced synthetic 50/50 weights and fake-looking outputs, which was not acceptable. The user required the ONS lookup for exact fit relationships and NSPL postcode evidence for non-uniform shares. The user also clarified that the map must use polygon boundaries, not point or centroid substitutes.

## Decision

Use the **ONS LSOA 2011 to LSOA 2021 Exact Fit Lookup V3** as the relationship authority.

Build and bundle a static crosswalk from:

- Exact Fit Lookup V3 relationship rows;
- NSPL 2011 Census August 2024;
- NSPL 2021 Census August 2024;
- active residential England postcode filter: `ctry = E92000001`, empty `doterm`, `usertype = 0`.

The app bundles the resulting crosswalk with:

- `share` for `2011 → 2021`, normalised within each LSOA 2011;
- `reverseShare` for `2021 → 2011`, normalised within each LSOA 2021.

For map QA, bundle direction-specific changed-boundary polygon assets using ONS Generalised Clipped boundaries:

- `2011 → 2021`: changed LSOA 2021 target/output polygons from LSOA 2021 Boundaries EW BGC V5;
- `2021 → 2011`: changed LSOA 2011 target/output polygons from LSOA 2011 Boundaries EW BGC V3.

## Consequences

- Users only upload a variable CSV; they do not need to upload boundaries or lookup files for the standard workflow.
- The app stays static and reproducible.
- The app avoids browser-heavy full postcode point-in-polygon processing at upload time.
- The map preserves polygon representation while avoiding all-LSOA national polygon rendering; it loads only changed polygons for the selected direction.
- The production JavaScript bundle is large while polygon JSON is statically imported. Lazy-loading these assets is a future optimization.

## Verification expectations

Before release or commit:

- `npm run check` passes.
- `npm run build` passes.
- Crosswalk coverage is verified against expected counts: 33,856 rows, 32,844 LSOA11 areas, 33,755 LSOA21 areas.
- Changed code sets match polygon features:
  - 1,945 changed LSOA21 target codes/features;
  - 1,034 changed LSOA11 target/output codes/features.
- Browser verification confirms both directions render polygon SVG paths and conservation checks pass.

## Alternatives considered

- **Mock crosswalk / synthetic splits** — rejected; not official and produced misleading 50/50 or fake-code behavior.
- **Live full point-in-polygon in browser** — rejected for the standard workflow because postcode-level national precompute is too heavy for a static app runtime.
- **All national LSOA polygons on the map** — rejected for default UI because it made the map slow or invisible.
- **Point/centroid changed-boundary layer** — rejected because it changes the agreed map representation; user approval is required before such a fallback.
