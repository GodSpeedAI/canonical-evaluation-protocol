CEP-0000 - Derivation Ladder and First Principles

Status: Draft
Category: Normative
Version: 0.1
Protocol: Canonical Evaluation Protocol
Document Type: Foundational Specification

Abstract

The Canonical Evaluation Protocol exists to evaluate systems through represented transformations rather than isolated outputs.

This document defines the derivation ladder from which all core CEP concepts SHALL be derived.

The purpose of the ladder is to prevent two failure modes:

Overcompression - reducing every concept to a single vague primitive, such as “constraint,” until the protocol becomes unfalsifiable.

Ontology sprawl - adding concepts because they are useful rhetorically rather than because they are necessary operationally.

CEP-0000 therefore defines a lawful order of emergence.

Each layer in the ladder enables a form of computation, evaluation, or governance that cannot be supported by the prior layers alone.

A concept MAY enter the CEP core only if its location in this derivation ladder is clear and its operational necessity can be demonstrated.

1. Scope

This document defines the foundational ordering of CEP concepts.

It does not define the complete schema, runner protocol, benchmark language, evidence model, semantic envelope format, or conformance suite.

Those are defined in later specifications.

This document is concerned with one question:

What must exist before a system can be evaluated through represented transformation?

CEP assumes that evaluation requires more than task completion.

Evaluation requires:

preserved distinctions,

relations among distinctions,

representations,

situated states,

transformations,

observations,

questions,

evidence,

and settlement.

These concepts do not appear simultaneously.

They emerge in a necessary order.

2. Design Doctrine

CEP SHALL be derived, not accumulated.

Every core concept SHALL answer four questions:

Derivation - From which prior layer does this concept emerge?

Necessity - What becomes possible at this layer that was impossible before?

Operational Consequence - What must an implementation do differently because this concept exists?

Failure Mode - What breaks if this concept is absent or collapsed into another concept?

A concept that cannot answer these questions SHALL NOT become part of the CEP core.

3. The Derivation Ladder

The CEP derivation ladder is:

0. Indeterminate Field
1. Constraint
2. Distinction
3. Relation
4. Representation
5. State
6. Transformation
7. Observation
8. Question
9. Evidence
10. Settlement

Layers 1 through 10 are protocol-relevant.

Layer 0 is outside the protocol boundary.

4. Layer 0 - Indeterminate Field

Definition

The Indeterminate Field is the pre-representational condition before any constraint, distinction, relation, or state has been preserved.

It is not an object.

It is not data.

It is not reality as such.

It is the condition prior to CEP computation.

Protocol Status

Layer 0 is outside the scope of CEP.

CEP SHALL NOT attempt to compute, serialize, benchmark, or evaluate the Indeterminate Field.

Necessity

This boundary prevents CEP from claiming direct access to reality.

CEP begins only when some constraint becomes representable.

Failure Mode

If CEP claims to evaluate reality directly, it collapses into metaphysical overclaiming.

CEP evaluates representations of reality, not reality itself.

5. Layer 1 - Constraint

Definition

A constraint is any condition that limits, enables, shapes, or differentiates possible states.

Constraint is the first positive concept in CEP.

A constraint does not need to be negative.

A constraint can prevent action.

A constraint can enable action.

A constraint can shape the form an action may take.

A constraint can make one state distinguishable from another.

Necessity

Constraint introduces possibility structure.

Without constraint, nothing can be limited, enabled, shaped, compared, selected, or transformed.

Operational Consequence

An implementation MUST be able to represent constraints explicitly or implicitly.

Constraints MAY appear as:

rules,

policies,

dependencies,

permissions,

resource limits,

physical limits,

semantic boundaries,

schema requirements,

temporal conditions,

confidence thresholds,

cost boundaries,

role expectations,

or environmental conditions.

Failure Mode

If constraint is absent, CEP cannot explain why some transformations are possible while others are not.

If all constraints are treated as identical, CEP cannot distinguish physical impossibility, policy prohibition, resource insufficiency, semantic mismatch, and evidence insufficiency.

Therefore, later specifications SHALL define typed constraints.

6. Layer 2 - Distinction

Definition

A distinction is a constraint made differentiable.

A distinction marks that one condition is not another condition.

Distinction is the first form of protocol-relevant difference.

Derivation

Distinction derives from constraint.

A constraint becomes operational when it creates or preserves a difference.

Necessity

Without distinction, no representation can preserve anything.

There is no “before” versus “after.”

There is no “allowed” versus “denied.”

There is no “declared” versus “observed.”

There is no “complete” versus “settled.”

There is no “capable” versus “incapable.”

Operational Consequence

An implementation MUST preserve distinctions that are relevant to a benchmark, semantic envelope, state model, evidence model, or transformation.

A distinction MAY be binary, graded, categorical, temporal, relational, probabilistic, or contextual.

Failure Mode

If distinction is absent, evaluation collapses.

A benchmark cannot score a system if the relevant differences are not preserved.

RealityGapBench, AuthorityBench, SettlementBench, and CapabilityBench all require preserved distinctions.

7. Layer 3 - Relation

Definition

A relation is a preserved connection between distinctions.

Relation allows distinctions to become structured.

Relations include, but are not limited to:

depends on,

contradicts,

permits,

prohibits,

causes,

updates,

observes,

supports,

weakens,

precedes,

follows,

belongs to,

authorizes,

settles,

transforms,

and refers to.

Derivation

Relation derives from distinction.

Once two or more distinctions exist, their connection can be represented.

Necessity

Distinctions alone are isolated.

Relations make comparison, dependency, contradiction, sequence, and causality representable.

Operational Consequence

An implementation MUST be able to preserve relations among distinctions.

The protocol SHALL NOT treat all represented facts as flat assertions.

Relations are necessary for:

evidence linking,

authority evaluation,

semantic envelopes,

benchmark scoring,

state comparison,

transformation history,

and settlement reasoning.

Failure Mode

If relation is absent, CEP cannot determine whether evidence supports a claim, whether a policy applies to an action, whether an observation contradicts a declared state, or whether a transformation caused a later condition.

8. Layer 4 - Representation

Definition

A representation is a preserved structure of distinctions and relations.

A representation does not preserve reality directly.

It preserves selected constraints, distinctions, and relations in a form usable by an observer, tool, benchmark, or protocol implementation.

Derivation

Representation derives from distinction and relation.

A representation exists when distinctions and relations become preservable across time, communication, computation, or evaluation.

Necessity

Without representation, CEP has nothing to compute over.

Representations make systems available to protocol operations.

Operational Consequence

An implementation MUST operate on representations rather than reality directly.

Representations MAY include:

files,

schemas,

event logs,

policies,

traces,

natural language documents,

code,

benchmark cases,

semantic envelopes,

evidence packets,

state graphs,

and result records.

Failure Mode

If representation is treated as reality itself, CEP loses the ability to reason about representational error.

This would make Reality Gap, evidence quality, semantic drift, and settlement uncertainty impossible to model.

9. Layer 5 - State

Definition

A state is a situated representation.

A state preserves relevant distinctions and relations under a specific context.

A state may include:

time,

scope,

actor,

environment,

authority context,

resource context,

evidence context,

confidence level,

and version identity.

Derivation

State derives from representation.

A representation becomes a state when it is situated enough to support comparison, transformation, or evaluation.

Necessity

Without state, CEP cannot say what condition a system was in before, during, or after a transformation.

State enables before-after comparison.

Operational Consequence

An implementation MUST distinguish unsituated representation from state.

A policy document is not automatically a state.

A log line is not automatically a state.

A semantic envelope MAY contain many states.

A benchmark case MUST define at least one state or enough information to derive one.

Failure Mode

If state is absent, transformations cannot be evaluated.

A benchmark cannot determine what changed if it cannot identify the represented condition prior to change.

10. Layer 6 - Transformation

Definition

A transformation is a change from one state to another state.

A transformation alters one or more represented constraints, distinctions, or relations.

A transformation is not merely an action.

An action is attempted.

A transformation is the represented change produced or claimed by action, drift, update, observation, policy revision, environmental change, or system behavior.

Derivation

Transformation derives from state.

Once states exist, changes between states become representable.

Necessity

Transformation is the central unit of CEP.

CEP evaluates systems by examining whether transformations preserve required invariants.

Operational Consequence

An implementation MUST represent transformations explicitly.

A transformation SHOULD include:

source state,

target state or claimed target state,

triggering event,

actor or originating process when known,

affected distinctions,

affected relations,

applicable constraints,

expected invariants,

observed consequences,

evidence references,

and confidence.

Failure Mode

If transformation is absent, CEP collapses into static documentation review.

Task completion cannot be meaningfully distinguished from settlement, capability, governance, or drift.

11. Layer 7 - Observation

Definition

Observation is a transformation registered from a perspective.

Observation does not mean passive seeing.

Observation means that some change, condition, or relation becomes represented as visible within a perspective.

Derivation

Observation derives from transformation and representation.

A transformation must be registered into a representation before it can become usable for evaluation.

Necessity

Not every transformation is observed.

Not every observed transformation is observed equally.

Observation introduces perspective, salience, and visibility.

Operational Consequence

An implementation MUST distinguish between:

what occurred,

what was observed,

who or what observed it,

how it was observed,

when it was observed,

and what representation was produced by the observation.

Failure Mode

If observation is collapsed into transformation, CEP cannot model blind spots.

This would make it impossible to distinguish:

a transformation that did not occur,

a transformation that occurred but was not observed,

a transformation that was observed incorrectly,

and a transformation that was observed but not understood.

12. Layer 8 - Question

Definition

A question is a constraint over observation.

A question determines which distinctions, relations, states, transformations, and evidence become relevant.

A question may be expressed as natural language, formal query, benchmark objective, evaluation criterion, policy concern, or search objective.

Derivation

Question derives from observation.

Once observation exists, questions constrain what observation is directed toward.

Necessity

Observation is not exhaustive.

Questions direct attention.

Attention determines which parts of the representational field become computationally relevant.

Operational Consequence

An implementation MUST preserve the question or evaluation objective that makes a transformation relevant.

Benchmark cases MUST make the operative question explicit or derivable.

Examples:

Where does declared reality diverge from observed reality?

Was this transformation authorized?

Has this transformation settled?

Did repeated settlement reduce future transformation cost?

Which affordances became reachable after this transformation?

Failure Mode

If question is absent, CEP cannot determine relevance.

The same data may support different evaluations depending on the question being asked.

Without question, benchmarks become arbitrary scoring rituals rather than directed evaluation systems.

13. Layer 9 - Evidence

Definition

Evidence is a representation that changes confidence in a claim about a state, transformation, observation, relation, or invariant.

Evidence is not raw data.

Evidence is data situated in relation to a question and a claim.

Derivation

Evidence derives from question and observation.

An observation becomes evidence only when it bears on a question.

Necessity

Without evidence, CEP cannot distinguish assertion from support.

Evidence enables confidence updates, contradiction detection, settlement, and benchmark scoring.

Operational Consequence

An implementation MUST distinguish:

claim,

evidence,

evidence source,

evidence target,

evidence reliability,

evidence relevance,

evidence timestamp,

and confidence impact.

Evidence MAY support, weaken, contradict, qualify, or fail to affect a claim.

Failure Mode

If evidence is absent or untyped, CEP cannot distinguish:

an agent claiming success,

a test log showing success,

a human approving success,

a monitor confirming stability,

and an audit record proving authority.

All may be representations.

They are not equivalent evidence.

14. Layer 10 - Settlement

Definition

Settlement is reliable consequence registration after transformation.

A transformation is settled when available evidence is sufficient for the evaluation context to update the represented state without unresolved contradictions exceeding defined thresholds.

Settlement does not mean success.

Settlement does not mean approval.

Settlement does not mean moral legitimacy.

Settlement does not mean the transformation was beneficial.

Settlement means the consequence is sufficiently registered to support continued computation, evaluation, or action.

Derivation

Settlement derives from transformation, question, and evidence.

A transformation cannot settle unless its consequences become sufficiently evidenced relative to a question.

Necessity

Without settlement, CEP cannot distinguish completion claims from consequence-backed state updates.

Settlement is the boundary between asserted change and usable change.

Operational Consequence

An implementation MUST distinguish:

attempted transformation,

claimed completion,

observed consequence,

evidenced consequence,

settled transformation,

unsettled transformation,

failed transformation,

harmful but settled transformation,

unauthorized but settled transformation,

beneficial but unsettled transformation,

and incomplete transformation.

Failure Mode

If settlement is collapsed into completion, systems will prematurely declare success.

If settlement is collapsed into approval, systems will hide harmful but real consequences.

If settlement is collapsed into evidence, systems will confuse support with final consequence registration.

15. Derived Core Constructs

The following CEP constructs are derived from the ladder.

They are not foundational layers.

They are named compositions.

15.1 Reality Gap

Reality Gap is the represented divergence between declared state and observed state under a question, supported by evidence.

Derived from:

representation,

state,

observation,

question,

evidence,

and transformation.

Reality Gap exists only when a relevant question makes the divergence visible.

15.2 Authority

Authority is a constraint over permissible transformations from a recognized governance perspective.

Derived from:

constraint,

relation,

state,

transformation,

and question.

Authority does not describe what can happen.

Authority describes what is legitimate within a governance context.

15.3 Affordance

An affordance is a reachable, payable, permissible, executable, and settleable transformation from a current state.

Derived from:

constraint,

state,

transformation,

authority,

evidence,

settlement,

and capability.

A theoretical possibility is not an affordance.

A destination without a spendable path is not an affordance.

15.4 Capability

Capability is the persistent reduction in payment burden for repeated settlement under variation.

Derived from:

transformation history,

evidence,

settlement,

and affordance change.

Capability is not isolated success.

Capability is durable improvement in the system’s ability to produce settled transformations.

15.5 Semantic Envelope

A Semantic Envelope is the canonical transport structure for preserving CEP-relevant context across transformations.

A Semantic Envelope MAY carry:

constraints,

distinctions,

relations,

representations,

states,

transformations,

observations,

questions,

evidence,

settlements,

authority context,

capability updates,

and affordance changes.

Derived from the full ladder.

A Semantic Envelope is not merely a message.

It is a portable transformation context.

15.6 Benchmark

A benchmark is a structured evaluation of transformations against specified invariants under a question.

Derived from:

question,

transformation,

evidence,

settlement,

and metrics.

A benchmark does not merely ask whether an output is correct.

A benchmark asks whether the relevant invariants were preserved, violated, repaired, or transformed.

16. Benchmark Families as Derived Questions

CEP benchmark families are specialized questions over the derivation ladder.

RealityGapBench

Primary question:

Where does declared state diverge from observed state?

Primary evaluation:

Can the system detect, classify, evidence, and explain represented divergence?

AuthorityBench

Primary question:

Was this transformation permissible under the applicable authority constraints?

Primary evaluation:

Can the system correctly allow, deny, or escalate transformations using evidence and policy context?

SettlementBench

Primary question:

Has this transformation produced sufficiently registered consequences to update state?

Primary evaluation:

Can the system distinguish completion claims from settled consequences?

CapabilityBench

Primary question:

Did repeated settlement reduce future transformation cost under variation?

Primary evaluation:

Can the system detect durable capability gain rather than isolated performance?

17. Core Invariants

Every CEP-compliant implementation SHALL preserve the following invariants.

Invariant 1 - Representation Boundary

CEP evaluates representations, not reality directly.

Invariant 2 - Transformation Centrality

CEP evaluation SHALL be organized around transformations, not isolated outputs.

Invariant 3 - Question Dependence

Evaluation SHALL preserve the question or objective that makes evidence relevant.

Invariant 4 - Evidence Traceability

Claims about state, transformation, authority, settlement, or capability SHALL be traceable to evidence or marked as unsupported.

Invariant 5 - Settlement Separation

Settlement SHALL remain distinct from completion, success, approval, and benefit.

Invariant 6 - Authority Separation

Permissibility SHALL remain distinct from possibility.

Invariant 7 - Affordance Discipline

Affordance SHALL mean reachable transformation, not abstract possibility.

Invariant 8 - Capability Durability

Capability SHALL require repeated settlement under variation, not isolated task success.

18. Admission Rule for New Concepts

A new CEP concept MAY be introduced only if it satisfies all conditions below.

It has a clear location in the derivation ladder.

It enables an operation not supported by prior concepts.

It has a defined failure mode.

It can be represented in a Semantic Envelope or derived from one.

It affects validation, scoring, conformance, or interpretation.

It does not collapse an existing distinction.

It does not introduce a new primitive unless the protocol undergoes major revision.

19. Anti-Collapse Rules

CEP implementations SHALL NOT collapse the following distinctions.

19.1 Completion vs Settlement

Completion is a claim that work is done.

Settlement is reliable consequence registration after transformation.

19.2 Possibility vs Affordance

Possibility means a transformation can be imagined.

Affordance means a transformation is reachable, payable, permissible, executable, and settleable from the current state.

19.3 Authority vs Capability

Capability means a system can perform a transformation.

Authority means the transformation is permissible.

19.4 Observation vs Evidence

Observation is registered visibility.

Evidence is observation made relevant to a claim or question.

19.5 Representation vs Reality

Representation preserves selected constraints, distinctions, and relations.

Reality is not directly evaluated by CEP.

19.6 Success vs Settlement

A transformation may settle and still be harmful.

A transformation may be beneficial and still be unsettled.

19.7 Data vs Evidence

Data becomes evidence only when related to a question and claim.

20. First Principles Summary

CEP rests on the following first principles.

Evaluation begins only when constraints become representable.

Constraints become operational through distinctions.

Distinctions become computable through relations.

Relations become durable through representation.

Representations become evaluable as states.

States become meaningful through transformations.

Transformations become visible through observation.

Observation becomes directed through questions.

Questions make observations evidential.

Evidence enables settlement.

Settlement enables state update.

Repeated settlement under variation enables capability.

Capability changes the affordance horizon.

Affordance expansion is the developmental signal of a system becoming more capable.

21. Protocol Consequence

CEP is therefore a protocol for evaluating represented transformations through evidence-backed settlement.

Its core concern is not whether a system produced an output.

Its core concern is whether the system preserved, transformed, violated, repaired, or expanded the relevant constraints governing future action.

22. Derived Specification Sequence

The following documents SHALL derive from CEP-0000.

CEP-0001 - Ontology

Defines the core entities and relationships implied by the derivation ladder.

CEP-0002 - Representation Model

Defines how distinctions and relations are preserved.

CEP-0003 - State Model

Defines situated representations and state identity.

CEP-0004 - Transformation Model

Defines transformation records, invariants, transition types, and transformation validity.

CEP-0005 - Question Model

Defines questions as constraints over observation and evaluation.

CEP-0006 - Evidence Model

Defines evidence types, evidence strength, confidence updates, provenance, and contradiction handling.

CEP-0007 - Settlement Model

Defines settlement states, settlement thresholds, premature completion, settlement debt, and consequence registration.

CEP-0008 - Semantic Envelope

Defines the canonical interchange object for CEP-compatible systems.

CEP-0009 - Benchmark Model

Defines benchmark structure, benchmark cases, answer keys, metrics, scoring, and reporting.

CEP-0010 - Conformance

Defines what it means for tools, benchmarks, runners, validators, and semantic envelopes to be CEP-compliant.

23. Closing Definition

CEP evaluates systems by deriving settlement from constrained transformations through representation, observation, question, and evidence.

This sentence is normative.

Every CEP specification SHALL remain consistent with it.

The next settlement is CEP-0001 - Ontology. That document should convert this ladder into entities, relationships, required fields, and anti-collapse rules so an implementation agent can actually build against it.

Sources:

Excerpt from the Book of Thoth: The Naples Arrangement