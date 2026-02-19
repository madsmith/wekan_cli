"""
Handlers for the 'create' action.
"""

from ._helpers import error_exit, merge_fields, output


def handle_create_board(client, args):
    fields = merge_fields(args)
    output(client.create_board(args.title, args.owner_id, **fields), args.format)


def handle_create_list(client, args):
    output(client.create_list(args.board_id, args.title), args.format)


def handle_create_card(client, args):
    fields = merge_fields(args)
    description = fields.pop("description", None)
    lst = client.get_list(args.board_id, args.list_id)
    if lst is None:
        error_exit(f"List {args.list_id} not found")
    output(
        client.create_card(
            args.board_id,
            args.list_id,
            args.title,
            args.author_id,
            lst.swimlaneId,
            description=description,
            **fields,
        ),
        args.format,
    )


def handle_create_comment(client, args):
    card = client.get_card_by_id(args.card_id)
    if card is None:
        error_exit(f"Card {args.card_id} not found")
    output(
        client.create_comment(card.boardId, args.card_id, args.author_id, args.comment),
        args.format,
    )


def handle_create_checklist(client, args):
    card = client.get_card_by_id(args.card_id)
    if card is None:
        error_exit(f"Card {args.card_id} not found")
    fields = merge_fields(args)
    items = fields.pop("items", None)
    output(
        client.create_checklist(card.boardId, args.card_id, args.title, items),
        args.format,
    )


def handle_create_checklist_item(client, args):
    card = client.get_card_by_id(args.card_id)
    if card is None:
        error_exit(f"Card {args.card_id} not found")
    output(
        client.create_checklist_item(
            card.boardId, args.card_id, args.checklist_id, args.title
        ),
        args.format,
    )


def handle_create_swimlane(client, args):
    output(client.create_swimlane(args.board_id, args.title), args.format)
