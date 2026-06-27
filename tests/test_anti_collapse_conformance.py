from pathlib import Path
from typing import cast

from cep.conformance.anti_collapse import check_fixture, run_reality_gap_anti_collapse
from cep.io import load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "fixtures" / "anti-collapse" / "reality-gap"


def test_anti_collapse_fixtures_trigger_expected_failures() -> None:
    results = run_reality_gap_anti_collapse()

    assert results, "No anti-collapse fixtures discovered"
    assert all(result.ok for result in results), [result for result in results if not result.ok]


def test_conformance_runs_detector_not_self_declaration(tmp_path: Path) -> None:
    # A fixture whose submitted_answer does NOT actually collapse must fail
    # conformance, even if its expected_validation still claims it is invalid.
    # This proves the harness scores the answer instead of trusting the fixture.
    fixture_path = FIXTURES / "rg-ac-0002-claim-as-evidence.json"
    payload = load_json(fixture_path)
    # Repair the answer so it cites a real evidence record (no longer a collapse).
    answer = cast("dict[str, object]", payload["submitted_answer"])
    answer["evidence_refs"] = ["ev-rg-0003-001"]
    repaired_fixture = tmp_path / fixture_path.name
    write_json(repaired_fixture, payload)

    result = check_fixture(repaired_fixture, expected_errors=["claim_as_evidence"])

    assert not result.ok
    assert "claim_as_evidence" in result.missing_errors
    assert "claim_as_evidence" not in result.observed_errors


def test_detector_observes_real_collapse() -> None:
    # The unmodified fixture really does collapse, detected from content.
    result = check_fixture(
        FIXTURES / "rg-ac-0002-claim-as-evidence.json",
        expected_errors=["claim_as_evidence"],
    )
    assert result.ok
    assert "claim_as_evidence" in result.observed_errors
