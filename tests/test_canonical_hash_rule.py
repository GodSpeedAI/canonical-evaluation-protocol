"""CEP-0008 section 16.5: SHA-256 over RFC 8785 canonical JSON (real JCS library)."""

from __future__ import annotations

import hashlib
import json

import pytest
import rfc8785

from cep.paths import SCHEMAS_DIR

DOC = json.loads((SCHEMAS_DIR / "fixtures" / "canonical-hash" / "vectors.json").read_text("utf-8"))


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    out: dict = {}
    for key, value in pairs:
        if key in out:
            msg = f"duplicate member {key}"
            raise ValueError(msg)
        out[key] = value
    return out


@pytest.mark.parametrize("vec", DOC["vectors"], ids=lambda v: v["id"])
def test_vector_canonical_bytes_and_digest(vec: dict) -> None:
    canonical = rfc8785.dumps(json.loads(vec["input"], object_pairs_hook=_no_duplicates))
    assert canonical == vec["canonical"].encode("utf-8")
    assert canonical.hex() == vec["canonical_hex"]
    assert hashlib.sha256(canonical).hexdigest() == vec["sha256"]


def test_key_order_and_whitespace_do_not_change_the_digest() -> None:
    a = rfc8785.dumps(json.loads('{"a":1,"b":[1,2]}'))
    b = rfc8785.dumps(json.loads(' { "b" : [1, 2], "a" : 1.0 } '))
    assert a == b


def test_array_order_changes_the_digest() -> None:
    assert rfc8785.dumps([1, 2]) != rfc8785.dumps([2, 1])


@pytest.mark.parametrize("case", DOC["must_reject"], ids=lambda c: c["id"])
def test_inputs_the_rule_refuses(case: dict) -> None:
    def run() -> bytes:
        return rfc8785.dumps(json.loads(case["input"], object_pairs_hook=_no_duplicates))

    with pytest.raises((ValueError, TypeError, rfc8785.CanonicalizationError)):
        run()
