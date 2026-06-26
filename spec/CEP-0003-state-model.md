CEP-0003 — State Model

Status: Draft
Category: Normative
Version: 0.1
Protocol: Canonical Evaluation Protocol
Depends On:

CEP-0000 — Derivation Ladder and First Principles

CEP-0001 — Ontology

CEP-0002 — Representation Model

Document Type: Foundational Specification

Abstract

This document defines the CEP State Model.

CEP evaluates represented transformations. A transformation cannot be evaluated unless CEP can identify what condition existed before, what condition existed after, and whether both conditions refer to a sufficiently continuous evaluation subject.

The State Model defines how a representation becomes situated enough to support comparison, transformation, observation, evidence, settlement, and benchmark scoring.

A state is not reality.

A state is a situated representation.

1. Purpose

The purpose of the State Model is to prevent CEP implementations from treating unsituated information as evaluable condition.

A policy document, event log, model output, trace, interview, or benchmark input is not automatically a state.

It becomes a state only when it is situated by enough context to answer:

What condition is being represented?

What entity, system, process, actor, artifact, organization, or environment does the condition apply to?

At what time or interval does the condition apply?

Under which scope does the condition hold?

Under which identity assumptions is continuity preserved?

Which constraints are active, inactive, satisfied, violated, unknown, or out of scope?

Which distinctions and relations are preserved?

Which perspective or question makes the state relevant?

What is known, unknown, omitted, uncertain, or contested?

What transformations can be evaluated from or into this state?

A CEP-compatible implementation MUST preserve enough state context to support its evaluation claims.

2. Scope

This document defines:

state definition,

state sufficiency,

state identity,

state continuity,

state context,

state types,

declared and observed states,

expected, actual, claimed, authorized, settled, unsettled, and counterfactual states,

state validity,

state operations,

state comparison,

state conformance,

and anti-collapse rules.

This document does not define:

the complete Transformation Model,

settlement thresholds,

evidence scoring,

benchmark scoring algorithms,

Semantic Envelope serialization,

or final schema syntax.

Those are defined in later CEP specifications.

3. Core Definition

A State is a situated Representation.

A Representation becomes a State when it preserves sufficient context to support comparison, transformation, observation, evidence, settlement, or evaluation.

A State MUST NOT be treated as reality itself.

A State is an evaluable representation of condition under context.

4. State Sufficiency

A Representation is state-sufficient when it preserves enough context to answer what condition is represented, where it applies, when it applies, and what identity it concerns.

4.1 Required State-Sufficiency Fields

A state-sufficient Representation MUST preserve:

state_id
representation_refs
state_type
scope
time_context
identity_refs
relevant_constraints
relevant_distinctions
relevant_relations
confidence
provenance_refs
omission_record
uncertainty_record

4.2 Conditional State-Sufficiency Fields

A State SHOULD preserve the following when materially relevant:

actor_context
authority_context
resource_context
environment_context
question_refs
perspective_refs
evidence_refs
version
lifecycle_status
validity_record

4.3 State-Sufficiency Failure

If a Representation lacks state sufficiency, it MAY still be stored, referenced, or analyzed.

It MUST NOT be used as the basis for transformation, settlement, capability, authority, affordance, or benchmark scoring unless the missing context is explicitly marked and accepted by the evaluation context.

5. State Boundary

Every State has a boundary.

The State boundary defines what the State includes, excludes, treats as unknown, or leaves out of scope.

5.1 Boundary Requirements

A State boundary MUST preserve:

scope
subject_ref
time_context
included_entities
excluded_entities when known
unknown_entities when relevant
out_of_scope_entities when relevant
active_constraints
inactive_constraints when relevant

5.2 Boundary Discipline

A State MUST NOT be projected outside its boundary without explicit projection rules.

A State valid for one process, team, environment, version, actor, or time period MUST NOT be silently reused as if globally valid.

5.3 Boundary Failure

If State boundary is absent, CEP cannot determine whether a transformation applies to the same subject, same scope, same process, same authority context, or same environment.

This creates false comparison and invalid benchmark scoring.

6. State Subject

A State MUST have a subject.

The subject is the entity, system, process, artifact, actor, organization, environment, or composite structure whose condition is represented.

6.1 Subject Types

A State subject MAY be:

actor
agent
human
team
organization
system
service
tool
artifact
process
policy
resource
environment
benchmark_case
semantic_envelope
composite
unknown

6.2 Subject Requirement

A State without a subject is not evaluable.

If the subject is uncertain, the State MUST preserve subject uncertainty rather than omit subject identity.

7. State Identity

Identity is the rule by which CEP determines that a State concerns the same evaluation subject across time, comparison, or transformation.

Identity is not perfect sameness.

Identity is continuity sufficient for evaluation.

7.1 Identity Record

A State identity record SHOULD preserve:

identity_ref
subject_ref
continuity_basis
version
scope
time_context
confidence
evidence_refs
known_discontinuities

7.2 Continuity Basis

Continuity MAY be established by:

persistent_identifier
version_lineage
semantic_equivalence
artifact_history
role_continuity
process_continuity
policy_continuity
actor_continuity
system_continuity
organizational_continuity
spatial_continuity
temporal_continuity
external_attestation
human_attestation

7.3 Identity Uncertainty

If identity continuity cannot be established, the State MUST be marked as identity-uncertain.

A transformation involving identity-uncertain states MUST preserve that uncertainty.

7.4 Identity Failure

Without identity, CEP cannot determine whether:

a system changed,

a system was replaced,

a policy was revised,

a policy was substituted,

a process drifted,

a different process was observed,

a capability repeated,

or a new event merely resembled a prior event.

Identity failure invalidates transformation evaluation unless explicitly accepted by the benchmark or evaluation context.

8. Time Context

A State MUST preserve time context when time affects evaluation.

8.1 Time Context Record

A Time Context record SHOULD preserve:

valid_at
valid_from
valid_until
observed_at
declared_at
created_at
updated_at
time_zone
temporal_precision
temporal_uncertainty

8.2 Temporal Precision

Temporal precision MAY be:

instant
interval
date
sequence_order
version_order
event_order
unknown

8.3 Time Failure

If time context is absent, CEP cannot distinguish:

prior condition from later condition,

active policy from superseded policy,

observed drift from expected update,

stale evidence from current evidence,

and delayed settlement from immediate settlement.

9. Scope Context

A State MUST preserve scope.

Scope defines where the represented condition applies.

9.1 Scope Record

A Scope record SHOULD preserve:

domain
organization_or_system
team
process
artifact
environment
jurisdiction
role_context
benchmark_family
evaluation_context
limitations

9.2 Scope Failure

If scope is absent, CEP cannot determine whether a State applies to the transformation being evaluated.

A correct State in one scope may be false, irrelevant, or dangerous in another.

10. Constraint Context

A State MUST preserve the constraints relevant to its evaluation context.

10.1 Constraint Status

Constraints in a State SHOULD be marked using statuses such as:

active
inactive
pending
satisfied
violated
superseded
unknown
out_of_scope

10.2 Constraint Context Record

A State SHOULD preserve:

constraint_ref
constraint_type
status
applies_to
source
effective_time
confidence
evidence_refs

10.3 Constraint Failure

If relevant constraints are not preserved, CEP cannot determine whether a transformation was possible, permissible, blocked, costly, risky, required, or settleable.

11. Distinction Context

A State MUST preserve distinctions relevant to comparison or evaluation.

11.1 Required Distinction Examples

A State SHOULD be capable of preserving distinctions such as:

declared / observed
expected / actual
claimed / evidenced
active / inactive
allowed / denied
possible / permissible
attempted / transformed
completed / settled
capable / incapable
reachable / unreachable
known / unknown
valid / invalid

11.2 Distinction Failure

If relevant distinctions are absent, CEP cannot compare States reliably.

This directly breaks Reality Gap, Authority, Settlement, Capability, and Affordance evaluation.

12. Relation Context

A State MUST preserve relations relevant to its condition.

12.1 State Relation Examples

Relations in a State MAY include:

actor_has_role
role_has_authority
policy_applies_to_process
process_requires_approval
artifact_depends_on_resource
evidence_supports_claim
constraint_blocks_transformation
state_supersedes_state
state_contradicts_state
state_updates_state

12.2 Relation Failure

If relations are absent, CEP cannot determine what applies to what.

This causes invalid authority evaluation, evidence interpretation, state comparison, and settlement update.

13. State Types

CEP recognizes the following core State types:

declared
observed
expected
actual
claimed
authorized
unauthorized
settled
unsettled
counterfactual
projected
baseline
target
unknown

A State MAY have more than one type if the types are not contradictory.

For example, a State may be both declared and expected.

A State MUST NOT silently merge contradictory types.

14. Declared State

14.1 Definition

A Declared State represents what a system, actor, organization, policy, requirement, design, benchmark, or governance structure claims should be true, intended, required, permitted, prohibited, or expected.

14.2 Sources

Declared States MAY derive from:

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
model_plan

14.3 Requirements

A Declared State MUST preserve:

declaration_source
declared_condition
scope
effective_time
authority_or_ownership when relevant
confidence

14.4 Failure Mode

If Declared State is not preserved separately from Observed State, Reality Gap evaluation becomes impossible.

15. Observed State

15.1 Definition

An Observed State represents what appears to have occurred, existed, changed, failed, settled, or drifted according to observation.

15.2 Sources

Observed States MAY derive from:

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

15.3 Requirements

An Observed State MUST preserve:

observation_source
observed_condition
observation_method
observed_at
scope
confidence
limitations

15.4 Failure Mode

If Observed State is collapsed into Declared State, CEP cannot detect drift, noncompliance, mismatch, or emergent behavior.

16. Expected State

16.1 Definition

An Expected State represents what should result if a proposed or attempted transformation behaves according to specified rules, plans, models, policies, or predictions.

16.2 Use

Expected States support:

transformation evaluation,

test planning,

benchmark answer keys,

authority decisions,

settlement expectations,

and capability projection.

16.3 Failure Mode

If Expected State is absent, CEP cannot distinguish intended transformation from unintended transformation.

17. Actual State

17.1 Definition

An Actual State is the best currently supported representation of the condition after evidence integration.

Actual State is still representational.

It is not reality itself.

17.2 Requirement

An Actual State SHOULD preserve:

supporting_evidence_refs
confidence
unresolved_contradictions
settlement_status
state_derivation_refs

17.3 Failure Mode

If Actual State is treated as objective reality, CEP loses uncertainty discipline.

18. Claimed State

18.1 Definition

A Claimed State represents a condition asserted by an actor, system, model, document, tool, or process.

18.2 Requirement

A Claimed State MUST preserve the claimant.

claimant_ref
claim_source
claim_time
claim_confidence
supporting_evidence_refs when available

18.3 Failure Mode

If Claimed State is treated as Evidenced State, systems can self-attest success without support.

This breaks settlement evaluation.

19. Authorized State

19.1 Definition

An Authorized State represents a condition in which one or more transformations are permissible under applicable authority constraints.

19.2 Requirement

An Authorized State MUST preserve:

authority_refs
permitted_transformations
prohibited_transformations
escalation_conditions
effective_time
scope

19.3 Failure Mode

If Authorized State is collapsed into Capability State, CEP cannot distinguish what can be done from what may be done.

20. Unauthorized State

20.1 Definition

An Unauthorized State represents a condition in which one or more transformations are prohibited, invalid, or require escalation under applicable authority constraints.

20.2 Requirement

An Unauthorized State MUST preserve the violated, missing, or unresolved authority constraint.

20.3 Failure Mode

If Unauthorized State is not representable, CEP cannot evaluate governance failure.

21. Settled State

21.1 Definition

A Settled State is a State updated through reliable consequence registration after a transformation.

A Settled State does not imply success, approval, benefit, or legitimacy.

It means consequences have been sufficiently registered for the evaluation context.

21.2 Requirement

A Settled State MUST preserve:

settlement_refs
transformation_refs
evidence_refs
confidence
unresolved_contradictions
settlement_time

21.3 Failure Mode

If Settled State is collapsed into Completed State, CEP rewards premature completion claims.

22. Unsettled State

22.1 Definition

An Unsettled State is a State whose consequences, evidence, identity, authority, or contradictions are insufficiently resolved for state update.

22.2 Requirement

An Unsettled State SHOULD preserve what prevents settlement:

missing_evidence
unresolved_contradictions
identity_uncertainty
authority_uncertainty
temporal_uncertainty
scope_uncertainty
pending_observations

22.3 Failure Mode

If Unsettled State is not representable, systems will overclaim readiness and hide uncertainty.

23. Counterfactual State

23.1 Definition

A Counterfactual State represents a condition that did not occur, is not known to have occurred, or is considered for comparison, planning, simulation, or benchmark generation.

23.2 Requirement

A Counterfactual State MUST be marked as counterfactual.

It MUST NOT be treated as observed or actual.

23.3 Use

Counterfactual States support:

simulation,

scenario generation,

benchmark case generation,

risk analysis,

authority testing,

and capability projection.

23.4 Failure Mode

If Counterfactual State is collapsed into Observed State, CEP corrupts evidence and benchmark validity.

24. Projected State

24.1 Definition

A Projected State represents a possible future condition inferred from current state, expected transformations, or model predictions.

24.2 Requirement

A Projected State MUST preserve:

projection_method
source_state_refs
assumptions
confidence
time_horizon
limitations

24.3 Failure Mode

If Projected State is treated as Settled State, planning artifacts become false evidence.

25. Baseline State

25.1 Definition

A Baseline State is the reference condition against which later states or transformations are compared.

25.2 Requirement

A Baseline State MUST preserve why it was chosen as baseline.

25.3 Failure Mode

If baseline selection is implicit, benchmark scores and capability deltas become manipulable.

26. Target State

26.1 Definition

A Target State represents a desired, intended, required, or benchmark-expected condition.

26.2 Requirement

A Target State MUST preserve its source of desirability or requirement.

26.3 Failure Mode

If Target State is collapsed into Expected State, CEP cannot distinguish desire from prediction.

27. Unknown State

27.1 Definition

An Unknown State represents a condition that is not sufficiently known.

Unknown does not mean false.

Unknown does not mean not applicable.

Unknown does not mean absent.

27.2 Requirement

Unknown State SHOULD preserve why the state is unknown.

not_observed
not_collected
redacted
ambiguous
inaccessible
identity_uncertain
out_of_scope
unavailable

27.3 Failure Mode

If Unknown State is collapsed into falsehood or absence, CEP produces invalid evaluation.

28. State Lifecycle

A State MAY pass through lifecycle statuses such as:

draft
proposed
declared
active
observed
claimed
validated
contradicted
superseded
settled
unsettled
deprecated
rejected
archived
unknown

Lifecycle status MUST NOT be confused with truth.

A declared State may be false.

An observed State may be mistaken.

A settled State may be harmful.

A rejected State may still serve as evidence of error.

29. State Operations

CEP-compatible implementations MAY perform operations over States.

When performed, these operations MUST preserve provenance, identity assumptions, and uncertainty.

29.1 State Creation

State Creation converts one or more Representations into a State.

Creation MUST preserve:

source_representation_refs
state_type
scope
time_context
identity_refs
provenance_refs

29.2 State Comparison

State Comparison identifies differences between States.

Comparison MUST preserve:

compared_state_refs
comparison_question_ref
identity_assumptions
relevant_distinctions
detected_differences
confidence

Reality Gap evaluation is a specialized State Comparison between Declared State and Observed State.

29.3 State Diff

State Diff identifies changes between two States over time or version lineage.

Diff MUST preserve:

source_state_ref
target_state_ref
changed_constraints
changed_distinctions
changed_relations
unchanged_entities
identity_basis
confidence

29.4 State Merge

State Merge combines multiple States into a composite State.

Merge MUST preserve:

source_state_refs
conflicts
resolution_rules
omissions
confidence_impact

A State Merge MUST NOT silently resolve contradictions.

29.5 State Projection

State Projection creates a future, hypothetical, scoped, or filtered State from one or more source States.

Projection MUST preserve:

source_state_refs
projection_rules
assumptions
excluded_entities
confidence
limitations

29.6 State Update

State Update modifies a State based on evidence, settlement, transformation, or revision.

Update MUST preserve:

prior_state_ref
update_reason
transformation_ref when applicable
evidence_refs
updated_entities
supersession_record
confidence_impact

A State Update based on settlement MUST preserve settlement reference.

29.7 State Validation

State Validation checks whether a State satisfies required constraints.

Validation MUST distinguish:

schema_validity
semantic_validity
identity_validity
scope_validity
evidence_validity
authority_validity
settlement_validity
benchmark_validity

30. State Comparison Semantics

State comparison is valid only when identity, scope, and question are preserved.

30.1 Required Comparison Context

A valid State comparison MUST preserve:

state_a_ref
state_b_ref
comparison_type
question_ref
identity_basis
scope_alignment
time_alignment
confidence

30.2 Comparison Types

CEP recognizes:

declared_vs_observed
expected_vs_actual
claimed_vs_evidenced
authorized_vs_executed
baseline_vs_current
current_vs_target
before_vs_after
counterfactual_vs_observed
projected_vs_actual

30.3 Comparison Failure

A comparison is invalid if:

subjects differ without projection,

scopes differ without alignment,

identity is unresolved,

time contexts are incompatible,

or the comparison question is absent.

31. State Validity

A State may be valid in one dimension and invalid in another.

CEP recognizes the following validity dimensions:

representation_validity
identity_validity
scope_validity
temporal_validity
semantic_validity
constraint_validity
relation_validity
evidence_validity
authority_validity
settlement_validity
benchmark_validity

A CEP-compatible implementation MUST NOT collapse these dimensions.

31.1 Example

A State may be representation-valid and temporal-valid but authority-invalid.

For example, an observed deployment may have occurred and be well evidenced while still violating authority constraints.

32. State Confidence

A State SHOULD preserve confidence.

Confidence represents degree of support for the State as represented.

32.1 Confidence Basis

State confidence SHOULD be based on:

source_quality
evidence_strength
identity_confidence
scope_confidence
temporal_confidence
relation_confidence
contradiction_level
review_status
settlement_status

32.2 Confidence Failure

A State with high confidence but no confidence basis SHOULD be treated as unsupported.

Confidence MUST NOT be treated as truth.

33. State Contradictions

A State MAY contain unresolved contradictions.

Contradictions MUST be marked when known.

33.1 Contradiction Record

A contradiction record SHOULD preserve:

contradiction_id
entity_refs
relation_refs
description
severity
evidence_refs
resolution_status
impact

33.2 Contradiction Failure

If contradictions are hidden, CEP may falsely settle unstable States.

Known contradictions MUST NOT be silently discarded during merge, update, or benchmark scoring.

34. State Omission and Unknowns

A State MUST preserve material omissions and unknowns.

34.1 State Omission Examples

A State SHOULD mark when:

authority context is unknown,

identity is uncertain,

evidence is missing,

observations are delayed,

scope is ambiguous,

time context is incomplete,

actor is unknown,

resource context is unavailable,

or relevant constraints were not collected.

34.2 Failure Mode

If unknowns are treated as false, CEP produces invalid authority, settlement, capability, and Reality Gap evaluations.

35. State and Transformation

A Transformation requires at least one source State and one target, claimed target, expected target, observed target, or updated State.

A State does not become a Transformation merely because it differs from another State.

A Transformation requires a represented change relationship.

35.1 Minimum Transformation Readiness

A State is transformation-ready when it preserves:

identity_refs
scope
time_context
relevant_constraints
relevant_distinctions
relevant_relations
confidence

A benchmark MAY specify stricter readiness requirements.

36. State and Settlement

Settlement updates State.

A settled transformation produces or validates a State update.

36.1 Settlement-Ready State

A State is settlement-ready when it preserves:

transformation_ref
evidence_refs
settlement_question_ref
confidence
unresolved_contradictions
threshold_ref

36.2 Settlement Failure

A State MUST NOT be marked settled only because an actor claimed completion.

37. State and Capability

Capability requires repeated settlements across State changes under variation.

A State may participate in capability evaluation if it preserves:

capability_relevant_transformation_refs
settlement_history_refs
variation_context
payment_burden_context
affordance_delta_refs

A single State cannot establish Capability.

38. State and Affordance

Affordance depends on current State.

A State may support affordance evaluation if it preserves:

reachable_transformations
authority_context
capability_context
resource_context
payment_burden_context
settlement_requirements
evidence_requirements

A State that merely describes a possible future does not establish an affordance.

39. State and Benchmark Cases

A benchmark case MUST define or derive the States required for evaluation.

39.1 Minimal Benchmark State Requirements

A CEP-compatible benchmark case SHOULD preserve:

case_id
state_refs
state_types
comparison_question_ref
expected_transformations when applicable
answer_key_state_refs when applicable
evidence_requirements
scoring_relevant_distinctions

39.2 Benchmark State Failure

A benchmark case is invalid if the States required for scoring cannot be identified, compared, or situated.

40. Minimal Valid State

A minimally valid CEP State MUST preserve:

state_id
state_type
subject_ref
representation_refs
scope
time_context
identity_refs OR identity_uncertainty
relevant_constraints OR constraint_status
relevant_distinctions
relevant_relations
confidence OR confidence_status
provenance_refs
omission_record OR omission_status

A State lacking subject, scope, time context, and identity information is not CEP-valid.

A State lacking relevant distinctions is not benchmark-valid.

A State lacking provenance is not settlement-valid.

41. Invalid State Conditions

A State is invalid for CEP evaluation if:

it lacks a subject,

it lacks scope,

it lacks time context when time matters,

it lacks identity or identity uncertainty,

it collapses declared and observed conditions,

it collapses claimed and evidenced conditions,

it treats unknown as false,

it treats target as actual,

it treats projected as settled,

it hides material contradictions,

it omits material constraints,

it lacks provenance,

or it cannot support the comparison required by its benchmark or evaluation context.

Invalid States MAY still be stored.

Invalid States MUST NOT be used for settlement, capability, authority, affordance, or benchmark scoring unless the invalidity itself is the object of evaluation.

42. State Invariants

CEP-compatible systems SHALL preserve the following State invariants.

Invariant 1 — State Is Situated Representation

A State SHALL remain distinct from unsituated Representation.

Invariant 2 — State Is Not Reality

A State SHALL NOT be treated as reality itself.

Invariant 3 — Identity Preservation

A State SHALL preserve identity continuity or identity uncertainty.

Invariant 4 — Scope Preservation

A State SHALL preserve scope.

Invariant 5 — Temporal Preservation

A State SHALL preserve relevant time context.

Invariant 6 — Constraint Preservation

A State SHALL preserve relevant constraints and their statuses.

Invariant 7 — Distinction Preservation

A State SHALL preserve distinctions required for comparison and evaluation.

Invariant 8 — Relation Preservation

A State SHALL preserve relations required for evaluation.

Invariant 9 — Declared/Observed Separation

Declared State and Observed State SHALL remain separable.

Invariant 10 — Claimed/Evidenced Separation

Claimed State and Evidenced State SHALL remain separable.

Invariant 11 — Settlement Separation

Settled State SHALL remain distinct from completed, successful, authorized, or beneficial State.

Invariant 12 — Unknown Discipline

Unknown SHALL remain distinct from false, absent, not applicable, and out of scope.

43. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:

state into reality
state into representation
declared state into observed state
observed state into actual state
claimed state into evidenced state
expected state into actual state
target state into expected state
projected state into settled state
authorized state into capable state
settled state into successful state
unknown state into false state
counterfactual state into observed state
baseline state into neutral truth

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

44. State Conformance

A CEP-compatible State implementation MUST:

distinguish Representation from State,

preserve State subject,

preserve State scope,

preserve relevant time context,

preserve identity or identity uncertainty,

preserve relevant constraints,

preserve relevant distinctions,

preserve relevant relations,

preserve provenance,

preserve omissions and unknowns,

support declared and observed State separation,

support State comparison,

support State update,

support contradiction marking,

support confidence and confidence basis when confidence is used,

and reject or warn on anti-collapse violations.

45. Implementation Consequence

A CEP-compatible system that evaluates transformations MUST implement the State Model.

A system that only stores documents, logs, traces, prompts, model outputs, or benchmark inputs without converting them into situated States cannot perform CEP-compliant evaluation.

This requirement exists because CEP evaluates represented transformations.

Without situated States, there is no stable basis for determining what changed, whether the change was observed, whether it was evidenced, whether it settled, whether authority was preserved, or whether capability improved.

46. Closing Definition

A State is a situated Representation.

A valid State preserves subject, scope, time context, identity, relevant constraints, distinctions, relations, provenance, omissions, uncertainty, and confidence.

CEP transformations begin and end with States.

Therefore, the reliability of every CEP evaluation depends on the quality of the States it compares, transforms, observes, evidences, and settles.

The next document is CEP-0004 — Transformation Model. That one becomes the spine of the whole protocol: source state, target state, attempted action, represented change, invariant preservation, authority relevance, evidence hooks, and settlement readiness.