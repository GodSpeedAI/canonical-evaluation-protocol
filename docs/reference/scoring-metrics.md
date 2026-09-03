---
type: "CEP Technical Reference"
id: "cep-reference-scoring-metrics"
title: "Benchmark Scoring Metrics and Thresholds Reference"
description: "Reference guide for numerical scoring thresholds, status classification, and metric calculations across CEP benchmark families."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - reference
  - scoring
  - metrics
timestamp: "2026-06-27T00:00:00Z"
---

# Benchmark Scoring Metrics and Thresholds Reference

This reference details the exact mathematical formulas, classification thresholds, and score caps utilized across the CEP evaluation engine.

---

## 1. Classification Thresholds

Defined in [src/cep/scoring/common.py](../../src/cep/scoring/common.py):

| Constant | Value | Description |
|---|---|---|
| `PASS_THRESHOLD` | `85.0` | Minimum score required for `status = "pass"`. Requires zero critical failures. |
| `PARTIAL_THRESHOLD` | `60.0` | Minimum score required for `status = "partial"`. Requires zero critical failures. |
| `INVALID_FAILURE_THRESHOLD` | `40.0` | Upper score boundary for `status = "invalid"` when critical failures are present. |
| `UNGROUNDED_REASONING_CAP` | `84.0` | Hard cap applied when `gap_summary` lacks grounding keywords (`declared` and `observed`). |

---

## 2. Status Decision Matrix (`status_from_score`)

```python
def status_from_score(score: float, critical_failures: list[str]) -> ScoreStatus:
    if critical_failures and score <= INVALID_FAILURE_THRESHOLD:
        return "invalid"
    if score >= PASS_THRESHOLD and not critical_failures:
        return "pass"
    if score >= PARTIAL_THRESHOLD and not critical_failures:
        return "partial"
    if score > 0:
        return "fail"
    return "invalid"
```

| Final Score | Critical Failures | Resulting Status | Meaning |
|---|---|---|---|
| $\ge 85.0$ | Empty (`[]`) | `"pass"` | Comprehensive understanding and verified grounding. |
| $60.0 \le \text{Score} < 85.0$ | Empty (`[]`) | `"partial"` | Substantial recall without ontological collapse. |
| $< 60.0$ and $> 0.0$ | Empty (`[]`) | `"fail"` | Insufficient recall or incorrect classification. |
| $\le 40.0$ | Non-empty | `"invalid"` | Ontological collapse committed; result rejected. |
| $> 40.0$ | Non-empty | `"fail"` | Critical collapse present with moderate partial credit (rare). |
| $0.0$ | Any | `"invalid"` | Zero credit earned. |

---

## 3. Score Cap Mechanics

When an answer commits multiple collapses, the final score is the minimum of the raw score and the strictest applicable cap:

$$\text{Final Score} = \min\left(\text{Raw Score}, \min_{c \in \text{Failures}}(\text{Cap}_c), \text{GroundingCap}\right)$$

* Caps are never averaged.
* The most restrictive failure cap strictly dictates the score ceiling.
* An answer committing `declared_observed_collapse` (cap: 35.0) and `summary_source_collapse` (cap: 45.0) will be capped at **35.0**, resulting in status `"invalid"`.
