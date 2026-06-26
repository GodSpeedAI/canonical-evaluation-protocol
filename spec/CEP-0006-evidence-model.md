CEP-0006 — Evidence Model

Status: Draft
Category: Normative
Version: 0.1
Protocol: Canonical Evaluation Protocol
Depends On:

CEP-0000 — Derivation Ladder and First Principles

CEP-0001 — Ontology

CEP-0002 — Representation Model

CEP-0003 — State Model

CEP-0004 — Transformation Model

CEP-0005 — Question Model

Document Type: Foundational Specification

Abstract

This document defines the CEP Evidence Model.

CEP evaluates represented transformations through evidence-backed settlement. Evidence is the bridge between observation and justified state update.

Evidence is not raw data.

Evidence is not merely a document, log, test, trace, artifact, human statement, or model output.

Evidence is a representation that changes confidence in a claim relative to a question.

The Evidence Model defines how evidence is represented, targeted, typed, sourced, evaluated, contradicted, weighted, invalidated, and used to support settlement, authority, Reality Gap, capability, affordance, and benchmark evaluation.

1. Purpose

The purpose of the Evidence Model is to prevent CEP implementations from treating available information as automatically evidential.

A representation becomes evidence only when it is related to:

a Question,

a Claim,

a target State, Transformation, Relation, Constraint, Invariant, Settlement, Affordance, Capability, or Benchmark result,

a relevance rule,

a reliability assessment,

and a confidence impact.

Evidence separates assertion from support.

Without evidence, CEP cannot distinguish:

claimed completion from settled consequence,

model output from verified observation,

self-report from independent confirmation,

policy text from authority decision,

data from proof,

and plausible narrative from supported evaluation.

2. Scope

This document defines:

evidence definition,

evidence sufficiency,

evidence identity,

evidence target binding,

evidence types,

evidence source and provenance,

evidence relevance,

evidence reliability,

evidence direction,

evidence strength,

evidence admissibility,

evidence confidence impact,

contradiction handling,

corroboration,

evidence lifecycle,

evidence operations,

evidence validity,

conformance,

and anti-collapse rules.

This document does not define:

final scoring algorithms,

universal statistical confidence calculus,

benchmark-specific evidence weights,

settlement thresholds,

Semantic Envelope serialization,

or runner implementation.

Those are defined in later CEP specifications.

3. Core Definition

Evidence is a Representation that changes confidence in a Claim relative to a Question.

Evidence MUST have:

question_ref
claim_ref OR target_invariant_ref OR target_entity_ref
representation_ref
source
provenance
relevance
reliability
direction
confidence_impact

Evidence MAY support, weaken, contradict, qualify, or fail to affect a Claim.

Evidence MUST NOT be treated as truth.

Evidence updates confidence.

Settlement determines whether available evidence is sufficient for consequence-backed state update.

4. Evidence Is Not Data

CEP SHALL distinguish Data from Evidence.

4.1 Data

Data is represented material that may or may not bear on a Question or Claim.

Examples:

raw logs,

raw traces,

screenshots,

database records,

policy documents,

model outputs,

emails,

human statements,

test artifacts,

monitoring signals.

4.2 Evidence

Evidence is data made relevant to a Question and Claim.

Example:

Data:
A CI log showing 42 tests passed.

Question:
Did the code transformation satisfy the required test invariant?

Claim:
The transformation passed the required test suite.

Evidence:
The CI log supports the claim, subject to source reliability and scope.

4.3 Anti-Collapse Rule

A CEP implementation MUST NOT treat data as evidence unless the Question, Claim, relevance, reliability, and direction are explicit or derivable.

5. Evidence Is Not Claim

CEP SHALL distinguish Claim from Evidence.

5.1 Claim

A Claim asserts something.

Example:

"The deployment completed successfully."

5.2 Evidence

Evidence bears on whether the Claim should be believed, weakened, qualified, contradicted, or treated as unsupported.

Example:

Deployment log.
Monitoring signal.
Rollback record.
Incident report.
Approval record.
Test result.

5.3 Anti-Collapse Rule

A Claim MUST NOT be treated as evidence for itself.

Self-attestation MAY be evidence only when the evaluation context admits attestation as evidence and marks its reliability accordingly.

6. Evidence Sufficiency

Evidence is sufficient when it preserves enough structure to affect evaluation.

6.1 Required Evidence Fields

A CEP-compatible Evidence record MUST preserve:

evidence_id
evidence_type
question_ref
target_claim_ref OR target_entity_ref
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

6.2 Conditional Evidence Fields

An Evidence record SHOULD preserve the following when materially relevant:

chain_of_custody
collection_method
observer_ref
perspective_ref
authority_context
admissibility_status
integrity_record
freshness_record
independence_record
corroboration_refs
contradiction_refs
confidence_basis
weight
review_status

6.3 Evidence-Sufficiency Failure

An Evidence record is not CEP-valid if it lacks a target Claim, target entity, or target invariant.

An Evidence record is not benchmark-valid if it lacks a Question.

An Evidence record is not settlement-valid if it lacks provenance, relevance, reliability, and confidence impact.

7. Evidence Identity

Evidence MUST have identity.

Evidence identity allows CEP to distinguish:

original evidence from derived evidence,

source artifact from evidence record,

evidence version from evidence interpretation,

duplicate evidence from independent corroboration,

stale evidence from current evidence,

and tampered evidence from intact evidence.

7.1 Evidence Identity Record

An Evidence identity record SHOULD preserve:

evidence_id
version
representation_ref
source_ref
content_hash
semantic_hash
created_at
collected_at
observed_at
updated_at
lineage_refs
supersedes
superseded_by

7.2 Identity Failure

If Evidence identity is absent, CEP cannot determine whether two evidence records are independent, duplicated, stale, modified, superseded, or corrupted.

8. Evidence Target

Evidence MUST target something.

The target determines what confidence is being updated.

8.1 Evidence Target Types

Evidence MAY target:

claim
state
transformation
constraint
distinction
relation
observation
authority_decision
invariant
settlement
affordance
capability
benchmark_result
conformance_result

8.2 Target Binding Record

An Evidence target binding SHOULD preserve:

evidence_ref
target_type
target_ref
question_ref
claim_ref when applicable
relation_to_target
confidence_impact
limitations

8.3 Target Failure

Evidence without target binding is uninterpretable.

A log, policy, trace, or statement may be useful, but it is not CEP-valid evidence until its target is known.

9. Evidence Question Binding

Evidence exists relative to a Question.

The same Representation may be evidence for one Question and irrelevant to another.

9.1 Question Binding Record

Evidence SHOULD preserve:

question_ref
question_type
relevance_rule_refs
answer_shape_ref
evaluation_context

9.2 Example

A passing test result may support:

"Did the transformation preserve the test invariant?"

but may not support:

"Was the transformation authorized?"

9.3 Question Binding Failure

If Question binding is absent, CEP cannot determine why a Representation counts as Evidence.

10. Evidence Types

CEP recognizes the following top-level Evidence types.

execution_log
test_result
audit_record
monitoring_signal
trace
document
policy_reference
human_attestation
model_output
configuration_snapshot
artifact_diff
external_record
manual_inspection
sensor_record
approval_record
access_record
incident_record
benchmark_result
conformance_result
unknown

Implementations MAY define domain-specific evidence subtypes.

Domain-specific subtypes MUST map to one or more CEP top-level Evidence types.

11. Evidence Source

Evidence MUST preserve source.

Source identifies where the Representation came from.

11.1 Source Record

An Evidence source record SHOULD preserve:

source_id
source_type
source_ref
source_owner
source_system
source_method
created_at
collected_at
accessed_at
source_scope
source_limitations

11.2 Source Types

CEP recognizes:

human
agent
system
tool
log_store
test_runner
monitoring_system
audit_system
repository
document_store
database
external_service
sensor
benchmark_runner
model
unknown

11.3 Source Failure

If source is absent, evidence reliability cannot be evaluated.

Evidence without source MUST be treated as unsupported for settlement unless the benchmark explicitly tests unknown-source reasoning.

12. Provenance

Evidence MUST preserve provenance.

Provenance describes how the Evidence was produced, collected, transformed, reviewed, or derived.

12.1 Provenance Record

An Evidence provenance record SHOULD preserve:

provenance_id
source_ref
collection_method
collector_ref
production_method
derived_from
transformation_refs
tool_refs
model_refs
human_refs
review_status
verification_status
timestamp

12.2 Derived Evidence

Derived Evidence is Evidence produced by transformation of prior evidence or representation.

Examples:

summarized logs,

normalized traces,

extracted policy rule,

model-generated classification,

compiled evidence packet,

benchmark score.

Derived Evidence MUST preserve lineage to source evidence.

12.3 Provenance Failure

If provenance is absent, CEP cannot distinguish original source from interpretation, summary, extraction, or model-generated inference.

13. Chain of Custody

Chain of custody records control, access, movement, and modification of evidence.

A chain of custody record is REQUIRED when evidence integrity materially affects evaluation.

13.1 Chain of Custody Record

A chain of custody record SHOULD preserve:

custody_id
evidence_ref
holder_refs
access_events
modification_events
transfer_events
integrity_checks
signature_refs
tamper_status

13.2 Tamper Status

Tamper status SHOULD be one of:

intact
modified
tampered
unknown
not_applicable

13.3 Custody Failure

If chain of custody is required but absent, evidence SHOULD NOT be used for high-stakes settlement or authority decisions.

14. Evidence Integrity

Evidence integrity describes whether evidence content is preserved without unauthorized modification.

14.1 Integrity Record

An integrity record SHOULD preserve:

content_hash
signature
verification_method
verification_status
tamper_status
checked_at
checker_ref

14.2 Verification Status

Verification status SHOULD be one of:

verified
unverified
failed
unknown
not_applicable

14.3 Integrity Failure

If evidence integrity is unknown, CEP MAY still use the evidence, but confidence impact MUST reflect uncertainty.

15. Evidence Relevance

Relevance describes how Evidence bears on a Question and Claim.

15.1 Relevance Record

An Evidence relevance record SHOULD preserve:

relevance_value
relevance_scale
relevance_basis
question_ref
claim_ref
target_entity_ref
limitations

15.2 Relevance Scale

Implementations MAY use numeric, ordinal, or categorical relevance scales.

The scale MUST be declared.

Examples:

irrelevant
weakly_relevant
moderately_relevant
strongly_relevant
decisive
unknown

15.3 Relevance Failure

Evidence with unknown relevance MAY be stored.

It MUST NOT be used for settlement unless admissible under the evaluation context.

16. Evidence Reliability

Reliability describes how much the Evidence source, method, integrity, and provenance should be trusted for the target Question.

16.1 Reliability Record

An Evidence reliability record SHOULD preserve:

reliability_value
reliability_scale
reliability_basis
source_quality
method_quality
integrity_status
provenance_quality
independence_status
known_limitations

16.2 Reliability Scale

Implementations MAY use numeric, ordinal, or categorical reliability scales.

The scale MUST be declared.

Examples:

unreliable
weak
moderate
strong
verified
unknown

16.3 Reliability Failure

Evidence with low reliability may still affect confidence, but it SHOULD NOT independently settle a claim unless the evaluation context explicitly allows it.

17. Evidence Direction

Evidence direction describes how Evidence affects a Claim.

17.1 Direction Values

Evidence direction MUST be one of:

supports
weakens
contradicts
qualifies
irrelevant
unknown

17.2 Direction Discipline

Direction is claim-relative.

The same Evidence may support one Claim and contradict another.

17.3 Direction Failure

If direction is absent, confidence impact cannot be interpreted.

Evidence without direction is not settlement-valid.

18. Confidence Impact

Confidence impact describes how Evidence changes confidence in a target Claim, State, Transformation, Invariant, Settlement, Affordance, Capability, or Benchmark result.

CEP does not require one universal confidence calculus in this document.

However, confidence impact MUST be represented when Evidence is used for evaluation.

18.1 Confidence Impact Record

A confidence impact record SHOULD preserve:

prior_confidence
impact_direction
impact_magnitude
posterior_confidence
confidence_scale
calculation_method
confidence_basis
limitations

18.2 Impact Direction

Impact direction SHOULD be one of:

increase
decrease
qualify
no_change
unknown

18.3 Confidence Failure

A confidence impact without declared scale or basis is invalid for benchmark comparison.

Confidence impact MUST NOT be treated as certainty.

19. Evidence Strength

Evidence strength is the combined effect of relevance, reliability, direction, independence, freshness, and confidence impact.

CEP does not define a universal strength formula here.

However, if strength is used, the calculation method MUST be declared.

19.1 Strength Record

An evidence strength record SHOULD preserve:

strength_value
strength_scale
strength_basis
relevance_ref
reliability_ref
confidence_impact_ref
freshness_ref
independence_ref
corroboration_refs
calculation_method

19.2 Strength Failure

Evidence strength without calculation basis is not benchmark-valid.

20. Evidence Freshness

Freshness describes whether Evidence remains temporally valid for the Question.

20.1 Freshness Record

A freshness record SHOULD preserve:

evidence_ref
observed_at
valid_from
valid_until
staleness_threshold
freshness_status
time_uncertainty

20.2 Freshness Status

Freshness status SHOULD be one of:

fresh
stale
expired
unknown
not_applicable

20.3 Freshness Failure

Stale Evidence may remain historically valid while being invalid for current settlement.

21. Evidence Independence

Independence describes whether Evidence provides non-duplicative support.

21.1 Independence Record

An independence record SHOULD preserve:

evidence_ref
related_evidence_refs
independence_status
shared_source_refs
shared_method_refs
dependency_reason
confidence

21.2 Independence Status

Independence status SHOULD be one of:

independent
partially_independent
dependent
duplicate
unknown
not_applicable

21.3 Independence Failure

Multiple evidence records from the same source or method MUST NOT be treated as independent corroboration unless independence is established.

22. Corroboration

Corroboration occurs when multiple Evidence records support the same Claim, State, Transformation, Invariant, or Settlement through sufficiently independent sources or methods.

22.1 Corroboration Record

A corroboration record SHOULD preserve:

corroboration_id
target_claim_ref
evidence_refs
independence_assessment
combined_relevance
combined_reliability
combined_confidence_impact
limitations

22.2 Corroboration Failure

Corroboration is invalid if all Evidence records depend on the same unverified source and no dependency is marked.

23. Contradiction

Contradiction occurs when Evidence conflicts with a Claim, another Evidence record, a State, a Transformation, an Invariant, or a Settlement.

23.1 Contradiction Record

A contradiction record SHOULD preserve:

contradiction_id
evidence_refs
target_refs
contradiction_type
description
severity
resolution_status
impact_on_confidence
impact_on_settlement

23.2 Contradiction Types

CEP recognizes:

claim_contradiction
state_contradiction
transformation_contradiction
authority_contradiction
settlement_contradiction
capability_contradiction
affordance_contradiction
benchmark_contradiction
source_contradiction
temporal_contradiction
identity_contradiction
semantic_contradiction

23.3 Resolution Status

Resolution status SHOULD be one of:

unresolved
partially_resolved
resolved
accepted_conflict
dismissed
unknown

23.4 Contradiction Failure

Known contradictions MUST NOT be hidden.

A settlement claim with unresolved material contradiction MUST either remain unsettled or explicitly justify why the contradiction does not block settlement.

24. Evidence Admissibility

Admissibility describes whether Evidence may be used for a specific evaluation context.

24.1 Admissibility Record

An admissibility record SHOULD preserve:

evidence_ref
question_ref
evaluation_context
admissibility_status
admissibility_basis
exclusion_reason
limitations

24.2 Admissibility Status

Admissibility status SHOULD be one of:

admissible
inadmissible
conditionally_admissible
unknown
not_applicable

24.3 Admissibility Failure

Evidence may be relevant but inadmissible.

For example, an unverified model output may be relevant to a hypothesis but inadmissible for settlement.

25. Evidence Weight

Evidence weight is a benchmark-specific or evaluation-specific value assigned to Evidence.

CEP does not require a universal weighting scheme.

If evidence weighting is used, the weighting rule MUST be declared.

25.1 Weight Record

A weight record SHOULD preserve:

evidence_ref
weight_value
weight_scale
weight_rule_ref
question_ref
metric_ref
limitations

25.2 Weight Failure

Evidence weighting without declared rule is not benchmark-valid.

26. Evidence Lifecycle

Evidence MAY pass through lifecycle statuses.

created
collected
normalized
classified
linked
reviewed
verified
admitted
excluded
superseded
contradicted
stale
archived
unknown

Lifecycle status MUST NOT be confused with truth.

Verified Evidence may later be contradicted.

Excluded Evidence may still be useful for diagnosis.

Stale Evidence may remain useful for historical evaluation.

27. Evidence Operations

CEP-compatible implementations MAY perform operations over Evidence.

Operations MUST preserve provenance, lineage, scope, and uncertainty.

27.1 Collect Evidence

Creates or imports Evidence candidate from a source Representation.

Collection MUST preserve source and method.

27.2 Classify Evidence

Assigns Evidence type, direction, relevance, reliability, admissibility, or target.

Classification MUST preserve classification basis.

27.3 Bind Evidence

Connects Evidence to a Claim, Question, State, Transformation, Invariant, or Settlement.

Binding MUST preserve target and relation.

27.4 Validate Evidence

Checks Evidence sufficiency, provenance, integrity, admissibility, and target binding.

Validation MUST distinguish schema validity from semantic and settlement validity.

27.5 Normalize Evidence

Maps Evidence into a standard form.

Normalization MUST preserve source and loss notes.

27.6 Compare Evidence

Identifies whether Evidence records support, duplicate, contradict, qualify, or supersede one another.

Comparison MUST preserve question and target.

27.7 Corroborate Evidence

Combines multiple Evidence records to assess independent support.

Corroboration MUST preserve independence assumptions.

27.8 Contradict Evidence

Marks conflict between Evidence and target Claim or other Evidence.

Contradiction MUST preserve impact on confidence and settlement.

27.9 Supersede Evidence

Marks one Evidence record as replaced or made obsolete by another.

Supersession MUST NOT delete the prior Evidence record.

27.10 Exclude Evidence

Marks Evidence as inadmissible for a particular evaluation.

Exclusion MUST preserve reason.

28. Evidence and Observation

Observation becomes Evidence only when bound to a Question and Claim.

28.1 Minimal Observation-to-Evidence Pattern

Observation
→ Representation
→ Question
→ Claim
→ Relevance Assessment
→ Reliability Assessment
→ Evidence

28.2 Failure Mode

If Observation is treated as Evidence without Question and Claim, CEP cannot determine what the observation proves, weakens, contradicts, or qualifies.

29. Evidence and Claims

Every Evidence record MUST bear on at least one target.

When the target is a Claim, the Evidence MUST indicate direction.

29.1 Claim-Evidence Pattern

Claim
← supports / weakens / contradicts / qualifies
Evidence

29.2 Failure Mode

Evidence detached from Claim cannot support settlement.

30. Evidence and Authority

Authority decisions require Evidence when permissibility is evaluated.

30.1 Minimal Authority Evidence Pattern

Actor
→ Proposed Transformation
→ Authority Constraint
→ Authority Question
→ Policy or Rule Evidence
→ Decision Evidence
→ allow / deny / escalate / unknown

30.2 Authority Evidence Requirements

Authority Evidence SHOULD preserve:

authority_constraint_ref
policy_or_rule_ref
actor_ref
transformation_ref
scope
effective_time
decision_ref
confidence

30.3 Failure Mode

If authority decisions lack Evidence, they are unsupported.

If Evidence shows capability but not permissibility, it is insufficient for authority.

31. Evidence and Reality Gap

Reality Gap evaluation requires Evidence for divergence between Declared State and Observed State.

31.1 Minimal Reality Gap Evidence Pattern

Declared State
→ Observed State
→ Divergence Question
→ Gap Claim
→ Evidence
→ Gap Classification

31.2 Gap Evidence Requirements

Reality Gap Evidence SHOULD preserve:

declared_state_ref
observed_state_ref
affected_distinctions
affected_relations
gap_claim_ref
evidence_refs
severity_basis
confidence

31.3 Failure Mode

If Evidence does not target the divergence claim, Reality Gap scoring is invalid.

32. Evidence and Settlement

Settlement depends on Evidence sufficiency.

Evidence supports settlement only when it addresses the settlement Question and consequence Claim.

32.1 Minimal Settlement Evidence Pattern

Transformation
→ Completion Claim
→ Observed Consequence
→ Evidence
→ Contradiction Handling
→ Settlement Status

32.2 Settlement Evidence Requirements

Settlement Evidence SHOULD preserve:

transformation_ref
consequence_claim_ref
observed_consequence_refs
evidence_refs
missing_evidence
unresolved_contradictions
confidence_impact
settlement_threshold_ref

32.3 Failure Mode

A completion claim alone is not sufficient Evidence for settlement.

Evidence may support that an action executed without supporting that consequences settled.

33. Evidence and Capability

Capability requires Evidence of repeated settled transformations under variation.

33.1 Minimal Capability Evidence Pattern

Transformation Chain
→ Settlement History
→ Variation Context
→ Payment Burden Before
→ Payment Burden After
→ Affordance Delta
→ Capability Claim
→ Evidence

33.2 Capability Evidence Requirements

Capability Evidence SHOULD preserve:

settlement_history_refs
variation_context
burden_measure_refs
affordance_delta_refs
repetition_basis
decay_conditions
confidence

33.3 Failure Mode

Evidence of one success is insufficient to establish Capability.

34. Evidence and Affordance

Affordance evaluation requires Evidence that a Transformation is reachable, payable, permissible, executable, and settleable from current State.

34.1 Minimal Affordance Evidence Pattern

Current State
→ Candidate Transformation
→ Constraint Evidence
→ Authority Evidence
→ Capability Evidence
→ Payment Evidence
→ Settlement Requirement Evidence
→ Reachability Status

34.2 Failure Mode

Evidence that a transformation is imaginable or theoretically possible is insufficient to establish affordance.

35. Evidence and Benchmarks

A CEP-compatible Benchmark MUST define evidence requirements.

35.1 Benchmark Evidence Requirement Record

A benchmark evidence requirement SHOULD preserve:

benchmark_ref
case_ref
question_ref
claim_ref
required_evidence_types
minimum_relevance
minimum_reliability
admissibility_rules
scoring_rules
missing_evidence_penalty
contradiction_handling

35.2 Benchmark Evidence Failure

A benchmark that scores answers without evaluating evidence traceability is not CEP-compliant.

A benchmark case that requires evidence but does not define what evidence counts is under-specified.

36. Evidence and Semantic Envelope

A Semantic Envelope MUST be capable of carrying Evidence context.

An Evidence record carried in a Semantic Envelope SHOULD include:

evidence_id
evidence_type
question_ref
target_claim_ref
target_entity_ref
representation_ref
source
provenance_refs
relevance
reliability
direction
confidence_impact
timestamp
scope
integrity_record
admissibility_status
corroboration_refs
contradiction_refs
limitations

A Semantic Envelope MUST preserve whether Evidence context is complete, partial, unknown, unavailable, or out of scope.

37. Minimal Valid Evidence

A minimally valid CEP Evidence record MUST preserve:

evidence_id
evidence_type
question_ref
target_claim_ref OR target_entity_ref
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

A minimally valid Evidence record SHOULD preserve:

integrity_record
freshness_record
admissibility_status
independence_record
corroboration_refs
contradiction_refs
review_status

Evidence lacking Question binding is not benchmark-valid.

Evidence lacking target binding is not CEP-valid.

Evidence lacking provenance is not settlement-valid.

Evidence lacking direction is not confidence-valid.

38. Invalid Evidence Conditions

Evidence is invalid for CEP evaluation if:

it lacks a target,

it lacks a Question,

it lacks source,

it lacks provenance,

it lacks relevance assessment,

it lacks reliability assessment,

it lacks direction,

it lacks confidence impact,

it treats Claim as Evidence for itself,

it treats data as Evidence without binding,

it treats model output as verified observation without qualification,

it treats duplicate Evidence as independent corroboration,

it hides material contradiction,

it lacks freshness where freshness matters,

it lacks chain of custody where custody is required,

or it is inadmissible for the evaluation context.

Invalid Evidence MAY still be stored.

Invalid Evidence MUST NOT be used for settlement, authority decision, capability claim, affordance claim, or benchmark scoring unless the invalidity itself is the object of evaluation.

39. Evidence Invariants

CEP-compatible systems SHALL preserve the following Evidence invariants.

Invariant 1 — Evidence Is Question-Bound

Evidence SHALL be interpreted relative to a Question.

Invariant 2 — Evidence Is Target-Bound

Evidence SHALL target a Claim, State, Transformation, Invariant, Settlement, Affordance, Capability, or Benchmark result.

Invariant 3 — Evidence Is Not Data

Data SHALL NOT be treated as Evidence without relevance and target binding.

Invariant 4 — Evidence Is Not Claim

A Claim SHALL NOT be treated as Evidence for itself.

Invariant 5 — Evidence Updates Confidence

Evidence SHALL affect confidence rather than establish absolute truth.

Invariant 6 — Source Preservation

Evidence SHALL preserve source.

Invariant 7 — Provenance Preservation

Evidence SHALL preserve provenance.

Invariant 8 — Direction Preservation

Evidence SHALL preserve whether it supports, weakens, contradicts, qualifies, is irrelevant, or is unknown.

Invariant 9 — Reliability Preservation

Evidence SHALL preserve reliability or reliability uncertainty.

Invariant 10 — Relevance Preservation

Evidence SHALL preserve relevance or relevance uncertainty.

Invariant 11 — Contradiction Preservation

Known contradictions SHALL NOT be hidden.

Invariant 12 — Corroboration Discipline

Dependent or duplicate Evidence SHALL NOT be treated as independent corroboration.

40. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:

data into evidence
observation into evidence without question
claim into evidence
source into evidence
evidence into truth
confidence into certainty
model output into verified evidence
summary into source evidence
duplicate evidence into corroboration
relevance into reliability
reliability into relevance
freshness into reliability
admissibility into truth
policy text into authority decision
test pass into settlement
execution log into consequence settlement
human attestation into independent verification
absence of contradiction into proof
missing evidence into negative evidence

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

41. Evidence Conformance

A CEP-compatible Evidence implementation MUST:

distinguish data from evidence,

distinguish Claim from Evidence,

preserve Evidence identity,

preserve Question binding,

preserve target binding,

preserve source,

preserve provenance,

preserve relevance,

preserve reliability,

preserve direction,

preserve confidence impact,

preserve scope,

preserve timestamp,

preserve limitations,

preserve contradiction records when known,

preserve independence or dependency when corroboration is claimed,

preserve admissibility when used in benchmark or settlement context,

preserve freshness when time matters,

preserve integrity when integrity matters,

support evidence validation,

support evidence comparison,

support evidence binding to claims, transformations, states, invariants, and settlements,

and reject or warn on anti-collapse violations.

42. Implementation Consequence

A CEP-compatible system that evaluates transformations MUST implement the Evidence Model.

A system that only records logs, traces, model outputs, human statements, or test results without binding them to Questions and Claims is not CEP-compliant.

A system that scores benchmark answers without evidence traceability is not CEP-compliant.

A system that declares settlement without evidence sufficiency is not CEP-compliant.

This requirement exists because CEP does not evaluate isolated assertions.

CEP evaluates represented transformations through evidence-backed settlement.

Evidence is the mechanism by which observations become usable for confidence update and state transition.

43. Closing Definition

Evidence is a Representation that changes confidence in a Claim relative to a Question.

Evidence is not data.

Evidence is not truth.

Evidence is not self-attestation.

Evidence is not settlement.

Evidence is the structured support, contradiction, qualification, or weakening that makes consequence-backed evaluation possible.

Without Evidence, CEP cannot distinguish assertion from support, completion from settlement, authority from capability, or output from evaluated transformation.

The next document should be CEP-0007 — Settlement Model. That is the key GodSpeed distinction: when represented consequences are reliable enough to update state, without confusing settlement with success, approval, morality, or completion.