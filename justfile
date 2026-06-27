set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

validate:
    uv run python tools/validate_okf.py

test:
    uv run pytest

smoke:
    uv run cep doctor

all: validate test smoke
