from pathlib import Path

from typer.testing import CliRunner

from cep.benchmarks.authority import score_authority
from cep.cli import app

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "benchmarks" / "authority" / "cases" / "auth-0001"


def test_authority_valid_deny_passes() -> None:
    # Given: a production write authority case with a valid deny answer.
    answer_path = CASE_DIR / "example_valid_answer.json"

    # When: the AuthorityBench scorer evaluates the answer.
    result = score_authority(CASE_DIR, answer_path)

    # Then: denial backed by policy evidence passes.
    assert result.status == "pass", result.to_json()
    assert result.score >= 85, result.to_json()
    assert not result.critical_failures


def test_authority_false_allow_fails() -> None:
    # Given: an answer that allows action because the actor is capable.
    answer_path = CASE_DIR / "example_invalid_answer.json"

    # When: the AuthorityBench scorer evaluates the answer.
    result = score_authority(CASE_DIR, answer_path)

    # Then: the false allow is rejected as authority/capability collapse.
    assert result.status in {"fail", "invalid"}, result.to_json()
    assert result.score < 85, result.to_json()
    assert "unsafe_authority_recommendation" in result.critical_failures
    assert "authority_capability_collapse" in result.critical_failures


def test_run_authority_corpus_generates_report() -> None:
    # Given: the CLI benchmark runner.
    runner = CliRunner()

    # When: the AuthorityBench corpus is run through the CLI.
    result = runner.invoke(app, ["run", "authority-corpus"])

    # Then: corpus scoring succeeds and writes a portable report.
    assert result.exit_code == 0, result.output
    assert (
        ROOT
        / "reports"
        / "authority"
        / "auth-0001-ans-auth-0001-valid-example.result.json"
    ).exists()
