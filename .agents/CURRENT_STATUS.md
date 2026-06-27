---
type: "CEP Guide"
id: "cep-agent-state"
title: "Agent State"
description: "Agent state and completion checklist for the Canonical Evaluation Protocol."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - agent
  - metadata
timestamp: "2026-06-27T00:00:00Z"
---

# Agent State

## Last Updated

2026-06-27 — Codex

## Current Outcome Being Pursued

Complete the `.tmp/cr.md` review pass for the RealityGapBench executable proof and preserve a pushed handoff.

## Last Completed Work

- Added OKF frontmatter to `AGENTS.md` and `CLAUDE.md`.
- Updated root `index.md` to link to `.agents/CURRENT_STATUS.md`, `.agents/EVIDENCE.md`, and `.agents/OPEN_QUESTIONS.md`.
- Removed all obsolete handoff-file references.
- Added `uv`-portable Python package metadata, CLI, inventory helpers, schema-profile validation, schemas, tests, `justfile`, and `uv.lock`.
- Tightened schema contracts, registry validation, OKF link handling, portable root discovery, and the `doctor` runtime probe per `.tmp/cr.md`.
- Validated the current RealityGapBench corpus and review fixes without rewriting existing corpus artifacts.
- Added RealityGapBench scoring, anti-collapse conformance, JSON report generation, CLI run commands, `just all`, and CI.
- Ran phase-specific tests and the full local proof command.
- Verified all 18 `.tmp/cr.md` review prompts against current code, fixed the remaining schema-validation gaps, and struck completed review text.

## Current Repo State

Phases 0 through 7 of `.agents/plans/full-cep.md` are complete and the `.tmp/cr.md` review pass is complete. The `cep` CLI supports `doctor`, `validate`, `conformance anti-collapse`, `run reality-gap`, and `run reality-gap-corpus`. `just all` validates OKF docs, schemas, the current RealityGapBench corpus, anti-collapse conformance, tests, and smoke report generation.

## Next Affordable Move

Implement Phase 8: AuthorityBench bootstrap and executable false-allow slice.

## Why This Next Move Matters

RealityGapBench now has local executable proof. AuthorityBench is the next benchmark family in the plan and extends CEP proof from reality gaps into pre-action authority preservation.

## Validation / Evidence

See `.agents/EVIDENCE.md` entries `EV-OKF-REPAIR`, `EV-CR-REVIEW-FIXES`, `EV-REALITY-GAP-PROOF`, and `EV-CR-PHASE4-7-REVIEW`.

## Files Recently Modified

- `AGENTS.md`
- `CLAUDE.md`
- `index.md`
- `tools/validate_okf.py`
- `.tmp/cr.md`
- `pyproject.toml`
- `uv.lock`
- `justfile`
- `src/cep/`
- `schemas/`
- `tests/`
- `.github/workflows/ci.yml`
- `README.md`
- `.agents/plans/full-cep.md`
- `.agents/EVIDENCE.md`
- `.agents/DEBT.md`

## Cautions for Next Agent

- Preserve current RealityGapBench corpus shapes; schemas intentionally reflect fields like `case_ref` and `evidence_id`.
- `uv` is the expected command runner for portability.
- `.tmp/cr.md` has all verified review prompts struck through after implementation.
- Generated reports are ignored via `reports/`; rerun `uv run cep run reality-gap-corpus` or `just all` to regenerate them.
