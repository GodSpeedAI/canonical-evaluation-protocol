"""`allOf` support: profiles layer over the full envelope schema with
`allOf [ {$ref: base}, tightening ]`, so every branch must hold."""

from __future__ import annotations

import json
from pathlib import Path

from cep.schema_profile import SchemaProfile, schema_profile_errors
from cep.schema_value import validate_value


def _profile(schema: dict[str, object], root: Path) -> SchemaProfile:
    return SchemaProfile(schema=schema, root=root)


def test_all_of_is_an_accepted_schema_keyword() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "layered",
        "type": "object",
        "allOf": [{"required": ["a"]}, {"required": ["b"]}],
    }
    assert schema_profile_errors(schema) == []


def test_all_of_rejects_non_array_and_non_object_branches() -> None:
    base = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "layered",
        "type": "object",
    }
    assert schema_profile_errors({**base, "allOf": {}})
    assert schema_profile_errors({**base, "allOf": []})
    assert schema_profile_errors({**base, "allOf": ["nope"]})


def test_every_all_of_branch_must_hold(tmp_path: Path) -> None:
    schema = {"allOf": [{"required": ["a"]}, {"required": ["b"]}]}
    profile = _profile(schema, tmp_path)
    assert validate_value({"a": 1, "b": 2}, profile, "$") == []
    errors = validate_value({"a": 1}, profile, "$")
    assert any("missing required field: b" in e for e in errors)
    both = validate_value({}, profile, "$")
    assert any("field: a" in e for e in both)
    assert any("field: b" in e for e in both)


def test_all_of_resolves_a_relative_ref_branch(tmp_path: Path) -> None:
    (tmp_path / "base.json").write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["id"],
                "properties": {"id": {"type": "string"}},
                "additionalProperties": False,
            }
        )
    )
    layered = {
        "allOf": [
            {"$ref": "./base.json"},
            {"required": ["tier"], "properties": {"tier": {"type": "string"}}},
        ]
    }
    profile = _profile(layered, tmp_path)
    # base forbids unknown fields, so the layered `tier` is rejected by the base
    errors = validate_value({"id": "x", "tier": "gold"}, profile, "$")
    assert any("unknown field: tier" in e for e in errors)
    assert any(
        "missing required field: id" in e for e in validate_value({"tier": "t"}, profile, "$")
    )
