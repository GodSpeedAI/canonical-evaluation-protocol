---
type: "CEP Subsystem Guide"
id: "cep-subsystem-schema-validation"
title: "Schema and Validation Subsystem"
description: "Specification and operational guide for the schema profiling, schema value validation, and corpus integrity verification subsystem."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - subsystem
  - schema
  - validation
timestamp: "2026-06-27T00:00:00Z"
---

# Schema and Validation Subsystem

## 1. Purpose
The Schema and Validation Subsystem guarantees structural and semantic contract enforcement across all CEP data artifacts. It validates that JSON schemas conform to an explicitly constrained JSON Schema Draft 2020-12 profile and verifies that all benchmark cases, answer keys, candidate answers, evidence records, conformance fixtures, and semantic envelopes strictly comply with their registered schemas.

---

## 2. Responsibilities and Non-Responsibilities

### Responsibilities
* **Schema Profile Enforcement**: Restricting schema keywords to an auditable, deterministic subset (`SUPPORTED_SCHEMA_KEYS`), rejecting unhandled meta-keywords.
* **Instance Validation**: Validating arbitrary JSON objects against profiled schemas (types, bounds, enum, regex patterns, required keys, `additionalProperties: false`, and `anyOf` branches).
* **Registry Integrity**: Ensuring all schemas registered in `schemas/index.json` exist and validate cleanly.
* **Corpus Structural Invariants**: Validating that every evidence reference in a case's `evidence_requirements` resolves to a real evidence file in `evidence/`, and verifying that `case_ref` in answer keys and answers matches the directory name.

### Non-Responsibilities
* **Anti-Collapse Semantic Inspection**: Does not inspect candidate prose or reasoning for ontological collapses (owned by `cep.detect`).
* **Answer Scoring**: Does not calculate recall or numerical scores (owned by `cep.benchmarks.*`).
* **Persistence**: Does not write or mutate schemas or corpus files at runtime.

---

## 3. Position in the System

```text
[schemas/index.json] ──> [validate_schema_registry()]
                               │
[JSON Schemas (*.schema.json)] ┴──> [schema_profile_errors()] (Profile Verification)
                                            │
[Corpus Files (*.json)] ──────────> [validate_value()] (Instance Verification)
                                            │
                                            ▼
                                   [ValidationResult]
```

* **Called by**: `cep.cli.validate_*`, `cep.cli.doctor`, `tests/test_validation.py`, `tools/validate_okf.py`.
* **Calls**: `cep.io.load_json`, standard Python `re`, `pathlib.Path`.

---

## 4. Core Abstractions

### `SchemaProfile` (`cep.schema_profile: SchemaProfile`)
An immutable dataclass holding the parsed schema `JsonObject` and its directory `root: Path` for resolving relative `$ref` pointers.

### `SUPPORTED_SCHEMA_KEYS` (`cep.schema_profile: SUPPORTED_SCHEMA_KEYS`)
A closed set of permitted JSON Schema keywords:
`$id`, `$ref`, `$schema`, `additionalProperties`, `anyOf`, `const`, `description`, `enum`, `items`, `maximum`, `minimum`, `minItems`, `minLength`, `minProperties`, `pattern`, `properties`, `required`, `title`, `type`.
Any schema containing keywords outside this set fails profile validation.

### `ValidationResult` (`cep.validation: ValidationResult`)
A frozen dataclass representing the verification outcome:
* `ok: bool`: True if zero errors occurred.
* `target: str`: Path or identifier of the checked document.
* `errors: list[str]`: Detailed error messages with dot-separated object locations (e.g., `$.properties.evidence_refs`).

---

## 5. Internal Operation and Validation Logic

### 5.1 Schema Profiling (`schema_profile.py`)
1. Rejects unknown keywords.
2. Asserts root schema specifies `$schema`, `title`, and `type: "object"`.
3. Recursively validates nested definitions under `properties`, `items`, and `anyOf`.
4. Enforces that `required` is an array of non-empty strings and `additionalProperties` is a boolean.

### 5.2 Instance Value Validation (`schema_value.py`)
1. Type checking: `array`, `boolean`, `number`, `object`, `string`, `null`.
2. Constraint checking: `minimum`, `maximum`, `minLength`, `minProperties`, `minItems`, `pattern`, `const`, `enum`.
3. Object recursion: Enforces all `required` keys are present. If `additionalProperties: false`, rejects unexpected keys.
4. Reference resolution: Automatically resolves relative local `$ref` pointers relative to the parent schema's directory.

### 5.3 Corpus Linkage Verification (`validation.py`)
* `_case_evidence_refs(case_file)`: Reads `case_payload["evidence_requirements"]` (`required_evidence_refs` and `optional_evidence_refs`) and asserts that `case_dir / "evidence" / f"{ref}.json"` exists for each reference.
* `_case_ref_matches(path, field_name)`: Confirms that `payload[field_name] == path.parent.name`.

---

## 6. Failure Modes and Diagnostics

| Symptom | Cause | Diagnostic Command | Remedy |
|---|---|---|---|
| `unsupported schema keyword $defs` | Schema uses keywords outside `SUPPORTED_SCHEMA_KEYS`. | `uv run cep validate schemas` | Remove keyword or expand `SUPPORTED_SCHEMA_KEYS` in `schema_profile.py` if justifiable. |
| `missing evidence file: ev-rg-0001-009` | Case references an evidence record not present on disk. | `uv run cep validate reality-gap-corpus` | Add missing file to `benchmarks/<family>/cases/<id>/evidence/` or remove from requirements. |
| `case_ref must be rg-0002` | Answer key or answer file `case_ref` does not match directory. | `uv run cep validate reality-gap-corpus` | Align `case_ref` field with containing directory name. |
| `invalid fixture must fail validation` | An invalid semantic envelope fixture unexpectedly passed schema validation. | `uv run cep validate semantic-envelope` | Ensure negative test fixtures violate a required schema constraint. |

---

## 7. Extension Points

1. **Adding a New Schema**:
   * Create `schemas/<new-schema>.schema.json`.
   * Ensure it only uses `SUPPORTED_SCHEMA_KEYS`.
   * Register its filename in `schemas/index.json`.
   * Verify via `uv run cep validate schemas`.
2. **Adding Custom Corpus Validators**:
   * In `src/cep/validation.py`, compose a new validation function returning `list[ValidationResult]`.
   * Expose the check via `src/cep/cli.py` under the `validate` command group.

---

## 8. Source Trail

* [schema_profile.py](../../src/cep/schema_profile.py) — `SUPPORTED_SCHEMA_KEYS`, `SchemaProfile`, `schema_profile_errors()`
* [schema_value.py](../../src/cep/schema_value.py) — `validate_value()`, `validate_object()`, `_resolve_ref()`
* [validation.py](../../src/cep/validation.py) — `validate_schema_registry()`, `validate_all_schemas()`, `validate_reality_gap_corpus()`
* [schemas/index.json](../../schemas/index.json) — Official registry of schemas
* [tests/test_validation.py](../../tests/test_validation.py) — Schema validation test suite
