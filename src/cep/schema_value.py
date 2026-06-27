from __future__ import annotations

import re
from typing import TYPE_CHECKING

from cep.io import load_json
from cep.json_types import JsonObject
from cep.schema_profile import SchemaProfile, as_object, as_string, as_string_list

if TYPE_CHECKING:
    from pydantic import JsonValue


def _json_type_name(value: JsonValue) -> str:
    match value:
        case bool():
            return "boolean"
        case str():
            return "string"
        case int() | float():
            return "number"
        case list():
            return "array"
        case dict():
            return "object"
        case None:
            return "null"


def _matches_type(value: JsonValue, expected_type: str) -> bool:
    match expected_type:
        case "array":
            return isinstance(value, list)
        case "boolean":
            return isinstance(value, bool)
        case "number":
            return isinstance(value, int | float) and not isinstance(value, bool)
        case "object":
            return isinstance(value, dict)
        case "string":
            return isinstance(value, str)
        case _:
            return False


def _number_bound_errors(value: JsonValue, schema: JsonObject, location: str) -> list[str]:
    match value:
        case int() | float() if not isinstance(value, bool):
            number_value = value
        case _:
            return []

    errors: list[str] = []
    minimum = schema.get("minimum")
    maximum = schema.get("maximum")
    if (
        isinstance(minimum, int | float)
        and not isinstance(minimum, bool)
        and number_value < minimum
    ):
        errors.append(f"{location} must be >= {minimum}")
    if (
        isinstance(maximum, int | float)
        and not isinstance(maximum, bool)
        and number_value > maximum
    ):
        errors.append(f"{location} must be <= {maximum}")
    return errors


def _resolve_ref(profile: SchemaProfile, ref: str) -> SchemaProfile:
    ref_path = profile.root / ref.removeprefix("./")
    return SchemaProfile(schema=load_json(ref_path), root=ref_path.parent)


def validate_value(value: JsonValue, profile: SchemaProfile, location: str) -> list[str]:
    schema = profile.schema
    ref = as_string(schema.get("$ref"))
    if ref:
        return validate_value(value, _resolve_ref(profile, ref), location)

    errors: list[str] = []
    expected_type = as_string(schema.get("type"))
    if expected_type and not _matches_type(value, expected_type):
        return [f"{location} must be {expected_type}, got {_json_type_name(value)}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{location} must equal {schema['const']}")

    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and value not in enum_values:
        errors.append(f"{location} must be one of {enum_values}")

    pattern = as_string(schema.get("pattern"))
    if pattern and isinstance(value, str) and re.fullmatch(pattern, value) is None:
        errors.append(f"{location} must match pattern {pattern}")

    errors.extend(_number_bound_errors(value, schema, location))
    errors.extend(_validate_nested(value, profile, location))
    return errors


def _validate_nested(value: JsonValue, profile: SchemaProfile, location: str) -> list[str]:
    match value:
        case dict():
            return validate_object(value, profile, location)
        case list():
            item_schema = as_object(profile.schema.get("items"))
            if item_schema is None:
                return []
            item_profile = SchemaProfile(schema=item_schema, root=profile.root)
            errors: list[str] = []
            for index, item in enumerate(value):
                errors.extend(validate_value(item, item_profile, f"{location}[{index}]"))
            return errors
        case _:
            return []


def validate_object(instance: JsonObject, profile: SchemaProfile, location: str = "$") -> list[str]:
    schema = profile.schema
    errors = [
        f"{location}: missing required field: {field}"
        for field in as_string_list(schema.get("required"))
        if field not in instance
    ]

    properties = as_object(schema.get("properties")) or {}
    if schema.get("additionalProperties") is False:
        errors.extend(
            f"{location}: unknown field: {field}" for field in instance if field not in properties
        )

    for field, field_schema_value in properties.items():
        field_schema = as_object(field_schema_value)
        if field_schema is None or field not in instance:
            continue
        errors.extend(
            validate_value(
                instance[field],
                SchemaProfile(schema=field_schema, root=profile.root),
                f"{location}.{field}",
            ),
        )

    return errors
