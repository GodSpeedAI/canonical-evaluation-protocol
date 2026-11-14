---
type: CEP Profile Specification
id: GODSPEED-INTERACTION-EVENT-v1
title: GodSpeed Interaction Event Extension v1
description: The extension object carried at extensions["godspeed.interaction_event"] on an execution_trace envelope, with field table, error codes and fixtures.
status: Draft
version: 1.0.0
tags:
- cep
- profile
- extension
timestamp: '2026-11-13T00:00:00Z'
protocol: Canonical Evaluation Protocol
category: Profile
document_type: Profile Specification
depends_on:
- CEP-0008
- GODSPEED-PROFILES-v1
---

# GodSpeed Interaction Event Extension v1

An interaction event is one consequential interaction observed by an emitter, carried in `extensions["godspeed.interaction_event"]` on a [`godspeed.execution_trace`](./GODSPEED-PROFILES-v1.md) envelope (CEP-0008 §39: an extension adds, and never overrides, core semantics). The event is observation, not evidence of settlement: `outcome.status` is what the emitter saw, never what it inferred. `agent-event-v1` is not used.

Schema: [`schemas/extensions/godspeed.interaction_event.v1.json`](../../schemas/extensions/godspeed.interaction_event.v1.json). Digest manifest: `schemas/extensions/DIGESTS`; consumers vendor by digest and `tools/check_contract_digests.py` fails on drift. Hash rule: CEP-0008 §16.5. Source section column below refers to the GodSpeed FDE integration architecture (E), the document that fixes these fields.

## Fields

All objects are closed (`additionalProperties: false`). Types are JSON Schema types.

| Field | Type | Required | Meaning | E |
| --- | --- | --- | --- | --- |
| `world_ref` | string `world:<name>@sha256:<64hex>` | yes | model of the element | §5 |
| `semantic_ref` | string `namespace::name` | yes | declared element addressed | §5 |
| `declaration_key` | string `concept:<uuidv5>` | yes | derived and checked by the receiver, never trusted | §2, §5 |
| `actor.principal` | string | yes | authenticated principal | §5 |
| `actor.role` | string | yes | SOP role | §5 |
| `operation` | string | yes | declared or observed operation | §5 |
| `resource` | string | yes | resource acted on | §5 |
| `context.case_id` | string | yes | case anchor | §5 |
| `context.plan_item_id` | string | yes | case anchor | §5 |
| `context.episode_ref` | string `episode:<case_id>:<plan_item_id>:<n>@sha256:<64hex>` | when `kind` is `evaluated` | frozen reference | §2, §5 |
| `context.assignment_id` | string `assign:<caseId>:<stepId>:<n>:<k>` | if delegated | delegation instance | §2, §5 |
| `correlation` | object `{case_id, assignment_id?, episode_ref?, run_id?}` | yes | structured; never parsed from a string | §2, §5 |
| `causation_id` | string | if caused | record id of the cause in the owning system | §5 |
| `authority.decision_id` | string (a decision id, `not_required`, or `unknown`) | yes | verified against SEA-Forge at ingest | §5 |
| `expectation_ref` | string `question:...` or `threshold:...` | when `kind` is `evaluated` | RealityTrace question or threshold id | §5 |
| `outcome.status` | enum `succeeded`, `failed`, `denied`, `interrupted`, `unknown` | yes | observed, never inferred | §5 |
| `outcome.effect_refs` | string[] | no | effects observed | §5 |
| `evidence_refs` | string[] | no | evidence ids | §5 |
| `settlement_ref` | string | no | settlement events only | §5 |
| `source.system` | string | yes | owning system | §5 |
| `source.record_id` | string | yes | pointer to the untouched source record | §5 |
| `source.sequence` | integer >= 0 | yes | owning system's sequence; the ordering field | §5, §14 |
| `source.recorded_at` | RFC 3339 timestamp (pattern) | yes | emitter clock; informational only, never orders | §5 |
| `executor_provenance` | enum `program`, `live`, `injected_fault` | yes | provenance of the execution | §5 |
| `kind` | enum `evaluated`, `exploratory` | yes | whether the event belongs to an evaluated episode | §14 |
| `emitter.signature` | `{key_id, alg, sig}` | from WP-33 | workload-identity signature over the canonical extension (CEP-0008 §16.5) with `emitter` removed; absent before WP-33 | §5 |

## Error codes

Schema violations map to a stable code. The code is for consumers (RealityTrace ingest); the schema reports the keyword.

| Code | Rule broken | Keyword |
| --- | --- | --- |
| `IE_OUTCOME_STATUS` | `outcome.status` outside the five values | `enum` |
| `IE_EPISODE_REF_MISSING` | `kind` is `evaluated` and `context.episode_ref` absent | `required` (via `anyOf`) |
| `IE_EXPECTATION_REF_MISSING` | `kind` is `evaluated` and `expectation_ref` absent | `required` (via `anyOf`) |
| `IE_IDENTITY_MISSING` | `world_ref`, `semantic_ref` or `declaration_key` absent | `required` |
| `IE_IDENTITY_FORMAT` | `world_ref` not pinned, or `declaration_key` not a UUIDv5 concept id | `pattern` |
| `IE_SOURCE_MISSING` | `source.*` field absent | `required` |
| `IE_SEQUENCE` | `source.sequence` not a non-negative integer | `type`, `minimum` |
| `IE_CORRELATION_SHAPE` | `correlation` not a structured object | `type` |
| `IE_PROVENANCE` | `executor_provenance` or `kind` outside its enum | `enum` |
| `IE_ASSIGNMENT_ID` | `assignment_id` lacks the `:<n>:<k>` counters | `pattern` |
| `IE_SIGNATURE_SHAPE` | `emitter.signature` lacks `key_id`, `alg` or `sig` | `required` |
| `IE_UNKNOWN_FIELD` | field not in this table | `additionalProperties` |
| `IE_AUTHORITY_ID` | `authority.decision_id` empty | `minLength` |

Checks a schema cannot make (receiver obligations, owned by RealityTrace ingest): recompute `declaration_key` from `semantic_ref`; resolve `semantic_ref` against the pinned world; resolve `source.record_id` at the owning system; verify `authority.decision_id` at SEA-Forge; verify the signature. Their codes (`INGEST_REJECTED_IDENTITY`, and so on) belong to those packages.

## Choices where E is silent

- `kind` (`evaluated` | `exploratory`) is a required event field; E §14 says it is carried on events, and "evaluated: yes" in §5 needs a discriminator.
- `expectation_ref` is a single string with prefix `question:` or `threshold:`; E §5 types it `string`.
- `context.episode_ref` and `correlation.episode_ref` use one pattern; `case_id` and `plan_item_id` inside it contain no `:` or `@`.
- `emitter.signature.alg` is any non-empty string until WP-33 fixes the algorithm.
- `source.recorded_at` is checked by pattern, not `format`, because CEP's own validator does not implement `format`.

## Fixtures

`schemas/fixtures/interaction-event/valid/` (4) and `invalid/` (15), each invalid file named for the rule it breaks; `manifest.json` records the expected keyword. `tests/test_interaction_event_contract.py` checks them. CEP's own `cep.schema_value` validator has no `integer` type, so these fixtures are checked with the standard `jsonschema` library only (debt DEBT-IE-01 in `.agents/DEBT.md`).
