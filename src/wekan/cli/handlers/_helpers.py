"""
Shared helpers for handler functions.
"""

import json
import sys

from ..utils import format_output


def read_json_stdin():
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


def merge_fields_with_stdin(args):
    """Merge --json stdin data with -f fields. -f takes precedence."""
    fields = {}
    if getattr(args, "use_json", False):
        fields.update(read_json_stdin())
    if getattr(args, "fields", None):
        fields.update(args.fields)
    return fields


def output(data, fmt):
    """Format and print data."""
    print(format_output(data, fmt))


def error_exit(message):
    """Print error message to stderr and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def not_found(label):
    """Print not-found message and exit."""
    error_exit(f"{label} not found")


def resolve_card(client, card_id):
    """Fetch a card by ID or exit with not-found."""
    card = client.get_card_by_id(card_id)
    if not card:
        not_found(f"Card {card_id}")
    return card


def not_implemented(label):
    """Print not-implemented message and exit."""
    error_exit(f"Not implemented: {label}")
