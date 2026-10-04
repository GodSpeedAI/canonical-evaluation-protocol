"""GodSpeed CEP-0008 profiles: generated schemas, shared corpus, semantics."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest
from referencing import Registry, Resource
from typer.testing import CliRunner

from cep import godspeed
from cep.cli import app
from cep.paths import SCHEMAS_DIR
from cep.schema_profile import SchemaProfile
from cep.schema_value import validate_value

ROOT = Path(__file__).resolve().parent.parent
CORPUS = SCHEMAS_DIR / "fixtures" / "godspeed"
VENDORED = SCHEMAS_DIR / "vendored" / "world_ref"
MANIFEST = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
VECTORS = json.loads((VENDORED / "golden-vectors.json").read_text(encoding="utf-8"))

# Pinned to DomainForge feat/world-ref a3a4157. Re-vendor from DomainForge; never edit.
PIN_VECTORS = "419ef06c458388c2fa2d0dfd66abf88898872b7dc5c0818a12eb555619006955"
PIN_REFERENCE = "b28e2b1534547fe6d85c368771c3c2aaee68d292abffdffbf52f2fa2bfa84327"


def _load(name: str) -> dict:
    return json.loads((CORPUS / name).read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_vendored_domainforge_vectors_match_their_pin() -> None:
    assert _sha(VENDORED / "golden-vectors.json") == PIN_VECTORS
    assert _sha(VENDORED / "world_ref_reference.py") == PIN_REFERENCE


@pytest.mark.parametrize("tool", ["generate_godspeed_profiles.py", "generate_godspeed_fixtures.py"])
def test_generated_files_are_up_to_date(tool: str) -> None:
    result = subprocess.run(  # noqa: S603
        [sys.executable, str(ROOT / "tools" / tool), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_schema_world_ref_mirrors_domainforge_vectors() -> None:
    schema_path = godspeed.PROFILE_DIR / "world-transition.v1.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    world = SchemaProfile(schema=schema["properties"]["source_world_ref"], root=schema_path.parent)
    for case in VECTORS["valid"]:
        assert validate_value(case["world_ref"], world, "$") == [], case["case"]
    for bad in VECTORS["invalid_refs"]:
        assert validate_value(bad, world, "$"), f"schema accepted {bad!r}"


def test_digest_recomputation_matches_the_vendored_reference() -> None:
    spec = importlib.util.spec_from_file_location("ref", VENDORED / "world_ref_reference.py")
    assert spec is not None
    assert spec.loader is not None
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    for case in VECTORS["valid"]:
        assert godspeed.identity_digest(case["identity"]) == case["canonical_digest"]
        assert ref.canonical_digest(case["identity"]) == case["canonical_digest"]


@pytest.mark.parametrize("case", MANIFEST["cases"], ids=lambda c: c["file"])
def test_corpus_schema_verdicts(case: dict) -> None:
    errors = godspeed.validate_profile(_load(case["file"]), case["profile"])
    if case["schema"] == "valid":
        assert errors == []
    else:
        assert errors, "expected schema errors"
        needle = case.get("schema_error_contains")
        if needle:
            assert any(needle in e for e in errors), errors


@pytest.mark.parametrize(
    "case",
    [c for c in MANIFEST["cases"] if c["schema"] == "valid"],
    ids=lambda c: c["file"],
)
def test_corpus_semantic_verdicts(case: dict) -> None:
    errors = godspeed.verify_semantics(_load(case["file"]), case["profile"])
    if case["semantic"] == "ok":
        assert errors == []
    else:
        assert errors
        needle = case.get("semantic_error_contains")
        if needle:
            assert any(needle in e for e in errors), errors


def test_every_profile_has_a_valid_and_an_invalid_fixture() -> None:
    for profile in godspeed.PROFILES:
        mine = [c for c in MANIFEST["cases"] if c["profile"] == profile]
        assert any(c["schema"] == "valid" for c in mine), profile
        assert any(c["schema"] == "invalid" for c in mine), profile


def test_all_seven_dispositions_have_valid_fixtures() -> None:
    names = {c["file"] for c in MANIFEST["cases"] if c["schema"] == "valid"}
    for decision in (
        "allow",
        "deny",
        "escalate",
        "unknown",
        "constrained_allow",
        "boundary",
        "degraded",
    ):
        assert f"valid/authority_decision-{decision}.json" in names


@pytest.mark.parametrize("chain", MANIFEST["chains"], ids=lambda c: c["case"])
def test_lineage_must_stay_in_one_world(chain: dict) -> None:
    envelopes = []
    for name in chain["files"]:
        env = _load(name)
        override = chain.get("override", {}).get(name)
        if override:
            env["scope"]["world_ref"] = override
        envelopes.append(env)
    errors = godspeed.check_world_consistency(envelopes)
    assert (errors == []) == (chain["expect"] == "consistent"), errors


def test_world_transition_is_explicit_and_must_move() -> None:
    a = MANIFEST["worlds"]["A"]["world_ref"]
    b = MANIFEST["worlds"]["B"]["world_ref"]
    good = {
        "source_world_ref": a,
        "target_world_ref": b,
        "transition_kind": "semantic_change",
        "reason": "corporate policy model gained a Pump entity",
        "compatibility": "backward_compatible",
        "semantic_closure_equal": False,
    }
    assert godspeed.validate_world_transition(good) == []
    assert godspeed.validate_world_transition({**good, "target_world_ref": a})
    assert godspeed.validate_world_transition({k: v for k, v in good.items() if k != "reason"})
    assert godspeed.validate_world_transition({**good, "target_world_ref": "world:corporate"})
    assert godspeed.validate_world_transition({**good, "surprise": 1})


def test_registry_validates_with_the_new_schemas() -> None:

    result = CliRunner().invoke(app, ["validate", "schemas"])
    assert result.exit_code == 0, result.output


def test_standard_jsonschema_library_agrees_with_cep_validator_on_the_whole_corpus() -> None:
    """Independent validator (full Draft 2020-12) must reach the same verdict."""

    base = json.loads((SCHEMAS_DIR / "cep-semantic-envelope.schema.json").read_text("utf-8"))
    registry = Registry().with_resource(base["$id"], Resource.from_contents(base))
    for case in MANIFEST["cases"]:
        schema = json.loads(godspeed.profile_schema_path(case["profile"]).read_text("utf-8"))
        validator = jsonschema.Draft202012Validator(schema, registry=registry)
        env = _load(case["file"])
        standard_ok = not list(validator.iter_errors(env))
        cep_ok = not godspeed.validate_profile(env, case["profile"])
        assert standard_ok == cep_ok == (case["schema"] == "valid"), case["file"]
