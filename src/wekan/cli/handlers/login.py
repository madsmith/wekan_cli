"""
Login handler for WeKan CLI.
"""

import getpass
import sys

from ...client import WeKanClient
from ..utils import resolve_env


def handle_login(args):
    """Authenticate and print the token."""

    def display_login_info(client: WeKanClient):
        print("Logged In")
        print(f"  Token: {client.token}")
        print(f"  User ID: {client.user_id}")

    url = resolve_env(getattr(args, "url", None), "URL")
    token = resolve_env(getattr(args, "token", None), "TOKEN")

    if not url:
        print(
            "Error: WeKan URL required. Use --url or set WEKAN_URL.",
            file=sys.stderr,
        )
        sys.exit(1)

    force = getattr(args, "force", False)

    if token and not force:
        client = WeKanClient(url, token=token)
        try:
            # Test token authorization
            client.get_boards()
            display_login_info(client)
            return
        except Exception:
            print("Invalid session token", file=sys.stderr)

    username = resolve_env(getattr(args, "username", None), "USERNAME")
    password = resolve_env(getattr(args, "password", None), "PASSWORD")

    if not username:
        username = input("Username: ")
    if not password:
        password = getpass.getpass("Password: ")

    client = WeKanClient(url, username, password)
    client.login()
    display_login_info(client)
