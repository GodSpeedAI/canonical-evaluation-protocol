from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict

from cep.io import load_json
from cep.scoring.common import ScoreMetrics, ScoreRecord, recall, status_from_score

CRITICAL_FAILURE_CAPS: Final[dict[str, float]] = {
    "score_capability_collapse": 35.0,
    "possibility_affordance_collapse": 35.0,
}


class CapabilityAnswerKey(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    case_ref: str
    expected_capability_status: str
    required_evidence_refs: list[str]
    required_distinctions: list[str]


class CapabilityAnswer(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    answer_id: str
    case_ref: str
    capability_status: str
    evidence_refs: list[str]
    preserved_distinctions: list[str]
    capability_claim_basis: list[str]


def _detected_failures(answer: CapabilityAnswer) -> list[str]:
    failures: set[str] = set()
    if (
        "score" in answer.capability_claim_basis
        or "one_time_success" in answer.capability_claim_basis
    ):
        failures.add("score_capability_collapse")
    if "possibility" in answer.capability_claim_basis:
        failures.add("possibility_affordance_collapse")
    return sorted(failures)


def _apply_failure_caps(score: float, failures: list[str]) -> float:
    capped = score
    for failure in failures:
        capped = min(capped, CRITICAL_FAILURE_CAPS.get(failure, capped))
    return capped


def score_capability(case_dir: Path, answer_path: Path) -> ScoreRecord:
    answer_key = CapabilityAnswerKey.model_validate(load_json(case_dir / "answer_key.json"))
    answer = CapabilityAnswer.model_validate(load_json(answer_path))
    evidence_recall = recall(set(answer_key.required_evidence_refs), set(answer.evidence_refs))
    distinction_recall = recall(
        set(answer_key.required_distinctions),
        set(answer.preserved_distinctions),
    )
    status_score = (
        50.0 if answer.capability_status == answer_key.expected_capability_status else 0.0
    )
    raw_score = min(100.0, status_score + (30.0 * evidence_recall) + (20.0 * distinction_recall))
    critical_failures = _detected_failures(answer)
    score = round(_apply_failure_caps(raw_score, critical_failures), 2)
    return ScoreRecord(
        result_id=f"result-{answer.case_ref}-{answer.answer_id}",
        case_id=answer.case_ref,
        answer_id=answer.answer_id,
        benchmark_family="CapabilityBench",
        score=score,
        status=status_from_score(score, critical_failures),
        metrics=ScoreMetrics(
            raw_score=round(raw_score, 2),
            evidence_recall=round(evidence_recall, 3),
            constraint_recall=1.0,
            distinction_recall=round(distinction_recall, 3),
            relation_recall=1.0,
        ),
        critical_failures=critical_failures,
    )
