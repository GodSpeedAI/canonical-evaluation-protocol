RealityGapBench v0.1 — Benchmark Family Specification

Status: Draft
Category: Normative Benchmark Family
Version: 0.1
Protocol: Canonical Evaluation Protocol
Depends On:

CEP-0000 — Derivation Ladder and First Principles

CEP-0001 — Ontology

CEP-0002 — Representation Model

CEP-0003 — State Model

CEP-0004 — Transformation Model

CEP-0005 — Question Model

CEP-0006 — Evidence Model

CEP-0007 — Settlement Model

CEP-0008 — Semantic Envelope

CEP-0009 — Benchmark Model

CEP-0010 — Conformance

Repository Path: benchmarks/reality-gap/BENCHMARK.md

Abstract

RealityGapBench is a CEP benchmark family for evaluating whether a system can detect, classify, evidence, and explain divergence between declared reality and observed reality.

Declared reality is what a system, organization, process, policy, agent, benchmark, or actor says should be true, intended, required, permitted, prohibited, expected, or completed.

Observed reality is what appears to be true based on logs, traces, artifacts, interviews, audits, execution records, test results, monitoring signals, configuration snapshots, or other observations.

RealityGapBench evaluates whether a system can preserve the declared/observed distinction, identify meaningful divergence, bind evidence to gap claims, estimate severity, and recommend the next settlement-oriented move.

RealityGapBench does not reward generic summarization.

RealityGapBench does not reward confident speculation.

RealityGapBench rewards question-bound, evidence-backed gap detection.

1. Primary Question

RealityGapBench is organized around the primary Question:

Where does declared state diverge from observed state under the evaluation scope?

Every RealityGapBench case MUST preserve this Question or a case-specific refinement of it.

2. Purpose

RealityGapBench exists because agentic systems, organizations, workflows, and governance layers routinely fail at the same boundary:

what we say is true
vs
what is actually happening

The benchmark evaluates whether a system can identify this divergence without collapsing:

policy into practice,

plan into execution,

role into behavior,

authority into capability,

completion into settlement,

test pass into production safety,

documentation into operational reality,

declared state into observed state.

RealityGapBench is the first CEP benchmark family because it validates the most basic organizational cognition function:

Can the system see the difference between represented intention and represented actuality?

3. Benchmark Family Definition

A RealityGapBench family record MUST preserve:

family_id: RealityGapBench
family_version
cep_version
primary_question_ref
required_state_types
required_transformation_types
required_evidence_types
required_answer_shape
core_metrics
failure_modes
anti_collapse_rules

The canonical family identity is:

family_id: reality-gap
family_name: RealityGapBench
family_version: 0.1
cep_version: 0.1

4. Core Evaluation Target

RealityGapBench evaluates whether a system can:

preserve Declared State separately from Observed State,

identify whether a meaningful gap exists,

classify the gap,

cite evidence for the gap claim,

distinguish missing evidence from no gap,

distinguish unknown from false,

estimate severity,

identify affected constraints, distinctions, and relations,

avoid unsupported claims,

recommend a next move that would reduce representational error or support settlement.

5. Non-Goals

RealityGapBench v0.1 does not evaluate:

broad reasoning ability,

general summarization,

legal judgment,

moral judgment,

universal truth finding,

open-ended investigation,

production incident response,

final organizational diagnosis,

or capability across repeated settlements.

Those may be evaluated by later benchmark families or higher-level campaigns.

RealityGapBench v0.1 evaluates bounded declared-vs-observed divergence.

6. Required Case Structure

A RealityGapBench case MUST include:

case_id
case_version
family_ref
benchmark_ref
primary_question_ref
case_question_ref
declared_state_ref
observed_state_ref
input_envelope_ref OR input_context
evidence_refs OR evidence_requirements
expected_answer_shape
answer_key_ref
metric_refs
scoring_rules
invalidity_conditions
provenance_refs

A case SHOULD include:

scenario_description
domain
difficulty_level
gap_type
severity_key
hidden_context_refs
public_context_refs
known_omissions
known_uncertainties
redactions
review_status

7. Required Case Files

Each case directory SHOULD use the following structure:

cases/
└── rg-0001/
    ├── case.cep.json
    ├── declared.md
    ├── observed.jsonl
    ├── evidence/
    │   ├── evidence-0001.json
    │   └── evidence-0002.json
    ├── answer_key.json
    └── README.md

7.1 case.cep.json

Primary machine-readable case definition.

MUST include the case metadata, question, state references, expected answer shape, evidence requirements, metrics, and scoring rules.

7.2 declared.md

Human-readable declared state source.

Examples:

SOP excerpt,

role definition,

policy,

plan,

architecture statement,

workflow expectation,

project commitment,

authority model.

7.3 observed.jsonl

Observed records.

Each line SHOULD represent an observation, log event, trace, interview note, audit finding, execution record, or artifact record.

7.4 evidence/

Evidence records bound to gap claims or expected answer elements.

7.5 answer_key.json

Structured answer key.

MUST match the expected answer shape.

7.6 README.md

Human-readable case summary.

MUST NOT reveal hidden answer key details when the case is used for evaluation.

8. Declared State Requirements

A Declared State in RealityGapBench MUST preserve:

state_id
state_type: declared
subject_ref
representation_refs
scope
time_context
identity_refs OR identity_uncertainty
declared_condition
source
provenance_refs
confidence OR confidence_status

Declared State MAY be derived from:

policy
SOP
requirement
design_document
architecture_diagram
org_chart
role_definition
mission_statement
control_plan
contract
benchmark_spec
human_commitment

Declared State MUST remain distinct from Observed State.

9. Observed State Requirements

An Observed State in RealityGapBench MUST preserve:

state_id
state_type: observed
subject_ref
representation_refs
scope
time_context
identity_refs OR identity_uncertainty
observed_condition
observation_method
source
provenance_refs
confidence OR confidence_status
limitations

Observed State MAY be derived from:

logs
traces
monitoring_signals
test_results
audit_records
interviews
manual_inspection
execution_outputs
incident_reports
artifact_diffs
sensor_records
model_observations

Observed State MUST remain distinct from Declared State.

10. Gap Claim

A Gap Claim asserts that declared state and observed state diverge in a specific way.

10.1 Gap Claim Fields

A Gap Claim SHOULD preserve:

gap_claim_id
case_ref
question_ref
declared_state_ref
observed_state_ref
gap_detected
gap_type
gap_description
affected_constraints
affected_distinctions
affected_relations
evidence_refs
severity
confidence
limitations

10.2 Gap Claim Discipline

A gap claim MUST be evidence-targetable.

A gap claim without evidence or missing-evidence status is invalid.

11. Gap Detection Values

A RealityGapBench answer MUST classify whether a gap exists using one of:

gap_detected
no_gap_detected
insufficient_evidence
contradictory_evidence
out_of_scope
unknown

11.1 gap_detected

There is sufficient evidence that declared state and observed state diverge.

11.2 no_gap_detected

There is sufficient evidence that declared and observed state align for the evaluation question.

11.3 insufficient_evidence

Available evidence is not enough to determine gap status.

11.4 contradictory_evidence

Evidence conflicts materially and blocks confident gap classification.

11.5 out_of_scope

The available material does not fall within the case scope.

11.6 unknown

The system cannot determine status and cannot classify the reason more specifically.

12. Canonical Gap Types

RealityGapBench v0.1 MUST support the following gap types.

authority_drift
process_drift
role_gap
evidence_gap
settlement_gap
policy_conflict
semantic_drift
resource_gap
capability_gap
affordance_gap
identity_gap
temporal_gap
scope_gap
unknown

13. Gap Type Definitions

13.1 Authority Drift

Declared authority constraints differ from observed behavior.

Example:

Declared:
Only certified operators may perform the activity.

Observed:
Uncertified personnel performed the activity due to staffing shortage.

13.2 Process Drift

Declared workflow differs from observed workflow.

Example:

Declared:
All changes require peer review before merge.

Observed:
Several commits were merged directly to main.

13.3 Role Gap

Declared role ownership differs from observed responsibility or behavior.

Example:

Declared:
Operations representative communicates training requirements to the department.

Observed:
Operations team members were unaware of certification requirements.

13.4 Evidence Gap

Declared completion, compliance, or readiness lacks sufficient evidence.

Example:

Declared:
The project is ready for launch.

Observed:
No test results, approval records, or monitoring plan are available.

13.5 Settlement Gap

Declared completion differs from evidence-backed consequence registration.

Example:

Declared:
The agent completed the task.

Observed:
The file changed, but tests were not run and output was not verified.

13.6 Policy Conflict

Two or more declared states conflict.

Example:

Policy A permits direct approval by role X.
Policy B requires independent review by role Y.

13.7 Semantic Drift

Terms, categories, or meanings shift between declared and observed use.

Example:

Declared:
"Certified" means formally qualified by the certifier.

Observed:
"Trained" is being treated as "certified."

13.8 Resource Gap

Declared work assumes resources that are not observed to exist.

Example:

Declared:
A trained backup team supports the process.

Observed:
Only one trained person is available.

13.9 Capability Gap

Declared capability exceeds repeated settled performance under variation.

Example:

Declared:
The team can process this order type reliably.

Observed:
The process fails when two trained people are absent.

13.10 Affordance Gap

Declared option is not actually reachable, payable, permissible, executable, or settleable from current state.

Example:

Declared:
The team can proceed with processing.

Observed:
The required certified operators are unavailable and escalation path is undefined.

13.11 Identity Gap

Declared and observed states may not refer to the same subject.

Example:

Declared:
Training requirement applies to Line A.

Observed:
Evidence comes from Line B.

13.12 Temporal Gap

Declared and observed states apply to different time contexts.

Example:

Declared:
Policy version 3 applies after June 1.

Observed:
Execution followed policy version 2 after June 1.

13.13 Scope Gap

Declared and observed states apply to different scopes.

Example:

Declared:
Procedure applies to pilot orders only.

Observed:
Procedure is used for production orders.

14. Severity

RealityGapBench answers SHOULD estimate gap severity.

14.1 Severity Values

Severity SHOULD be one of:

none
low
medium
high
critical
unknown

14.2 Severity Basis

Severity SHOULD consider:

authority_exposure
safety_exposure
customer_exposure
regulatory_exposure
settlement_blockage
capability_overclaim
affordance_misrepresentation
reversibility
scope
frequency
confidence

14.3 Severity Failure

A severity estimate without basis SHOULD be penalized.

A system SHOULD NOT assign high severity merely because a gap exists.

15. Difficulty Levels

RealityGapBench cases SHOULD be labeled by difficulty.

easy
medium
hard
adversarial
unknown

15.1 Easy

Single clear gap, explicit declared state, explicit observed contradiction, direct evidence.

15.2 Medium

Gap requires comparing multiple records or recognizing missing evidence.

15.3 Hard

Gap requires preserving scope, time, identity, authority, or semantic distinction across multiple records.

15.4 Adversarial

Case includes tempting collapse, misleading evidence, ambiguous terminology, hidden scope shift, or plausible but unsupported claim.

16. Required Answer Shape

A RealityGapBench answer MUST conform to this structure:

answer_id
case_ref
gap_status
gap_type
severity
gap_summary
declared_state_refs
observed_state_refs
affected_constraints
affected_distinctions
affected_relations
evidence_refs
missing_evidence
contradictions
confidence
recommended_next_action
limitations

16.1 Required Field Semantics

gap_status

MUST be one of:

gap_detected
no_gap_detected
insufficient_evidence
contradictory_evidence
out_of_scope
unknown

gap_type

MUST be one of the canonical gap types or a profile-declared extension.

If gap_status is not gap_detected, gap_type MAY be unknown or not_applicable.

severity

MUST be one of the declared severity values.

gap_summary

A short explanation of the divergence.

declared_state_refs

References to declared state elements used in the answer.

observed_state_refs

References to observed state elements used in the answer.

affected_constraints

Constraints implicated by the gap.

affected_distinctions

Distinctions required to understand the gap.

affected_relations

Relations implicated by the gap.

evidence_refs

Evidence records supporting, weakening, or qualifying the gap claim.

missing_evidence

Evidence that would be required for stronger settlement.

contradictions

Known contradictions that affect confidence.

confidence

Confidence in the answer.

recommended_next_action

A settlement-oriented next move.

limitations

Known limitations of the answer.

17. Recommended Next Action

RealityGapBench answers MUST recommend a next action when a gap is detected or evidence is insufficient.

The next action MUST be settlement-oriented.

It SHOULD reduce representational error, gather evidence, repair drift, escalate authority, update state, or define a missing owner.

17.1 Valid Next Action Types

collect_evidence
escalate_authority
update_declared_state
repair_observed_process
clarify_role
resolve_policy_conflict
define_certification_boundary
run_audit
create_settlement_threshold
block_transformation
continue_monitoring
no_action_required
unknown

17.2 Next Action Failure

A vague recommendation such as “improve communication” SHOULD be penalized unless it is translated into a specific transformation.

A destination without a spendable path is not a valid next action.

18. Evidence Requirements

RealityGapBench requires evidence binding.

A valid answer MUST cite evidence or explicitly mark missing evidence.

18.1 Required Evidence Fields

Evidence records SHOULD preserve:

evidence_id
evidence_type
question_ref
target_claim_ref
representation_ref
source
provenance_refs
relevance
reliability
direction
confidence_impact
timestamp
scope
limitations

18.2 Admissible Evidence Types

RealityGapBench v0.1 SHOULD admit:

policy_reference
document
execution_log
trace
audit_record
monitoring_signal
test_result
configuration_snapshot
artifact_diff
human_attestation
manual_inspection
external_record

18.3 Evidence Failure

An answer that identifies the correct gap but cites no evidence SHOULD receive partial credit at most.

An answer that cites irrelevant evidence SHOULD be penalized.

An answer that fabricates evidence SHOULD fail the case.

19. Metrics

RealityGapBench v0.1 SHOULD include the following metrics.

gap_detection_accuracy
gap_type_accuracy
severity_accuracy
evidence_precision
evidence_recall
anti_collapse_score
unsupported_claim_rate
recommended_action_quality
confidence_calibration
invalid_answer_rate

20. Metric Definitions

20.1 Gap Detection Accuracy

Measures whether the system correctly determines gap status.

20.2 Gap Type Accuracy

Measures whether the system classifies the gap correctly.

20.3 Severity Accuracy

Measures whether the severity estimate matches the answer key or accepted range.

20.4 Evidence Precision

Measures whether cited evidence is actually relevant.

20.5 Evidence Recall

Measures whether the answer cites required evidence.

20.6 Anti-Collapse Score

Measures whether the answer preserves required CEP distinctions.

20.7 Unsupported Claim Rate

Measures how often the answer makes claims without evidence.

20.8 Recommended Action Quality

Measures whether the recommendation is specific, reachable, and settlement-oriented.

20.9 Confidence Calibration

Measures whether confidence is appropriate given evidence quality and uncertainty.

20.10 Invalid Answer Rate

Measures how often responses fail required answer shape.

21. Scoring Overview

RealityGapBench v0.1 SHOULD use a 100-point scoring model.

Recommended allocation:

gap_status: 20
gap_type: 15
severity: 10
evidence: 20
anti_collapse: 15
recommended_next_action: 10
confidence_and_limitations: 10

Benchmark profiles MAY adjust scoring, but MUST preserve scoring rules.

22. Scoring Detail

22.1 Gap Status — 20 Points

20 = correct status
10 = partially correct status
0  = incorrect status

Example:

Correctly says gap_detected: 20

Says insufficient_evidence when answer key allows weak but present evidence: 10

Says no_gap_detected when gap exists: 0

22.2 Gap Type — 15 Points

15 = correct primary gap type
10 = correct family of gap but wrong subtype
5  = secondary but plausible gap type
0  = wrong or unsupported gap type

22.3 Severity — 10 Points

10 = correct severity or accepted range
5  = adjacent severity
0  = unsupported or wrong severity

22.4 Evidence — 20 Points

Suggested split:

10 = cites required evidence
5  = evidence relevance
5  = evidence reliability / limitations handled

22.5 Anti-Collapse — 15 Points

Deduct for protected distinction collapse.

Critical collapses may zero the case.

Protected distinctions include:

declared / observed
claim / evidence
completion / settlement
authority / capability
possible / permissible
unknown / false
summary / source

22.6 Recommended Next Action — 10 Points

10 = specific, reachable, settlement-oriented
5  = directionally useful but under-specified
0  = vague, unreachable, or unsupported

22.7 Confidence and Limitations — 10 Points

5 = confidence appropriate to evidence
5 = limitations and unknowns preserved

23. Critical Failure Conditions

A RealityGapBench answer SHOULD receive zero or invalid status if it commits any critical failure.

Critical failures:

fabricated_evidence
declared_observed_collapse
completion_settlement_collapse
claim_as_evidence
unknown_as_false
opposite_answer_with_high_confidence
unsafe_authority_recommendation
answer_shape_invalid
out_of_scope_answer

A benchmark profile MAY define whether critical failure produces zero score or invalid result.

24. Answer Key Structure

An answer key MUST preserve:

answer_key_id
case_ref
question_ref
expected_gap_status
accepted_gap_statuses
expected_gap_types
accepted_gap_types
expected_severity
accepted_severity_range
required_evidence_refs
optional_evidence_refs
required_affected_constraints
required_affected_distinctions
required_affected_relations
accepted_next_actions
partial_credit_rules
critical_failure_conditions
confidence_expectations
provenance_refs

25. Minimal answer_key.json Shape

{
  "answer_key_id": "ak-rg-0001",
  "case_ref": "rg-0001",
  "question_ref": "q-rg-primary",
  "expected_gap_status": "gap_detected",
  "accepted_gap_statuses": ["gap_detected"],
  "expected_gap_types": ["authority_drift"],
  "accepted_gap_types": ["authority_drift", "role_gap"],
  "expected_severity": "high",
  "accepted_severity_range": ["medium", "high"],
  "required_evidence_refs": ["ev-rg-0001-001", "ev-rg-0001-002"],
  "optional_evidence_refs": [],
  "required_affected_constraints": ["certification_required"],
  "required_affected_distinctions": ["trained/certified", "possible/permissible"],
  "required_affected_relations": ["actor_performed_activity_without_certification"],
  "accepted_next_actions": [
    "escalate_authority",
    "block_transformation",
    "define_certification_boundary",
    "collect_evidence"
  ],
  "critical_failure_conditions": [
    "declared_observed_collapse",
    "claim_as_evidence",
    "unknown_as_false"
  ]
}

26. Minimal case.cep.json Shape

{
  "case_id": "rg-0001",
  "case_version": "0.1",
  "family_ref": "reality-gap",
  "benchmark_ref": "RealityGapBench-v0.1",
  "primary_question_ref": "q-rg-primary",
  "case_question_ref": "q-rg-0001",
  "difficulty_level": "easy",
  "domain": "operations_governance",
  "declared_state_ref": "state-declared-rg-0001",
  "observed_state_ref": "state-observed-rg-0001",
  "expected_answer_shape_ref": "shape-rg-v0.1",
  "answer_key_ref": "ak-rg-0001",
  "metric_refs": [
    "gap_detection_accuracy",
    "gap_type_accuracy",
    "severity_accuracy",
    "evidence_precision",
    "evidence_recall",
    "anti_collapse_score",
    "recommended_action_quality",
    "confidence_calibration"
  ],
  "evidence_requirements": {
    "required": true,
    "minimum_relevance": "moderately_relevant",
    "minimum_reliability": "moderate"
  },
  "invalidity_conditions": [
    "answer_shape_invalid",
    "fabricated_evidence",
    "declared_observed_collapse"
  ],
  "provenance_refs": ["prov-rg-0001"]
}

27. Case Generation Rules

RealityGapBench cases MAY be manually authored, generated, or derived from logs, policies, interviews, audits, or traces.

Generated cases MUST be marked as generated and reviewed before acceptance.

27.1 Generation Record

A generated case SHOULD preserve:

generation_id
generator_ref
generation_method
source_refs
seed
constraints_used
target_gap_type
target_difficulty
human_review_status
validation_status
known_limitations

27.2 Accepted Case Requirements

A case MUST NOT be accepted into the benchmark dataset unless:

declared state is present
observed state is present
case question is present
answer key is present
evidence requirements are present
expected answer shape is present
scoring rules are present
provenance is present
human review status is accepted or not_required

28. Minimum v0 Dataset

RealityGapBench v0.1 SHOULD launch with at least:

3 valid public cases
3 invalid public cases
3 anti-collapse cases

28.1 Valid Case Targets

Initial valid cases SHOULD include:

rg-0001 authority_drift
rg-0002 process_drift
rg-0003 evidence_gap

28.2 Invalid Case Targets

Initial invalid cases SHOULD include:

rg-invalid-0001 missing_declared_state
rg-invalid-0002 missing_answer_key
rg-invalid-0003 missing_evidence_requirements

28.3 Anti-Collapse Case Targets

Initial anti-collapse cases SHOULD include:

rg-ac-0001 declared_observed_collapse
rg-ac-0002 claim_as_evidence
rg-ac-0003 unknown_as_false

29. Baseline Systems

RealityGapBench SHOULD define baseline systems.

Initial baselines:

random_baseline
keyword_baseline
summary_only_baseline
simple_rule_baseline
human_reviewer_baseline

29.1 Random Baseline

Randomly assigns gap status and type.

29.2 Keyword Baseline

Uses keyword matching between declared and observed records.

29.3 Summary-Only Baseline

Summarizes inputs and attempts to infer gap without structured evidence binding.

29.4 Simple Rule Baseline

Uses hand-written rules for common gap patterns.

29.5 Human Reviewer Baseline

Human-reviewed answer set.

Human reviewer baseline MUST preserve review method, reviewer criteria, and evidence references.

30. Runner Requirements

A RealityGapBench runner MUST:

load case definitions,

validate case structure,

provide declared and observed context to the system under evaluation,

preserve primary and case Questions,

collect answer,

validate answer shape,

verify evidence references,

score answer using declared scoring rules,

emit errors and warnings,

produce benchmark result envelope,

produce conformance report.

31. Result Record

A RealityGapBench result MUST preserve:

result_id
benchmark_ref
case_ref
system_ref
runner_ref
adapter_ref
answer_ref
score_refs
gap_status_score
gap_type_score
severity_score
evidence_score
anti_collapse_score
next_action_score
confidence_score
total_score
errors
warnings
conformance_status
created_at
provenance_refs

32. Result Status

A RealityGapBench result status SHOULD be one of:

scored
partially_scored
invalid_answer
invalid_case
runner_error
adapter_error
not_evaluable
unknown

33. Result Envelope

RealityGapBench results SHOULD be carried as Semantic Envelopes.

A result envelope MUST preserve:

envelope_kind: benchmark_result
benchmark_ref
family_ref
case_ref
system_ref
runner_ref
adapter_ref
answer_ref
score_refs
evidence_refs
errors
warnings
conformance_status
run_metadata
provenance_refs

34. Reporting Requirements

A RealityGapBench report SHOULD include:

benchmark version
dataset version
system under evaluation
runner version
adapter version
case count
overall score
metric scores
gap detection accuracy
gap type accuracy
evidence precision
evidence recall
anti-collapse score
unsupported claim rate
invalid answer rate
errors
warnings
known limitations

The report MUST NOT claim capability from a single benchmark run.

The report MAY say:

This result provides evidence relevant to capability evaluation.

The report MUST NOT say:

This system has the capability.

unless repeated settlement under variation has been evaluated separately.

35. Conformance Requirements

A RealityGapBench implementation MUST conform to:

CEP-Benchmark
CEP-Question
CEP-State
CEP-Evidence
CEP-Result

If using Semantic Envelopes, it MUST also conform to:

CEP-Envelope

If running automated evaluation, it SHOULD conform to:

CEP-Runner
CEP-Adapter

36. Validation Requirements

A RealityGapBench validator MUST check:

case has primary question
case has declared state
case has observed state
case preserves declared/observed separation
case has answer key
case has expected answer shape
case has scoring rules
case has evidence requirements
answer matches answer shape
answer cites valid evidence refs when required
answer does not fabricate evidence
answer does not collapse declared and observed
result preserves provenance
result preserves errors and warnings

37. Anti-Collapse Rules

RealityGapBench implementations SHALL NOT collapse:

declared state into observed state
observed state into declared state
policy into practice
plan into execution
role into behavior
claim into evidence
data into evidence
completion into settlement
authority into capability
possibility into affordance
unknown into false
missing evidence into no gap
summary into source
score into capability
benchmark result into settled truth

Violation of these anti-collapse rules SHOULD produce validation errors or scoring penalties.

38. Invalid Answer Conditions

A RealityGapBench answer is invalid if:

it does not match expected answer shape,

it fabricates evidence,

it references nonexistent evidence,

it collapses declared and observed state,

it treats missing evidence as proof of no gap,

it treats claim as evidence for itself,

it treats unknown as false,

it answers outside case scope,

it omits gap status,

or it cannot identify the declared and observed state basis for its answer.

Invalid answers MAY be stored.

Invalid answers MUST NOT receive full scoring.

39. Invalid Case Conditions

A RealityGapBench case is invalid if:

it lacks declared state,

it lacks observed state,

it lacks Question,

it lacks answer key or oracle,

it lacks expected answer shape,

it lacks scoring rules,

it lacks evidence requirements,

it lacks provenance,

it hides material assumptions,

or it collapses declared and observed state in the case itself.

40. Example Case Summary

Case rg-0001 — Certification Authority Drift

Declared State

Only certified team members may perform a controlled activity.

Training is not equivalent to certification.

Operations representative is responsible for communicating staffing readiness to the broader operations group.

Observed State

Due to two trained staff being unavailable, operations proceeded using additional personnel who had received partial training but had not been certified.

The project team was not notified that more certified personnel were needed.

Expected Gap

gap_status: gap_detected
gap_type: authority_drift
severity: high

Required Evidence

declared certification rule
observed work execution record
staff qualification record
communication or absence-of-communication record

Accepted Next Actions

block_transformation
escalate_authority
define_certification_boundary
collect_evidence
clarify_role

41. Example Answer

{
  "answer_id": "ans-rg-0001-example",
  "case_ref": "rg-0001",
  "gap_status": "gap_detected",
  "gap_type": "authority_drift",
  "severity": "high",
  "gap_summary": "The declared state requires certified personnel for the controlled activity, but the observed state shows operations proceeded with personnel who had partial training but were not certified.",
  "declared_state_refs": ["state-declared-rg-0001"],
  "observed_state_refs": ["state-observed-rg-0001"],
  "affected_constraints": ["certification_required"],
  "affected_distinctions": ["trained/certified", "possible/permissible"],
  "affected_relations": ["actor_performed_activity_without_required_certification"],
  "evidence_refs": ["ev-rg-0001-001", "ev-rg-0001-002"],
  "missing_evidence": ["complete staffing roster for execution window"],
  "contradictions": [],
  "confidence": {
    "value": "high",
    "basis": "Declared certification rule and observed staffing record directly support the gap claim."
  },
  "recommended_next_action": {
    "type": "escalate_authority",
    "description": "Pause or escalate the activity until certification authority confirms whether partially trained personnel may perform the work and records the decision."
  },
  "limitations": [
    "The full staffing roster for the execution window is not available."
  ]
}

42. Example Invalid Answer

{
  "answer_id": "ans-rg-0001-invalid",
  "case_ref": "rg-0001",
  "gap_status": "no_gap_detected",
  "gap_type": "unknown",
  "severity": "none",
  "gap_summary": "The work was completed, so the process was acceptable.",
  "declared_state_refs": [],
  "observed_state_refs": [],
  "affected_constraints": [],
  "affected_distinctions": [],
  "affected_relations": [],
  "evidence_refs": [],
  "missing_evidence": [],
  "contradictions": [],
  "confidence": {
    "value": "high",
    "basis": "The operation completed."
  },
  "recommended_next_action": {
    "type": "no_action_required",
    "description": "No action is needed."
  },
  "limitations": []
}

This answer is invalid because it collapses completion into settlement, ignores the certification distinction, cites no evidence, and treats observed execution as authorization.

43. Minimum v0.1 Settlement

RealityGapBench v0.1 is settled when:

BENCHMARK.md exists
METRICS.md exists
CASE_SCHEMA.md exists
expected answer shape exists
minimum 3 valid cases exist
minimum 3 invalid cases exist
minimum 3 anti-collapse cases exist
answer keys validate
runner can load and score cases
result envelope is emitted
conformance report is emitted
sample report is generated

RealityGapBench v0.1 is not settled if:

cases lack declared state
cases lack observed state
cases lack evidence requirements
answers can score fully without evidence
declared and observed collapse
runner produces score without provenance
reports imply capability from one run

44. Closing Definition

RealityGapBench evaluates whether a system can detect, classify, evidence, and explain the gap between declared reality and observed reality.

It is not a summarization benchmark.

It is not a generic reasoning benchmark.

It is not a compliance checklist.

It is a benchmark for represented divergence under question-bound evidence.

RealityGapBench is the first executable proof of CEP because it tests the basic cognitive operation every governed agentic organization needs:

Can the system see where what we say is true is no longer what is happening?

The next useful artifact is the first concrete case pack: rg-0001 Certification Authority Drift, including case.cep.json, declared.md, observed.jsonl, evidence records, and answer_key.json.