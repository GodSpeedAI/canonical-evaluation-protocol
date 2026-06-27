---
type: "CEP Guide"
id: "cep-docs-anti-collapse"
title: "Anti-Collapse Reference"
description: "The semantic collapses CEP protects against, the detector codes, and how engine-backed conformance works."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - reference
  - anti-collapse
  - conformance
timestamp: "2026-06-27T00:00:00Z"
---

# Anti-Collapse Reference

CEP exists to keep distinctions that most evaluation systems collapse. This
document is the reference for which collapses CEP detects, how, and where the
detection lives.

## The protected distinctions

A semantic collapse is treating one side of these pairs as if it were the other:

```text
claim ≠ evidence
completion ≠ settlement
possibility ≠ affordance
authority ≠ capability
score ≠ capability
observation ≠ evidence
representation ≠ reality
declared state ≠ observed state
policy text ≠ authority decision
one-time success ≠ metabolized capability
test pass ≠ production readiness
summary ≠ source
unknown ≠ false
```

Any answer, schema, fixture, or scorer that blurs one of these is wrong, no
matter how high it would otherwise score. A critical failure caps the result.

## How detection works

Detection is content-based and lives in one place:
`src/cep/detect.py`. It inspects the **content** of a submitted answer — its
state references, evidence references, summary prose, confidence basis,
recommended action, and stated limitations — and returns the collapse codes the
answer commits. It never decides by file name or by trusting a fixture's
self-declared verdict.

Both the RealityGapBench scorer and the conformance harness call this same
detector, so a green conformance run reflects real engine behaviour. This is the
fix for the central audit finding (F-01): previously the conformance suite read
each fixture's own `expected_validation` block and so proved nothing about the
engine.

## Detector codes (RealityGapBench)

| Code | Collapse | Triggered when… |
|------|----------|-----------------|
| `declared_observed_collapse` | declared ≠ observed | declared and observed state refs are non-empty and identical |
| `claim_as_evidence` | claim ≠ evidence | an answer cites an evidence ref that is not a real evidence record for the case |
| `summary_source_collapse` | summary ≠ source | an answer cites a derived summary as evidence, or claims a gap with no declared/observed grounding |
| `completion_settlement_collapse` | completion ≠ settlement | "completed, therefore settled / no gap" |
| `ci_approval_collapse` | CI pass ≠ peer approval | a CI pass is treated as governance approval ("no gap because CI passed") |
| `possibility_affordance_collapse` | possibility ≠ affordance | "they can do it, so proceed" past a constraint |
| `authority_capability_collapse` | authority ≠ capability | execution treated as proof of authorization/capability |
| `unknown_as_false` / `missing_evidence_as_failure_proof` | unknown ≠ false | a failure is concluded from a missing record, without preserving that the record may exist elsewhere |
| `missing_evidence_as_no_gap` | missing evidence ≠ no gap | "no evidence was provided, so there is no gap" |
| `score_capability_collapse` / `single_success_capability_collapse` | score ≠ capability | capability is claimed from a benchmark score or a single success |
| `opposite_answer_with_high_confidence` | confidence ≠ correctness | a high-confidence answer asserts the opposite of the case's expected status |

The other families carry their own checks in their scorers:
`unsafe_authority_recommendation` (AuthorityBench false-allow),
`completion_settlement_collapse` (SettlementBench premature completion), and
`score_capability_collapse` / `possibility_affordance_collapse`
(CapabilityBench overclaim).

## Grounding (not a collapse, but related)

A RealityGapBench answer that claims a gap must reference both the declared and
the observed side in its `gap_summary`. If it does not, the result carries an
`ungrounded_reasoning` warning and is capped below `pass`. This stops a
label-correct answer with empty or irrelevant reasoning from scoring well —
representation ≠ reality, applied to the answer's own prose.

## Running the checks

```bash
uv run cep conformance anti-collapse
```

This runs:

1. the ten RealityGapBench anti-collapse fixtures
   (`conformance/fixtures/anti-collapse/reality-gap/`), each scored by the
   detector against its target case;
2. the cross-family invariants — every family's `example_invalid_answer` must
   produce a critical collapse failure, and every `example_valid_answer` must
   not.

A `PASS` line means the engine actually caught (or correctly cleared) the
answer. See [CEP-0010 Conformance](../spec/CEP-0010-conformance.md) for the
normative requirements and [Running the Benchmarks](running-benchmarks.md) for
the full command set.
