"""GodSpeed CEP-0008 profile validation (reference implementation).

Schema validation uses the generated profile schemas under
``schemas/profiles/godspeed``. The checks here cover what a schema cannot:
recomputing the DomainForge identity digest, keeping a lineage in one pinned
world, and rejecting a world transition that does not move anywhere.

The ``world_ref`` grammar is defined by DomainForge. This module never parses
it; it only compares the digest suffix against a recomputed identity digest.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path

from pydantic import JsonValue

from cep.io import load_json
from cep.json_types import JsonObject
from cep.paths import SCHEMAS_DIR
from cep.schema_profile import SchemaProfile, as_object, as_string
from cep.schema_value import validate_value

PROFILE_DIR = SCHEMAS_DIR / "profiles" / "godspeed"
PROFILES = (
    "semantic_snapshot",
    "authority_request",
    "authority_decision",
    "execution_trace",
    "evidence_packet",
    "settlement_packet",
)
IDENTITY_NS = "domainforge.identity"


def _canonical_json(value: JsonValue) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def identity_digest(identity: JsonObject) -> str:
    """sha256 over canonical JSON of the DomainModelIdentity fields."""
    return "sha256:" + hashlib.sha256(_canonical_json(identity).encode("utf-8")).hexdigest()


def profile_schema_path(profile: str) -> Path:
    if profile not in PROFILES:
        raise ValueError(f"unknown GodSpeed profile: {profile}")
    return PROFILE_DIR / f"{profile}.v1.schema.json"


def validate_profile(envelope: JsonValue, profile: str) -> list[str]:
    """Schema errors for `envelope` against one profile (empty means valid)."""
    path = profile_schema_path(profile)
    return validate_value(envelope, SchemaProfile(schema=load_json(path), root=path.parent), "$")


def world_ref_of(envelope: JsonObject) -> str | None:
    scope = as_object(envelope.get("scope"))
    return as_string(scope.get("world_ref")) if scope else None


def verify_semantics(envelope: JsonObject, profile: str) -> list[str]:
    """Checks beyond the schema. Empty means the envelope's claims hold."""
    errors: list[str] = []
    declared = _profile_declared(envelope)
    if declared != f"godspeed.{profile}":
        errors.append(f"declared profile {declared!r} does not match {profile!r}")
    if profile == "semantic_snapshot":
        errors.extend(_verify_snapshot(envelope))
    return errors


def _profile_declared(envelope: JsonObject) -> str | None:
    ext = as_object(envelope.get("extensions"))
    decl = as_object(ext.get("cep.profile")) if ext else None
    return as_string(decl.get("profile_id")) if decl else None


def _verify_snapshot(envelope: JsonObject) -> list[str]:
    world_ref = world_ref_of(envelope)
    if envelope.get("completeness_status") == "invalid":
        if world_ref is not None:
            return ["an invalid semantic world must not carry a world_ref"]
        return []
    if world_ref is None:
        return ["a valid semantic snapshot must pin a world_ref"]

    ext = as_object(envelope.get("extensions"))
    block = as_object(ext.get(IDENTITY_NS)) if ext else None
    if block is None:
        return [f"missing extensions[{IDENTITY_NS!r}]"]
    identity = as_object(block.get("domain_model_identity"))
    if identity is None:
        return ["missing domain_model_identity"]

    errors: list[str] = []
    recomputed = identity_digest(identity)
    if not world_ref.endswith("@" + recomputed):
        errors.append(
            f"world_ref digest does not match the recomputed identity digest {recomputed}"
        )
    closure = identity.get("semantic_closure_hash")
    if block.get("semantic_closure_hash") != closure:
        errors.append(
            "semantic_closure_hash differs from domain_model_identity.semantic_closure_hash"
        )
    integrity = as_object(envelope.get("integrity"))
    if integrity is not None and integrity.get("semantic_hash") != closure:
        errors.append(
            "integrity.semantic_hash differs from domain_model_identity.semantic_closure_hash"
        )
    return errors


def check_world_consistency(envelopes: Iterable[JsonObject]) -> list[str]:
    """A lineage must stay in one pinned world; a move needs an explicit transition."""
    pinned: dict[str, str] = {}
    for env in envelopes:
        ref = world_ref_of(env)
        if ref is None:
            return [f"envelope {env.get('envelope_id')!r} pins no world_ref"]
        pinned[str(env.get("envelope_id"))] = ref
    if len(set(pinned.values())) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in pinned.items())
        return [f"lineage spans more than one world without an explicit transition: {detail}"]
    return []


def validate_world_transition(record: JsonValue) -> list[str]:
    path = PROFILE_DIR / "world-transition.v1.schema.json"
    errors = validate_value(record, SchemaProfile(schema=load_json(path), root=path.parent), "$")
    obj = as_object(record)
    if (
        not errors
        and obj is not None
        and obj.get("source_world_ref") == obj.get("target_world_ref")
    ):
        errors.append("source_world_ref and target_world_ref must differ")
    return errors
