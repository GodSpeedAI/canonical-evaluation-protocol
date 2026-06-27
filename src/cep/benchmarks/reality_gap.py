from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict, Field

from cep.detect import (
    detect_reality_gap_collapses,
    reasoning_is_grounded,
    valid_evidence_ids,
)
from cep.io import load_json
from cep.scoring.common import ScoreMetrics, ScoreRecord, recall, status_from_score

# Every cap below is reachable: each key is a code that detect.py can emit.
CRITICAL_FAILURE_CAPS: Final[dict[str, float]] = {
    "declared_observed_collapse": 35.0,
    "claim_as_evidence": 35.0,
    "summary_source_collapse": 45.0,
    "unknown_as_false": 40.0,
    "missing_evidence_as_failure_proof": 40.0,
    "missing_evidence_as_no_gap": 35.0,
    "completion_settlement_collapse": 35.0,
    "ci_approval_collapse": 40.0,
    "possibility_affordance_collapse": 35.0,
    "authority_capability_collapse": 35.0,
    "score_capability_collapse": 45.0,
    "single_success_capability_collapse": 45.0,
    "opposite_answer_with_high_confidence": 35.0,
}

# An answer with correct labels but ungrounded reasoning cannot reach PASS.
UNGROUNDED_REASONING_CAP: Final[float] = 84.0


class PartialCreditRules(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    gap_status: dict[str, float] = Field(default_factory=dict)
    gap_type: dict[str, float] = Field(default_factory=dict)
    severity: dict[str, float] = Field(default_factory=dict)


class AnswerKey(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    case_ref: str
    accepted_gap_statuses: list[str]
    accepted_gap_types: list[str]
    accepted_severity_range: list[str]
    required_evidence_refs: list[str]
    required_affected_constraints: list[str]
    required_affected_distinctions: list[str]
    required_affected_relations: list[str]
    accepted_next_actions: list[str]
    partial_credit_rules: PartialCreditRules


class RecommendedNextAction(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    type: str


class Confidence(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    value: str


class RealityGapAnswer(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    answer_id: str
    case_ref: str
    gap_status: str
    gap_type: str
    severity: str
    gap_summary: str
    affected_constraints: list[str]
    affected_distinctions: list[str]
    affected_relations: list[str]
    evidence_refs: list[str]
    confidence: Confidence
    recommended_next_action: RecommendedNextAction


def _score_rule(rules: dict[str, float], observed: str, accepted: list[str]) -> float:
    if observed in accepted:
        return rules.get(observed, 0.0)
    return 0.0


def _next_action_score(answer_key: AnswerKey, answer: RealityGapAnswer) -> float:
    if answer.recommended_next_action.type in answer_key.accepted_next_actions:
        return 4.0
    return 0.0


def _apply_failure_caps(score: float, failures: list[str]) -> float:
    capped = score
    for failure in failures:
        capped = min(capped, CRITICAL_FAILURE_CAPS.get(failure, capped))
    return capped


def _load_answer_key(case_dir: Path) -> AnswerKey:
    return AnswerKey.model_validate(load_json(case_dir / "answer_key.json"))


def _load_answer(answer_path: Path) -> RealityGapAnswer:
    return RealityGapAnswer.model_validate(load_json(answer_path))


def score_reality_gap(case_dir: Path, answer_path: Path) -> ScoreRecord:
    answer_key = _load_answer_key(case_dir)
    answer = _load_answer(answer_path)
    raw_answer = load_json(answer_path)

    evidence_recall = recall(set(answer_key.required_evidence_refs), set(answer.evidence_refs))
    constraint_recall = recall(
        set(answer_key.required_affected_constraints),
        set(answer.affected_constraints),
    )
    distinction_recall = recall(
        set(answer_key.required_affected_distinctions),
        set(answer.affected_distinctions),
    )
    relation_recall = recall(
        set(answer_key.required_affected_relations),
        set(answer.affected_relations),
    )

    raw_score = min(
        100.0,
        _score_rule(
            answer_key.partial_credit_rules.gap_status,
            answer.gap_status,
            answer_key.accepted_gap_statuses,
        )
        + _score_rule(
            answer_key.partial_credit_rules.gap_type,
            answer.gap_type,
            answer_key.accepted_gap_types,
        )
        + _score_rule(
            answer_key.partial_credit_rules.severity,
            answer.severity,
            answer_key.accepted_severity_range,
        )
        + (20.0 * evidence_recall)
        + (10.0 * constraint_recall)
        + (10.0 * distinction_recall)
        + (10.0 * relation_recall)
        + _next_action_score(answer_key, answer),
    )
    critical_failures = detect_reality_gap_collapses(
        raw_answer,
        valid_evidence_ids(case_dir),
        answer_key.accepted_gap_statuses,
    )
    warnings: list[str] = []
    capped = _apply_failure_caps(raw_score, critical_failures)
    if not reasoning_is_grounded(raw_answer):
        warnings.append("ungrounded_reasoning")
        capped = min(capped, UNGROUNDED_REASONING_CAP)
    score = round(capped, 2)

    return ScoreRecord(
        result_id=f"result-{answer.case_ref}-{answer.answer_id}",
        case_id=answer.case_ref,
        answer_id=answer.answer_id,
        benchmark_family="RealityGapBench",
        score=score,
        status=status_from_score(score, critical_failures),
        metrics=ScoreMetrics(
            raw_score=round(raw_score, 2),
            evidence_recall=round(evidence_recall, 3),
            constraint_recall=round(constraint_recall, 3),
            distinction_recall=round(distinction_recall, 3),
            relation_recall=round(relation_recall, 3),
        ),
        critical_failures=critical_failures,
        warnings=warnings,
    )
