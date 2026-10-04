---
type: "CEP How-To Guide"
id: "cep-howto-evaluate-external-corpus"
title: "How to Evaluate an External Corpus"
description: "Step-by-step instructions for submitting third-party evaluation records to the CEP anti-collapse conformance gate."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - how-to
  - external-corpus
  - conformance
timestamp: "2026-06-27T00:00:00Z"
---

# How to Evaluate an External Corpus

## Goal
Submit an externally produced evaluation dataset (such as an export from `sxr` or another autonomous agent evaluation framework) to CEP's anti-collapse evaluator to verify that the dataset contains zero semantic collapses.

---

## Prerequisites
1. CEP environment installed (`uv sync`).
2. Candidate corpus formatted as a JSON file adhering to the `cep/anti-collapse-corpus@1` transport envelope.

---

## Procedure

### Step 1: Format the External Corpus
Ensure your JSON file contains a `$schema` key and a `records` array. Each record must specify:
* `record_id`: Unique string identifier.
* `accepted_gap_statuses`: Array of valid statuses (e.g. `["no_gap_detected"]`).
* `valid_evidence_ids`: Array of valid evidence record IDs known to exist.
* `submitted_answer`: Candidate answer object containing `gap_summary`, `declared_state_refs`, `observed_state_refs`, etc.

Example `my_external_corpus.json`:
```json
{
  "$schema": "cep/anti-collapse-corpus@1",
  "corpus_id": "sxr-batch-2026-06",
  "records": [
    {
      "record_id": "rec-001",
      "accepted_gap_statuses": ["no_gap_detected"],
      "valid_evidence_ids": ["ev-101"],
      "submitted_answer": {
        "answer_id": "ans-001",
        "case_ref": "rg-0001",
        "gap_status": "no_gap_detected",
        "gap_summary": "Declared policy and observed traces are aligned.",
        "declared_state_refs": ["state-decl-01"],
        "observed_state_refs": ["state-obs-01"],
        "evidence_refs": ["ev-101"],
        "recommended_next_action": {
          "type": "no_action_required",
          "description": "Proceed as planned."
        },
        "limitations": []
      }
    }
  ]
}
```

### Step 2: Run the Conformance Command
Execute the command passing `--corpus`:
```bash
uv run cep conformance anti-collapse --corpus path/to/my_external_corpus.json
```

### Step 3: Interpret Results and Exit Codes
* **All Records Clean**:
  ```text
  PASS rec-001: No anti-collapse failures.
  corpus: 1/1 passed
  ```
  Exits with code `0`.
* **Collapse Detected**:
  ```text
  FAIL rec-001: Violated invariants: declared_observed_collapse
  corpus: 0/1 passed
  ```
  Exits with code `1`.

---

## Implementation Locations
* [corpus.py](../../src/cep/conformance/corpus.py) — Parser, validator, and evaluator loop.
* [detect.py](../../src/cep/detect.py) — Semantic collapse detection rules.
* [cli.py](../../src/cep/cli.py) — `conformance_anti_collapse_command()`.

---

## Validation
Verify your evaluation by testing against negative records:
```bash
uv run pytest tests/test_anti_collapse_corpus.py
```

---

## Common Failures and Troubleshooting

| Symptom | Cause | Remedy |
|---|---|---|
| `ERROR unsupported corpus schema '...'` | `$schema` is missing or does not equal `"cep/anti-collapse-corpus@1"`. | Set `"$schema": "cep/anti-collapse-corpus@1"`. |
| `ERROR corpus has no 'records' array` | Top-level payload missing `records`. | Wrap records in a `"records": [...]` list. |
| `ERROR record with empty record_id is unsupported` | A record has missing or empty `record_id`. | Supply a non-empty string for each `record_id`. |
