---
type: "CEP How-To Guide"
id: "cep-howto-export-ratchet-ledger"
title: "How to Export and Ratchet PostgreSQL Ledger Events"
description: "Instructions for running the live PostgreSQL event exporter, generating benchmark cases, and enforcing the anti-collapse performance ratchet."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - how-to
  - ledger
  - postgres
  - ratchet
timestamp: "2026-06-27T00:00:00Z"
---

# How to Export and Ratchet PostgreSQL Ledger Events

## Goal
Extract real `SettlementRecorded` and causal `EvidenceRecorded` events from a live PostgreSQL event store, score them as a genuine CEP benchmark corpus, and enforce that capabilities have not regressed week-over-week.

---

## Prerequisites
1. PostgreSQL running with `event_log.agent_events` populated.
2. `psycopg` installed (`uv add psycopg`).
3. Connection string (DSN) to the database.

---

## Procedure

### Step 1: Run the Exporter and Ratchet Recipe
Run the `ledger-eval` recipe via `just`:
```bash
just ledger-eval PG_DSN="postgresql://user:password@localhost:5432/agent_memory"
```

Or invoke via Python directly:
```bash
uv run python -c "
from cep.exporters.ledger_postgres import export_settlement_corpus, ratchet_against
import sys

report = export_settlement_corpus('postgresql://user:password@localhost:5432/agent_memory', 'reports/ledger/current')
exit_code = ratchet_against('reports/ledger/previous-aggregate.json', report)
sys.exit(exit_code)
"
```

### Step 2: Inspect the Generated Corpus
The exporter writes one case directory per recorded settlement into `reports/ledger/current/`:
```bash
ls -la reports/ledger/current/
```
In each `case-<work_request_id>/` folder:
* `settlement_recorded.json`: The original event payload from Postgres.
* `answer_key.json`: Ground truth derived from causal evidence.
* `example_ledger_answer.json`: Adapted settlement answer.
* `result.json`: CEP evaluation score and metrics.

### Step 3: Inspect the Aggregate Summary
View `reports/ledger/current/aggregate.json`:
```json
{
  "case_count": 12,
  "collapse_count": 0,
  "fail_count": 1,
  "mean_score": 88.5,
  "pass_count": 10,
  "scored": 11,
  "skipped_no_evidence": 1
}
```

### Step 4: Promote the Baseline
If running in CI, update the historical baseline when the ratchet passes:
```bash
cp reports/ledger/current/aggregate.json reports/ledger/previous-aggregate.json
```

---

## Troubleshooting

| Symptom | Cause | Remedy |
|---|---|---|
| `psycopg.OperationalError: connection refused` | PostgreSQL is not running or port 5432 is blocked. | Verify database status (`docker compose ps` or `pg_isready`). |
| `RATCHET FAIL: X settlement collapse(s) detected` | An agent claimed settlement (`usable`) when evidence showed failure. | Inspect `reports/ledger/current/case-*/result.json` to find the violating task ID. |
| `All rows skipped_no_evidence` | Settlements lack causal `EvidenceRecorded` events on the same `(work_request_id, proof_result_id)`. | Verify your agent emits `EvidenceRecorded` before `SettlementRecorded`. |
