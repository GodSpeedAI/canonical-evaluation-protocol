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
