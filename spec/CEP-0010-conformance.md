CEP-0010 — Conformance

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

CEP-0006 — Evidence Model

CEP-0007 — Settlement Model

CEP-0008 — Semantic Envelope

CEP-0009 — Benchmark Model

Document Type: Foundational Specification

Abstract

This document defines CEP conformance.

Conformance specifies what it means for an implementation, tool, runner, benchmark, dataset, Semantic Envelope, result, adapter, or profile to be compatible with the Canonical Evaluation Protocol.

CEP conformance is not a branding claim.

CEP conformance is a testable claim that an implementation preserves the distinctions, structures, invariants, and anti-collapse rules required to evaluate represented transformations through evidence-backed settlement.

A system is not CEP-compliant merely because it uses CEP vocabulary.

A system is CEP-compliant only when it preserves the required protocol semantics and can produce evidence of doing so.

1. Purpose

The purpose of conformance is to protect the protocol from semantic dilution.

CEP introduces distinctions that are easy to say and easy to collapse:

representation vs reality,

state vs representation,

action vs transformation,

prompt vs question,

data vs evidence,

claim vs evidence,

completion vs settlement,

settlement vs success,

authority vs capability,

possibility vs affordance,

score vs capability.

A CEP-conformant implementation MUST preserve these distinctions in structure and behavior.

Conformance exists so that independent implementations can exchange Semantic Envelopes, run benchmarks, validate results, and compare evaluations without redefining the protocol each time.

2. Scope

This document defines:

conformance claims,

conformance classes,

conformance levels,

validation targets,

required validation outputs,

error and warning categories,

required evidence for conformance,

conformance profiles,

conformance testing,

conformance reports,

non-conformance handling,

compatibility and versioning,

extension conformance,

and anti-collapse enforcement.

This document does not define:

final JSON Schema,

final CLI behavior,

implementation language,

hosted registry governance,

certification authority,

or legal certification rules.

Those are defined in later implementation profiles or governance documents.

3. Core Definition

Conformance is the demonstrated preservation of CEP-required semantics for a declared conformance target, scope, profile, and protocol version.

A conformance claim MUST identify:

conformance_claim_id
target_ref
target_type
cep_version
profile_refs
conformance_level
scope
validation_method
validation_result_ref
evidence_refs
created_at
claimed_by
limitations

A conformance claim without target, version, scope, validation result, and evidence is not CEP-valid.

4. Conformance Is Not Compatibility

CEP SHALL distinguish conformance from compatibility.

4.1 Compatibility

Compatibility means a system can interoperate with some CEP-related structure.

Examples:

can read a Semantic Envelope,

can export a benchmark result,

can parse a CEP-like case file,

can map internal records to CEP fields.

4.2 Conformance

Conformance means a system preserves required CEP semantics and passes applicable validation requirements.

A compatible system may be non-conformant.

4.3 Anti-Collapse Rule

A CEP implementation MUST NOT claim conformance merely because it is compatible with a CEP file format.

5. Conformance Is Not Certification

CEP conformance is a protocol-level validation claim.

Certification is an external governance process that MAY use conformance results.

CEP does not define legal, commercial, regulatory, or third-party certification in this document.

A system may be CEP-conformant without being externally certified.

A system may be certified by an external body only if that body defines its own certification process.

6. Conformance Targets

CEP conformance MAY apply to the following target types:

representation
state
transformation
question
evidence
settlement
semantic_envelope
benchmark
benchmark_case
benchmark_dataset
benchmark_result
runner
adapter
system_under_evaluation
profile
extension
validator
conformance_report
implementation

Each target type has different requirements.

A target MUST NOT claim general CEP conformance when it only satisfies a narrower conformance class.

7. Conformance Classes

CEP defines the following conformance classes.

CEP-Core
CEP-Representation
CEP-State
CEP-Transformation
CEP-Question
CEP-Evidence
CEP-Settlement
CEP-Envelope
CEP-Benchmark
CEP-Runner
CEP-Adapter
CEP-Result
CEP-Profile
CEP-Validator
CEP-Implementation

7.1 CEP-Core

Preserves the foundational ontology, derivation ladder, and anti-collapse rules.

7.2 CEP-Representation

Conforms to CEP-0002.

7.3 CEP-State

Conforms to CEP-0003.

7.4 CEP-Transformation

Conforms to CEP-0004.

7.5 CEP-Question

Conforms to CEP-0005.

7.6 CEP-Evidence

Conforms to CEP-0006.

7.7 CEP-Settlement

Conforms to CEP-0007.

7.8 CEP-Envelope

Conforms to CEP-0008.

7.9 CEP-Benchmark

Conforms to CEP-0009.

7.10 CEP-Runner

Can execute CEP Benchmarks while preserving benchmark, case, answer, result, evidence, and provenance semantics.

7.11 CEP-Adapter

Maps between a Runner and System Under Evaluation without hiding transformation, question, evidence, or answer semantics.

7.12 CEP-Result

Preserves benchmark result structure, score basis, provenance, evidence, errors, warnings, and conformance status.

7.13 CEP-Profile

Adds domain-specific or benchmark-specific constraints without overwriting core CEP semantics.

7.14 CEP-Validator

Can validate one or more CEP target types and produce conformance reports.

7.15 CEP-Implementation

A system implementing multiple CEP classes under declared scope.

8. Conformance Levels

CEP defines four conformance levels.

L0 — Non-Conformant
L1 — Structural Conformance
L2 — Semantic Conformance
L3 — Operational Conformance
L4 — Evidence-Backed Conformance

8.1 L0 — Non-Conformant

The target fails required CEP validation or does not preserve required semantics.

8.2 L1 — Structural Conformance

The target satisfies required structural fields.

Example:

A Semantic Envelope has required metadata, sections, identifiers, and references.

Structural conformance does not prove semantic correctness.

8.3 L2 — Semantic Conformance

The target preserves required CEP meanings, anti-collapse distinctions, scope, provenance, and entity relationships.

Example:

A benchmark preserves the distinction between completion and settlement.

8.4 L3 — Operational Conformance

The target behaves correctly under required operations.

Example:

A Runner validates cases, preserves answer shape, records evidence, scores results, emits warnings, and preserves run provenance.

8.5 L4 — Evidence-Backed Conformance

The target provides evidence that it satisfied required structural, semantic, and operational requirements.

Example:

A Runner produces conformance evidence showing validation checks, error handling, benchmark version, case hashes, adapter mapping, evidence references, and result provenance.

8.6 Level Discipline

A target MUST NOT claim a higher conformance level than it has demonstrated.

A target MAY be L1-conformant for one class and L0 for another.

9. Conformance Status

A conformance result MUST use one of the following statuses:

conformant
partially_conformant
non_conformant
not_evaluable
unknown

9.1 Conformant

All required checks for the declared target, class, profile, and level passed.

9.2 Partially Conformant

Some required checks passed and others failed, were skipped, or were out of scope.

Partial conformance MUST specify which requirements failed or were not evaluated.

9.3 Non-Conformant

One or more required checks failed.

9.4 Not Evaluable

The target lacks enough information to evaluate conformance.

9.5 Unknown

Conformance status has not been determined.

10. Conformance Claim

A Conformance Claim is an assertion that a target satisfies specific CEP requirements.

10.1 Required Claim Fields

A Conformance Claim MUST preserve:

claim_id
target_ref
target_type
cep_version
conformance_class
conformance_level
profile_refs
scope
claimant_ref
validation_result_ref
evidence_refs
created_at
limitations

10.2 Claim Failure

A Conformance Claim is invalid if it lacks target, version, class, level, validation result, and evidence.

A claim that says “CEP-compatible” without specifying class and level is ambiguous and SHOULD be rejected or downgraded to an informal compatibility claim.

11. Conformance Report

A Conformance Report records validation results.

11.1 Required Report Fields

A Conformance Report MUST preserve:

report_id
target_ref
target_type
cep_version
conformance_class
conformance_level
profile_refs
validation_method
validator_ref
validation_time
requirements_evaluated
passed_requirements
failed_requirements
skipped_requirements
warnings
errors
evidence_refs
conformance_status
limitations

11.2 Report Portability

A Conformance Report SHOULD be representable as a Semantic Envelope.

11.3 Report Failure

A Conformance Report without evaluated requirements, validation method, and evidence is not CEP-valid.

12. Validation Requirement

A validation requirement is a specific rule that must be checked.

12.1 Requirement Record

A validation requirement SHOULD preserve:

requirement_id
spec_ref
requirement_text
target_type
severity
validation_method
failure_condition
repair_guidance

12.2 Requirement Severity

Requirement severity SHOULD be one of:

error
warning
info
profile_specific

12.3 Requirement Failure

A requirement that lacks failure condition cannot be validated.

13. Validation Methods

CEP recognizes the following validation methods:

schema_validation
semantic_validation
reference_validation
provenance_validation
integrity_validation
anti_collapse_validation
operation_validation
evidence_validation
settlement_validation
benchmark_validation
manual_review
hybrid_review
unknown

13.1 Schema Validation

Checks structural fields, types, required sections, and syntax.

13.2 Semantic Validation

Checks whether CEP meanings and relations are preserved.

13.3 Reference Validation

Checks whether references are resolvable, available, or correctly marked unavailable.

13.4 Provenance Validation

Checks source, lineage, and derivation metadata.

13.5 Integrity Validation

Checks hashes, signatures, tamper status, or content identity.

13.6 Anti-Collapse Validation

Checks whether CEP distinctions were preserved.

13.7 Operation Validation

Checks whether required operations behave correctly.

13.8 Evidence Validation

Checks evidence target binding, question binding, source, provenance, reliability, relevance, and direction.

13.9 Settlement Validation

Checks threshold, evidence sufficiency, consequence registration, contradictions, debt, and state update recommendation.

13.10 Benchmark Validation

Checks benchmark questions, cases, answer keys, metrics, scoring rules, result provenance, and reproducibility.

14. Error and Warning Model

CEP validation MUST distinguish errors from warnings.

14.1 Error

An Error indicates violation of a required conformance rule.

Errors usually prevent conformance for the declared level, class, or profile.

14.2 Warning

A Warning indicates weakness, uncertainty, incompleteness, or risk that does not necessarily invalidate conformance.

14.3 Required Error Fields

An Error SHOULD preserve:

error_id
requirement_ref
target_ref
error_type
message
severity
repair_guidance
evidence_refs

14.4 Required Warning Fields

A Warning SHOULD preserve:

warning_id
requirement_ref
target_ref
warning_type
message
risk
repair_guidance
evidence_refs

15. Core Error Types

CEP recognizes the following core error types:

missing_required_field
invalid_reference
invalid_scope
missing_provenance
missing_identity
missing_question
missing_answer_shape
missing_evidence_binding
missing_settlement_threshold
missing_state_context
missing_transformation_context
invalid_conformance_claim
anti_collapse_violation
unsupported_claim
invalid_score
invalid_result
invalid_envelope
invalid_benchmark
invalid_runner_output
profile_violation
version_incompatibility
unknown

16. Core Warning Types

CEP recognizes the following core warning types:

partial_context
weak_evidence
low_confidence
stale_evidence
scope_uncertainty
identity_uncertainty
temporal_uncertainty
hidden_assumption
known_omission
unresolved_contradiction
non_blocking_profile_issue
incomplete_provenance
reference_unavailable
manual_review_recommended
unknown

17. Anti-Collapse Conformance

Anti-collapse rules are central to CEP conformance.

A target is not semantically conformant if it collapses protected distinctions.

17.1 Protected Distinctions

A CEP validator SHOULD check that the following distinctions are preserved when relevant:

representation / reality
representation / state
state / transformation
action / transformation
prompt / question
question / answer
data / evidence
claim / evidence
evidence / settlement
completion / settlement
settlement / success
settlement / approval
settlement / benefit
possibility / affordance
authority / capability
score / capability
signature / truth
summary / source
redaction / absence
unknown / false

17.2 Anti-Collapse Error

If a protected distinction is required and collapsed, the validator MUST emit an anti-collapse violation.

17.3 Anti-Collapse Warning

If a protected distinction may be collapsed but evidence is insufficient to prove violation, the validator SHOULD emit a warning.

18. Conformance Evidence

Conformance MUST be evidence-backed at L4.

18.1 Conformance Evidence Types

Conformance evidence MAY include:

schema_validation_result
semantic_validation_result
test_result
conformance_suite_result
manual_review_record
golden_case_result
operation_trace
runner_log
adapter_mapping_record
hash_verification
signature_verification
benchmark_result_envelope
evidence_packet
settlement_packet

18.2 Evidence Requirements

Conformance Evidence MUST preserve:

evidence_ref
target_ref
requirement_ref
question_ref
source
provenance
relevance
reliability
direction
confidence_impact

18.3 Evidence Failure

A conformance claim without evidence MAY be treated as L1, L2, or L3 only if the level does not require evidence-backed proof.

It MUST NOT claim L4.

19. CEP-Core Conformance

A target conforms to CEP-Core when it preserves the foundational protocol invariants.

19.1 CEP-Core Requirements

A CEP-Core conformant target MUST:

preserve representation boundary,

preserve transformation centrality when evaluating change,

preserve question dependence,

preserve evidence traceability,

preserve settlement separation,

preserve authority separation,

preserve affordance discipline,

preserve capability durability,

preserve omissions and unknowns when material,

preserve provenance when used for evaluation.

19.2 CEP-Core Failure

A target that collapses CEP’s core distinctions is not CEP-Core conformant.

20. Representation Conformance

A CEP-Representation target conforms when it satisfies CEP-0002.

20.1 Required Checks

A validator SHOULD check:

representation_id exists
scope exists
provenance exists
boundary exists
preserved distinctions exist or preserved entities exist
omission status exists
uncertainty status exists when material
source and derived lineage are preserved
summary is not treated as source
absence is not treated as false

21. State Conformance

A CEP-State target conforms when it satisfies CEP-0003.

21.1 Required Checks

A validator SHOULD check:

state_id exists
state_type exists
subject_ref exists
scope exists
time_context exists when material
identity_refs or identity_uncertainty exists
relevant_constraints exist or are marked
relevant_distinctions exist
relevant_relations exist
provenance exists
declared and observed states remain separable
claimed and evidenced states remain separable
unknown is not treated as false

22. Transformation Conformance

A CEP-Transformation target conforms when it satisfies CEP-0004.

22.1 Required Checks

A validator SHOULD check:

transformation_id exists
transformation_type exists
source_state_ref exists
target-like state or target claim exists
scope exists
identity basis or uncertainty exists
time context exists when material
affected distinctions or constraints exist
status exists
action is not collapsed into transformation
expected, claimed, observed, actual, and settled targets remain separable
authority context exists when authority is material
evidence hooks exist when settlement is claimed

23. Question Conformance

A CEP-Question target conforms when it satisfies CEP-0005.

23.1 Required Checks

A validator SHOULD check:

question_id exists
question_form exists
question_type exists
scope exists
target entities, states, or transformations exist
relevance rules or relevance basis exists
expected answer shape exists
evaluation context exists
question is not collapsed into prompt
question is not collapsed into answer
material assumptions are marked
material unknowns are marked

24. Evidence Conformance

A CEP-Evidence target conforms when it satisfies CEP-0006.

24.1 Required Checks

A validator SHOULD check:

evidence_id exists
evidence_type exists
question_ref exists
target claim or target entity exists
representation_ref exists
source exists
provenance exists
relevance exists
reliability exists
direction exists
confidence impact exists
timestamp exists
scope exists
data is not collapsed into evidence
claim is not evidence for itself
known contradictions are preserved

25. Settlement Conformance

A CEP-Settlement target conforms when it satisfies CEP-0007.

25.1 Required Checks

A validator SHOULD check:

settlement_id exists
settlement_status exists
transformation_ref exists
question_ref exists
evidence_refs exist
threshold or threshold basis exists
observed consequences or missing consequence record exists
confidence or confidence status exists
unresolved contradictions or contradiction status exists
missing evidence or missing evidence status exists
state update recommendation exists
completion is not collapsed into settlement
settlement is not collapsed into success, approval, or benefit
debt is preserved when present

26. Semantic Envelope Conformance

A CEP-Envelope target conforms when it satisfies CEP-0008.

26.1 Required Checks

A validator SHOULD check:

envelope_id exists
cep_version exists
envelope_version exists
envelope_kind exists
created_at exists
created_by exists
scope exists
boundary record exists
completeness status exists
provenance exists
at least one CEP entity section exists
omission status exists
raw context is not treated as semantic structure
references preserve availability and integrity status
merge conflicts are not silently resolved
extensions do not overwrite core semantics

27. Benchmark Conformance

A CEP-Benchmark target conforms when it satisfies CEP-0009.

27.1 Required Checks

A validator SHOULD check:

benchmark_id exists
benchmark_name exists
benchmark_version exists
cep_version exists
primary_question_ref exists
case_refs exist
metric_refs exist
answer_key_refs or oracle mechanism exists
expected_answer_shape exists
scoring_rules exist
evidence requirements or evidence status exists
provenance exists
conformance requirements exist
benchmark is not collapsed into task list
score is not collapsed into capability
answer correctness is not collapsed into evidence sufficiency

28. Runner Conformance

A CEP-Runner target conforms when it correctly executes CEP Benchmarks under declared scope.

28.1 Required Runner Checks

A Runner SHOULD demonstrate that it can:

load benchmark definitions,

validate benchmark structure,

validate benchmark cases,

provide case inputs without corrupting context,

preserve primary and case Questions,

collect system answers,

validate answer shape,

preserve system identity,

preserve runner identity,

preserve adapter identity,

bind evidence when required,

score according to declared metrics,

emit errors and warnings,

produce result records,

produce result envelopes,

preserve run provenance,

preserve reproducibility metadata.

28.2 Runner Failure

A Runner that produces scores without preserving run context is not CEP-Runner conformant.

29. Adapter Conformance

A CEP-Adapter target conforms when it maps between Runner and System Under Evaluation without semantic corruption.

29.1 Required Adapter Checks

An Adapter SHOULD preserve:

adapter_id
adapter_type
system_ref
input_mapping
output_mapping
evidence_mapping
limitations
version
provenance_refs

29.2 Adapter Failure

An Adapter that changes question, answer shape, evidence semantics, or case context without recording transformation provenance is non-conformant.

30. Result Conformance

A CEP-Result target conforms when it preserves benchmark result context.

30.1 Required Result Checks

A Result MUST preserve:

result_id
benchmark_ref
case_ref OR campaign_ref
system_ref
runner_ref
adapter_ref
answer_ref
score_refs
status
errors
warnings
provenance_refs
created_at

30.2 Result Failure

A Result without benchmark version, case reference, system identity, runner identity, score basis, and provenance is not CEP-Result conformant.

31. Profile Conformance

A CEP-Profile target conforms when it adds requirements without violating CEP core semantics.

31.1 Profile Requirements

A Profile MUST preserve:

profile_id
profile_name
profile_version
cep_version
target_classes
additional_requirements
validation_rules
compatibility_notes
extension_rules

31.2 Profile Failure

A Profile is invalid if it overwrites CEP core meanings, collapses protected distinctions, or makes a non-conformant target appear conformant.

32. Extension Conformance

A CEP extension conforms when it is namespaced, versioned, declared, and non-destructive.

32.1 Extension Requirements

An Extension SHOULD preserve:

extension_id
namespace
extension_version
schema_ref
target_classes
content
compatibility_notes
required_or_optional

32.2 Extension Failure

An Extension is non-conformant if it silently changes core CEP semantics.

33. Validator Conformance

A CEP-Validator conforms when it can evaluate declared target classes and produce valid conformance reports.

33.1 Validator Requirements

A Validator SHOULD preserve:

validator_id
validator_name
validator_version
cep_version
supported_classes
supported_profiles
validation_methods
known_limitations
conformance_status

33.2 Validator Behavior

A Validator MUST:

identify target type,

identify applicable CEP version,

identify applicable class and profile,

evaluate required checks,

emit errors and warnings,

preserve validation evidence,

produce conformance status,

produce conformance report.

33.3 Validator Failure

A Validator that cannot explain failed requirements is not CEP-Validator conformant.

34. Implementation Conformance

An Implementation may claim CEP conformance only for declared classes, levels, and profiles.

34.1 Implementation Claim Example

Implementation X claims:

CEP-Envelope L3
CEP-Benchmark L2
CEP-Runner L1
CEP-Evidence L0

This is valid if supported by conformance reports.

34.2 Implementation Failure

A system MUST NOT claim general CEP conformance if it only supports one class.

Claims such as “CEP-compatible” SHOULD be treated as incomplete unless class and level are specified.

35. Version Compatibility

CEP conformance is versioned.

A target MUST declare the CEP version it conforms to.

35.1 Version Compatibility Values

compatible
partially_compatible
requires_migration
incompatible
unknown

35.2 Version Failure

If CEP version is absent, conformance status is unknown or invalid.

36. Migration Conformance

A target MAY be migrated from one CEP version to another.

36.1 Migration Record

A migration record SHOULD preserve:

migration_id
source_cep_version
target_cep_version
target_ref
migration_method
changed_fields
loss_notes
validation_result_ref
confidence

36.2 Migration Failure

A migrated target that loses required distinctions without marking loss is non-conformant.

37. Manual Review

Some conformance checks MAY require human review.

Manual review MUST be represented.

37.1 Manual Review Record

A manual review record SHOULD preserve:

review_id
reviewer_ref
target_ref
review_question_ref
review_method
decision
evidence_refs
confidence
limitations
reviewed_at

37.2 Review Failure

Manual review without review question, evidence, and decision basis is weak evidence.

38. Conformance Suite

A Conformance Suite is a collection of tests, fixtures, cases, validators, and expected results used to evaluate conformance.

38.1 Suite Fields

A Conformance Suite SHOULD preserve:

suite_id
suite_version
cep_version
target_classes
test_case_refs
fixture_refs
expected_result_refs
validator_refs
coverage_report
provenance_refs

38.2 Suite Failure

A conformance suite without coverage report and expected results is under-specified.

39. Golden Cases

Golden Cases are canonical cases used to verify conformance behavior.

39.1 Golden Case Fields

A Golden Case SHOULD preserve:

golden_case_id
target_class
input_ref
expected_output_ref
expected_errors
expected_warnings
anti_collapse_conditions
provenance_refs

39.2 Golden Case Failure

A golden case without expected errors, warnings, or output is not useful for conformance validation.

40. Non-Conformance Handling

A CEP implementation MUST preserve non-conformance rather than hide it.

40.1 Non-Conformance Record

A non-conformance record SHOULD preserve:

non_conformance_id
target_ref
requirement_ref
failure_type
severity
detected_at
detected_by
repair_guidance
waiver_status
evidence_refs

40.2 Waiver

A Waiver records that a non-conformance is knowingly accepted under specified scope.

A Waiver MUST preserve:

waiver_id
non_conformance_ref
waiver_reason
approved_by
scope
expires_at
risk_acceptance

40.3 Waiver Failure

A waiver MUST NOT make a non-conformant target conformant.

It only records accepted risk.

41. Repair and Revalidation

A non-conformant target MAY be repaired and revalidated.

41.1 Repair Record

A repair record SHOULD preserve:

repair_id
non_conformance_ref
repair_transformation_ref
changed_entities
validation_result_ref
remaining_issues

41.2 Revalidation Rule

After repair, conformance MUST be revalidated before conformance status is updated.

42. Minimal Valid Conformance Report

A minimally valid CEP Conformance Report MUST preserve:

report_id
target_ref
target_type
cep_version
conformance_class
conformance_level
validation_method
validator_ref
validation_time
requirements_evaluated
passed_requirements
failed_requirements
warnings
errors
conformance_status
evidence_refs
limitations

A Conformance Report lacking target, version, class, level, requirements evaluated, validation method, and status is invalid.

43. Invalid Conformance Conditions

A conformance claim or report is invalid if:

it lacks target,

it lacks CEP version,

it lacks conformance class,

it lacks conformance level,

it lacks validation result,

it lacks evaluated requirements,

it hides failed requirements,

it hides errors or warnings,

it claims L4 without evidence,

it claims general conformance without scope,

it treats compatibility as conformance,

it treats certification as conformance,

it uses a profile that overwrites core CEP semantics,

it omits limitations,

or it cannot identify what was validated.

Invalid conformance claims MUST NOT be used for benchmark scoring, certification, capability claims, authority decisions, or public comparison.

44. Conformance Invariants

CEP-compatible conformance systems SHALL preserve the following invariants.

Invariant 1 — Conformance Is Scoped

Conformance SHALL always declare scope, class, level, profile, and CEP version.

Invariant 2 — Conformance Is Targeted

Conformance SHALL identify what target is being evaluated.

Invariant 3 — Conformance Is Evidence-Backed At L4

L4 conformance SHALL preserve evidence.

Invariant 4 — Compatibility Is Not Conformance

Compatibility SHALL remain distinct from conformance.

Invariant 5 — Certification Is Not Conformance

External certification SHALL remain distinct from protocol conformance.

Invariant 6 — Failed Requirements Are Preserved

Failures SHALL NOT be hidden.

Invariant 7 — Warnings Are Preserved

Warnings SHALL NOT be hidden.

Invariant 8 — Anti-Collapse Rules Are Enforced

Protected CEP distinctions SHALL be validated when relevant.

Invariant 9 — Profiles Do Not Override Core Semantics

Profiles SHALL add requirements without corrupting CEP core.

Invariant 10 — Extensions Are Contained

Extensions SHALL remain namespaced and non-destructive.

Invariant 11 — Version Is Preserved

CEP version SHALL be declared for every conformance claim.

Invariant 12 — Waiver Is Not Conformance

A waived non-conformance SHALL remain a non-conformance.

45. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:

compatibility into conformance
certification into conformance
schema validity into semantic conformance
semantic conformance into operational conformance
operational conformance into evidence-backed conformance
conformance claim into conformance proof
validator output into truth
waiver into conformance
profile into core protocol
extension into core semantics
passing test into complete conformance
benchmark score into conformance
conformance into capability
conformance into authority

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

46. Conformance Labeling

Public conformance labels SHOULD use the following structure:

CEP-{Class} L{Level} / CEP {Version} / Profile {Profile}

Examples:

CEP-Envelope L3 / CEP 0.1 / Core

CEP-Benchmark L2 / CEP 0.1 / RealityGapBench

CEP-Runner L4 / CEP 0.1 / AuthorityBench

CEP-Implementation Mixed / CEP 0.1

A mixed implementation MUST provide class-level details.

47. Conformance and Semantic Envelope

Conformance reports SHOULD be carried as Semantic Envelopes.

A conformance envelope SHOULD include:

envelope_kind: conformance_report
target_ref
target_type
cep_version
conformance_class
conformance_level
profile_refs
requirements_evaluated
passed_requirements
failed_requirements
warnings
errors
evidence_refs
validator_refs
conformance_status
limitations

This makes conformance portable, inspectable, and auditable.

48. Conformance and Benchmarks

A benchmark result MAY depend on conformance.

For example:

a Runner must be CEP-Runner conformant,

a Benchmark must be CEP-Benchmark conformant,

a Result must be CEP-Result conformant,

an Envelope must be CEP-Envelope conformant.

Benchmark reports SHOULD preserve conformance status for all relevant components.

A benchmark result produced by non-conformant components MAY still be stored, but its limitations MUST be disclosed.

49. Conformance and Capability

Conformance does not imply capability.

A system may conform to CEP structures but perform poorly on benchmarks.

A system may perform well on one benchmark without broad capability.

Capability requires repeated settlement under variation.

Conformance only states that the system preserves protocol semantics under declared scope.

50. Conformance and Authority

Conformance does not imply authority.

A conformant system may still be unauthorized to perform a transformation.

Authority must be evaluated separately.

A conformance label MUST NOT be treated as permission.

51. Conformance and Affordance

Conformance may affect affordance but does not itself establish affordance.

A conformant tool may make certain transformations easier to reach.

However, an affordance still requires current state, authority, capability, payment burden, evidence requirements, and settlement requirements.

52. Implementation Consequence

Any implementation claiming CEP conformance MUST produce conformance reports.

Any implementation claiming L4 conformance MUST produce evidence-backed conformance reports.

A system that uses CEP terms but cannot validate its structures, preserve anti-collapse distinctions, report failures, or produce conformance evidence is not CEP-compliant.

This requirement exists because CEP is an evaluation protocol.

An evaluation protocol that cannot evaluate its own implementations cannot protect its own meaning.

53. Closing Definition

CEP Conformance is the scoped, versioned, evidence-backed demonstration that a target preserves the protocol semantics required to evaluate represented transformations through evidence-backed settlement.

Conformance protects CEP from becoming vocabulary without discipline.

It ensures that tools, benchmarks, runners, envelopes, results, profiles, and implementations preserve the distinctions that make CEP useful.

Without Conformance, CEP can be imitated.

With Conformance, CEP can be implemented.

The foundation set is now coherent enough to support the next settlement: create the repository artifact plan — file tree, RFC index, implementation phases, schemas, conformance fixtures, and the first benchmark family spec, starting with RealityGapBench.