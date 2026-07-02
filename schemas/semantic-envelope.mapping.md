---
type: "CEP Guide"
id: "cep-semantic-envelope-mapping"
title: "Semantic Envelope Schema Mapping"
description: "Maps semantic-envelope.schema.json fields to CEP-0008 distinctions and documents the v1 field-set gap."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - schema
  - semantic-envelope
timestamp: "2026-07-01T00:00:00Z"
---

# Semantic Envelope Schema Mapping (CEP-0008 -> v1 flat contract)

`semantic-envelope.schema.json` is a JSON Schema profile of CEP-0008's
Semantic Envelope, scoped to what the v1 flat contract
(`sea.agent.event.v1.json`, durably enforced at agent-memory-ledger's
boundary) can actually carry. It reuses v1's field names — it does not
invent new ones. `$comment` isn't used because the reference implementation's
schema validator (`src/cep/schema_profile.py: SUPPORTED_SCHEMA_KEYS`) doesn't
support it; the mapping lives here instead.

| v1 field | CEP-0008 distinction |
|---|---|
| `schema_version` | `cep_version` / `envelope_version` (SS7.1) |
| `event_id` | `envelope_id` (SS7.1) |
| `idempotency_key` | `lineage_refs` (SS7.1) |
| `source` | `source_system_refs` (SS7.2) |
| `source_agent` | `created_by` (SS7.1) |
| `event_type` | `envelope_kind` (SS9) |
| `occurred_at` | `created_at` (SS7.1) |
| `correlation_id` | trace `envelope_refs` (SS45) |
| `causation_id` | trace `ordering_rule` (SS45) |
| `trace_id` | `trace_id` (SS45) |
| `payload` | opaque carrier for states/transformations/questions/claims/evidence/settlements (SS23-29) |
| `provenance.origin`, `provenance.chain` | SS15 Envelope Provenance Record (`provenance_id`, `source_envelope_refs`) |
| `metadata` | opaque carrier for boundary/completeness/omission/conformance status (SS8, SS10, SS34, SS38) |

## Delta from v1's own schema

`provenance` is `required` here even though v1 marks it optional. CEP-0008
SS15.2 treats an envelope without provenance as not settlement-valid, so this
profile enforces that MUST. Any real v1 instance that already populates
`provenance` (which agent-memory-ledger events do in practice) satisfies both
schemas unchanged.

## Open gap (not resolved here — see `.agents/OPEN_QUESTIONS.md` OQ-0009)

CEP-0008 SS52 requires a minimally valid envelope to preserve `scope`,
`boundary_record`, `completeness_status`, and `omission_status` as identifiable
concepts. The v1 flat contract has no dedicated top-level field for any of
these — they can only live unenforced inside the opaque `payload` or
`metadata` objects (both `type: object` with no `additionalProperties: false`
at that level, so nesting them there doesn't violate v1). This profile does
not add top-level fields for them, per this plan's guardrail against
inventing a compromise schema. Whether v1 should grow those fields, or
whether CEP-0008 should define an explicit "opaque carrier" allowance for
flat envelope profiles, is a cross-repo decision, not one made here.
