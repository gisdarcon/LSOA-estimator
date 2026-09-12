---
id: 0004
title: Static client library stack
status: Accepted
date: 2026-09-12
deciders: User, Hermes Agent
tags: [architecture, frontend, gis, static-site]
---

# ADR 0004 — Static client library stack

## Context

The app must be static, GitHub Pages-compatible, and must use the client's browser processing resources for difficult computations. The user also requested that library options be presented before adoption.

The first library selection prompt offered options for the static app framework, GIS analysis library, and shapefile loading. The user selected:

- Vite + TypeScript + Svelte for the static app framework.
- Turf.js for point-in-polygon and GeoJSON operations.
- `shpjs` for browser ZIP shapefile to GeoJSON parsing.

## Decision

Use Vite + TypeScript + Svelte as the static client app stack, Turf.js as the first GIS analysis library, and `shpjs` as the first shapefile parser.

The implementation must run computationally heavy work on client resources. Expensive parsing and GIS steps should run in Web Workers where practical, with progress reporting and cancellable/defensive UX for large files.

## Consequences

- Build output must remain static and GitHub Pages-safe.
- Svelte components should handle UI/state; heavy GIS computation should be isolated from the UI thread.
- Turf.js is the first choice for point-in-polygon and GeoJSON operations; if it cannot handle later polygon overlay requirements, present alternatives before adding another GIS library.
- `shpjs` is the first choice for zipped shapefile uploads; if it fails on target ONS shapefiles or projection/encoding cases, present alternatives before switching.
- TypeScript types and worker message contracts should be explicit because data objects can be large and expensive to copy.

## Alternatives considered

- **Vite + TypeScript + React** — viable, but not selected.
- **Vanilla TypeScript with Vite** — simpler dependency surface, but not selected.
- **OpenLayers** — strong map-first GIS library, but not selected as the first analysis library.
- **Leaflet + Turf.js** — possible for map UI later, but not selected as the first GIS analysis choice.
- **GeoJSON-only first upload** — rejected because the user selected direct zipped shapefile support through `shpjs`.
- **Testing two shapefile parsers before deciding** — reasonable, but not selected for the first implementation path.
