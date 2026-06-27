"""Cross-family anti-collapse invariants.

RealityGapBench has dedicated anti-collapse fixtures (see anti_collapse.py).
The other three families assert the same protection through their reviewed
example answers: every `example_invalid_answer` encodes a semantic collapse
and MUST be caught as a critical failure, and every `example_valid_answer`
MUST score without one. This runs the real scorers, so a "PASS" reflects
engine behaviour, not a declared expectation.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from cep.benchmarks.authority import score_authority
from cep.benchmarks.capability import score_capability
from cep.benchmarks.settlement import score_settlement
from cep.inventory import (
    iter_authority_case_dirs,
    iter_capability_case_dirs,
    iter_settlement_case_dirs,
)
from cep.scoring.common import ScoreRecord

Scorer = Callable[[Path, Path], ScoreRecord]


class InvariantResult(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    family: str
    case_id: str
    ok: bool
    message: str


def _check_case(family: str, case_dir: Path, scorer: Scorer) -> list[InvariantResult]:
    results: list[InvariantResult] = []

    invalid = case_dir / "example_invalid_answer.json"
    if invalid.exists():
        record = scorer(case_dir, invalid)
        ok = bool(record.critical_failures) and record.status in {"invalid", "fail"}
        results.append(
            InvariantResult(
                family=family,
                case_id=f"{case_dir.name} invalid",
                ok=ok,
                message=f"status={record.status} critical_failures={record.critical_failures}",
            )
        )

    valid = case_dir / "example_valid_answer.json"
    if valid.exists():
        record = scorer(case_dir, valid)
        ok = not record.critical_failures and record.status in {"pass", "partial"}
        results.append(
            InvariantResult(
                family=family,
                case_id=f"{case_dir.name} valid",
                ok=ok,
                message=f"status={record.status} critical_failures={record.critical_failures}",
            )
        )

    return results


def run_benchmark_anti_collapse() -> list[InvariantResult]:
    families: list[tuple[str, list[Path], Scorer]] = [
        ("AuthorityBench", iter_authority_case_dirs(), score_authority),
        ("SettlementBench", iter_settlement_case_dirs(), score_settlement),
        ("CapabilityBench", iter_capability_case_dirs(), score_capability),
    ]
    results: list[InvariantResult] = []
    for family, case_dirs, scorer in families:
        for case_dir in case_dirs:
            results.extend(_check_case(family, case_dir, scorer))
    return results
