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


def merge_fields(args):
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


def not_implemented(label):
    """Print not-implemented message and exit."""
    print(f"Error: Not implemented: {label}", file=sys.stderr)
    sys.exit(1)
