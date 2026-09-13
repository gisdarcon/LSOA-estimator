# LSOA 2011 ↔ LSOA 2021 Estimator

Static Svelte/TypeScript web app for estimating additive variables, especially counts such as population, between England LSOA 2011 and LSOA 2021 boundaries.

The app is designed for GitHub Pages: users upload only a variable CSV; the official crosswalk, weights, and changed-boundary map layers are bundled as static assets.

## Current workflow

1. Upload a CSV with an LSOA code column and a numeric variable column, for example `lsoa2011,pop` or `lsoa2021,pop`.
2. The app auto-detects the direction:
   - `lsoa2011` / LSOA 2011 codes → `2011 → 2021`
   - `lsoa2021` / LSOA 2021 codes → `2021 → 2011`
3. Run national apportionment.
4. Review conservation totals, changed-boundary map, split statistics, and sample output rows.
5. Export detailed relationship-level CSV:

```csv
lsoa2011,lsoa2021,weight,pop
E01000010,E01034473,0.4557,1633.67
E01000010,E01034474,0.5443,1951.33
```

## Method summary

- Relationship authority: **ONS LSOA 2011 to LSOA 2021 Exact Fit Lookup V3**.
- Weight evidence: **NSPL 2011 Census August 2024** joined to **NSPL 2021 Census August 2024** by normalised postcode.
- Filter: active residential England postcodes only: `ctry = E92000001`, empty `doterm`, `usertype = 0`.
- Forward weights sum within each 2011 LSOA.
- Reverse weights sum within each 2021 LSOA.
- Direct use is for additive variables only; rates/percentages need numerator/denominator treatment first.

## Boundary map

The map uses real ONS **Generalised Clipped polygon boundaries**, not points.

| Direction | Changed polygons shown | Bundled feature count | Source |
|---|---:|---:|---|
| `2011 → 2021` | LSOA 2021 target/output polygons | 1,945 | Lower Layer Super Output Areas (December 2021) Boundaries EW BGC V5 |
| `2021 → 2011` | LSOA 2011 target/output polygons | 1,034 | Lower Layer Super Output Areas (December 2011) Boundaries EW BGC V3 |

The app intentionally maps only changed polygons, not every LSOA polygon, to keep the static browser UI responsive while preserving polygon geometry.

## Development

Local development mirror:

```bash
cd /home/kd/projects/lsoa-estimator
npm install
npm run check
npm run build
npx vite preview --host 0.0.0.0 --port 4173 --strictPort
```

Project/tracking repository:

```text
/home/kd/NAS_Hermes/work/lsoa11-to-lsoa21-estimator
```

Current preview URL:

```text
http://localhost:4173/
```
