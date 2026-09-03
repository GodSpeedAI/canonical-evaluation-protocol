---
type: "CEP How-To Guide"
id: "cep-howto-integrate-settlement"
title: "How to Integrate Synchronous Settlement Scoring in an Agent Runtime"
description: "Instructions for embedding CEP settlement scoring directly into live autonomous agent execution loops."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - how-to
  - settlement
  - integration
timestamp: "2026-06-27T00:00:00Z"
---

# How to Integrate Synchronous Settlement Scoring in an Agent Runtime

## Goal
Enable an external agent platform (such as `godspeed_agent`) to evaluate its own `SettlementRecorded` events synchronously at runtime, computing a verified settlement score and checking for `completion_settlement_collapse` before updating capabilities.

---

## Prerequisites
1. CEP library available in the agent runtime environment (`pip install -e /path/to/cep` or Python path).
2. Agent emits `SettlementRecorded` payloads containing `work_request_id`, `evidence_event_id`, and `outcome`.

---

## Procedure

### Step 1: Import the Settlement API
In your agent's settlement or capability loop adapter:
```python
from cep.benchmarks.settlement import (
    SettlementAnswerKey,
    from_settlement_recorded,
    score_settlement_answer,
)
```

### Step 2: Map the Runtime Event to a Settlement Answer
Call `from_settlement_recorded()` to transform the raw producer event into CEP vocabulary:
```python
settlement_payload = {
    "work_request_id": "req-9842",
    "evidence_event_id": "ev-proof-101",
    "outcome": "usable",  # "usable" | "partial" | "unusable"
}

answer = from_settlement_recorded(
    settlement_payload,
    evidence_refs=["ev-proof-101"],
    preserved_distinctions=["completion_vs_settlement"],
)
```

### Step 3: Construct the Case Expectation
Define the ground truth expectation derived from the original task request:
```python
answer_key = SettlementAnswerKey(
    case_ref="req-9842",
    expected_settlement_status="settled",  # Expected for this work request
    required_evidence_refs=["ev-proof-101"],
    required_distinctions=["completion_vs_settlement"],
)
```

### Step 4: Compute the Score Record
```python
record = score_settlement_answer(answer_key, answer)

print(f"Status: {record.status}")
print(f"Score: {record.score}")
print(f"Critical Failures: {record.critical_failures}")
```

### Step 5: Gate Downstream Capability Updates
Check for critical failures before promoting agent state:
```python
if "completion_settlement_collapse" in record.critical_failures:
    logger.error("Agent committed completion_settlement_collapse! Rejecting capability update.")
    raise CapabilityGateError("Premature settlement claim rejected by CEP.")
```

---

## Alternative: CLI Ingestion
If running out-of-process, save the payload and expectation into a JSON document and invoke:
```bash
cep score-settlement --input my-settlement-call.json
```
Refer to the input format schema in [Settlement Scoring Call Surface](../settlement-call-surface.md).

---

## Implementation Locations
* [benchmarks/settlement.py](../../src/cep/benchmarks/settlement.py) — `from_settlement_recorded()`, `score_settlement_answer()`
* [cli.py](../../src/cep/cli.py) — `score_settlement_command()`
* [docs/settlement-call-surface.md](../settlement-call-surface.md) — Public contract specification

---

## Validation
Test your integration against the sample fixture:
```bash
uv run cep score-settlement --input tests/fixtures/sample_settlement_recorded.json
```
*Expected Output*:
```text
INVALID req-e2e-0001 ev-proof-0001 score=30.0
critical_failures=['completion_settlement_collapse']
```
