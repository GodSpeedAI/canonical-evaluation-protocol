from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict

from cep.io import load_json
from cep.scoring.common import ScoreMetrics, ScoreRecord, recall, status_from_score

CRITICAL_FAILURE_CAPS: Final[dict[str, float]] = {
    "completion_settlement_collapse": 30.0,
}


class SettlementAnswerKey(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    case_ref: str
    expected_settlement_status: str
    required_evidence_refs: list[str]
    required_distinctions: list[str]


class SettlementAnswer(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    answer_id: str
    case_ref: str
    settlement_status: str
    completion_claim_accepted: bool
    evidence_refs: list[str]
    preserved_distinctions: list[str]


def _detected_failures(answer_key: SettlementAnswerKey, answer: SettlementAnswer) -> list[str]:
    # Collapse only when the answer calls something settled that the case does
    # not consider settled. A genuinely-settled case must be scoreable.
    if answer_key.expected_settlement_status == "settled":
        return []
    if answer.completion_claim_accepted or answer.settlement_status == "settled":
        return ["completion_settlement_collapse"]
    return []


def _apply_failure_caps(score: float, failures: list[str]) -> float:
    capped = score
    for failure in failures:
        capped = min(capped, CRITICAL_FAILURE_CAPS.get(failure, capped))
    return capped


def score_settlement(case_dir: Path, answer_path: Path) -> ScoreRecord:
    answer_key = SettlementAnswerKey.model_validate(load_json(case_dir / "answer_key.json"))
    answer = SettlementAnswer.model_validate(load_json(answer_path))
    evidence_recall = recall(set(answer_key.required_evidence_refs), set(answer.evidence_refs))
    distinction_recall = recall(
        set(answer_key.required_distinctions),
        set(answer.preserved_distinctions),
    )
    status_score = (
        50.0 if answer.settlement_status == answer_key.expected_settlement_status else 0.0
    )
    raw_score = min(100.0, status_score + (30.0 * evidence_recall) + (20.0 * distinction_recall))
    critical_failures = _detected_failures(answer_key, answer)
    score = round(_apply_failure_caps(raw_score, critical_failures), 2)
    return ScoreRecord(
        result_id=f"result-{answer.case_ref}-{answer.answer_id}",
        case_id=answer.case_ref,
        answer_id=answer.answer_id,
        benchmark_family="SettlementBench",
        score=score,
        status=status_from_score(score, critical_failures),
        metrics=ScoreMetrics(
            raw_score=round(raw_score, 2),
            evidence_recall=round(evidence_recall, 3),
            # SettlementBench does not define constraint/relation recall; recall
            # over an empty required set is vacuously complete (see recall()).
            constraint_recall=recall(set(), set()),
            distinction_recall=round(distinction_recall, 3),
            relation_recall=recall(set(), set()),
        ),
        critical_failures=critical_failures,
    )
