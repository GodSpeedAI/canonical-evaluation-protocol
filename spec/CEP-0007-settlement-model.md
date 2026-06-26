---
type: CEP Specification
id: CEP-0007
title: Settlement Model
description: This document defines the CEP Settlement Model.
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
- CEP-0004
- CEP-0005
- CEP-0006
supersedes: []
superseded_by: []
conformance_class: null
benchmark_family: null
schema_ref: null
defines:
- Settlement
- Settlement Threshold
- Settlement Debt
- Settlement Horizon
- Settlement Latency
- Settlement Cost
- Settlement Status
- Settlement Dimensions
used_by:
- CEP-0008
- CEP-0009
- CEP-0010
related:
- CEP-0006
- CEP-0008
---

# CEP-0007 — Settlement Model

## Navigation

**Depends on:** [CEP-0000](./CEP-0000-derivation-ladder.md), [CEP-0001](./CEP-0001-ontology.md), and the prior protocol chain through [CEP-0006](./CEP-0006-evidence-model.md)
**Defines:** Settlement, Settlement Threshold, Settlement Debt, Settlement Horizon, Settlement Latency, Settlement Cost, Settlement Status, Settlement Dimensions
**Used by:** [CEP-0008](./CEP-0008-semantic-envelope.md), [CEP-0009](./CEP-0009-benchmark-model.md), [CEP-0010](./CEP-0010-conformance.md)

## Abstract

This document defines the CEP Settlement Model.

CEP evaluates represented transformations through evidence-backed settlement.

Settlement is reliable consequence registration after transformation.

Settlement does not mean success.

Settlement does not mean approval.

Settlement does not mean benefit.

Settlement does not mean moral legitimacy.

Settlement does not mean task completion.

Settlement means that the represented consequences of a transformation are sufficiently evidenced, bounded, and coherent for a specified evaluation context to update state, preserve uncertainty, or register unresolved contradiction.

The Settlement Model defines how transformations become settled, partially settled, unsettled, failed, reversed, harmful, unauthorized, debt-bearing, or settlement-blocked.

## 1. Purpose

The purpose of the Settlement Model is to prevent CEP implementations from prematurely treating claims of completion as consequence-backed state updates.

Most systems overvalue completion.

- CEP separates:
- attempted action
- executed action
- claimed completion
- observed consequence
- evidenced consequence
- settled consequence
- state update
- capability update
- affordance update

A CEP-compatible implementation MUST preserve these distinctions.

Without settlement, systems cannot distinguish:
- “the agent said it finished,”
- “the action executed,”
- “the expected change occurred,”
- “the consequence was observed,”
- “the consequence was evidenced,”
- “the consequence was safe,”
- “the consequence was authorized,”
- “the consequence was beneficial,”

and “the system may now update future action based on this result.”

## 2. Scope

This document defines:
- settlement definition
- settlement sufficiency
- settlement identity
- settlement target
- settlement context
- settlement status
- settlement thresholds
- settlement horizons
- settlement evidence
- settlement contradictions
- settlement debt
- settlement failure
- settlement operations
- settlement and state update
- settlement and authority
- settlement and capability
- settlement and affordance
- settlement and benchmarks
- conformance requirements
- anti-collapse rules

This document does not define:
- universal scoring weights
- benchmark-specific settlement metrics
- legal liability
- moral evaluation
- final [Semantic Envelope](./CEP-0008-semantic-envelope.md) serialization
- runner implementation

Those are defined in later CEP specifications or domain-specific profiles.

## 3. Core Definition

Settlement is reliable consequence registration after [Transformation](./CEP-0004-transformation-model.md).

A Settlement occurs when available Evidence is sufficient for a [Question](./CEP-0005-question-model.md) and evaluation context to determine whether a represented Transformation may update State, remain unsettled, fail, reverse, produce debt, or require further observation.

A Settlement MUST preserve:
- settlement_id
- transformation_ref
- question_ref
- settlement_status
- evidence_refs
- observed_consequence_refs
- confidence
- threshold_ref
- state_update_refs
- unresolved_contradictions
- missing_evidence
- settled_at OR settlement_time_context
- limitations

Settlement is always question-bound.

A transformation may be settled for one Question and unsettled for another.

## 4. Settlement Is Not Completion

CEP SHALL distinguish Completion from Settlement.

### 4.1 Completion

Completion is a Claim that work, action, execution, or task performance is done.

Completion may be asserted by:
- human
- agent
- tool
- workflow
- model
- system
- process
- ticket
- status flag
- benchmark response

### 4.2 Settlement

Settlement is consequence-backed state readiness.

Settlement requires evidence about what changed, what consequence followed, what contradictions remain, and whether the evaluation context can safely update state.

### 4.3 Anti-Collapse Rule

A CEP implementation MUST NOT treat completion claims as settlement.

A completion claim MAY become evidence, but only with declared relevance and reliability.

## 5. Settlement Is Not Success

CEP SHALL distinguish Settlement from Success.

A transformation may be settled and unsuccessful.

Examples:

The deployment failed and rollback completed.
The unauthorized deletion occurred and is evidenced.
The process drifted and the drift is confirmed.
The agent violated policy and the violation is settled.

In each case, the consequence may be settled even though the result is undesirable.

### 5.1 Anti-Collapse Rule

A CEP implementation MUST NOT treat settlement status as success status.

## 6. Settlement Is Not Approval

CEP SHALL distinguish Settlement from Approval.

Approval concerns legitimacy, authorization, preference, or acceptance.

Settlement concerns reliable consequence registration.

A transformation may be:
- approved_but_unsettled
- unapproved_but_settled
- authorized_but_failed
- unauthorized_but_settled
- beneficial_but_unapproved
- harmful_but_settled

### 6.1 Anti-Collapse Rule

A CEP implementation MUST NOT treat settled consequence as approval, authorization, endorsement, or normative acceptance.

## 7. Settlement Is Not Evidence

CEP SHALL distinguish [Evidence](./CEP-0006-evidence-model.md) from Settlement.

Evidence changes confidence.

Settlement determines whether evidence is sufficient for consequence registration under a [Question](./CEP-0005-question-model.md).

A single evidence record may support settlement.

It is not settlement by itself.

### 7.1 Anti-Collapse Rule

A CEP implementation MUST NOT treat evidence existence as settlement sufficiency.

## 8. Settlement Sufficiency

A Settlement is sufficient when the evaluation context can update [State](./CEP-0003-state-model.md) or preserve an explicit unsettled condition without hiding material contradiction.

### 8.1 Required Settlement Fields

A CEP-compatible Settlement MUST preserve:
- settlement_id
- settlement_status
- transformation_ref
- question_ref
- evidence_refs
- observed_consequence_refs
- threshold_ref
- confidence
- unresolved_contradictions
- missing_evidence
- state_update_recommendation
- time_context
- scope
- provenance_refs

### 8.2 Conditional Settlement Fields

A Settlement SHOULD preserve the following when materially relevant:

- authority_status
- approval_status
- success_status
- benefit_status
- harm_status
- reversibility_status
- debt_status
- settlement_horizon
- settlement_latency
- settlement_cost
- observer_refs
- perspective_refs
- benchmark_refs
- capability_update_refs
- affordance_delta_refs
- risk_record

### 8.3 Settlement-Sufficiency Failure

A Settlement is not CEP-valid if it lacks a [Transformation](./CEP-0004-transformation-model.md), Question, Evidence basis, and status.

A Settlement is not state-update-valid if it does not specify whether and how State may be updated.

A Settlement is not benchmark-valid if it lacks threshold, answer shape, or scoring relevance.

## 9. Settlement Target

A Settlement MUST target something.

The primary settlement target is usually a [Transformation](./CEP-0004-transformation-model.md).

Settlement MAY also target:
- state_update
- authority_decision
- evidence_claim
- capability_claim
- affordance_claim
- benchmark_result
- conformance_result
- repair_claim
- risk_claim

### 9.1 Target Binding Record

A Settlement target binding SHOULD preserve:
- settlement_ref
- target_type
- target_ref
- question_ref
- claim_refs
- evidence_refs
- state_update_refs
- confidence
- limitations

### 9.2 Target Failure

A Settlement without a target is uninterpretable.

## 10. Settlement Question Binding

Settlement exists relative to a [Question](./CEP-0005-question-model.md).

### 10.1 Question Binding Record

A Settlement SHOULD preserve:
- question_ref
- question_type
- answer_shape_ref
- settlement_requirements
- threshold_ref
- evaluation_context

### 10.2 Example

A transformation may be settled under:
- "Did the file change occur?"
but unsettled under:
- "Did the change reduce production risk?"

### 10.3 Question Binding Failure

If Settlement is not bound to a Question, settlement may be overgeneralized beyond its evidence.

## 11. Settlement Status

CEP recognizes the following top-level Settlement statuses.

- unsettled
- partially_settled
- settled
- failed
- blocked
- reversed
- superseded
- harmful_but_settled
- beneficial_but_unsettled
- unauthorized_but_settled
- authorized_but_unsettled
- settled_with_debt
- unknown

### 11.1 Unsettled

The consequence is not sufficiently registered for the evaluation context.

### 11.2 Partially Settled

Some consequences are registered, but material evidence, scope, identity, authority, or contradiction issues remain.

### 11.3 Settled

Consequences are sufficiently registered to update State for the specified [Question](./CEP-0005-question-model.md) and context.

### 11.4 Failed

The transformation did not produce the expected, claimed, or required consequence.

Failure may itself be settled.

### 11.5 Blocked

The transformation did not proceed because a constraint prevented it.

A blocked transformation may be a valid settlement if the blocking condition is evidenced.

### 11.6 Reversed

A later transformation reversed, rolled back, compensated for, or superseded the prior transformation.

Reversal does not erase the original transformation.

### 11.7 Superseded

A later settlement replaces the earlier settlement for future evaluation while preserving historical record.

### 11.8 Harmful But Settled

The consequence is reliably registered and harmful.

### 11.9 Beneficial But Unsettled

The consequence appears beneficial, but evidence is insufficient for settlement.

### 11.10 Unauthorized But Settled

The consequence is reliably registered, but authority constraints were violated.

### 11.11 Authorized But Unsettled

The transformation was permissible, but consequences remain insufficiently registered.

### 11.12 Settled With Debt

The consequence is sufficiently registered for limited state update, but unresolved work, risk, contradiction, cleanup, review, or evidence gap remains.

### 11.13 Unknown

Settlement status cannot be determined from available representation.

## 12. Settlement Dimensions

Settlement status MAY be decomposed into dimensions.

A CEP-compatible system SHOULD preserve relevant dimensions rather than forcing one flat status.

### 12.1 Core Dimensions

- consequence_registration
- evidence_sufficiency
- identity_continuity
- scope_alignment
- temporal_resolution
- authority_resolution
- contradiction_resolution
- reversibility_resolution
- risk_resolution
- state_update_readiness

### 12.2 Dimension Values

Each dimension SHOULD support values such as:

- satisfied
- partially_satisfied
- unsatisfied
- blocked
- unknown
- not_applicable

### 12.3 Dimensional Failure

If settlement is represented as one undifferentiated status, systems may hide why a transformation is unsettled or settled only in a limited context.

## 13. Settlement Threshold

A Settlement Threshold defines what evidence and contradiction conditions are sufficient for a specific settlement decision.

### 13.1 Threshold Record

A Settlement Threshold SHOULD preserve:
- threshold_id
- question_ref
- evaluation_context
- required_evidence_types
- minimum_relevance
- minimum_reliability
- minimum_confidence
- required_independence
- allowed_contradictions
- blocking_contradictions
- time_requirements
- authority_requirements
- state_update_requirements

### 13.2 Threshold Discipline

Thresholds MUST be declared or derivable before settlement scoring.

Different Questions may require different thresholds.

Example:

A local formatting change may require only diff evidence and test evidence.

A production deployment may require approval evidence, execution evidence, monitoring evidence, rollback readiness, and authority evidence.

### 13.3 Threshold Failure

If threshold is absent, settlement becomes arbitrary.

A system may over-settle trivial evidence or under-settle sufficient evidence.

## 14. Settlement Horizon

Settlement Horizon describes the time scale over which consequences must be observed.

### 14.1 Horizon Types

- CEP recognizes:
- immediate
- short
- delayed
- long
- recurring
- unknown

### 14.2 Immediate Settlement

Consequences can be registered immediately after transformation.

Example:

A file hash changed.
A unit test passed.
A command returned expected output.

### 14.3 Short Settlement

Consequences require short follow-up.

Example:

A service deploys and remains healthy for a defined monitoring window.

### 14.4 Delayed Settlement

Consequences require delayed observation.

Example:

A process change reduces defect escapes over several cycles.

### 14.5 Long Settlement

Consequences require extended observation.

Example:

A capability improvement reduces coordination cost over a quarter.

### 14.6 Recurring Settlement

Consequences must repeatedly settle across repeated transformations.

Example:

A team repeatedly executes governed agentic workflows without authority drift.

### 14.7 Horizon Failure

If horizon is omitted, CEP may prematurely settle delayed consequences.

## 15. Settlement Evidence

Settlement requires Evidence relevant to the settlement [Question](./CEP-0005-question-model.md).

### 15.1 Settlement Evidence Record

Settlement [Evidence](./CEP-0006-evidence-model.md) SHOULD preserve:
- settlement_ref
- transformation_ref
- claim_refs
- evidence_refs
- required_evidence_refs
- missing_evidence
- evidence_sufficiency_status
- contradiction_refs
- confidence_impact

### 15.2 Evidence Sufficiency Status

Evidence sufficiency SHOULD be one of:
- sufficient
- partially_sufficient
- insufficient
- contradicted
- unknown

### 15.3 Evidence Failure

If Settlement lacks evidence sufficiency assessment, it is not settlement-valid.

## 16. Settlement Contradictions

A Settlement MUST preserve material contradictions.

### 16.1 Contradiction Record

A Settlement contradiction record SHOULD preserve:
- contradiction_ref
- settlement_ref
- affected_claim_refs
- affected_evidence_refs
- severity
- resolution_status
- impact_on_settlement
- required_resolution

### 16.2 Blocking Contradiction

A blocking contradiction prevents settlement under the current threshold.

### 16.3 Non-Blocking Contradiction

A non-blocking contradiction does not prevent settlement, but MUST be preserved.

### 16.4 Contradiction Failure

A Settlement with hidden material contradiction is invalid.

## 17. Missing Evidence

Settlement MUST preserve missing evidence when evidence is insufficient.

### 17.1 Missing Evidence Record

A missing evidence record SHOULD preserve:
- missing_evidence_id
- settlement_ref
- required_evidence_type
- reason_required
- impact
- collection_path
- blocking_status

### 17.2 Blocking Status

Missing evidence may be:
- blocking
- non_blocking
- optional
- unknown

### 17.3 Missing Evidence Failure

If missing evidence is hidden, unsettled transformations may be falsely treated as settled.

## 18. Settlement Debt

Settlement Debt is unresolved burden created when a transformation is allowed to proceed, partially settle, or update [State](./CEP-0003-state-model.md) despite remaining evidence, contradiction, repair, governance, cleanup, monitoring, or capability obligations.

Settlement Debt is not necessarily bad.

It must be represented.

### 18.1 Settlement Debt Record

A Settlement Debt record SHOULD preserve:
- debt_id
- settlement_ref
- debt_type
- description
- created_by_transformation_ref
- blocking_status
- owner_ref
- due_condition
- risk_if_unresolved
- evidence_requirements
- repair_transformation_refs
- status

### 18.2 Debt Types

- CEP recognizes:
- evidence_debt
- authority_debt
- repair_debt
- monitoring_debt
- documentation_debt
- identity_debt
- scope_debt
- contradiction_debt
- capability_debt
- affordance_debt
- technical_debt
- coordination_debt
- unknown

### 18.3 Debt Status

Debt status SHOULD be one of:
- open
- accepted
- in_progress
- resolved
- superseded
- expired
- unknown

### 18.4 Debt Failure

If debt is hidden, partial settlement becomes false finality.

Settlement with debt MUST NOT be treated as fully settled without qualification.

## 19. Settlement Latency

Settlement Latency is the time between [Transformation](./CEP-0004-transformation-model.md) and Settlement.

### 19.1 Latency Record

A latency record SHOULD preserve:
- transformation_ref
- settlement_ref
- transformation_time
- settlement_time
- latency_value
- latency_unit
- horizon_type
- latency_reason

### 19.2 Latency Use

Settlement Latency supports:
- capability evaluation
- process improvement
- evidence bottleneck detection
- governance delay detection
- benchmark scoring
- affordance analysis

### 19.3 Latency Failure

If latency is omitted, CEP cannot tell whether a system is becoming faster at settling transformations.

## 20. Settlement Cost

Settlement Cost is the payment burden required to reach settlement.

### 20.1 Cost Record

A settlement cost record SHOULD preserve:
- settlement_ref
- cost_types
- estimated_cost
- actual_cost
- payer_refs
- evidence_cost
- coordination_cost
- authority_cost
- monitoring_cost
- confidence

### 20.2 Cost Types

Settlement cost MAY include:
- time
- attention
- money
- coordination
- risk
- complexity
- technical_debt
- emotional_cost
- opportunity_cost
- authority_cost
- evidence_cost
- monitoring_cost

### 20.3 Cost Failure

If settlement cost is omitted, CEP cannot evaluate whether capability improved through reduced future payment burden.

## 21. Settlement Operations

CEP-compatible implementations MAY perform settlement operations.

Operations MUST preserve evidence, threshold, state update, contradiction, and debt implications.

### 21.1 Evaluate Settlement

Determines settlement status for a [Transformation](./CEP-0004-transformation-model.md) under a Question and Threshold.

- Required inputs:
- transformation_ref
- question_ref
- evidence_refs
- threshold_ref
- observed_consequence_refs
- state_refs
- Required outputs:
- settlement_status
- confidence
- missing_evidence
- unresolved_contradictions
- state_update_recommendation
- limitations

### 21.2 Register Settlement

Creates a Settlement record.

Registration MUST preserve provenance and time context.

### 21.3 Update State From Settlement

Applies settled consequence to produce [State](./CEP-0003-state-model.md) update.

State update MUST preserve Settlement reference.

### 21.4 Mark Unsettled

Marks transformation as unsettled and records why.

### 21.5 Mark Partially Settled

Marks which dimensions are settled and which remain unresolved.

### 21.6 Record Settlement Debt

Creates debt record for unresolved obligations.

### 21.7 Supersede Settlement

Marks one Settlement as superseded by another.

Supersession MUST NOT delete the prior Settlement.

### 21.8 Reverse Settlement

Marks a prior Settlement as reversed or invalidated by later evidence or transformation.

Reversal MUST preserve reason and evidence.

### 21.9 Reopen Settlement

Reopens a prior Settlement due to new evidence, contradiction, drift, or invalid assumption.

### 21.10 Compare Settlements

Compares Settlements across transformations, time, teams, benchmarks, or capability contexts.

## 22. Settlement and State Update

Settlement enables [State](./CEP-0003-state-model.md) update.

A State MUST NOT be updated as settled unless the Settlement Model requirements are satisfied or the update is explicitly marked as provisional.

### 22.1 State Update Recommendation

A Settlement SHOULD produce one of:
- update_state
- do_not_update_state
- update_state_with_debt
- update_state_provisionally
- revert_state
- escalate
- unknown

### 22.2 State Update Record

A Settlement-based State update SHOULD preserve:
- prior_state_ref
- new_state_ref
- settlement_ref
- transformation_ref
- evidence_refs
- update_reason
- confidence
- debt_refs
- limitations

### 22.3 State Update Failure

If State is updated without Settlement or provisional marking, CEP cannot distinguish asserted change from consequence-backed change.

## 23. Settlement and Authority

Settlement does not imply authority.

A transformation may settle while violating authority.

### 23.1 Authority-Aware Settlement

A Settlement SHOULD preserve authority status when authority is material.

- authority_status
- authority_decision_ref
- authority_evidence_refs
- authority_contradictions

### 23.2 Authority Status Values

- authorized
- unauthorized
- escalated
- unknown
- not_applicable

### 23.3 Authority Failure

If a settled transformation is treated as authorized because it occurred, CEP collapses occurrence into permissibility.

## 24. Settlement and Success

Settlement does not imply success.

A Settlement SHOULD preserve success status separately when success matters.

### 24.1 Success Status Values

- successful
- unsuccessful
- partially_successful
- harmful
- unknown
- not_applicable

### 24.2 Success Failure

If successful outcome is inferred from settlement, harmful but settled transformations may be hidden.

## 25. Settlement and Benefit

Settlement does not imply benefit.

A Settlement MAY preserve benefit status when evaluation requires it.

### 25.1 Benefit Status Values

- beneficial
- harmful
- neutral
- mixed
- unknown
- not_applicable

### 25.2 Benefit Failure

If benefit is inferred from settlement, CEP confuses reality registration with normative evaluation.

## 26. Settlement and Capability

Capability requires repeated Settlement under variation.

A single Settlement is insufficient to establish Capability.

### 26.1 Capability-Relevant Settlement Record

A capability-relevant Settlement SHOULD preserve:
- settlement_ref
- transformation_family_ref
- variation_context
- payment_burden
- latency
- evidence_cost
- repeatability_indicators
- affordance_delta_refs

### 26.2 Capability Failure

If Capability is inferred from isolated Settlement, CEP cannot distinguish repeatable ability from one-time occurrence.

## 27. Settlement and Affordance

Affordance depends on what transformations become reachable after Settlement.

A Settlement MAY expand, constrain, reveal, or invalidate affordances.

### 27.1 Affordance Delta Record

A Settlement SHOULD preserve affordance delta when relevant.

- settlement_ref
- prior_affordance_refs
- new_affordance_refs
- blocked_affordance_refs
- changed_payment_burden
- changed_authority_requirements
- changed_evidence_requirements
- confidence

### 27.2 Affordance Failure

If Settlement does not update affordance horizon, systems may complete work without learning what became newly reachable.

## 28. Settlement and Reality Gap

Reality Gap settlement registers whether a declared-observed divergence is sufficiently evidenced.

### 28.1 Reality Gap Settlement Pattern

[Declared State](./CEP-0003-state-model.md)
→ **[Observed State](./CEP-0003-state-model.md)**
→ **Divergence [Question](./CEP-0005-question-model.md)**
→ **Gap Claim**
→ **Gap [Evidence](./CEP-0006-evidence-model.md)**
→ **Gap Settlement Status**

### 28.2 Gap Settlement Outcomes

- gap_settled
- gap_partially_settled
- gap_unsettled
- no_gap_settled
- gap_contradicted
- gap_unknown

### 28.3 Reality Gap Failure

If gap claims are scored without evidence-backed settlement, Reality Gap evaluation becomes unsupported assertion.

## 29. Settlement and Benchmarks

A CEP-compatible [Benchmark](./CEP-0009-benchmark-model.md) SHOULD include settlement requirements when evaluating transformation consequence.

### 29.1 Benchmark Settlement Requirement Record

A benchmark settlement requirement SHOULD preserve:
- benchmark_ref
- case_ref
- question_ref
- settlement_threshold_ref
- required_evidence_types
- allowed_statuses
- missing_evidence_penalty
- premature_completion_penalty
- contradiction_penalty
- state_update_rules

### 29.2 Benchmark Settlement Failure

A benchmark that rewards completion without settlement is not evaluating CEP settlement.

SettlementBench MUST penalize premature completion.

CapabilityBench MUST require repeated settlement history.

## 30. Premature Completion

Premature Completion occurs when a system claims completion, success, readiness, or state update before Settlement requirements are satisfied.

### 30.1 Premature Completion Record

A premature completion record SHOULD preserve:
- claim_ref
- transformation_ref
- missing_evidence
- unresolved_contradictions
- unsatisfied_thresholds
- prematurity_severity
- potential_harm
- confidence

### 30.2 Prematurity Severity

Prematurity severity SHOULD consider:
- evidence_missing
- contradiction_level
- authority_uncertainty
- risk_exposure
- state_update_impact
- reversibility
- time_horizon

### 30.3 Premature Completion Failure

A system that cannot detect premature completion cannot perform CEP-compliant settlement evaluation.

## 31. Settlement Failure

Settlement Failure occurs when a transformation cannot settle under the required threshold.

### 31.1 Failure Reasons

Settlement may fail because of:
- missing_evidence
- contradictory_evidence
- identity_uncertainty
- scope_mismatch
- authority_violation
- temporal_uncertainty
- consequence_absence
- source_unreliability
- integrity_failure
- threshold_not_met
- benchmark_invalidity
- unknown

### 31.2 Failure Record

A Settlement Failure record SHOULD preserve:
- failure_id
- settlement_ref
- failure_reason
- blocking_conditions
- required_repair
- required_evidence
- escalation_path
- confidence

### 31.3 Failure Value

A failed Settlement may still produce valuable evidence.

Failure MUST NOT be discarded simply because it did not settle.

## 32. Settlement Reversal

A Settlement may be reversed or invalidated by later evidence, contradiction, correction, or transformation.

### 32.1 Reversal Record

A reversal record SHOULD preserve:
- prior_settlement_ref
- reversal_reason
- new_evidence_refs
- contradiction_refs
- reversal_time
- new_settlement_status
- state_update_implications

### 32.2 Reversal Discipline

Settlement reversal MUST NOT delete the original Settlement.

Historical settlement remains part of the semantic trace.

### 32.3 Reversal Failure

If reversals erase prior settlements, CEP loses auditability and capability history.

## 33. Settlement Repair

Settlement Repair is a transformation that resolves missing evidence, contradiction, debt, authority issue, or consequence uncertainty.

### 33.1 Repair Record

A repair record SHOULD preserve:
- repair_transformation_ref
- settlement_ref
- repair_target
- repair_reason
- expected_repair_outcome
- evidence_requirements
- repair_status

### 33.2 Repair Failure

If repair work is not represented as transformation, systems hide the cost of settlement.

## 34. Settlement and Semantic Envelope

A [Semantic Envelope](./CEP-0008-semantic-envelope.md) MUST be capable of carrying Settlement context.

A Settlement record carried in a Semantic Envelope SHOULD include:

- settlement_id
- transformation_ref
- question_ref
- settlement_status
- threshold_ref
- evidence_refs
- observed_consequence_refs
- confidence
- unresolved_contradictions
- missing_evidence
- debt_refs
- state_update_refs
- authority_status
- success_status
- benefit_status
- settlement_horizon
- settlement_latency
- settlement_cost
- provenance_refs
- limitations

A Semantic Envelope MUST preserve whether Settlement context is complete, partial, unknown, unavailable, or out of scope.

## 35. Minimal Valid Settlement

A minimally valid CEP Settlement MUST preserve:

- settlement_id
- settlement_status
- transformation_ref
- question_ref
- evidence_refs
- threshold_ref OR threshold_basis
- observed_consequence_refs OR missing_consequence_record
- confidence OR confidence_status
- unresolved_contradictions OR contradiction_status
- missing_evidence OR missing_evidence_status
- state_update_recommendation
- time_context
- scope
- provenance_refs
A minimally valid Settlement SHOULD preserve:
- authority_status
- success_status
- benefit_status
- settlement_horizon
- settlement_latency
- settlement_cost
- debt_refs
- affordance_delta_refs
- capability_update_refs

Settlement lacking [Transformation](./CEP-0004-transformation-model.md) is invalid.

Settlement lacking [Question](./CEP-0005-question-model.md) is invalid.

Settlement lacking [Evidence](./CEP-0006-evidence-model.md) basis is invalid.

Settlement lacking status is invalid.

## 36. Invalid Settlement Conditions

A Settlement is invalid for CEP evaluation if:

- it lacks a [Transformation](./CEP-0004-transformation-model.md)
- it lacks a [Question](./CEP-0005-question-model.md)
- it lacks evidence basis
- it lacks settlement status
- it lacks threshold or threshold basis
- it treats completion as settlement
- it treats settlement as success
- it treats settlement as approval
- it treats settlement as benefit
- it hides material contradictions
- it hides missing evidence
- it updates [State](./CEP-0003-state-model.md) without state update recommendation
- it collapses authority status into settlement status
- it lacks scope
- it lacks time context when time matters
- it cannot identify what consequence was registered

Invalid Settlements MAY still be stored.

Invalid Settlements MUST NOT be used for capability claim, affordance update, benchmark scoring, or conformance claim unless the invalidity itself is the object of evaluation.

## 37. Settlement Invariants

CEP-compatible systems SHALL preserve the following Settlement invariants.

**Invariant 1 — Settlement Is Consequence Registration**

Settlement SHALL remain reliable consequence registration after [Transformation](./CEP-0004-transformation-model.md).

**Invariant 2 — Settlement Is Question-Bound**

Settlement SHALL preserve the [Question](./CEP-0005-question-model.md) under which it is evaluated.

**Invariant 3 — Settlement Requires Evidence**

Settlement SHALL preserve evidence basis or missing evidence status.

**Invariant 4 — Settlement Is Not Completion**

Completion claims SHALL remain distinct from Settlement.

**Invariant 5 — Settlement Is Not Success**

Success status SHALL remain distinct from Settlement status.

**Invariant 6 — Settlement Is Not Approval**

Approval and authority status SHALL remain distinct from Settlement status.

**Invariant 7 — Settlement Is Not Benefit**

Benefit status SHALL remain distinct from Settlement status.

**Invariant 8 — Settlement Preserves Contradiction**

Known contradictions SHALL NOT be hidden.

**Invariant 9 — Settlement Preserves Debt**

Settlement with unresolved obligations SHALL preserve debt.

**Invariant 10 — Settlement Updates State Explicitly**

[State](./CEP-0003-state-model.md) update from Settlement SHALL preserve Settlement reference.

**Invariant 11 — Settlement May Be Reversed**

Later evidence may reverse or supersede Settlement without erasing history.

**Invariant 12 — Settlement Is Horizon-Bound**

Time horizon SHALL be preserved when consequences require delayed observation.

## 38. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:
- completion into settlement
- execution into settlement
- observation into settlement
- evidence into settlement
- claim into settlement
- settlement into success
- settlement into approval
- settlement into authorization
- settlement into benefit
- settlement into morality
- settlement into finality
- settled state into true reality
- authorized into settled
- successful into settled
- beneficial into settled
- uncontradicted into settled
- missing evidence into negative evidence
- partial settlement into full settlement
- settlement with debt into clean settlement
- reversal into deletion
- repair into absence of failure

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

## 39. Settlement Conformance

A CEP-compatible Settlement implementation MUST:
- distinguish Settlement from completion
- distinguish Settlement from execution
- distinguish Settlement from success
- distinguish Settlement from approval
- distinguish Settlement from benefit
- preserve Settlement identity
- preserve [Transformation](./CEP-0004-transformation-model.md) reference
- preserve [Question](./CEP-0005-question-model.md) reference
- preserve [Evidence](./CEP-0006-evidence-model.md) basis
- preserve threshold or threshold basis
- preserve settlement status
- preserve observed consequences or missing consequence status
- preserve missing evidence
- preserve unresolved contradictions
- preserve [State](./CEP-0003-state-model.md) update recommendation
- preserve scope
- preserve time context
- preserve confidence or confidence status
- preserve authority status when authority matters
- preserve debt when partial obligations remain
- support Settlement reversal and supersession
- support Settlement comparison
- support Settlement latency and cost when capability is evaluated
- reject or warn on anti-collapse violations

## 40. Implementation Consequence

A CEP-compatible system that evaluates transformations MUST implement the Settlement Model.

A system that declares work complete without registering consequences is not settlement-compliant.

A system that updates [State](./CEP-0003-state-model.md) based only on completion claims is not CEP-compliant.

A system that evaluates capability without repeated settled transformations is not CEP-compliant.

A system that treats harmful, unauthorized, or failed transformations as irrelevant because they are undesirable is not CEP-compliant.

This requirement exists because CEP evaluates represented transformations through evidence-backed settlement.

Settlement is the boundary where represented consequence becomes reliable enough to affect future action.

## 41. Closing Definition

Settlement is reliable consequence registration after [Transformation](./CEP-0004-transformation-model.md).

It is the point where evidence-backed consequence becomes sufficient for a [Question](./CEP-0005-question-model.md) and evaluation context to update State, preserve uncertainty, register debt, identify failure, trigger repair, or revise future affordances.

Settlement is not completion.

Settlement is not success.

Settlement is not approval.

Settlement is not benefit.

Settlement is not final truth.

Settlement is the disciplined registration of what became consequential.

The next document should be CEP-0008 — [Semantic Envelope](./CEP-0008-semantic-envelope.md). That is where the protocol becomes portable: one canonical interchange object capable of carrying state, transformation, question, evidence, settlement, authority, affordance, and capability context without collapsing the distinctions we just defined.