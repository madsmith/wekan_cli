"""
WeKan CLI - Command line interface for WeKan REST API
"""

import sys

import click

from . import __version__
from .client import WeKanClient
from .utils import format_output, handle_errors, resolve_env, wekan_command


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
@wekan_command
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
@wekan_command
def users(client: WeKanClient, output_format):
    """List all users"""
    result = client.get_users()
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@wekan_command
def board(client: WeKanClient, board_id, output_format):
    """Get details of a specific board"""
    result = client.get_board(board_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@wekan_command
def lists(client: WeKanClient, board_id, output_format):
    """List all lists in a board"""
    result = client.get_lists(board_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@wekan_command
def swimlanes(client: WeKanClient, board_id, output_format):
    """List all swimlanes in a board"""
    result = client.get_swimlanes(board_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("list_id")
@wekan_command
def cards(client: WeKanClient, board_id, list_id, output_format):
    """List all cards in a list"""
    result = client.get_cards(board_id, list_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("card_id")
@click.argument("board_id", required=False)
@click.argument("list_id", required=False)
@wekan_command
def card(client: WeKanClient, card_id, board_id, list_id, output_format):
    """Get details of a specific card.

    With one argument, looks up by CARD_ID only.
    With three arguments: CARD_ID BOARD_ID LIST_ID.
    """
    if board_id and list_id:
        result = client.get_card(board_id, list_id, card_id)
    else:
        result = client.get_card_by_id(card_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("title")
@click.argument("owner_id")
@wekan_command
def create_board(client: WeKanClient, title, owner_id, output_format):
    """Create a new board"""
    result = client.create_board(title, owner_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("title")
@wekan_command
def create_list(client: WeKanClient, board_id, title, output_format):
    """Create a new list in a board"""
    result = client.create_list(board_id, title)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("list_id")
@click.argument("title")
@click.argument("author_id")
@click.argument("swimlane_id")
@click.option("--description", help="Card description")
@wekan_command
def create_card(
    client: WeKanClient,
    board_id,
    list_id,
    title,
    author_id,
    swimlane_id,
    description,
    output_format,
):
    """Create a new card in a list"""
    result = client.create_card(
        board_id, list_id, title, author_id, swimlane_id, description
    )
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("list_id")
@click.argument("card_id")
@click.option("--title", help="New title")
@click.option("--description", help="New description")
@click.option("--board-id", "new_board_id", help="New board ID")
@click.option("--list-id", "new_list_id", help="New list ID (move card)")
@click.option("--swimlane-id", "new_swimlane_id", help="New swimlane ID")
@click.option("--color", help="New color")
@click.option("--label-ids", help="New label IDs (comma-separated)")
@click.option("--members", help="New member IDs (comma-separated)")
@click.option("--assignees", help="New assignee IDs (comma-separated)")
@click.option("--requested-by", help="New requestedBy value")
@click.option("--assigned-by", help="New assignedBy value")
@click.option("--due-at", help="New due date")
@click.option("--start-at", help="New start date")
@click.option("--end-at", help="New end date")
@click.option("--received-at", help="New received date")
@click.option("--spent-time", help="New spent time")
@click.option("--is-over-time", type=bool, help="Is over time")
@click.option("--archive", help="Archive value")
@click.option("--sort", help="New sort value")
@click.option("--parent-id", help="New parent card ID")
@click.option("--author-id", help="New author ID")
@wekan_command
def edit_card(
    client: WeKanClient, board_id, list_id, card_id, output_format, **options
):
    """Edit a card's fields. Only provided options are sent."""
    field_map = {
        "new_board_id": "newBoardId",
        "new_list_id": "newListId",
        "new_swimlane_id": "newSwimlaneId",
        "archive": "archive",
        "title": "title",
        "description": "description",
        "color": "color",
        "label_ids": "labelIds",
        "members": "members",
        "assignees": "assignees",
        "requested_by": "requestedBy",
        "assigned_by": "assignedBy",
        "due_at": "dueAt",
        "start_at": "startAt",
        "end_at": "endAt",
        "received_at": "receivedAt",
        "spent_time": "spentTime",
        "is_over_time": "isOverTime",
        "sort": "sort",
        "parent_id": "parentId",
        "author_id": "authorId",
    }
    kwargs = {}
    for opt_key, api_key in field_map.items():
        val = options.get(opt_key)
        if val is not None:
            kwargs[api_key] = val

    if not kwargs:
        click.echo("Error: No fields to update. Provide at least one option.", err=True)
        sys.exit(1)
    result = client.edit_card(board_id, list_id, card_id, **kwargs)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("list_id")
@click.argument("card_id")
@wekan_command(format_option=False)
def delete_card(client: WeKanClient, board_id, list_id, card_id):
    """Delete a card"""
    client.delete_card(board_id, list_id, card_id)
    click.echo("Card deleted.", err=True)


@main.command()
@click.argument("board_id")
@click.argument("swimlane_id")
@wekan_command
def swimlane_cards(client: WeKanClient, board_id, swimlane_id, output_format):
    """List all cards in a swimlane"""
    result = client.get_swimlane_cards(board_id, swimlane_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@wekan_command
def comments(client: WeKanClient, board_id, card_id, output_format):
    """List all comments on a card"""
    result = client.get_comments(board_id, card_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@click.argument("author_id")
@click.argument("comment")
@wekan_command
def create_comment(
    client: WeKanClient, board_id, card_id, author_id, comment, output_format
):
    """Add a comment to a card"""
    result = client.create_comment(board_id, card_id, author_id, comment)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@wekan_command
def checklists(client: WeKanClient, board_id, card_id, output_format):
    """List all checklists on a card"""
    result = client.get_checklists(board_id, card_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@click.argument("title")
@click.option("--items", help="Comma-separated list of checklist items")
@wekan_command
def create_checklist(
    client: WeKanClient, board_id, card_id, title, items, output_format
):
    """Create a checklist on a card"""
    result = client.create_checklist(board_id, card_id, title, items)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@click.argument("checklist_id")
@wekan_command
def checklist(client: WeKanClient, board_id, card_id, checklist_id, output_format):
    """Get details of a specific checklist"""
    result = client.get_checklist(board_id, card_id, checklist_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@click.argument("checklist_id")
@click.argument("title")
@wekan_command
def create_checklist_item(
    client: WeKanClient, board_id, card_id, checklist_id, title, output_format
):
    """Add a new item to a checklist"""
    result = client.create_checklist_item(board_id, card_id, checklist_id, title)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@click.argument("checklist_id")
@click.argument("item_id")
@wekan_command
def checklist_item(
    client: WeKanClient, board_id, card_id, checklist_id, item_id, output_format
):
    """Get a checklist item"""
    result = client.get_checklist_item(board_id, card_id, checklist_id, item_id)
    click.echo(format_output(result, output_format))


@main.command()
@click.argument("board_id")
@click.argument("card_id")
@click.argument("checklist_id")
@click.argument("item_id")
@click.option("--title", help="New title")
@click.option("--sort", type=int, help="Sort order")
@click.option("--is-finished", type=bool, help="Mark item as finished or not")
@wekan_command
def edit_checklist_item(
    client: WeKanClient,
    board_id,
    card_id,
    checklist_id,
    item_id,
    title,
    is_finished,
    output_format,
):
    """Edit a checklist item"""
    kwargs = {}
    if title is not None:
        kwargs["title"] = title
    if is_finished is not None:
        kwargs["isFinished"] = str(is_finished).lower()
    if not kwargs:
        click.echo("Error: No fields to update. Provide at least one option.", err=True)
        sys.exit(1)
    result = client.edit_checklist_item(
        board_id, card_id, checklist_id, item_id, **kwargs
    )
    click.echo(format_output(result, output_format))


if __name__ == "__main__":
    main()
