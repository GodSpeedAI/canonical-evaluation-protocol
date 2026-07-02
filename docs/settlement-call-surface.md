---
type: "CEP Guide"
id: "cep-settlement-call-surface"
title: "Settlement Scoring Call Surface"
description: "How a producer repo calls CEP's SettlementBench scorer synchronously at settlement time."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - guide
  - settlement
timestamp: "2026-07-01T00:00:00Z"
---

# Settlement Scoring Call Surface

Any producer repo (today: `godspeed_agent`) can score a settlement event
synchronously, without CEP knowing anything about the producer, NATS, or the
live loop. CEP owns the vocabulary translation; the producer supplies its own
`SettlementRecorded`-shaped payload and its own expectation for that case.

## Python

```python
from cep.benchmarks.settlement import (
    SettlementAnswerKey,
    from_settlement_recorded,
    score_settlement_answer,
)

answer = from_settlement_recorded(
    settlement_recorded_payload,       # dict: the real SettlementRecorded event's "payload"
    evidence_refs=["ev-0001"],          # optional, what the producer actually gathered
    preserved_distinctions=[],          # optional
)
answer_key = SettlementAnswerKey(
    case_ref=settlement_recorded_payload["work_request_id"],
    expected_settlement_status="partially_settled",  # from the producer's own work request
    required_evidence_refs=["ev-0001"],
    required_distinctions=["completion_vs_settlement"],
)
result = score_settlement_answer(answer_key, answer)
result.score, result.status, result.critical_failures
```

`from_settlement_recorded` maps godspeed_agent's real event fields
(`agentic_capability_loop/adapters.py: emit_settlement_recorded`) —
`work_request_id`, `evidence_event_id`, `outcome` (`usable` | `partial` |
`unusable`) — onto CEP's `SettlementAnswer` vocabulary. `outcome` maps to
`settlement_status` (`settled` | `partially_settled` | `unsettled`);
`completion_claim_accepted` is true only for `usable`.

CEP does not know what a case *expects* — that's the producer's own work
request context, not something CEP can derive from the event. Callers must
supply `expected_settlement_status`, `required_evidence_refs`, and
`required_distinctions` themselves.

## CLI

```bash
cep score-settlement --input path/to/input.json
```

Input file shape:

```json
{
  "settlement_recorded": { "...": "the real SettlementRecorded envelope" },
  "expected": {
    "expected_settlement_status": "partially_settled",
    "required_evidence_refs": ["ev-0001"],
    "required_distinctions": ["completion_vs_settlement"]
  },
  "evidence_refs": [],
  "preserved_distinctions": []
}
```

Output: one line, `<STATUS> <case_id> <answer_id> score=<score>`, plus a
second line listing `critical_failures` when present. Exit code is always 0
for a successfully scored input (the printed status carries the verdict);
CEP does not fail the process on a low score, since a low score is a valid,
expected outcome for a genuinely-unsettled case.

A fixture that claims `usable` (settled) when the case only expected
`partially_settled` triggers `completion_settlement_collapse` and caps the
score at 30 — this routes through the same `CRITICAL_FAILURE_CAPS` used by
every other SettlementBench answer; it is not a separate, unenforced path.
See `tests/fixtures/sample_settlement_recorded.json` for a worked example.
