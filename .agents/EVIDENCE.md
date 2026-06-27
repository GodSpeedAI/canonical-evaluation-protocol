---
type: "CEP Guide"
id: "cep-evidence"
title: "Evidence"
description: "Execution evidence records for the Canonical Evaluation Protocol development."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - evidence
  - audit
timestamp: "2026-06-26T14:13:47Z"
---

# Evidence

## Bootstrap Execution

- **JSON Source File Used**: `ChatGPT-AgentWorld-benchmarks.json`
- **Number of Messages Parsed**: 106
- **Newest Message Timestamp**: 6/26/2026, 8:35:48 AM
- **Oldest Message Timestamp**: 6/25/2026, 7:17:36 AM

### Artifacts Extracted
- specs/CEP-0000 through CEP-0010
- RealityGapBench specification
- RealityGapBench Case Packs (rg-0001, rg-0002, rg-0003)
- Conformance Fixtures (manifest.json and 10 JSON files)

### Files Created
- `.agents/CURRENT_STATUS.md`
- `.agents/DECISIONS.md`
- `.agents/OPEN_QUESTIONS.md`
- `.agents/PLAN.md`
- Root project documents: `CONTRIBUTING.md`, `GOVERNANCE.md`, `LICENSE`, `OPEN_QUESTIONS.md`, `README.md`, `ROADMAP.md`, `SPEC_INDEX.md`
- RealityGapBench documents and case artifacts under `benchmarks/reality-gap/`
- Anti-collapse fixture artifacts under `conformance/fixtures/anti-collapse/reality-gap/`
- RFC documents under `rfc/`
- CEP specification files under `spec/`
- `spec/index.md`

### Files Skipped
Strategic briefs/operating briefs from older messages (Msg 45, 47, 49) were skipped as they do not constitute normative or informative protocol specification files.

### Conflicts Found
None. Newer content replaced older content automatically in accordance with processing order.

### Unresolved Placement Questions
None.

## OKF Conversion Pass (EV-OKF)

- **Date**: 2026-06-26
- **Agent Name**: Antigravity
- **Task Summary**: Formatted the Canonical Evaluation Protocol repository as an OKF-compatible knowledge bundle. Added/repaired YAML frontmatter on all concept documents and generated/updated log and index files.
- **Files Inspected**:
  - `spec/CEP-0000-derivation-ladder.md` to `spec/CEP-0010-conformance.md`
  - `benchmarks/reality-gap/BENCHMARK.md`
  - `benchmarks/reality-gap/cases/rg-000x/README.md` and `declared.md`
  - `rfc/RFC-0000-template.md`, `rfc/README.md`
  - Root documents: `README.md`, `ROADMAP.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `SPEC_INDEX.md`, `.agents/CURRENT_STATUS.md`, `.agents/EVIDENCE.md`, `.agents/OPEN_QUESTIONS.md`
- **Files Modified**:
  - All specification files in `spec/` (11 files)
  - `benchmarks/reality-gap/BENCHMARK.md`
  - `benchmarks/reality-gap/cases/rg-0001/README.md` and `declared.md`
  - `benchmarks/reality-gap/cases/rg-0002/README.md` and `declared.md`
  - `benchmarks/reality-gap/cases/rg-0003/README.md` and `declared.md`
  - `rfc/RFC-0000-template.md` and `rfc/README.md`
  - `README.md`, `ROADMAP.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `SPEC_INDEX.md`, `.agents/CURRENT_STATUS.md`, `.agents/EVIDENCE.md`, `.agents/OPEN_QUESTIONS.md`
  - `spec/index.md`
- **Files Created**:
  - `tools/validate_okf.py`
  - `index.md` (root)
  - `log.md` (root)
  - `spec/log.md`
  - `benchmarks/index.md`
  - `benchmarks/reality-gap/index.md`
  - `benchmarks/reality-gap/log.md`
  - `conformance/index.md`
  - `conformance/log.md`
  - `rfc/index.md`
  - `rfc/log.md`
- **Validation Command Run**: `wsl python3 tools/validate_okf.py`
- **Validation Output**:
  ```
  Validating 39 markdown files...
  All checks passed successfully!
  ```
- **Unresolved Questions**:
  - Version and timestamp defaults for specifications (draft default `0.1.0` and bootstrap date `2026-06-26T14:13:47Z` used). Recorded in `OPEN_QUESTIONS.md` as OQ-0006 and OQ-0007.
- **Known Limitations**:
  - The validation script excludes hidden files/directories (starting with `.`) like `.git`, `.agents` and `.tmp` by design.

## EV-OKF-REPAIR — Phases 0-3 Executable Validation Slice

- **ID**: EV-OKF-REPAIR
- **Date**: 2026-06-27
- **Agent**: Codex
- **Task**: Implement phases 0 through 3 of `.agents/plans/full-cep.md`.
- **Outcome**: Completed OKF repair, `uv`-portable Python package/CLI scaffolding, corpus-derived schema registry, RealityGapBench inventory helpers, and CLI validators for schemas plus the current RealityGapBench corpus.
- **Files Changed**:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `index.md`
  - `tools/validate_okf.py`
  - `pyproject.toml`
  - `uv.lock`
  - `justfile`
  - `src/cep/`
  - `schemas/`
  - `tests/`
  - `.agents/plans/full-cep.md`
  - `.agents/CURRENT_STATUS.md`
  - `.agents/EVIDENCE.md`
  - `.agents/DEBT.md`
- **Validation Commands**:
  - `uv run ruff format --check src tests`
  - `uv run ruff check src tests`
  - `uv run basedpyright`
  - `uv run pytest`
  - `uv run cep --help`
  - `uv run cep doctor`
  - `uv run cep validate all`
  - `uv run python tools/validate_okf.py`
  - Hidden-file ripgrep search for the obsolete handoff filename.
- **Validation Result**:
  - Ruff format: passed.
  - Ruff lint: passed.
  - Basedpyright: `0 errors, 0 warnings, 0 notes`.
  - Pytest: 10 passed.
  - CLI help: passed.
  - CLI doctor: printed `CEP runtime OK`.
  - CLI validation: all schemas, RealityGapBench cases, answer keys, example answers, evidence files, anti-collapse manifest, and anti-collapse fixtures passed.
  - OKF validation: passed.
  - Obsolete handoff reference search: no matches.
- **Fidelity Notes**:
  - Existing RealityGapBench cases, answer keys, examples, evidence files, and anti-collapse fixtures were not rewritten.
  - Schemas follow the current corpus field names such as `case_ref`, `evidence_id`, `family_ref`, and `benchmark_ref` rather than forcing simplified plan examples.
  - The validation surface uses `uv` commands for portability.
- **Remaining Gaps**:
  - Phase 4 scorer is not implemented.
- **Status**: Complete.

## EV-CR-REVIEW-FIXES — `.tmp/cr.md` Review Follow-Up

- **ID**: EV-CR-REVIEW-FIXES
- **Date**: 2026-06-27
- **Agent**: Codex
- **Task**: Verify and address the 18 review prompts in `.tmp/cr.md`, strike completed items, then commit and push.
- **Outcome**: Implemented all still-valid review fixes with stricter JSON schema contracts, stricter registry/profile validation, portable repo-root discovery through `CEP_REPO_ROOT`/working-tree discovery, a real `cep doctor` schema probe, failing OKF link checks for concept documents, and corrected plan snippets.
- **Files Changed**:
  - `.tmp/cr.md`
  - `.agents/CURRENT_STATUS.md`
  - `.agents/EVIDENCE.md`
  - `.agents/plans/full-cep.md`
  - `schemas/`
  - `src/cep/`
  - `tests/`
  - `tools/validate_okf.py`
- **Validation Commands**:
  - `uv run ruff format --check src tests`
  - `uv run ruff check src tests`
  - `uv run basedpyright`
  - `uv run pytest`
  - `uv run cep doctor`
  - `uv run cep validate all`
  - `uv run python tools/validate_okf.py`
  - `rg --hidden --glob '!.git/**' -n "AGENT_STATE\\.md" .`
- **Validation Result**:
  - Ruff format: passed.
  - Ruff lint: passed.
  - Basedpyright: `0 errors, 0 warnings, 0 notes`.
  - Pytest: 10 passed.
  - CLI doctor: printed `CEP runtime OK`.
  - CLI validation: all schemas and current corpus artifacts passed.
  - OKF validation: passed.
  - Obsolete handoff reference search: no matches.
- **Fidelity Notes**:
  - Review prompts were verified against current files before changes.
  - The validator rejects unsupported schema keywords rather than silently under-validating.
  - Strict schemas preserve existing corpus fields and CEP protected distinctions.
- **Remaining Gaps**:
  - Phase 4 scorer remains the next executable proof.
- **Status**: Complete.

## EV-REALITY-GAP-PROOF — Phases 4-7 RealityGapBench Executable Proof

- **ID**: EV-REALITY-GAP-PROOF
- **Date**: 2026-06-27
- **Agent**: Codex
- **Task**: Complete phases 4 through 7 of `.agents/plans/full-cep.md`.
- **Outcome**: Added RealityGapBench scoring against existing answer keys, anti-collapse conformance checks, JSON report generation, CLI run commands, repeatable `just all` proof command, and CI workflow.
- **Files Changed**:
  - `.github/workflows/ci.yml`
  - `.gitignore`
  - `.agents/CURRENT_STATUS.md`
  - `.agents/EVIDENCE.md`
  - `.agents/plans/full-cep.md`
  - `README.md`
  - `justfile`
  - `schemas/benchmark-result.schema.json`
  - `src/cep/benchmarks/`
  - `src/cep/conformance/`
  - `src/cep/reports.py`
  - `src/cep/scoring/`
  - `src/cep/cli.py`
  - `tests/test_anti_collapse_conformance.py`
  - `tests/test_reality_gap_reports.py`
  - `tests/test_reality_gap_scoring.py`
- **Validation Commands**:
  - `uv run ruff format --check src tests`
  - `uv run ruff check src tests`
  - `uv run basedpyright`
  - `uv run pytest`
  - `uv run python tools/validate_okf.py`
  - `uv run pytest tests/test_reality_gap_scoring.py tests/test_anti_collapse_conformance.py tests/test_reality_gap_reports.py`
  - `uv run cep run reality-gap --case-dir benchmarks/reality-gap/cases/rg-0001 --answer benchmarks/reality-gap/cases/rg-0001/example_valid_answer.json`
  - `just all`
- **Validation Result**:
  - Ruff format: passed.
  - Ruff lint: passed.
  - Basedpyright: `0 errors, 0 warnings, 0 notes`.
  - Pytest: 18 passed.
  - OKF validation: passed.
  - Phase-specific tests: 8 passed.
  - Single-case CLI run generated a RealityGapBench result report.
  - `just all` passed after validating OKF docs, schema/corpus artifacts, tests, anti-collapse conformance, and RealityGapBench smoke reports.
- **Fidelity Notes**:
  - Existing RealityGapBench case, answer-key, example-answer, evidence, and anti-collapse fixture content was not replaced.
  - Scoring uses existing fields such as `accepted_gap_statuses`, `accepted_gap_types`, `accepted_severity_range`, `required_evidence_refs`, affected constraints, distinctions, relations, and `accepted_next_actions`.
  - Anti-collapse conformance checks fixture `expected_validation.errors` against manifest `expected_errors`; a silent pass fails conformance.
  - Reports are generated under `reports/reality-gap/` and ignored as regenerated proof artifacts.
- **Remaining Gaps**:
  - AuthorityBench, SettlementBench, and CapabilityBench executable slices remain unimplemented.
- **Status**: Complete.

## EV-CR-PHASE4-7-REVIEW — `.tmp/cr.md` Review Completion

- **ID**: EV-CR-PHASE4-7-REVIEW
- **Date**: 2026-06-27
- **Agent**: Codex
- **Task**: Follow `.tmp/cr.md`, strike completed review items, commit, and push.
- **Outcome**: Verified all 18 review prompts against current code. Most prompts were already satisfied by the existing schema, validation, path, CLI, conformance, and handoff changes. Fixed the remaining still-valid gaps by tightening `partial_credit_rules` numeric rule maps and making `validate_instance()` reject malformed or unsupported schemas before validating payloads. Struck the completed review text in `.tmp/cr.md`.
- **Files Changed**:
  - `.agents/CURRENT_STATUS.md`
  - `.agents/EVIDENCE.md`
  - `.tmp/cr.md`
  - `schemas/reality-gap-answer-key.schema.json`
  - `src/cep/validation.py`
  - `tests/test_validation.py`
- **Validation Commands**:
  - `uv run pytest tests/test_validation.py`
  - `uv run ruff format --check src tests`
  - `uv run ruff check src tests`
  - `uv run basedpyright`
  - `uv run pytest`
  - `uv run python tools/validate_okf.py`
  - `just all`
- **Validation Result**:
  - Focused validation tests: 9 passed.
  - Ruff format: passed.
  - Ruff lint: passed.
  - Basedpyright: `0 errors, 0 warnings, 0 notes`.
  - Pytest: 20 passed.
  - OKF validation: passed.
  - `just all` passed after validating OKF docs, schema/corpus artifacts, tests, anti-collapse conformance, and RealityGapBench smoke reports.
- **Fidelity Notes**:
  - The review fixes preserve the existing RealityGapBench corpus shape.
  - Unsupported schema features now fail fast during instance validation instead of being silently ignored.
  - `partial_credit_rules` now preserves scoring meaning by requiring numeric values for known rule keys.
- **Remaining Gaps**:
  - AuthorityBench, SettlementBench, and CapabilityBench executable slices remain unimplemented.
- **Status**: Complete.
