from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

ScoreStatus = Literal["pass", "partial", "fail", "invalid", "blocked"]
INVALID_FAILURE_THRESHOLD = 40
PASS_THRESHOLD = 85
PARTIAL_THRESHOLD = 60


class ScoreMetrics(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    raw_score: float = Field(ge=0, le=100)
    evidence_recall: float = Field(ge=0, le=1)
    constraint_recall: float = Field(ge=0, le=1)
    distinction_recall: float = Field(ge=0, le=1)
    relation_recall: float = Field(ge=0, le=1)


class ScoreRecord(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    result_id: str
    case_id: str
    answer_id: str
    benchmark_family: str
    score: float = Field(ge=0, le=100)
    status: ScoreStatus
    metrics: ScoreMetrics
    critical_failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def to_json(self) -> str:
        return self.model_dump_json()


def recall(expected: set[str], observed: set[str]) -> float:
    if not expected:
        return 1.0
    return len(expected & observed) / len(expected)


def status_from_score(score: float, critical_failures: list[str]) -> ScoreStatus:
    if critical_failures and score <= INVALID_FAILURE_THRESHOLD:
        return "invalid"
    if score >= PASS_THRESHOLD and not critical_failures:
        return "pass"
    if score >= PARTIAL_THRESHOLD and not critical_failures:
        return "partial"
    if score > 0:
        return "fail"
    return "invalid"
