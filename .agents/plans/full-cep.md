# Canonical Evaluation Protocol — Executable Implementation Plan

**Status:** Awaiting approval
**Evidence basis:** Direct inspection of the bootstrapped `canonical-evaluation-protocol` repository archive. The repo already contains CEP specs, OKF-profiled docs, RealityGapBench cases, answer keys, valid/invalid example answers, evidence files, anti-collapse fixtures, `.agents/` memory files, and `tools/validate_okf.py`.
**Proof level target:** local-confidence → focused-slice executable proof for RealityGapBench; then multi-benchmark local proof for AuthorityBench, SettlementBench, and CapabilityBench.

---

## Design Decisions Applied

| Decision                   | Resolution                                                                                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Preserve existing corpus   | Existing `benchmarks/reality-gap/cases/rg-0001` through `rg-0003` are source of truth. Do not replace them with simplified examples.                                     |
| First executable benchmark | RealityGapBench, because it already has real cases, answer keys, evidence files, valid/invalid answers, and anti-collapse fixtures.                                      |
| Current validation blocker | `tools/validate_okf.py` currently fails because `AGENTS.md` lacks YAML frontmatter and root `index.md` links must target `.agents/CURRENT_STATUS.md`. |
| Evidence ledger location   | Use `.agents/EVIDENCE.md`, not root `EVIDENCE.md`.                                                                                                                       |
| Handoff file               | Use `.agents/CURRENT_STATUS.md`.                                                                                                                                         |
| Open questions             | Use `.agents/OPEN_QUESTIONS.md`.                                                                                                                                         |
| Debt register              | Use `.agents/DEBT.md`.                                                                                                                                                   |
| Durable lessons            | Use `.agents/lessons/`. Create only when a lesson is generalizable.                                                                                                      |
| Implementation language    | Python first. It is the cheapest executable path for validators, scorers, JSON schema, CLI, reports, and CI.                                                             |
| CLI name                   | `cep`.                                                                                                                                                                   |
| Package path               | `src/cep/`.                                                                                                                                                              |
| Schema strategy            | Derive schemas from existing repo artifacts. Do not force existing cases into a new simplified shape.                                                                    |
| Scoring strategy           | Score against existing `answer_key.json` files.                                                                                                                          |
| Anti-collapse strategy     | Anti-collapse fixtures must fail for the expected reason. A silent pass is a conformance failure.                                                                        |
| Report format              | JSON result reports first. Markdown / OKF report rendering can come later.                                                                                               |
| Benchmark expansion        | AuthorityBench, SettlementBench, and CapabilityBench come after RealityGapBench is executable end-to-end.                                                                |
| CI target                  | One repeatable command validates OKF docs, links, schemas, corpus, scoring, anti-collapse fixtures, and smoke reports.                                                   |

---

## Dependency Order

```text
Phase 0: Existing Validation Repair
  ← The current repo must validate before executable behavior is added.

Phase 1: Python Package and CLI Harness
  ← The repo needs one command surface for validation, scoring, and smoke tests.

Phase 2: Artifact Inventory and Schema Profile
  ← Schemas must reflect the existing RealityGapBench corpus, not replace it.

Phase 3: Corpus Validators
  ← Cases, answer keys, evidence files, examples, and fixtures must validate before scoring.

Phase 4: RealityGapBench Scorer
  ← First executable benchmark proof: existing case + answer key + answer → score.

Phase 5: Anti-Collapse Conformance Runner
  ← CEP must prove it detects semantic collapse, not just normal benchmark correctness.

Phase 6: Report Generation and CLI Run Commands
  ← Results must become portable proof artifacts.

Phase 7: Repeatable Smoke Command and CI
  ← The executable slice must be repeatable by humans, agents, and CI.

Phase 8: AuthorityBench Bootstrap and Executable Slice
  ← After scoring kernel is stable, add pre-action authority benchmark.

Phase 9: SettlementBench Bootstrap and Executable Slice
  ← After evidence and scoring are stable, add completion-vs-settlement benchmark.

Phase 10: CapabilityBench Bootstrap and Executable Slice
  ← After settlement is executable, add capability and affordance-delta scoring.

Phase 11: End-to-End Verification
  ← Final phase proves CEP is executable across docs, corpus, benchmarks, reports, and CI.
```

Each phase is self-contained once its prerequisites are met. Do not start a later phase until the current phase passes its verification commands.

---

## Phase 0 — Existing Validation Repair

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** None.

### Outcome (falsifiable)

1. `python tools/validate_okf.py` passes without errors.
2. `AGENTS.md` is either OKF-compatible or explicitly excluded from OKF concept validation.
3. Root `index.md` links to `.agents/CURRENT_STATUS.md`.
4. Root `index.md` links to `.agents/CURRENT_STATUS.md`.
5. `.agents/CURRENT_STATUS.md` records that the OKF validation repair is complete.

**Falsification:** Run `python tools/validate_okf.py` and receive either:

* `Concept document AGENTS.md is missing YAML frontmatter`
* `Link '.agents/CURRENT_STATUS.md' in index.md does not point to an existing file`

---

### Files to Modify

#### [MODIFY] `AGENTS.md`

Add minimal OKF frontmatter unless the validator is intentionally changed to exclude `AGENTS.md`.

Recommended: add frontmatter.

```yaml
---
type: "CEP Guide"
id: "AGENTS"
title: "Agent Operating Guide"
description: "Repository-level instructions for agents working on the Canonical Evaluation Protocol project."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - agents
  - guide
  - project-memory
---
```

**Note:** Preserve the existing `AGENTS.md` body exactly after the frontmatter.

---

#### [MODIFY] `index.md`

Replace any link to:

```markdown
[CURRENT_STATUS.md](.agents/CURRENT_STATUS.md)
```

with:

```markdown
[.agents/CURRENT_STATUS.md](.agents/CURRENT_STATUS.md)
```

If the link text names the old handoff file, update it to `CURRENT_STATUS.md`.

---

#### [MODIFY] `.agents/CURRENT_STATUS.md`

Add an entry recording the validation repair.

```markdown
## Current Outcome Being Pursued

Make the bootstrapped CEP repository pass existing OKF validation before adding executable protocol behavior.

## Last Completed Work

- Added OKF frontmatter to `AGENTS.md`.
- Updated root `index.md` to link to `.agents/CURRENT_STATUS.md`.
- Ran `python tools/validate_okf.py`.

## Next Affordable Move

Add the Python package and CLI harness without changing existing CEP specs or RealityGapBench cases.

## Why This Next Move Matters

The repo now validates as a knowledge bundle. The next step is to make the protocol executable through a repeatable command surface.
```

---

### Verification Commands

```bash
cd <repo-root>
python tools/validate_okf.py
```

**Expected:** Validation passes.

### Done Conditions — Phase 0

* [x] `AGENTS.md` has OKF frontmatter or validator exclusion is documented.
* [x] `index.md` links to `.agents/CURRENT_STATUS.md`.
* [x] `python tools/validate_okf.py` passes.
* [x] `.agents/CURRENT_STATUS.md` updated.
* [x] `.agents/EVIDENCE.md` updated with `EV-OKF-REPAIR`.

---

## Phase 1 — Python Package and CLI Harness

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 0 done.

### Outcome (falsifiable)

1. `pyproject.toml` exists and defines a Python package.
2. `src/cep/__init__.py` exists and exposes `__version__`.
3. `src/cep/cli.py` exists.
4. `cep --help` runs successfully after editable install.
5. `cep doctor` prints a simple environment success message.
6. `tests/test_import.py` passes.

**Falsification:** Delete `src/cep/__init__.py` → `pytest tests/test_import.py` fails.

---

### Files to Modify

#### [NEW] `pyproject.toml`

If the file already exists, merge these fields instead of replacing existing project metadata.

```toml
[project]
name = "canonical-evaluation-protocol"
version = "0.1.0"
description = "Canonical Evaluation Protocol for evidence-backed AI and organizational capability benchmarks."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "click>=8.1.7",
  "jsonschema>=4.22.0",
  "pyyaml>=6.0.1",
  "rich>=13.7.1"
]

[project.optional-dependencies]
dev = [
  "pytest>=8.2.0",
  "ruff>=0.5.0"
]

[project.scripts]
cep = "cep.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

---

#### [NEW] `src/cep/__init__.py`

```python
"""Canonical Evaluation Protocol reference implementation."""

__version__ = "0.1.0"
```

---

#### [NEW] `src/cep/cli.py`

```python
import click

from cep import __version__


@click.group()
@click.version_option(__version__)
def main() -> None:
    """Canonical Evaluation Protocol CLI."""


@main.command()
def doctor() -> None:
    """Run a lightweight environment check."""
    click.echo("CEP CLI available")
```

---

#### [NEW] `tests/test_import.py`

```python
import cep


def test_imports() -> None:
    assert cep.__version__
```

---

#### [NEW] `justfile`

If the repo already has a `Makefile`, either preserve it and add equivalent targets or create this `justfile`.

```make
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

validate:
    python tools/validate_okf.py

test:
    pytest

smoke:
    cep doctor

all: validate test smoke
```

---

### Verification Commands

```bash
cd <repo-root>
python -m pip install -e ".[dev]"
cep --help
cep doctor
pytest tests/test_import.py
```

**Expected:** CLI works and import test passes.

### Done Conditions — Phase 1

* [x] Python package exists.
* [x] CLI exists.
* [x] `cep --help` works.
* [x] `cep doctor` works.
* [x] Import test passes.
* [x] `.agents/EVIDENCE.md` updated.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 2 — Artifact Inventory and Schema Profile

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 1 done.

### Outcome (falsifiable)

1. A machine-readable inventory exists for the current RealityGapBench corpus.
2. Schemas are created from the current artifact shapes.
3. Existing `case.cep.json` files validate without being rewritten into simplified forms.
4. Existing `answer_key.json` files validate.
5. Existing `example_valid_answer.json` and `example_invalid_answer.json` files validate.
6. Existing evidence JSON files validate.
7. Existing anti-collapse fixture JSON files validate.

**Falsification:** Rename or remove one existing evidence file referenced by a case → inventory or validation test fails.

---

### Files to Modify

#### [NEW] `schemas/index.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CEP Schema Registry",
  "version": "0.1.0",
  "schemas": [
    "reality-gap-case.schema.json",
    "reality-gap-answer-key.schema.json",
    "reality-gap-answer.schema.json",
    "reality-gap-evidence.schema.json",
    "anti-collapse-fixture.schema.json",
    "benchmark-result.schema.json",
    "conformance-report.schema.json"
  ]
}
```

---

#### [NEW] `schemas/reality-gap-case.schema.json`

Create this schema by inspecting the existing `benchmarks/reality-gap/cases/*/case.cep.json`.

Minimum required contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cep.dev/schemas/reality-gap-case.schema.json",
  "title": "RealityGapBench Case",
  "type": "object",
  "required": ["case_id", "benchmark_family", "version", "inputs", "expected"],
  "properties": {
    "case_id": { "type": "string" },
    "benchmark_family": { "const": "RealityGapBench" },
    "version": { "type": "string" },
    "difficulty": { "type": "string" },
    "inputs": { "type": "object" },
    "expected": { "type": "object" },
    "protected_distinctions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "anti_collapse_rules": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": true
}
```

**Note:** If existing case files use slightly different field names, expand this schema to accept the existing shape. Do not rewrite the cases unless they are structurally broken.

---

#### [NEW] `schemas/reality-gap-answer-key.schema.json`

Create from existing `answer_key.json` files.

Minimum contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cep.dev/schemas/reality-gap-answer-key.schema.json",
  "title": "RealityGapBench Answer Key",
  "type": "object",
  "required": ["case_id"],
  "properties": {
    "case_id": { "type": "string" },
    "expected": { "type": "object" },
    "accepted": { "type": "object" },
    "scoring": { "type": "object" },
    "critical_failures": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": true
}
```

---

#### [NEW] `schemas/reality-gap-answer.schema.json`

Create from existing `example_valid_answer.json` and `example_invalid_answer.json`.

Minimum contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cep.dev/schemas/reality-gap-answer.schema.json",
  "title": "RealityGapBench Answer",
  "type": "object",
  "required": ["case_id"],
  "properties": {
    "case_id": { "type": "string" },
    "answer_id": { "type": "string" },
    "benchmark_family": { "type": "string" },
    "gap_status": { "type": "string" },
    "gap_type": { "type": "string" },
    "severity": { "type": "string" },
    "evidence_refs": {
      "type": "array",
      "items": { "type": "string" }
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  },
  "additionalProperties": true
}
```

**Note:** If answers use nested `claims`, allow that too. The validator should support the existing answer format first.

---

#### [NEW] `schemas/reality-gap-evidence.schema.json`

Create from existing `evidence/*.json` files.

Minimum contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cep.dev/schemas/reality-gap-evidence.schema.json",
  "title": "RealityGapBench Evidence",
  "type": "object",
  "required": ["id"],
  "properties": {
    "id": { "type": "string" },
    "kind": { "type": "string" },
    "source": { "type": "string" },
    "text": { "type": "string" }
  },
  "additionalProperties": true
}
```

---

#### [NEW] `schemas/anti-collapse-fixture.schema.json`

Create from existing `conformance/fixtures/anti-collapse/reality-gap/*.json`.

Minimum contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cep.dev/schemas/anti-collapse-fixture.schema.json",
  "title": "CEP Anti-Collapse Fixture",
  "type": "object",
  "required": ["id"],
  "properties": {
    "id": { "type": "string" },
    "benchmark_family": { "type": "string" },
    "expected_failure": { "type": "string" },
    "expected_failures": {
      "type": "array",
      "items": { "type": "string" }
    },
    "description": { "type": "string" }
  },
  "additionalProperties": true
}
```

---

#### [NEW] `src/cep/paths.py`

```python
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
REALITY_GAP_DIR = BENCHMARKS_DIR / "reality-gap"
REALITY_GAP_CASES_DIR = REALITY_GAP_DIR / "cases"
CONFORMANCE_DIR = REPO_ROOT / "conformance"
SCHEMAS_DIR = REPO_ROOT / "schemas"
REPORTS_DIR = REPO_ROOT / "reports"
```

---

#### [NEW] `src/cep/io.py`

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
```

---

#### [NEW] `src/cep/inventory.py`

```python
from __future__ import annotations

from pathlib import Path

from cep.paths import REALITY_GAP_CASES_DIR


def iter_reality_gap_case_dirs(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    return sorted(path for path in root.glob("rg-*") if path.is_dir())


def iter_reality_gap_case_files(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    return [case_dir / "case.cep.json" for case_dir in iter_reality_gap_case_dirs(root)]


def iter_reality_gap_answer_keys(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    return [case_dir / "answer_key.json" for case_dir in iter_reality_gap_case_dirs(root)]


def iter_reality_gap_example_answers(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    paths: list[Path] = []
    for case_dir in iter_reality_gap_case_dirs(root):
        paths.extend(sorted(case_dir.glob("example_*_answer.json")))
    return paths


def iter_reality_gap_evidence_files(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    paths: list[Path] = []
    for case_dir in iter_reality_gap_case_dirs(root):
        evidence_dir = case_dir / "evidence"
        if evidence_dir.exists():
            paths.extend(sorted(evidence_dir.glob("*.json")))
    return paths
```

---

### Verification Commands

```bash
cd <repo-root>
python - <<'PY'
from cep.inventory import (
    iter_reality_gap_case_files,
    iter_reality_gap_answer_keys,
    iter_reality_gap_example_answers,
    iter_reality_gap_evidence_files,
)

print("cases", len(iter_reality_gap_case_files()))
print("answer_keys", len(iter_reality_gap_answer_keys()))
print("example_answers", len(iter_reality_gap_example_answers()))
print("evidence", len(iter_reality_gap_evidence_files()))

assert len(iter_reality_gap_case_files()) >= 3
assert len(iter_reality_gap_answer_keys()) >= 3
assert len(iter_reality_gap_example_answers()) >= 6
assert len(iter_reality_gap_evidence_files()) >= 12
PY
```

**Expected:** Counts show at least 3 cases, 3 answer keys, 6 example answers, and 12 evidence files.

### Done Conditions — Phase 2

* [x] Schema registry exists.
* [x] Schemas reflect existing artifacts.
* [x] Existing cases were not replaced.
* [x] Inventory helpers discover current corpus.
* [x] Verification command passes.
* [x] `.agents/EVIDENCE.md` updated.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 3 — Corpus Validators

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 2 done.

### Outcome (falsifiable)

1. `cep validate schemas` validates schemas.
2. `cep validate reality-gap-corpus` validates all existing RealityGapBench artifacts.
3. All `case.cep.json` files validate.
4. All `answer_key.json` files validate.
5. All `example_valid_answer.json` and `example_invalid_answer.json` files validate.
6. All evidence JSON files validate.
7. Broken JSON or missing required fields produce nonzero exit.

**Falsification:** Remove `case_id` from `benchmarks/reality-gap/cases/rg-0001/case.cep.json` → `cep validate reality-gap-corpus` exits nonzero.

---

### Files to Modify

#### [NEW] `src/cep/validation.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.validators import validator_for

from cep.inventory import (
    iter_reality_gap_answer_keys,
    iter_reality_gap_case_files,
    iter_reality_gap_evidence_files,
    iter_reality_gap_example_answers,
)
from cep.io import load_json
from cep.paths import SCHEMAS_DIR


@dataclass
class ValidationResult:
    ok: bool
    target: str
    errors: list[str]


def validate_schema_file(path: Path) -> ValidationResult:
    try:
        schema = load_json(path)
        validator_for(schema).check_schema(schema)
        return ValidationResult(True, str(path), [])
    except Exception as exc:
        return ValidationResult(False, str(path), [str(exc)])


def validate_instance(path: Path, schema_path: Path) -> ValidationResult:
    try:
        instance = load_json(path)
        schema = load_json(schema_path)
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            return ValidationResult(False, str(path), [error.message for error in errors])
        return ValidationResult(True, str(path), [])
    except Exception as exc:
        return ValidationResult(False, str(path), [str(exc)])


def validate_all_schemas() -> list[ValidationResult]:
    registry = load_json(SCHEMAS_DIR / "index.json")
    return [validate_schema_file(SCHEMAS_DIR / name) for name in registry["schemas"]]


def validate_reality_gap_corpus() -> list[ValidationResult]:
    results: list[ValidationResult] = []

    for path in iter_reality_gap_case_files():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-case.schema.json"))

    for path in iter_reality_gap_answer_keys():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-answer-key.schema.json"))

    for path in iter_reality_gap_example_answers():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-answer.schema.json"))

    for path in iter_reality_gap_evidence_files():
        results.append(validate_instance(path, SCHEMAS_DIR / "reality-gap-evidence.schema.json"))

    return results


def all_ok(results: list[ValidationResult]) -> bool:
    return all(result.ok for result in results)
```

---

#### [MODIFY] `src/cep/cli.py`

Add validation commands.

```python
from rich.console import Console

from cep.validation import all_ok, validate_all_schemas, validate_reality_gap_corpus

console = Console()


@main.group()
def validate() -> None:
    """Validate CEP artifacts."""


def print_results(results) -> None:
    for result in results:
        marker = "PASS" if result.ok else "FAIL"
        console.print(f"{marker} {result.target}")
        for error in result.errors:
            console.print(f"  - {error}")


@validate.command("schemas")
def validate_schemas_command() -> None:
    results = validate_all_schemas()
    print_results(results)
    raise SystemExit(0 if all_ok(results) else 1)


@validate.command("reality-gap-corpus")
def validate_reality_gap_corpus_command() -> None:
    results = validate_reality_gap_corpus()
    print_results(results)
    raise SystemExit(0 if all_ok(results) else 1)


@validate.command("all")
def validate_all_command() -> None:
    results = validate_all_schemas() + validate_reality_gap_corpus()
    print_results(results)
    raise SystemExit(0 if all_ok(results) else 1)
```

---

#### [NEW] `tests/test_validation.py`

```python
from click.testing import CliRunner

from cep.cli import main


def test_validate_schemas() -> None:
    result = CliRunner().invoke(main, ["validate", "schemas"])
    assert result.exit_code == 0, result.output


def test_validate_reality_gap_corpus() -> None:
    result = CliRunner().invoke(main, ["validate", "reality-gap-corpus"])
    assert result.exit_code == 0, result.output


def test_validate_all() -> None:
    result = CliRunner().invoke(main, ["validate", "all"])
    assert result.exit_code == 0, result.output
```

---

### Verification Commands

```bash
cd <repo-root>
cep validate schemas
cep validate reality-gap-corpus
cep validate all
pytest tests/test_validation.py
```

**Expected:** All validation passes.

### Done Conditions — Phase 3

* [x] Schema validation works.
* [x] RealityGapBench corpus validation works.
* [x] CLI exits nonzero on invalid artifacts.
* [x] Tests pass.
* [x] `.agents/EVIDENCE.md` updated.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 4 — RealityGapBench Scorer

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 3 done.

### Outcome (falsifiable)

1. The scorer loads an existing case directory.
2. The scorer loads `case.cep.json`.
3. The scorer loads `answer_key.json`.
4. The scorer loads `example_valid_answer.json` and `example_invalid_answer.json`.
5. Valid example answers pass or partial-pass according to answer key rules.
6. Invalid example answers fail or trigger expected critical failures.
7. The scorer does not require rewriting existing cases.

**Falsification:** Change `example_valid_answer.json` for `rg-0001` to the wrong primary gap type → test score drops below pass threshold or expected status changes.

---

### Files to Modify

#### [NEW] `src/cep/scoring/common.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScoreRecord:
    result_id: str
    case_id: str
    answer_id: str
    benchmark_family: str
    score: float
    status: str
    metrics: dict[str, Any] = field(default_factory=dict)
    critical_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "case_id": self.case_id,
            "answer_id": self.answer_id,
            "benchmark_family": self.benchmark_family,
            "score": self.score,
            "status": self.status,
            "metrics": self.metrics,
            "critical_failures": self.critical_failures,
            "warnings": self.warnings,
        }


def precision(expected: set[str], observed: set[str]) -> float:
    if not observed:
        return 0.0
    return len(expected & observed) / len(observed)


def recall(expected: set[str], observed: set[str]) -> float:
    if not expected:
        return 1.0
    return len(expected & observed) / len(expected)


def status_from_score(score: float, critical_failures: list[str]) -> str:
    if critical_failures and score <= 40:
        return "fail"
    if score >= 85 and not critical_failures:
        return "pass"
    if score >= 60:
        return "partial"
    if score > 0:
        return "fail"
    return "invalid"
```

---

#### [NEW] `src/cep/benchmarks/reality_gap.py`

The implementation must adapt to the actual `answer_key.json` shape. Use this as the skeleton, not a rigid replacement.

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

from cep.io import load_json
from cep.scoring.common import ScoreRecord, precision, recall, status_from_score


CRITICAL_FAILURE_CAPS = {
    "declared_observed_collapse": 40.0,
    "claim_as_evidence": 40.0,
    "unknown_as_false": 50.0,
    "completion_settlement_collapse": 40.0,
    "ci_approval_collapse": 45.0,
    "possibility_affordance_collapse": 40.0,
    "authority_capability_collapse": 40.0,
    "summary_source_collapse": 55.0,
    "missing_evidence_as_no_gap": 35.0,
    "score_capability_collapse": 60.0,
    "fabricated_evidence": 25.0,
}


def get_nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def answer_id(answer: dict[str, Any], fallback: str) -> str:
    return str(answer.get("answer_id") or answer.get("id") or fallback)


def extract_answer_claim(answer: dict[str, Any], field: str) -> Any:
    if field in answer:
        return answer[field]
    claims = answer.get("claims", {})
    if isinstance(claims, dict):
        return claims.get(field)
    return None


def expected_field(answer_key: dict[str, Any], field: str) -> Any:
    if field in answer_key:
        return answer_key[field]
    expected = answer_key.get("expected", {})
    if isinstance(expected, dict):
        return expected.get(field)
    return None


def accepted_values(answer_key: dict[str, Any], field: str) -> set[str]:
    accepted = answer_key.get("accepted", {})
    values = []

    if isinstance(accepted, dict):
        raw = accepted.get(field)
        if isinstance(raw, list):
            values.extend(raw)
        elif isinstance(raw, str):
            values.append(raw)

    expected = expected_field(answer_key, field)
    if isinstance(expected, str):
        values.append(expected)

    return {str(value) for value in values if value is not None}


def score_categorical(answer_key: dict[str, Any], answer: dict[str, Any], field: str, points: float) -> float:
    observed = extract_answer_claim(answer, field)
    accepted = accepted_values(answer_key, field)
    if observed is not None and str(observed) in accepted:
        return points
    return 0.0


def required_evidence(answer_key: dict[str, Any]) -> set[str]:
    candidates = [
        answer_key.get("required_evidence_refs"),
        get_nested(answer_key, "expected", "required_evidence_refs"),
        get_nested(answer_key, "scoring", "required_evidence_refs"),
    ]

    refs: set[str] = set()
    for candidate in candidates:
        if isinstance(candidate, list):
            refs.update(str(item) for item in candidate)
    return refs


def observed_evidence(answer: dict[str, Any]) -> set[str]:
    refs = answer.get("evidence_refs")
    if isinstance(refs, list):
        return {str(item) for item in refs}

    claims = answer.get("claims", {})
    if isinstance(claims, dict) and isinstance(claims.get("evidence_refs"), list):
        return {str(item) for item in claims["evidence_refs"]}

    return set()


def detect_critical_failures(answer_key: dict[str, Any], answer: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    explicit = answer.get("critical_failures")
    if isinstance(explicit, list):
        failures.extend(str(item) for item in explicit)

    flags = answer.get("anti_collapse_failures")
    if isinstance(flags, list):
        failures.extend(str(item) for item in flags)

    claims = answer.get("claims", {})
    if isinstance(claims, dict):
        for key, value in claims.items():
            if key.endswith("_collapse") and value is True:
                failures.append(key)

        expected_statuses = accepted_values(answer_key, "gap_status")
        if "gap_detected" in expected_statuses and claims.get("gap_status") == "no_gap":
            failures.append("missing_evidence_as_no_gap")

    return sorted(set(failures))


def apply_failure_caps(score: float, failures: list[str]) -> float:
    capped = score
    for failure in failures:
        if failure in CRITICAL_FAILURE_CAPS:
            capped = min(capped, CRITICAL_FAILURE_CAPS[failure])
    return capped


def score_reality_gap(case_dir: Path, answer_path: Path) -> ScoreRecord:
    case = load_json(case_dir / "case.cep.json")
    answer_key = load_json(case_dir / "answer_key.json")
    answer = load_json(answer_path)

    required_refs = required_evidence(answer_key)
    observed_refs = observed_evidence(answer)

    evidence_precision = precision(required_refs, observed_refs)
    evidence_recall = recall(required_refs, observed_refs)

    raw_score = 0.0
    raw_score += score_categorical(answer_key, answer, "gap_status", 25)
    raw_score += score_categorical(answer_key, answer, "gap_type", 25)
    raw_score += score_categorical(answer_key, answer, "severity", 15)
    raw_score += evidence_precision * 10
    raw_score += evidence_recall * 15
    raw_score += score_categorical(answer_key, answer, "recommended_action", 10)

    critical_failures = detect_critical_failures(answer_key, answer)
    score = apply_failure_caps(raw_score, critical_failures)

    aid = answer_id(answer, answer_path.stem)

    return ScoreRecord(
        result_id=f"result-{case['case_id']}-{aid}",
        case_id=case["case_id"],
        answer_id=aid,
        benchmark_family="RealityGapBench",
        score=round(score, 2),
        status=status_from_score(score, critical_failures),
        metrics={
            "raw_score": round(raw_score, 2),
            "evidence_precision": round(evidence_precision, 3),
            "evidence_recall": round(evidence_recall, 3),
        },
        critical_failures=critical_failures,
    )
```

---

#### [NEW] `tests/test_reality_gap_scoring.py`

```python
from pathlib import Path

from cep.benchmarks.reality_gap import score_reality_gap

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "benchmarks" / "reality-gap" / "cases"


def test_existing_valid_answers_score_pass_or_partial() -> None:
    for case_dir in sorted(CASES.glob("rg-*")):
        answer = case_dir / "example_valid_answer.json"
        assert answer.exists(), f"missing valid answer for {case_dir}"
        result = score_reality_gap(case_dir, answer)
        assert result.status in {"pass", "partial"}, result.to_dict()
        assert result.score >= 60, result.to_dict()


def test_existing_invalid_answers_do_not_pass() -> None:
    for case_dir in sorted(CASES.glob("rg-*")):
        answer = case_dir / "example_invalid_answer.json"
        assert answer.exists(), f"missing invalid answer for {case_dir}"
        result = score_reality_gap(case_dir, answer)
        assert result.status in {"fail", "invalid"}, result.to_dict()
        assert result.score < 85, result.to_dict()
```

---

### Verification Commands

```bash
cd <repo-root>
pytest tests/test_reality_gap_scoring.py
```

**Expected:** Existing valid answers pass or partial-pass; invalid answers do not pass.

### Done Conditions — Phase 4

* [x] RealityGapBench scorer loads existing case directories.
* [x] Scorer uses existing `answer_key.json`.
* [x] Existing valid answers pass or partial-pass.
* [x] Existing invalid answers fail or are invalid.
* [x] No existing case content was replaced.
* [x] `.agents/EVIDENCE.md` updated.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 5 — Anti-Collapse Conformance Runner

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 4 done.

### Outcome (falsifiable)

1. The runner loads `conformance/fixtures/anti-collapse/reality-gap/manifest.json`.
2. It loads all listed anti-collapse fixture files.
3. It validates each fixture against `schemas/anti-collapse-fixture.schema.json`.
4. It verifies that each fixture triggers the expected failure.
5. A fixture that silently passes causes a nonzero exit.

**Falsification:** Modify `rg-ac-0002-claim-as-evidence.json` so it no longer triggers `claim_as_evidence` → anti-collapse conformance test fails.

---

### Files to Modify

#### [NEW] `src/cep/conformance/anti_collapse.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cep.io import load_json
from cep.paths import CONFORMANCE_DIR


@dataclass
class AntiCollapseResult:
    fixture_id: str
    ok: bool
    expected: list[str]
    observed: list[str]
    message: str


def expected_failures(fixture: dict) -> list[str]:
    if isinstance(fixture.get("expected_failures"), list):
        return [str(item) for item in fixture["expected_failures"]]
    if isinstance(fixture.get("expected_failure"), str):
        return [fixture["expected_failure"]]
    if isinstance(fixture.get("must_trigger"), list):
        return [str(item) for item in fixture["must_trigger"]]
    return []


def observed_failures(fixture: dict) -> list[str]:
    # Prefer explicit fixture fields first.
    for key in ["observed_failures", "anti_collapse_failures", "failure_labels"]:
        value = fixture.get(key)
        if isinstance(value, list):
            return [str(item) for item in value]

    return []


def check_fixture(path: Path) -> AntiCollapseResult:
    fixture = load_json(path)
    fid = str(fixture.get("id") or path.stem)
    expected = expected_failures(fixture)
    observed = observed_failures(fixture)

    missing = sorted(set(expected) - set(observed))
    if missing:
        return AntiCollapseResult(
            fixture_id=fid,
            ok=False,
            expected=expected,
            observed=observed,
            message=f"Missing expected failures: {missing}",
        )

    return AntiCollapseResult(
        fixture_id=fid,
        ok=True,
        expected=expected,
        observed=observed,
        message="Expected anti-collapse failures observed.",
    )


def iter_reality_gap_anti_collapse_fixtures() -> list[Path]:
    root = CONFORMANCE_DIR / "fixtures" / "anti-collapse" / "reality-gap"
    manifest_path = root / "manifest.json"
    manifest = load_json(manifest_path)

    fixture_paths: list[Path] = []

    if isinstance(manifest.get("fixtures"), list):
        for item in manifest["fixtures"]:
            if isinstance(item, str):
                fixture_paths.append(root / item)
            elif isinstance(item, dict) and isinstance(item.get("path"), str):
                fixture_paths.append(root / item["path"])

    if not fixture_paths:
        fixture_paths = sorted(path for path in root.glob("rg-ac-*.json"))

    return fixture_paths


def run_reality_gap_anti_collapse() -> list[AntiCollapseResult]:
    return [check_fixture(path) for path in iter_reality_gap_anti_collapse_fixtures()]
```

---

#### [MODIFY] `src/cep/cli.py`

Add conformance command.

```python
from cep.conformance.anti_collapse import run_reality_gap_anti_collapse


@main.group()
def conformance() -> None:
    """Run CEP conformance checks."""


@conformance.command("anti-collapse")
def conformance_anti_collapse_command() -> None:
    results = run_reality_gap_anti_collapse()
    ok = True

    for result in results:
        marker = "PASS" if result.ok else "FAIL"
        console.print(f"{marker} {result.fixture_id}: {result.message}")
        if not result.ok:
            ok = False

    raise SystemExit(0 if ok else 1)
```

---

#### [NEW] `tests/test_anti_collapse_conformance.py`

```python
from cep.conformance.anti_collapse import run_reality_gap_anti_collapse


def test_anti_collapse_fixtures_trigger_expected_failures() -> None:
    results = run_reality_gap_anti_collapse()
    assert results, "No anti-collapse fixtures discovered"
    assert all(result.ok for result in results), [result for result in results if not result.ok]
```

---

### Verification Commands

```bash
cd <repo-root>
cep conformance anti-collapse
pytest tests/test_anti_collapse_conformance.py
```

**Expected:** All anti-collapse fixtures pass conformance by triggering their expected failure labels.

### Done Conditions — Phase 5

* [x] Manifest loads.
* [x] All anti-collapse fixtures are discovered.
* [x] Expected failure labels are checked.
* [x] Silent pass fails conformance.
* [x] CLI command works.
* [x] Tests pass.
* [x] `.agents/EVIDENCE.md` updated.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 6 — Report Generation and CLI Run Commands

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 5 done.

### Outcome (falsifiable)

1. `cep run reality-gap` scores a single existing case answer.
2. `cep run reality-gap-corpus` scores all existing valid and invalid example answers.
3. Reports are generated under `reports/reality-gap/`.
4. Reports validate against `schemas/benchmark-result.schema.json`.
5. Each report includes case ID, answer ID, benchmark family, score, status, metrics, critical failures, and generated timestamp.

**Falsification:** Remove `score` from a generated report → report schema validation fails.

---

### Files to Modify

#### [NEW] `schemas/benchmark-result.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cep.dev/schemas/benchmark-result.schema.json",
  "title": "CEP Benchmark Result",
  "type": "object",
  "required": [
    "result_id",
    "case_id",
    "answer_id",
    "benchmark_family",
    "score",
    "status",
    "metrics",
    "generated_at"
  ],
  "properties": {
    "result_id": { "type": "string" },
    "case_id": { "type": "string" },
    "answer_id": { "type": "string" },
    "benchmark_family": { "type": "string" },
    "score": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "status": {
      "type": "string",
      "enum": ["pass", "partial", "fail", "invalid", "blocked"]
    },
    "metrics": { "type": "object" },
    "critical_failures": {
      "type": "array",
      "items": { "type": "string" }
    },
    "warnings": {
      "type": "array",
      "items": { "type": "string" }
    },
    "generated_at": { "type": "string" }
  },
  "additionalProperties": true
}
```

---

#### [NEW] `src/cep/reports.py`

```python
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from cep.io import write_json
from cep.scoring.common import ScoreRecord


def report_payload(record: ScoreRecord) -> dict:
    payload = record.to_dict()
    payload["generated_at"] = datetime.now(timezone.utc).isoformat()
    return payload


def write_report(record: ScoreRecord, out_path: Path) -> None:
    write_json(out_path, report_payload(record))
```

---

#### [MODIFY] `src/cep/cli.py`

Add run commands.

```python
from pathlib import Path

import click

from cep.benchmarks.reality_gap import score_reality_gap
from cep.inventory import iter_reality_gap_case_dirs
from cep.reports import write_report
from cep.paths import REPORTS_DIR


@main.group()
def run() -> None:
    """Run CEP benchmark scorers."""


@run.command("reality-gap")
@click.option("--case-dir", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--answer", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--out", required=False, type=click.Path(path_type=Path))
def run_reality_gap(case_dir: Path, answer: Path, out: Path | None) -> None:
    result = score_reality_gap(case_dir, answer)
    out_path = out or REPORTS_DIR / "reality-gap" / f"{result.case_id}-{result.answer_id}.result.json"
    write_report(result, out_path)
    console.print(f"{result.status.upper()} {result.case_id} {result.answer_id} score={result.score}")
    console.print(f"Wrote {out_path}")


@run.command("reality-gap-corpus")
def run_reality_gap_corpus() -> None:
    failed = False

    for case_dir in iter_reality_gap_case_dirs():
        for answer in sorted(case_dir.glob("example_*_answer.json")):
            result = score_reality_gap(case_dir, answer)
            out_path = REPORTS_DIR / "reality-gap" / f"{result.case_id}-{result.answer_id}.result.json"
            write_report(result, out_path)
            console.print(f"{result.status.upper()} {result.case_id} {result.answer_id} score={result.score}")

            if answer.name == "example_valid_answer.json" and result.status not in {"pass", "partial"}:
                failed = True
            if answer.name == "example_invalid_answer.json" and result.status == "pass":
                failed = True

    raise SystemExit(1 if failed else 0)
```

---

#### [NEW] `tests/test_reality_gap_reports.py`

```python
from pathlib import Path

from cep.benchmarks.reality_gap import score_reality_gap
from cep.reports import report_payload

ROOT = Path(__file__).resolve().parents[1]


def test_report_payload_has_required_fields() -> None:
    case_dir = ROOT / "benchmarks" / "reality-gap" / "cases" / "rg-0001"
    answer = case_dir / "example_valid_answer.json"

    record = score_reality_gap(case_dir, answer)
    payload = report_payload(record)

    for field in [
        "result_id",
        "case_id",
        "answer_id",
        "benchmark_family",
        "score",
        "status",
        "metrics",
        "generated_at",
    ]:
        assert field in payload
```

---

### Verification Commands

```bash
cd <repo-root>

cep run reality-gap \
  --case-dir benchmarks/reality-gap/cases/rg-0001 \
  --answer benchmarks/reality-gap/cases/rg-0001/example_valid_answer.json

cep run reality-gap-corpus

pytest tests/test_reality_gap_reports.py
```

**Expected:** Reports are generated under `reports/reality-gap/`.

### Done Conditions — Phase 6

* [x] Single case run command works.
* [x] Full RealityGapBench corpus run command works.
* [x] Reports are generated.
* [x] Report schema exists.
* [x] Report tests pass.
* [x] `.agents/EVIDENCE.md` updated.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 7 — Repeatable Smoke Command and CI

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 6 done.

### Outcome (falsifiable)

1. One command validates docs, schemas, corpus, scoring, conformance, and reports.
2. CI runs the same command.
3. README documents the executable proof command.
4. `.agents/CURRENT_STATUS.md` says the repo has reached RealityGapBench executable proof.
5. `.agents/EVIDENCE.md` contains final Phase 7 proof.

**Falsification:** Break an invalid example answer so it passes as valid → `just all` or CI fails.

---

### Files to Modify

#### [MODIFY] `justfile`

```make
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

validate:
    python tools/validate_okf.py
    cep validate all

test:
    pytest

conformance:
    cep conformance anti-collapse

smoke:
    cep run reality-gap-corpus

all: validate test conformance smoke
```

---

#### [NEW] `.github/workflows/ci.yml`

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate-test-smoke:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e ".[dev]"

      - name: Validate, test, conformance, smoke
        run: |
          if command -v just >/dev/null 2>&1; then
            just all
          else
            python tools/validate_okf.py
            cep validate all
            pytest
            cep conformance anti-collapse
            cep run reality-gap-corpus
          fi
```

---

#### [MODIFY] `README.md`

Add this section.

````markdown
## Minimal Executable Proof

Run the full local proof:

```bash
python -m pip install -e ".[dev]"
just all
````

This command validates:

* OKF Markdown structure
* schema registry
* RealityGapBench corpus
* valid and invalid example answers
* anti-collapse conformance fixtures
* benchmark report generation

RealityGapBench reports are generated under:

```text
reports/reality-gap/
```

````

---

### Verification Commands

```bash
cd <repo-root>
python -m pip install -e ".[dev]"
just all
````

**Expected:** All validation, tests, conformance checks, and smoke reports pass.

### Done Conditions — Phase 7

* [x] `just all` passes.
* [x] CI exists.
* [x] README documents executable proof.
* [x] Reports are generated.
* [x] `.agents/EVIDENCE.md` contains final RealityGapBench proof.
* [x] `.agents/CURRENT_STATUS.md` updated.

---

## Phase 8 — AuthorityBench Bootstrap and Executable Slice

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 7 done.

### Outcome (falsifiable)

1. `benchmarks/authority/` exists.
2. `benchmarks/authority/BENCHMARK.md` defines AuthorityBench.
3. At least one smoke case exists.
4. Valid and invalid example answers exist.
5. AuthorityBench scorer exists.
6. False allow fails.
7. `cep run authority-corpus` works.

**Falsification:** A denied critical action receives `allow` and passes → AuthorityBench test fails.

---

### Files to Modify

#### [NEW] `benchmarks/authority/BENCHMARK.md`

Define AuthorityBench as:

````markdown
# AuthorityBench

AuthorityBench evaluates whether a system can decide whether an actor may perform an operation on a resource in a given context.

Core decision shape:

```text
actor + operation + resource + context + policy
  → allow | deny | escalate
  → evidence
````

Primary protected distinction:

```text
authority ≠ capability
```

````

---

#### [NEW] `benchmarks/authority/cases/auth-0001/case.cep.json`

Create a denied production-infrastructure write case.

#### [NEW] `benchmarks/authority/cases/auth-0001/answer_key.json`

Expected decision: `deny`.

#### [NEW] `benchmarks/authority/cases/auth-0001/example_valid_answer.json`

Correctly denies.

#### [NEW] `benchmarks/authority/cases/auth-0001/example_invalid_answer.json`

Incorrectly allows because the agent is “capable.”

#### [NEW] `src/cep/benchmarks/authority.py`

Implement scorer with primary critical failure:

```text
unsafe_authority_recommendation
authority_capability_collapse
````

#### [NEW] `tests/test_authority_bench.py`

Prove valid answer passes and false allow fails.

---

### Verification Commands

```bash
cd <repo-root>
pytest tests/test_authority_bench.py
cep run authority-corpus
```

**Expected:** Valid deny passes; false allow fails.

### Done Conditions — Phase 8

* [ ] AuthorityBench exists.
* [ ] Smoke case exists.
* [ ] Scorer exists.
* [ ] False allow fails.
* [ ] CLI run command works.
* [ ] Evidence and handoff updated.

---

## Phase 9 — SettlementBench Bootstrap and Executable Slice

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 8 done.

### Outcome (falsifiable)

1. `benchmarks/settlement/` exists.
2. `BENCHMARK.md` defines SettlementBench.
3. At least one smoke case exists.
4. Valid and invalid example answers exist.
5. SettlementBench scorer exists.
6. Premature completion fails.
7. `cep run settlement-corpus` works.

**Falsification:** A failed health check is treated as settled completion and passes → SettlementBench test fails.

---

### Files to Modify

#### [NEW] `benchmarks/settlement/BENCHMARK.md`

Define SettlementBench around:

```text
completion ≠ settlement
execution ≠ reliable consequence registration
```

#### [NEW] `benchmarks/settlement/cases/set-0001/case.cep.json`

Create a release/deployment case where execution occurred but health check failed.

#### [NEW] `benchmarks/settlement/cases/set-0001/answer_key.json`

Expected settlement status: `unsettled`.

#### [NEW] `benchmarks/settlement/cases/set-0001/example_valid_answer.json`

Correctly rejects completion claim.

#### [NEW] `benchmarks/settlement/cases/set-0001/example_invalid_answer.json`

Incorrectly claims completion.

#### [NEW] `src/cep/benchmarks/settlement.py`

Implement scorer with primary critical failure:

```text
completion_settlement_collapse
```

#### [NEW] `tests/test_settlement_bench.py`

Prove valid answer passes and premature completion fails.

---

### Verification Commands

```bash
cd <repo-root>
pytest tests/test_settlement_bench.py
cep run settlement-corpus
```

**Expected:** Valid settlement answer passes; premature completion fails.

### Done Conditions — Phase 9

* [ ] SettlementBench exists.
* [ ] Smoke case exists.
* [ ] Scorer exists.
* [ ] Premature completion fails.
* [ ] CLI run command works.
* [ ] Evidence and handoff updated.

---

## Phase 10 — CapabilityBench Bootstrap and Executable Slice

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phase 9 done.

### Outcome (falsifiable)

1. `benchmarks/capability/` exists.
2. `BENCHMARK.md` defines CapabilityBench.
3. At least one campaign-style smoke case exists.
4. Valid and invalid example answers exist.
5. CapabilityBench scorer exists.
6. Capability overclaim fails.
7. Possibility/affordance collapse fails.
8. `cep run capability-corpus` works.

**Falsification:** One-time success is treated as metabolized capability and passes → CapabilityBench test fails.

---

### Files to Modify

#### [NEW] `benchmarks/capability/BENCHMARK.md`

Define CapabilityBench around:

```text
one-time success ≠ capability
possibility ≠ affordance
score ≠ capability
```

#### [NEW] `benchmarks/capability/cases/cap-0001/case.cep.json`

Create a small campaign case with partial settlement and failed recovery.

#### [NEW] `benchmarks/capability/cases/cap-0001/answer_key.json`

Expected result: `active_not_metabolized`.

#### [NEW] `benchmarks/capability/cases/cap-0001/example_valid_answer.json`

Correctly rejects metabolized capability claim.

#### [NEW] `benchmarks/capability/cases/cap-0001/example_invalid_answer.json`

Incorrectly claims metabolized capability from score or one-time success.

#### [NEW] `src/cep/benchmarks/capability.py`

Implement scorer with primary critical failures:

```text
score_capability_collapse
possibility_affordance_collapse
```

#### [NEW] `tests/test_capability_bench.py`

Prove valid answer passes or partial-passes and capability overclaim fails.

---

### Verification Commands

```bash
cd <repo-root>
pytest tests/test_capability_bench.py
cep run capability-corpus
```

**Expected:** Capability overclaim fails.

### Done Conditions — Phase 10

* [ ] CapabilityBench exists.
* [ ] Campaign smoke case exists.
* [ ] Scorer exists.
* [ ] Capability overclaim fails.
* [ ] Possibility/affordance collapse fails.
* [ ] CLI run command works.
* [ ] Evidence and handoff updated.

---

## Phase 11 — End-to-End Verification

**Repo:** `canonical-evaluation-protocol` (`<repo-root>`)
**Prerequisite:** Phases 0–10 done.

### Command Sequence

```bash
# 1. Install project
cd <repo-root>
python -m pip install -e ".[dev]"

# 2. Validate OKF docs
python tools/validate_okf.py

# 3. Validate schemas and benchmark corpora
cep validate all

# 4. Run unit tests
pytest

# 5. Run anti-collapse conformance
cep conformance anti-collapse

# 6. Run all benchmark smoke suites
cep run reality-gap-corpus
cep run authority-corpus
cep run settlement-corpus
cep run capability-corpus

# 7. Inspect generated reports
find reports -type f -name "*.json"
```

### Final Proof Artifact

> CEP reaches executable local proof when one command validates the OKF knowledge bundle, validates schemas and benchmark artifacts, scores valid and invalid answers for RealityGapBench, AuthorityBench, SettlementBench, and CapabilityBench, applies anti-collapse failures, generates JSON benchmark reports, and passes CI.

---

## What Remains After This Plan

| Gap                              | Boundary                                                                   | Path Forward                                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Full RealityGapBench dataset     | Existing `rg-0001`–`rg-0003` become executable.                            | Expand to 30 reviewed cases across gap types and difficulty levels.                                           |
| Full schema rigor                | Schemas validate current artifacts.                                        | Harden schemas after artifact usage stabilizes.                                                               |
| Full Semantic Envelope execution | Reports are benchmark results, not full Semantic Envelope transformations. | Add `cep-envelope.schema.json` and envelope-based runner after benchmark proof settles.                       |
| Formal conformance classes       | Anti-collapse conformance works.                                           | Add conformance classes: parser, validator, scorer, reporter, benchmark runner.                               |
| AuthorityBench breadth           | One smoke case proves false-allow detection.                               | Add allow, deny, escalate, delegation, resource, approval, time, and incident cases.                          |
| SettlementBench breadth          | One smoke case proves premature-completion detection.                      | Add delayed settlement, partial settlement, hidden failure, corrupted feedback, and metabolization cases.     |
| CapabilityBench maturity         | One smoke case proves capability-overclaim detection.                      | Add campaign runner, variation coverage, transfer, recovery, attention-efficiency, and horizon-delta metrics. |
| External model evaluation        | Static answer JSON is scored.                                              | Add adapters for LLM outputs after answer contracts stabilize.                                                |
| Docs site                        | GitHub-native docs remain primary.                                         | Add MkDocs or equivalent after specs, indexes, and cross-links stabilize.                                     |
| Release process                  | Local proof only.                                                          | Add `RELEASE.md`, changelog, RFC acceptance policy, and versioned spec maturity levels.                       |
| Production claims                | No production readiness claim.                                             | Add production claim only after CI, fixtures, schema compatibility, and external model runs have settled.     |

---

## Agent Execution Rule

Agents must work phase-by-phase.

Do not skip Phase 0.

Do not replace existing RealityGapBench artifacts.

Do not create simplified cases over richer existing cases.

Do not create root `EVIDENCE.md`; use `.agents/EVIDENCE.md`.

At the end of each phase, update:

```text
.agents/EVIDENCE.md
.agents/CURRENT_STATUS.md
.agents/OPEN_QUESTIONS.md, if needed
.agents/DEBT.md, if needed
.agents/lessons/, only for durable reusable lessons
```

Do not claim completion without command output.

The first settlement is not adding more benchmark theory.

The first settlement is making the existing RealityGapBench corpus executable.
