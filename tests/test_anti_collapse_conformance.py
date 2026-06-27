from pathlib import Path

from cep.conformance.anti_collapse import check_fixture, run_reality_gap_anti_collapse
from cep.io import load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "fixtures" / "anti-collapse" / "reality-gap"


def test_anti_collapse_fixtures_trigger_expected_failures() -> None:
    results = run_reality_gap_anti_collapse()

    assert results, "No anti-collapse fixtures discovered"
    assert all(result.ok for result in results), [result for result in results if not result.ok]


def test_silent_pass_fails_conformance(tmp_path: Path) -> None:
    fixture_path = FIXTURES / "rg-ac-0002-claim-as-evidence.json"
    payload = load_json(fixture_path)
    payload["expected_validation"] = {
        "status": "valid",
        "errors": [],
        "warnings": [],
        "critical": False,
    }
    silent_fixture = tmp_path / fixture_path.name
    write_json(silent_fixture, payload)

    result = check_fixture(silent_fixture, expected_errors=["claim_as_evidence"])

    assert not result.ok
    assert "claim_as_evidence" in result.missing_errors
