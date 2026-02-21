"""
Shared helpers for handler functions.
"""

from __future__ import annotations

import argparse
import json
import sys
import types as _types
import typing
from typing import Any, NoReturn

from pydantic.fields import FieldInfo

from wekan.client import CardDetails, WeKanClient, WeKanModel

from ..utils import format_output


def _resolve_field_info(
    model: type[WeKanModel], key: str
) -> FieldInfo | None:
    """Look up a field by name, falling back to edit_key metadata."""
    info = model.model_fields.get(key)
    if info:
        return info
    for _name, fi in model.model_fields.items():
        extra = fi.json_schema_extra if isinstance(fi.json_schema_extra, dict) else {}
        if extra.get("edit_key") == key:
            return fi
    return None


def _unwrap_annotation(ann: Any) -> tuple[Any, bool, bool]:
    """Unwrap Optional and list from a type annotation.

    Returns (base_type, is_list, is_optional).
    """
    is_optional = False
    is_list = False

    # Unwrap X | None
    if isinstance(ann, _types.UnionType):
        args = [a for a in typing.get_args(ann) if a is not type(None)]
        if len(args) == 1:
            is_optional = True
            ann = args[0]

    # Unwrap list[X]
    origin = typing.get_origin(ann)
    if origin is list:
        is_list = True
        list_args = typing.get_args(ann)
        if list_args:
            ann = list_args[0]

    return ann, is_list, is_optional


def _strip_quotes(s: str) -> str:
    """Remove matching outer quotes from a string."""
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


def _coerce_str(value: str) -> str:
    return _strip_quotes(value)


def _coerce_bool(value: str) -> bool:
    return value.lower() in ("true", "yes")


def _coerce_int(value: str) -> int | str:
    try:
        return int(value)
    except ValueError:
        return value


def _coerce_float(value: str) -> float | str:
    try:
        return float(value)
    except ValueError:
        return value


def _coerce_list(value: str) -> list[str]:
    if value.startswith("["):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        value = value[1:-1] if value.endswith("]") else value[1:]
    if "," in value:
        return [_strip_quotes(item.strip()) for item in value.split(",")]
    return [_strip_quotes(value)]


def coerce_value(value: str, field_info: FieldInfo | None = None) -> Any:
    """Coerce a string value using field type info, or heuristics as fallback."""
    if field_info is not None:
        ann = field_info.annotation
        base, is_list, is_optional = _unwrap_annotation(ann)

        if is_optional and value.lower() in ("", "null", "none"):
            return None
        if is_list:
            return _coerce_list(value)
        if isinstance(base, type) and issubclass(base, bool):
            return _coerce_bool(value)
        if isinstance(base, type) and issubclass(base, int):
            return _coerce_int(value)
        if isinstance(base, type) and issubclass(base, float):
            return _coerce_float(value)
        return _coerce_str(value)

    # No field info — heuristic fallback
    if value.lower() in ("null", "none"):
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith(("[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    return value


def read_json_stdin() -> dict[str, Any]:
    """Read a JSON object from stdin."""
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print("Error: JSON input must be an object", file=sys.stderr)
        sys.exit(1)
    return data


def merge_fields_with_stdin(
    args: argparse.Namespace,
    model: type[WeKanModel] | None = None,
) -> dict[str, Any]:
    """Merge --json stdin data with -f fields. -f takes precedence.

    When *model* is provided, string values from -f flags are coerced to the
    type declared in the model's field annotations.  Values from --json are
    already typed and are not coerced.
    """
    json_fields: dict[str, Any] = {}
    if getattr(args, "use_json", False):
        json_fields = read_json_stdin()

    cli_fields: dict[str, Any] = {}
    if getattr(args, "fields", None):
        for key, value in args.fields.items():
            if isinstance(value, str) and model is not None:
                field_info = _resolve_field_info(model, key)
                cli_fields[key] = coerce_value(value, field_info)
            else:
                cli_fields[key] = value

    return {**json_fields, **cli_fields}


def output(data: Any, fmt: str) -> None:
    """Format and print data."""
    print(format_output(data, fmt))


def error_exit(message: str) -> NoReturn:
    """Print error message to stderr and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def not_found(label: str) -> NoReturn:
    """Print not-found message and exit."""
    error_exit(f"{label} not found")


def resolve_card(client: WeKanClient, card_id: str) -> CardDetails:
    """Fetch a card by ID or exit with not-found."""
    card = client.get_card_by_id(card_id)
    if not card:
        not_found(f"Card {card_id}")
    return card


def not_implemented(label: str) -> NoReturn:
    """Print not-implemented message and exit."""
    error_exit(f"Not implemented: {label}")
