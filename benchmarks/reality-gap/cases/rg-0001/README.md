# rg-0001 — Certification Authority Drift

## Summary

This case evaluates whether a system can detect a gap between a declared certification requirement and observed operational execution.

The declared state says that only certified personnel may perform a controlled activity. The observed state shows that operations proceeded with personnel who had received partial training but had not been certified.

The benchmark tests whether the system preserves the distinction between:

- trained and certified,
- possible and permissible,
- completion and settlement,
- observed execution and authorized execution.

## Primary Question

Where does declared state diverge from observed state under the evaluation scope?

## Expected Result

The system should detect an authority drift gap.

## Expected Gap Status

`gap_detected`

## Expected Primary Gap Type

`authority_drift`

## Expected Severity

`high`

## Required Evidence

The answer should cite:

- the declared certification rule,
- the observed execution record,
- the staffing qualification record,
- and the communication gap record.

## Critical Failure Conditions

The answer should fail or receive severe penalty if it:

- treats partial training as certification,
- treats the fact that work occurred as proof that it was authorized,
- treats completion as settlement,
- treats missing evidence as proof of no gap,
- or ignores the declared/observed distinction.
RealityGapBench Case Pack — rg-0001

Case ID: rg-0001
Title: Certification Authority Drift
Benchmark Family: RealityGapBench
Version: 0.1
Difficulty: Easy
Domain: Operations Governance / Training Compliance
Primary Gap Type: authority_drift
Secondary Gap Types: role_gap, evidence_gap, affordance_gap

Directory Layout

benchmarks/reality-gap/cases/rg-0001/

├── README.md
├── case.cep.json
├── declared.md
├── observed.jsonl
├── answer_key.json
└── evidence/
    ├── ev-rg-0001-001.json
    ├── ev-rg-0001-002.json
    ├── ev-rg-0001-003.json
    └── ev-rg-0001-004.json


## Why This Invalid Answer Fails


1. It treats completion as settlement.
2. It treats observed execution as authorization.
3. It ignores the trained/certified distinction.
4. It cites no evidence.
5. It does not reference declared or observed state.
6. It gives high confidence without support.
7. It fails to identify the authority drift gap.


## Scoring Expectation


A strong answer should score approximately:

gap_status: 20 / 20
gap_type: 15 / 15
severity: 8-10 / 10
evidence: 15-20 / 20
anti_collapse: 15 / 15
recommended_next_action: 8-10 / 10
confidence_and_limitations: 8-10 / 10

A weak answer that notices “something is off” but does not cite evidence or preserve the authority distinction should receive partial credit.

An answer that says no gap exists because the work was completed should fail the case or receive near-zero score.


## Settlement Criteria for rg-0001


This case is settled when:

case.cep.json validates.
declared.md exists.
observed.jsonl exists.
All evidence records validate.
answer_key.json validates.
Valid example answer scores above 85.
Invalid example answer triggers critical failure.
Anti-collapse checks detect completion/settlement and possible/permissible collapse.

Next, the build path needs rg-0002 Process Drift and rg-0003 Evidence Gap so the first RealityGapBench dataset covers more than one kind of declared/observed divergence.