# Contributing — rules for humans *and* agents

> Canonical, tool-agnostic statement of repo rules, referenced from `AGENTS.md`.
> Keep it short.

## Setup (once per clone)
```bash
git init                          # if not already a repo
scripts/install-hooks.sh          # enable the committed pre-commit gate
```
`install-hooks.sh` sets `core.hooksPath` to `scripts/hooks/`, so the hooks in
this repo are used directly (no copying, works on every clone).

## The pre-commit gate
Every `git commit` runs `scripts/hooks/pre-commit`, which does:
1. **doc-lint** (`scripts/doc_lint.py`) — wiki frontmatter, wikilink resolution,
   ADR numbering, index completeness.
2. **secret scan** (`scripts/secret_scan.py`) — blocks likely credentials/keys.
3. **review report** (`scripts/review.py`) — if `REVIEW.md` exists, reports open
   human-review comments and schema/anchor warnings. This is informational by
   default and does not block commits while a document is under review.

Fix failures, then commit again. This gate is the *mechanical* enforcement of
the rules in AGENTS.md — a rule that can't be enforced mechanically will be broken.

## Human review loop for documents
Papers/research projects include `REVIEW.md` as the durable human→agent feedback
channel. A human reviews the rendered document, records anchored comments there,
and the agent works open comments before other writing/synthesis work. The doc is
**review-clean** when `scripts/review.py . --check` returns 0.

## Non-negotiables
- **Do not use `git commit --no-verify`.** The gate exists to catch real problems;
  bypassing it (human *or* agent) is how secrets and broken docs ship.
- **No secrets in the repo.** Use a gitignored `.env`; the secret scan blocks keys.
- **Docs are load-bearing.** Change structure → update `architecture.md`; decide
  something → add an ADR in `docs/adrs/`; learn something → file it in `/home/kd/NAS_Hermes/wiki/`;
  keep `PROJECT_STATE.md` and `tasks.md` current.
- **Check before deciding.** Read `docs/adrs/` before any architectural choice.

## Enforcement note (git-only by design)
This repo enforces via **git hooks only** — there is intentionally no CI/server
backstop. Consequence: `--no-verify`, or a fresh clone before
`install-hooks.sh`, can skip the gate — so the non-negotiables above are the real
contract. If this project moves to a shared remote, add a CI mirror of the
same checks.
