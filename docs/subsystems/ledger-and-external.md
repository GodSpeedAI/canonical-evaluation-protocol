---
type: "CEP Subsystem Guide"
id: "cep-subsystem-ledger-external"
title: "Ledger Exporter and External Integration Subsystem"
description: "Architecture and operational mechanics for the PostgreSQL event ledger exporter, week-over-week ratchet, and external runtime scoring surfaces."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - subsystem
  - ledger
  - postgres
  - ratchet
timestamp: "2026-06-27T00:00:00Z"
---

# Ledger Exporter and External Integration Subsystem

## 1. Purpose
The Ledger Exporter and External Integration Subsystem connects CEP to live external production runtimes. It enables the extraction of real telemetry from event stores (such as the `godspeed_agent` PostgreSQL event log), converts live runtime events into scored benchmark cases, enforces week-over-week performance ratchets, and exposes synchronous scoring interfaces for in-memory agent loops.

---

## 2. Responsibilities and Non-Responsibilities

### Responsibilities
* **Database Ingestion**: Querying PostgreSQL `event_log.agent_events` for `SettlementRecorded` rows.
* **Causation Joining**: Joining settlements to their causal `EvidenceRecorded` rows on `(work_request_id, proof_result_id)`.
* **Ground Truth Derivation**: Determining `expected_settlement_status` strictly by comparing observed and expected results in real evidence—never synthesizing artificial ground truth.
* **Corpus Generation**: Emitting structured benchmark case directories containing raw payloads, answer keys, answers, and result JSONs.
* **Regression & Anti-Collapse Ratcheting**: Comparing current aggregate metrics to previous runs and failing on mean-score degradation or any detected settlement collapse.
* **Synchronous Runtime Ingestion**: Exposing `score-settlement` CLI and Python functions for caller runtimes.

### Non-Responsibilities
* **Schema Migration & Table Creation**: Does not manage external PostgreSQL schemas or run DDL statements.
* **Event Broker Management**: Does not run NATS or Kafka message consumers.

---

## 3. Position in the System

```text
[External Agent Runtime (godspeed_agent)]
       │
       ▼ (Emits SettlementRecorded & EvidenceRecorded)
[PostgreSQL: event_log.agent_events]
       │
       ▼ (Read via SQL join in cep.exporters.ledger_postgres)
[export_settlement_corpus()]
       ├── Writes case directories to reports/ledger/current/
       ├── Scores via cep.benchmarks.settlement.score_settlement_answer()
       └── Generates reports/ledger/current/aggregate.json
              │
              ▼
       [ratchet_against()] ──(Compares with reports/ledger/previous-aggregate.json)
              │
              ├── Fails if collapse_count > 0
              ├── Fails if mean_score regressed > max_regression
              └── Returns exit code 0 or 1
```

---

## 4. Causation Join Mechanics

The PostgreSQL extractor queries `event_log.agent_events`:

```sql
SELECT
    s.payload->>'work_request_id'   AS work_request_id,
    s.payload                       AS settlement_payload,
    e.payload->>'observed_result'   AS observed_result,
    e.payload->>'expected_result'   AS expected_result
FROM event_log.agent_events s
LEFT JOIN event_log.agent_events e
    ON e.event_type = 'EvidenceRecorded'
   AND e.payload->>'work_request_id'   = s.payload->>'work_request_id'
   AND e.payload->>'proof_result_id'   = s.payload->>'proof_result_id'
WHERE s.event_type = 'SettlementRecorded'
  AND (%s::text IS NULL OR s.created_at >= %s::timestamptz)
ORDER BY s.created_at;
```

### Truth Grounding Rule
1. If `observed_result` or `expected_result` is missing (no causation evidence): the case is recorded in `settlement_recorded.json` but marked as `skipped_no_evidence`. It is **not** scored because ground truth cannot be verified without evidence.
2. If `observed_result == expected_result`: ground truth `expected_settlement_status = "settled"`.
3. If `observed_result != expected_result`: ground truth `expected_settlement_status = "unsettled"`.
If the agent's settlement payload claimed `outcome = "usable"` while evidence shows mismatch, the scorer flags `completion_settlement_collapse` and caps the score at 30.0.

---

## 5. Ratchet Enforcement Rules

The ratchet function (`ratchet_against`) ensures quality does not regress over time:

1. **Anti-Collapse Hard Cap**: If `collapse_count > 0` in the current aggregate, the ratchet job **immediately fails** (returns exit code `1`), regardless of the score.
2. **Mean Score Regression**: If `prev_mean - current_mean > max_regression` (default: 0.0), the ratchet fails.
3. **Cold Start**: If no previous aggregate file exists, the first run establishes the baseline (returns exit code `0`).

---

## 6. Synchronous Scoring Interface

For runtime loops that evaluate events without database queries, CEP provides a synchronous call surface documented in [Settlement Scoring Call Surface](../settlement-call-surface.md).

### Python API
```python
from cep.benchmarks.settlement import (
    SettlementAnswerKey,
    from_settlement_recorded,
    score_settlement_answer,
)

answer = from_settlement_recorded(
    event_payload,
    evidence_refs=["ev-001"],
    preserved_distinctions=["completion_vs_settlement"],
)
answer_key = SettlementAnswerKey(
    case_ref=event_payload["work_request_id"],
    expected_settlement_status="partially_settled",
    required_evidence_refs=["ev-001"],
    required_distinctions=["completion_vs_settlement"],
)
result = score_settlement_answer(answer_key, answer)
```

### CLI Command
```bash
cep score-settlement --input path/to/settlement-payload.json
```

---

## 7. Failure Modes and Diagnostics

| Symptom | Cause | Diagnostic Command | Remedy |
|---|---|---|---|
| `ImportError: No module named 'psycopg'` | `psycopg` is not installed in the environment. | `python -c "import psycopg"` | Install psycopg via `uv add psycopg` or run pytest with `--ignore=tests/test_ledger_exporter.py`. |
| `RATCHET FAIL: 1 settlement collapse(s) detected` | Live agent claimed a task was settled when evidence did not match expectation. | `cat reports/ledger/current/aggregate.json` | Inspect failed case in `reports/ledger/current/case-*/result.json` to identify unverified settlement claim. |
| `RATCHET FAIL: mean_score regressed` | Average capability score dropped below previous baseline. | `just ledger-eval` | Review agent prompt or tool changes that degraded performance. |

---

## 8. Source Trail

* [ledger_postgres.py](../../src/cep/exporters/ledger_postgres.py) — `export_settlement_corpus()`, `ratchet_against()`, `ExportReport`
* [benchmarks/settlement.py](../../src/cep/benchmarks/settlement.py) — `from_settlement_recorded()`, `score_settlement_answer()`, `ScoreSettlementInput`
* [justfile](../../justfile) — `ledger-eval` recipe
* [docs/settlement-call-surface.md](../settlement-call-surface.md) — Public contract specification
* [tests/test_ledger_exporter.py](../../tests/test_ledger_exporter.py) — PostgreSQL end-to-end integration tests
