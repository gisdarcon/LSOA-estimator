# Architecture Decision Records

> Durable, numbered, supersedable records of **why** the project is shaped the
> way it is. This is the "why" layer — complementary to `PLAN.md` (what we're
> doing), `/home/kd/NAS_Hermes/wiki/` (what we know), and `architecture.md` (how it's built now).

## Rules
- **Check before you decide.** Before any architectural choice (framework,
  database, protocol, deployment pattern, major dependency), read this folder
  for an existing decision. Do **not** silently contradict an accepted ADR.
- **One decision per file.** File name: `NNNN-kebab-title.md` (4-digit, zero-padded,
  sequential from the highest existing number).
- **Immutable once accepted.** A superseded ADR is never edited or deleted — it
  is marked `Superseded by: NNNN` in its Status and a new ADR records the change.
- **Review agent-drafted ADRs.** If an agent generates an ADR from a codebase
  scan, verify the Context and Consequences against actual intent — agents can
  capture the *what* but fabricate the *why*.

## Status values
`Proposed` → `Accepted` → (`Superseded by: NNNN` | `Deprecated`)

## Index
| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-adopt-adr-catalogue.md) | Adopt an ADR catalogue | Accepted |
| [0002](0002-bidirectional-gis-first-method.md) | Bidirectional GIS-first method with postcode-count starting weights | Accepted |
| [0003](0003-static-github-pages-deployment.md) | Static GitHub Pages deployment | Accepted |

Create a new record by copying [TEMPLATE.md](TEMPLATE.md) to the next number.
