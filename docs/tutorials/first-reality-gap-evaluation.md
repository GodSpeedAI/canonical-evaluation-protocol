---
type: "CEP Tutorial"
id: "cep-tutorial-first-reality-gap-eval"
title: "Tutorial: Scoring Your First RealityGap Answer"
description: "A step-by-step guided tutorial for running and evaluating candidate answers using RealityGapBench."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - tutorial
  - reality-gap
  - getting-started
timestamp: "2026-06-27T00:00:00Z"
---

# Tutorial: Scoring Your First RealityGap Answer

## 1. Learning Objective
By the end of this tutorial, you will:
1. Understand the structure of a RealityGapBench case.
2. Score a candidate answer using the CEP command-line interface.
3. Inspect the resulting JSON report document.
4. Intentionally introduce a semantic collapse and observe how the engine caps the score.

---

## 2. Prerequisites
* Python 3.11+ installed.
* `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
* Repository checkout at `/home/.../cep`.

Verify your environment before starting:
```bash
uv run cep --version
```
*Expected Output*: `0.1.0`

---

## 3. Step 1: Inspect the Target Benchmark Case

Examine the existing smoke case `rg-0001`:
```bash
ls -la benchmarks/reality-gap/cases/rg-0001/
```
You will see:
* `case.cep.json`: The problem definition (declared policy vs observed activity).
* `evidence/`: Grounding records (`ev-rg-0001-001.json`, etc.).
* `answer_key.json`: The scoring rules and accepted answers.
* `example_valid_answer.json`: A well-grounded model answer.
* `example_invalid_answer.json`: A flawed model answer committing a collapse.

---

## 4. Step 2: Score the Valid Candidate Answer

Run the scorer on the valid example answer:
```bash
uv run cep run reality-gap \
  --case-dir benchmarks/reality-gap/cases/rg-0001 \
  --answer benchmarks/reality-gap/cases/rg-0001/example_valid_answer.json \
  --out reports/reality-gap/my-valid-test.result.json
```

### Expected Output
```text
PASS rg-0001 ans-rg-0001-valid-example score=99.0
Wrote reports/reality-gap/my-valid-test.result.json
```

---

## 5. Step 3: Inspect the Generated Report

Inspect the result JSON:
```bash
cat reports/reality-gap/my-valid-test.result.json
```

### Expected Output
```json
{
  "answer_id": "ans-rg-0001-valid-example",
  "benchmark_family": "RealityGapBench",
  "case_id": "rg-0001",
  "critical_failures": [],
  "metrics": {
    "constraint_recall": 1.0,
    "distinction_recall": 1.0,
    "evidence_recall": 1.0,
    "raw_score": 99.0,
    "relation_recall": 1.0
  },
  "result_id": "result-rg-0001-ans-rg-0001-valid-example",
  "score": 99.0,
  "status": "pass",
  "warnings": []
}
```
Notice:
* `status` is `"pass"` because the score exceeds 85.0 and `critical_failures` is empty.
* Recall is 1.0 across all four dimensions.

---

## 6. Step 4: Score an Answer Committing a Semantic Collapse

Now score the invalid answer:
```bash
uv run cep run reality-gap \
  --case-dir benchmarks/reality-gap/cases/rg-0001 \
  --answer benchmarks/reality-gap/cases/rg-0001/example_invalid_answer.json \
  --out reports/reality-gap/my-invalid-test.result.json
```

### Expected Output
```text
INVALID rg-0001 ans-rg-0001-invalid-example score=0.0
Wrote reports/reality-gap/my-invalid-test.result.json
```

Inspect the output document:
```bash
cat reports/reality-gap/my-invalid-test.result.json
```
Notice the `critical_failures` array:
```json
"critical_failures": [
  "completion_settlement_collapse",
  "declared_observed_collapse",
  "opposite_answer_with_high_confidence"
]
```
Even if partial credit points were earned, the engine detected that the candidate answer used observed telemetry as declared state, capping the score and setting the status to `"invalid"`.

---

## 7. Next Steps
* Learn how score capping works mathematically in [Why Hard Score Caps are Enforced](../explanation/scoring-and-failure-caps.md).
* Learn how to author a complete benchmark case in [Tutorial: Authoring a Benchmark Case](authoring-a-benchmark-case.md).
