---
type: "CEP Source Map"
id: "cep-source-map"
title: "Canonical Evaluation Protocol Source Map"
description: "Direct mapping between architectural concepts, capabilities, subsystems, and concrete repository implementation files and code symbols."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - source-map
  - traceability
  - architecture
timestamp: "2026-06-27T00:00:00Z"
---

# Canonical Evaluation Protocol: Source Map

This document establishes concrete, bidirectional traceability between high-level architectural concepts, capabilities, specifications, and the exact files, modules, classes, and functions in the implementation.

---

## 1. Subsystem Implementation Map

| Subsystem | Primary Module | Key Classes & Functions | Test Coverage |
|---|---|---|---|
| **Path & Environment** | [src/cep/paths.py](src/cep/paths.py) | `REPO_ROOT`, `_discover_repo_root()`, `_looks_like_repo_root()` | [tests/test_import.py](tests/test_import.py) |
| **Document I/O & Types** | [src/cep/io.py](src/cep/io.py), [src/cep/json_types.py](src/cep/json_types.py) | `load_json()`, `write_json()`, `JsonObject`, `JsonObjectError` | [tests/test_import.py](tests/test_import.py) |
| **Schema Profiling** | [src/cep/schema_profile.py](src/cep/schema_profile.py) | `SchemaProfile`, `SUPPORTED_SCHEMA_KEYS`, `schema_profile_errors()` | [tests/test_validation.py](tests/test_validation.py) |
| **Schema Validation** | [src/cep/schema_value.py](src/cep/schema_value.py) | `validate_value()`, `validate_object()`, `_resolve_ref()` | [tests/test_validation.py](tests/test_validation.py) |
| **Corpus & Registry Validation** | [src/cep/validation.py](src/cep/validation.py) | `validate_schema_registry()`, `validate_all_schemas()`, `validate_reality_gap_corpus()` | [tests/test_validation.py](tests/test_validation.py) |
| **Anti-Collapse Detection** | [src/cep/detect.py](src/cep/detect.py) | `detect_reality_gap_collapses()`, `reasoning_is_grounded()`, `valid_evidence_ids()` | [tests/test_anti_collapse_conformance.py](tests/test_anti_collapse_conformance.py) |
| **Scoring Foundation** | [src/cep/scoring/common.py](src/cep/scoring/common.py) | `recall()`, `status_from_score()`, `ScoreMetrics`, `ScoreRecord` | [tests/test_reality_gap_scoring.py](tests/test_reality_gap_scoring.py) |
| **RealityGapBench** | [src/cep/benchmarks/reality_gap.py](src/cep/benchmarks/reality_gap.py) | `score_reality_gap()`, `CRITICAL_FAILURE_CAPS`, `AnswerKey`, `RealityGapAnswer` | [tests/test_reality_gap_scoring.py](tests/test_reality_gap_scoring.py) |
| **AuthorityBench** | [src/cep/benchmarks/authority.py](src/cep/benchmarks/authority.py) | `score_authority()`, `AuthorityAnswerKey`, `AuthorityAnswer` | [tests/test_authority_bench.py](tests/test_authority_bench.py) |
| **SettlementBench** | [src/cep/benchmarks/settlement.py](src/cep/benchmarks/settlement.py) | `score_settlement()`, `score_settlement_answer()`, `from_settlement_recorded()` | [tests/test_settlement_bench.py](tests/test_settlement_bench.py) |
| **CapabilityBench** | [src/cep/benchmarks/capability.py](src/cep/benchmarks/capability.py) | `score_capability()`, `CapabilityAnswerKey`, `CapabilityAnswer` | [tests/test_capability_bench.py](tests/test_capability_bench.py) |
| **Anti-Collapse Conformance** | [src/cep/conformance/anti_collapse.py](src/cep/conformance/anti_collapse.py) | `run_reality_gap_anti_collapse()`, `check_fixture()` | [tests/test_anti_collapse_conformance.py](tests/test_anti_collapse_conformance.py) |
| **Benchmark Invariants** | [src/cep/conformance/benchmark_invariants.py](src/cep/conformance/benchmark_invariants.py) | `run_benchmark_anti_collapse()`, `_check_case()` | [tests/test_benchmark_invariants.py](tests/test_benchmark_invariants.py) |
| **External Corpus Ingestion** | [src/cep/conformance/corpus.py](src/cep/conformance/corpus.py) | `load_corpus()`, `evaluate_corpus()`, `CorpusRecord`, `CorpusError` | [tests/test_anti_collapse_corpus.py](tests/test_anti_collapse_corpus.py) |
| **PostgreSQL Ledger Exporter** | [src/cep/exporters/ledger_postgres.py](src/cep/exporters/ledger_postgres.py) | `export_settlement_corpus()`, `ratchet_against()`, `ExportReport` | [tests/test_ledger_exporter.py](tests/test_ledger_exporter.py) |
| **Inventory & Discovery** | [src/cep/inventory.py](src/cep/inventory.py) | `iter_case_dirs()`, `iter_reality_gap_case_dirs()`, `iter_authority_case_dirs()` | [tests/test_inventory.py](tests/test_inventory.py) |
| **Reporting & Serialization** | [src/cep/reports.py](src/cep/reports.py) | `write_report()`, `report_payload()`, `BenchmarkReport` | [tests/test_reality_gap_reports.py](tests/test_reality_gap_reports.py) |
| **Command-Line Interface** | [src/cep/cli.py](src/cep/cli.py) | `app`, `doctor()`, `score_settlement_command()`, `run_app`, `validate_app` | [tests/test_import.py](tests/test_import.py) |

---

## 2. Normative Specifications to Code Implementation

| Specification | Core Concepts Defined | Source Code Realization |
|---|---|---|
| [spec/CEP-0000-derivation-ladder.md](spec/CEP-0000-derivation-ladder.md) | Derivation Ladder, Invariants | [src/cep/scoring/common.py](src/cep/scoring/common.py) (`ScoreMetrics` recall dimensions) |
| [spec/CEP-0001-ontology.md](spec/CEP-0001-ontology.md) | Ontology, Protected Distinctions | [src/cep/detect.py](src/cep/detect.py) (`detect_reality_gap_collapses`) |
| [spec/CEP-0002-representation-model.md](spec/CEP-0002-representation-model.md) | Representation, Grounding | [src/cep/detect.py](src/cep/detect.py) (`reasoning_is_grounded`) |
| [spec/CEP-0003-state-model.md](spec/CEP-0003-state-model.md) | Declared vs Observed State | [schemas/reality-gap-case.schema.json](schemas/reality-gap-case.schema.json), [src/cep/detect.py](src/cep/detect.py) |
| [spec/CEP-0004-transformation-model.md](spec/CEP-0004-transformation-model.md) | Transformations, Actions | [src/cep/benchmarks/reality_gap.py](src/cep/benchmarks/reality_gap.py) (`gap_type`, `severity`) |
| [spec/CEP-0005-question-model.md](spec/CEP-0005-question-model.md) | Questions, Operational Probes | [schemas/reality-gap-case.schema.json](schemas/reality-gap-case.schema.json) (`primary_question`) |
| [spec/CEP-0006-evidence-model.md](spec/CEP-0006-evidence-model.md) | Evidence Records, Causation Binding | [schemas/reality-gap-evidence.schema.json](schemas/reality-gap-evidence.schema.json), [src/cep/validation.py](src/cep/validation.py) |
| [spec/CEP-0007-settlement-model.md](spec/CEP-0007-settlement-model.md) | Settlement, Consequence Registration | [src/cep/benchmarks/settlement.py](src/cep/benchmarks/settlement.py) (`score_settlement_answer`) |
| [spec/CEP-0008-semantic-envelope.md](spec/CEP-0008-semantic-envelope.md) | Semantic Envelope Transport Format | [schemas/cep-semantic-envelope.schema.json](schemas/cep-semantic-envelope.schema.json), [src/cep/validation.py](src/cep/validation.py) |
| [spec/CEP-0009-benchmark-model.md](spec/CEP-0009-benchmark-model.md) | Benchmark Families, Cases, Scorers | [src/cep/benchmarks/](src/cep/benchmarks/) (`reality_gap`, `authority`, `settlement`, `capability`) |
| [spec/CEP-0010-conformance.md](spec/CEP-0010-conformance.md) | Conformance Levels, L2 Gate, Manifests | [src/cep/conformance/anti_collapse.py](src/cep/conformance/anti_collapse.py), [src/cep/conformance/corpus.py](src/cep/conformance/corpus.py) |

---

## 3. CLI Command Execution Map

| CLI Command | Function Entry Point in `src/cep/cli.py` | Dispatched Engine Functions | Output Location |
|---|---|---|---|
| `cep doctor` | `doctor()` | `validate_all_schemas()` | stdout |
| `cep validate schemas` | `validate_schemas_command()` | `validate_schema_registry(SCHEMAS_DIR / "index.json")` | stdout |
| `cep validate reality-gap-corpus` | `validate_reality_gap_corpus_command()` | `validate_reality_gap_corpus()` | stdout |
| `cep validate semantic-envelope` | `validate_semantic_envelope_command()` | `validate_semantic_envelope_corpus()`, `validate_instance()` | stdout |
| `cep validate all` | `validate_all_command()` | Aggregates all schema and corpus validation functions | stdout |
| `cep conformance anti-collapse` | `conformance_anti_collapse_command()` | `run_reality_gap_anti_collapse()`, `run_benchmark_anti_collapse()` | stdout |
| `cep conformance anti-collapse --corpus <file>` | `conformance_anti_collapse_command()` | `evaluate_corpus()` in `cep.conformance.corpus` | stdout |
| `cep run reality-gap` | `run_reality_gap_command()` | `score_reality_gap()`, `write_report()` | `reports/reality-gap/*.result.json` |
| `cep run reality-gap-corpus` | `run_reality_gap_corpus_command()` | `_run_corpus()`, `score_reality_gap()` | `reports/reality-gap/*.result.json` |
| `cep run authority-corpus` | `run_authority_corpus_command()` | `_run_corpus()`, `score_authority()` | `reports/authority/*.result.json` |
| `cep run settlement-corpus` | `run_settlement_corpus_command()` | `_run_corpus()`, `score_settlement()` | `reports/settlement/*.result.json` |
| `cep run capability-corpus` | `run_capability_corpus_command()` | `_run_corpus()`, `score_capability()` | `reports/capability/*.result.json` |
| `cep score-settlement` | `score_settlement_command()` | `from_settlement_recorded()`, `score_settlement_answer()` | stdout |
