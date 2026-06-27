from pathlib import Path

from typer.testing import CliRunner

from cep.benchmarks.reality_gap import score_reality_gap
from cep.cli import app
from cep.io import write_json
from cep.reports import report_payload
from cep.validation import validate_instance

ROOT = Path(__file__).resolve().parents[1]


def test_report_payload_has_required_fields() -> None:
    case_dir = ROOT / "benchmarks" / "reality-gap" / "cases" / "rg-0001"
    answer_path = case_dir / "example_valid_answer.json"

    payload = report_payload(score_reality_gap(case_dir, answer_path))

    for field in [
        "result_id",
        "case_id",
        "answer_id",
        "benchmark_family",
        "score",
        "status",
        "metrics",
        "critical_failures",
        "warnings",
        "generated_at",
    ]:
        assert field in payload


def test_report_payload_validates_against_schema() -> None:
    case_dir = ROOT / "benchmarks" / "reality-gap" / "cases" / "rg-0001"
    answer_path = case_dir / "example_valid_answer.json"
    report_path = ROOT / "reports" / "test-rg-0001-valid.result.json"

    payload = report_payload(score_reality_gap(case_dir, answer_path))
    write_json(report_path, payload)

    result = validate_instance(report_path, ROOT / "schemas" / "benchmark-result.schema.json")

    assert result.ok, result.errors


def test_run_reality_gap_corpus_generates_reports() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["run", "reality-gap-corpus"])

    assert result.exit_code == 0, result.output
    assert (
        ROOT / "reports" / "reality-gap" / "rg-0001-ans-rg-0001-valid-example.result.json"
    ).exists()
