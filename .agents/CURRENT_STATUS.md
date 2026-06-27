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

Keep the Phase 0-3 executable validation slice complete while applying the `.tmp/cr.md` review fixes.

## Last Completed Work

- Added OKF frontmatter to `AGENTS.md` and `CLAUDE.md`.
- Updated root `index.md` to link to `.agents/CURRENT_STATUS.md`, `.agents/EVIDENCE.md`, and `.agents/OPEN_QUESTIONS.md`.
- Removed all obsolete handoff-file references.
- Added `uv`-portable Python package metadata, CLI, inventory helpers, schema-profile validation, schemas, tests, `justfile`, and `uv.lock`.
- Tightened schema contracts, registry validation, OKF link handling, portable root discovery, and the `doctor` runtime probe per `.tmp/cr.md`.
- Validated the current RealityGapBench corpus and review fixes without rewriting existing corpus artifacts.

## Current Repo State

Phases 0 through 3 of `.agents/plans/full-cep.md` are complete. The `cep` CLI supports `doctor` and `validate` commands. `cep doctor` now runs a schema registry probe. `cep validate all` validates registered schemas, RealityGapBench case artifacts, answer keys, examples, evidence files, anti-collapse manifest, and anti-collapse fixtures.

## Next Affordable Move

Implement Phase 4: RealityGapBench scoring against existing `answer_key.json` files and example answers.

## Why This Next Move Matters

The corpus now validates structurally. Scoring is the next executable proof that CEP can distinguish correct answers, partial answers, invalid answers, and anti-collapse failures without changing the benchmark corpus.

## Validation / Evidence

See `.agents/EVIDENCE.md` entries `EV-OKF-REPAIR` and `EV-CR-REVIEW-FIXES`.

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
- `.agents/plans/full-cep.md`
- `.agents/EVIDENCE.md`
- `.agents/DEBT.md`

## Cautions for Next Agent

- Preserve current RealityGapBench corpus shapes; schemas intentionally reflect fields like `case_ref` and `evidence_id`.
- `uv` is the expected command runner for portability.
- `.tmp/cr.md` has all verified review prompts struck through after implementation.
