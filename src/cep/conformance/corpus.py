"""External anti-collapse corpus evaluation (CEP-0010 L2 level gate).

`cep conformance anti-collapse` evaluates CEP's *own* fixtures. This module
generalizes the same command so it can evaluate an **externally supplied**
corpus — including `sxr`-exported records — through the *same* semantic
authority (the RealityGapBench anti-collapse detector in `cep.detect`).

Design intent (Slice 4, sxr): CEP owns CEP meaning and anti-collapse semantics.
`sxr` produces CEP records. The proof gate is

    sxr exported corpus -> independent CEP evaluator -> anti-collapse PASS/FAIL

not ``sxr judges its own CEP semantics``. This module closes that tooling gap
without redefining anti-collapse: it adapts an external corpus into the
evaluator's existing internal representation and reuses
`detect_reality_gap_collapses` verbatim as the single source of truth.

Corpus format (``cep/anti-collapse-corpus@1``): a JSON object

    {
      "corpus_id": "<id>",
      "records": [
        {
          "record_id": "<id>",
          "record_ref": "<provenance, optional>",
          "accepted_gap_statuses": ["no_gap_detected"],
          "valid_evidence_ids": ["ev-1"],
          "submitted_answer": { ...answer fields... }
        }
      ]
    }

The adapter normalizes the *transport* shape (JSON schema, optional nesting)
into the evaluator's internal ``(answer, known_evidence_ids,
accepted_gap_statuses)`` triple. It does not reinterpret CEP meaning.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import pydantic
from pydantic import BaseModel, ConfigDict, Field

from cep.detect import detect_reality_gap_collapses
from cep.io import load_json

CORPUS_SCHEMA_VERSION = "cep/anti-collapse-corpus@1"

_MISSING_FIELDS_HINT = (
    "each record MUST carry record_id, accepted_gap_statuses, valid_evidence_ids, "
    "and submitted_answer (an object)"
)


class _CorpusEnvelope(BaseModel):
    """Canonical external-corpus envelope."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        protected_namespaces=(),  # allow the "$schema" -> schema_variant alias field
    )

    corpus_id: str | None = None
    schema_variant: str | None = Field(default=None, alias="$schema")
    records: list[_CorpusRecordEnvelope]


class _CorpusRecordEnvelope(BaseModel):
    """One evaluated record in the external corpus."""

    model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

    record_id: str
    record_ref: str | None = None
    accepted_gap_statuses: list[str] = Field(default_factory=list)
    valid_evidence_ids: list[str] = Field(default_factory=list)
    submitted_answer: dict[str, object]


@dataclass(frozen=True, slots=True)
class CorpusRecord:
    """Normalized internal record handed to the evaluator.

    This is the adapter's stable output shape; it holds exactly the triple
    `detect_reality_gap_collapses` needs plus identity for reporting.
    """

    record_id: str
    record_ref: str | None
    answer: dict[str, object]
    valid_evidence_ids: list[str]
    accepted_gap_statuses: list[str]


class CorpusResult(BaseModel):
    """One record's anti-collapse verdict."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    record_id: str
    ok: bool
    observed_errors: list[str]
    message: str


class CorpusError(Exception):
    """Raised when the external corpus is malformed or unsupported at the boundary."""

    def __init__(self, path: Path, reason: str) -> None:
        self.path: Path = path
        self.reason: str = reason
        super().__init__(f"{path}: {reason}")


def _load_corpus(path: Path) -> _CorpusEnvelope:
    """Load + validate an external corpus, failing loudly at the boundary."""
    try:
        raw = load_json(path)
    except Exception as exc:  # pydantic vio or io error → explicit failure
        raise CorpusError(path, f"malformed corpus: {exc}") from exc

    declared = raw.get("$schema") or raw.get("schema")
    if isinstance(declared, str) and declared != CORPUS_SCHEMA_VERSION:
        unsupported = f"unsupported corpus schema {declared!r} (supported: {CORPUS_SCHEMA_VERSION})"
        raise CorpusError(path, unsupported)

    records = raw.get("records")
    if not isinstance(records, list):
        raise CorpusError(path, f"corpus has no 'records' array; {_MISSING_FIELDS_HINT}")

    try:
        envelope = _CorpusEnvelope.model_validate(raw)
    except pydantic.ValidationError as exc:
        raise CorpusError(path, f"corpus validation failed: {exc}; {_MISSING_FIELDS_HINT}") from exc

    for rec in envelope.records:
        # A record must be evaluable; an unsupported one is a hard diagnostic, never a skip.
        if not rec.record_id:
            raise CorpusError(path, "record with empty record_id is unsupported")
    return envelope


def load_corpus(path: Path) -> list[CorpusRecord]:
    """Adapter: external corpus representation -> evaluator's internal records."""
    envelope = _load_corpus(path)
    return [
        CorpusRecord(
            record_id=rec.record_id,
            record_ref=rec.record_ref,
            answer=rec.submitted_answer,
            valid_evidence_ids=list(rec.valid_evidence_ids),
            accepted_gap_statuses=list(rec.accepted_gap_statuses),
        )
        for rec in envelope.records
    ]


def evaluate_corpus(path: Path) -> list[CorpusResult]:
    """Run the existing anti-collapse evaluator over an external corpus.

    Each record reuses `detect_reality_gap_collapses` — the same detector the
    fixture mode uses — so PASS/FAIL reflects engine behaviour, not an external
    self-declaration. A record is OK when it commits no collapse.
    """
    records = load_corpus(path)
    results: list[CorpusResult] = []
    for rec in records:
        observed = detect_reality_gap_collapses(
            answer=rec.answer,
            known_evidence_ids=set(rec.valid_evidence_ids),
            accepted_gap_statuses=rec.accepted_gap_statuses,
        )
        ok = not observed
        message = (
            "No anti-collapse failures." if ok else f"Violated invariants: {', '.join(observed)}"
        )
        results.append(
            CorpusResult(
                record_id=rec.record_id,
                ok=ok,
                observed_errors=observed,
                message=message,
            )
        )
    # Deterministic order by record_id so output is byte-stable across runs.
    results.sort(key=lambda r: r.record_id)
    return results
