import json
from pathlib import Path

from typer.testing import CliRunner

from cep.cli import app
from cep.validation import validate_instance, validate_schema_file, validate_schema_registry


def test_validate_schemas() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["validate", "schemas"])

    assert result.exit_code == 0, result.output


def test_validate_reality_gap_corpus() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["validate", "reality-gap-corpus"])

    assert result.exit_code == 0, result.output


def test_validate_all() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["validate", "all"])

    assert result.exit_code == 0, result.output


def test_validate_instance_rejects_missing_required_field(tmp_path: Path) -> None:
    invalid_case = tmp_path / "case.cep.json"
    _ = invalid_case.write_text("{}\n", encoding="utf-8")

    result = validate_instance(invalid_case, Path("schemas/reality-gap-case.schema.json"))

    assert not result.ok
    assert any("case_id" in error for error in result.errors)


def test_validate_instance_rejects_unknown_fields_when_schema_is_strict(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    payload = tmp_path / "payload.json"
    _ = schema.write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Strict Test",
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {"type": "string"},
                },
                "additionalProperties": False,
            },
        ),
        encoding="utf-8",
    )
    _ = payload.write_text(
        json.dumps(
            {
                "id": "ok",
                "extra": True,
            },
        ),
        encoding="utf-8",
    )

    result = validate_instance(payload, schema)

    assert not result.ok
    assert any("unknown field" in error for error in result.errors)


def test_validate_schema_file_rejects_malformed_required(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    _ = schema.write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Malformed Required",
                "type": "object",
                "required": [123],
                "properties": {},
            },
        ),
        encoding="utf-8",
    )

    result = validate_schema_file(schema)

    assert not result.ok
    assert any("required" in error for error in result.errors)


def test_validate_all_schemas_rejects_malformed_registry(tmp_path: Path) -> None:
    registry = tmp_path / "index.json"
    _ = registry.write_text(
        json.dumps(
            {
                "schemas": "not-a-list",
            },
        ),
        encoding="utf-8",
    )

    result = validate_schema_registry(registry)

    assert len(result) == 1
    assert not result[0].ok
    assert any("schemas" in error for error in result[0].errors)
