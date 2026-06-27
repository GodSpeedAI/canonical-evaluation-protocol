from pathlib import Path

from cep.benchmarks.reality_gap import score_reality_gap

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "benchmarks" / "reality-gap" / "cases"


def test_existing_valid_answers_score_pass_or_partial() -> None:
    for case_dir in sorted(CASES.glob("rg-*")):
        answer_path = case_dir / "example_valid_answer.json"

        result = score_reality_gap(case_dir, answer_path)

        assert result.status in {"pass", "partial"}, result.to_json()
        assert result.score >= 60, result.to_json()


def test_existing_invalid_answers_do_not_pass() -> None:
    for case_dir in sorted(CASES.glob("rg-*")):
        answer_path = case_dir / "example_invalid_answer.json"

        result = score_reality_gap(case_dir, answer_path)

        assert result.status in {"fail", "invalid"}, result.to_json()
        assert result.score < 85, result.to_json()


def test_wrong_primary_gap_type_lowers_valid_answer_score(tmp_path: Path) -> None:
    case_dir = CASES / "rg-0001"
    answer_path = case_dir / "example_valid_answer.json"
    mutated_answer_path = tmp_path / "wrong-gap-type.json"
    mutated = answer_path.read_text(encoding="utf-8").replace(
        '"gap_type": "authority_drift"',
        '"gap_type": "process_drift"',
    )
    _ = mutated_answer_path.write_text(mutated, encoding="utf-8")

    result = score_reality_gap(case_dir, mutated_answer_path)

    assert result.score < 85, result.to_json()
