"""godspeed.interaction_event v1: every fixture validates, or fails for its named reason."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

from cep import godspeed
from cep.paths import SCHEMAS_DIR

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SCHEMAS_DIR / "extensions" / "godspeed.interaction_event.v1.json"
CORPUS = SCHEMAS_DIR / "fixtures" / "interaction-event"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
MANIFEST = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)


def _load(kind: str, name: str) -> dict:
    return json.loads((CORPUS / kind / name).read_text(encoding="utf-8"))


def _flat(errors: list[jsonschema.ValidationError]) -> list[jsonschema.ValidationError]:
    out: list[jsonschema.ValidationError] = []
    for err in errors:
        out.append(err)
        out.extend(_flat(list(err.context or [])))
    return out


def test_schema_is_valid_draft_2020_12() -> None:
    jsonschema.Draft202012Validator.check_schema(SCHEMA)


def test_manifest_covers_every_fixture_file() -> None:
    on_disk_valid = sorted(p.name for p in (CORPUS / "valid").glob("*.json"))
    on_disk_invalid = sorted(p.name for p in (CORPUS / "invalid").glob("*.json"))
    assert on_disk_valid == MANIFEST["valid"]
    assert on_disk_invalid == sorted(i["file"] for i in MANIFEST["invalid"])
    assert len(on_disk_valid) >= 2
    assert len(on_disk_invalid) >= 3


@pytest.mark.parametrize("name", MANIFEST["valid"])
def test_valid_fixture_passes(name: str) -> None:
    event = _load("valid", name)
    assert not list(VALIDATOR.iter_errors(event))


@pytest.mark.parametrize("case", MANIFEST["invalid"], ids=lambda c: c["file"])
def test_invalid_fixture_fails_for_its_named_rule(case: dict) -> None:
    event = _load("invalid", case["file"])
    errors = _flat(list(VALIDATOR.iter_errors(event)))
    assert errors, "fixture unexpectedly valid"
    assert any(
        e.validator == case["keyword"]
        and case["contains"] in (e.message + "/".join(map(str, e.absolute_path)))
        for e in errors
    ), [(e.validator, e.message) for e in errors]


@pytest.mark.parametrize("status", ["succeeded", "failed", "denied", "interrupted", "unknown"])
def test_every_outcome_status_is_accepted(status: str) -> None:
    event = copy.deepcopy(_load("valid", MANIFEST["valid"][0]))
    event["outcome"]["status"] = status
    assert not list(VALIDATOR.iter_errors(event))


def test_extension_rides_an_execution_trace_envelope() -> None:
    trace = SCHEMAS_DIR / "fixtures" / "godspeed" / "valid" / "execution_trace.json"
    envelope = json.loads(trace.read_text("utf-8"))
    event = _load("valid", MANIFEST["valid"][0])
    envelope["extensions"]["godspeed.interaction_event"] = event
    assert godspeed.validate_profile(envelope, "execution_trace") == []
    assert not list(VALIDATOR.iter_errors(envelope["extensions"]["godspeed.interaction_event"]))


def test_digest_manifest_matches_schema_files() -> None:
    result = subprocess.run(  # noqa: S603
        [sys.executable, str(ROOT / "tools" / "check_contract_digests.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout


def test_digest_check_fails_when_a_schema_drifts(tmp_path: Path) -> None:
    mod = ROOT / "tools" / "check_contract_digests.py"
    src = mod.read_text(encoding="utf-8")
    (tmp_path / "schemas" / "extensions").mkdir(parents=True)
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "check_contract_digests.py").write_text(src, encoding="utf-8")
    (tmp_path / "schemas" / "extensions" / "DIGESTS").write_text(
        (SCHEMAS_DIR / "extensions" / "DIGESTS").read_text("utf-8"), encoding="utf-8"
    )
    (tmp_path / "schemas" / "extensions" / SCHEMA_PATH.name).write_text(
        SCHEMA_PATH.read_text("utf-8") + " ", encoding="utf-8"
    )
    result = subprocess.run(  # noqa: S603
        [sys.executable, str(tmp_path / "tools" / "check_contract_digests.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "DIGEST MISMATCH" in result.stdout
