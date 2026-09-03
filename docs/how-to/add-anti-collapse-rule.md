---
type: "CEP How-To Guide"
id: "cep-howto-add-anti-collapse-rule"
title: "How to Add a New Anti-Collapse Detection Rule"
description: "Step-by-step instructions for extending the CEP detection engine with new collapse codes and regression tests."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - how-to
  - anti-collapse
  - development
timestamp: "2026-06-27T00:00:00Z"
---

# How to Add a New Anti-Collapse Detection Rule

## Goal
Add a new semantic collapse code (e.g., detecting when an answer confuses temporary caching with persistent storage) to `src/cep/detect.py`, assign its failure score cap, and add automated regression fixtures to the conformance suite.

---

## Prerequisites
* Development environment with `pytest` and `ruff` (`uv sync --dev`).
* Familiarity with the 21 protected distinctions in [AGENTS.md](../../AGENTS.md).

---

## Procedure

### Step 1: Implement the Detection Heuristic
In `src/cep/detect.py`, locate `_semantic_collapses(s: _Signals)`:
1. Define the triggering conditions using answer text, relations, or action types.
2. Add the collapse code to `failures`:
```python
# cache ≠ persistence collapse: "cached in memory, so permanently saved"
if "cached" in s.text and any(p in s.text for p in ("persisted", "permanently saved")):
    failures.add("cache_persistence_collapse")
```

### Step 2: Assign a Score Failure Cap
In `src/cep/benchmarks/reality_gap.py`, add the failure cap to `CRITICAL_FAILURE_CAPS`:
```python
CRITICAL_FAILURE_CAPS: Final[dict[str, float]] = {
    ...
    "cache_persistence_collapse": 35.0,
}
```

### Step 3: Author a Conformance Fixture
Create `conformance/fixtures/anti-collapse/reality-gap/rg-ac-0011-cache-persistence-collapse.json`:
```json
{
  "fixture_id": "rg-ac-0011",
  "fixture_type": "anti-collapse",
  "benchmark_family": "RealityGapBench",
  "target_case_ref": "rg-0001",
  "description": "Answer treats in-memory cache update as persistent storage settlement.",
  "submitted_answer": {
    "answer_id": "ans-rg-ac-0011",
    "case_ref": "rg-0001",
    "gap_status": "no_gap_detected",
    "gap_type": "none",
    "severity": "none",
    "gap_summary": "Declared state and observed state match because record is cached in memory, so permanently saved.",
    "declared_state_refs": ["state-decl-01"],
    "observed_state_refs": ["state-obs-01"],
    "evidence_refs": ["ev-rg-0001-001"],
    "confidence": { "value": "high", "basis": "Cache confirmed." },
    "recommended_next_action": { "type": "no_action_required", "description": "Done." },
    "limitations": []
  },
  "expected_validation": {
    "status": "invalid",
    "errors": ["cache_persistence_collapse"],
    "warnings": [],
    "critical": true
  },
  "protected_distinctions": ["state / transformation"],
  "why_invalid": ["Treats volatile cache as durable persistence."]
}
```

### Step 4: Register the Fixture in the Manifest
Edit `conformance/fixtures/anti-collapse/reality-gap/manifest.json` and append:
```json
{
  "fixture_id": "rg-ac-0011",
  "file": "rg-ac-0011-cache-persistence-collapse.json",
  "expected_errors": ["cache_persistence_collapse"]
}
```

---

## Validation

Run the conformance suite and unit tests:
```bash
# Verify the conformance harness catches the new fixture
uv run cep conformance anti-collapse

# Run pytest
uv run pytest tests/test_anti_collapse_conformance.py
```
*Expected Output*: `PASS rg-ac-0011: Expected anti-collapse failures observed.`

---

## Rollback / Recovery
If the heuristic introduces false positives across existing cases:
1. Revert changes in `src/cep/detect.py` and `reality_gap.py`.
2. Remove the fixture file and unregister it from `manifest.json`.
3. Verify `just all` returns to green.
