---
id: 0003
title: Static GitHub Pages deployment
status: Accepted
date: 2026-09-12
deciders: User, Hermes Agent
tags: [architecture, deployment, static-site]
---

# ADR 0003 — Static GitHub Pages deployment

## Context

The user confirmed that the web app must be static and able to be served by GitHub Pages. This constrains the architecture: the production application cannot require a server process, database, server-side upload handling, or private backend job queue.

The app still needs GIS functionality: uploaded LSOA boundaries, postcode lookup data, point-in-polygon checks, spatial diagnostics, bidirectional share calculation, and export. Therefore these operations must run in the browser, using the client machine's processing resources. Web Workers should be used for heavy parsing and spatial analysis so the UI remains responsive.

GitHub Pages also affects build and routing choices. The app should produce static assets that work under a repository subpath, not only at the domain root. Runtime access to user files should use the browser File API; optional sample data can be bundled or fetched as static files if licensing and file size allow.

## Decision

Build and deploy the app as a static client-side web application compatible with GitHub Pages. All core v1 processing must run in the browser using static JavaScript assets, browser file uploads, and client-side exports. Do not introduce a required backend for v1.

Use static-site-compatible tooling and design choices:

- build output is static HTML/CSS/JS suitable for GitHub Pages;
- route handling must work on a GitHub Pages subpath, using hash routing or correctly configured relative base paths;
- GIS parsing, point-in-polygon, and other difficult computations should run client-side using browser/client processing resources, with Web Workers for large datasets;
- no server-only APIs, server-side secrets, database writes, or backend upload storage;
- optional static sample datasets must be license-checked and size-conscious.

## Consequences

- Browser memory and CPU limits become first-class constraints for boundary and postcode lookup processing because the client machine performs the difficult computations.
- The implementation should prefer libraries that work in browser bundles and avoid Node-only geospatial dependencies.
- Large-file UX must include progress indicators, warnings, and failure modes rather than relying on a backend rescue path.
- If a future backend-assisted mode becomes necessary, it must be optional and recorded in a new ADR; it cannot be required for the GitHub Pages version.
- Data privacy is improved because user-uploaded files can remain local in the browser, but this must be stated clearly in the UX and method documentation.

## Alternatives considered

- **Backend-assisted processing** — rejected for v1 because the user requires GitHub Pages/static hosting. May be revisited only as an optional future mode.
- **Desktop/server GIS pipeline** — rejected for the app target because it would not be a GitHub Pages-compatible web app.
- **Static UI with remote API processing** — rejected for v1 because it would still require operating a backend and handling uploaded data outside the user's browser.
