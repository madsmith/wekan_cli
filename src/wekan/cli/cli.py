"""
WeKan CLI - Command line interface for WeKan REST API
"""

import argparse
import os
import sys

from pydantic import ValidationError

from .. import __version__
from ..client import (
    BoardDetails,
    CardDetails,
    ChecklistDetails,
    ChecklistItemDetails,
    CommentDetails,
    ListDetails,
    SwimlaneDetails,
    WeKanAPIError,
    WeKanClient,
    WeKanModel,
)
from .handlers import (
    handle_create_board,
    handle_create_card,
    handle_create_checklist,
    handle_create_checklist_item,
    handle_create_comment,
    handle_create_list,
    handle_create_swimlane,
    handle_delete_board,
    handle_delete_card,
    handle_delete_checklist,
    handle_delete_checklist_item,
    handle_delete_comment,
    handle_delete_list,
    handle_delete_swimlane,
    handle_edit_card,
    handle_edit_checklist_item,
    handle_get_board,
    handle_get_card,
    handle_get_checklist,
    handle_get_checklist_item,
    handle_get_comment,
    handle_get_list,
    handle_get_swimlane,
    handle_list_boards,
    handle_list_cards,
    handle_list_checklists,
    handle_list_comments,
    handle_list_lists,
    handle_list_swimlanes,
    handle_list_users,
    handle_login,
)
from .utils import resolve_env

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class KeyValueAction(argparse.Action):
    """Parse repeated -f key=value into a dict."""

    def __call__(self, parser, namespace, values, option_string=None):
        if values is None or not isinstance(values, str) or "=" not in values:
            parser.error(f"invalid field format '{values}', expected key=value")
        key, value = values.split("=", 1)
        fields = getattr(namespace, self.dest, None) or {}
        fields[key] = value
        setattr(namespace, self.dest, fields)


def create_client(args):
    """Create and authenticate a WeKanClient from parsed args."""
    url = resolve_env(getattr(args, "url", None), "URL")
    username = resolve_env(getattr(args, "username", None), "USERNAME")
    password = resolve_env(getattr(args, "password", None), "PASSWORD")
    token = resolve_env(getattr(args, "token", None), "TOKEN")

    if not url:
        print(
            "Error: WeKan URL required. Use --url or set WEKAN_URL.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = WeKanClient(url, username, password, token)

    if not token and username and password:
        client.login()

    return client


def add_data_field_options(parser):
    """Add -f/--field and --json options to a subparser."""
    parser.add_argument(
        "-f",
        "--field",
        dest="fields",
        action=KeyValueAction,
        metavar="KEY=VALUE",
        help="Set a field (repeatable)",
    )
    parser.add_argument(
        "--json",
        dest="use_json",
        action="store_true",
        default=False,
        help="Read JSON object from stdin",
    )


# ---------------------------------------------------------------------------
# Help text constants
# ---------------------------------------------------------------------------


def _fields_help(model, label):
    """Generate a help string listing fields and descriptions from a Pydantic model."""
    import types as _types
    import typing

    lines = [f"{label}:"]

    col = 28  # column where descriptions start

    def _type_label(cls):
        """Return config title or convert 'BoardMember' to 'Board Member'."""
        title = cls.model_config.get("title")
        if title:
            return title
        import re

        return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", cls.__name__)

    def _collect(mdl, depth=0):
        indent = "  " * (depth + 1)
        for name, info in mdl.model_fields.items():
            desc = info.description or ""
            field = f"{indent}{name}"
            padding = max(1, col - len(field))
            lines.append(f"{field}{' ' * padding}{desc}")
            # Unwrap Optional (X | None) and list[X] to check for nested WeKanModel
            ann = info.annotation
            if isinstance(ann, _types.UnionType):
                args = [a for a in typing.get_args(ann) if a is not type(None)]
                if len(args) == 1:
                    ann = args[0]
            origin = typing.get_origin(ann)
            if origin is list:
                list_args = typing.get_args(ann)
                if list_args:
                    ann = list_args[0]
            if isinstance(ann, type) and issubclass(ann, WeKanModel):
                child_indent = "  " * (depth + 2)
                lines.append(f"{child_indent}{_type_label(ann)} fields:")
                _collect(ann, depth + 2)

    _collect(model)
    schema_extra = model.model_config.get("json_schema_extra") or {}
    if schema_extra.get("partial_field_def"):
        lines.append("")
        lines.append("Partial field list, consult API docs for full object schema")
    return "\n".join(lines)


BOARD_FIELDS_HELP = _fields_help(BoardDetails, "board fields")
LIST_FIELDS_HELP = _fields_help(ListDetails, "list fields")
SWIMLANE_FIELDS_HELP = _fields_help(SwimlaneDetails, "swimlane fields")
CARD_FIELDS_HELP = _fields_help(CardDetails, "card fields")
COMMENT_FIELDS_HELP = _fields_help(CommentDetails, "comment fields")
CHECKLIST_FIELDS_HELP = _fields_help(ChecklistDetails, "checklist fields")
CHECKLIST_ITEM_FIELDS_HELP = _fields_help(ChecklistItemDetails, "checklist-item fields")


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _build_parser_action_get(actions):
    get_parser = actions.add_parser(
        "get",
        help="Get a single resource by ID",
        description="Get a single resource by ID.",
        epilog="Run 'wekancli get TYPE --help' for type-specific arguments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    types = get_parser.add_subparsers(dest="type", title="types", metavar="TYPE")

    p = types.add_parser("board", help="Get board details")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.set_defaults(handler=handle_get_board)

    p = types.add_parser("list", help="Get list details")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("list_id", metavar="LIST_ID")
    p.set_defaults(handler=handle_get_list)

    p = types.add_parser("swimlane", help="Get swimlane details")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("swimlane_id", metavar="SWIMLANE_ID")
    p.set_defaults(handler=handle_get_swimlane)

    p = types.add_parser("card", help="Get card details")
    p.add_argument("card_id", metavar="CARD_ID")
    p.set_defaults(handler=handle_get_card)

    p = types.add_parser("checklist", help="Get checklist details")
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("checklist_id", metavar="CHECKLIST_ID")
    p.set_defaults(handler=handle_get_checklist)

    p = types.add_parser("checklist-item", help="Get checklist item details")
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("checklist_id", metavar="CHECKLIST_ID")
    p.add_argument("item_id", metavar="ITEM_ID")
    p.set_defaults(handler=handle_get_checklist_item)

    p = types.add_parser("comment", help="Get comment details")
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("comment_id", metavar="COMMENT_ID")
    p.set_defaults(handler=handle_get_comment)


def _build_parser_action_list(actions):
    list_parser = actions.add_parser(
        "list",
        help="List resources",
        description="List resources.",
        epilog="Run 'wekancli list TYPE --help' for type-specific arguments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    types = list_parser.add_subparsers(dest="type", title="types", metavar="TYPE")

    p = types.add_parser("boards", help="List boards")
    p.add_argument("user_id", metavar="USER_ID", nargs="?", help="Filter by user ID")
    p.set_defaults(handler=handle_list_boards)

    p = types.add_parser("lists", help="List lists in a board")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.set_defaults(handler=handle_list_lists)

    p = types.add_parser("swimlanes", help="List swimlanes in a board")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.set_defaults(handler=handle_list_swimlanes)

    p = types.add_parser("cards", help="List cards in a list or swimlane")
    p.add_argument("board_id", metavar="BOARD_ID")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--list-id", metavar="LIST_ID", help="List cards in a list")
    source.add_argument(
        "--swimlane-id", metavar="SWIMLANE_ID", help="List cards in a swimlane"
    )
    p.set_defaults(handler=handle_list_cards)

    p = types.add_parser("users", help="List all users")
    p.set_defaults(handler=handle_list_users)

    p = types.add_parser("comments", help="List comments on a card")
    p.add_argument("card_id", metavar="CARD_ID")
    p.set_defaults(handler=handle_list_comments)

    p = types.add_parser("checklists", help="List checklists on a card")
    p.add_argument("card_id", metavar="CARD_ID")
    p.set_defaults(handler=handle_list_checklists)


def _build_parser_action_create(actions):
    create_parser = actions.add_parser(
        "create",
        help="Create a new resource",
        description="Create a new resource.",
        epilog="Run 'wekancli create TYPE --help' for type-specific arguments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    types = create_parser.add_subparsers(dest="type", title="types", metavar="TYPE")

    p = types.add_parser(
        "board",
        help="Create a board",
        epilog=BOARD_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("title", metavar="TITLE")
    p.add_argument("owner_id", metavar="OWNER_ID")
    add_data_field_options(p)
    p.set_defaults(handler=handle_create_board)

    p = types.add_parser(
        "list",
        help="Create a list in a board",
        epilog=LIST_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("title", metavar="TITLE")
    p.set_defaults(handler=handle_create_list)

    p = types.add_parser(
        "card",
        help="Create a card",
        epilog=CARD_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("list_id", metavar="LIST_ID")
    p.add_argument("title", metavar="TITLE")
    p.add_argument("author_id", metavar="AUTHOR_ID")
    add_data_field_options(p)
    p.set_defaults(handler=handle_create_card)

    p = types.add_parser(
        "comment",
        help="Add a comment to a card",
        epilog=COMMENT_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("author_id", metavar="AUTHOR_ID")
    p.add_argument("comment", metavar="COMMENT")
    p.set_defaults(handler=handle_create_comment)

    p = types.add_parser(
        "checklist",
        help="Create a checklist on a card",
        epilog=CHECKLIST_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("title", metavar="TITLE")
    add_data_field_options(p)
    p.set_defaults(handler=handle_create_checklist)

    p = types.add_parser(
        "checklist-item",
        help="Add item to a checklist",
        epilog=CHECKLIST_ITEM_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("checklist_id", metavar="CHECKLIST_ID")
    p.add_argument("title", metavar="TITLE")
    p.set_defaults(handler=handle_create_checklist_item)

    p = types.add_parser(
        "swimlane",
        help="Create a swimlane in a board",
        epilog=SWIMLANE_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("title", metavar="TITLE")
    p.set_defaults(handler=handle_create_swimlane)


def _build_parser_action_edit(actions):
    edit_parser = actions.add_parser(
        "edit",
        help="Edit an existing resource",
        description="Edit an existing resource.",
        epilog="Run 'wekancli edit TYPE --help' for type-specific arguments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    types = edit_parser.add_subparsers(dest="type", title="types", metavar="TYPE")

    p = types.add_parser(
        "card",
        help="Edit a card",
        epilog=CARD_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("card_id", metavar="CARD_ID")
    add_data_field_options(p)
    p.set_defaults(handler=handle_edit_card)

    p = types.add_parser(
        "checklist-item",
        help="Edit a checklist item",
        epilog=CHECKLIST_ITEM_FIELDS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("checklist_id", metavar="CHECKLIST_ID")
    p.add_argument("item_id", metavar="ITEM_ID")
    add_data_field_options(p)
    p.set_defaults(handler=handle_edit_checklist_item)


def _build_parser_action_delete(actions):
    delete_parser = actions.add_parser(
        "delete",
        help="Delete a resource",
        description="Delete a resource.",
        epilog="Run 'wekancli delete TYPE --help' for type-specific arguments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    types = delete_parser.add_subparsers(dest="type", title="types", metavar="TYPE")

    p = types.add_parser("board", help="Delete a board")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.set_defaults(handler=handle_delete_board)

    p = types.add_parser("list", help="Delete a list")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("list_id", metavar="LIST_ID")
    p.set_defaults(handler=handle_delete_list)

    p = types.add_parser("card", help="Delete a card")
    p.add_argument("card_id", metavar="CARD_ID")
    p.set_defaults(handler=handle_delete_card)

    p = types.add_parser("swimlane", help="Delete a swimlane")
    p.add_argument("board_id", metavar="BOARD_ID")
    p.add_argument("swimlane_id", metavar="SWIMLANE_ID")
    p.set_defaults(handler=handle_delete_swimlane)

    p = types.add_parser("comment", help="Delete a comment")
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("comment_id", metavar="COMMENT_ID")
    p.set_defaults(handler=handle_delete_comment)

    p = types.add_parser("checklist", help="Delete a checklist")
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("checklist_id", metavar="CHECKLIST_ID")
    p.set_defaults(handler=handle_delete_checklist)

    p = types.add_parser("checklist-item", help="Delete a checklist item")
    p.add_argument("card_id", metavar="CARD_ID")
    p.add_argument("checklist_id", metavar="CHECKLIST_ID")
    p.add_argument("item_id", metavar="ITEM_ID")
    p.set_defaults(handler=handle_delete_checklist_item)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="wekancli",
        description="WeKan CLI - Kanban board management",
        epilog="Run 'wekancli ACTION --help' for action-specific types and arguments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"wekancli {__version__}"
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=["json", "json-pretty", "text"],
        default=None,
        help="Output format (default: json, env: WEKAN_OUTPUT_FORMAT)",
    )

    conn = parser.add_argument_group("connection options")
    conn.add_argument(
        "--url", metavar="URL", help="WeKan instance URL (env: WEKAN_URL)"
    )
    conn.add_argument(
        "--username", metavar="USER", help="Username (env: WEKAN_USERNAME)"
    )
    conn.add_argument(
        "--password", metavar="PASS", help="Password (env: WEKAN_PASSWORD)"
    )
    conn.add_argument("--token", metavar="TOKEN", help="Auth token (env: WEKAN_TOKEN)")

    actions = parser.add_subparsers(dest="action", title="actions", metavar="ACTION")
    p = actions.add_parser("login", help="Authenticate and print token")
    p.add_argument(
        "--username",
        metavar="USER",
        default=argparse.SUPPRESS,
        help="Username (env: WEKAN_USERNAME)",
    )
    p.add_argument(
        "--password",
        metavar="PASS",
        default=argparse.SUPPRESS,
        help="Password (env: WEKAN_PASSWORD)",
    )
    p.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Login with username/password even if a token is available",
    )
    p.set_defaults(handler=handle_login)
    _build_parser_action_get(actions)
    _build_parser_action_list(actions)
    _build_parser_action_create(actions)
    _build_parser_action_edit(actions)
    _build_parser_action_delete(actions)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.format is None:
        env_fmt = os.getenv("WEKAN_OUTPUT_FORMAT", "json").lower()
        if env_fmt in ("json", "json-pretty", "text"):
            args.format = env_fmt
        else:
            args.format = "json"

    if not args.action:
        parser.print_help()
        sys.exit(0)

    handler = getattr(args, "handler", None)
    if not handler:
        parser.parse_args([args.action, "--help"])
        sys.exit(0)

    try:
        if args.action == "login":
            handler(args)
        else:
            client = create_client(args)
            handler(client, args)
    except WeKanAPIError as e:
        print(f"Error: {e.error}", file=sys.stderr)
        sys.exit(1)
    except ValidationError:
        print("Error: API returned invalid response", file=sys.stderr)
        sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        print(f"Error: {e} ({type(e).__name__})", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
