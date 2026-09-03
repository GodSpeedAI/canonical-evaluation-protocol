---
type: "CEP Technical Reference"
id: "cep-reference-schemas"
title: "JSON Schema and Document Format Reference"
description: "Precise technical reference for registered CEP JSON schemas, document models, and semantic envelopes."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - reference
  - schemas
  - specifications
timestamp: "2026-06-27T00:00:00Z"
---

# JSON Schema and Document Format Reference

This reference documents the official JSON schemas registered in `schemas/index.json`. All schemas conform to JSON Schema Draft 2020-12 and the CEP schema profile (`cep.schema_profile`).

---

## Registered Schema Index

| Schema File | Schema Title | Purpose |
|---|---|---|
| `reality-gap-case.schema.json` | RealityGapBench Case | Validates `case.cep.json` files defining reality gap scenarios. |
| `reality-gap-answer-key.schema.json` | RealityGapBench Answer Key | Validates `answer_key.json` files defining accepted answers and recall sets. |
| `reality-gap-answer.schema.json` | RealityGapBench Answer | Validates candidate answer files (`example_*_answer.json`). |
| `reality-gap-evidence.schema.json` | RealityGapBench Evidence | Validates grounding records under `evidence/ev-*.json`. |
| `anti-collapse-manifest.schema.json` | Anti-Collapse Manifest | Validates `conformance/fixtures/anti-collapse/reality-gap/manifest.json`. |
| `anti-collapse-fixture.schema.json` | Anti-Collapse Fixture | Validates individual negative fixtures (`rg-ac-*.json`). |
| `benchmark-result.schema.json` | Benchmark Result | Validates output score reports written to `reports/`. |
| `conformance-report.schema.json` | Conformance Report | Validates aggregate conformance execution records. |
| `semantic-envelope.schema.json` | Semantic Envelope (Draft) | Validates legacy transport envelope payloads. |
| `cep-semantic-envelope.schema.json` | CEP Semantic Envelope (Full) | Validates normative CEP-0008 transformation envelopes. |

---

## 1. RealityGap Case (`reality-gap-case.schema.json`)

* **Target File**: `benchmarks/reality-gap/cases/<case_id>/case.cep.json`
* **Required Properties**:
  * `case_id` (`string`): Pattern `^rg-[0-9]{4}$`.
  * `title` (`string`): Non-empty summary title.
  * `evaluation_scope` (`object`): Boundaries of the evaluation.
  * `declared_state` (`object`): References and assertions of declared policy.
  * `observed_state` (`object`): Telemetry traces and observation refs.
  * `evidence_requirements` (`object`): Contains `required_evidence_refs` and `optional_evidence_refs`.
  * `primary_question` (`string`): The operational probe being tested.
* **Constraints**: `additionalProperties: false`.

---

## 2. RealityGap Answer Key (`reality-gap-answer-key.schema.json`)

* **Target File**: `benchmarks/reality-gap/cases/<case_id>/answer_key.json`
* **Required Properties**:
  * `case_ref` (`string`): Must match containing directory name.
  * `accepted_gap_statuses` (`array[string]`): Permitted statuses (`gap_detected`, `no_gap_detected`, etc.).
  * `accepted_gap_types` (`array[string]`): Expected gap types.
  * `accepted_severity_range` (`array[string]`): Expected severity levels (`critical`, `high`, `medium`, `low`).
  * `required_evidence_refs` (`array[string]`): IDs that must be cited for full evidence recall.
  * `required_affected_constraints` (`array[string]`): Constraints that must be cited.
  * `required_affected_distinctions` (`array[string]`): Distinctions that must be preserved.
  * `required_affected_relations` (`array[string]`): Relations that must be cited.
  * `accepted_next_actions` (`array[string]`): Accepted action types.
  * `partial_credit_rules` (`object`): Award point values per status/type/severity.

---

## 3. RealityGap Answer (`reality-gap-answer.schema.json`)

* **Target File**: Candidate answer JSON (`example_*_answer.json` or external submission)
* **Required Properties**:
  * `answer_id` (`string`): Unique identifier for this candidate answer.
  * `case_ref` (`string`): Case being answered.
  * `gap_status` (`string`): Asserted gap status.
  * `gap_type` (`string`): Asserted gap type.
  * `severity` (`string`): Asserted severity.
  * `gap_summary` (`string`): Natural language rationale. Must reference declared and observed states.
  * `affected_constraints` (`array[string]`): Cited constraint identifiers.
  * `affected_distinctions` (`array[string]`): Preserved distinctions.
  * `affected_relations` (`array[string]`): Cited relation identifiers.
  * `evidence_refs` (`array[string]`): Cited evidence record stems.
  * `confidence` (`object`): Contains `value` (`low`, `medium`, `high`) and `basis` (`string`).
  * `recommended_next_action` (`object`): Contains `type` and `description`.
  * `limitations` (`array[string]`): Stated epistemic limitations.

---

## 4. Benchmark Result (`benchmark-result.schema.json`)

* **Target File**: Generated reports under `reports/<family>/<case_id>-<answer_id>.result.json`
* **Required Properties**:
  * `result_id` (`string`): Unique result identifier.
  * `case_id` (`string`): Case evaluated.
  * `answer_id` (`string`): Answer evaluated.
  * `benchmark_family` (`string`): Name of benchmark suite.
  * `score` (`number`): Floating point score $\in [0.0, 100.0]$.
  * `status` (`string`): Enum: `"pass"`, `"partial"`, `"fail"`, `"invalid"`, `"blocked"`.
  * `metrics` (`object`):
    * `raw_score` (`number`): Score before failure caps.
    * `evidence_recall` (`number`): $\in [0.0, 1.0]$.
    * `constraint_recall` (`number`): $\in [0.0, 1.0]$.
    * `distinction_recall` (`number`): $\in [0.0, 1.0]$.
    * `relation_recall` (`number`): $\in [0.0, 1.0]$.
  * `critical_failures` (`array[string]`): Collapse codes that capped the score.
  * `warnings` (`array[string]`): Non-fatal notices (e.g., `ungrounded_reasoning`).
  * `generated_at` (`string`): ISO 8601 UTC timestamp.

---

## 5. Anti-Collapse External Corpus (`cep/anti-collapse-corpus@1`)

* **Schema Identifier**: `"cep/anti-collapse-corpus@1"`
* **Structure**:
  ```json
  {
    "$schema": "cep/anti-collapse-corpus@1",
    "corpus_id": "string",
    "records": [
      {
        "record_id": "string",
        "record_ref": "string (optional)",
        "accepted_gap_statuses": ["string"],
        "valid_evidence_ids": ["string"],
        "submitted_answer": { "...answer properties..." }
      }
    ]
  }
  ```
