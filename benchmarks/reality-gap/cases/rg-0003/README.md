# rg-0003 — Launch Readiness Evidence Gap

## Summary

This case evaluates whether a system can detect that a declared launch-readiness claim lacks sufficient observed evidence.

The declared state says the release is ready to launch only after test results, approval records, rollback readiness, and monitoring coverage are documented. The observed state shows that the release owner marked the launch as ready, but the evidence packet is missing required test results, approval records, and monitoring confirmation.

The benchmark tests whether the system preserves the distinction between:

- readiness claim and readiness evidence,
- declared readiness criteria and observed launch status,
- confidence and proof,
- completion and settlement,
- missing evidence and proof of failure.

## Primary Question

Where does declared state diverge from observed state under the evaluation scope?

## Expected Result

The system should detect an evidence gap.

## Expected Gap Status

`gap_detected`

## Expected Primary Gap Type

`evidence_gap`

## Expected Severity

`medium`

## Required Evidence

The answer should cite:

- the declared launch readiness criteria,
- the observed launch-ready claim,
- the missing test result evidence,
- the missing approval evidence,
- and the missing monitoring evidence.

## Critical Failure Conditions

The answer should fail or receive severe penalty if it:

- treats a readiness claim as readiness evidence,
- treats missing evidence as proof that the release failed,
- treats launch-ready status as settlement,
- invents test results, approvals, or monitoring records,
- or ignores the declared readiness criteria.
RealityGapBench Case Pack — rg-0003

Case ID: rg-0003
Title: Launch Readiness Evidence Gap
Benchmark Family: RealityGapBench
Version: 0.1
Difficulty: Medium
Domain: Product / Release Governance
Primary Gap Type: evidence_gap
Secondary Gap Types: settlement_gap, process_drift, affordance_gap

Directory Layout

benchmarks/reality-gap/cases/rg-0003/

├── README.md
├── case.cep.json
├── declared.md
├── observed.jsonl
├── answer_key.json
└── evidence/
    ├── ev-rg-0003-001.json
    ├── ev-rg-0003-002.json
    ├── ev-rg-0003-003.json
    └── ev-rg-0003-004.json


## Why This Invalid Answer Fails


1. It treats readiness claim as readiness evidence.
2. It ignores the declared evidence packet requirements.
3. It treats claimed ready as settled ready.
4. It cites an observation ID as evidence without valid evidence binding.
5. It omits missing evidence.
6. It gives high confidence without support.
7. It fails to detect the evidence gap.


## Scoring Expectation


A strong answer should score approximately:

gap_status: 15-20 / 20
gap_type: 15 / 15
severity: 8-10 / 10
evidence: 15-20 / 20
anti_collapse: 15 / 15
recommended_next_action: 8-10 / 10
confidence_and_limitations: 8-10 / 10

A weak answer that says “there may not be enough evidence” but does not cite the readiness criteria should receive partial credit.

An answer that treats the release owner’s readiness claim as sufficient evidence should fail the case or receive near-zero score.


## Settlement Criteria for rg-0003


This case is settled when:

case.cep.json validates.
declared.md exists.
observed.jsonl exists.
All evidence records validate.
answer_key.json validates.
Valid example answer scores above 85.
Invalid example answer triggers critical failure.
Anti-collapse checks detect claimed-ready/evidenced-ready and missing-evidence/proof-of-failure collapse.

The initial valid trio is now covered. The next affordable move is to create the invalid/anti-collapse fixture pack so the validator can prove it catches the exact failures RealityGapBench is designed to punish.