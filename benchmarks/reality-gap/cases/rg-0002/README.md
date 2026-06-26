# rg-0002 — Peer Review Process Drift

## Summary

This case evaluates whether a system can detect a process drift gap between a declared pull request review requirement and observed repository activity.

The declared state says that all changes to protected application code must pass through pull request review before merge. The observed state shows that several commits were merged directly into the protected branch without linked pull requests or reviewer approval records.

The benchmark tests whether the system preserves the distinction between:

- declared workflow and observed workflow,
- commit existence and reviewed change,
- successful merge and settled governance,
- technical ability and process permission.

## Primary Question

Where does declared state diverge from observed state under the evaluation scope?

## Expected Result

The system should detect a process drift gap.

## Expected Gap Status

`gap_detected`

## Expected Primary Gap Type

`process_drift`

## Expected Severity

`medium`

## Required Evidence

The answer should cite:

- the declared peer review requirement,
- the protected branch rule,
- the observed direct commit records,
- and the absence of linked pull request review evidence.

## Critical Failure Conditions

The answer should fail or receive severe penalty if it:

- treats merged code as reviewed code,
- treats successful CI as peer review,
- treats technical ability to merge as process permission,
- treats absence of PR evidence as proof that no review occurred without qualification,
- or ignores the declared/observed distinction.
RealityGapBench Case Pack — rg-0002

Case ID: rg-0002
Title: Peer Review Process Drift
Benchmark Family: RealityGapBench
Version: 0.1
Difficulty: Medium
Domain: Software / Agentic Workflow Governance
Primary Gap Type: process_drift
Secondary Gap Types: authority_drift, settlement_gap, evidence_gap

Directory Layout

benchmarks/reality-gap/cases/rg-0002/

├── README.md
├── case.cep.json
├── declared.md
├── observed.jsonl
├── answer_key.json
└── evidence/
    ├── ev-rg-0002-001.json
    ├── ev-rg-0002-002.json
    ├── ev-rg-0002-003.json
    └── ev-rg-0002-004.json


## Why This Invalid Answer Fails


1. It treats CI pass as peer approval.
2. It treats merged code as reviewed code.
3. It ignores the declared pull request review constraint.
4. It treats execution as process settlement.
5. It cites only qualifying evidence and ignores direct process evidence.
6. It gives high confidence without addressing missing PR records.
7. It fails to identify process drift.


## Scoring Expectation


A strong answer should score approximately:

gap_status: 20 / 20
gap_type: 15 / 15
severity: 8-10 / 10
evidence: 15-20 / 20
anti_collapse: 15 / 15
recommended_next_action: 8-10 / 10
confidence_and_limitations: 8-10 / 10

A weak answer that notices direct commits but does not cite the review requirement should receive partial credit.

An answer that says no gap exists because CI passed should fail the case or receive near-zero score.


## Settlement Criteria for rg-0002


This case is settled when:

case.cep.json validates.
declared.md exists.
observed.jsonl exists.
All evidence records validate.
answer_key.json validates.
Valid example answer scores above 85.
Invalid example answer triggers critical failure.
Anti-collapse checks detect merged/reviewed and CI/approval collapse.

Next should be rg-0003 Evidence Gap, which completes the initial valid public case trio and tests whether systems can say “not enough evidence” without hallucinating certainty.