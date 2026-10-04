from pathlib import Path

from typer.testing import CliRunner

from cep.benchmarks.capability import score_capability
from cep.cli import app

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "benchmarks" / "capability" / "cases" / "cap-0001"


def test_capability_valid_active_not_metabolized_answer_passes() -> None:
    # Given: a campaign with partial settlement and failed recovery.
    answer_path = CASE_DIR / "example_valid_answer.json"

    # When: the CapabilityBench scorer evaluates the answer.
    result = score_capability(CASE_DIR, answer_path)

    # Then: rejecting a metabolized capability claim passes or partial-passes.
    assert result.status in {"pass", "partial"}, result.to_json()
    assert result.score >= 60, result.to_json()
    assert not result.critical_failures


def test_capability_overclaim_fails() -> None:
    # Given: an answer that treats a score and possible action as capability.
    answer_path = CASE_DIR / "example_invalid_answer.json"

    # When: the CapabilityBench scorer evaluates the answer.
    result = score_capability(CASE_DIR, answer_path)

    # Then: capability overclaim and affordance collapse are critical failures.
    assert result.status in {"fail", "invalid"}, result.to_json()
    assert result.score < 85, result.to_json()
    assert "score_capability_collapse" in result.critical_failures
    assert "possibility_affordance_collapse" in result.critical_failures


def test_run_capability_corpus_generates_report() -> None:
    # Given: the CLI benchmark runner.
    runner = CliRunner()

    # When: the CapabilityBench corpus is run through the CLI.
    result = runner.invoke(app, ["run", "capability-corpus"])

    # Then: corpus scoring succeeds and writes a portable report.
    assert result.exit_code == 0, result.output
    assert (
        ROOT / "reports" / "capability" / "cap-0001-ans-cap-0001-valid-example.result.json"
    ).exists()
