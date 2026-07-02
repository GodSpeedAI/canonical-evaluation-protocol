from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict, Field

from cep.io import load_json
from cep.json_types import JsonObject
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
    return score_settlement_answer(answer_key, answer)


# Stable call surface for producers (e.g. godspeed_agent) scoring a settlement
# synchronously at `SettlementRecorded` time, without a benchmark case_dir on
# disk. Input/output contract: docs/settlement-call-surface.md.
def score_settlement_answer(
    answer_key: SettlementAnswerKey,
    answer: SettlementAnswer,
) -> ScoreRecord:
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


class ScoreSettlementInput(BaseModel):
    """Input document shape for `cep score-settlement --input <file>`; see
    docs/settlement-call-surface.md for the full contract."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    settlement_recorded: JsonObject
    expected: JsonObject
    evidence_refs: list[str] = Field(default_factory=list)
    preserved_distinctions: list[str] = Field(default_factory=list)


_OUTCOME_TO_SETTLEMENT_STATUS: Final[dict[str, str]] = {
    "usable": "settled",
    "partial": "partially_settled",
    "unusable": "unsettled",
}


def from_settlement_recorded(
    payload: JsonObject,
    *,
    evidence_refs: list[str] | None = None,
    preserved_distinctions: list[str] | None = None,
) -> SettlementAnswer:
    """Adapt a real `SettlementRecorded` event payload (godspeed_agent
    `agentic_capability_loop/adapters.py: emit_settlement_recorded`) into a
    `SettlementAnswer`. CEP owns this translation so producers never reshape
    their own event to match CEP's vocabulary.

    `outcome` ("usable" | "partial" | "unusable") maps to `settlement_status`
    ("settled" | "partially_settled" | "unsettled"); `completion_claim_accepted`
    is true only for "usable", since that's the only outcome the producer
    itself is claiming as a settled result. `evidence_refs` and
    `preserved_distinctions` aren't part of the raw event and must be
    supplied by the caller if required for scoring.
    """
    outcome = str(payload["outcome"])
    return SettlementAnswer(
        answer_id=str(payload["evidence_event_id"]),
        case_ref=str(payload["work_request_id"]),
        settlement_status=_OUTCOME_TO_SETTLEMENT_STATUS.get(outcome, "unknown"),
        completion_claim_accepted=outcome == "usable",
        evidence_refs=evidence_refs or [],
        preserved_distinctions=preserved_distinctions or [],
    )
