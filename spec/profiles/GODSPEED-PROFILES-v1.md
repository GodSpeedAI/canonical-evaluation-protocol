---
type: CEP Profile Specification
id: GODSPEED-PROFILES-v1
title: GodSpeed CEP-0008 Profiles v1
description: Six CEP-0008 envelope profiles and the world_ref scope pin used where meaning, authority, observation, evidence and settlement cross a GodSpeed subsystem boundary.
status: Draft
version: 1.0.0
tags:
- cep
- profile
- world_ref
timestamp: '2026-10-04T00:00:00Z'
protocol: Canonical Evaluation Protocol
category: Profile
document_type: Profile Specification
depends_on:
- CEP-0008
---

# GodSpeed CEP-0008 Profiles v1

These profiles are CEP-0008 §18 profiles. They add requirements to the full semantic-envelope schema and never new top-level fields. They do not change CEP meaning and do not replace any subsystem's native representation: a component keeps its own internal types and speaks these profiles only where meaning, authority, observation, evidence or settlement must survive a subsystem boundary. CEP is not the transport.

## 1. Declaration

An envelope claiming a profile MUST declare it at `extensions["cep.profile"]` with `profile_id` (`godspeed.<envelope_kind>`) and `profile_version` (`1.0.0`). A tool that assumes a profile the envelope does not declare is interpreting it invalidly (CEP-0008 §18.3).

## 2. world_ref

`scope.world_ref` pins exactly one immutable semantic-world revision. Every profile requires it, except a `semantic_snapshot` of an invalid world (§3).

- DomainForge owns the grammar and the identity: `world:<name>@sha256:<digest>`, where the digest is `DomainModelIdentity::canonical_digest()`. The authoritative definition is `docs/reference/sea-application-contract.md` §14.1 in DomainForge. The schema patterns in this repository mirror it and are pinned to DomainForge's golden vectors (`schemas/vendored/world_ref/`).
- `scope.world_alias` (`world:<name>`) is a mutable selector. It is informational only and MUST NOT be the only world reference on a durable or consequential record.
- `scope.world_label` is presentation only and is never identity.
- Historical `world_ref` values are never retargeted. Every envelope in one lineage stays in one pinned world unless an explicit world transition (§5) joins two worlds.
- An unknown or unverifiable `world_ref` at a protected boundary MUST fail closed or escalate. This is a receiver obligation; a schema cannot decide it.

## 3. Profiles

| Profile | Envelope kind | Added requirements |
| --- | --- | --- |
| `godspeed.semantic_snapshot` | `semantic_snapshot` | Valid world: `scope.world_ref`, `integrity`, `representations`, `references`, `provenance`, and `extensions["domainforge.identity"]` carrying the 11-field `domain_model_identity` and `semantic_closure_hash`. Invalid world: `completeness_status` is `invalid`, `omissions` are recorded, and no `world_ref` is carried. |
| `godspeed.authority_request` | `authority_request` | `transformations`, `authority` (each with `subject_actor_ref`), `references`, `provenance`; `extensions["godspeed.authority_request"]` with `operation_id` and `correlation_id`. |
| `godspeed.authority_decision` | `authority_decision` | `transformations`, `authority`, `provenance`; non-empty `lineage_refs` naming the request; `extensions["godspeed.authority_decision"]` with `decision`, `operation_id`, `request_ref`. |
| `godspeed.execution_trace` | `execution_trace` | `transformations`, `provenance`; non-empty `lineage_refs` naming the authority decision; `extensions["godspeed.execution_trace"]` with `operation_id`, `authority_decision_ref`, `correlation_id`. |
| `godspeed.evidence_packet` | `evidence_packet` | `evidence`, `questions`, `provenance`; non-empty `lineage_refs`; `extensions["godspeed.evidence_packet"]` with `operation_id`. |
| `godspeed.settlement_packet` | `settlement_packet` | `settlements`, `evidence`, `questions`, `provenance`; non-empty `lineage_refs`; `extensions["godspeed.settlement_packet"]` with `operation_id`. |

### 3.1 Authority dispositions

`decision` is one of `allow`, `deny`, `escalate`, `unknown`, `constrained_allow`, `boundary`, `degraded`. It is never a boolean.

- `constrained_allow` and `boundary` MUST carry at least one envelope `constraints` record and a `policy_basis`. A `boundary` decision is not an unrestricted allow.
- `degraded` MUST also carry `compensating_controls`. It keeps its controls and policy basis.

### 3.2 Distinctions this profile set preserves

An `execution_trace` is observation of what was done, not settlement. An `evidence_packet` is evidence relative to a question, not raw data and not settlement. Only a `settlement_packet` settles, and only from evidence. Authority is not capability: a decision permits one transformation and implies nothing about what the actor can do generally.

## 4. Checks a schema cannot make

Conforming validators MUST also check:

1. For a valid `semantic_snapshot`, the digest recomputed from `domain_model_identity` equals the digest in `scope.world_ref`, and `semantic_closure_hash` agrees across the identity, the extension and `integrity.semantic_hash`.
2. An invalid-world snapshot carries no `world_ref`.
3. The declared profile matches the envelope kind.
4. All envelopes of a lineage pin the same `world_ref` unless an explicit transition (§5) is present.

## 5. World transition

A world transition record moves work from `source_world_ref` to a different `target_world_ref`. It requires `transition_kind` (`semantic_change`, `source_edit_only`, `compiler_upgrade`, `migration`), `reason`, `compatibility` and `semantic_closure_equal`; it may reference a semantic diff, a migration, an authority decision and evidence. A transition is never implied by retargeting an alias. Source and target MUST differ. The schema is `schemas/profiles/godspeed/world-transition.v1.schema.json`; the envelope kind that carries it (`semantic_diff`) is profiled later.

## 6. Generated artifacts

Profile schemas are generated by `tools/generate_godspeed_profiles.py` and the conformance corpus by `tools/generate_godspeed_fixtures.py`; both have `--check` modes enforced by tests. The corpus under `schemas/fixtures/godspeed/` is shared by the Python, Rust and TypeScript validators.
