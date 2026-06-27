from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from cep.detect import (
    accepted_gap_statuses_for_case,
    detect_reality_gap_collapses,
    valid_evidence_ids,
)
from cep.inventory import (
    iter_reality_gap_anti_collapse_fixtures,
    reality_gap_anti_collapse_manifest,
)
from cep.io import load_json
from cep.paths import REALITY_GAP_CASES_DIR


class ManifestFixture(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    fixture_id: str
    file: str
    expected_errors: list[str]


class AntiCollapseManifest(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    fixtures: list[ManifestFixture]


class ExpectedValidation(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    status: str
    errors: list[str] = Field(default_factory=list)


class AntiCollapseFixture(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")

    fixture_id: str
    target_case_ref: str
    submitted_answer: dict[str, object]
    expected_validation: ExpectedValidation


class AntiCollapseResult(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    fixture_id: str
    ok: bool
    expected_errors: list[str]
    observed_errors: list[str]
    missing_errors: list[str]
    status: str
    message: str


def _manifest() -> AntiCollapseManifest:
    return AntiCollapseManifest.model_validate(load_json(reality_gap_anti_collapse_manifest()))


def expected_fixture_errors() -> dict[str, list[str]]:
    return {fixture.file: fixture.expected_errors for fixture in _manifest().fixtures}


def _observed_collapses(fixture: AntiCollapseFixture) -> list[str]:
    case_dir = REALITY_GAP_CASES_DIR / fixture.target_case_ref
    return detect_reality_gap_collapses(
        fixture.submitted_answer,
        valid_evidence_ids(case_dir),
        accepted_gap_statuses_for_case(case_dir),
    )


def check_fixture(path: Path, expected_errors: list[str] | None = None) -> AntiCollapseResult:
    fixture = AntiCollapseFixture.model_validate(load_json(path))
    expected = (
        expected_errors if expected_errors is not None else fixture.expected_validation.errors
    )
    # Observed errors come from running the detector on the submitted answer,
    # NOT from the fixture's self-declared expected_validation block.
    observed = _observed_collapses(fixture)
    missing = sorted(set(expected) - set(observed))
    status = "invalid" if observed else "valid"
    ok = not missing
    message = "Expected anti-collapse failures observed." if ok else "Missing expected failures."

    return AntiCollapseResult(
        fixture_id=fixture.fixture_id,
        ok=ok,
        expected_errors=expected,
        observed_errors=observed,
        missing_errors=missing,
        status=status,
        message=message,
    )


def run_reality_gap_anti_collapse() -> list[AntiCollapseResult]:
    expected_by_file = expected_fixture_errors()
    return [
        check_fixture(path, expected_errors=expected_by_file.get(path.name, []))
        for path in iter_reality_gap_anti_collapse_fixtures()
    ]
