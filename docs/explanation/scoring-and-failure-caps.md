---
type: "CEP Explanation Guide"
id: "cep-explanation-scoring-caps"
title: "Why Hard Score Caps and Multi-Factor Recall are Enforced"
description: "Mathematical and epistemological rationale for score capping, recall weighting, and ungrounded reasoning penalties."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - explanation
  - scoring
  - metrics
  - math
timestamp: "2026-06-27T00:00:00Z"
---

# Why Hard Score Caps and Multi-Factor Recall are Enforced

## 1. The Myth of the Monolithic Metric

In conventional benchmarks, performance is summarized as an aggregate scalar (e.g., accuracy = 87.4%). In complex workflows, aggregate scalars mask severe systemic vulnerabilities. A model can:
1. Accurately predict an output category by guessing or exploiting surface tokens.
2. Fabricate completely non-existent evidence IDs.
3. Fail to identify the governing policy constraint.
4. Conflate its execution attempt with verifiable settlement.

Under standard averaging, that answer might score 70% or 80%. In production systems, such an answer is dangerous: it represents an ungrounded hallucination masquerading as verified operational action.

---

## 2. Multi-Factor Recall Architecture

CEP separates evaluation into multiple orthogonal recall dimensions:

$$\begin{aligned}
\text{Evidence Recall} &= \frac{|\text{Required Evidence} \cap \text{Cited Evidence}|}{|\text{Required Evidence}|} \\
\text{Constraint Recall} &= \frac{|\text{Required Constraints} \cap \text{Cited Constraints}|}{|\text{Required Constraints}|} \\
\text{Distinction Recall} &= \frac{|\text{Required Distinctions} \cap \text{Cited Distinctions}|}{|\text{Required Distinctions}|} \\
\text{Relation Recall} &= \frac{|\text{Required Relations} \cap \text{Cited Relations}|}{|\text{Required Relations}|}
\end{aligned}$$

### Why Vacuous Completeness Evaluates to 1.0
In `cep.scoring.common.recall`:
```python
def recall(expected: set[str], observed: set[str]) -> float:
    if not expected:
        return 1.0
    return len(expected & observed) / len(expected)
```
If a benchmark case does not demand specific constraint or relation citations (for example, in lightweight cases like `AuthorityBench`), the expected set is empty. Rather than causing a division by zero or penalizing the candidate, vacuous completeness is mathematically defined as $1.0$, allowing simpler benchmark families to share the unified `ScoreMetrics` schema.

---

## 3. The Rationale for Asymmetric Failure Caps

When an answer commits a semantic collapse, CEP applies a **Failure Cap** (`CRITICAL_FAILURE_CAPS`).

```text
Final Score = min(Raw Score, min(Caps for all triggered critical failures))
```

### Why Caps Override High Raw Scores
Suppose an answer correctly identifies `gap_status="divergence_detected"`, `gap_type="unauthorized_change"`, and `severity="critical"`, earning 60 points of partial credit. However, in its citations, it copies `state-observed-01` into both `declared_state_refs` and `observed_state_refs`.

This triggers `declared_observed_collapse` (collapse cap: 35.0).
* The raw score is 60.0.
* The capped score is 35.0.
* The status is set to `invalid`.

**Rationale**: Treating the observed state as the declared state means the system has no concept of policy baseline. Allowing that candidate to pass or receive partial credit would signal operational readiness when the system actually lacks basic boundary awareness.

---

## 4. The Ungrounded Reasoning Penalty (84.0 Cap)

Why is the ungrounded reasoning cap specifically set to **84.0**?

In `cep.scoring.common`:
* `PASS_THRESHOLD = 85`
* `UNGROUNDED_REASONING_CAP = 84.0`

If a candidate answer correctly guesses the exact status, type, severity, and action, but its `gap_summary` fails to reference both declared and observed realities (`reasoning_is_grounded`), the engine caps its score at 84.0.

Because 84.0 is strictly below the pass threshold of 85.0:
* The candidate receives `status="partial"`.
* It receives warning `"ungrounded_reasoning"`.
* It is mathematically blocked from passing.

This prevents models from achieving perfect scores through label gaming without providing coherent reasoning.

---

## 5. Source Trail

* [src/cep/scoring/common.py](../../src/cep/scoring/common.py) — Thresholds, recall function, `status_from_score()`
* [src/cep/benchmarks/reality_gap.py](../../src/cep/benchmarks/reality_gap.py) — `CRITICAL_FAILURE_CAPS`, `UNGROUNDED_REASONING_CAP`
* [tests/test_reality_gap_scoring.py](../../tests/test_reality_gap_scoring.py) — Verification tests for failure caps and thresholds
