CEP-0002 — Representation Model

Status: Draft
Category: Normative
Version: 0.1
Protocol: Canonical Evaluation Protocol
Depends On:

CEP-0000 — Derivation Ladder and First Principles

CEP-0001 — Ontology

Document Type: Foundational Specification

Abstract

This document defines the CEP Representation Model.

CEP evaluates represented transformations, not reality directly. Therefore, every CEP-compatible implementation must preserve how reality is represented, what distinctions are preserved, what relations are encoded, what context is attached, what uncertainty remains, and what omissions are known.

CEP-0002 defines how constraints, distinctions, and relations become durable enough to support state, transformation, observation, question, evidence, settlement, and benchmark evaluation.

This document does not define a final serialization format.

It defines the required representational semantics that any serialization format MUST preserve.

1. Purpose

The purpose of the Representation Model is to prevent CEP implementations from treating text, logs, policies, traces, schemas, benchmark cases, or model outputs as self-explanatory facts.

A representation is never reality.

A representation is a bounded preservation of selected distinctions and relations.

Therefore, every CEP-compatible representation MUST preserve enough context to answer:

What is being represented?

Which distinctions are preserved?

Which relations are preserved?

What is the scope of the representation?

What was omitted, unknown, compressed, or inferred?

Who or what produced the representation?

From what source was it derived?

Under which perspective or question was it produced?

How confident is the representation?

What can safely be computed from it?

2. Scope

This document defines:

representation boundaries,

representation structure,

representation identity,

preserved distinctions,

preserved relations,

provenance,

scope,

uncertainty,

omissions,

compression,

representation operations,

representation validity,

and representation conformance.

This document does not define:

JSON Schema,

YAML syntax,

benchmark file format,

runner implementation,

evidence scoring,

settlement thresholds,

or Semantic Envelope serialization.

Those are defined in later CEP specifications.

3. Core Definition

A Representation is a bounded, versioned, provenance-bearing preservation of selected constraints, distinctions, and relations in a form usable by CEP computation.

A Representation MUST NOT be treated as reality itself.

A Representation MAY be derived from reality, another representation, a document, a log, a model output, a human judgment, a benchmark case, a semantic envelope, a trace, a policy, a state graph, or any other source that preserves relevant distinctions and relations.

4. Representation Boundary

Every Representation has a boundary.

The boundary defines what the Representation includes, excludes, compresses, abstracts, or leaves unknown.

A CEP-compatible Representation MUST preserve this boundary explicitly or provide enough metadata for it to be reconstructed.

4.1 Boundary Requirements

A Representation boundary MUST define:

scope

source

representation_type

included_entities

excluded_entities when known

unknown_entities when relevant

compression_notes when compression is material

perspective_ref when perspective affects representation

question_ref when the representation was produced in response to a question

4.2 Boundary Failure

If a Representation lacks a boundary, downstream systems may treat omitted distinctions as nonexistent.

This creates representational error.

A CEP implementation MUST NOT silently treat absence as falsehood.

Absence MAY mean:

intentionally omitted,

unknown,

not observed,

unavailable,

out of scope,

compressed away,

not applicable,

or lost.

The meaning of absence MUST be preserved when materially relevant.

5. Representation Kinds

CEP recognizes three top-level Representation kinds.

5.1 Atomic Representation

An Atomic Representation preserves one primary claim, distinction, relation, observation, or constraint.

Examples:

“Actor A is authorized to perform operation B.”

“Policy P prohibits transformation T.”

“Test suite S passed at time X.”

“Declared process requires approval before deployment.”

“Observed event shows deployment occurred without approval.”

5.2 Composite Representation

A Composite Representation preserves multiple entities and relations.

Examples:

policy document,

event log,

benchmark case,

semantic envelope,

state graph,

system trace,

organizational map,

authority model,

settlement packet.

5.3 Derived Representation

A Derived Representation is produced from one or more prior Representations.

Examples:

summary,

projection,

transformation diff,

model-generated interpretation,

benchmark result,

normalized schema,

compiled DomainForge output,

evidence packet,

capability update.

A Derived Representation MUST preserve derivation provenance.

6. Minimal Representation Record

A CEP-compatible Representation MUST be able to preserve the following fields.

representation_id
cep_version
representation_kind
representation_type
title_or_label
scope
source
created_at
created_by
version
content_ref
inline_content
preserved_entities
preserved_distinctions
preserved_relations
omission_record
uncertainty_record
provenance_record
identity_refs
perspective_refs
question_refs
evidence_refs
confidence
validation_status

A representation MAY omit optional fields only when they are not material to evaluation.

If a required concept is unknown, it MUST be marked as unknown rather than silently omitted.

7. Representation Identity

A Representation MUST have identity.

Representation identity allows CEP to distinguish:

an original representation from a revision,

a source representation from a derived representation,

a representation from a state,

a representation from an observation,

and a representation from evidence.

7.1 Required Identity Fields

A Representation identity record SHOULD preserve:

representation_id
version
lineage_refs
source_hash
content_hash
semantic_hash
created_at
updated_at
supersedes
superseded_by
equivalence_claims

7.2 Identity Failure

If identity is absent, CEP cannot determine whether a representation was updated, replaced, summarized, corrupted, normalized, or reinterpreted.

This breaks state comparison, transformation evaluation, evidence traceability, and benchmark reproducibility.

8. Content Reference

A Representation MAY preserve content inline or by reference.

8.1 Inline Content

Inline content is embedded directly in the Representation.

This is appropriate for small representations, benchmark cases, claims, short observations, and normalized records.

8.2 External Content Reference

A content reference points to an external artifact.

Examples:

file path,

URI,

content-addressed hash,

database record,

trace ID,

commit hash,

document ID,

object storage key.

If content is external, the Representation MUST preserve enough information to retrieve or verify it.

8.3 Content Integrity

When possible, external content SHOULD be content-addressed.

A Representation SHOULD preserve one or more of:

content_hash

source_hash

semantic_hash

signature

timestamp

version_ref

9. Preserved Entities

A Representation MAY preserve any CEP ontology entity.

At minimum, a Representation MUST be able to preserve references to:

Constraints,

Distinctions,

Relations,

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

and Semantic Envelopes.

A Representation does not need to contain all of these.

It MUST preserve which entities are included and which materially relevant entities are omitted, unknown, or out of scope.

10. Preserved Distinctions

Distinctions are the minimum unit of evaluable difference.

A CEP-compatible Representation MUST preserve distinctions required for its evaluation context.

10.1 Distinction Record

A Distinction record SHOULD preserve:

distinction_id
left_term
right_term
basis
distinction_kind
scope
source
confidence
evidence_refs

10.2 Required Distinction Examples

CEP implementations SHOULD be able to preserve distinctions such as:

declared / observed
possible / permissible
attempted / transformed
completed / settled
authorized / unauthorized
supported / unsupported
known / unknown
included / omitted
capable / incapable
reachable / unreachable
beneficial / harmful
valid / invalid

10.3 Distinction Failure

If a relevant distinction is not preserved, CEP cannot evaluate the transformation requiring that distinction.

For example:

RealityGapBench fails if declared and observed state collapse.

AuthorityBench fails if possible and permissible collapse.

SettlementBench fails if completion and settlement collapse.

CapabilityBench fails if isolated success and durable capability collapse.

11. Preserved Relations

Relations connect distinctions and entities.

A CEP-compatible Representation MUST preserve relations required for its evaluation context.

11.1 Relation Record

A Relation record SHOULD preserve:

relation_id
relation_type
source_entity_ref
target_entity_ref
scope
confidence
evidence_refs
temporal_context
authority_context

11.2 Required Relation Support

CEP-compatible Representations MUST support at least the relation types defined in CEP-0001:

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

11.3 Relation Failure

If relations are not preserved, CEP cannot determine:

what evidence supports,

what policy applies,

what transformation occurred,

what state changed,

what authority governs,

what contradiction exists,

or what settlement updates.

12. Scope

Scope defines the boundary within which a Representation is valid or intended to be interpreted.

12.1 Scope Record

A Scope record SHOULD preserve:

scope_id
domain
organization_or_system
process
team
artifact
actor_group
time_range
jurisdiction
environment
benchmark_family
evaluation_context
limitations

12.2 Scope Discipline

A Representation MUST NOT be applied outside its scope without either:

an explicit projection,

an explicit assumption,

or an explicit out-of-scope warning.

12.3 Scope Failure

If scope is not preserved, a valid local representation may be incorrectly treated as globally valid.

This creates false authority, false capability, false settlement, and false affordance claims.

13. Perspective

A Perspective determines what distinctions and relations become visible, relevant, or meaningful within a Representation.

13.1 Perspective Requirement

A Representation MUST preserve Perspective when interpretation materially depends on it.

Examples:

auditor perspective,

operator perspective,

agent perspective,

customer perspective,

regulator perspective,

benchmark perspective,

organization perspective.

13.2 Perspective Failure

If Perspective is omitted, CEP cannot explain why the same underlying event appears as:

acceptable to an operator,

noncompliant to an auditor,

invisible to a customer,

risky to a security team,

or decisive to a benchmark.

14. Question Context

A Representation MAY be created in response to a Question.

When it is, the Question MUST be preserved.

14.1 Question Context Record

A Question Context record SHOULD preserve:

question_ref
question_type
evaluation_objective
target_entities
relevance_rules
expected_answer_shape

14.2 Question Failure

If Question is omitted, CEP cannot determine why certain evidence or distinctions were selected.

A Representation without question context may still be valid, but its evaluative meaning is limited.

15. Provenance

Provenance records where a Representation came from and how it was produced.

CEP-compatible Representations MUST preserve provenance.

15.1 Provenance Record

A Provenance record SHOULD include:

provenance_id
source_type
source_ref
producer
production_method
created_at
derived_from
transformation_refs
tool_refs
model_refs
human_refs
review_status
verification_status

15.2 Provenance Types

CEP recognizes the following source types:

human_statement
policy_document
system_log
trace
test_result
monitoring_signal
code_artifact
configuration
model_output
benchmark_case
semantic_envelope
external_record
manual_observation
compiled_representation
unknown

15.3 Provenance Failure

If provenance is absent, CEP cannot distinguish:

source from interpretation,

original from derived,

evidence from claim,

human judgment from automated observation,

and verified representation from unreviewed model output.

16. Omission Record

Every Representation is incomplete.

A CEP-compatible Representation MUST preserve material omissions when known.

16.1 Omission Record

An Omission record SHOULD preserve:

omission_id
omission_type
description
reason
known_or_suspected
impact
affected_entities
confidence

16.2 Omission Types

CEP recognizes the following omission types:

unknown
unobserved
unavailable
out_of_scope
intentionally_excluded
compressed
redacted
lost
not_applicable
not_collected
ambiguous

16.3 Absence Semantics

A CEP-compatible implementation MUST distinguish:

false
unknown
missing
not_applicable
out_of_scope
redacted
not_observed
not_collected
intentionally_omitted

16.4 Omission Failure

If omissions are not preserved, a system may mistake unknown for false, unobserved for absent, or redacted for nonexistent.

This causes invalid evaluation.

17. Uncertainty Record

A Representation MUST preserve uncertainty when uncertainty materially affects evaluation.

17.1 Uncertainty Record

An Uncertainty record SHOULD preserve:

uncertainty_id
uncertainty_type
affected_entities
description
confidence
confidence_basis
evidence_refs
resolution_requirements

17.2 Uncertainty Types

CEP recognizes the following uncertainty types:

identity_uncertainty
scope_uncertainty
source_uncertainty
temporal_uncertainty
semantic_uncertainty
authority_uncertainty
evidence_uncertainty
settlement_uncertainty
causal_uncertainty
confidence_uncertainty

17.3 Uncertainty Failure

If uncertainty is not represented, systems overstate confidence.

This leads to premature settlement, false authority, false capability, and unreliable benchmark results.

18. Confidence

Confidence expresses the represented degree of support for a Representation, entity, relation, claim, or derived result.

CEP does not require one universal confidence calculus in this document.

However, confidence MUST be preserved when used.

18.1 Confidence Record

A Confidence record SHOULD include:

confidence_value
confidence_scale
confidence_basis
evidence_refs
calculation_method
limitations

18.2 Confidence Scale

Implementations MAY use numeric, ordinal, categorical, or qualitative confidence scales.

The scale MUST be declared.

Examples:

0.0 - 1.0 numeric
low / medium / high
unsupported / weak / moderate / strong
unknown / partial / confident

18.3 Confidence Failure

A confidence value without a declared scale is invalid for protocol-level comparison.

A confidence value without a basis SHOULD be treated as unsupported.

19. Compression

All Representations compress.

Compression is not a flaw.

Unmarked compression is a flaw.

19.1 Compression Record

A Compression record SHOULD preserve:

compression_type
source_representation_refs
preserved_distinctions
discarded_distinctions
summary_rules
loss_notes
confidence_impact

19.2 Compression Types

CEP recognizes:

summary
abstraction
generalization
projection
normalization
aggregation
filtering
sampling
embedding
schema_mapping
model_interpretation
manual_interpretation

19.3 Compression Failure

If compression is not marked, downstream tools may treat summaries, embeddings, or interpretations as complete source records.

This corrupts evidence and settlement.

20. Representation Operations

CEP-compatible implementations MAY perform operations over Representations.

When these operations are performed, they SHOULD preserve provenance and loss.

20.1 Projection

Projection creates a Representation containing selected distinctions and relations from a source Representation.

Projection MUST preserve what was selected and what was excluded when material.

20.2 Composition

Composition combines multiple Representations into a larger Representation.

Composition MUST preserve source lineage and conflict records.

20.3 Comparison

Comparison identifies differences between Representations.

Comparison MUST preserve the question or criteria under which differences are relevant.

20.4 Diff

Diff is a comparison optimized to identify changes across versions, states, or transformations.

Diff MUST preserve identity assumptions.

20.5 Normalization

Normalization maps a Representation into a standard form.

Normalization MUST preserve mapping rules and loss notes.

20.6 Translation

Translation maps a Representation from one language, schema, domain model, or ontology into another.

Translation MUST preserve uncertainty and semantic loss.

20.7 Summarization

Summarization creates a compressed Representation.

Summarization MUST NOT be treated as equivalent to the source Representation unless equivalence is explicitly established.

20.8 Validation

Validation checks whether a Representation satisfies required constraints.

Validation MUST distinguish schema validity from semantic validity.

20.9 Enrichment

Enrichment adds additional context, evidence, relations, or metadata to a Representation.

Enrichment MUST preserve the source of added material.

21. Equivalence

Two Representations MAY be considered equivalent only under declared criteria.

CEP recognizes several equivalence types.

byte_equivalent
schema_equivalent
semantic_equivalent
functional_equivalent
evidence_equivalent
state_equivalent
benchmark_equivalent

Equivalence MUST preserve:

equivalence_type
criteria
scope
confidence
evidence_refs
limitations

21.1 Equivalence Failure

If equivalence criteria are omitted, systems may treat paraphrases, summaries, translations, or projections as identical.

This is invalid.

22. Validity

A Representation may be valid in one sense and invalid in another.

CEP recognizes the following validity dimensions.

syntax_validity
schema_validity
semantic_validity
provenance_validity
scope_validity
identity_validity
evidence_validity
benchmark_validity
settlement_validity

A CEP-compatible implementation MUST NOT collapse these validity dimensions.

22.1 Example

A model-generated summary may be syntactically valid and semantically plausible while lacking provenance validity and evidence validity.

Such a Representation may be usable for exploration but not settlement.

23. Representation Lifecycle

A Representation MAY pass through the following lifecycle states.

created
draft
normalized
validated
reviewed
accepted
superseded
deprecated
rejected
archived
unknown

Lifecycle state MUST NOT be confused with truth.

An accepted Representation may later be contradicted.

A draft Representation may preserve accurate distinctions.

A rejected Representation may still be useful as evidence of error.

24. Representation Quality

CEP-compatible implementations MAY assess Representation quality.

Quality SHOULD be evaluated across:

fidelity
completeness
traceability
scope_clarity
identity_clarity
evidence_support
semantic_precision
loss_marking
confidence_calibration
updateability

Representation quality is context-dependent.

A high-quality Representation for one Question may be low-quality for another.

25. Representation Errors

CEP recognizes the following representation error classes.

omission_error
commission_error
scope_error
identity_error
relation_error
temporal_error
semantic_error
authority_error
evidence_error
confidence_error
compression_error
translation_error
projection_error
equivalence_error
staleness_error

A CEP-compatible implementation SHOULD classify representation errors when they materially affect evaluation.

26. Declared and Observed Representations

CEP makes frequent use of declared and observed Representations.

26.1 Declared Representation

A Declared Representation preserves what a system, actor, organization, policy, or benchmark claims should be true, intended, required, permitted, prohibited, or expected.

Examples:

policies,

SOPs,

org charts,

design documents,

role definitions,

architecture diagrams,

intended workflows,

requirements,

mission statements,

control plans.

26.2 Observed Representation

An Observed Representation preserves what appears to have occurred, existed, changed, failed, settled, or drifted.

Examples:

logs,

traces,

test results,

monitoring data,

interviews,

audit records,

diffs,

incident reports,

actual workflows,

model outputs,

execution records.

26.3 Reality Gap Requirement

Reality Gap evaluation MUST preserve declared and observed Representations separately.

A CEP implementation MUST NOT overwrite declared Representation with observed Representation or vice versa.

27. Representation and State

A Representation is not automatically a State.

A Representation becomes a State when it is situated enough to support comparison, transformation, or evaluation.

27.1 State-Sufficient Representation

A Representation is state-sufficient when it preserves:

scope
time_context
identity_refs
relevant_constraints
relevant_distinctions
relevant_relations
confidence

A benchmark case SHOULD make clear whether a Representation is state-sufficient.

28. Representation and Evidence

A Representation is not automatically Evidence.

A Representation becomes Evidence when it is related to a Claim and Question.

28.1 Evidence-Sufficient Representation

A Representation is evidence-sufficient when it preserves:

source
provenance
target_claim_ref
question_ref
relevance
reliability
confidence_impact
limitations

A log line may be a Representation.

It becomes Evidence only when it bears on a Claim.

29. Representation and Semantic Envelope

A Semantic Envelope is a Composite Representation optimized for transporting CEP-relevant context across Transformations.

A Semantic Envelope MUST preserve Representation semantics defined in this document.

A Semantic Envelope MAY contain multiple Representations, States, Transformations, Observations, Claims, Evidence records, and Settlements.

A Semantic Envelope MUST preserve omissions, uncertainty, provenance, and identity when materially relevant.

30. Representation and Benchmark Cases

A benchmark case is a Composite Representation.

A CEP-compatible benchmark case MUST preserve:

case_id
benchmark_ref
question_ref
input_representations
expected_answer_shape
answer_key
evidence_requirements
scoring_rules
omission_records
uncertainty_records
source_provenance

A benchmark case MUST NOT hide material answer-key assumptions from the evaluator unless the benchmark explicitly tests hidden-state inference.

31. Representation Conformance

A CEP-compatible Representation implementation MUST satisfy the following requirements.

It MUST preserve Representation identity.

It MUST preserve scope.

It MUST preserve provenance.

It MUST distinguish preserved, omitted, unknown, and out-of-scope material.

It MUST preserve relevant distinctions.

It MUST preserve relevant relations.

It MUST distinguish Representation from State.

It MUST distinguish Representation from Evidence.

It MUST preserve confidence when confidence is used.

It MUST preserve uncertainty when uncertainty is material.

It MUST preserve derivation lineage for Derived Representations.

It MUST mark compression, projection, summarization, translation, or normalization when performed.

It MUST NOT treat absence as falsehood unless explicitly justified.

It MUST NOT treat summaries as equivalent to sources without declared equivalence criteria.

It MUST NOT treat model output as verified evidence without provenance and evidence qualification.

32. Minimal Valid Representation

A minimally valid CEP Representation MUST contain:

representation_id
representation_kind
representation_type
scope
source
created_at
version
content_ref OR inline_content
provenance_record
preserved_distinctions OR preserved_entities
omission_record OR omission_status
confidence OR confidence_status

A Representation lacking both preserved distinctions and preserved entities is not CEP-valid.

A Representation lacking provenance is not settlement-valid.

A Representation lacking scope is not benchmark-valid.

33. Invalid Representation Conditions

A Representation is invalid for CEP evaluation if:

it lacks identity,

it lacks scope,

it lacks provenance,

it erases known omissions,

it collapses declared and observed material,

it treats model interpretation as verified fact,

it treats unknown as false,

it treats summary as source,

it loses material distinction,

it loses material relation,

it lacks confidence basis when confidence is used,

or it cannot be traced to source or derivation lineage.

Invalid Representations MAY still be stored.

Invalid Representations MUST NOT be used for settlement, authority decision, capability claim, or benchmark scoring unless the invalidity itself is the object of evaluation.

34. Representation Invariants

CEP-compatible systems SHALL preserve the following invariants.

Invariant 1 — Boundary Preservation

A Representation SHALL preserve what it includes and what it excludes when material.

Invariant 2 — Reality Separation

A Representation SHALL NOT be treated as reality itself.

Invariant 3 — Distinction Preservation

A Representation SHALL preserve distinctions required by its evaluation context.

Invariant 4 — Relation Preservation

A Representation SHALL preserve relations required by its evaluation context.

Invariant 5 — Provenance Preservation

A Representation SHALL preserve source and derivation provenance.

Invariant 6 — Omission Preservation

Known omissions SHALL be marked.

Invariant 7 — Uncertainty Preservation

Material uncertainty SHALL be marked.

Invariant 8 — Compression Honesty

Compression SHALL be disclosed when material.

Invariant 9 — Scope Discipline

A Representation SHALL NOT be applied outside scope without projection or warning.

Invariant 10 — Evidence Separation

A Representation SHALL NOT be treated as Evidence unless related to a Claim and Question.

35. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:

representation into reality
representation into state
representation into evidence
source into summary
claim into evidence
absence into falsehood
unknown into not applicable
observed into declared
declared into observed
confidence into truth
syntax validity into semantic validity
model output into verified observation
projection into full source
translation into equivalence

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

36. Implementation Consequence

Any CEP-compatible implementation that creates, consumes, validates, scores, stores, or transports Representations MUST implement representation metadata.

A system that only passes raw text, raw JSON, raw logs, or raw model output without boundary, provenance, scope, omission, and uncertainty semantics is not CEP-compliant.

This requirement exists because CEP evaluates transformations through representations.

If the representation is unbounded, unscoped, unprovenanced, or semantically collapsed, the evaluation is unreliable.

37. Closing Definition

The CEP Representation Model defines how constraints, distinctions, and relations become durable enough to support state, transformation, observation, question, evidence, settlement, and benchmark evaluation.

A Representation is not reality.

A Representation is a bounded preservation of selected distinctions and relations.

Everything CEP evaluates depends on the quality, scope, provenance, and integrity of that preservation.

The next document should be CEP-0003 — State Model. That is where we define how a representation becomes situated, how identity continuity works, and how declared, observed, expected, claimed, authorized, settled, and counterfactual states behave.