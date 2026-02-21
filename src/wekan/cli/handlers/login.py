"""
Login handler for WeKan CLI.
"""

import argparse
import getpass
import sys

from ...client import WeKanClient
from ..utils import resolve_env


def handle_login(args: argparse.Namespace) -> None:
    """Authenticate and print the token."""

    def display_login_info(client: WeKanClient):
        print("Logged In")
        print(f"  Token: {client.token}")
        if client.user_id:
            print(f"  User ID: {client.user_id}")

    url = resolve_env(getattr(args, "url", None), "URL")

    if not url:
        print(
            "Error: WeKan URL required. Use --url or set WEKAN_URL.",
            file=sys.stderr,
        )
        sys.exit(1)

    username = resolve_env(getattr(args, "username", None), "USERNAME")
    password = resolve_env(getattr(args, "password", None), "PASSWORD")
    token = resolve_env(getattr(args, "token", None), "TOKEN")

    # Try existing token if no credentials provided
    if token and not (username or password):
        client = WeKanClient(url, token=token)
        try:
            user = client.get_user()
            client.user_id = user.userId
            display_login_info(client)
            return
        except Exception:
            print("Invalid session token", file=sys.stderr)

    # Prompt for missing credentials
    if not username:
        username = input("Username: ")
    if not password:
        password = getpass.getpass("Password: ")

    client = WeKanClient(url, username, password)
    client.login()
    display_login_info(client)
