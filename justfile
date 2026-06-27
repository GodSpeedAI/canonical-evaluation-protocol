set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

validate:
    uv run python tools/validate_okf.py
    uv run cep validate all

test:
    uv run pytest

conformance:
    uv run cep conformance anti-collapse

smoke:
    uv run cep run reality-gap-corpus

all: validate test conformance smoke
