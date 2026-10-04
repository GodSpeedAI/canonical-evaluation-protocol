"""A snapshot emitted by the real DomainForge binary conforms to the profile.

Gated: set CEP_TEST_DOMAINFORGE_BIN to a `domainforge` build that supports
`--world-name` (DomainForge feat/cep-snapshot-world-ref or later). Skipped
otherwise, so `just test` stays hermetic.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

import jsonschema
import pytest
from referencing import Registry, Resource

from cep import godspeed

BIN = os.environ.get("CEP_TEST_DOMAINFORGE_BIN")
pytestmark = pytest.mark.skipif(not BIN, reason="CEP_TEST_DOMAINFORGE_BIN not set")

VALID = 'Entity "User" in auth\nEntity "Role" in auth\n'
HEADER = '@namespace "auth"\n@version "1.0.0"\n\n'


def _emit(source: str, *flags: str) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "model.sea"
        path.write_text(source, encoding="utf-8")
        proc = subprocess.run(  # noqa: S603
            [str(BIN), "envelope", "--emit", "cep", *flags, str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
    return proc.returncode, json.loads(proc.stdout)


def test_valid_world_snapshot_conforms_and_verifies() -> None:
    code, env = _emit(
        HEADER + VALID,
        "--world-name",
        "godspeed-corporate",
        "--world-alias",
        "world:corporate",
        "--world-label",
        "GodSpeed Corporate World",
    )
    assert code == 0
    assert godspeed.validate_profile(env, "semantic_snapshot") == []
    assert godspeed.verify_semantics(env, "semantic_snapshot") == []
    assert godspeed.world_ref_of(env) is not None


def test_invalid_syntax_world_is_flagged_not_pinned_and_conforms() -> None:
    code, env = _emit("this is not sea", "--world-name", "godspeed-corporate")
    assert code != 0
    assert godspeed.world_ref_of(env) is None
    assert godspeed.validate_profile(env, "semantic_snapshot") == []
    assert godspeed.verify_semantics(env, "semantic_snapshot") == []


def test_snapshot_without_world_name_is_not_a_profile_snapshot() -> None:
    code, env = _emit(HEADER + VALID)
    assert code == 0
    assert godspeed.validate_profile(env, "semantic_snapshot"), "must not claim the profile"


def test_standard_jsonschema_agrees_on_emitted_snapshots() -> None:
    base = json.loads(
        (godspeed.PROFILE_DIR.parent.parent / "cep-semantic-envelope.schema.json").read_text(
            "utf-8"
        )
    )
    registry = Registry().with_resource(base["$id"], Resource.from_contents(base))
    schema = json.loads(godspeed.profile_schema_path("semantic_snapshot").read_text("utf-8"))
    validator = jsonschema.Draft202012Validator(schema, registry=registry)
    for flags, source in [
        (("--world-name", "godspeed-corporate"), HEADER + VALID),
        (("--world-name", "godspeed-corporate"), "this is not sea"),
    ]:
        _, env = _emit(source, *flags)
        assert not list(validator.iter_errors(env))
