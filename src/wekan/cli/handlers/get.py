"""
Handlers for the 'get' action.
"""

import sys

from ._helpers import output


def _not_found(label):
    print(f"{label} not found.", file=sys.stderr)
    raise SystemExit(1)


def handle_get_board(client, args):
    result = client.get_board(args.board_id)
    if result is None:
        _not_found("Board")
    output(result, args.format)


def handle_get_list(client, args):
    result = client.get_list(args.board_id, args.list_id)
    if result is None:
        _not_found("List")
    output(result, args.format)


def handle_get_swimlane(client, args):
    result = client.get_swimlane(args.board_id, args.swimlane_id)
    if result is None:
        _not_found("Swimlane")
    output(result, args.format)


def handle_get_card(client, args):
    if args.board_id and args.list_id:
        result = client.get_card(args.board_id, args.list_id, args.card_id)
    else:
        result = client.get_card_by_id(args.card_id)
    if result is None:
        _not_found("Card")
    output(result, args.format)


def handle_get_checklist(client, args):
    result = client.get_checklist(args.board_id, args.card_id, args.checklist_id)
    if result is None:
        _not_found("Checklist")
    output(result, args.format)


def handle_get_checklist_item(client, args):
    result = client.get_checklist_item(
        args.board_id, args.card_id, args.checklist_id, args.item_id
    )
    if result is None:
        _not_found("Checklist item")
    output(result, args.format)


def handle_get_comment(client, args):
    result = client.get_comment(args.board_id, args.card_id, args.comment_id)
    if result is None:
        _not_found("Comment")
    output(result, args.format)
