---
type: "CEP Guide"
id: "cep-open-questions"
title: "Open Questions"
description: "Unresolved design decisions and open questions in the Canonical Evaluation Protocol."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - design
  - open-questions
timestamp: "2026-06-26T14:13:47Z"
---

# Open Questions

## OQ-0001 — License
- **Question**: Should the repository use Apache-2.0, MIT, MPL-2.0, or another license?
- **Default**: Apache-2.0.
- **Impact**: Affects public reuse and compliance.

## OQ-0002 — Python-first or Rust-first Reference Implementation
- **Question**: Should the first reference implementation be Python-first, Rust-first, or both?
- **Default**: Python-first for speed, Rust later.
- **Impact**: Affects execution velocity.

## OQ-0003 — File Syntax
- **Question**: Should benchmark cases use JSON, YAML, Markdown+frontmatter, or custom `.cep` language?
- **Default**: JSON Schema first.
- **Impact**: Affects ergonomics.

## OQ-0004 — Public Benchmark Cases
- **Question**: Should initial RealityGapBench cases be synthetic only, anonymized real cases, or both?
- **Default**: Synthetic only for v0.
- **Impact**: Affects legal risk.

## OQ-0005 — Human Review Requirement
- **Question**: Should generated benchmark cases require human review before acceptance?
- **Default**: Yes.
- **Impact**: Affects benchmark quality.

## OQ-0006 — Specification Default Metadata Version
- **Question**: Several specifications listed version `0.1`. Should this be normalized to a standard semver `0.1.0` in the OKF frontmatter?
- **Default**: `0.1.0`
- **Impact**: Standardizes OKF metadata schema.

## OQ-0007 — Metadata Timestamps
- **Question**: The specifications and benchmarks do not contain creation or update timestamps. What timestamp should be used?
- **Default**: `2026-06-26T14:13:47Z` (the bootstrap timestamp of the repository).
- **Impact**: Provides auditability for standard knowledge bundles.

## OQ-0008 — Anti-collapse conformance design intent
- **Question**: Was the self-referential anti-collapse harness (fixtures declare their own `expected_validation.errors`; the engine is never run) a deliberate v0 placeholder, or an oversight? CEP-0010 requires behavioral enforcement.
- **Raised By**: Final Protocol Audit (F-01 / DEBT-0002), 2026-06-27.
- **Default**: Treat as a blocker to fix — drive fixtures through the real scorer/validator before claiming anti-collapse conformance publicly.
- **Impact**: Determines whether `cep conformance anti-collapse` is evidence of detection or only of fixture authoring.
- **Resolved (2026-06-27)**: Implemented as a real detector (`src/cep/detect.py`); the harness now scores `submitted_answer` content. No human decision needed.

## OQ-0009 — v1 flat contract has no top-level field for scope/boundary/completeness/omission status
- **Question**: CEP-0008 SS52 requires a minimally valid envelope to preserve `scope`, `boundary_record`, `completeness_status`, and `omission_status`. The v1 flat contract (`sea.agent.event.v1.json`) has no dedicated top-level field for any of these under `additionalProperties: false`; they can only be nested unenforced inside `payload` or `metadata`. Should v1 grow explicit top-level fields for these, or should CEP-0008 define an "opaque carrier" allowance for flat envelope profiles that don't expose them?
- **Raised By**: Plan `02-cep.md` Task 1 (schema conformance work), 2026-07-01. See `schemas/semantic-envelope.mapping.md` for the full mapping and gap detail.
- **Default**: Leave open; `semantic-envelope.schema.json` does not invent fields to close this gap.
- **Impact**: Determines whether v1 producers (e.g. agent-memory-ledger) need a schema migration, or whether CEP-0008's SS52 minimal-envelope requirement needs a flat-profile carve-out.
