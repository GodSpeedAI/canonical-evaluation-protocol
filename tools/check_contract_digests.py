#!/usr/bin/env python3
"""Fail when a schema under schemas/extensions/ differs from its DIGESTS manifest.

Consumers vendor these schemas by digest. `--update` rewrites the manifest.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "schemas" / "extensions"
MANIFEST = DIR / "DIGESTS"


def current() -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DIR.glob("*.json"))}


def main(argv: list[str]) -> int:
    actual = current()
    if "--update" in argv:
        MANIFEST.write_text("".join(f"{d}  {n}\n" for n, d in actual.items()), encoding="utf-8")
        return 0
    recorded: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        recorded[name] = digest
    bad = [n for n in sorted(set(actual) | set(recorded)) if actual.get(n) != recorded.get(n)]
    for name in bad:
        print(f"DIGEST MISMATCH {name}: manifest={recorded.get(name)} actual={actual.get(name)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
