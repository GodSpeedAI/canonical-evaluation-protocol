from pathlib import Path

from typer.testing import CliRunner

from cep.benchmarks.settlement import score_settlement
from cep.cli import app

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "benchmarks" / "settlement" / "cases" / "set-0001"


def test_settlement_valid_unsettled_answer_passes() -> None:
    # Given: a deployment case where execution happened but health checks failed.
    answer_path = CASE_DIR / "example_valid_answer.json"

    # When: the SettlementBench scorer evaluates the answer.
    result = score_settlement(CASE_DIR, answer_path)

    # Then: rejecting the completion claim as unsettled passes.
    assert result.status == "pass", result.to_json()
    assert result.score >= 85, result.to_json()
    assert not result.critical_failures


def test_settlement_premature_completion_fails() -> None:
    # Given: an answer that treats execution completion as settlement.
    answer_path = CASE_DIR / "example_invalid_answer.json"

    # When: the SettlementBench scorer evaluates the answer.
    result = score_settlement(CASE_DIR, answer_path)

    # Then: completion/settlement collapse is a critical failure.
    assert result.status in {"fail", "invalid"}, result.to_json()
    assert result.score < 85, result.to_json()
    assert "completion_settlement_collapse" in result.critical_failures


def test_run_settlement_corpus_generates_report() -> None:
    # Given: the CLI benchmark runner.
    runner = CliRunner()

    # When: the SettlementBench corpus is run through the CLI.
    result = runner.invoke(app, ["run", "settlement-corpus"])

    # Then: corpus scoring succeeds and writes a portable report.
    assert result.exit_code == 0, result.output
    assert (
        ROOT
        / "reports"
        / "settlement"
        / "set-0001-ans-set-0001-valid-example.result.json"
    ).exists()
