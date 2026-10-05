#!/usr/bin/env python3
"""Generate the GodSpeed CEP-0008 profile schemas from one table.

Each profile is `allOf [ {$ref: full envelope}, tightening ]`: it adds
requirements to the full envelope schema and never new top-level fields
(CEP-0008 §18, §39). The `world_ref` grammar is defined by DomainForge; the
patterns here mirror it and are pinned by the vendored golden vectors.

    python tools/generate_godspeed_profiles.py          # write schemas
    python tools/generate_godspeed_profiles.py --check  # fail on drift
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "schemas" / "profiles" / "godspeed"
BASE_REF = "../../cep-semantic-envelope.schema.json"
ID_BASE = "https://cep.dev/schemas/profiles/godspeed"
SCHEMA = "https://json-schema.org/draft/2020-12/schema"
PROFILE_VERSION = "1.0.0"

# world_ref = "world:" name "@" "sha256:" 64 lowercase hex; name length 1..64.
# Two patterns (structure, length) because the CEP validator has no lookahead
# and Rust's regex crate has none either.
WORLD_REF_STRUCTURE = r"^world:[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*@sha256:[0-9a-f]{64}$"
WORLD_REF_NAME_LENGTH = r"^world:[^@]{1,64}@.*$"
WORLD_ALIAS_STRUCTURE = r"^world:[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$"
WORLD_ALIAS_NAME_LENGTH = r"^world:[^@]{1,64}$"
HASH = r"^sha256:[0-9a-f]{64}$"

IDENTITY_FIELDS = [
    "identity_scheme_version",
    "producer",
    "producer_version",
    "language_schema_version",
    "compiler_interpretation_version",
    "canonicalization_version",
    "source_set_hash",
    "content_hash",
    "semantic_closure_hash",
]
IDENTITY_OPTIONAL_HASHES = ["semantic_pack_set_hash", "registry_content_hash"]


def world_ref_schema(description: str) -> dict:
    return {
        "type": "string",
        "description": description,
        "allOf": [
            {"pattern": WORLD_REF_STRUCTURE},
            {"pattern": WORLD_REF_NAME_LENGTH},
        ],
    }


def world_alias_schema() -> dict:
    return {
        "type": "string",
        "description": (
            "Mutable selector (world:<name>). Informational only; "
            "consequential records pin world_ref."
        ),
        "allOf": [
            {"pattern": WORLD_ALIAS_STRUCTURE},
            {"pattern": WORLD_ALIAS_NAME_LENGTH},
        ],
    }


def nonempty_string() -> dict:
    return {"type": "string", "minLength": 1}


def scope_requirements(pinned: bool = True) -> dict:
    scope: dict = {
        "type": "object",
        "properties": {
            "world_ref": world_ref_schema(
                "Immutable reference to exactly one resolved semantic-world revision "
                "(world:<name>@sha256:<digest>); defined by DomainForge."
            ),
            "world_alias": world_alias_schema(),
            "world_label": {
                "type": "string",
                "minLength": 1,
                "description": "Presentation only; never identity.",
            },
        },
    }
    if pinned:
        scope["required"] = ["world_ref"]
    return scope


def profile_declaration(profile_id: str) -> dict:
    return {
        "type": "object",
        "required": ["profile_id", "profile_version"],
        "properties": {
            "profile_id": {"const": profile_id},
            "profile_version": {"const": PROFILE_VERSION},
        },
    }


def identity_schema() -> dict:
    props: dict = {f: nonempty_string() for f in IDENTITY_FIELDS}
    props["identity_scheme_version"] = {"const": "v2-full-preimage"}
    for f in ("source_set_hash", "content_hash", "semantic_closure_hash"):
        props[f] = {"type": "string", "pattern": HASH}
    for f in IDENTITY_OPTIONAL_HASHES:
        # Serialized as null when absent (DomainForge reference §14).
        props[f] = {"anyOf": [{"const": None}, {"type": "string", "pattern": HASH}]}
    return {
        "type": "object",
        "required": IDENTITY_FIELDS + IDENTITY_OPTIONAL_HASHES,
        "properties": props,
    }


def items_require(*fields: str) -> dict:
    return {"minItems": 1, "items": {"required": list(fields)}}


def extension_require(namespace: str, *fields: str, properties: dict | None = None) -> dict:
    ext: dict = {"type": "object", "required": list(fields)}
    if properties:
        ext["properties"] = properties
    return {namespace: ext}


def tightening(  # noqa: PLR0913 - keyword-only profile knobs
    kind: str,
    *,
    required: list[str],
    lineage_min: int = 0,
    extra_properties: dict | None = None,
    extension_required: list[str] | None = None,
    extension_properties: dict | None = None,
) -> dict:
    properties: dict = {
        "envelope_kind": {"const": kind},
        "scope": scope_requirements(),
        "extensions": {
            "type": "object",
            "required": ["cep.profile", *(extension_required or [])],
            "properties": {
                "cep.profile": profile_declaration(f"godspeed.{kind}"),
                **(extension_properties or {}),
            },
        },
    }
    if lineage_min:
        properties["lineage_refs"] = {"minItems": lineage_min}
    properties.update(extra_properties or {})
    return {
        "required": ["scope", "extensions", *required],
        "properties": properties,
    }


DECISION_PLAIN = ["allow", "deny", "escalate", "unknown"]
DECISION_CONSTRAINED = ["constrained_allow", "boundary"]
DECISION_DEGRADED = "degraded"


def decision_extension(decisions: dict, *required: str) -> dict:
    return {
        "type": "object",
        "required": ["decision", "operation_id", "request_ref", *required],
        "properties": {
            "decision": decisions,
            "operation_id": nonempty_string(),
            "request_ref": nonempty_string(),
            "policy_basis": {"type": "array", "minItems": 1, "items": nonempty_string()},
            "compensating_controls": {
                "type": "array",
                "minItems": 1,
                "items": nonempty_string(),
            },
        },
    }


def authority_decision_profile() -> dict:
    base = tightening(
        "authority_decision",
        required=["transformations", "authority", "provenance"],
        lineage_min=1,
        extra_properties={
            "authority": items_require("authority_id", "subject_actor_ref"),
        },
    )
    ns = "godspeed.authority_decision"

    def branch(decisions: dict, *ext_required: str, constraints: bool, description: str) -> dict:
        b: dict = {
            "description": description,
            "required": ["extensions", *(["constraints"] if constraints else [])],
            "properties": {
                "extensions": {
                    "required": [ns],
                    "properties": {ns: decision_extension(decisions, *ext_required)},
                }
            },
        }
        if constraints:
            b["properties"]["constraints"] = {"minItems": 1}
        return b

    base["anyOf"] = [
        branch(
            {"enum": DECISION_PLAIN},
            constraints=False,
            description="plain decision: allow, deny, escalate or unknown",
        ),
        branch(
            {"enum": DECISION_CONSTRAINED},
            "policy_basis",
            constraints=True,
            description="constrained_allow or boundary keeps its constraints and policy basis",
        ),
        branch(
            {"const": DECISION_DEGRADED},
            "policy_basis",
            "compensating_controls",
            constraints=True,
            description="degraded keeps its compensating controls, constraints and policy basis",
        ),
    ]
    return base


def semantic_snapshot_profile() -> dict:
    ns = "domainforge.identity"
    status = "model_validation_status"
    valid_world = {
        "description": "valid world: pinned world_ref, identity and integrity present",
        "required": ["scope", "integrity", "representations", "references", "provenance"],
        "properties": {
            "scope": scope_requirements(pinned=True),
            "extensions": {
                "required": [ns],
                "properties": {
                    ns: {
                        "type": "object",
                        "required": ["domain_model_identity", "semantic_closure_hash"],
                        "properties": {
                            "domain_model_identity": identity_schema(),
                            "semantic_closure_hash": {"type": "string", "pattern": HASH},
                        },
                    },
                    # DomainForge omits the flag for a valid model; when present it must say valid.
                    "domainforge": {"properties": {status: {"const": "valid"}}},
                },
            },
        },
    }
    invalid_world = {
        "description": (
            "invalid world: explicitly flagged invalid by the producer; it is never pinned "
            "(no world_ref), so it cannot masquerade as a valid world"
        ),
        "required": ["extensions"],
        "properties": {
            "extensions": {
                "required": ["domainforge"],
                "properties": {
                    "domainforge": {
                        "type": "object",
                        "required": [status],
                        "properties": {status: {"const": "invalid"}},
                    }
                },
            }
        },
    }
    base = tightening("semantic_snapshot", required=["provenance"])
    # The pinned-scope requirement belongs to the valid-world branch only.
    base["properties"]["scope"] = scope_requirements(pinned=False)
    base["anyOf"] = [valid_world, invalid_world]
    return base


RETRIEVAL_COMPLETENESS = ["complete", "partial", "none"]
CONTEXT_NS = "godspeed.context_bundle"


def context_bundle_profile() -> dict:
    """A context bundle never presents partial retrieval as complete.

    `retrieval_completeness` (the producer's own statement) and the envelope's
    `completeness_status` must agree, and anything short of `complete` must carry
    at least one omission, so absence is never read as falsehood (CEP-0008 §34).
    """
    base = tightening(
        "context_bundle",
        required=["provenance", "completeness_status"],
        extension_required=[CONTEXT_NS],
        extension_properties=extension_require(
            CONTEXT_NS,
            "work_request_ref",
            "retrieval_completeness",
            properties={
                "work_request_ref": nonempty_string(),
                "retrieval_completeness": {"enum": RETRIEVAL_COMPLETENESS},
            },
        ),
    )

    def branch(level: str, statuses: dict, *, references: bool, description: str) -> dict:
        required = ["extensions", "completeness_status"]
        properties: dict = {
            "completeness_status": statuses,
            "extensions": {
                "required": [CONTEXT_NS],
                "properties": {
                    CONTEXT_NS: {
                        "required": ["retrieval_completeness"],
                        "properties": {"retrieval_completeness": {"const": level}},
                    }
                },
            },
        }
        if references:
            required.append("references")
            properties["references"] = {"minItems": 1}
        else:
            # Nothing retrieved: the context question stands, unanswered, and is the
            # envelope's entity section (a CEP envelope needs at least one).
            required.append("questions")
            properties["questions"] = {"minItems": 1}
        if level != "complete":
            required.append("omissions")
            properties["omissions"] = {"minItems": 1}
        return {"description": description, "required": required, "properties": properties}

    base["anyOf"] = [
        branch(
            "complete",
            {"const": "complete_for_context"},
            references=True,
            description="complete retrieval: cited references, status complete_for_context",
        ),
        branch(
            "partial",
            {"enum": ["partial", "minimal", "unknown"]},
            references=True,
            description="partial retrieval: cited references and marked omissions, never complete",
        ),
        branch(
            "none",
            {"enum": ["minimal", "unknown"]},
            references=False,
            description="nothing retrieved: the unanswered question and marked omissions, never complete",
        ),
    ]
    return base


PROFILES: dict[str, dict] = {
    "semantic_snapshot": semantic_snapshot_profile(),
    "context_bundle": context_bundle_profile(),
    "authority_request": tightening(
        "authority_request",
        required=["transformations", "authority", "provenance", "references"],
        extra_properties={
            "authority": items_require("authority_id", "subject_actor_ref"),
            "transformations": items_require("transformation_id", "transformation_type"),
        },
        extension_required=["godspeed.authority_request"],
        extension_properties=extension_require(
            "godspeed.authority_request", "operation_id", "correlation_id"
        ),
    ),
    "authority_decision": authority_decision_profile(),
    "execution_trace": tightening(
        "execution_trace",
        required=["transformations", "provenance"],
        lineage_min=1,
        extra_properties={
            "transformations": items_require("transformation_id", "transformation_type"),
        },
        extension_required=["godspeed.execution_trace"],
        extension_properties=extension_require(
            "godspeed.execution_trace",
            "operation_id",
            "authority_decision_ref",
            "correlation_id",
        ),
    ),
    "evidence_packet": tightening(
        "evidence_packet",
        required=["evidence", "questions", "provenance"],
        lineage_min=1,
        extension_required=["godspeed.evidence_packet"],
        extension_properties=extension_require("godspeed.evidence_packet", "operation_id"),
    ),
    "settlement_packet": tightening(
        "settlement_packet",
        required=["settlements", "evidence", "questions", "provenance"],
        lineage_min=1,
        extension_required=["godspeed.settlement_packet"],
        extension_properties=extension_require("godspeed.settlement_packet", "operation_id"),
    ),
}

# The semantic_snapshot extension namespace is DomainForge's; the others are GodSpeed's.
# Profiles that carry a snapshot-style identity declare it in `extensions`.
DESCRIPTIONS = {
    "semantic_snapshot": "Bounded state of a semantic world, pinned by world_ref (CEP-0008 §9.11).",
    "context_bundle": (
        "Context retrieved for a work request, pinned to a world. Partial retrieval is "
        "never presented as complete (CEP-0008 §9.2, §34)."
    ),
    "authority_request": (
        "Request to govern one consequential transformation inside a pinned world (CEP-0008 §9.3)."
    ),
    "authority_decision": (
        "Governed disposition of an authority request; constrained "
        "dispositions keep their constraints (CEP-0008 §9.4)."
    ),
    "execution_trace": (
        "What was done under an authority decision. A trace is not settlement (CEP-0008 §9.5)."
    ),
    "evidence_packet": (
        "Evidence relative to a question or claim. Evidence is not settlement (CEP-0008 §9.6)."
    ),
    "settlement_packet": "Settlement of an operation from its evidence (CEP-0008 §9.7).",
}


def profile_schema(kind: str) -> dict:
    return {
        "$schema": SCHEMA,
        "$id": f"{ID_BASE}/{kind}.v1.schema.json",
        "title": f"GodSpeed {kind} profile v{PROFILE_VERSION}",
        "description": DESCRIPTIONS[kind],
        "type": "object",
        "allOf": [{"$ref": BASE_REF}, PROFILES[kind]],
    }


def world_transition_schema() -> dict:
    return {
        "$schema": SCHEMA,
        "$id": f"{ID_BASE}/world-transition.v1.schema.json",
        "title": f"GodSpeed world transition v{PROFILE_VERSION}",
        "description": (
            "Explicit move of work from one immutable semantic world to another. "
            "Never implied by an alias retarget. source_world_ref and target_world_ref "
            "must differ (checked by the typed validators)."
        ),
        "type": "object",
        "required": [
            "source_world_ref",
            "target_world_ref",
            "transition_kind",
            "reason",
            "compatibility",
            "semantic_closure_equal",
        ],
        "additionalProperties": False,
        "properties": {
            "source_world_ref": world_ref_schema("World the work is pinned to today."),
            "target_world_ref": world_ref_schema("World the work moves to."),
            "transition_kind": {
                "enum": ["semantic_change", "source_edit_only", "compiler_upgrade", "migration"]
            },
            "reason": nonempty_string(),
            "compatibility": {"enum": ["compatible", "backward_compatible", "breaking", "unknown"]},
            "semantic_closure_equal": {
                "type": "boolean",
                "description": "True only when both worlds have the same semantic_closure_hash.",
            },
            "semantic_diff_ref": nonempty_string(),
            "migration_ref": nonempty_string(),
            "authority_decision_ref": nonempty_string(),
            "evidence_refs": {"type": "array", "items": nonempty_string()},
        },
    }


def outputs() -> dict[Path, str]:
    files: dict[Path, str] = {}
    for kind in PROFILES:
        files[OUT / f"{kind}.v1.schema.json"] = (
            json.dumps(profile_schema(kind), indent=2, ensure_ascii=False) + "\n"
        )
    files[OUT / "world-transition.v1.schema.json"] = (
        json.dumps(world_transition_schema(), indent=2, ensure_ascii=False) + "\n"
    )
    return files


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale: list[str] = []
    for path, text in outputs().items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    if check:
        if stale:
            print("stale generated profile schemas (run tools/generate_godspeed_profiles.py):")
            print("\n".join(f"  {s}" for s in stale))
            return 1
        print("godspeed profile schemas are up to date")
        return 0
    print(f"wrote {len(outputs())} schemas to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
