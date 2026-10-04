from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from cep.json_types import JsonObject

if TYPE_CHECKING:
    from pydantic import JsonValue

SUPPORTED_SCHEMA_KEYS = {
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "allOf",
    "anyOf",
    "const",
    "description",
    "enum",
    "items",
    "maximum",
    "minimum",
    "minItems",
    "minLength",
    "minProperties",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
}


@dataclass(frozen=True, slots=True)
class SchemaProfile:
    schema: JsonObject
    root: Path


def as_object(value: JsonValue | None) -> JsonObject | None:
    match value:
        case dict():
            return value
        case _:
            return None


def as_string(value: JsonValue | None) -> str | None:
    match value:
        case str():
            return value
        case _:
            return None


def as_string_list(value: JsonValue | None) -> list[str]:
    match value:
        case list():
            items: list[str] = []
            for item in value:
                match item:
                    case str():
                        items.append(item)
                    case _:
                        continue
            return items
        case _:
            return []


def _required_errors(schema: JsonObject, location: str) -> list[str]:
    if "required" not in schema:
        return []
    required = schema["required"]
    match required:
        case list():
            errors: list[str] = []
            for index, item in enumerate(required):
                match item:
                    case str() if item:
                        continue
                    case _:
                        errors.append(f"{location}.required[{index}] must be a non-empty string")
            return errors
        case _:
            return [f"{location}.required must be an array of strings"]


def _root_schema_errors(schema: JsonObject, location: str) -> list[str]:
    if location != "$":
        return []

    errors: list[str] = []
    if as_string(schema.get("$schema")) is None:
        errors.append("schema is missing $schema")
    if as_string(schema.get("title")) is None:
        errors.append("schema is missing title")
    if as_string(schema.get("type")) != "object":
        errors.append("schema type must be object")
    return errors


def _property_schema_errors(schema: JsonObject, location: str) -> list[str]:
    properties = as_object(schema.get("properties"))
    if "properties" in schema and properties is None:
        return [f"{location}.properties must be an object"]
    if not properties:
        return []

    errors: list[str] = []
    for field, field_schema in properties.items():
        nested = as_object(field_schema)
        if nested is None:
            errors.append(f"{location}.properties.{field} must be an object")
            continue
        errors.extend(_schema_profile_errors(nested, f"{location}.properties.{field}"))
    return errors


def _item_schema_errors(schema: JsonObject, location: str) -> list[str]:
    items = schema.get("items")
    if items is None:
        return []

    nested_items = as_object(items)
    if nested_items is None:
        return [f"{location}.items must be an object"]

    return _schema_profile_errors(nested_items, f"{location}.items")


def _all_of_schema_errors(schema: JsonObject, location: str) -> list[str]:
    all_of = schema.get("allOf")
    if all_of is None:
        return []

    if not isinstance(all_of, list) or not all_of:
        return [f"{location}.allOf must be a non-empty array"]

    errors: list[str] = []
    for index, branch in enumerate(all_of):
        nested = as_object(branch)
        if nested is None:
            errors.append(f"{location}.allOf[{index}] must be an object")
            continue
        errors.extend(_schema_profile_errors(nested, f"{location}.allOf[{index}]"))
    return errors


def _any_of_schema_errors(schema: JsonObject, location: str) -> list[str]:
    any_of = schema.get("anyOf")
    if any_of is None:
        return []

    if not isinstance(any_of, list) or not any_of:
        return [f"{location}.anyOf must be a non-empty array"]

    errors: list[str] = []
    for index, branch in enumerate(any_of):
        nested = as_object(branch)
        if nested is None:
            errors.append(f"{location}.anyOf[{index}] must be an object")
            continue
        errors.extend(_schema_profile_errors(nested, f"{location}.anyOf[{index}]"))
    return errors


def _schema_profile_errors(schema: JsonObject, location: str = "$") -> list[str]:
    errors = [
        f"{location}: unsupported schema keyword {key}"
        for key in schema
        if key not in SUPPORTED_SCHEMA_KEYS
    ]
    errors.extend(_root_schema_errors(schema, location))
    errors.extend(_required_errors(schema, location))
    errors.extend(_property_schema_errors(schema, location))
    errors.extend(_item_schema_errors(schema, location))
    errors.extend(_any_of_schema_errors(schema, location))
    errors.extend(_all_of_schema_errors(schema, location))

    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        errors.append(f"{location}.additionalProperties must be boolean")

    return errors


def schema_profile_errors(schema: JsonObject) -> list[str]:
    return _schema_profile_errors(schema)
