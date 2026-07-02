"""WP-2 (F-12) contract drift check for the cep repo.

cep owns the CEP-0008 semantic-envelope *profile* (`schemas/semantic-envelope.schema.json`)
and is also a consumer of the v1 wire schema (`sea.agent.event.v1.json`), which
its conformance fixtures validate against. This test pins the vendored v1 copy
to the canonical hash from hassos-addon-agent-memory-ledger's
`contracts/CONTRACTS_VERSION`.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

_SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "schemas"
    / "vendored"
    / "sea.agent.event.v1.json"
)
_PIN = "d2a245183f7a52672dec11d7a8e9236d3db78dac674ab066d944fb758443e195"


def test_vendored_v1_schema_matches_contracts_pin() -> None:
    digest = hashlib.sha256(_SCHEMA.read_bytes()).hexdigest()
    assert digest == _PIN, (
        "cep vendored v1 schema drifted from the ledger's CONTRACTS_VERSION pin"
    )
