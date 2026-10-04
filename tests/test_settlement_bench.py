import json
from pathlib import Path

from typer.testing import CliRunner

from cep.benchmarks.settlement import (
    SettlementAnswerKey,
    from_settlement_recorded,
    score_settlement,
    score_settlement_answer,
)
from cep.cli import app
from cep.json_types import JsonObject

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "benchmarks" / "settlement" / "cases" / "set-0001"
SAMPLE_SETTLEMENT_RECORDED = ROOT / "tests" / "fixtures" / "sample_settlement_recorded.json"


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
        ROOT / "reports" / "settlement" / "set-0001-ans-set-0001-valid-example.result.json"
    ).exists()


def test_from_settlement_recorded_maps_usable_outcome_to_settled() -> None:
    # Given: a real SettlementRecorded payload shape (godspeed_agent adapters.py).
    payload: JsonObject = {
        "work_request_id": "wr-0001",
        "proof_result_id": "proof-0001",
        "evidence_event_id": "evidence-0001",
        "outcome": "usable",
        "outcome_reason": "Observed result matches expected result",
        "context_packet_id": None,
        "settled_at": "2026-07-01T12:05:00Z",
    }

    # When: adapted into a SettlementAnswer.
    answer = from_settlement_recorded(payload)

    # Then: CEP's vocabulary is applied without godspeed_agent reshaping its event.
    assert answer.case_ref == "wr-0001"
    assert answer.answer_id == "evidence-0001"
    assert answer.settlement_status == "settled"
    assert answer.completion_claim_accepted is True


def test_score_settlement_answer_caps_score_on_completion_settlement_collapse() -> None:
    # Given: a producer's "usable" outcome for a case that expected only partial settlement.
    answer_key = SettlementAnswerKey(
        case_ref="wr-0001",
        expected_settlement_status="partially_settled",
        required_evidence_refs=["ev-0001"],
        required_distinctions=["completion_vs_settlement"],
    )
    payload: JsonObject = {
        "work_request_id": "wr-0001",
        "proof_result_id": "proof-0001",
        "evidence_event_id": "evidence-0001",
        "outcome": "usable",
        "outcome_reason": "Observed result matches expected result",
    }
    answer = from_settlement_recorded(payload)

    # When: scored through the stable call surface, routed through the real scorer.
    result = score_settlement_answer(answer_key, answer)

    # Then: anti-collapse enforcement caps the score, proving this isn't a stub.
    assert "completion_settlement_collapse" in result.critical_failures
    assert result.score <= 30.0, result.to_json()


def test_cli_score_settlement_reads_realistic_fixture() -> None:
    # Given: the CLI's score-settlement passthrough and a realistic fixture.
    runner = CliRunner()

    # When: it scores a SettlementRecorded-shaped input file.
    result = runner.invoke(app, ["score-settlement", "--input", str(SAMPLE_SETTLEMENT_RECORDED)])

    # Then: it runs the real scorer end to end and reports the collapse.
    assert result.exit_code == 0, result.output
    assert "INVALID" in result.output or "FAIL" in result.output
    assert "completion_settlement_collapse" in result.output
