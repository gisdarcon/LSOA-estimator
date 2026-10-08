# LSOA 2011 ↔ LSOA 2021 Estimator

A static browser app for estimating additive variables between England LSOA 2011 and LSOA 2021 geographies.

The app is designed for GitHub Pages. Users upload a simple CSV containing LSOA codes and one numeric additive variable, such as population. The app auto-detects the input geography, applies official relationship-level fractional weights, reports conservation checks, displays changed-boundary polygons, and exports a detailed audit CSV.

Created by Hermes Agent (GPT 5.5) & **Konstantinos Daras** — Konstantinos.Daras@liverpool.ac.uk

## Live app

When published with GitHub Pages, the app will be available at:

```text
https://<github-user-or-org>.github.io/<repository-name>/
```

For local preview:

```bash
npm install
npm run check
npm run build
npm run preview
```

## What the app does

1. Upload a CSV with an LSOA code column and one numeric additive variable.
2. The app auto-detects direction:
   - `lsoa2011` / LSOA 2011 codes → `2011 → 2021`
   - `lsoa2021` / LSOA 2021 codes → `2021 → 2011`
3. Run the national estimation.
4. Review:
   - input and estimated totals;
   - conservation check;
   - input-side splits and output-side merges;
   - changed-boundary polygon map;
   - sample relationship-level output rows.
5. Export a detailed CSV.

## Input CSV format

Example 2011 input:

```csv
lsoa2011,pop
E01000001,1980
E01000010,3585
```

Example 2021 input:

```csv
lsoa2021,pop
E01000001,2012
E01034473,1634
```

The variable must be additive, for example population, household counts, case counts, or totals. Do not directly estimate rates, percentages, medians, ranks, or indices unless they are first converted to additive numerator/denominator components.

## Output CSV format

The exported file name follows:

```text
<Direction>_<Variable name>.csv
```

Examples:

```text
LSOA2011toLSOA2021_Pop.csv
LSOA2021toLSOA2011_Pop.csv
```

The CSV is relationship-level and uses the uploaded variable name:

```csv
lsoa2011,lsoa2021,weight,pop
E01000010,E01034473,0.4557,1633.67
E01000010,E01034474,0.5443,1951.33
```

## Method summary

The estimator uses a precomputed static crosswalk bundled into the site.

- Relationship authority: **ONS LSOA (2011) to LSOA (2021) Exact Fit Lookup for EW V3**.
- Weight evidence: **NSPL 2011 Census August 2024** joined to **NSPL 2021 Census August 2024** by normalised postcode.
- Postcode filter: active residential England postcodes only:
  - `ctry = E92000001`
  - empty `doterm`
  - `usertype = 0`
- Forward weights are normalised within each 2011 LSOA.
- Reverse weights are normalised within each 2021 LSOA.
- The app preserves the official ONS LSOA codes exactly.

The browser app does not run national point-in-polygon processing at upload time. The heavy data preparation is precomputed and stored as static JSON so the published GitHub Pages app can run fully client-side.

## Current crosswalk coverage

| Measure | Count |
|---|---:|
| LSOA 2011 areas | 32,844 |
| LSOA 2021 areas | 33,755 |
| Exact-fit relationship rows | 33,856 |
| Active residential England postcode records used | 1,415,849 |

### Split and merge relationships

| View | Count |
|---|---:|
| 2011 LSOAs split across 2+ 2021 LSOAs | 838 |
| 2011 LSOAs split across 3+ 2021 LSOAs | 130 |
| 2021 LSOAs made from 2+ 2011 LSOAs | 101 |
| 2021 LSOAs made from 3+ 2011 LSOAs | 0 |

## Boundary map

The map uses real ONS **Generalised Clipped polygon boundaries**, not points or centroids.

| Direction | Changed polygons shown | Bundled feature count | Source |
|---|---|---:|---|
| `2011 → 2021` | LSOA 2021 target/output polygons | 1,945 | Lower Layer Super Output Areas December 2021 Boundaries EW BGC V5 |
| `2021 → 2011` | LSOA 2011 target/output polygons | 1,034 | Lower Layer Super Output Areas December 2011 Boundaries EW BGC V3 |

Only changed polygons are mapped by default. This keeps the static browser app responsive while preserving the agreed polygon representation.

## Official data sources

- [LSOA (2011) to LSOA (2021) to Local Authority District (2022) Exact Fit Lookup for EW V3](https://geoportal.statistics.gov.uk/datasets/ons::lsoa-2011-to-lsoa-2021-to-local-authority-district-2022-exact-fit-lookup-for-ew-v3/about)
- [National Statistics Postcode Lookup - 2011 Census (August 2024) for the UK](https://geoportal.statistics.gov.uk/datasets/c5afedb9204a47e99559a4880feddcb1/about)
- [National Statistics Postcode Lookup - 2021 Census (August 2024) for the UK](https://geoportal.statistics.gov.uk/datasets/73ce619853044aaaa6f7fa5b90765b85/about)
- [Lower Layer Super Output Areas December 2011 Boundaries EW BGC V3](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2011-boundaries-ew-bgc-v3/about)
- [Lower Layer Super Output Areas December 2021 Boundaries Generalised Clipped EW BGC](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-generalised-clipped-ew-bgc/about)

## Technology

- Vite
- Svelte
- TypeScript
- Tailwind CSS
- Leaflet
- Static JSON data assets
- GitHub Pages deployment workflow

## Development

This project is developed as a static client-side app.

```bash
npm install
npm run check
npm run build
npm run preview
```

Local preview is usually served at:

```text
http://localhost:4173/
```

## Publishing to GitHub Pages

This repository includes a GitHub Actions workflow at:

```text
.github/workflows/deploy.yml
```

The workflow builds the app and publishes `dist/` to the `gh-pages` branch when changes are pushed to `main`.

Before publishing as a project page, set the Vite base path in `vite.config.ts`:

```ts
export default defineConfig({
  plugins: [svelte()],
  base: '/<repository-name>/',
})
```

Then:

1. Push `main` to GitHub.
2. In GitHub, enable Actions workflow write permission:
   - Repository → Settings → Actions → General → Workflow permissions → Read and write permissions.
3. In GitHub Pages settings, choose:
   - Source: Deploy from a branch
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. Wait for the deploy workflow to complete.

## Licence and attribution

Source datasets are from the ONS Open Geography Portal and associated ONS geography products. OpenStreetMap tiles are used for the basemap with attribution retained in the map UI.
