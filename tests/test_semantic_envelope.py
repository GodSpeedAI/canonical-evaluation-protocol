import json
from pathlib import Path

from typer.testing import CliRunner

from cep.cli import app
from cep.io import load_json
from cep.paths import SCHEMAS_DIR
from cep.validation import all_ok, validate_instance, validate_semantic_envelope_corpus

SCHEMA_PATH = SCHEMAS_DIR / "semantic-envelope.schema.json"


def test_semantic_envelope_fixtures_are_conformant() -> None:
    # Given: the committed v1-shaped Semantic Envelope fixtures.
    # When: they are validated against the CEP-0008 schema profile.
    results = validate_semantic_envelope_corpus()

    # Then: every fixture validates.
    assert results, "expected at least one semantic-envelope fixture"
    assert all_ok(results), [error for result in results for error in result.errors]


def test_semantic_envelope_missing_provenance_fails_named_distinction(tmp_path: Path) -> None:
    # Given: a v1-shaped instance mutated to drop provenance.
    fixture_path = SCHEMAS_DIR / "fixtures" / "semantic-envelope" / "v1-minimal.json"
    valid = load_json(fixture_path)
    del valid["provenance"]
    mutated_path = tmp_path / "missing-provenance.json"
    _ = mutated_path.write_text(json.dumps(valid), encoding="utf-8")

    # When: validated against the CEP-0008 schema profile.
    result = validate_instance(mutated_path, SCHEMA_PATH)

    # Then: it fails, naming the missing distinction, not a generic error.
    assert not result.ok
    assert any("provenance" in error for error in result.errors), result.errors


def test_cli_validate_semantic_envelope() -> None:
    # Given: the CLI validate command.
    runner = CliRunner()

    # When: it validates the committed Semantic Envelope fixtures.
    result = runner.invoke(app, ["validate", "semantic-envelope"])

    # Then: the fixtures pass and the exit code reflects it.
    assert result.exit_code == 0, result.output
