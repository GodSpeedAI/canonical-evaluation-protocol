---
type: "CEP Documentation Map"
id: "cep-documentation-map"
title: "Canonical Evaluation Protocol Documentation Map"
description: "Comprehensive registry of all documentation pages, audience needs, Diátaxis classifications, prerequisites, and relationships."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - documentation
  - map
  - diataxis
timestamp: "2026-06-27T00:00:00Z"
---

# Canonical Evaluation Protocol: Documentation Map

This document catalogs every documentation page in the repository, defining its purpose, audience need, Diátaxis quadrant, prerequisites, and cross-references.

---

## Documentation System Structure

The documentation system combines Diátaxis with progressive-depth layers:
* **Orientation & Mental Model** (Layers 0 & 1)
* **Architecture & Subsystems** (Layers 2 & 3)
* **Workflows and Traces** (Layer 4)
* **Explanation & Design** (Layer 5)
* **Tutorials** (Layer 6)
* **How-To Guides** (Layer 7)
* **Technical Reference** (Layer 8)
* **Troubleshooting**

---

## Page Registry

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/index.md](docs/index.md) | Documentation Home | Orientation | Quick mental model, initial concepts, navigation by reader intent. | None | [README.md](README.md), [docs/mental-model.md](docs/mental-model.md) |
| [docs/getting-started.md](docs/getting-started.md) | Getting Started | Tutorial / Guide | Rapid environment verification, installation, and first test run. | None | [docs/running-benchmarks.md](docs/running-benchmarks.md) |
| [docs/mental-model.md](docs/mental-model.md) | System Mental Model | Explanation | Conceptual understanding of transformations, settlement, and anti-collapse. | [docs/index.md](docs/index.md) | [architecture.md](architecture.md), [spec/CEP-0000-derivation-ladder.md](spec/CEP-0000-derivation-ladder.md) |
| [architecture.md](architecture.md) | Architecture Overview | Architecture / Reference | Deep architectural specification, multi-view diagrams, and source trails. | [docs/mental-model.md](docs/mental-model.md) | [source-map.md](source-map.md), [docs/subsystems/schema-and-validation.md](docs/subsystems/schema-and-validation.md) |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Troubleshooting Guide | How-To / Reference | Diagnosing errors, understanding score caps, and recovering from failures. | None | [docs/reference/cli.md](docs/reference/cli.md), [docs/reference/anti-collapse-codes.md](docs/reference/anti-collapse-codes.md) |

### Subsystem Guides

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/subsystems/schema-and-validation.md](docs/subsystems/schema-and-validation.md) | Schema & Validation | Explanation / Reference | Understanding JSON Schema Draft 2020-12 profiling and corpus validation. | [architecture.md](architecture.md) | [docs/reference/schemas.md](docs/reference/schemas.md) |
| [docs/subsystems/anti-collapse-and-conformance.md](docs/subsystems/anti-collapse-and-conformance.md) | Anti-Collapse & Conformance | Explanation / Reference | How content-based collapse detection operates across fixtures and external corpora. | [architecture.md](architecture.md) | [docs/reference/anti-collapse-codes.md](docs/reference/anti-collapse-codes.md) |
| [docs/subsystems/benchmark-suites.md](docs/subsystems/benchmark-suites.md) | Benchmark Suites & Scoring | Explanation / Reference | Mathematical formulation of recall, partial credit, and failure caps. | [architecture.md](architecture.md) | [docs/reference/scoring-metrics.md](docs/reference/scoring-metrics.md) |
| [docs/subsystems/ledger-and-external.md](docs/subsystems/ledger-and-external.md) | Ledger Exporter & Integration | Explanation / Reference | Live PostgreSQL ingestion, causation joining, and week-over-week ratchets. | [architecture.md](architecture.md) | [docs/settlement-call-surface.md](docs/settlement-call-surface.md) |
| [docs/subsystems/cli-and-reporting.md](docs/subsystems/cli-and-reporting.md) | CLI & Reporting | Explanation / Reference | Command dispatch, path resolution, case discovery, and report models. | [architecture.md](architecture.md) | [docs/reference/cli.md](docs/reference/cli.md) |

### Workflows and Execution Traces

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/workflows/startup-and-discovery.md](docs/workflows/startup-and-discovery.md) | Startup & Discovery | Reference (Trace) | Trace of environment initialization, path discovery, and inventory enumeration. | [docs/getting-started.md](docs/getting-started.md) | [docs/subsystems/cli-and-reporting.md](docs/subsystems/cli-and-reporting.md) |
| [docs/workflows/reality-gap-evaluation.md](docs/workflows/reality-gap-evaluation.md) | RealityGap Evaluation | Reference (Trace) | Step-by-step trace of candidate answer scoring and collapse detection. | [docs/mental-model.md](docs/mental-model.md) | [docs/subsystems/benchmark-suites.md](docs/subsystems/benchmark-suites.md) |
| [docs/workflows/conformance-verification.md](docs/workflows/conformance-verification.md) | Conformance Verification | Reference (Trace) | Execution sequence for engine self-defense against negative fixtures. | [architecture.md](architecture.md) | [docs/subsystems/anti-collapse-and-conformance.md](docs/subsystems/anti-collapse-and-conformance.md) |
| [docs/workflows/external-corpus-evaluation.md](docs/workflows/external-corpus-evaluation.md) | External Corpus Evaluation | Reference (Trace) | Trace of third-party evaluation record adaptation and independent evaluation. | [architecture.md](architecture.md) | [docs/how-to/evaluate-external-corpus.md](docs/how-to/evaluate-external-corpus.md) |
| [docs/workflows/ledger-export-and-ratchet.md](docs/workflows/ledger-export-and-ratchet.md) | Ledger Export & Ratchet | Reference (Trace) | Trace of PostgreSQL extraction, causation matching, and ratchet enforcement. | [architecture.md](architecture.md) | [docs/how-to/export-and-ratchet-ledger.md](docs/how-to/export-and-ratchet-ledger.md) |

### Explanation and Design Rationale

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/explanation/preventing-semantic-collapse.md](docs/explanation/preventing-semantic-collapse.md) | Preventing Semantic Collapse | Explanation | Theoretical derivation ladder and why conventional benchmarks fail. | [docs/mental-model.md](docs/mental-model.md) | [spec/CEP-0000-derivation-ladder.md](spec/CEP-0000-derivation-ladder.md) |
| [docs/explanation/content-based-detection-rationale.md](docs/explanation/content-based-detection-rationale.md) | Content-Based Detection Rationale | Explanation | Architectural rationale behind audit finding F-01 and deterministic heuristics. | [architecture.md](architecture.md) | [docs/subsystems/anti-collapse-and-conformance.md](docs/subsystems/anti-collapse-and-conformance.md) |
| [docs/explanation/scoring-and-failure-caps.md](docs/explanation/scoring-and-failure-caps.md) | Scoring & Failure Caps Rationale | Explanation | Mathematical defense of asymmetric caps, vacuous recall, and 84.0 ceiling. | [docs/mental-model.md](docs/mental-model.md) | [docs/reference/scoring-metrics.md](docs/reference/scoring-metrics.md) |
| [docs/explanation/integration-and-ratchet-design.md](docs/explanation/integration-and-ratchet-design.md) | Integration & Ratchet Design | Explanation | Rationale for decoupling protocol schemas from producer event stores. | [architecture.md](architecture.md) | [docs/subsystems/ledger-and-external.md](docs/subsystems/ledger-and-external.md) |

### Tutorials

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/tutorials/first-reality-gap-evaluation.md](docs/tutorials/first-reality-gap-evaluation.md) | Scoring First RealityGap Answer | Tutorial | Guided hands-on experience scoring valid and invalid candidate answers. | [docs/getting-started.md](docs/getting-started.md) | [docs/workflows/reality-gap-evaluation.md](docs/workflows/reality-gap-evaluation.md) |
| [docs/tutorials/authoring-a-benchmark-case.md](docs/tutorials/authoring-a-benchmark-case.md) | Authoring a Benchmark Case | Tutorial | Guided tutorial for laying out, configuring, and verifying a new benchmark case. | [docs/getting-started.md](docs/getting-started.md) | [docs/authoring-cases.md](docs/authoring-cases.md) |

### How-To Guides

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/how-to/evaluate-external-corpus.md](docs/how-to/evaluate-external-corpus.md) | Evaluate External Corpus | How-To | Submitting third-party `cep/anti-collapse-corpus@1` files for evaluation. | [docs/getting-started.md](docs/getting-started.md) | [docs/workflows/external-corpus-evaluation.md](docs/workflows/external-corpus-evaluation.md) |
| [docs/how-to/integrate-settlement-scoring.md](docs/how-to/integrate-settlement-scoring.md) | Integrate Settlement Scoring | How-To | Embedding synchronous settlement scoring in an external agent platform. | [docs/getting-started.md](docs/getting-started.md) | [docs/settlement-call-surface.md](docs/settlement-call-surface.md) |
| [docs/how-to/add-anti-collapse-rule.md](docs/how-to/add-anti-collapse-rule.md) | Add Anti-Collapse Rule | How-To | Adding a new collapse heuristic, score cap, and conformance test fixture. | [docs/getting-started.md](docs/getting-started.md) | [docs/reference/anti-collapse-codes.md](docs/reference/anti-collapse-codes.md) |
| [docs/how-to/export-and-ratchet-ledger.md](docs/how-to/export-and-ratchet-ledger.md) | Export & Ratchet Ledger | How-To | Running the PostgreSQL live exporter and verifying the regression ratchet. | [docs/getting-started.md](docs/getting-started.md) | [docs/subsystems/ledger-and-external.md](docs/subsystems/ledger-and-external.md) |
| [docs/authoring-cases.md](docs/authoring-cases.md) | Authoring Benchmark Cases Guide | How-To | Human review standards and authoring conventions for new cases. | [docs/getting-started.md](docs/getting-started.md) | [docs/tutorials/authoring-a-benchmark-case.md](docs/tutorials/authoring-a-benchmark-case.md) |
| [docs/running-benchmarks.md](docs/running-benchmarks.md) | Running the Benchmarks | How-To | Complete command reference for running benchmark families and reading outputs. | [docs/getting-started.md](docs/getting-started.md) | [docs/reference/cli.md](docs/reference/cli.md) |

### Technical Reference

| Page Path | Title | Diátaxis Quadrant | Target Audience Need | Prerequisites | Related Pages |
|---|---|---|---|---|---|
| [docs/reference/cli.md](docs/reference/cli.md) | CLI Reference | Reference | Exact syntax, options, exit codes, and examples for `cep` CLI. | None | [docs/subsystems/cli-and-reporting.md](docs/subsystems/cli-and-reporting.md) |
| [docs/reference/schemas.md](docs/reference/schemas.md) | JSON Schema Reference | Reference | Required fields, types, and constraints across all registered schemas. | None | [schemas/index.json](schemas/index.json) |
| [docs/reference/anti-collapse-codes.md](docs/reference/anti-collapse-codes.md) | Collapse Codes Reference | Reference | Complete dictionary of collapse error codes, trigger heuristics, and score caps. | None | [src/cep/detect.py](src/cep/detect.py) |
| [docs/reference/scoring-metrics.md](docs/reference/scoring-metrics.md) | Scoring Metrics Reference | Reference | Mathematical formulas, thresholds (`85.0`, `60.0`, `40.0`, `84.0`), and status matrix. | None | [src/cep/scoring/common.py](src/cep/scoring/common.py) |
| [docs/reference/repository-layout.md](docs/reference/repository-layout.md) | Repository Layout Reference | Reference | Directory hierarchy, file naming conventions, and discovery patterns. | None | [source-map.md](source-map.md) |
| [docs/settlement-call-surface.md](docs/settlement-call-surface.md) | Settlement Call Surface | Reference | Ingestion payload and schema contract for synchronous settlement scoring. | None | [docs/how-to/integrate-settlement-scoring.md](docs/how-to/integrate-settlement-scoring.md) |
| [docs/anti-collapse.md](docs/anti-collapse.md) | Anti-Collapse Reference | Reference | Protected distinctions, detector codes, and harness operation overview. | None | [docs/reference/anti-collapse-codes.md](docs/reference/anti-collapse-codes.md) |
