---
type: CEP Specification
id: CEP-0004
title: Transformation Model
description: This document defines the CEP Transformation Model.
status: Draft
version: 0.1.0
tags:
- cep
timestamp: '2026-06-26T14:13:47Z'
protocol: Canonical Evaluation Protocol
category: Normative
document_type: Foundational Specification
depends_on:
- CEP-0000
- CEP-0001
- CEP-0002
- CEP-0003
supersedes: []
superseded_by: []
conformance_class: null
benchmark_family: null
schema_ref: null
---

# CEP-0004 — Transformation Model

## Abstract

This document defines the CEP Transformation Model.

CEP evaluates represented transformations rather than isolated outputs, static artifacts, or task completion claims.

A Transformation is a represented change from one State to another State under preserved identity, scope, constraints, and evaluation context.

The Transformation Model defines how changes are represented, classified, validated, evidenced, authorized, settled, reversed, compared, and scored.

A Transformation is not merely an action.

An action is attempted.

A Transformation is the represented change produced, claimed, observed, inferred, or settled after action, drift, decision, failure, update, observation, or environmental change.

1. Purpose

The purpose of the Transformation Model is to prevent CEP implementations from confusing:

action with change,

execution with consequence,

completion with settlement,

intention with result,

possibility with permissibility,

observation with occurrence,

and isolated success with capability.

A CEP-compatible system MUST represent transformations explicitly because all CEP benchmark families depend on transformation evaluation.

RealityGapBench evaluates divergence across represented transformations.

AuthorityBench evaluates whether transformations are permissible.

SettlementBench evaluates whether transformations have produced reliable consequence registration.

CapabilityBench evaluates whether repeated settled transformations reduce future payment burden under variation.

2. Scope

This document defines:

transformation definition,

transformation sufficiency,

transformation identity,

transformation lifecycle,

transformation types,

transformation status,

source and target state rules,

expected, claimed, observed, actual, and settled transformations,

invariant preservation,

authority relevance,

evidence hooks,

settlement readiness,

transformation comparison,

transformation validity,

transformation operations,

benchmark usage,

conformance,

and anti-collapse rules.

This document does not define:

the complete Evidence Model,

settlement thresholds,

benchmark scoring algorithms,

Semantic Envelope serialization,

final schema syntax,

or runner implementation.

Those are defined in later CEP specifications.

3. Core Definition

A Transformation is a represented change from one State to another State.

A Transformation alters one or more represented constraints, distinctions, relations, identities, scopes, confidence levels, authority statuses, evidence statuses, settlement statuses, affordances, or capabilities.

A Transformation MUST preserve enough context to answer:

What State existed before?

What State was expected, claimed, observed, or settled after?

What changed?

What did not change?

What caused or triggered the change when known?

Who or what initiated, participated in, authorized, blocked, or observed the change?

Which constraints applied?

Which invariants were expected to hold?

Which invariants were preserved, violated, repaired, or transformed?

What evidence supports the transformation claim?

Was the transformation permissible?

Has the transformation settled?

What affordances changed as a result?

What capability update, if any, is justified?

4. Transformation Is Not Action

CEP SHALL distinguish Action from Transformation.

4.1 Action

An Action is an attempted intervention.

Examples:

an agent writes a file,

a developer opens a pull request,

an operator approves a release,

a policy is edited,

a script is executed,

a model emits an answer,

a team changes a process.

4.2 Transformation

A Transformation is represented change.

Examples:

the file content changed,

the pull request introduced a new dependency,

approval status changed,

authority constraints changed,

production configuration drifted,

evidence confidence increased,

a claimed state became settled,

an affordance became reachable,

a capability became more reliable.

4.3 Anti-Collapse Rule

A CEP implementation MUST NOT treat attempted Action as Transformation unless represented change is identified or claimed.

An attempted Action MAY fail to transform anything.

A Transformation MAY occur without intentional Action.

Examples of non-action transformations include:

drift,

decay,

environmental change,

external dependency change,

passive observation update,

evidence arrival,

authority expiration,

capability decay.

5. Transformation Sufficiency

A Transformation record is sufficient when it preserves enough context to support evaluation.

5.1 Required Transformation Fields

A CEP-compatible Transformation MUST preserve:

transformation_id
transformation_type
source_state_ref
target_state_ref OR claimed_target_state_ref OR observed_target_state_ref
scope
time_context
identity_basis
trigger
affected_entities
affected_constraints
affected_distinctions
affected_relations
expected_invariants
status
confidence
provenance_refs

5.2 Conditional Transformation Fields

A Transformation SHOULD preserve the following when materially relevant:

actor_refs
authority_refs
question_refs
perspective_refs
evidence_refs
settlement_refs
expected_state_ref
claimed_state_ref
observed_state_ref
actual_state_ref
settled_state_ref
payment_burden
affordance_delta_refs
capability_delta_refs
risk_record
contradiction_record
omission_record
uncertainty_record

5.3 Transformation-Sufficiency Failure

If a Transformation lacks source state, target state or target claim, identity basis, affected distinctions, and scope, it is not CEP-valid.

If a Transformation lacks evidence references, it MAY be transformation-valid but is not settlement-valid.

If a Transformation lacks authority context when authority is material, it is not authority-valid.

If a Transformation lacks question context when used in a benchmark, it is not benchmark-valid.

6. Source and Target States

A Transformation MUST relate at least one source State to at least one target-like State.

CEP recognizes multiple target-like State roles.

6.1 Source State

The Source State represents the condition before transformation.

A Source State MUST preserve enough identity and scope to support comparison with target-like States.

6.2 Expected Target State

The Expected Target State represents what should result if the transformation behaves according to plan, policy, model, requirement, or benchmark answer key.

6.3 Claimed Target State

The Claimed Target State represents what an actor, system, model, agent, tool, or document asserts resulted.

6.4 Observed Target State

The Observed Target State represents what was registered through observation after the transformation.

6.5 Actual Target State

The Actual Target State represents the best currently supported representation after evidence integration.

Actual Target State is still representational.

It is not reality itself.

6.6 Settled Target State

The Settled Target State represents the consequence-backed state update after sufficient evidence and contradiction handling.

A Settled Target State does not imply success, approval, benefit, or legitimacy.

6.7 Target Role Discipline

CEP implementations SHALL NOT collapse these target roles.

A claimed target may differ from an observed target.

An expected target may differ from an actual target.

An observed target may remain unsettled.

A settled target may be unauthorized or harmful.

7. Transformation Identity

A Transformation MUST preserve identity continuity.

Identity continuity defines why source and target States are treated as belonging to the same evaluation subject.

7.1 Identity Basis

A Transformation SHOULD preserve:

identity_basis
source_identity_ref
target_identity_ref
continuity_confidence
known_discontinuities
identity_evidence_refs

7.2 Identity Discontinuity

If identity discontinuity is detected, the Transformation MUST mark whether the change represents:

same_subject_changed
subject_replaced
subject_split
subject_merged
subject_removed
subject_created
identity_unknown

7.3 Identity Failure

Without identity continuity, CEP cannot determine whether the same system changed or a different system appeared.

Identity failure invalidates transformation comparison unless explicitly accepted by the evaluation context.

8. Time Context

A Transformation MUST preserve time context when time affects evaluation.

8.1 Time Context Record

A Transformation SHOULD preserve:

proposed_at
attempted_at
executed_at
observed_at
evidenced_at
settled_at
valid_from
valid_until
sequence_order
temporal_precision
temporal_uncertainty

8.2 Temporal Failure

If time context is absent, CEP cannot distinguish:

proposed change from executed change,

immediate consequence from delayed consequence,

stale evidence from current evidence,

authority valid at the time from authority expired at the time,

repeated capability from coincidental similarity.

9. Transformation Scope

A Transformation MUST preserve scope.

Scope determines where the change applies.

9.1 Scope Record

A Transformation SHOULD preserve:

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

If Transformation scope is absent, CEP cannot determine whether a change applies to the evaluated subject.

A valid transformation in one scope may be irrelevant, invalid, unauthorized, or harmful in another.

10. Transformation Types

CEP recognizes the following top-level Transformation types.

action
decision
drift
update
execution
observation
authorization
evidence_update
settlement
capability_update
affordance_update
failure
reversal
repair
escalation
projection
simulation
generation
unknown

10.1 Action Transformation

A represented change caused by attempted action.

10.2 Decision Transformation

A represented change in choice, approval, denial, priority, or commitment.

10.3 Drift Transformation

A represented change that occurs without explicit intended action or outside declared process.

10.4 Update Transformation

A represented revision of an artifact, policy, model, state, schema, representation, or configuration.

10.5 Execution Transformation

A represented change resulting from executing code, command, workflow, plan, or procedure.

10.6 Observation Transformation

A represented change caused by new visibility.

Observation may transform the represented state without changing the underlying external condition.

10.7 Authorization Transformation

A represented change in permissibility.

Examples include allow, deny, escalation, revocation, delegation, or expired authority.

10.8 Evidence Update Transformation

A represented change in confidence caused by new evidence.

10.9 Settlement Transformation

A represented change from unsettled, partially settled, or claimed-complete status into a settlement status.

10.10 Capability Update Transformation

A represented change in durable ability to produce repeated settlement under variation.

10.11 Affordance Update Transformation

A represented change in the reachable transformation horizon.

10.12 Failure Transformation

A represented change showing that expected transformation did not occur or produced invalid consequence.

10.13 Reversal Transformation

A represented change that attempts to undo, compensate for, or supersede a prior transformation.

10.14 Repair Transformation

A represented change that resolves contradiction, violation, drift, defect, or settlement debt.

10.15 Escalation Transformation

A represented change that moves a decision, claim, evidence issue, or authority question to a different perspective or authority context.

10.16 Projection Transformation

A represented change into a projected future state.

10.17 Simulation Transformation

A represented change inside a counterfactual or simulated state space.

10.18 Generation Transformation

A represented change caused by generation of a new representation, scenario, benchmark case, answer, artifact, or plan.

11. Transformation Status

A Transformation SHOULD have one or more lifecycle statuses.

proposed
planned
attempted
executed
claimed_complete
observed
evidenced
partially_evidenced
contradicted
settlement_pending
settled
partially_settled
failed
blocked
reversed
repaired
escalated
superseded
unknown

11.1 Status Discipline

Transformation status MUST NOT be confused with transformation value.

A settled transformation may be harmful.

An executed transformation may be unauthorized.

A claimed-complete transformation may be unsettled.

A failed transformation may produce valuable evidence.

A blocked transformation may preserve authority.

12. Transformation Lifecycle

CEP recognizes the following general transformation lifecycle:

Proposed
→ Attempted
→ Executed or Blocked
→ Claimed
→ Observed
→ Evidenced
→ Settled or Unsettled
→ State Updated or Rejected
→ Affordance/Capability Updated when justified

This lifecycle is not mandatory for every transformation.

Some transformations begin as observations.

Some transformations are discovered after the fact.

Some transformations are simulated.

Some transformations remain permanently unsettled.

12.1 Lifecycle Requirement

A CEP implementation MUST preserve which lifecycle stages are known, unknown, skipped, inapplicable, or out of scope.

12.2 Lifecycle Failure

If lifecycle stages are collapsed, systems will overclaim completion, hide uncertainty, or confuse execution with settlement.

13. Invariants

An Invariant is a condition expected to remain preserved across transformation.

CEP evaluates transformations by checking whether specified invariants were preserved, violated, repaired, transformed, or made irrelevant.

13.1 Invariant Record

A Transformation SHOULD preserve:

invariant_id
invariant_type
description
source
applies_to
expected_status
observed_status
evidence_refs
violation_severity
confidence

13.2 Invariant Types

CEP recognizes the following invariant types:

identity
scope
authority
semantic
evidence
settlement
safety
security
performance
resource
temporal
capability
affordance
policy
schema
benchmark
unknown

13.3 Invariant Status

Invariant status SHOULD be one of:

preserved
violated
repaired
transformed
not_applicable
unknown

13.4 Invariant Failure

If invariants are absent, CEP cannot determine what matters about a transformation.

Without invariants, benchmark scoring collapses into output comparison.

14. Constraints Applied to Transformations

Transformations occur under constraints.

A CEP-compatible Transformation MUST preserve material constraints that govern possibility, permissibility, affordability, evidence sufficiency, and settlement readiness.

14.1 Constraint Roles

A constraint may function as:

enabling_constraint
blocking_constraint
authority_constraint
resource_constraint
evidence_constraint
settlement_constraint
scope_constraint
temporal_constraint
identity_constraint
semantic_constraint
risk_constraint

14.2 Constraint Failure

If transformation constraints are omitted, CEP cannot determine whether a transformation was reachable, permissible, executable, payable, or settleable.

15. Authority Relevance

A Transformation is authority-relevant when permissibility matters.

15.1 Authority-Relevant Transformations

Examples include:

file modification,

API call,

deployment,

commit,

data access,

policy change,

approval,

delegation,

escalation,

resource modification,

evidence alteration,

benchmark result publication.

15.2 Authority Evaluation Requirement

An authority-relevant Transformation MUST preserve:

actor_refs
authority_constraint_refs
governance_perspective_ref
proposed_transformation
authority_question_ref
decision
decision_evidence_refs
decision_time

15.3 Authority Decision Values

Authority decision MUST be one of:

allow
deny
escalate
unknown

15.4 Authority Failure

If authority-relevant Transformations lack authority context, they are not authority-valid.

If possibility is collapsed into permissibility, governance evaluation is invalid.

16. Evidence Hooks

A Transformation MUST be able to bind evidence.

Evidence hooks define what kind of evidence would support, weaken, contradict, qualify, or settle transformation claims.

16.1 Evidence Hook Record

A Transformation SHOULD preserve:

evidence_requirement_id
target_claim_ref
required_evidence_type
minimum_reliability
minimum_relevance
source_requirements
timing_requirements
settlement_threshold_ref

16.2 Evidence Requirement Examples

Transformation evidence may include:

execution_log
test_result
artifact_diff
monitoring_signal
audit_record
trace
policy_reference
human_attestation
configuration_snapshot
external_record
manual_inspection

16.3 Evidence Failure

If evidence hooks are absent, CEP cannot determine what would support or falsify a transformation claim.

Without evidence hooks, settlement becomes arbitrary.

17. Claims About Transformations

A Transformation may have one or more associated Claims.

17.1 Claim Types

Transformation claims MAY include:

transformation_occurred
transformation_did_not_occur
transformation_was_attempted
transformation_was_completed
transformation_was_authorized
transformation_was_unauthorized
transformation_preserved_invariant
transformation_violated_invariant
transformation_settled
transformation_failed
transformation_repaired
transformation_expanded_affordance
transformation_reduced_capability

17.2 Claim Requirement

Every Transformation Claim MUST be targetable by Evidence.

A Claim without possible evidence support is not settlement-valid.

18. Observed Consequences

A Transformation SHOULD preserve observed consequences when known.

18.1 Consequence Record

A consequence record SHOULD include:

consequence_id
consequence_type
affected_state_ref
affected_entities
description
observed_at
evidence_refs
confidence
severity
intended_or_unintended

18.2 Consequence Types

CEP recognizes:

intended
unintended
beneficial
harmful
neutral
unknown
delayed
reversible
irreversible
partial
contradictory

18.3 Consequence Failure

If consequences are absent, CEP cannot distinguish execution from outcome.

If harmful consequences are hidden because the transformation was intended, settlement evaluation is corrupted.

19. Payment Burden

Payment burden is the cost required to perform, evidence, govern, or settle a transformation.

Payment burden MAY include:

time
attention
energy
money
coordination
risk
complexity
technical_debt
emotional_cost
opportunity_cost
authority_cost
evidence_cost
settlement_cost

19.1 Payment Burden Record

A Transformation SHOULD preserve payment burden when relevant to affordance or capability evaluation.

payment_burden_id
burden_types
estimated_burden
observed_burden
payer_refs
constraints
confidence

19.2 Payment Failure

If payment burden is omitted, CEP may confuse possible transformation with affordable transformation.

This breaks affordance and capability evaluation.

20. Transformation Validity

A Transformation may be valid in one dimension and invalid in another.

CEP recognizes the following validity dimensions:

representation_validity
state_validity
identity_validity
scope_validity
temporal_validity
semantic_validity
authority_validity
evidence_validity
settlement_validity
capability_validity
affordance_validity
benchmark_validity

20.1 Validity Discipline

A CEP implementation MUST NOT collapse validity dimensions.

Example:

A deployment transformation may be execution-valid and evidence-valid while authority-invalid.

Another transformation may be authority-valid but settlement-invalid due to missing consequence evidence.

21. Transformation Comparison

Transformation comparison identifies similarity, difference, repetition, drift, repair, regression, or capability development across transformations.

21.1 Comparison Context

A valid Transformation comparison MUST preserve:

transformation_a_ref
transformation_b_ref
comparison_question_ref
identity_basis
scope_alignment
time_alignment
invariant_refs
confidence

21.2 Comparison Types

CEP recognizes:

same_transformation
similar_transformation
repeated_transformation
drifted_transformation
repaired_transformation
regressed_transformation
counterfactual_comparison
expected_vs_observed
claimed_vs_evidenced
authorized_vs_executed
settled_vs_unsettled

21.3 Comparison Failure

A comparison is invalid if identity, scope, or question are not preserved.

22. Transformation Operations

CEP-compatible implementations MAY perform operations over Transformations.

Operations MUST preserve provenance, identity, scope, uncertainty, and evidence implications.

22.1 Create Transformation

Creates a Transformation record from source and target-like States.

Required outputs:

transformation_id
source_state_ref
target_state_ref OR target_claim
affected_entities
scope
identity_basis
status
provenance_refs

22.2 Classify Transformation

Assigns Transformation type, status, and validity dimensions.

Classification MUST preserve classification basis.

22.3 Validate Transformation

Checks whether a Transformation satisfies required constraints, invariants, and context.

Validation MUST distinguish schema validity from semantic, authority, evidence, settlement, and benchmark validity.

22.4 Diff Transformation

Identifies changed constraints, distinctions, relations, and State attributes.

Diff MUST preserve identity assumptions.

22.5 Bind Evidence

Connects Evidence records to Transformation Claims, Invariants, or Consequences.

Binding MUST preserve relevance and reliability.

22.6 Evaluate Authority

Determines whether the Transformation was permissible.

Authority evaluation MUST return allow, deny, escalate, or unknown.

22.7 Evaluate Settlement

Determines whether Transformation consequences are sufficiently registered for State update.

Settlement evaluation MUST NOT treat completion claim as settlement.

22.8 Update State

Produces a State update from an evidenced or settled Transformation.

Update MUST preserve prior state, new state, settlement status, and evidence basis.

22.9 Reverse Transformation

Represents an attempted reversal, rollback, compensation, or supersession.

A reversal is itself a Transformation.

It MUST NOT erase the original Transformation.

22.10 Repair Transformation

Represents a corrective change addressing violation, contradiction, drift, or settlement debt.

A repair is itself a Transformation.

It MUST preserve the failure or violation it repairs.

22.11 Project Transformation

Represents a possible, predicted, simulated, or counterfactual change.

Projection MUST be marked as projected and MUST NOT be treated as observed or settled.

23. Transformation Chains

A Transformation Chain is an ordered set of related Transformations.

23.1 Chain Use

Transformation Chains support:

process evaluation,

agent trace evaluation,

capability evaluation,

settlement history,

affordance evolution,

root cause analysis,

benchmark campaigns,

semantic exhaust,

organizational memory.

23.2 Chain Record

A Transformation Chain SHOULD preserve:

chain_id
transformation_refs
ordering_rule
shared_subject_refs
shared_scope
chain_question_ref
chain_invariants
chain_status
confidence

23.3 Chain Failure

If chains are not preserved, CEP cannot evaluate repeated settlement, capability development, process drift, or cumulative affordance change.

24. Transformation and Reality Gap

Reality Gap evaluation depends on Transformations connecting or comparing Declared and Observed States.

24.1 Reality Gap Transformation Pattern

A minimal Reality Gap pattern is:

Declared State
→ Expected Transformation or Declared Invariant
→ Observed State
→ Divergence Claim
→ Evidence
→ Gap Classification

24.2 Reality Gap Failure

Reality Gap evaluation is invalid if:

Declared State and Observed State collapse,

transformation history is absent when needed,

divergence question is absent,

evidence is not bound to the gap claim,

or identity continuity is unresolved.

25. Transformation and Authority

Authority evaluation asks whether a proposed, attempted, executed, or settled Transformation was permissible under applicable constraints.

25.1 Minimal Authority Transformation Pattern

Actor
→ Proposed Transformation
→ Authority Constraint
→ Governance Perspective
→ Authority Decision
→ Evidence

25.2 Authority Failure

Authority evaluation is invalid if:

actor is unknown when actor matters,

authority constraints are omitted,

applicable scope is absent,

decision is not allow, deny, escalate, or unknown,

or capability is treated as authority.

26. Transformation and Settlement

Settlement evaluation asks whether a Transformation has produced reliable consequence registration sufficient for State update.

26.1 Minimal Settlement Transformation Pattern

Source State
→ Transformation
→ Completion Claim
→ Observed Consequence
→ Evidence
→ Settlement Status
→ State Update

26.2 Settlement Failure

Settlement evaluation is invalid if:

completion claim is treated as settlement,

evidence is missing,

consequences are not represented,

contradictions are hidden,

or settled status implies success, approval, or benefit.

27. Transformation and Capability

Capability evaluation depends on repeated settled Transformations under variation.

27.1 Minimal Capability Transformation Pattern

Transformation Chain
→ Settlement History
→ Variation Context
→ Payment Burden Before
→ Payment Burden After
→ Affordance Delta
→ Capability Claim

27.2 Capability Failure

Capability evaluation is invalid if:

only one transformation is considered,

settlement is missing,

variation is absent,

payment burden is not represented,

or performance is treated as capability.

28. Transformation and Affordance

Affordance evaluation asks which Transformations are reachable from current State.

28.1 Minimal Affordance Transformation Pattern

Current State
→ Candidate Transformation
→ Constraint Check
→ Authority Check
→ Capability Check
→ Payment Burden Check
→ Settlement Requirement Check
→ Reachability Status

28.2 Affordance Failure

Affordance evaluation is invalid if:

theoretical possibility is treated as reachability,

payment burden is omitted,

authority is omitted when material,

settlement requirements are unknown,

or current State is insufficient.

29. Transformation and Semantic Envelope

A Semantic Envelope MUST be capable of carrying Transformation context.

A Transformation carried in a Semantic Envelope SHOULD include:

transformation_id
source_state_refs
target_state_refs
transformation_type
status
scope
time_context
identity_basis
actor_refs
constraint_refs
question_refs
evidence_refs
settlement_refs
authority_refs
affordance_delta_refs
capability_delta_refs
provenance_refs
uncertainty_record
omission_record

A Semantic Envelope MUST preserve whether Transformation context is complete, partial, unknown, or out of scope.

30. Transformation and Benchmark Cases

A benchmark case is often structured around one or more Transformations.

30.1 Benchmark Transformation Requirements

A CEP-compatible benchmark case SHOULD preserve:

case_id
benchmark_ref
question_ref
source_state_refs
transformation_refs
expected_target_state_refs
answer_key_refs
evidence_requirements
invariants
scoring_rules
invalidity_conditions

30.2 Benchmark Failure

A benchmark case is invalid if the Transformation being evaluated cannot be identified, if expected invariants are unknown, or if the scoring question is absent.

31. Minimal Valid Transformation

A minimally valid CEP Transformation MUST preserve:

transformation_id
transformation_type
source_state_ref
target_state_ref OR claimed_target_state_ref OR observed_target_state_ref
scope
time_context OR temporal_uncertainty
identity_basis OR identity_uncertainty
affected_entities
affected_distinctions OR affected_constraints
status
confidence OR confidence_status
provenance_refs

A minimally valid Transformation SHOULD preserve:

question_refs
evidence_refs
authority_refs
expected_invariants
observed_consequences
settlement_refs
payment_burden

A Transformation lacking source State is invalid.

A Transformation lacking all target-like State references or target claims is invalid.

A Transformation lacking identity basis or identity uncertainty is invalid.

32. Invalid Transformation Conditions

A Transformation is invalid for CEP evaluation if:

it lacks source State,

it lacks target-like State or target claim,

it lacks scope,

it lacks identity basis or identity uncertainty,

it collapses action into transformation,

it collapses claimed completion into settlement,

it collapses expected target into observed target,

it collapses observed target into settled target,

it treats possibility as permissibility,

it lacks authority context when authority is material,

it lacks evidence hooks when settlement is claimed,

it hides material contradictions,

it omits affected distinctions,

it cannot identify applicable invariants,

or it cannot answer the benchmark question for which it is used.

Invalid Transformations MAY still be stored.

Invalid Transformations MUST NOT be used for settlement, capability, authority, affordance, or benchmark scoring unless the invalidity itself is the object of evaluation.

33. Transformation Invariants

CEP-compatible systems SHALL preserve the following Transformation invariants.

Invariant 1 — Transformation Is Represented Change

A Transformation SHALL remain distinct from Action.

Invariant 2 — State Anchoring

A Transformation SHALL reference source and target-like States.

Invariant 3 — Identity Continuity

A Transformation SHALL preserve identity basis or identity uncertainty.

Invariant 4 — Scope Preservation

A Transformation SHALL preserve scope.

Invariant 5 — Temporal Preservation

A Transformation SHALL preserve relevant time context.

Invariant 6 — Affected Difference Preservation

A Transformation SHALL preserve affected constraints, distinctions, or relations.

Invariant 7 — Target Role Separation

Expected, claimed, observed, actual, and settled target States SHALL remain separable.

Invariant 8 — Authority Separation

Permissibility SHALL remain distinct from possibility and capability.

Invariant 9 — Evidence Traceability

Transformation Claims SHALL be traceable to Evidence or marked unsupported.

Invariant 10 — Settlement Separation

Settlement SHALL remain distinct from execution, completion, success, approval, and benefit.

Invariant 11 — Consequence Preservation

Known consequences SHALL be preserved, including harmful, unintended, delayed, partial, and contradictory consequences.

Invariant 12 — Reversal Preservation

Reversal or repair SHALL NOT erase the original Transformation.

34. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:

action into transformation
transformation into action
execution into consequence
completion into settlement
settlement into success
settlement into approval
possibility into permissibility
capability into authority
expected target into observed target
claimed target into evidenced target
observed target into settled target
source state into target state
projection into observation
simulation into execution
reversal into deletion
repair into absence of failure
evidence update into truth
confidence into certainty

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

35. Transformation Conformance

A CEP-compatible Transformation implementation MUST:

represent Transformations explicitly,

distinguish Action from Transformation,

preserve source State,

preserve target-like State or target claim,

preserve identity basis or uncertainty,

preserve scope,

preserve relevant time context,

preserve affected constraints, distinctions, or relations,

preserve status,

preserve expected invariants when used for evaluation,

preserve authority context when authority is material,

preserve evidence hooks when evidence is required,

preserve observed consequences when known,

distinguish expected, claimed, observed, actual, and settled targets,

distinguish completion from settlement,

preserve provenance,

preserve uncertainty and omissions,

support Transformation comparison,

support Transformation chains,

and reject or warn on anti-collapse violations.

36. Implementation Consequence

A CEP-compatible system that evaluates benchmark cases, agent work, organizational behavior, authority, settlement, capability, or affordance must implement the Transformation Model.

A system that only evaluates final outputs is not CEP-compliant.

A system that only records actions is not CEP-compliant.

A system that records executed actions without consequence, evidence, identity, scope, and settlement context cannot perform CEP-compliant evaluation.

This requirement exists because CEP evaluates represented transformations through evidence-backed settlement.

37. Closing Definition

A Transformation is represented change between States under preserved identity, scope, constraints, and evaluation context.

CEP uses Transformations to determine what changed, what should have changed, what was claimed to have changed, what was observed to have changed, what was evidenced, what settled, what became permissible, what became reachable, and what became repeatable.

The Transformation Model is therefore the spine of CEP.

Without explicit Transformations, there is no Reality Gap, no Authority evaluation, no Settlement evaluation, no Capability evaluation, and no affordance horizon expansion.

The next document should be CEP-0005 — Question Model. That will formalize questions as constraints over observation and relevance, which is what makes benchmarks, evidence, and scoring directed instead of arbitrary.