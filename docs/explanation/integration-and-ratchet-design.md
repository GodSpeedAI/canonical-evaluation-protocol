---
type: "CEP Explanation Guide"
id: "cep-explanation-integration-ratchet"
title: "Why Decoupled Call Surfaces and Export Ratchets were Designed"
description: "Architectural rationale for separating protocol vocabulary from producer event formats and enforcing week-over-week performance ratchets."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - explanation
  - integration
  - ledger
  - ratchet
timestamp: "2026-06-27T00:00:00Z"
---

# Why Decoupled Call Surfaces and Export Ratchets were Designed

## 1. The Integration Problem: Vocabulary Imposition

When integrating an evaluation protocol into live agent platforms (such as `godspeed_agent`), two bad architectural extremes emerge:
1. **Producer Imposes on Protocol**: The protocol is rewritten to accept whatever ad-hoc event format the agent happens to emit. This destroys protocol neutrality and tightly couples evaluation to one vendor.
2. **Protocol Imposes on Producer**: The agent is forced to rewrite its internal event representations and state machines to mirror the exact vocabulary of CEP (`settlement_status`, `case_ref`, `distinctions`).

### The Solution: Stable Adapter Boundaries
CEP enforces a clean boundary:
* **The Producer owns its event payload**: `godspeed_agent` emits standard `SettlementRecorded` rows with fields like `work_request_id`, `evidence_event_id`, and `outcome: "usable" | "partial" | "unusable"`.
* **CEP owns the adaptation logic**: In `cep.benchmarks.settlement.from_settlement_recorded()`, CEP explicitly maps the producer's fields to the protocol's vocabulary.
* **Neither side bleeds into the other**: The producer does not need to know CEP schema internals, and CEP does not assume knowledge of NATS message brokers or internal agent loops.

---

## 2. Why Ground Truth is Joined Rather Than Synthesized

In `cep.exporters.ledger_postgres`, an essential design invariant is enforced: **ground truth is never hallucinated or synthesized**.

When reading a `SettlementRecorded` event:
* Does CEP declare the task "settled"?
* No. The exporter performs a SQL `LEFT JOIN` on `(work_request_id, proof_result_id)` to find the causal `EvidenceRecorded` event.
* If no causal evidence exists: ground truth is unknown. The case is counted as `skipped_no_evidence` and **not scored**.
* If causal evidence exists: `observed_result == expected_result` objectively defines whether the outcome was settled.

This enforces the protected distinction: `claim ≠ evidence`. A settlement event claiming `outcome="usable"` is merely a claim; only the presence of matching causal evidence makes it a settled fact.

---

## 3. The Philosophy of the Week-over-Week Ratchet

Conventional CI checks compare code against arbitrary static thresholds (e.g., test coverage must be $\ge 80\%$). For emerging AI capabilities, arbitrary thresholds are either trivially easy or prematurely restrictive.

The CEP ratchet (`ratchet_against`) operates on a **ratchet principle**:
1. **Baseline Inception**: The first run against a live event database establishes the historical baseline (`previous-aggregate.json`).
2. **Monotonic Progress**: Subsequent runs fail if mean capability score regresses by more than `max_regression`.
3. **Zero Tolerance for Semantic Collapse**: While mean score regression allows slight operational noise, **any settlement collapse (`collapse_count > 0`) triggers an immediate, non-negotiable exit code 1**.

This guarantees that while agent models and prompts evolve, they can never regress into conflating mechanical task execution with verified settlement.

---

## 4. Source Trail

* [src/cep/exporters/ledger_postgres.py](../../src/cep/exporters/ledger_postgres.py) — `export_settlement_corpus()`, `ratchet_against()`
* [src/cep/benchmarks/settlement.py](../../src/cep/benchmarks/settlement.py) — `from_settlement_recorded()`, `score_settlement_answer()`
* [docs/settlement-call-surface.md](../settlement-call-surface.md) — Public synchronous call surface specification
* [justfile](../../justfile) — `ledger-eval` command definition
