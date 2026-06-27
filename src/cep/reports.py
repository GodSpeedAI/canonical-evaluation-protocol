from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from cep.io import write_json
from cep.json_types import JsonObject
from cep.scoring.common import ScoreMetrics, ScoreRecord, ScoreStatus


class BenchmarkReport(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    result_id: str
    case_id: str
    answer_id: str
    benchmark_family: str
    score: float = Field(ge=0, le=100)
    status: ScoreStatus
    metrics: ScoreMetrics
    critical_failures: list[str]
    warnings: list[str]
    generated_at: str


def _metrics_payload(metrics: ScoreMetrics) -> JsonObject:
    return {
        "raw_score": metrics.raw_score,
        "evidence_recall": metrics.evidence_recall,
        "constraint_recall": metrics.constraint_recall,
        "distinction_recall": metrics.distinction_recall,
        "relation_recall": metrics.relation_recall,
    }


def _string_values(items: list[str]) -> list[JsonValue]:
    values: list[JsonValue] = []
    values.extend(items)
    return values


def _report_model(record: ScoreRecord) -> BenchmarkReport:
    return BenchmarkReport(
        result_id=record.result_id,
        case_id=record.case_id,
        answer_id=record.answer_id,
        benchmark_family=record.benchmark_family,
        score=record.score,
        status=record.status,
        metrics=record.metrics,
        critical_failures=record.critical_failures,
        warnings=record.warnings,
        generated_at=datetime.now(UTC).isoformat(),
    )


def report_payload(record: ScoreRecord) -> JsonObject:
    report = _report_model(record)
    return {
        "result_id": report.result_id,
        "case_id": report.case_id,
        "answer_id": report.answer_id,
        "benchmark_family": report.benchmark_family,
        "score": report.score,
        "status": report.status,
        "metrics": _metrics_payload(report.metrics),
        "critical_failures": _string_values(report.critical_failures),
        "warnings": _string_values(report.warnings),
        "generated_at": report.generated_at,
    }


def write_report(record: ScoreRecord, out_path: Path) -> None:
    write_json(out_path, report_payload(record))
