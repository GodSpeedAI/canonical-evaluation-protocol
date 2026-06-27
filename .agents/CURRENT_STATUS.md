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

Expand the executable benchmark corpus breadth, starting with additional reviewed RealityGapBench cases across the declared gap types.

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
- Added AuthorityBench, SettlementBench, and CapabilityBench benchmark definitions, smoke cases, valid/invalid answers, typed scorers, tests, and CLI corpus runners.
- Extended `just all` smoke coverage to run RealityGapBench, AuthorityBench, SettlementBench, and CapabilityBench corpora.
- Validated the new slices with phase-specific tests, direct CLI runs, full pytest, basedpyright, focused Ruff, and `just all`.
- Added a standard `dev` optional extra to `pyproject.toml` so the Phase 11 `python -m pip install -e ".[dev]"` command installs cleanly.
- Completed Phase 11 end-to-end verification with the explicit command sequence, report inspection, and aggregate `just all` proof command.

## Current Repo State

Phases 0 through 11 of `.agents/plans/full-cep.md` are complete and the `.tmp/cr.md` review pass is complete. The `cep` CLI supports `doctor`, `validate`, `conformance anti-collapse`, `run reality-gap`, `run reality-gap-corpus`, `run authority-corpus`, `run settlement-corpus`, and `run capability-corpus`. `just all` validates OKF docs, schemas, the current RealityGapBench corpus, anti-collapse conformance, tests, and smoke report generation for all four executable benchmark families. Phase 11 confirmed generated JSON reports for RealityGapBench, AuthorityBench, SettlementBench, and CapabilityBench.

## Next Affordable Move

Expand the executable benchmark corpus breadth, starting with additional reviewed RealityGapBench cases across the declared gap types.

## Why This Next Move Matters

The repo now has end-to-end local executable proof. More reviewed cases will reduce overfitting risk and test whether the current schemas and scorers preserve CEP distinctions beyond the smoke corpus.

## Validation / Evidence

See `.agents/EVIDENCE.md` entries `EV-OKF-REPAIR`, `EV-CR-REVIEW-FIXES`, `EV-REALITY-GAP-PROOF`, `EV-CR-PHASE4-7-REVIEW`, `EV-MULTI-BENCH-PHASE8-10`, and `EV-END-TO-END-PHASE11`.

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
- `.gitignore`
- `benchmarks/authority/`
- `benchmarks/settlement/`
- `benchmarks/capability/`
- `src/cep/benchmarks/authority.py`
- `src/cep/benchmarks/settlement.py`
- `src/cep/benchmarks/capability.py`
- `src/cep/cli.py`
- `src/cep/inventory.py`
- `src/cep/paths.py`
- `tests/test_authority_bench.py`
- `tests/test_settlement_bench.py`
- `tests/test_capability_bench.py`

## Cautions for Next Agent

- Preserve current RealityGapBench corpus shapes; schemas intentionally reflect fields like `case_ref` and `evidence_id`.
- `uv` is the expected command runner for portability.
- `.tmp/cr.md` has all verified review prompts struck through after implementation.
- Generated reports are ignored via `reports/`; rerun `just all` to regenerate current benchmark reports.
- `uv run ruff check .` still reports pre-existing lint debt in `tools/validate_okf.py`; touched code passes `uv run ruff check src tests`.
- Do not convert the Phase 11 local proof into a production-readiness claim; the plan still lists full dataset breadth, formal conformance classes, Semantic Envelope execution, external model evaluation, docs site, release process, and production claims as future work.
