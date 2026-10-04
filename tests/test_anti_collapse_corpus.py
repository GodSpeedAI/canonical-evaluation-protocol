from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from cep.conformance.anti_collapse import run_reality_gap_anti_collapse
from cep.conformance.corpus import (
    CORPUS_SCHEMA_VERSION,
    CorpusError,
    evaluate_corpus,
    load_corpus,
)
from cep.io import write_json
from cep.json_types import JsonObject

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "fixtures" / "anti-collapse" / "reality-gap"


def _minimal_answer() -> dict[str, object]:
    """A submitted answer that commits no anti-collapse violation."""
    return {
        "gap_status": "no_gap_detected",
        "gap_summary": "The declared and observed states agree; no residual gap.",
        "declared_state_refs": ["state-declared-1"],
        "observed_state_refs": ["state-observed-1"],
        "evidence_refs": ["ev-1"],
        "confidence": {"value": "high", "basis": "A qualifying evidence record."},
        "recommended_next_action": {"type": "review", "description": "No ungrounded claim."},
        "limitations": ["The observed state does not prove the declared state."],
    }


def _corpus(records: list[dict[str, object]], path: Path) -> Path:
    payload: object = {
        "$schema": CORPUS_SCHEMA_VERSION,
        "corpus_id": "test-corpus",
        "records": records,
    }
    write_json(path, cast("JsonObject", payload))
    return path


# ── fixture mode unchanged ────────────────────────────────────────────────


def test_fixture_mode_unaffected_by_corpus_module() -> None:
    # Importing + using the corpus path never changes the fixture discovery.
    results = run_reality_gap_anti_collapse()
    assert results, "No anti-collapse fixtures discovered"
    assert all(result.ok for result in results), [result for result in results if not result.ok]


# ── adapter / loading ─────────────────────────────────────────────────────


def test_load_corpus_normalizes_records(tmp_path: Path) -> None:
    p = _corpus(
        [
            {
                "record_id": "rec-1",
                "record_ref": "sxr://evidence/1",
                "accepted_gap_statuses": ["no_gap_detected"],
                "valid_evidence_ids": ["ev-1"],
                "submitted_answer": _minimal_answer(),
            }
        ],
        tmp_path / "corpus.json",
    )
    records = load_corpus(p)
    assert len(records) == 1
    assert records[0].record_id == "rec-1"
    assert records[0].record_ref == "sxr://evidence/1"
    assert records[0].valid_evidence_ids == ["ev-1"]
    assert records[0].accepted_gap_statuses == ["no_gap_detected"]


def test_malformed_corpus_back_and_forth(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    _ = bad.write_text("{ not json")
    with pytest.raises(CorpusError):
        _ = load_corpus(bad)


def test_corpus_without_records_fails(tmp_path: Path) -> None:
    p = tmp_path / "c.json"
    write_json(p, {"$schema": CORPUS_SCHEMA_VERSION})
    with pytest.raises(CorpusError):
        _ = load_corpus(p)


def test_unsupported_schema_fails_loudly(tmp_path: Path) -> None:
    p = tmp_path / "c.json"
    write_json(p, {"$schema": "cep/unknown@1", "records": []})
    with pytest.raises(CorpusError):
        _ = load_corpus(p)


def test_record_missing_submitted_answer_fails_not_skipped(tmp_path: Path) -> None:
    p = _corpus(
        [{"record_id": "rec-x", "accepted_gap_statuses": [], "valid_evidence_ids": []}],
        tmp_path / "c.json",
    )
    with pytest.raises(CorpusError):
        _ = load_corpus(p)


# ── evaluator reuse ───────────────────────────────────────────────────────


def test_valid_corpus_passes(tmp_path: Path) -> None:
    p = _corpus(
        [
            {
                "record_id": "rec-valid",
                "valid_evidence_ids": ["ev-1"],
                "accepted_gap_statuses": ["no_gap_detected"],
                "submitted_answer": _minimal_answer(),
            }
        ],
        tmp_path / "c.json",
    )
    results = evaluate_corpus(p)
    assert len(results) == 1
    assert results[0].ok
    assert results[0].observed_errors == []


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (
            {
                "evidence_refs": ["not-a-real-evidence"],
            },
            "claim_as_evidence",
        ),
        (
            {
                "declared_state_refs": ["same"],
                "observed_state_refs": ["same"],
            },
            "declared_observed_collapse",
        ),
        (
            {
                "gap_status": "no_gap_detected",
                "gap_summary": "The release is complete and settled, therefore no gap.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
            },
            "completion_settlement_collapse",
        ),
        (
            {
                "gap_status": "no_gap_detected",
                "gap_summary": "CI passes, so no gap.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
            },
            "ci_approval_collapse",
        ),
        (
            {
                "gap_status": "no_gap_detected",
                "gap_summary": "They can perform the action even without a fixture.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
                "recommended_next_action": {"type": "no_action_required"},
            },
            "possibility_affordance_collapse",
        ),
        (
            {
                "gap_status": "no_gap_detected",
                "gap_summary": "Authority and capability were proven, proceed.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
                "recommended_next_action": {"type": "no_action_required"},
            },
            "authority_capability_collapse",
        ),
        (
            {
                "gap_status": "no_gap_detected",
                "gap_summary": "No evidence was provided, so no gap.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
                "evidence_refs": [],
            },
            "missing_evidence_as_no_gap",
        ),
        (
            {
                "gap_status": "gap_detected",
                "gap_summary": "It failed because no record was present.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
                "evidence_refs": ["ev-1"],
                "limitations": [],
            },
            "unknown_as_false",
        ),
        (
            {
                "gap_status": "no_gap_detected",
                "gap_summary": "The score proves capability, so no gap.",
                "declared_state_refs": ["d"],
                "observed_state_refs": ["o"],
            },
            "score_capability_collapse",
        ),
    ],
)
def test_corpus_records_with_each_violation_fail(
    tmp_path: Path, mutate: dict[str, object], expected: str
) -> None:
    answer = _minimal_answer()
    answer.update(mutate)
    p = _corpus(
        [
            {
                "record_id": f"rec-bad-{expected}",
                "valid_evidence_ids": ["ev-1"],
                "accepted_gap_statuses": ["no_gap_detected"],
                "submitted_answer": answer,
            }
        ],
        tmp_path / f"{expected}.json",
    )
    results = evaluate_corpus(p)
    result = results[0]
    assert not result.ok
    assert expected in result.observed_errors


# ── deterministic output / boundary visibility ───────────────────────────


def test_results_are_deterministically_ordered(tmp_path: Path) -> None:
    records: list[dict[str, object]] = cast(
        "list[dict[str, object]]",
        [
            {
                "record_id": f"rec-{i}",
                "valid_evidence_ids": ["ev-1"],
                "accepted_gap_statuses": ["no_gap_detected"],
                "submitted_answer": _minimal_answer(),
            }
            for i in [3, 1, 2]
        ],
    )
    p = _corpus(records, tmp_path / "c.json")
    first = [(r.record_id, r.ok) for r in evaluate_corpus(p)]
    second = [(r.record_id, r.ok) for r in evaluate_corpus(p)]
    assert first == second
    assert [rid for rid, _ in first] == ["rec-1", "rec-2", "rec-3"]


def test_failures_id_both_record_and_invariant(tmp_path: Path) -> None:
    answer = _minimal_answer()
    answer["evidence_refs"] = ["summary:not-an-evidence"]
    p = _corpus(
        [
            {
                "record_id": "rec-survey",
                "valid_evidence_ids": ["ev-1"],
                "accepted_gap_statuses": ["no_gap_detected"],
                "submitted_answer": answer,
            }
        ],
        tmp_path / "c.json",
    )
    results = evaluate_corpus(p)
    assert not results[0].ok
    assert results[0].record_id == "rec-survey"
    assert "summary_source_collapse" in results[0].observed_errors
