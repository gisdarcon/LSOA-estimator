---
id: 0001
title: Adopt an ADR catalogue
status: Accepted
date: 2026-09-09
deciders: project owner
tags: [meta, decision]
---

# ADR 0001 — Adopt an ADR catalogue

## Context
This project is built with AI agents. Agents scaffold systems quickly, but the
rationale for architectural choices tends to get buried in code with no durable
record. Without a "why" trail, both humans and future agents risk contradicting
earlier decisions or re-litigating them.

## Decision
Maintain a numbered, immutable catalogue of Architecture Decision Records in
`docs/adrs/`. Before making any non-trivial architectural choice, check this
catalogue; record the choice and its rationale here; supersede rather than edit
when a decision changes.

## Consequences
- Adds one file per major decision — small, durable cost.
- Agents must read `docs/adrs/` before architectural changes (enforced via
  AGENTS.md guardrails).
- The "why" survives across sessions, machines, and tools because it is
  version-controlled in the repo.

## Alternatives considered
- **Inline comments / PLAN.md section only** — lost in prose, not searchable,
  no supersession discipline. Rejected.
