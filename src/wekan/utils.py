"""
Utility functions for WeKan CLI.
"""

import functools
import json
import os
import sys

import click

from .client import WeKanClient


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


def with_client_login(fn):
    """Decorator that creates a WeKanClient from url/username/password/token
    kwargs, performs login if needed, and passes client to the wrapped function."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        url = kwargs.pop("url", None)
        username = kwargs.pop("username", None)
        password = kwargs.pop("password", None)
        token = kwargs.pop("token", None)

        base_url = resolve_env(url, "URL")
        username = resolve_env(username, "USERNAME")
        password = resolve_env(password, "PASSWORD")
        token = resolve_env(token, "TOKEN")

        if not base_url:
            click.echo(
                "Error: WeKan URL is required. Provide via --url or WEKAN_URL environment variable.",
                err=True,
            )
            sys.exit(1)

        client = WeKanClient(base_url, username, password, token)

        if not token and username and password:
            client.login()

        return fn(client, *args, **kwargs)

    return wrapper
