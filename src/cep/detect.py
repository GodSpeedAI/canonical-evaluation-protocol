"""Content-based anti-collapse detection for RealityGapBench answers.

This module inspects the *content* of a submitted answer and reports which
CEP semantic collapses it commits. It is the single source of truth for
anti-collapse detection used by both the RealityGapBench scorer and the
conformance harness, so a "PASS" reflects engine behaviour rather than a
fixture's self-declaration.

All detection is grounded in answer fields (state refs, evidence refs,
gap_summary, confidence basis, recommended action, limitations) — never in
file names or the fixture's own `expected_validation` block.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from cep.io import load_json

# Phrases that signal an answer is reasoning from the *absence* of a record.
_ABSENCE_TERMS = (
    "missing",
    "not provided",
    "no evidence",
    "nothing to evaluate",
    "no record",
    "no test",
    "not found",
    "was not present",
    "no regression",
)
_PROCEED_ACTIONS = {"no_action_required", "repair_observed_process", "update_declared_state"}
_HIGH_CONFIDENCE = {"high", "medium_high"}


Answer = Mapping[str, object]


def _as_str_list(value: object) -> list[str]:
    if isinstance(value, list):
        items = cast("list[object]", value)
        return [item for item in items if isinstance(item, str)]
    return []


def _evidence_collapses(refs: list[str], known_evidence_ids: set[str]) -> set[str]:
    failures: set[str] = set()
    for ref in refs:
        if ref in known_evidence_ids:
            continue
        # summary ≠ source vs claim ≠ evidence, depending on what was cited.
        failures.add("summary_source_collapse" if "summary" in ref.lower() else "claim_as_evidence")
    return failures


def _nested_str(answer: Answer, key: str, sub: str) -> str:
    value = answer.get(key)
    if isinstance(value, Mapping):
        return str(cast("Mapping[str, object]", value).get(sub, ""))
    return ""


def _answer_text(answer: Answer) -> str:
    return " ".join(
        [
            str(answer.get("gap_summary", "")),
            _nested_str(answer, "confidence", "basis"),
            _nested_str(answer, "recommended_next_action", "description"),
        ]
    ).lower()


def _limitation_text(answer: Answer) -> str:
    return " ".join(_as_str_list(answer.get("limitations"))).lower()


def valid_evidence_ids(case_dir: Path) -> set[str]:
    """Evidence record IDs that actually exist for a case (file stems)."""
    evidence_dir = case_dir / "evidence"
    if not evidence_dir.exists():
        return set()
    return {path.stem for path in evidence_dir.glob("*.json")}


def detect_reality_gap_collapses(
    answer: Answer,
    known_evidence_ids: set[str],
    accepted_gap_statuses: list[str],
) -> list[str]:
    """Return the anti-collapse error codes a RealityGapBench answer commits."""
    failures: set[str] = set()

    no_gap = str(answer.get("gap_status", "")) == "no_gap_detected"
    text = _answer_text(answer)
    high_conf = _nested_str(answer, "confidence", "value") in _HIGH_CONFIDENCE
    declared = set(_as_str_list(answer.get("declared_state_refs")))
    observed = set(_as_str_list(answer.get("observed_state_refs")))
    relations = " ".join(_as_str_list(answer.get("affected_relations"))).lower()
    action_type = _nested_str(answer, "recommended_next_action", "type")
    has_absence = any(term in text for term in _ABSENCE_TERMS)

    # declared state ≠ observed state — using one as the other.
    if declared and declared == observed:
        failures.add("declared_observed_collapse")

    # claim/summary ≠ evidence — citing something that is not an evidence record.
    failures |= _evidence_collapses(_as_str_list(answer.get("evidence_refs")), known_evidence_ids)

    # summary ≠ source — a gap claimed with no declared/observed grounding at all.
    if not declared and not observed and not no_gap:
        failures.add("summary_source_collapse")

    signals = _Signals(
        text=text,
        relations=relations,
        action_type=action_type,
        no_gap=no_gap,
        has_absence=has_absence,
        safe_limitation=any(
            phrase in _limitation_text(answer) for phrase in ("may exist", "does not prove")
        ),
    )
    failures |= _semantic_collapses(signals)

    # A confident answer that asserts the opposite of the case's expected status.
    if no_gap and "no_gap_detected" not in accepted_gap_statuses and high_conf:
        failures.add("opposite_answer_with_high_confidence")

    return sorted(failures)


@dataclass(frozen=True, slots=True)
class _Signals:
    text: str
    relations: str
    action_type: str
    no_gap: bool
    has_absence: bool
    safe_limitation: bool


def _semantic_collapses(s: _Signals) -> set[str]:
    """Collapses detectable from the answer's prose, relations, and action."""
    failures: set[str] = set()
    text, relations, no_gap = s.text, s.relations, s.no_gap

    # completion ≠ settlement — "completed, therefore settled / no gap".
    if no_gap and "complet" in text and "settl" in text:
        failures.add("completion_settlement_collapse")

    # CI pass ≠ peer approval — a technical pass treated as governance settlement.
    if no_gap and re.search(r"\bci\b", text) and "pass" in text:
        failures.add("ci_approval_collapse")

    # possibility ≠ affordance — "they can do it, so proceed" past a constraint.
    can_do = "can_perform" in relations or any(
        p in text for p in ("can perform", "could perform", "able to perform")
    )
    if can_do and (s.action_type in _PROCEED_ACTIONS or "proceed" in text):
        failures.add("possibility_affordance_collapse")

    # authority ≠ capability — execution treated as proof of authorization/capability.
    if (
        "authority and capability" in text
        or "therefore_authorized" in relations
        or ("proceed" in text and "authoriz" in text)
    ):
        failures.add("authority_capability_collapse")

    # unknown ≠ false — concluding failure from a missing record.
    if not no_gap and "fail" in text and s.has_absence and not s.safe_limitation:
        failures |= {"unknown_as_false", "missing_evidence_as_failure_proof"}

    # missing evidence ≠ no gap — "no evidence was provided, so no gap".
    if no_gap and s.has_absence:
        failures |= {"missing_evidence_as_no_gap", "unknown_as_false"}

    # score / one success ≠ capability.
    capability_basis = ("score", "benchmark", "one-time", "single")
    if "capability" in text and any(t in text for t in capability_basis):
        failures |= {"score_capability_collapse", "single_success_capability_collapse"}

    return failures


def reasoning_is_grounded(answer: Answer) -> bool:
    """A gap claim must reference both the declared and observed sides.

    Catches label-correct answers with empty or irrelevant reasoning
    (representation ≠ reality at the prose level).
    """
    if str(answer.get("gap_status", "")) == "no_gap_detected":
        return True
    summary = str(answer.get("gap_summary", "")).lower()
    return "declared" in summary and "observed" in summary


def accepted_gap_statuses_for_case(case_dir: Path) -> list[str]:
    key = load_json(case_dir / "answer_key.json")
    return _as_str_list(key.get("accepted_gap_statuses"))
