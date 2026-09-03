---
type: "CEP Guide"
id: "cep-troubleshooting"
title: "Troubleshooting and Diagnostics Guide"
description: "Diagnostic procedures, common failure symptoms, root causes, and recovery recipes for CEP development and operations."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - troubleshooting
  - diagnostics
  - debugging
timestamp: "2026-06-27T00:00:00Z"
---

# Troubleshooting and Diagnostics Guide

This guide details common failure modes across CEP commands, test runners, and integrations, linking symptoms to underlying subsystems and recovery actions.

---

## 1. Fast Diagnostic Triage

When encountering unexpected failures, run the triage sequence:

```bash
# 1. Check Python environment and schema registry
uv run cep doctor

# 2. Validate all corpus documents against schemas
uv run cep validate all

# 3. Check anti-collapse self-defense
uv run cep conformance anti-collapse

# 4. Run full unit and benchmark smoke suite
just all
```

---

## 2. Common Symptoms and Remediation Recipes

### 2.1 `ModuleNotFoundError: No module named 'psycopg'`
* **Symptom**: `uv run pytest` fails during collection on `tests/test_ledger_exporter.py`.
* **Subsystem**: Ledger Exporter (`cep.exporters.ledger_postgres`).
* **Root Cause**: `psycopg` is an optional dependency for live database testing and is not installed in the standard dev virtualenv.
* **Remedy**:
  * If testing core CEP without Postgres: run pytest ignoring the optional test:
    ```bash
    uv run pytest --ignore=tests/test_ledger_exporter.py
    ```
  * If working on Postgres ledger integration: install psycopg into the virtualenv:
    ```bash
    uv add psycopg
    ```

---

### 2.2 Candidate Answer Scores High Raw Points but Status is `INVALID`
* **Symptom**: `cep run reality-gap` outputs `INVALID <case_id> <answer_id> score=35.0` despite matching all labels.
* **Subsystem**: Anti-Collapse Detector (`cep.detect`) and Scorer (`cep.benchmarks.reality_gap`).
* **Root Cause**: The candidate committed one or more semantic collapses. In `reports/<family>/<result>.json`, inspect `critical_failures`. If `declared_observed_collapse` fired, `declared_state_refs` and `observed_state_refs` were set-identical.
* **Remedy**: Ensure the candidate distinguishes what was declared from what was observed. Score caps are non-negotiable and override partial credit.

---

### 2.3 Candidate Answer Receives Score of 84.0 and Cannot Pass
* **Symptom**: Candidate predicted correct `gap_status`, `gap_type`, and `severity`, but received `status: "partial"` with score `84.0`.
* **Subsystem**: Anti-Collapse Detector (`cep.detect: reasoning_is_grounded`).
* **Root Cause**: `gap_summary` did not include both words `"declared"` and `"observed"`. The engine flagged `ungrounded_reasoning` and capped the score at 84.0 (below `PASS_THRESHOLD = 85`).
* **Remedy**: Ensure the candidate's reasoning explicitly compares declared expectations with observed traces.

---

### 2.4 `missing evidence file: ev-rg-XXXX-XXX`
* **Symptom**: `cep validate reality-gap-corpus` reports a missing evidence file.
* **Subsystem**: Validation Subsystem (`cep.validation:_case_evidence_refs`).
* **Root Cause**: `case.cep.json` lists an evidence ID under `required_evidence_refs` or `optional_evidence_refs` that does not exist in `benchmarks/reality-gap/cases/<case_id>/evidence/`.
* **Remedy**: Add the missing `<evidence_id>.json` file or remove the reference from `case.cep.json`.

---

### 2.5 `unsupported schema keyword $defs`
* **Symptom**: `cep validate schemas` fails with `unsupported schema keyword $defs`.
* **Subsystem**: Schema Profile Engine (`cep.schema_profile`).
* **Root Cause**: CEP enforces a strict JSON Schema Draft 2020-12 profile (`SUPPORTED_SCHEMA_KEYS`) to ensure deterministic validation. `$defs` is not permitted in root schemas; use direct properties or external schema references.
* **Remedy**: Inline the definition or reference an external registered schema file.

---

### 2.6 `tools/validate_okf.py` Fails with Missing Link Error
* **Symptom**: `just validate` fails with `ERROR: Link '...' in concept ... does not point to an existing file`.
* **Subsystem**: Repository Documentation Tool (`tools/validate_okf.py`).
* **Root Cause**: A markdown link points to a non-existent file or uses an unsupported absolute path format.
* **Remedy**: Use relative paths from the markdown file's directory and verify that the target document exists.

---

## 3. Diagnostic Commands Reference

| Check | Command | Expected Output |
|---|---|---|
| Schema Integrity | `uv run cep validate schemas` | `PASS schemas/...` for all 10 schemas. |
| RealityGap Corpus | `uv run cep validate reality-gap-corpus` | `PASS` for all cases, keys, answers, and evidence. |
| Conformance Suite | `uv run cep conformance anti-collapse` | `PASS rg-ac-0001` through `rg-ac-0010` and cross-family invariants. |
| Single Answer Run | `uv run cep run reality-gap --case-dir benchmarks/reality-gap/cases/rg-0001 --answer benchmarks/reality-gap/cases/rg-0001/example_valid_answer.json` | `PASS rg-0001 ans-rg-0001-valid-example score=99.0` |
| Full Local Proof | `just all` | Clean run of validate, test, conformance, and smoke. |
