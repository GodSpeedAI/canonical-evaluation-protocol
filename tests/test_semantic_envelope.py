import json
from pathlib import Path

from typer.testing import CliRunner

from cep.cli import app
from cep.io import load_json
from cep.paths import SCHEMAS_DIR
from cep.validation import (
    all_ok,
    validate_instance,
    validate_instance_json,
    validate_semantic_envelope_corpus,
    validate_semantic_envelope_full_corpus,
)

SCHEMA_PATH = SCHEMAS_DIR / "semantic-envelope.schema.json"
FULL_SCHEMA_PATH = SCHEMAS_DIR / "cep-semantic-envelope.schema.json"
FULL_FIXTURES_DIR = SCHEMAS_DIR / "fixtures" / "semantic-envelope-full"

REQUIRED_SS52_FIELDS = [
    "envelope_id",
    "cep_version",
    "envelope_version",
    "envelope_kind",
    "created_at",
    "created_by",
    "scope",
    "boundary_record",
    "completeness_status",
    "provenance_refs",
    "omission_status",
]

INVALID_FIXTURES = {
    "invalid-missing-identity.json": "envelope_id",
    "invalid-missing-cep-version.json": "cep_version",
    "invalid-missing-scope.json": "scope",
    "invalid-missing-boundary-record.json": "boundary_record",
    "invalid-missing-provenance.json": "provenance",
    "invalid-missing-completeness-status.json": "completeness",
    "invalid-no-entity-section.json": "entity section",
    "invalid-no-validation-conformance-status.json": "anyOf",
    "invalid-raw-context-as-envelope.json": "raw_context",
    "invalid-data-as-evidence.json": "raw_data",
    "invalid-representation-as-reality.json": "is_reality",
    "invalid-action-as-transformation.json": "action",
    "invalid-completion-as-settlement.json": "completion_status",
    "invalid-authority-as-capability.json": "authority_grant",
    "invalid-possibility-as-affordance.json": "is_possible",
    "invalid-hidden-omissions.json": "omission_id",
    "invalid-hidden-contradictions.json": "contradiction_id",
    "invalid-signature-as-truth.json": "signature_is_truth",
    "invalid-unmarked-unavailable-reference.json": "availability_status",
    "invalid-unknown-top-level-field.json": "silent_uncertainty_drop",
}


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


def test_full_profile_valid_fixtures_pass() -> None:
    # Given: the committed canonical full-profile fixtures.
    # When: they are validated against cep-semantic-envelope.schema.json.
    results = validate_semantic_envelope_full_corpus()
    valid_names = {
        path.name for path in (FULL_FIXTURES_DIR / "valid-*.json").parent.glob("valid-*.json")
    }

    # Then: every valid fixture passes.
    assert valid_names, "expected at least one valid full-profile fixture"
    valid_results = [result for result in results if Path(result.target).name in valid_names]
    assert valid_results, "expected valid fixtures in the full corpus results"
    assert all_ok(valid_results), [error for result in valid_results for error in result.errors]


def test_full_profile_every_ss52_field_individually_required(tmp_path: Path) -> None:
    # Given: the smallest lawful envelope.
    base = load_json(FULL_FIXTURES_DIR / "valid-minimal.json")

    # When: each SS52-required field is dropped in turn.
    for field in REQUIRED_SS52_FIELDS:
        mutated = {key: value for key, value in base.items() if key != field}
        mutated_path = tmp_path / f"missing-{field}.json"
        _ = mutated_path.write_text(json.dumps(mutated), encoding="utf-8")
        result = validate_instance(mutated_path, FULL_SCHEMA_PATH)

        # Then: validation fails naming the dropped field.
        assert not result.ok, f"envelope without {field} must be invalid"
        assert any(field in error for error in result.errors), (
            f"expected error naming {field}, got: {result.errors}"
        )


def test_full_profile_invalid_fixtures_fail_for_named_reason() -> None:
    # Given: one invalid fixture per CEP-0008 SS53 bullet.
    # When: each is validated against the canonical full profile.
    for fixture_name, named_reason in INVALID_FIXTURES.items():
        result = validate_instance(FULL_FIXTURES_DIR / fixture_name, FULL_SCHEMA_PATH)

        # Then: it fails with a structurally detectable, named reason.
        assert not result.ok, f"{fixture_name} must be invalid"
        assert any(named_reason in error for error in result.errors), (
            f"{fixture_name} should fail for reason {named_reason!r}, got: {result.errors}"
        )


def test_full_profile_flat_fixtures_stay_scoped_to_flat_profile() -> None:
    # Given: the v1 flat profile and its own fixtures.
    flat_results = validate_semantic_envelope_corpus()

    # Then: the flat profile is unchanged and still validates its fixtures.
    assert all_ok(flat_results), [error for result in flat_results for error in result.errors]


def test_cli_validate_single_envelope_path() -> None:
    # Given: a valid canonical envelope and the CLI validate command.
    runner = CliRunner()

    # When: it validates that single envelope by path.
    result = runner.invoke(
        app,
        ["validate", "semantic-envelope", str(FULL_FIXTURES_DIR / "valid-minimal.json")],
    )

    # Then: it passes with exit code 0.
    assert result.exit_code == 0, result.output


def test_cli_validate_single_invalid_envelope_path() -> None:
    # Given: an invalid canonical envelope and the CLI validate command.
    runner = CliRunner()

    # When: it validates that single envelope by path.
    result = runner.invoke(
        app,
        ["validate", "semantic-envelope", str(FULL_FIXTURES_DIR / "invalid-missing-identity.json")],
    )

    # Then: it fails with exit code 1 naming the reason.
    assert result.exit_code == 1
    assert "envelope_id" in result.output


def test_cli_validate_semantic_envelope_stdin() -> None:
    # Given: a canonical envelope on standard input.
    runner = CliRunner()
    envelope = load_json(FULL_FIXTURES_DIR / "valid-work-request.json")

    # When: the CLI validates stdin.
    result = runner.invoke(
        app, ["validate", "semantic-envelope", "--stdin"], input=json.dumps(envelope)
    )

    # Then: it passes with exit code 0.
    assert result.exit_code == 0, result.output


def test_cli_validate_semantic_envelope_stdin_invalid() -> None:
    # Given: an invalid canonical envelope on standard input.
    runner = CliRunner()
    envelope = load_json(FULL_FIXTURES_DIR / "invalid-missing-identity.json")

    # When: the CLI validates stdin.
    result = runner.invoke(
        app, ["validate", "semantic-envelope", "--stdin"], input=json.dumps(envelope)
    )

    # Then: it fails with exit code 1 naming the reason.
    assert result.exit_code == 1
    assert "envelope_id" in result.output


def test_validate_instance_json_stdin_equivalence() -> None:
    # Given: the same envelope content as a JSON string and as a file.
    content = (FULL_FIXTURES_DIR / "valid-semantic-snapshot.json").read_text(encoding="utf-8")
    string_result = validate_instance_json(content, FULL_SCHEMA_PATH, target="stdin")
    file_result = validate_instance(
        FULL_FIXTURES_DIR / "valid-semantic-snapshot.json", FULL_SCHEMA_PATH
    )

    # Then: both validation paths agree.
    assert string_result.ok
    assert file_result.ok
