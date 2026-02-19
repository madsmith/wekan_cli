"""
Handlers for the 'get' action.
"""

from ._helpers import not_implemented, output


def handle_get_board(client, args):
    output(client.get_board(args.board_id), args.format)


def handle_get_list(client, args):
    not_implemented("get list")


def handle_get_swimlane(client, args):
    not_implemented("get swimlane")


def handle_get_card(client, args):
    if args.board_id and args.list_id:
        output(client.get_card(args.board_id, args.list_id, args.card_id), args.format)
    else:
        output(client.get_card_by_id(args.card_id), args.format)


def handle_get_checklist(client, args):
    output(
        client.get_checklist(args.board_id, args.card_id, args.checklist_id),
        args.format,
    )


def handle_get_checklist_item(client, args):
    output(
        client.get_checklist_item(
            args.board_id, args.card_id, args.checklist_id, args.item_id
        ),
        args.format,
    )


def handle_get_comment(client, args):
    not_implemented("get comment")
