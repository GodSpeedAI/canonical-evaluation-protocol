---
type: "CEP Subsystem Guide"
id: "cep-subsystem-benchmark-suites"
title: "Benchmark Suites and Scoring Subsystem"
description: "Implementation, scoring mechanics, recall formulas, and failure caps for CEP benchmark families."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - subsystem
  - benchmarks
  - scoring
timestamp: "2026-06-27T00:00:00Z"
---

# Benchmark Suites and Scoring Subsystem

## 1. Purpose
The Benchmark Suites and Scoring Subsystem implements the evaluation mechanics for the four canonical benchmark families. It computes multidimensional recall, combines partial credit from data-driven answer keys, triggers collapse detectors, and enforces strict failure score caps to produce standardized `ScoreRecord` results.

---

## 2. Responsibilities and Non-Responsibilities

### Responsibilities
* **Mathematical Recall Calculation**: Calculating set-intersection recall over evidence IDs, constraints, distinctions, and relations.
* **Family-Specific Scoring Models**:
  * **RealityGapBench**: Multi-factor partial credit + recall + next-action evaluation.
  * **AuthorityBench**: Decision correctness (`allow`/`deny`/`escalate`) + distinction and evidence recall.
  * **SettlementBench**: Settlement status (`settled`/`partially_settled`/`unsettled`) + consequence evidence recall.
  * **CapabilityBench**: Capability status + affordance basis verification.
* **Failure Score Capping**: Overriding high scores when critical semantic collapses occur.
* **Standardized Status Assignment**: Categorizing outcomes into `pass`, `partial`, `fail`, or `invalid`.

### Non-Responsibilities
* **Report File Writing**: Does not serialize reports to disk (handled by `cep.reports`).
* **Fixture Discovery**: Does not traverse the filesystem (handled by `cep.inventory`).

---

## 3. Position in the System

```text
[Case Directory] ──> [load answer_key.json] ──┐
                                              ├──> [cep.benchmarks.<family>.score()]
[Candidate File] ──> [load answer.json]     ──┘                     │
                                                                    ▼
                                                            [recall() metrics]
                                                                    │
                                                        [Failure Caps Applied]
                                                                    │
                                                                    ▼
                                                             [ScoreRecord]
```

---

## 4. Scoring Formulation and Thresholds

### 4.1 Common Scoring Rules (`cep.scoring.common`)

#### Recall Formula
$$\text{Recall}(E, O) = \begin{cases} 1.0 & \text{if } |E| = 0 \\ \frac{|E \cap O|}{|E|} & \text{if } |E| > 0 \end{cases}$$
where $E$ is the set of required elements from the answer key and $O$ is the set of observed elements from the candidate answer. Vacuously complete sets evaluate to $1.0$.

#### Status Classification
* **`pass`**: $\text{Score} \ge 85.0$ and zero critical failures.
* **`partial`**: $60.0 \le \text{Score} < 85.0$ and zero critical failures.
* **`fail`**: $0.0 < \text{Score} < 60.0$, or score capped by critical failure.
* **`invalid`**: Critical failures present and $\text{Score} \le 40.0$, or score is $0.0$.

---

## 5. Family Scoring Details

### 5.1 RealityGapBench (`cep.benchmarks.reality_gap`)
Evaluates divergence between declared and observed reality.
* **Raw Score Breakdown (Max 100.0)**:
  * Gap Status match (from answer key partial credit rules): up to ~30 pts.
  * Gap Type match (partial credit rules): up to ~15 pts.
  * Severity match (partial credit rules): up to ~15 pts.
  * Evidence Recall: $20.0 \times \text{Recall}$.
  * Constraint Recall: $10.0 \times \text{Recall}$.
  * Distinction Recall: $10.0 \times \text{Recall}$.
  * Relation Recall: $10.0 \times \text{Recall}$.
  * Recommended Action Type match: up to $4.0$ pts.
* **Critical Failure Caps**:
  ```python
  CRITICAL_FAILURE_CAPS = {
      "declared_observed_collapse": 35.0,
      "claim_as_evidence": 35.0,
      "summary_source_collapse": 45.0,
      "unknown_as_false": 40.0,
      "missing_evidence_as_failure_proof": 40.0,
      "missing_evidence_as_no_gap": 35.0,
      "completion_settlement_collapse": 35.0,
      "ci_approval_collapse": 40.0,
      "possibility_affordance_collapse": 35.0,
      "authority_capability_collapse": 35.0,
      "score_capability_collapse": 45.0,
      "single_success_capability_collapse": 45.0,
      "opposite_answer_with_high_confidence": 35.0,
  }
  ```
* **Ungrounded Reasoning Cap**: If `gap_summary` fails to reference both declared and observed state, score is capped at `84.0` (with warning `ungrounded_reasoning`).

### 5.2 AuthorityBench (`cep.benchmarks.authority`)
Evaluates whether actor execution permissions preserve policy boundaries (`authority ≠ capability`).
* Decision Match (`allow`/`deny`/`escalate`): 50.0 pts.
* Evidence Recall: $30.0 \times \text{Recall}$.
* Distinction Recall: $20.0 \times \text{Recall}$.
* Critical Caps:
  * `unsafe_authority_recommendation` (allowed on deny case): capped at 25.0.
  * `authority_capability_collapse` (confusing capability with authority): capped at 35.0.

### 5.3 SettlementBench (`cep.benchmarks.settlement`)
Evaluates consequence registration vs mechanical completion (`completion ≠ settlement`).
* Settlement Status Match (`settled`/`partially_settled`/`unsettled`): 50.0 pts.
* Evidence Recall: $30.0 \times \text{Recall}$.
* Distinction Recall: $20.0 \times \text{Recall}$.
* Critical Caps:
  * `completion_settlement_collapse`: capped at 30.0.
* Synchronous Call Surface: Exposes `from_settlement_recorded()` and `score_settlement_answer()` for external agent runtime integration.

### 5.4 CapabilityBench (`cep.benchmarks.capability`)
Evaluates repeatable capability vs one-time success (`score ≠ capability`, `possibility ≠ affordance`).
* Capability Status Match: 50.0 pts.
* Evidence Recall: $30.0 \times \text{Recall}$.
* Distinction Recall: $20.0 \times \text{Recall}$.
* Critical Caps:
  * `score_capability_collapse`: capped at 35.0.
  * `possibility_affordance_collapse`: capped at 35.0.

---

## 6. Failure Modes and Diagnostics

| Symptom | Cause | Diagnostic Command | Remedy |
|---|---|---|---|
| Candidate answer scores 99.0 raw but status is `invalid` | Critical failure cap fired, truncating the final score to $\le 40.0$. | `uv run cep run reality-gap --case-dir ... --answer ...` | Check `critical_failures` in result JSON and resolve semantic collapse. |
| Candidate answer scores 84.0 and cannot reach `pass` | `ungrounded_reasoning` warning triggered; prose omits declared/observed grounding. | `uv run cep run reality-gap ...` | Ensure `gap_summary` articulates both declared expectations and observed telemetry. |
| Division by zero in recall | Answer key has empty requirements. | `pytest tests/test_reality_gap_scoring.py` | `recall()` handles empty sets by returning $1.0$ (vacuously complete). |

---

## 7. Extension Points

1. **Adding a New Benchmark Family**:
   * Create `src/cep/benchmarks/<new_family>.py` implementing `score_<new_family>(case_dir, answer_path) -> ScoreRecord`.
   * Define typed `AnswerKey` and `Answer` models inheriting from `pydantic.BaseModel`.
   * Add family case directory under `benchmarks/<new_family>/cases/`.
   * Register runner command in `src/cep/cli.py` under the `run` group.

---

## 8. Source Trail

* [scoring/common.py](../../src/cep/scoring/common.py) — `ScoreMetrics`, `ScoreRecord`, `recall()`, `status_from_score()`
* [benchmarks/reality_gap.py](../../src/cep/benchmarks/reality_gap.py) — `score_reality_gap()`, `CRITICAL_FAILURE_CAPS`, `UNGROUNDED_REASONING_CAP`
* [benchmarks/authority.py](../../src/cep/benchmarks/authority.py) — `score_authority()`, `AuthorityAnswerKey`, `AuthorityAnswer`
* [benchmarks/settlement.py](../../src/cep/benchmarks/settlement.py) — `score_settlement()`, `score_settlement_answer()`, `from_settlement_recorded()`
* [benchmarks/capability.py](../../src/cep/benchmarks/capability.py) — `score_capability()`, `CapabilityAnswerKey`, `CapabilityAnswer`
* [tests/test_reality_gap_scoring.py](../../tests/test_reality_gap_scoring.py) — RealityGap scoring test suite
* [tests/test_authority_bench.py](../../tests/test_authority_bench.py) — AuthorityBench test suite
* [tests/test_settlement_bench.py](../../tests/test_settlement_bench.py) — SettlementBench test suite
* [tests/test_capability_bench.py](../../tests/test_capability_bench.py) — CapabilityBench test suite
