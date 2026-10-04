#!/usr/bin/env python3
"""Generate the shared GodSpeed profile conformance corpus.

The corpus under schemas/fixtures/godspeed/ is consumed by the Python, Rust
and TypeScript validators, so all three are tested against the same bytes.
Digests come from the vendored DomainForge reference implementation.

    python tools/generate_godspeed_fixtures.py          # write corpus
    python tools/generate_godspeed_fixtures.py --check  # fail on drift
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "schemas" / "fixtures" / "godspeed"
REF_PATH = ROOT / "schemas" / "vendored" / "world_ref" / "world_ref_reference.py"
VECTORS_PATH = ROOT / "schemas" / "vendored" / "world_ref" / "golden-vectors.json"

spec = importlib.util.spec_from_file_location("world_ref_reference", REF_PATH)
ref = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(ref)  # type: ignore[union-attr]

VECTORS = {v["case"]: v for v in json.loads(VECTORS_PATH.read_text(encoding="utf-8"))["valid"]}
WORLD_A = VECTORS["minimal"]  # name godspeed-corporate
WORLD_B = VECTORS["semantic-change"]
NOW = "2026-10-04T12:00:00Z"
PROFILE_VERSION = "1.0.0"
HASH_X = "sha256:" + "ab" * 32


def envelope(kind: str, world: dict | None, **sections: object) -> dict:
    scope: dict = {"evaluation_context": f"godspeed-{kind}"}
    if world is not None:
        scope["world_ref"] = world["world_ref"]
        scope["world_alias"] = "world:corporate"
        scope["world_label"] = "GodSpeed Corporate World"
    env: dict = {
        "envelope_id": f"env-{kind}-0001",
        "cep_version": "1.0.0",
        "envelope_version": "1.0",
        "envelope_kind": kind,
        "created_at": NOW,
        "created_by": "godspeed-fixture-writer",
        "scope": scope,
        "boundary_record": {
            "scope": f"{kind} fixture",
            "included_sections": sorted(sections),
            "excluded_sections": [],
            "known_omissions": ["fixture content is illustrative"],
            "unknowns": [],
            "redactions": [],
            "compression_notes": [],
            "out_of_scope_entities": [],
            "classification": "test",
            "limitations": [],
        },
        "completeness_status": "partial",
        "omission_status": "marked",
        "provenance_refs": [f"prov-{kind}-0001"],
        "validation_status": "valid",
        "lineage_refs": [],
        "provenance": [
            {
                "provenance_id": f"prov-{kind}-0001",
                "source_system_refs": ["godspeed-fixtures"],
                "producer_refs": ["godspeed-fixture-writer"],
                "production_method": "fixture",
                "created_at": NOW,
            }
        ],
    }
    env.update(sections)
    return env


def profile_ext(kind: str, **extra: object) -> dict:
    ext: dict = {
        "cep.profile": {
            "profile_id": f"godspeed.{kind}",
            "profile_version": PROFILE_VERSION,
        }
    }
    ext.update(extra)
    return ext


def references() -> list[dict]:
    return [
        {
            "ref_id": "ref-resource-0001",
            "ref_type": "artifact_id",
            "target_uri_or_id": "artifact:report-0001",
            "availability_status": "available",
            "integrity_status": "verifiable",
        }
    ]


def transformation() -> list[dict]:
    return [
        {
            "transformation_id": "tr-op-0001",
            "transformation_type": "capability_invocation",
        }
    ]


def authority_ctx() -> list[dict]:
    return [{"authority_id": "auth-0001", "subject_actor_ref": "actor:agent-7"}]


def snapshot_valid(world: dict) -> dict:
    ident = world["identity"]
    env = envelope(
        "semantic_snapshot",
        world,
        references=references(),
        representations=[
            {
                "representation_id": "rep-d-0001",
                "representation_kind": "canonical_semantic_representation",
                "representation_type": "domainforge-semantic-envelope/v1",
                "content_hash": ident["content_hash"],
            }
        ],
        integrity={
            "content_hash": ident["content_hash"],
            "semantic_hash": ident["semantic_closure_hash"],
        },
    )
    env["extensions"] = profile_ext(
        "semantic_snapshot",
        **{
            "domainforge.identity": {
                "domain_model_identity": ident,
                "semantic_closure_hash": ident["semantic_closure_hash"],
            }
        },
    )
    return env


def snapshot_invalid_world() -> dict:
    env = envelope(
        "semantic_snapshot",
        None,
        references=references(),
        omissions=[
            {
                "omission_id": "om-0001",
                "omission_type": "canonical_representation_D",
                "reason": "model failed validation; no canonical representation exists",
            }
        ],
    )
    env["completeness_status"] = "incomplete_for_declared_state"
    env["extensions"] = profile_ext(
        "semantic_snapshot",
        domainforge={
            "model_validation_status": "invalid",
            "diagnostics": ["APP001: declared model failed validation"],
        },
    )
    return env


def authority_request(world: dict) -> dict:
    env = envelope(
        "authority_request",
        world,
        transformations=transformation(),
        authority=authority_ctx(),
        references=references(),
        states=[{"state_id": "st-0001", "state_type": "declared_state", "subject_ref": "run:0001"}],
    )
    env["extensions"] = profile_ext(
        "authority_request",
        **{
            "godspeed.authority_request": {
                "operation_id": "op-0001",
                "correlation_id": "corr-0001",
                "causation_id": "cause-0001",
            }
        },
    )
    return env


def authority_decision(world: dict, decision: str, **ext: object) -> dict:
    sections: dict = {
        "transformations": transformation(),
        "authority": authority_ctx(),
    }
    if decision in ("constrained_allow", "boundary", "degraded"):
        sections["constraints"] = [
            {"constraint_id": "con-0001", "constraint_type": "rate_limit", "description": "10/min"}
        ]
    env = envelope("authority_decision", world, **sections)
    env["lineage_refs"] = ["env-authority_request-0001"]
    body: dict = {
        "decision": decision,
        "operation_id": "op-0001",
        "request_ref": "env-authority_request-0001",
    }
    body.update(ext)
    env["extensions"] = profile_ext("authority_decision", **{"godspeed.authority_decision": body})
    return env


def execution_trace(world: dict) -> dict:
    env = envelope(
        "execution_trace",
        world,
        transformations=transformation(),
        observations=[{"observation_id": "obs-0001", "method": "process-exit-code"}],
    )
    env["lineage_refs"] = ["env-authority_decision-0001"]
    env["extensions"] = profile_ext(
        "execution_trace",
        **{
            "godspeed.execution_trace": {
                "operation_id": "op-0001",
                "authority_decision_ref": "env-authority_decision-0001",
                "correlation_id": "corr-0001",
            }
        },
    )
    return env


def evidence_packet(world: dict) -> dict:
    env = envelope(
        "evidence_packet",
        world,
        questions=[
            {"question_id": "q-0001", "question_form": "Did the artifact reach the expected state?"}
        ],
        evidence=[
            {
                "evidence_id": "ev-0001",
                "evidence_type": "observed_state_comparison",
                "question_ref": "q-0001",
                "target_entity_ref": "artifact:report-0001",
            }
        ],
    )
    env["lineage_refs"] = ["env-execution_trace-0001"]
    env["extensions"] = profile_ext(
        "evidence_packet", **{"godspeed.evidence_packet": {"operation_id": "op-0001"}}
    )
    return env


def settlement_packet(world: dict) -> dict:
    env = envelope(
        "settlement_packet",
        world,
        questions=[
            {"question_id": "q-0001", "question_form": "Did the artifact reach the expected state?"}
        ],
        evidence=[
            {
                "evidence_id": "ev-0001",
                "evidence_type": "observed_state_comparison",
                "question_ref": "q-0001",
                "target_entity_ref": "artifact:report-0001",
            }
        ],
        settlements=[
            {
                "settlement_id": "set-0001",
                "settlement_status": "settled",
                "transformation_ref": "tr-op-0001",
                "question_ref": "q-0001",
                "threshold_basis": "expected state equals observed state",
            }
        ],
    )
    env["lineage_refs"] = ["env-evidence_packet-0001"]
    env["extensions"] = profile_ext(
        "settlement_packet", **{"godspeed.settlement_packet": {"operation_id": "op-0001"}}
    )
    return env


def mutate(env: dict, fn) -> dict:
    out = copy.deepcopy(env)
    fn(out)
    return out


def build() -> tuple[dict[str, dict], list[dict]]:
    """Return (files by relative name, manifest entries)."""
    files: dict[str, dict] = {}
    manifest: list[dict] = []

    def add(
        name: str,
        profile: str,
        env: dict,
        *,
        schema: str,
        semantic: str = "ok",
        schema_error: str | None = None,
        semantic_error: str | None = None,
    ) -> None:
        files[name] = env
        entry: dict = {"file": name, "profile": profile, "schema": schema, "semantic": semantic}
        if schema_error:
            entry["schema_error_contains"] = schema_error
        if semantic_error:
            entry["semantic_error_contains"] = semantic_error
        manifest.append(entry)

    snap = snapshot_valid(WORLD_A)
    add("valid/semantic_snapshot.json", "semantic_snapshot", snap, schema="valid")
    add(
        "valid/semantic_snapshot-invalid-world.json",
        "semantic_snapshot",
        snapshot_invalid_world(),
        schema="valid",
    )
    req = authority_request(WORLD_A)
    add("valid/authority_request.json", "authority_request", req, schema="valid")
    add(
        "valid/authority_decision-allow.json",
        "authority_decision",
        authority_decision(WORLD_A, "allow"),
        schema="valid",
    )
    add(
        "valid/authority_decision-deny.json",
        "authority_decision",
        authority_decision(WORLD_A, "deny"),
        schema="valid",
    )
    add(
        "valid/authority_decision-escalate.json",
        "authority_decision",
        authority_decision(WORLD_A, "escalate"),
        schema="valid",
    )
    add(
        "valid/authority_decision-unknown.json",
        "authority_decision",
        authority_decision(WORLD_A, "unknown"),
        schema="valid",
    )
    add(
        "valid/authority_decision-constrained_allow.json",
        "authority_decision",
        authority_decision(WORLD_A, "constrained_allow", policy_basis=["policy:rate-limit-v2"]),
        schema="valid",
    )
    add(
        "valid/authority_decision-boundary.json",
        "authority_decision",
        authority_decision(WORLD_A, "boundary", policy_basis=["policy:boundary-v1"]),
        schema="valid",
    )
    add(
        "valid/authority_decision-degraded.json",
        "authority_decision",
        authority_decision(
            WORLD_A,
            "degraded",
            policy_basis=["policy:degraded-v1"],
            compensating_controls=["control:human-review"],
        ),
        schema="valid",
    )
    add("valid/execution_trace.json", "execution_trace", execution_trace(WORLD_A), schema="valid")
    add("valid/evidence_packet.json", "evidence_packet", evidence_packet(WORLD_A), schema="valid")
    add(
        "valid/settlement_packet.json",
        "settlement_packet",
        settlement_packet(WORLD_A),
        schema="valid",
    )

    # ---- schema-invalid ----
    def drop_world(e: dict) -> None:
        del e["scope"]["world_ref"]

    add(
        "invalid/semantic_snapshot-missing-world_ref.json",
        "semantic_snapshot",
        mutate(snap, drop_world),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/semantic_snapshot-alias-as-world_ref.json",
        "semantic_snapshot",
        mutate(snap, lambda e: e["scope"].__setitem__("world_ref", "world:godspeed-corporate")),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/semantic_snapshot-uppercase-digest.json",
        "semantic_snapshot",
        mutate(
            snap,
            lambda e: e["scope"].__setitem__(
                "world_ref", "world:godspeed-corporate@sha256:" + "A" * 64
            ),
        ),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/semantic_snapshot-missing-identity.json",
        "semantic_snapshot",
        mutate(snap, lambda e: e["extensions"].pop("domainforge.identity")),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/semantic_snapshot-invalid-world-unflagged.json",
        "semantic_snapshot",
        mutate(snapshot_invalid_world(), lambda e: e["extensions"].pop("domainforge")),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/semantic_snapshot-valid-claim-with-bogus-flag.json",
        "semantic_snapshot",
        mutate(
            snap,
            lambda e: e["extensions"].__setitem__(
                "domainforge", {"model_validation_status": "bogus"}
            ),
        ),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/authority_request-missing-world_ref.json",
        "authority_request",
        mutate(req, drop_world),
        schema="invalid",
        schema_error="world_ref",
    )
    add(
        "invalid/authority_request-missing-profile-declaration.json",
        "authority_request",
        mutate(req, lambda e: e["extensions"].pop("cep.profile")),
        schema="invalid",
        schema_error="cep.profile",
    )
    add(
        "invalid/authority_request-wrong-profile-declared.json",
        "authority_request",
        mutate(
            req,
            lambda e: e["extensions"]["cep.profile"].__setitem__(
                "profile_id", "godspeed.authority_decision"
            ),
        ),
        schema="invalid",
        schema_error="must equal",
    )
    add(
        "invalid/authority_request-missing-correlation.json",
        "authority_request",
        mutate(req, lambda e: e["extensions"]["godspeed.authority_request"].pop("correlation_id")),
        schema="invalid",
        schema_error="correlation_id",
    )
    add(
        "invalid/authority_request-unlabelled-actor.json",
        "authority_request",
        mutate(req, lambda e: e["authority"][0].pop("subject_actor_ref")),
        schema="invalid",
        schema_error="subject_actor_ref",
    )

    boundary = authority_decision(WORLD_A, "boundary", policy_basis=["policy:boundary-v1"])
    add(
        "invalid/authority_decision-boundary-without-constraints.json",
        "authority_decision",
        mutate(boundary, lambda e: e.pop("constraints")),
        schema="invalid",
        schema_error="anyOf",
    )
    degraded = authority_decision(
        WORLD_A,
        "degraded",
        policy_basis=["policy:degraded-v1"],
        compensating_controls=["control:human-review"],
    )
    add(
        "invalid/authority_decision-degraded-without-controls.json",
        "authority_decision",
        mutate(
            degraded,
            lambda e: e["extensions"]["godspeed.authority_decision"].pop("compensating_controls"),
        ),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/authority_decision-boolean-flattened.json",
        "authority_decision",
        mutate(
            authority_decision(WORLD_A, "allow"),
            lambda e: e["extensions"]["godspeed.authority_decision"].__setitem__("decision", True),
        ),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/authority_decision-unrecognised-disposition.json",
        "authority_decision",
        authority_decision(WORLD_A, "maybe"),
        schema="invalid",
        schema_error="anyOf",
    )
    add(
        "invalid/authority_decision-no-request-lineage.json",
        "authority_decision",
        mutate(authority_decision(WORLD_A, "allow"), lambda e: e.__setitem__("lineage_refs", [])),
        schema="invalid",
        schema_error="at least 1 items",
    )
    add(
        "invalid/execution_trace-no-decision-lineage.json",
        "execution_trace",
        mutate(execution_trace(WORLD_A), lambda e: e.__setitem__("lineage_refs", [])),
        schema="invalid",
        schema_error="at least 1 items",
    )
    add(
        "invalid/evidence_packet-data-without-question.json",
        "evidence_packet",
        mutate(evidence_packet(WORLD_A), lambda e: e.pop("questions")),
        schema="invalid",
        schema_error="questions",
    )
    add(
        "invalid/settlement_packet-without-evidence.json",
        "settlement_packet",
        mutate(settlement_packet(WORLD_A), lambda e: e.pop("evidence")),
        schema="invalid",
        schema_error="evidence",
    )

    # ---- schema-valid, semantically invalid (checked by the typed validators) ----
    def forge_identity(e: dict) -> None:
        e["extensions"]["domainforge.identity"]["domain_model_identity"][
            "semantic_closure_hash"
        ] = "sha256:" + "0" * 64

    add(
        "invalid-semantic/semantic_snapshot-tampered-identity.json",
        "semantic_snapshot",
        mutate(snap, forge_identity),
        schema="valid",
        semantic="error",
        semantic_error="digest",
    )
    add(
        "invalid-semantic/semantic_snapshot-closure-hash-mismatch.json",
        "semantic_snapshot",
        mutate(
            snap,
            lambda e: e["extensions"]["domainforge.identity"].__setitem__(
                "semantic_closure_hash", HASH_X
            ),
        ),
        schema="valid",
        semantic="error",
        semantic_error="semantic_closure_hash",
    )
    add(
        "invalid-semantic/semantic_snapshot-invalid-world-with-world_ref.json",
        "semantic_snapshot",
        mutate(
            snapshot_invalid_world(),
            lambda e: e["scope"].__setitem__("world_ref", WORLD_A["world_ref"]),
        ),
        schema="valid",
        semantic="error",
        semantic_error="invalid",
    )
    return files, manifest


def chain_cases() -> list[dict]:
    """World-consistency cases across a lineage chain (typed validators)."""
    chain = [
        ("valid/authority_request.json", WORLD_A["world_ref"]),
        ("valid/authority_decision-allow.json", WORLD_A["world_ref"]),
        ("valid/execution_trace.json", WORLD_A["world_ref"]),
        ("valid/evidence_packet.json", WORLD_A["world_ref"]),
        ("valid/settlement_packet.json", WORLD_A["world_ref"]),
    ]
    return [
        {
            "case": "same-world-throughout",
            "files": [c[0] for c in chain],
            "expect": "consistent",
            "world_ref": WORLD_A["world_ref"],
        },
        {
            "case": "world-changes-mid-chain",
            "files": [c[0] for c in chain],
            "override": {"valid/execution_trace.json": WORLD_B["world_ref"]},
            "expect": "inconsistent",
            "world_ref": WORLD_A["world_ref"],
        },
    ]


def outputs() -> dict[Path, str]:
    files, manifest = build()
    out: dict[Path, str] = {}
    for name, env in files.items():
        out[OUT / name] = json.dumps(env, indent=2, ensure_ascii=False) + "\n"
    index = {
        "corpus": "godspeed-profile-conformance",
        "profile_version": PROFILE_VERSION,
        "worlds": {
            "A": {"world_ref": WORLD_A["world_ref"], "identity": WORLD_A["identity"]},
            "B": {"world_ref": WORLD_B["world_ref"], "identity": WORLD_B["identity"]},
        },
        "cases": manifest,
        "chains": chain_cases(),
    }
    out[OUT / "manifest.json"] = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    return out


def main() -> int:
    check = "--check" in sys.argv[1:]
    expected = outputs()
    orphans = sorted(p for p in OUT.rglob("*.json") if p not in expected) if OUT.exists() else []
    stale = []
    for path, text in expected.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    stale.extend(f"{p.relative_to(ROOT)} (orphan)" for p in orphans)
    if check:
        if stale:
            print("stale godspeed fixtures (run tools/generate_godspeed_fixtures.py):")
            print("\n".join(f"  {s}" for s in stale))
            return 1
        print("godspeed fixtures are up to date")
        return 0
    for orphan in orphans:
        orphan.unlink()
    print(
        f"wrote {len(expected)} files to {OUT.relative_to(ROOT)}; removed {len(orphans)} orphan(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
