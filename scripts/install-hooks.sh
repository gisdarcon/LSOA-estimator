#!/usr/bin/env bash
# Point this repo's git at scripts/hooks/ so the committed hooks are used directly.
# Run once per clone:  scripts/install-hooks.sh
# Git-only by design (no CI / GitHub Actions) — see CONTRIBUTING.md.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
git config core.hooksPath "$ROOT/scripts/hooks"
echo "✓ git hooks enabled: core.hooksPath = $ROOT/scripts/hooks"
echo "  The committed hooks in scripts/hooks/ are now used directly (no copying)."
