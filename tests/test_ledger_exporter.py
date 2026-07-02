"""WP-7 (F-11) smoke test: export REAL ledger rows → CEP scored results.

Inserts a genuine SettlementRecorded + its causation EvidenceRecorded into the
ledger's `event_log.agent_events` (via the Task-3 docker-compose Postgres),
runs the exporter, and asserts a `benchmark-result.schema.json`-valid output
derived from real Postgres rows — not a hand-made fixture.

Teeth-check: corrupting the exported corpus makes the result invalid.

Requires the docker-compose stack up (run:
`docker compose -f ../godspeed_agent/tests/e2e/docker-compose.yml up -d`).
SKIPPED if Postgres is not reachable.
"""
from __future__ import annotations

import json
import os
import socket
import uuid
from pathlib import Path

import psycopg
import pytest

PG_DSN = os.getenv(
    "E2E_PG_DSN", "postgresql://bridge_worker:bridge_e2e_pw@127.0.0.1:5432/agent_memory"
)
REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_SCHEMA = REPO_ROOT / "schemas" / "benchmark-result.schema.json"


def _reachable(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


pytestmark = pytest.mark.skipif(
    not _reachable("127.0.0.1", 5432),
    reason="ledger Postgres not up (run the godspeed_agent e2e docker compose)",
)


def _insert_event(cur, event_type: str, payload: dict) -> str:
    event_id = str(uuid.uuid4())
    cur.execute(
        """
        INSERT INTO event_log.agent_events
            (id, source_agent, event_type, payload, idempotency_key)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (source_agent, idempotency_key) DO NOTHING
        """,
        (event_id, "godspeed-agent", event_type, json.dumps(payload), event_id),
    )
    return event_id


@pytest.fixture()
def real_settlement_pair(tmp_path):
    """Insert one usable (matched) and one unusable (mismatched) settlement,
    each joined to its real EvidenceRecorded, into the live ledger."""
    rows = []
    with psycopg.connect(PG_DSN) as conn, conn.cursor() as cur:
        # Case A: observed == expected → genuinely settled.
        ev_a = _insert_event(
            cur, "EvidenceRecorded",
            {
                "work_request_id": "wr-export-a",
                "proof_result_id": "pr-a",
                "observed_result": "ok",
                "expected_result": "ok",
            },
        )
        _insert_event(
            cur, "SettlementRecorded",
            {
                "work_request_id": "wr-export-a",
                "proof_result_id": "pr-a",
                "evidence_event_id": ev_a,
                "outcome": "usable",
                "outcome_reason": "matched",
            },
        )
        # Case B: observed != expected → unsettled, but settlement honestly
        # classifies it "unusable" (no collapse).
        ev_b = _insert_event(
            cur, "EvidenceRecorded",
            {
                "work_request_id": "wr-export-b",
                "proof_result_id": "pr-b",
                "observed_result": "nope",
                "expected_result": "ok",
            },
        )
        _insert_event(
            cur, "SettlementRecorded",
            {
                "work_request_id": "wr-export-b",
                "proof_result_id": "pr-b",
                "evidence_event_id": ev_b,
                "outcome": "unusable",
                "outcome_reason": "mismatched",
            },
        )
        conn.commit()
        rows = [("wr-export-a", "settled", "usable"), ("wr-export-b", "unsettled", "unusable")]
    yield rows


def test_exporter_produces_schema_valid_result_from_real_rows(real_settlement_pair, tmp_path):
    import jsonschema

    from cep.exporters.ledger_postgres import export_settlement_corpus

    out = tmp_path / "corpus"
    report = export_settlement_corpus(PG_DSN, out)
    assert report.case_count >= 2
    assert report.scored >= 2, "both seeded settlements must be scoreable (have evidence)"
    assert report.skipped_no_evidence == 0

    # At least one benchmark-result.json exists and validates against the schema.
    results = list(out.glob("case-*/result.json"))
    assert results, "no scored results written"
    schema = json.loads(RESULT_SCHEMA.read_text())
    for r in results:
        doc = json.loads(r.read_text())
        jsonschema.validate(doc, schema)  # raises on invalid → teeth

    # Case A (genuine match, claimed usable) must PASS; case B (mismatch,
    # claimed unusable) must also score cleanly — neither collapses.
    by_case = {}
    for r in results:
        doc = json.loads(r.read_text())
        by_case[doc["case_id"]] = doc
    assert by_case["wr-export-a"]["status"] == "pass", "genuine match should pass"
    assert "completion_settlement_collapse" not in by_case["wr-export-b"]["critical_failures"]


def test_exporter_detects_collapse(tmp_path):
    """If a settlement claims 'usable' on a mismatched evidence, that is a
    settlement collapse — the scorer's anti-collapse cap must fire."""
    with psycopg.connect(PG_DSN) as conn, conn.cursor() as cur:
        ev = _insert_event(
            cur, "EvidenceRecorded",
            {
                "work_request_id": "wr-collapse",
                "proof_result_id": "pr-c",
                "observed_result": "wrong",
                "expected_result": "right",
            },
        )
        _insert_event(
            cur, "SettlementRecorded",
            {
                "work_request_id": "wr-collapse",
                "proof_result_id": "pr-c",
                "evidence_event_id": ev,
                "outcome": "usable",  # dishonest: evidence mismatched
                "outcome_reason": "claimed settled",
            },
        )
        conn.commit()

    from cep.exporters.ledger_postgres import export_settlement_corpus

    report = export_settlement_corpus(PG_DSN, tmp_path / "collapse")
    collapse_results = [r for r in report.results if r["case_id"] == "wr-collapse"]
    assert collapse_results, "collapse case not scored"
    assert "completion_settlement_collapse" in collapse_results[0]["critical_failures"]
    assert collapse_results[0]["status"] == "invalid"


# ── Ratchet (§14: week-over-week non-regression + anti-collapse) ───────────────
# These are unit tests — no Postgres required.

def _report(score: float, collapses: int = 0):
    from cep.exporters.ledger_postgres import ExportReport

    r = ExportReport(out_dir=Path("/tmp"), case_count=1, scored=1, skipped_no_evidence=0)
    r.results = [{
        "score": score,
        "status": "pass" if score >= 85 else "fail",
        "critical_failures": ["completion_settlement_collapse"] if collapses else [],
    }]
    return r


def test_ratchet_first_run_establishes_baseline(tmp_path):
    from cep.exporters.ledger_postgres import ratchet_against

    prev = tmp_path / "prev-aggregate.json"
    assert ratchet_against(prev, _report(90.0)) == 0  # no baseline → OK


def test_ratchet_passes_on_no_regression(tmp_path):
    from cep.exporters.ledger_postgres import ratchet_against

    prev = tmp_path / "prev.json"
    prev.write_text(json.dumps({"mean_score": 80.0}))
    assert ratchet_against(prev, _report(85.0)) == 0


def test_ratchet_fails_on_regression(tmp_path):
    from cep.exporters.ledger_postgres import ratchet_against

    prev = tmp_path / "prev.json"
    prev.write_text(json.dumps({"mean_score": 90.0}))
    assert ratchet_against(prev, _report(70.0)) == 1  # regressed 20 points


def test_ratchet_fails_hard_on_any_collapse(tmp_path):
    from cep.exporters.ledger_postgres import ratchet_against

    prev = tmp_path / "prev.json"
    prev.write_text(json.dumps({"mean_score": 50.0}))
    # Even if the score IMPROVED, a collapse is a hard failure (§14).
    assert ratchet_against(prev, _report(99.0, collapses=1)) == 1
