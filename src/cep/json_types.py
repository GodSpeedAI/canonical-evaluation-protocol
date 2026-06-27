from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

from pydantic import JsonValue
from typing_extensions import override

JsonObject: TypeAlias = dict[str, JsonValue]


class JsonDocumentError(Exception):
    pass


class JsonObjectError(JsonDocumentError):
    def __init__(self, path: Path, reason: str = "must contain a JSON object") -> None:
        self.path: Path
        self.reason: str
        self.path = path
        self.reason = reason
        super().__init__(str(self))

    @override
    def __str__(self) -> str:
        return f"{self.path} {self.reason}"
