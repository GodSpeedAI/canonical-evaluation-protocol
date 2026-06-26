CEP-0001 — Ontology

Status: Draft
Category: Normative
Version: 0.1
Protocol: Canonical Evaluation Protocol
Depends On: CEP-0000 — Derivation Ladder and First Principles
Document Type: Foundational Specification

Abstract

This document defines the core ontology of the Canonical Evaluation Protocol.

CEP-0000 defines the derivation ladder:

Constraint
→ Distinction
→ Relation
→ Representation
→ State
→ Transformation
→ Observation
→ Question
→ Evidence
→ Settlement

CEP-0001 converts that ladder into protocol entities, relationships, identity rules, and anti-collapse requirements.

The purpose of this ontology is not to describe every possible domain.

The purpose is to define the minimum conceptual structure required for a system to evaluate represented transformations through evidence-backed settlement.

Every later CEP specification SHALL preserve this ontology unless explicitly superseded by a major protocol revision.

1. Scope

This document defines:

core entity classes,

derived entity classes,

required relationships,

identity and continuity rules,

ontology-level invariants,

anti-collapse rules,

and conformance expectations.

This document does not define:

serialization format,

benchmark language syntax,

JSON schemas,

scoring algorithms,

runner behavior,

evidence weighting,

or specific benchmark families.

Those are specified in later CEP documents.

2. Ontological Doctrine

CEP is an ontology for evaluation, not an ontology of all reality.

CEP SHALL only model entities necessary to answer questions about represented transformations.

The core evaluation question is:

Given a represented state, a transformation, and available evidence, what changed, under which constraints, according to which question, and has the consequence settled enough to update future action?

Any entity that does not help answer that question SHALL remain outside the CEP core.

3. Normative Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, MAY, and OPTIONAL are to be interpreted as normative protocol language.

4. Core Ontology Layers

CEP defines ten core ontology layers.

Each layer corresponds to a layer from CEP-0000.

Layer
Entity
Role
1
Constraint
Possibility structure
2
Distinction
Preserved difference
3
Relation
Connection between distinctions
4
Representation
Preserved structure of distinctions and relations
5
State
Situated representation
6
Transformation
Change between states
7
Observation
Registered visibility of state or transformation
8
Question
Constraint over observation and relevance
9
Evidence
Observation made relevant to a claim
10
Settlement
Reliable consequence registration

These entities are ordered.

A later entity SHALL NOT be defined in a way that erases its dependence on earlier entities.

5. Entity: Constraint

5.1 Definition

A Constraint is any represented condition that limits, enables, shapes, or differentiates possible states or transformations.

5.2 Derivation Layer

Layer 1.

5.3 Required Function

A Constraint defines possibility structure.

It explains why some states or transformations are possible, impossible, permitted, prohibited, costly, required, delayed, unstable, or uncertain.

5.4 Required Attributes

A CEP-compatible Constraint MUST preserve:

constraint_id

constraint_type

description

scope

source

status

applies_to

5.5 Constraint Types

CEP recognizes the following top-level constraint types:

physical

technical

semantic

temporal

resource

capacity

normative

authority

evidence

confidence

settlement

economic

coordination

environmental

unknown

Implementations MAY define domain-specific constraint subtypes.

Domain-specific subtypes MUST map to one or more CEP top-level constraint types.

5.6 Status Values

A Constraint SHOULD have one of the following statuses:

active

inactive

pending

violated

satisfied

superseded

unknown

5.7 Failure Mode

If Constraint is absent, CEP cannot distinguish possibility from impossibility, permissibility from capability, or affordability from fantasy.

If Constraint is untyped, CEP cannot distinguish policy prohibition from physical impossibility, resource insufficiency, or semantic mismatch.

6. Entity: Distinction

6.1 Definition

A Distinction is a preserved difference between two or more represented conditions.

6.2 Derivation Layer

Layer 2.

6.3 Required Function

A Distinction makes difference computable.

It allows CEP to preserve contrasts such as:

declared vs observed,

allowed vs denied,

complete vs settled,

capable vs incapable,

supported vs unsupported,

reachable vs unreachable,

possible vs permissible,

authorized vs unauthorized,

stable vs unstable.

6.4 Required Attributes

A CEP-compatible Distinction MUST preserve:

distinction_id

left_term

right_term

basis

scope

source

confidence

6.5 Distinction Kinds

A Distinction MAY be:

binary

graded

categorical

temporal

relational

probabilistic

contextual

normative

semantic

6.6 Failure Mode

If Distinction is absent, CEP cannot evaluate change.

Every benchmark requires preserved distinctions.

Without distinctions, scoring collapses into undifferentiated assertion.

7. Entity: Relation

7.1 Definition

A Relation is a preserved connection between entities.

Relations make distinctions structured.

7.2 Derivation Layer

Layer 3.

7.3 Required Function

A Relation allows CEP to represent dependency, contradiction, support, sequence, authority, causality, reference, and settlement.

7.4 Required Attributes

A CEP-compatible Relation MUST preserve:

relation_id

relation_type

source_entity

target_entity

scope

confidence

evidence_refs

7.5 Required Relation Types

CEP implementations MUST support at least the following relation types:

constrains

distinguishes

relates_to

depends_on

contradicts

supports

weakens

precedes

follows

updates

transforms

observes

questions

evidences

settles

authorizes

prohibits

permits

requires

produces

refers_to

7.6 Failure Mode

If Relation is absent, CEP cannot determine whether evidence supports a claim, whether a policy applies to a transformation, whether an observed state contradicts a declared state, or whether a transformation caused a later consequence.

8. Entity: Representation

8.1 Definition

A Representation is a preserved structure of constraints, distinctions, and relations.

CEP operates on Representations rather than reality directly.

8.2 Derivation Layer

Layer 4.

8.3 Required Function

A Representation gives CEP something to compute over.

Representations preserve selected aspects of a system in a durable, communicable, computable, or evaluable form.

8.4 Required Attributes

A CEP-compatible Representation MUST preserve:

representation_id

representation_type

content_ref

scope

source

created_at

version

preserved_entities

omitted_or_unknown_entities

8.5 Representation Types

A Representation MAY be:

document

schema

event_log

trace

policy

state_graph

semantic_envelope

benchmark_case

evidence_packet

result_record

natural_language_statement

code_artifact

configuration

model_output

human_judgment

system_observation

8.6 Representation Boundary

A Representation MUST NOT be treated as reality itself.

Every Representation is partial.

Every Representation preserves some distinctions while omitting others.

8.7 Failure Mode

If Representation is collapsed into reality, CEP cannot model representational error, semantic drift, evidence insufficiency, or Reality Gap.

9. Entity: State

9.1 Definition

A State is a situated Representation.

A Representation becomes a State when it is sufficiently contextualized to support comparison, transformation, or evaluation.

9.2 Derivation Layer

Layer 5.

9.3 Required Function

State enables before-after comparison.

Without State, Transformation cannot be evaluated.

9.4 Required Attributes

A CEP-compatible State MUST preserve:

state_id

representation_refs

state_type

scope

time_context

authority_context

actor_context

resource_context

environment_context

confidence

version

identity_refs

9.5 State Types

CEP recognizes the following State types:

declared

observed

expected

actual

claimed

authorized

settled

unsettled

counterfactual

unknown

9.6 Identity Requirement

A State MUST preserve enough identity information to support continuity across transformations.

If identity cannot be established, the State MUST be marked as identity-uncertain.

9.7 Failure Mode

If State is absent, CEP cannot determine what changed.

If identity is absent, CEP cannot distinguish transformation of the same system from replacement by a different system.

10. Entity: Transformation

10.1 Definition

A Transformation is a represented change from one State to another State.

A Transformation may be caused by action, drift, update, failure, environmental change, observation, policy change, or system behavior.

10.2 Derivation Layer

Layer 6.

10.3 Required Function

Transformation is the central unit of CEP evaluation.

CEP evaluates whether transformations preserve, violate, repair, or expand relevant invariants.

10.4 Required Attributes

A CEP-compatible Transformation MUST preserve:

transformation_id

source_state_ref

target_state_ref

transformation_type

trigger

actor_refs

affected_entities

applicable_constraints

expected_invariants

observed_consequences

evidence_refs

confidence

status

10.5 Transformation Types

CEP recognizes the following transformation types:

action

decision

drift

update

execution

observation

authorization

settlement

capability_update

affordance_update

failure

reversal

repair

escalation

unknown

10.6 Transformation Status Values

A Transformation SHOULD have one of the following statuses:

proposed

attempted

executed

claimed_complete

observed

evidenced

settled

failed

reversed

blocked

unknown

10.7 Failure Mode

If Transformation is absent, CEP collapses into static documentation review.

If Transformation is collapsed into action, CEP cannot model drift, consequences, observation updates, or settlement.

11. Entity: Observation

11.1 Definition

An Observation is a registered Representation of a State, Transformation, Relation, or Constraint from a Perspective.

11.2 Derivation Layer

Layer 7.

11.3 Required Function

Observation makes visibility explicit.

It separates what occurred from what was registered.

11.4 Required Attributes

A CEP-compatible Observation MUST preserve:

observation_id

observed_entity_ref

observer_ref

perspective_ref

method

timestamp

representation_ref

scope

confidence

limitations

11.5 Observation Methods

An Observation MAY be produced through:

human_report

automated_log

test_result

monitoring_signal

audit_record

sensor

model_inference

document_review

interview

trace_analysis

manual_inspection

unknown

11.6 Failure Mode

If Observation is collapsed into Transformation, CEP cannot represent blind spots, delayed visibility, misobservation, or conflicting perspectives.

12. Entity: Perspective

12.1 Definition

A Perspective is a rule or context that determines which distinctions, relations, and transformations become visible, relevant, or meaningful.

12.2 Derivation Layer

Perspective is derived from Observation.

Perspective is not a foundational layer, but it is required for implementation.

12.3 Required Function

Perspective explains why the same Representation may support different observations or evaluations.

12.4 Required Attributes

A CEP-compatible Perspective MUST preserve:

perspective_id

perspective_type

scope

selection_rules

relevance_rules

authority_context

limitations

12.5 Perspective Types

CEP recognizes the following Perspective types:

human

agent

organization

auditor

developer

operator

customer

regulator

benchmark

system

composite

unknown

12.6 Failure Mode

If Perspective is absent, CEP cannot explain why one observer sees a Reality Gap while another does not.

Without Perspective, relevance is smuggled into the protocol implicitly.

13. Entity: Question

13.1 Definition

A Question is a constraint over observation, attention, and relevance.

A Question determines which distinctions, states, transformations, observations, and evidence become relevant.

13.2 Derivation Layer

Layer 8.

13.3 Required Function

Question directs evaluation.

Question is what turns available Representation into a search space.

13.4 Required Attributes

A CEP-compatible Question MUST preserve:

question_id

question_text_or_form

question_type

scope

target_entities

relevance_rules

expected_answer_shape

evaluation_context

13.5 Question Types

CEP recognizes the following Question types:

divergence

authority

settlement

capability

affordance

evidence

causal

diagnostic

comparative

predictive

conformance

unknown

13.6 Failure Mode

If Question is absent, CEP cannot determine relevance.

The same observation can serve different evaluations depending on the question.

Without Question, benchmarks become arbitrary scoring rituals.

14. Entity: Claim

14.1 Definition

A Claim is a represented assertion about a Constraint, Distinction, Relation, Representation, State, Transformation, Observation, Settlement, Affordance, Capability, or Benchmark result.

14.2 Derivation Layer

Claim is derived from Representation and Question.

Claim is not one of the ten ladder layers, but it is required for Evidence.

14.3 Required Function

Claim provides the target that Evidence supports, weakens, contradicts, or qualifies.

14.4 Required Attributes

A CEP-compatible Claim MUST preserve:

claim_id

claim_text_or_form

claim_type

subject_ref

scope

source

confidence

status

evidence_refs

14.5 Claim Types

CEP recognizes the following Claim types:

state_claim

transformation_claim

authority_claim

settlement_claim

capability_claim

affordance_claim

evidence_claim

benchmark_claim

conformance_claim

unknown

14.6 Failure Mode

If Claim is absent, Evidence has no target.

CEP cannot evaluate whether something is supported, contradicted, or underdetermined.

15. Entity: Evidence

15.1 Definition

Evidence is a Representation that changes confidence in a Claim relative to a Question.

Evidence is not raw data.

Evidence is data made relevant.

15.2 Derivation Layer

Layer 9.

15.3 Required Function

Evidence separates assertion from support.

It enables confidence update, contradiction handling, settlement, and scoring.

15.4 Required Attributes

A CEP-compatible Evidence record MUST preserve:

evidence_id

evidence_type

source

target_claim_ref

question_ref

representation_ref

timestamp

relevance

reliability

direction

confidence_impact

limitations

15.5 Evidence Types

CEP recognizes the following Evidence types:

test_result

execution_log

audit_record

monitoring_signal

trace

document

human_attestation

model_output

policy_reference

configuration_snapshot

artifact_diff

external_record

manual_inspection

unknown

15.6 Evidence Direction

Evidence direction MUST be one of:

supports

weakens

contradicts

qualifies

irrelevant

unknown

15.7 Failure Mode

If Evidence is untyped, CEP cannot distinguish agent self-report from independent verification.

If Evidence lacks a Claim target, it becomes uninterpretable data.

16. Entity: Settlement

16.1 Definition

Settlement is reliable consequence registration after Transformation.

A Settlement occurs when available Evidence is sufficient for the evaluation context to update State without unresolved contradictions exceeding defined thresholds.

16.2 Derivation Layer

Layer 10.

16.3 Required Function

Settlement separates claimed completion from consequence-backed update.

16.4 Required Attributes

A CEP-compatible Settlement MUST preserve:

settlement_id

transformation_ref

question_ref

settlement_status

evidence_refs

confidence

unresolved_contradictions

threshold_ref

state_update_refs

settled_at

limitations

16.5 Settlement Status Values

CEP recognizes the following Settlement statuses:

unsettled

partially_settled

settled

failed

blocked

reversed

harmful_but_settled

beneficial_but_unsettled

unauthorized_but_settled

unknown

16.6 Failure Mode

If Settlement is collapsed into completion, CEP will reward premature success claims.

If Settlement is collapsed into approval, CEP will hide harmful but real consequences.

If Settlement is collapsed into Evidence, CEP will confuse support with state-update readiness.

17. Derived Entity: Actor

17.1 Definition

An Actor is an entity capable of initiating, participating in, authorizing, blocking, observing, or being affected by a Transformation.

17.2 Derivation

Actor derives from State, Transformation, Observation, and Perspective.

17.3 Required Attributes

A CEP-compatible Actor SHOULD preserve:

actor_id

actor_type

roles

authority_refs

capability_refs

scope

identity_refs

17.4 Actor Types

Actor types MAY include:

human

agent

team

organization

system

service

tool

external_entity

unknown

17.5 Failure Mode

If Actor is absent, CEP cannot attribute transformations, authority decisions, observations, or capability changes.

18. Derived Entity: Authority

18.1 Definition

Authority is a normative Constraint over permissible Transformations from a recognized governance Perspective.

18.2 Derivation

Authority derives from Constraint, Relation, State, Transformation, Question, and Perspective.

18.3 Required Attributes

A CEP-compatible Authority record MUST preserve:

authority_id

authority_type

subject_actor_ref

permitted_transformations

prohibited_transformations

escalation_conditions

scope

source

effective_time

evidence_refs

18.4 Authority Decision Values

Authority evaluations MUST produce one of:

allow

deny

escalate

unknown

18.5 Failure Mode

If Authority is collapsed into Capability, CEP cannot distinguish what can be done from what may be done.

That collapse destroys governance evaluation.

19. Derived Entity: Affordance

19.1 Definition

An Affordance is a reachable, payable, permissible, executable, and settleable Transformation from a current State.

19.2 Derivation

Affordance derives from Constraint, State, Transformation, Authority, Evidence, Settlement, Capability, and Perspective.

19.3 Required Attributes

A CEP-compatible Affordance record MUST preserve:

affordance_id

current_state_ref

transformation_ref

actor_ref

reachability_status

payment_burden

authority_status

execution_requirements

settlement_requirements

evidence_requirements

confidence

19.4 Reachability Status Values

Reachability SHOULD be one of:

reachable

reachable_with_payment

blocked

unknown

theoretical_only

19.5 Failure Mode

If Affordance is collapsed into possibility, CEP loses one of its central disciplines.

A destination without a spendable path is not an Affordance.

20. Derived Entity: Capability

20.1 Definition

Capability is persistent reduction in payment burden for repeated Settlement under variation.

20.2 Derivation

Capability derives from Transformation history, Evidence, Settlement, Affordance change, and repeated State updates.

20.3 Required Attributes

A CEP-compatible Capability record MUST preserve:

capability_id

capability_name

settlement_history_refs

variation_context

payment_burden_before

payment_burden_after

affordance_delta_refs

confidence

decay_conditions

refresh_conditions

20.4 Failure Mode

If Capability is collapsed into isolated success, CEP cannot distinguish lucky completion from durable organizational improvement.

21. Derived Entity: Metric

21.1 Definition

A Metric is a rule for evaluating represented transformations according to specified invariants.

21.2 Derivation

Metric derives from Question, Evidence, Settlement, and Benchmark.

21.3 Required Attributes

A CEP-compatible Metric MUST preserve:

metric_id

metric_name

question_ref

target_entities

scoring_rule

invariants

failure_conditions

confidence_handling

21.4 Failure Mode

If Metric is absent, benchmarks cannot convert evidence-backed evaluation into comparable results.

If Metric is detached from Question, scoring becomes contextless.

22. Derived Entity: Benchmark

22.1 Definition

A Benchmark is a structured evaluation of Transformations against specified invariants under a Question.

22.2 Derivation

Benchmark derives from Question, Transformation, Evidence, Settlement, Metric, and State.

22.3 Required Attributes

A CEP-compatible Benchmark MUST preserve:

benchmark_id

benchmark_name

question_ref

case_refs

metric_refs

answer_key_refs

evidence_requirements

conformance_requirements

result_schema_ref

22.4 Failure Mode

If Benchmark is collapsed into task output scoring, CEP cannot evaluate authority, settlement, capability, affordance expansion, or Reality Gap.

23. Derived Entity: Semantic Envelope

23.1 Definition

A Semantic Envelope is the canonical transport structure for preserving CEP-relevant context across Transformations.

23.2 Derivation

Semantic Envelope derives from the full ontology.

23.3 Required Function

Semantic Envelopes preserve enough context for tools, agents, benchmarks, and organizations to exchange transformation-relevant representations without losing critical distinctions.

23.4 Required Contents

A CEP-compatible Semantic Envelope MUST be capable of carrying references to:

Constraints,

Distinctions,

Relations,

Representations,

States,

Transformations,

Observations,

Perspectives,

Questions,

Claims,

Evidence,

Settlements,

Actors,

Authority records,

Affordances,

Capabilities,

Metrics,

Benchmarks,

Provenance,

and version identity.

A Semantic Envelope MAY omit entities not relevant to a specific transformation, but it MUST preserve whether omitted entities are intentionally absent, unknown, unavailable, or out of scope.

23.5 Failure Mode

If Semantic Envelope is treated as a message only, CEP loses transformation context.

If Semantic Envelope lacks provenance and identity, CEP cannot support trustworthy evaluation.

24. Identity and Continuity

24.1 Definition

Identity is the rule by which CEP determines that an entity remains sufficiently continuous across states or transformations.

Identity is not sameness.

Identity is continuity sufficient for evaluation.

24.2 Identity Requirement

CEP implementations MUST preserve identity rules for any entity participating in Transformation, Settlement, Affordance, Capability, or Benchmark evaluation.

24.3 Required Identity Fields

Identity records SHOULD include:

identity_ref

entity_ref

continuity_basis

version

scope

confidence

evidence_refs

24.4 Continuity Basis

Continuity MAY be based on:

persistent identifier,

semantic equivalence,

version lineage,

organizational role,

artifact history,

actor continuity,

process continuity,

policy continuity,

spatial continuity,

temporal continuity,

or human attestation.

24.5 Failure Mode

Without identity rules, CEP cannot distinguish:

a changed system from a replaced system,

a revised policy from a different policy,

a repeated capability from a one-time event,

or a settled transformation from an unrelated observation.

25. Ontology-Level Invariants

CEP-compatible implementations SHALL preserve the following invariants.

25.1 Representation Boundary

Representations SHALL NOT be treated as reality itself.

25.2 State Situatedness

States SHALL preserve sufficient context to support comparison and transformation.

25.3 Transformation Explicitness

Transformations SHALL be represented explicitly rather than inferred silently.

25.4 Observation Separation

Observation SHALL remain distinct from occurrence.

25.5 Question Preservation

The relevant Question SHALL be preserved for any Evidence, Metric, Benchmark, or Settlement.

25.6 Evidence Targeting

Evidence SHALL target at least one Claim, State, Transformation, Relation, Invariant, or Settlement.

25.7 Settlement Separation

Settlement SHALL remain distinct from completion, success, approval, and benefit.

25.8 Authority Separation

Authority SHALL remain distinct from Capability.

25.9 Affordance Discipline

Affordance SHALL remain distinct from possibility.

25.10 Capability Durability

Capability SHALL require repeated Settlement under variation.

26. Anti-Collapse Rules

CEP implementations SHALL NOT collapse the following concepts.

26.1 Constraint vs Distinction

A Constraint shapes possibility.

A Distinction preserves difference.

26.2 Distinction vs Relation

A Distinction marks difference.

A Relation connects differences.

26.3 Representation vs State

A Representation preserves structure.

A State situates that structure in context.

26.4 State vs Transformation

A State preserves condition.

A Transformation preserves change.

26.5 Transformation vs Action

An Action is attempted.

A Transformation is represented change.

26.6 Transformation vs Observation

A Transformation may occur without being observed.

An Observation may misrepresent a Transformation.

26.7 Observation vs Evidence

Observation is registered visibility.

Evidence is Observation made relevant to a Claim or Question.

26.8 Evidence vs Settlement

Evidence changes confidence.

Settlement updates consequence readiness.

26.9 Settlement vs Success

A settled Transformation may be harmful.

A successful intended action may remain unsettled.

26.10 Authority vs Capability

Capability describes capacity.

Authority describes permissibility.

26.11 Affordance vs Possibility

Possibility may be imagined.

Affordance must be reachable from the current State.

26.12 Capability vs Performance

Performance may occur once.

Capability must persist under variation.

27. Minimal CEP Evaluation Chain

A minimally valid CEP evaluation SHOULD preserve the following chain:

Question
→ State
→ Transformation
→ Observation
→ Claim
→ Evidence
→ Settlement
→ Result

A benchmark MAY include additional ontology entities.

A benchmark that lacks this minimal chain MUST explain why the omitted entities are not required.

28. Minimal Reality Gap Chain

A minimally valid Reality Gap evaluation MUST preserve:

Declared State
→ Observed State
→ Divergence Question
→ Gap Claim
→ Evidence
→ Settlement Status

Failure to preserve declared and observed state separately invalidates Reality Gap evaluation.

29. Minimal Authority Chain

A minimally valid Authority evaluation MUST preserve:

Actor
→ Proposed Transformation
→ Authority Constraint
→ Governance Perspective
→ Authority Question
→ Evidence
→ Decision

The decision MUST be one of:

allow

deny

escalate

unknown

30. Minimal Settlement Chain

A minimally valid Settlement evaluation MUST preserve:

Transformation
→ Completion Claim
→ Observed Consequence
→ Evidence
→ Settlement Question
→ Settlement Status

Failure to distinguish Completion Claim from Settlement Status invalidates Settlement evaluation.

31. Minimal Capability Chain

A minimally valid Capability evaluation MUST preserve:

Transformation History
→ Settlement History
→ Variation Context
→ Payment Burden Before
→ Payment Burden After
→ Affordance Delta
→ Capability Claim

A single successful Transformation is insufficient to establish Capability.

32. Conformance Expectations

A CEP-compatible implementation MUST:

Preserve the core ontology entities or provide lossless mappings to them.

Preserve required relations among entities.

Maintain identity and continuity rules.

Distinguish Representations from reality.

Represent Transformations explicitly.

Preserve Questions for Evidence and Metrics.

Target Evidence to Claims or invariants.

Distinguish Settlement from completion and success.

Distinguish Authority from Capability.

Distinguish Affordance from possibility.

Support Semantic Envelope interchange or provide a compatible adapter.

Produce validation errors when anti-collapse rules are violated.

33. Non-Core Concepts

The following concepts MAY be useful but are not part of the CEP core ontology unless defined by later specifications:

motivation,

preference,

emotion,

strategy,

value,

morality,

ownership,

economics,

market position,

culture,

intelligence,

creativity,

risk appetite,

maturity,

trust,

reputation.

These concepts MAY be represented through CEP entities when needed.

For example:

strategy MAY be represented as Questions, Constraints, States, and desired Transformations.

trust MAY be represented as Evidence history and confidence.

culture MAY be represented as repeated organizational Transformations and Settlement patterns.

value MAY be represented as evaluation criteria or outcome constraints.

CEP does not treat these as primitive.

34. Ontology Admission Test

A proposed new ontology entity MUST pass the following test:

Which CEP-0000 layer does it derive from?

Which existing entity is insufficient?

What operation becomes possible if this entity is admitted?

What failure occurs if it is not admitted?

What required fields does it preserve?

What relation types does it require?

Which anti-collapse rule protects it?

How would a Semantic Envelope carry it?

How would a benchmark score or validate it?

What would falsify or invalidate claims involving it?

If these questions cannot be answered, the entity SHALL NOT be admitted into the core ontology.

35. Closing Definition

The CEP ontology defines the entities required to evaluate represented transformations through evidence-backed settlement.

It exists to preserve the distinctions necessary for Reality Gap, Authority, Settlement, Capability, Affordance, and future benchmark families to be evaluated without collapsing into task completion.

Every later CEP specification SHALL preserve this ontology or explicitly revise it through protocol governance.

The next adjacent document should be CEP-0002 — Representation Model. That is where we stop using philosophical terms and define how distinctions, relations, identity, omissions, uncertainty, and provenance are actually represented.