"""Ledger → CEP corpus exporter (WP-7, F-11).

Turns real `SettlementRecorded` rows in the ledger's `event_log.agent_events`
into scored CEP `benchmark-result` documents, so the Evaluate arc sees live
behaviour instead of hand-made fixtures.

Ground truth is NOT synthesized. A settlement's expected status is derived by
joining it to its causation `EvidenceRecorded`: both events carry the same
``work_request_id`` + ``proof_result_id`` in their payloads, so the join works
on real bridge-inserted rows (the bridge stores only the event-specific
payload in ``agent_events``; the envelope ``event_id`` is not a column).
``observed_result == expected_result`` ⇒ genuinely settled; otherwise
unsettled. This gives the scorer a real answer key — and lets it detect
*collapse* (a settlement claims "usable" when the evidence did not match).

Uses CEP's documented call surface (`from_settlement_recorded` +
`score_settlement_answer`) rather than the fixture-bound `cep run
settlement-corpus` CLI, per `docs/settlement-call-surface.md`.

§14 scope guard: results are written for humans first; the ratchet job
compares week-over-week and enforces anti-collapse. No absolute threshold is
invented here.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psycopg

from cep.benchmarks.settlement import (
    SettlementAnswerKey,
    from_settlement_recorded,
    score_settlement_answer,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ExportReport:
    out_dir: Path
    case_count: int
    scored: int
    skipped_no_evidence: int
    results: list[dict[str, Any]] = field(default_factory=list)

    def aggregate(self) -> dict[str, Any]:
        scores = [r["score"] for r in self.results]
        collapses = sum(
            1 for r in self.results if "completion_settlement_collapse" in r["critical_failures"]
        )
        return {
            "generated_at": _now_iso(),
            "case_count": self.case_count,
            "scored": self.scored,
            "skipped_no_evidence": self.skipped_no_evidence,
            "mean_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
            "collapse_count": collapses,
            "pass_count": sum(1 for r in self.results if r["status"] == "pass"),
            "fail_count": sum(1 for r in self.results if r["status"] in ("fail", "invalid")),
        }


# Join SettlementRecorded to its EvidenceRecorded on the shared
# (work_request_id, proof_result_id) — both ride in the event payloads and are
# stable references present in real bridge-inserted agent_events rows.
_QUERY = """
    SELECT
        s.payload->>'work_request_id'   AS work_request_id,
        s.payload                       AS settlement_payload,
        e.payload->>'observed_result'   AS observed_result,
        e.payload->>'expected_result'   AS expected_result
    FROM event_log.agent_events s
    LEFT JOIN event_log.agent_events e
        ON e.event_type = 'EvidenceRecorded'
       AND e.payload->>'work_request_id'   = s.payload->>'work_request_id'
       AND e.payload->>'proof_result_id'   = s.payload->>'proof_result_id'
    WHERE s.event_type = 'SettlementRecorded'
      AND (%s::text IS NULL OR s.created_at >= %s::timestamptz)
    ORDER BY s.created_at
"""


def export_settlement_corpus(
    pg_dsn: str,
    out_dir: Path,
    *,
    since: str | None = None,
) -> ExportReport:
    """Export + score SettlementRecorded rows. Writes one case dir per row
    (``answer_key.json``, ``example_ledger_answer.json``, ``result.json``) and
    an ``aggregate.json`` summary. Rows with no matching EvidenceRecorded are
    counted as ``skipped_no_evidence`` (no ground truth → not scored, not
    fabricated)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = ExportReport(out_dir=out_dir, case_count=0, scored=0, skipped_no_evidence=0)

    with psycopg.connect(pg_dsn) as conn, conn.cursor() as cur:
        cur.execute(_QUERY, (since, since))
        rows = cur.fetchall()

    for work_request_id, settlement_payload, observed, expected in rows:
        report.case_count += 1
        settlement_payload = _loads(settlement_payload)
        work_request_id = work_request_id or settlement_payload.get("work_request_id") or uuid.uuid4().hex

        case_dir = out_dir / f"case-{work_request_id}"
        case_dir.mkdir(parents=True, exist_ok=True)
        # Auditable provenance: the raw settlement payload behind this case.
        (case_dir / "settlement_recorded.json").write_text(
            json.dumps(settlement_payload, indent=2, sort_keys=True), encoding="utf-8"
        )

        if observed is None or expected is None:
            # No causation evidence → no honest ground truth. Record the case
            # but do not score it (do not synthesize an answer key).
            report.skipped_no_evidence += 1
            continue

        observed, expected = str(observed), str(expected)
        # Ground-truth expected status from the evidence comparison itself.
        expected_status = (
            "settled"
            if observed.strip() and observed.strip() == expected.strip()
            else "unsettled"
        )

        answer_key = SettlementAnswerKey(
            case_ref=work_request_id,
            expected_settlement_status=expected_status,
            required_evidence_refs=[],
            required_distinctions=[],
        )
        answer = from_settlement_recorded(settlement_payload)

        (case_dir / "answer_key.json").write_text(
            answer_key.model_dump_json(indent=2), encoding="utf-8"
        )
        (case_dir / "example_ledger_answer.json").write_text(
            answer.model_dump_json(indent=2), encoding="utf-8"
        )

        record = score_settlement_answer(answer_key, answer)
        result = json.loads(record.to_json())
        result["generated_at"] = _now_iso()
        report.results.append(result)
        (case_dir / "result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True), encoding="utf-8"
        )
        report.scored += 1

    (out_dir / "aggregate.json").write_text(
        json.dumps(report.aggregate(), indent=2, sort_keys=True), encoding="utf-8"
    )
    return report


def _loads(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, (bytes, str)):
        return json.loads(value)
    return {}


def ratchet_against(previous: Path, current: ExportReport, *, max_regression: float = 0.0) -> int:
    """Compare this run's aggregate to the previous stored one. Fails (returns
    non-zero) on mean-score regression beyond ``max_regression`` OR any
    anti-collapse violation (a collapse is a hard failure per §14)."""
    if not previous.exists():
        # No baseline yet — first run establishes it. §14: no absolute
        # thresholds before live corpus history exists.
        return 0
    prev = json.loads(previous.read_text(encoding="utf-8"))
    curr = current.aggregate()
    if curr["collapse_count"] > 0:
        print(f"RATCHET FAIL: {curr['collapse_count']} settlement collapse(s) detected")
        return 1
    regression = prev.get("mean_score", 0.0) - curr["mean_score"]
    if regression > max_regression:
        print(
            f"RATCHET FAIL: mean_score regressed {regression:.2f} "
            f"({prev.get('mean_score')} → {curr['mean_score']})"
        )
        return 1
    print(
        f"RATCHET OK: mean_score {curr['mean_score']} (prev {prev.get('mean_score')}), "
        f"collapses={curr['collapse_count']}"
    )
    return 0
