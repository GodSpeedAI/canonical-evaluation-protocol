import json
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


def test_settlement_genuinely_settled_case_is_scoreable(tmp_path: Path) -> None:
    # Given: a case whose expected outcome IS settled, and an answer that agrees.
    case_dir = tmp_path / "set-9999"
    case_dir.mkdir()
    answer_key: dict[str, object] = {
        "case_ref": "set-9999",
        "expected_settlement_status": "settled",
        "required_evidence_refs": [],
        "required_distinctions": [],
    }
    answer: dict[str, object] = {
        "answer_id": "a1",
        "case_ref": "set-9999",
        "settlement_status": "settled",
        "completion_claim_accepted": True,
        "evidence_refs": [],
        "preserved_distinctions": [],
    }
    _ = (case_dir / "answer_key.json").write_text(json.dumps(answer_key), encoding="utf-8")
    answer_path = case_dir / "answer.json"
    _ = answer_path.write_text(json.dumps(answer), encoding="utf-8")

    # When: scored.
    result = score_settlement(case_dir, answer_path)

    # Then: calling it settled is correct here, not a collapse.
    assert not result.critical_failures, result.to_json()
    assert result.status == "pass", result.to_json()


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
