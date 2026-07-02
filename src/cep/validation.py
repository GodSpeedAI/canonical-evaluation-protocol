from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from cep.inventory import (
    iter_reality_gap_answer_keys,
    iter_reality_gap_anti_collapse_fixtures,
    iter_reality_gap_case_files,
    iter_reality_gap_evidence_files,
    iter_reality_gap_example_answers,
    iter_semantic_envelope_fixtures,
    reality_gap_anti_collapse_manifest,
)
from cep.io import load_json
from cep.json_types import JsonDocumentError, JsonObject
from cep.paths import SCHEMAS_DIR
from cep.schema_profile import SchemaProfile, as_string_list, schema_profile_errors
from cep.schema_value import validate_object


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    target: str
    errors: list[str]


def _document_error(
    path: Path,
    error: OSError | json.JSONDecodeError | JsonDocumentError,
) -> ValidationResult:
    return ValidationResult(ok=False, target=str(path), errors=[str(error)])


def validate_schema_file(path: Path) -> ValidationResult:
    try:
        schema = load_json(path)
    except (OSError, json.JSONDecodeError, JsonDocumentError) as exc:
        return _document_error(path, exc)

    errors = schema_profile_errors(schema)
    return ValidationResult(ok=not errors, target=str(path), errors=errors)


def validate_instance(path: Path, schema_path: Path) -> ValidationResult:
    try:
        instance = load_json(path)
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError, JsonDocumentError) as exc:
        return _document_error(path, exc)

    schema_errors = schema_profile_errors(schema)
    if schema_errors:
        return ValidationResult(ok=False, target=str(path), errors=schema_errors)

    errors = validate_object(instance, SchemaProfile(schema=schema, root=schema_path.parent))
    return ValidationResult(ok=not errors, target=str(path), errors=errors)


def _schema_names(registry_path: Path, registry: JsonObject) -> ValidationResult | list[str]:
    schemas = registry.get("schemas")
    match schemas:
        case list():
            names: list[str] = []
            for index, item in enumerate(schemas):
                match item:
                    case str() if item:
                        names.append(item)
                    case _:
                        return ValidationResult(
                            ok=False,
                            target=str(registry_path),
                            errors=[f"schemas[{index}] must be a non-empty string"],
                        )
            return names
        case _:
            return ValidationResult(
                ok=False,
                target=str(registry_path),
                errors=["schemas must be an array of strings"],
            )


def validate_schema_registry(registry_path: Path) -> list[ValidationResult]:
    try:
        registry = load_json(registry_path)
    except (OSError, json.JSONDecodeError, JsonDocumentError) as exc:
        return [_document_error(registry_path, exc)]

    names = _schema_names(registry_path, registry)
    match names:
        case ValidationResult():
            return [names]
        case list():
            return [validate_schema_file(registry_path.parent / name) for name in names]


def validate_all_schemas() -> list[ValidationResult]:
    return validate_schema_registry(SCHEMAS_DIR / "index.json")


def _case_evidence_refs(case_file: Path) -> ValidationResult:
    try:
        case_payload = load_json(case_file)
    except (OSError, json.JSONDecodeError, JsonDocumentError) as exc:
        return _document_error(case_file, exc)

    requirements = case_payload.get("evidence_requirements")
    required_refs: list[str] = []
    optional_refs: list[str] = []
    if isinstance(requirements, dict):
        required_refs = as_string_list(requirements.get("required_evidence_refs"))
        optional_refs = as_string_list(requirements.get("optional_evidence_refs"))

    missing = [
        ref
        for ref in required_refs + optional_refs
        if not (case_file.parent / "evidence" / f"{ref}.json").exists()
    ]
    if missing:
        return ValidationResult(
            ok=False,
            target=str(case_file),
            errors=[f"missing evidence file: {ref}" for ref in missing],
        )
    return ValidationResult(ok=True, target=str(case_file), errors=[])


def _case_ref_matches(path: Path, field_name: str) -> ValidationResult:
    try:
        payload = load_json(path)
    except (OSError, json.JSONDecodeError, JsonDocumentError) as exc:
        return _document_error(path, exc)

    expected = path.parent.name
    observed = payload.get(field_name)
    if observed != expected:
        return ValidationResult(
            ok=False,
            target=str(path),
            errors=[f"{field_name} must be {expected}"],
        )
    return ValidationResult(ok=True, target=str(path), errors=[])


def validate_reality_gap_corpus() -> list[ValidationResult]:
    results: list[ValidationResult] = []

    for path in iter_reality_gap_case_files():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-case.schema.json"))
        results.append(_case_evidence_refs(path))

    for path in iter_reality_gap_answer_keys():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-answer-key.schema.json"))
        results.append(_case_ref_matches(path, "case_ref"))

    for path in iter_reality_gap_example_answers():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-answer.schema.json"))
        results.append(_case_ref_matches(path, "case_ref"))

    results.extend(
        validate_instance(path, SCHEMAS_DIR / "reality-gap-evidence.schema.json")
        for path in iter_reality_gap_evidence_files()
    )

    manifest = reality_gap_anti_collapse_manifest()
    results.append(validate_instance(manifest, SCHEMAS_DIR / "anti-collapse-manifest.schema.json"))

    results.extend(
        validate_instance(path, SCHEMAS_DIR / "anti-collapse-fixture.schema.json")
        for path in iter_reality_gap_anti_collapse_fixtures()
    )

    return results


def validate_semantic_envelope_corpus() -> list[ValidationResult]:
    schema_path = SCHEMAS_DIR / "semantic-envelope.schema.json"
    return [
        validate_instance(path, schema_path) for path in iter_semantic_envelope_fixtures()
    ]


def all_ok(results: list[ValidationResult]) -> bool:
    return all(result.ok for result in results)
