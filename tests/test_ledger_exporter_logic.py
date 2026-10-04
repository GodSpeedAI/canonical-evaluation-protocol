"""DB-free tests for the exporter's pure logic (aggregation, ratchet, JSON loading)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("psycopg", reason="psycopg not installed (cep[exporters])")

from cep.exporters.ledger_postgres import ExportReport, _loads, ratchet_against


def _report(results: list[dict]) -> ExportReport:
    return ExportReport(
        out_dir=Path(),
        case_count=len(results) + 1,
        scored=len(results),
        skipped_no_evidence=1,
        results=results,
    )


def test_aggregate_counts_scores_passes_failures_and_collapses() -> None:
    agg = _report(
        [
            {"score": 100, "status": "pass", "critical_failures": []},
            {
                "score": 40,
                "status": "fail",
                "critical_failures": ["completion_settlement_collapse"],
            },
            {"score": 0, "status": "invalid", "critical_failures": []},
        ]
    ).aggregate()
    assert agg["mean_score"] == pytest.approx(46.67)
    assert (agg["pass_count"], agg["fail_count"], agg["collapse_count"]) == (1, 2, 1)
    assert (agg["case_count"], agg["scored"], agg["skipped_no_evidence"]) == (4, 3, 1)


def test_aggregate_of_nothing_is_zero_not_an_error() -> None:
    agg = _report([]).aggregate()
    assert agg["mean_score"] == 0.0
    assert agg["collapse_count"] == 0


def _baseline(tmp_path: Path, mean: float) -> Path:
    path = tmp_path / "previous.json"
    path.write_text(json.dumps({"mean_score": mean}), encoding="utf-8")
    return path


def test_ratchet_has_no_threshold_without_a_baseline(tmp_path: Path) -> None:
    assert ratchet_against(tmp_path / "missing.json", _report([])) == 0


def test_ratchet_fails_on_regression_and_passes_when_not_worse(tmp_path: Path) -> None:
    good = _report([{"score": 90, "status": "pass", "critical_failures": []}])
    assert ratchet_against(_baseline(tmp_path, 80.0), good) == 0
    assert ratchet_against(_baseline(tmp_path, 95.0), good) == 1
    assert ratchet_against(_baseline(tmp_path, 95.0), good, max_regression=10.0) == 0


def test_ratchet_fails_on_any_collapse_even_with_a_better_score(tmp_path: Path) -> None:
    collapsed = _report(
        [{"score": 99, "status": "fail", "critical_failures": ["completion_settlement_collapse"]}]
    )
    assert ratchet_against(_baseline(tmp_path, 10.0), collapsed) == 1


def test_loads_accepts_dicts_json_text_and_bytes_and_rejects_the_rest() -> None:
    assert _loads({"a": 1}) == {"a": 1}
    assert _loads('{"a": 1}') == {"a": 1}
    assert _loads(b'{"a": 1}') == {"a": 1}
    assert _loads("[1, 2]") == {}
    assert _loads(None) == {}
