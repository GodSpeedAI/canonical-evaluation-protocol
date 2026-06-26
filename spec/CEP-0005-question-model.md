---
type: CEP Specification
id: CEP-0005
title: Question Model
description: This document defines the CEP Question Model.
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
supersedes: []
superseded_by: []
conformance_class: null
benchmark_family: null
schema_ref: null
defines:
- Question
- Question Identity
- Question Scope
- Divergence Question
- Authority Question
- Settlement Question
- Capability Question
used_by:
- CEP-0006
- CEP-0007
- CEP-0008
- CEP-0009
- CEP-0010
related:
- CEP-0004
- CEP-0006
---

# CEP-0005 — Question Model

## Navigation

**Depends on:** [CEP-0000](./CEP-0000-derivation-ladder.md), [CEP-0001](./CEP-0001-ontology.md), and the prior protocol chain through [CEP-0004](./CEP-0004-transformation-model.md)
**Defines:** Question, Question Identity, Question Scope, Divergence Question, Authority Question, [Settlement](./CEP-0007-settlement-model.md) Question, Capability Question
**Used by:** [CEP-0006](./CEP-0006-evidence-model.md), [CEP-0007](./CEP-0007-settlement-model.md), [CEP-0008](./CEP-0008-semantic-envelope.md), [CEP-0009](./CEP-0009-benchmark-model.md), [CEP-0010](./CEP-0010-conformance.md)

## Abstract

This document defines the CEP Question Model.

CEP evaluates represented transformations through evidence-backed settlement. Evaluation is impossible without relevance. Relevance is impossible without a question.

A Question is a constraint over observation, attention, relevance, evidence selection, answer shape, and evaluation.

A Question is not merely a sentence.

A Question is an operational structure that determines which distinctions, relations, states, transformations, observations, claims, evidence, invariants, metrics, and settlements matter.

The Question Model defines how questions are represented, scoped, decomposed, answered, validated, bound to evidence, bound to benchmarks, and used to direct evaluation.

## 1. Purpose

The purpose of the Question Model is to prevent CEP implementations from treating evaluation as context-free scoring.

The same representation may produce different evidence under different questions.

The same transformation may be acceptable under one question and invalid under another.

The same observation may be irrelevant, decisive, misleading, or incomplete depending on the question being asked.

A CEP-compatible implementation MUST preserve the question that makes evaluation meaningful.

Without Question, there is no directed observation.

Without directed observation, there is no evidence.

Without evidence, there is no settlement.

Without settlement, there is no CEP-compliant evaluation.

## 2. Scope

This document defines:
- question definition
- question sufficiency
- question scope
- question identity
- question types
- question decomposition
- question composition
- question lifecycle
- question relevance rules
- question answer shapes
- question-evidence binding
- question-benchmark binding
- question validity
- question operations
- conformance requirements
- anti-collapse rules

This document does not define:
- complete benchmark scoring algorithms
- final benchmark language syntax
- evidence weighting
- settlement thresholds
- runner implementation
- [Semantic Envelope](./CEP-0008-semantic-envelope.md) serialization

Those are defined in later CEP specifications.

## 3. Core Definition

A Question is a constraint over observation, attention, relevance, and answer shape.

A Question determines what the evaluation is trying to find, distinguish, compare, prove, disprove, classify, explain, predict, settle, or make reachable.

A Question MUST preserve enough structure to answer:

- What is being asked?
- Why is this question relevant?
- Which entities are in scope?
- Which states or transformations are targeted?
- Which distinctions matter?
- Which relations matter?
- Which observations may become evidence?
- Which evidence types are admissible?
- What answer shape is expected?

What would count as sufficient, insufficient, contradictory, or irrelevant evidence?

What would falsify or weaken the answer?

What settlement or state update could follow from answering the question?

## 4. Question Is Not Prompt

CEP SHALL distinguish Question from Prompt.

### 4.1 Prompt

A Prompt is an instruction or input given to a human, model, agent, tool, or system.

A Prompt may contain a Question.

A Prompt may obscure a Question.

A Prompt may contain multiple Questions.

A Prompt may contain no evaluable Question.

### 4.2 Question

A Question is the evaluative structure that determines relevance and answer shape.

- Example:
- Prompt:

"Look at these logs and tell me what happened."

Possible CEP Question:
"Where does observed execution diverge from the declared deployment policy?"

### 4.3 Anti-Collapse Rule

A CEP implementation MUST NOT treat arbitrary natural language input as a valid Question unless the evaluative target, scope, relevance rules, and expected answer shape are explicit or derivable.

## 5. Question Sufficiency

A Question is sufficient when it preserves enough information to direct observation, evidence selection, and answer validation.

### 5.1 Required Question Fields

A CEP-compatible Question MUST preserve:
- question_id
- question_form
- question_type
- scope
- target_entities
- target_states
- target_transformations
- relevance_rules
- expected_answer_shape
- evaluation_context

### 5.2 Conditional Question Fields

A Question SHOULD preserve the following when materially relevant:

- perspective_refs
- authority_context
- evidence_requirements
- admissible_evidence_types
- inadmissible_evidence_types
- confidence_requirements
- settlement_requirements
- metric_refs
- benchmark_refs
- parent_question_ref
- subquestion_refs
- assumptions
- limitations
- unknowns

### 5.3 Question-Sufficiency Failure

A Question is not CEP-valid if it does not constrain relevance.

A Question is not benchmark-valid if it does not define or imply expected answer shape.

A Question is not evidence-valid if it does not define what kinds of observations could bear on the answer.

A Question is not settlement-valid if it cannot specify what evidence state would be sufficient for consequence registration.

## 6. Question Identity

A Question MUST have identity.

Question identity allows CEP to distinguish:
- original question from refined question
- parent question from subquestion
- benchmark question from case question
- diagnostic question from evidence question
- strategy question from implementation question

### 6.1 Question Identity Record

A Question identity record SHOULD preserve:
- question_id
- version
- lineage_refs
- parent_question_ref
- subquestion_refs
- supersedes
- superseded_by
- semantic_equivalence_claims
- created_at
- updated_at
- created_by

### 6.2 Question Equivalence

Two Questions MAY be considered equivalent only under declared criteria.

Possible equivalence types include:
- semantic_equivalent
- answer_shape_equivalent
- benchmark_equivalent
- evidence_equivalent
- scope_equivalent
- operationally_equivalent

Question equivalence MUST NOT be assumed from similar wording.

### 6.3 Identity Failure

If Question identity is absent, CEP cannot determine whether an answer, benchmark result, evidence packet, or settlement corresponds to the question actually being evaluated.

## 7. Question Scope

A Question MUST preserve scope.

Scope defines where the question applies and where it does not.

### 7.1 Scope Record

A Question scope record SHOULD preserve:
- domain
- organization_or_system
- team
- process
- artifact
- actor_group
- environment
- time_range
- jurisdiction
- benchmark_family
- evaluation_context
- limitations

### 7.2 Scope Discipline

A Question MUST NOT be applied outside its scope without explicit projection or reformulation.

Example:

A question about whether an agent was authorized to modify a local test file is not automatically equivalent to a question about whether the agent was authorized to modify production infrastructure.

### 7.3 Scope Failure

If Question scope is omitted, CEP may overgeneralize answers, evidence, and benchmark scores.

This creates false capability, false authority, false settlement, and false affordance claims.

## 8. Question Perspective

A Question MAY depend on Perspective.

Perspective determines which distinctions and relations are visible, relevant, or meaningful.

### 8.1 Perspective Examples

A single transformation may generate different Questions from different perspectives:

- Operator:
- "Did the workflow complete?"
- Auditor:

"Was the workflow performed by a certified actor?"

- Security:
- "Did the workflow violate access policy?"
- Customer:

"Did the outcome meet the promised service condition?"

[Benchmark](./CEP-0009-benchmark-model.md):
"Did the system preserve the declared/observed distinction and cite evidence?"

### 8.2 Perspective Requirement

A Question MUST preserve Perspective when interpretation depends on who or what is asking.

### 8.3 Perspective Failure

If Perspective is omitted, CEP cannot determine why the same State or [Transformation](./CEP-0004-transformation-model.md) is relevant under one evaluation and irrelevant under another.

## 9. Question Types

CEP recognizes the following top-level Question types.

- divergence
- authority
- settlement
- capability
- affordance
- evidence
- causal
- diagnostic
- comparative
- predictive
- conformance
- classification
- generative
- risk
- repair
- strategy
- unknown

Implementations MAY define domain-specific subtypes.

Domain-specific subtypes MUST map to one or more CEP top-level Question types.

## 10. Divergence Question

### 10.1 Definition

A Divergence Question asks where two or more States, Representations, Claims, Transformations, or Perspectives differ.

### 10.2 Canonical Form

Where does X diverge from Y under scope S and question context Q?

### 10.3 Examples

Where does declared reality diverge from observed reality?
Where does expected behavior differ from actual behavior?
Where does claimed completion differ from evidenced consequence?
Where does written policy diverge from operational practice?

### 10.4 Required Answer Shape

A Divergence answer SHOULD include:
- divergence_detected
- divergence_type
- source_entity_ref
- target_entity_ref
- affected_distinctions
- affected_relations
- severity
- evidence_refs
- confidence
- recommended_next_question_or_action

## 11. Authority Question

### 11.1 Definition

An Authority Question asks whether a [Transformation](./CEP-0004-transformation-model.md) is permissible under applicable authority constraints.

### 11.2 Canonical Form

Is actor A permitted to perform transformation T on subject S under authority context C?

### 11.3 Required Answer Shape

An Authority answer MUST return one of:

- allow
- deny
- escalate
- unknown
The answer SHOULD include:
- applicable_authority_refs
- policy_or_rule_refs
- constraint_refs
- evidence_refs
- reasoning_summary
- confidence
- limitations

### 11.4 Failure Mode

If an Authority Question returns only “can/cannot” rather than “may/may not,” it has collapsed capability into authority and is invalid.

## 12. Settlement Question

### 12.1 Definition

A Settlement Question asks whether a [Transformation](./CEP-0004-transformation-model.md) has produced sufficiently registered consequences to update State.

### 12.2 Canonical Form

Has transformation T settled sufficiently for evaluation context C?

### 12.3 Required Answer Shape

A [Settlement](./CEP-0007-settlement-model.md) answer SHOULD include:
- settlement_status
- completion_claim_ref
- observed_consequence_refs
- evidence_refs
- unresolved_contradictions
- missing_evidence
- confidence
- state_update_recommendation
- limitations

### 12.4 Failure Mode

If a Settlement Question treats completion claim as settlement evidence by itself, it is invalid.

## 13. Capability Question

### 13.1 Definition

A Capability Question asks whether repeated settled transformations under variation reduced future payment burden.

### 13.2 Canonical Form

Did repeated settlement of transformation family F under variation V reduce future payment burden and expand reachable affordances?

### 13.3 Required Answer Shape

A Capability answer SHOULD include:
- capability_claim
- transformation_chain_refs
- settlement_history_refs
- variation_context
- payment_burden_before
- payment_burden_after
- affordance_delta_refs
- evidence_refs
- confidence
- decay_or_refresh_conditions

### 13.4 Failure Mode

If a Capability Question can be answered from a single successful task, it is invalid.

Capability requires repeated settlement under variation.

## 14. Affordance Question

### 14.1 Definition

An Affordance Question asks which transformations are reachable from a current [State](./CEP-0003-state-model.md) under constraints, authority, capability, payment burden, evidence, and settlement requirements.

### 14.2 Canonical Form

Which transformations are reachable, payable, permissible, executable, and settleable from current state S?

### 14.3 Required Answer Shape

An Affordance answer SHOULD include:
- candidate_transformation_refs
- reachability_status
- payment_burden
- authority_status
- capability_requirements
- evidence_requirements
- settlement_requirements
- blocking_constraints
- confidence
- next_affordable_transformation

### 14.4 Failure Mode

If an Affordance Question returns abstract possibilities without reachable paths, it is invalid.

A destination without a spendable path is not an affordance.

## 15. Evidence Question

### 15.1 Definition

An [Evidence](./CEP-0006-evidence-model.md) Question asks what observations, records, traces, artifacts, or attestations support, weaken, contradict, qualify, or fail to affect a Claim.

### 15.2 Canonical Form

What evidence bears on claim C under question Q?

### 15.3 Required Answer Shape

An Evidence answer SHOULD include:
- claim_ref
- supporting_evidence_refs
- contradicting_evidence_refs
- qualifying_evidence_refs
- irrelevant_observations
- missing_evidence
- reliability_assessment
- confidence_impact
- limitations

### 15.4 Failure Mode

If an Evidence Question treats data as evidence without relation to a Claim, it is invalid.

## 16. Causal Question

### 16.1 Definition

A Causal Question asks whether one [Transformation](./CEP-0004-transformation-model.md), State, Constraint, Relation, or Observation contributed to another.

CEP does not require a universal causality model in this document.

However, causal Questions MUST preserve causal assumptions.

### 16.2 Required Answer Shape

A Causal answer SHOULD include:
- candidate_cause_refs
- effect_refs
- causal_relation_type
- supporting_evidence_refs
- alternative_explanations
- confidence
- limitations

### 16.3 Failure Mode

If a Causal Question treats sequence as causation without evidence or assumptions, it is invalid.

## 17. Diagnostic Question

### 17.1 Definition

A Diagnostic Question asks what explains a failure, divergence, contradiction, blockage, uncertainty, or unsettled condition.

### 17.2 Required Answer Shape

A Diagnostic answer SHOULD include:
- diagnosed_condition_ref
- candidate_explanations
- evidence_refs
- excluded_explanations
- confidence
- recommended_next_question
- recommended_next_transformation

### 17.3 Failure Mode

If a Diagnostic Question produces explanation without falsification path, it is weak or invalid depending on context.

## 18. Comparative Question

### 18.1 Definition

A Comparative Question asks how two or more entities, states, transformations, representations, capabilities, affordances, or benchmark results differ.

### 18.2 Required Answer Shape

A Comparative answer SHOULD include:
- compared_entity_refs
- comparison_basis
- preserved_distinctions
- detected_differences
- detected_similarities
- evidence_refs
- confidence
- limitations

### 18.3 Failure Mode

If comparison basis is omitted, the comparison is invalid.

## 19. Predictive Question

### 19.1 Definition

A Predictive Question asks what State, [Transformation](./CEP-0004-transformation-model.md), Evidence condition, Settlement status, Capability change, or Affordance change is expected in the future.

### 19.2 Required Answer Shape

A Predictive answer SHOULD include:
- projected_state_or_transformation_refs
- prediction_method
- assumptions
- time_horizon
- confidence
- evidence_refs
- falsification_conditions
- limitations

### 19.3 Failure Mode

If a Predictive Question treats projection as observation or settlement, it is invalid.

## 20. Conformance Question

### 20.1 Definition

A [Conformance](./CEP-0010-conformance.md) Question asks whether an entity, representation, state, transformation, benchmark, runner, result, or envelope satisfies CEP requirements.

### 20.2 Required Answer Shape

A Conformance answer SHOULD include:
- evaluated_entity_ref
- applicable_spec_refs
- passed_requirements
- failed_requirements
- warnings
- errors
- evidence_refs
- conformance_status

### 20.3 Conformance Status

Conformance status SHOULD be one of:
- conformant
- non_conformant
- partially_conformant
- not_evaluable
- unknown

## 21. Classification Question

### 21.1 Definition

A Classification Question asks which category an entity, state, transformation, gap, evidence record, settlement condition, or benchmark result belongs to.

### 21.2 Required Answer Shape

A Classification answer SHOULD include:
- classified_entity_ref
- assigned_class
- candidate_classes
- classification_basis
- evidence_refs
- confidence
- limitations

### 21.3 Failure Mode

If classification lacks candidate classes or basis, it is not CEP-valid.

## 22. Generative Question

### 22.1 Definition

A Generative Question asks what representation, benchmark case, scenario, transformation, question, or artifact should be produced.

### 22.2 Required Answer Shape

A Generative answer SHOULD include:
- generated_entity_ref
- generation_question_ref
- source_refs
- constraints_used
- omissions
- assumptions
- validation_requirements
- confidence

### 22.3 Failure Mode

If a generated artifact is treated as verified evidence without validation, it is invalid.

## 23. Risk Question

### 23.1 Definition

A Risk Question asks which transformations may produce harmful, unauthorized, unsettled, costly, irreversible, or capability-reducing consequences.

### 23.2 Required Answer Shape

A Risk answer SHOULD include:
- risk_condition_refs
- candidate_transformations
- harmful_consequence_refs
- likelihood_assessment
- severity_assessment
- evidence_refs
- blocking_constraints
- mitigation_transformations
- confidence

### 23.3 Failure Mode

If Risk is treated as fear, preference, or vague concern rather than a represented consequence pattern, it is not CEP-valid.

## 24. Repair Question

### 24.1 Definition

A Repair Question asks what transformation would reduce contradiction, resolve drift, restore authority, improve evidence, update state, or settle an unsettled condition.

### 24.2 Required Answer Shape

A Repair answer SHOULD include:
- condition_to_repair_ref
- candidate_repair_transformations
- required_authority
- required_evidence
- payment_burden
- expected_settlement_condition
- risks
- confidence

### 24.3 Failure Mode

If a Repair Question proposes a destination without a reachable transformation path, it fails affordance discipline.

## 25. Strategy Question

### 25.1 Definition

A Strategy Question asks which transformation should be pursued to expand the future affordance horizon under current constraints.

### 25.2 Required Answer Shape

A Strategy answer SHOULD include:
- current_state_ref
- desired_direction
- candidate_transformations
- affordance_delta_estimate
- payment_burden
- authority_requirements
- evidence_requirements
- settlement_target
- feedback_signal
- first_affordable_move
- confidence

### 25.3 Failure Mode

If a Strategy Question produces a destination without a spendable next transformation, it is invalid as a CEP strategy answer.

## 26. Question Relevance Rules

A Question MUST define or imply relevance rules.

Relevance rules determine which entities, observations, evidence records, distinctions, and transformations bear on the answer.

### 26.1 Relevance Rule Record

A relevance rule SHOULD preserve:
- relevance_rule_id
- question_ref
- target_entity_types
- included_relations
- excluded_relations
- required_distinctions
- admissible_evidence_types
- inadmissible_evidence_types
- scope_limits
- time_limits
- confidence_requirements

### 26.2 Relevance Failure

If relevance rules are absent, CEP cannot distinguish signal from noise.

A system may cite irrelevant evidence, ignore decisive evidence, or answer a different question.

## 27. Expected Answer Shape

A Question MUST define or imply an expected answer shape.

Answer shape is the structure a valid answer must satisfy.

### 27.1 Answer Shape Record

An expected answer shape SHOULD preserve:
- answer_shape_id
- question_ref
- required_fields
- optional_fields
- allowed_values
- confidence_required
- evidence_required
- explanation_required
- invalid_answer_conditions

### 27.2 Answer Shape Examples

Authority Question:

decision: allow | deny | escalate | unknown
- evidence_refs: required
- authority_refs: required
- confidence: required
Reality Gap Question:
- gap_detected: true | false | unknown
- gap_type: required if gap_detected=true
- severity: required if gap_detected=true
- evidence_refs: required
- [Settlement](./CEP-0007-settlement-model.md) Question:

settlement_status: unsettled | partially_settled | settled | failed | unknown
- missing_evidence: required if unsettled
- state_update_recommendation: required

### 27.3 Answer Shape Failure

If expected answer shape is absent, scoring becomes arbitrary.

A benchmark without answer shape is not CEP-valid.

## 28. Question Assumptions

Questions often depend on assumptions.

CEP-compatible Questions SHOULD preserve assumptions when material.

### 28.1 Assumption Record

An assumption record SHOULD preserve:
- assumption_id
- question_ref
- description
- assumption_type
- source
- confidence
- risk_if_false
- evidence_refs

### 28.2 Assumption Types

- CEP recognizes:
- scope_assumption
- identity_assumption
- authority_assumption
- semantic_assumption
- temporal_assumption
- evidence_assumption
- capability_assumption
- settlement_assumption
- causal_assumption

### 28.3 Assumption Failure

If assumptions are hidden, systems may produce confident answers under false context.

Hidden assumptions corrupt benchmark validity and settlement.

## 29. Question Unknowns

A Question MAY contain unknowns.

Unknowns MUST be marked when they materially affect answer validity.

### 29.1 Unknown Record

A question unknown record SHOULD preserve:
- unknown_id
- question_ref
- unknown_type
- description
- impact
- resolution_requirement

### 29.2 Unknown Types

- CEP recognizes:
- scope_unknown
- identity_unknown
- authority_unknown
- evidence_unknown
- temporal_unknown
- semantic_unknown
- settlement_unknown
- capability_unknown
- affordance_unknown

### 29.3 Unknown Failure

If unknowns are hidden, CEP may answer questions that are not answerable under the available representation.

## 30. Question Decomposition

A complex Question MAY be decomposed into subquestions.

### 30.1 Decomposition Requirement

Question decomposition SHOULD preserve:
- parent_question_ref
- subquestion_refs
- decomposition_basis
- dependency_order
- answer_composition_rule

### 30.2 Example

- Parent Question:
- Has this agentic workflow settled safely?
- Possible subquestions:
- Was the workflow authorized?
- Did the expected transformation occur?
- What consequences were observed?
- What evidence supports the consequence claim?
- Were any invariants violated?
- Are contradictions unresolved?
- Can state be updated?

### 30.3 Decomposition Failure

If decomposition is implicit, systems may skip necessary subquestions and overclaim settlement.

## 31. Question Composition

Multiple Questions MAY be composed into a higher-level Question.

### 31.1 Composition Requirement

Question composition SHOULD preserve:
- composed_question_id
- component_question_refs
- composition_rule
- conflict_resolution_rule
- required_answer_dependencies

### 31.2 Composition Failure

If composition rules are absent, answers to component Questions may be combined incorrectly.

For example, “authorized” plus “completed” does not automatically imply “settled.”

## 32. Question Refinement

A Question MAY be refined when it is too broad, ambiguous, underspecified, or unanswerable.

### 32.1 Refinement Record

A refinement record SHOULD preserve:
- original_question_ref
- refined_question_ref
- refinement_reason
- preserved_intent
- changed_scope
- changed_answer_shape
- changed_evidence_requirements

### 32.2 Refinement Failure

If refinement lineage is absent, systems may answer a different Question without preserving that the Question changed.

## 33. Question Projection

A Question MAY be projected into a different scope, benchmark family, domain, or abstraction level.

Projection MUST preserve changed assumptions and scope limits.

### 33.1 Projection Examples

- From:
- "Was this deployment authorized?"
- To:
- "Was this agentic file modification authorized?"
- From:

"Where did the SOP diverge from actual work?"

To:
"Where did declared organizational state diverge from observed transformation history?"

### 33.2 Projection Failure

If projection is unmarked, CEP may treat analogies as equivalences.

## 34. Question Lifecycle

A Question MAY pass through lifecycle states.

- draft
- proposed
- accepted
- operationalized
- decomposed
- answered
- partially_answered
- unanswerable
- superseded
- deprecated
- settlement_relevant
- archived
- unknown

Lifecycle state MUST NOT be confused with truth or importance.

A proposed Question may be powerful.

An accepted Question may later become obsolete.

An answered Question may remain unsettled if evidence is insufficient.

## 35. Question and Observation

Question constrains [Observation](./CEP-0001-ontology.md).

A CEP-compatible system MUST preserve how a Question directs what is observed or selected.

### 35.1 Observation Binding

A Question-to-Observation binding SHOULD preserve:
- question_ref
- observation_refs
- selection_basis
- excluded_observations
- limitations
- confidence

### 35.2 Observation Failure

If Question and Observation are not bound, CEP cannot determine whether observations were collected because they were relevant, convenient, biased, or accidental.

## 36. Question and Evidence

[Evidence](./CEP-0006-evidence-model.md) exists only relative to a Claim and Question.

A CEP-compatible Evidence record MUST preserve the Question that makes it evidential when materially relevant.

### 36.1 Evidence Binding

A Question-to-Evidence binding SHOULD preserve:
- question_ref
- claim_ref
- evidence_ref
- relevance
- reliability
- direction
- confidence_impact
- limitations

### 36.2 Evidence Failure

If evidence is detached from Question, CEP cannot determine whether the evidence actually bears on the answer.

## 37. Question and Claim

A Question often generates or targets Claims.

### 37.1 Claim Binding

A Question-to-Claim binding SHOULD preserve:
- question_ref
- claim_refs
- claim_role
- answer_status
- evidence_status

### 37.2 Claim Roles

Claim roles MAY include:
- candidate_answer
- partial_answer
- final_answer
- hypothesis
- counterclaim
- assumption
- invariant_claim
- settlement_claim
- authority_claim
- capability_claim
- affordance_claim

### 37.3 Claim Failure

If Claims are not tied to Questions, CEP cannot distinguish answer from unsupported assertion.

## 38. Question and Metric

A Metric evaluates an answer relative to a Question.

Metrics MUST NOT be detached from Questions.

### 38.1 Metric Binding

A Question-to-Metric binding SHOULD preserve:
- question_ref
- metric_refs
- scoring_target
- answer_shape_ref
- evidence_requirements
- failure_conditions

### 38.2 Metric Failure

If Metric is detached from Question, scoring becomes contextless.

A score is meaningless unless the Question being scored is preserved.

## 39. Question and Benchmark

A [Benchmark](./CEP-0009-benchmark-model.md) is a structured evaluation under one or more Questions.

A CEP-compatible Benchmark MUST preserve its primary Question.

### 39.1 Benchmark Question Record

A Benchmark Question record SHOULD preserve:
- benchmark_ref
- primary_question_ref
- case_question_refs
- metric_question_refs
- evidence_question_refs
- settlement_question_refs

### 39.2 Benchmark Failure

A Benchmark without a primary Question is not CEP-valid.

A benchmark case without a case Question is not case-valid unless the case Question is inherited unambiguously from the benchmark.

## 40. Question and Settlement

[Settlement](./CEP-0007-settlement-model.md) answers a Question about consequence registration.

A transformation may settle under one Question but remain unsettled under another.

### 40.1 Example

A code change may be settled under:

- "Did the tests pass?"
but unsettled under:
- "Did the change reduce production risk?"

### 40.2 Settlement Binding

A Question-to-Settlement binding SHOULD preserve:
- question_ref
- transformation_ref
- settlement_ref
- settlement_threshold_ref
- evidence_refs
- unresolved_contradictions
- confidence

### 40.3 Settlement Failure

If settlement is not question-bound, systems may overgeneralize settlement.

A transformation settled for one evaluation context is not automatically settled for all contexts.

## 41. Question and Affordance

Affordance depends on the Question being asked.

Different Questions expose different reachable transformations.

### 41.1 Example

Question:

"How do we ship this feature fastest?"

may expose one set of affordances.

Question:

"How do we ship this feature without increasing authority exposure?"

may expose a different set.

### 41.2 Affordance Binding

A Question-to-Affordance binding SHOULD preserve:
- question_ref
- current_state_ref
- candidate_transformation_refs
- reachability_rules
- payment_burden
- authority_context
- settlement_requirements

### 41.3 Affordance Failure

If affordances are not question-bound, systems may propose transformations that are reachable for the wrong objective.

## 42. Minimal Valid Question

A minimally valid CEP Question MUST preserve:

- question_id
- question_form
- question_type
- scope
- target_entities OR target_states OR target_transformations
- relevance_rules OR relevance_basis
- expected_answer_shape
- evaluation_context
A benchmark-valid Question MUST additionally preserve:
- metric_refs OR scoring_relevance
- evidence_requirements
- invalid_answer_conditions
A settlement-valid Question MUST additionally preserve:
- settlement_requirements
- confidence_requirements
- state_update_implications

## 43. Invalid Question Conditions

A Question is invalid for CEP evaluation if:

- it lacks scope
- it lacks target entities, states, or transformations
- it lacks relevance rules or relevance basis
- it lacks expected answer shape
- it collapses prompt into question
- it collapses answer into evidence
- it treats possibility as affordance
- it treats completion as settlement
- it treats capability as isolated success
- it treats authority as capability
- it hides material assumptions
- it hides material unknowns
- it lacks evidence requirements when evidence is required
- it cannot determine what would make an answer invalid

Invalid Questions MAY still be stored.

Invalid Questions MUST NOT be used for benchmark scoring, settlement, capability claim, authority decision, or affordance evaluation unless the invalidity itself is the object of evaluation.

## 44. Question Invariants

CEP-compatible systems SHALL preserve the following Question invariants.

**Invariant 1 — Question Directs Relevance**

A Question SHALL determine which observations, evidence, and distinctions matter.

**Invariant 2 — Question Is Not Prompt**

A Question SHALL remain distinct from the prompt or instruction that expresses it.

**Invariant 3 — Question Is Not Answer**

A Question SHALL remain distinct from candidate answers, final answers, claims, and conclusions.

**Invariant 4 — Question Requires Scope**

A Question SHALL preserve scope.

**Invariant 5 — Question Requires Answer Shape**

A Question SHALL define or imply valid answer shape.

**Invariant 6 — Question Binds Evidence**

[Evidence](./CEP-0006-evidence-model.md) SHALL be interpreted relative to a Question and Claim.

**Invariant 7 — Question Binds Metrics**

Metrics SHALL be interpreted relative to a Question.

**Invariant 8 — Question Binds Settlement**

[Settlement](./CEP-0007-settlement-model.md) SHALL be interpreted relative to a Question.

**Invariant 9 — Question Preserves Unknowns**

Material unknowns SHALL be marked.

**Invariant 10 — Question Preserves Assumptions**

Material assumptions SHALL be marked.

## 45. Anti-Collapse Rules

CEP implementations SHALL NOT collapse:
- question into prompt
- question into query
- question into metric
- question into answer
- question into claim
- question into evidence
- question into objective without answer shape
- question into topic
- question into keyword
- question into task
- question into benchmark name
- answer into settlement
- evidence into answer
- observation into evidence without question
- possibility into affordance
- completion into settlement
- authority into capability
- strategy into destination

Violation of these anti-collapse rules SHOULD produce validation warnings or errors depending on evaluation context.

## 46. Question Conformance

A CEP-compatible Question implementation MUST:
- preserve Question identity
- preserve Question scope
- preserve Question type
- preserve target entities, States, or Transformations
- preserve relevance rules or relevance basis
- preserve expected answer shape
- preserve evaluation context
- preserve assumptions when material
- preserve unknowns when material
- support Question decomposition
- support Question refinement lineage
- bind Questions to Observations when relevant
- bind Questions to Claims when relevant
- bind Questions to [Evidence](./CEP-0006-evidence-model.md) when relevant
- bind Questions to Metrics when relevant
- bind Questions to Benchmarks when relevant
- bind Questions to [Settlement](./CEP-0007-settlement-model.md) when relevant
- reject or warn on anti-collapse violations

## 47. Implementation Consequence

A CEP-compatible system that evaluates transformations MUST implement the Question Model.

A system that only evaluates outputs against hidden objectives is not CEP-compliant.

A system that scores benchmark cases without preserving the Question being asked is not CEP-compliant.

A system that collects evidence without preserving the Question that makes the evidence relevant is not CEP-compliant.

This requirement exists because CEP evaluation is question-directed.

Without Questions, there is no principled relevance.

Without relevance, there is no evidence.

Without evidence, there is no settlement.

Without settlement, there is no CEP-compliant evaluation.

## 48. Closing Definition

A Question is a constraint over observation, attention, relevance, evidence selection, answer shape, and evaluation.

CEP Questions make represented transformations evaluable.

They determine what matters, what counts, what would answer, what would falsify, what evidence is admissible, and what settlement could update future action.

Therefore, every CEP benchmark, metric, evidence record, settlement decision, capability claim, and affordance evaluation MUST preserve the Question that makes it meaningful.

The next document should be CEP-0006 — [Evidence Model](./CEP-0006-evidence-model.md). That will define the line between data, observation, evidence, claim support, contradiction, reliability, relevance, and confidence update.