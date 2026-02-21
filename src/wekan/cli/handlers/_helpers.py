"""
Shared helpers for handler functions.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, NoReturn

from wekan.client import CardDetails, WeKanClient

from ..utils import format_output


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


def merge_fields_with_stdin(args: argparse.Namespace) -> dict[str, Any]:
    """Merge --json stdin data with -f fields. -f takes precedence."""
    fields: dict[str, Any] = {}
    if getattr(args, "use_json", False):
        fields.update(read_json_stdin())
    if getattr(args, "fields", None):
        fields.update(args.fields)
    return fields


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
