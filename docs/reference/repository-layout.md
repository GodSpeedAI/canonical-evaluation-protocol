---
type: "CEP Technical Reference"
id: "cep-reference-repo-layout"
title: "Repository Layout and Artifact Index"
description: "Precise anatomical reference of repository directories, file formats, naming conventions, and inventory rules."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - reference
  - repository
  - inventory
timestamp: "2026-06-27T00:00:00Z"
---

# Repository Layout and Artifact Index

This reference outlines the physical file layout of the Canonical Evaluation Protocol repository, naming patterns, and artifact conventions.

---

## Directory Anatomy

```text
cep/
├── architecture.md               # Canonical high-level architecture specification
├── documentation-map.md          # Comprehensive index and Diátaxis classification map
├── source-map.md                 # Concept and subsystem to source code symbol map
├── justfile                      # Command runner automation recipes
├── pyproject.toml                # Package configuration, CLI entry points, tool options
├── uv.lock                       # Deterministic dependency lockfile
├── README.md                     # Project introductory documentation
├── SPEC_INDEX.md                 # High-level specification index
├── ROADMAP.md                    # Roadmap and milestone tracking
├── index.md                      # OKF Bundle root index
│
├── benchmarks/                   # Executable benchmark family suites
│   ├── reality-gap/              # RealityGapBench definitions and cases
│   │   ├── BENCHMARK.md          # Normative family specification
│   │   └── cases/rg-*            # Case directories (rg-0001, rg-0002, ...)
│   ├── authority/                # AuthorityBench suite
│   │   ├── BENCHMARK.md
│   │   └── cases/auth-*          # Case directories (auth-0001, ...)
│   ├── settlement/               # SettlementBench suite
│   │   ├── BENCHMARK.md
│   │   └── cases/set-*           # Case directories (set-0001, ...)
│   └── capability/               # CapabilityBench suite
│       ├── BENCHMARK.md
│       └── cases/cap-*           # Case directories (cap-0001, ...)
│
├── conformance/                  # Conformance manifests and negative test fixtures
│   └── fixtures/anti-collapse/
│       └── reality-gap/
│           ├── manifest.json     # Official fixture expectation registry
│           └── rg-ac-*.json      # Content-grounded anti-collapse fixtures (10 total)
│
├── docs/                         # Layered technical documentation knowledge system
│   ├── index.md                  # Documentation home and intent navigation
│   ├── mental-model.md           # System mental model and ontological concepts
│   ├── troubleshooting.md        # Failure diagnosis and remediation guide
│   ├── subsystems/               # Subsystem architecture specifications
│   ├── workflows/                # End-to-end operational execution traces
│   ├── explanation/              # Deep theoretical and architectural design rationales
│   ├── tutorials/                # Learning-oriented guided tutorials
│   ├── how-to/                   # Task-oriented operational guides
│   └── reference/                # Precise API, CLI, and schema reference sheets
│
├── reports/                      # Git-ignored generated result documents
│   ├── reality-gap/*.result.json
│   ├── authority/*.result.json
│   ├── settlement/*.result.json
│   ├── capability/*.result.json
│   └── ledger/                   # Exported Postgres cases and aggregates
│
├── schemas/                      # JSON Schema Draft 2020-12 normative schemas
│   ├── index.json                # Schema registry
│   ├── *.schema.json             # Individual schema documents
│   └── fixtures/                 # Semantic envelope validation fixtures
│
├── spec/                         # Normative foundational specifications (CEP-0000 to CEP-0010)
│   ├── index.md
│   └── CEP-*.md
│
├── src/cep/                      # Python core package implementation
│   ├── __init__.py
│   ├── paths.py                  # Auto-discovery of REPO_ROOT
│   ├── json_types.py             # Type aliases and document errors
│   ├── io.py                     # Safe JSON loading and writing
│   ├── detect.py                 # Content-based anti-collapse detector
│   ├── schema_profile.py         # JSON Schema profile enforcement
│   ├── schema_value.py           # Instance validation engine
│   ├── validation.py             # Corpus and schema integrity validators
│   ├── inventory.py              # Dynamic case and fixture discovery
│   ├── reports.py                # Result serialization
│   ├── cli.py                    # Typer command-line interface
│   ├── benchmarks/               # Scorers for each benchmark family
│   ├── conformance/              # Fixture and invariant test harnesses
│   ├── exporters/                # External ledger integration (PostgreSQL)
│   └── scoring/                  # Common recall and status models
│
├── tests/                        # Comprehensive pytest test suite (67+ tests)
└── tools/
    └── validate_okf.py           # Open Knowledge Format markdown validator
```
