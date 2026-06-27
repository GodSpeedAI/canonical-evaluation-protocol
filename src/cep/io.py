from __future__ import annotations

import json
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from cep.json_types import JsonObject, JsonObjectError

JSON_OBJECT_ADAPTER = TypeAdapter(JsonObject)


def _read_json_object(path: Path) -> JsonObject:
    try:
        return JSON_OBJECT_ADAPTER.validate_json(path.read_bytes())
    except ValidationError as exc:
        raise JsonObjectError(path, str(exc)) from exc


def load_json(path: Path) -> JsonObject:
    return _read_json_object(path)


def write_json(path: Path, payload: JsonObject) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
