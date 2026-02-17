"""
Utility functions for WeKan CLI.
"""

import functools
import json
import os
import sys

import click


def _to_serializable(data):
    """Convert Pydantic models to dicts for output formatting."""
    if isinstance(data, list):
        return [_to_serializable(item) for item in data]
    if hasattr(data, "model_dump"):
        return data.model_dump()
    return data


def format_output(data, format_type: str = "json", indent_level: int = 0):
    """
    Format output data for display

    Args:
        data: Data to format
        format_type: Output format (json, pretty, simple)
        indent_level: Current indentation level for nested structures

    Returns:
        Formatted string
    """
    data = _to_serializable(data)
    if format_type == "json":
        return json.dumps(data, indent=2)
    elif format_type == "pretty":
        indent = "  " * indent_level
        if isinstance(data, list):
            result = []
            for item in data:
                if isinstance(item, dict):
                    nested = format_output(item, "pretty", indent_level + 1)
                    result.append(f"{indent}- {nested.lstrip()}")
                elif isinstance(item, list):
                    nested = format_output(item, "pretty", indent_level + 1)
                    result.append(f"{indent}- {nested.lstrip()}")
                else:
                    result.append(f"{indent}- {item}")
            return "\n".join(result)
        elif isinstance(data, dict):
            result = []
            for k, v in data.items():
                if isinstance(v, dict):
                    result.append(f"{indent}{k}:")
                    nested = format_output(v, "pretty", indent_level + 1)
                    result.append(nested)
                elif isinstance(v, list):
                    result.append(f"{indent}{k}:")
                    nested = format_output(v, "pretty", indent_level + 1)
                    result.append(nested)
                else:
                    result.append(f"{indent}{k}: {v}")
            return "\n".join(result)
        else:
            return str(data)
    else:
        return str(data)


def resolve_env(value: str | None, key: str) -> str | None:
    """Return value if specified, otherwise os.getenv('WEKAN_{key}')."""
    return value or os.getenv(f"WEKAN_{key}")


def handle_errors(f):
    """Decorator that catches exceptions, prints to stderr, and exits."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

    return wrapper
