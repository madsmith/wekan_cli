"""
WeKan CLI - Command line interface for WeKan REST API
"""

import sys

import click

from . import __version__
from .client import WeKanClient
from .utils import format_output, handle_errors, resolve_env, with_client_login


@click.group()
@click.version_option(version=__version__)
def main():
    """
    WeKan CLI - Command line interface for WeKan REST API

    This tool allows you to interact with WeKan Kanban boards via REST API
    from the command line. It provides commands to manage boards, lists, and cards.

    Authentication can be provided via command-line options or environment variables:
    - WEKAN_URL: Base URL of your WeKan instance
    - WEKAN_USERNAME: Your username
    - WEKAN_PASSWORD: Your password
    - WEKAN_TOKEN: Authentication token (alternative to username/password)
    """
    pass


@main.command()
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
def login(url, username, password, token, output_format):
    """Login to WeKan and get authentication token"""
    if token:
        click.echo("Token provided, no need to login", err=True)
        return

    url = resolve_env(url, "URL")
    if not url:
        click.echo(
            "Error: WeKan URL is required. Provide via --url or WEKAN_URL environment variable.",
            err=True,
        )
        sys.exit(1)

    if not username:
        username = click.prompt("Username")
    if not password:
        password = click.prompt("Password", hide_input=True)

    client = WeKanClient(url, username, password)

    result = client.login()
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("user_name", required=False)
@click.option("--userid", help="Filter boards by user ID")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def boards(client: WeKanClient, user_name, userid, output_format):
    """List all public boards or boards visible to USER_NAME or --userid."""
    if user_name:
        users = client.get_users()
        match = next(
            (u for u in users if u.username.lower() == user_name.lower()), None
        )
        if not match:
            click.echo(f"Error: User '{user_name}' not found", err=True)
            sys.exit(1)
        result = client.get_boards_for_user(match.userId)
    elif userid:
        result = client.get_boards_for_user(userid)
    else:
        result = client.get_boards()
    click.echo(format_output(result, output_format))


@main.command()
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def users(client: WeKanClient, output_format):
    """List all users"""
    result = client.get_users()
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def board(client: WeKanClient, board_id, output_format):
    """Get details of a specific board"""
    result = client.get_board(board_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def lists(client: WeKanClient, board_id, output_format):
    """List all lists in a board"""
    result = client.get_lists(board_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("list_id")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def cards(client: WeKanClient, board_id, list_id, output_format):
    """List all cards in a list"""
    result = client.get_cards(board_id, list_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("title")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def create_board(client: WeKanClient, title, output_format):
    """Create a new board"""
    result = client.create_board(title)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("title")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def create_list(client: WeKanClient, board_id, title, output_format):
    """Create a new list in a board"""
    result = client.create_list(board_id, title)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("list_id")
@click.argument("title")
@click.option("--description", help="Card description")
@click.option("--url", help="WeKan instance URL")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication", hide_input=True)
@click.option("--token", help="Authentication token")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "pretty", "simple"]),
    default="json",
    help="Output format",
)
@handle_errors
@with_client_login
def create_card(
    client: WeKanClient, board_id, list_id, title, description, output_format
):
    """Create a new card in a list"""
    result = client.create_card(board_id, list_id, title, description)
    click.echo(format_output(result, output_format))


if __name__ == "__main__":
    main()
