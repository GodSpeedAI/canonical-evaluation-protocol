---
type: "CEP Subsystem Guide"
id: "cep-subsystem-cli-reporting"
title: "CLI and Reporting Subsystem"
description: "Architecture, command layout, path discovery, inventory mechanics, and report formatting for the CEP CLI."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - subsystem
  - cli
  - reporting
  - inventory
timestamp: "2026-06-27T00:00:00Z"
---

# CLI and Reporting Subsystem

## 1. Purpose
The CLI and Reporting Subsystem provides the user-facing and machine-facing operational boundary for CEP. Built on [Typer](https://typer.tiangolo.com/) and [Rich](https://github.com/Textualize/rich), it handles command routing, portable repository root discovery, file inventory traversal, and serialization of standardized JSON result documents conforming to `schemas/benchmark-result.schema.json`.

---

## 2. Responsibilities and Non-Responsibilities

### Responsibilities
* **CLI Command Routing**: Exposing top-level commands (`doctor`, `score-settlement`) and sub-typer groups (`validate`, `conformance`, `run`).
* **Environment & Path Resolution**: Locating repository root dynamically via `CEP_REPO_ROOT`, CWD, or module parent markers.
* **Corpus Inventory Discovery**: Traversing benchmark case directories (`rg-*`, `auth-*`, `set-*`, `cap-*`), example answers, and fixtures without hardcoded registries.
* **Standardized JSON Reporting**: Translating internal `ScoreRecord` models into JSON documents validated against `schemas/benchmark-result.schema.json`.
* **Exit Code Management**: Returning exit code `0` on success and `1` on validation/scoring regression (e.g. invalid answers passing or valid answers failing).

### Non-Responsibilities
* **Scoring Rules**: Does not implement recall formulas or collapse detectors.
* **Database Access**: Does not execute SQL queries.

---

## 3. Position in the System

```text
               [User Terminal / CI Pipeline]
                             │
                             ▼
                    [cep.cli.app (Typer)]
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
[cep.cli.validate]   [cep.cli.conformance]   [cep.cli.run]
       │                     │                     │
       ▼                     ▼                     ▼
[cep.validation]     [cep.conformance]     [cep.benchmarks]
                             │                     │
                             └──────────┬──────────┘
                                        ▼
                                [cep.reports.write_report()]
                                        │
                                        ▼
                             [reports/<family>/*.result.json]
```

---

## 4. Command Hierarchy and Flags

```text
cep
├── --version
├── doctor
├── score-settlement --input <file>
├── validate
│   ├── schemas
│   ├── reality-gap-corpus
│   ├── semantic-envelope [--stdin | <file>]
│   └── all
├── conformance
│   └── anti-collapse [--corpus <file>]
└── run
    ├── reality-gap --case-dir <dir> --answer <file> [--out <file>]
    ├── reality-gap-corpus
    ├── authority-corpus
    ├── settlement-corpus
    └── capability-corpus
```

---

## 5. Portable Path Discovery (`cep.paths`)

CEP eliminates reliance on absolute paths or assuming the current working directory is the repository root:

```python
def _looks_like_repo_root(path: Path) -> bool:
    return (path / "schemas" / "index.json").is_file() and (path / "benchmarks").is_dir()

def _discover_repo_root() -> Path:
    configured = os.environ.get("CEP_REPO_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    for candidate in (Path.cwd(), *Path(__file__).resolve().parents):
        if _looks_like_repo_root(candidate):
            return candidate
    return Path.cwd().resolve()
```

---

## 6. Inventory Traversal (`cep.inventory`)

Benchmark cases are discovered via directory glob patterns rather than explicit registries:
* RealityGap: `benchmarks/reality-gap/cases/rg-*`
* Authority: `benchmarks/authority/cases/auth-*`
* Settlement: `benchmarks/settlement/cases/set-*`
* Capability: `benchmarks/capability/cases/cap-*`

Within each directory, the inventory subsystem discovers `case.cep.json`, `answer_key.json`, and all `example_*_answer.json` files.

---

## 7. Reporting Model (`cep.reports`)

Every evaluated answer produces a report document:
```json
{
  "result_id": "result-rg-0001-ans-rg-0001-valid-example",
  "case_id": "rg-0001",
  "answer_id": "ans-rg-0001-valid-example",
  "benchmark_family": "RealityGapBench",
  "score": 99.0,
  "status": "pass",
  "metrics": {
    "raw_score": 99.0,
    "evidence_recall": 1.0,
    "constraint_recall": 1.0,
    "distinction_recall": 1.0,
    "relation_recall": 1.0
  },
  "critical_failures": [],
  "warnings": [],
  "generated_at": "2026-06-27T10:38:00+00:00"
}
```

---

## 8. Source Trail

* [cli.py](../../src/cep/cli.py) — Typer command routing, CLI options, console printing
* [paths.py](../../src/cep/paths.py) — `REPO_ROOT`, `_discover_repo_root()`, directory constants
* [inventory.py](../../src/cep/inventory.py) — Case directory and fixture discovery iterators
* [reports.py](../../src/cep/reports.py) — `BenchmarkReport`, `write_report()`, `report_payload()`
* [tests/test_inventory.py](../../tests/test_inventory.py) — Inventory discovery tests
* [tests/test_reality_gap_reports.py](../../tests/test_reality_gap_reports.py) — Report format validation
