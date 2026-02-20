"""
Handlers for the 'create' action.
"""

from ._helpers import error_exit, merge_fields_with_stdin, not_found, output


def handle_create_label(client, args):
    label_id = client.add_board_label(args.board_id, args.name, args.color)
    if label_id is None:
        error_exit("Label already exists on this board.")
    output({"labelId": label_id}, args.format)


def handle_create_board(client, args):
    fields = merge_fields_with_stdin(args)
    board = client.create_board(args.title, args.owner_id, **fields)
    output(board, args.format)


def handle_create_list(client, args):
    lst = client.create_list(args.board_id, args.title)
    output(lst, args.format)


def handle_create_card(client, args):
    fields = merge_fields_with_stdin(args)
    description = fields.pop("description", None)
    lst = client.get_list(args.board_id, args.list_id)
    if lst is None:
        not_found(f"List {args.list_id}")
    card = client.create_card(
        args.board_id,
        args.list_id,
        args.title,
        args.author_id,
        lst.swimlaneId,
        description=description,
        **fields,
    )
    output(card, args.format)


def handle_create_comment(client, args):
    card = client.get_card_by_id(args.card_id)
    if card is None:
        not_found(f"Card {args.card_id}")
    comment = client.create_comment(
        card.boardId, args.card_id, args.author_id, args.comment
    )
    output(comment, args.format)


def handle_create_checklist(client, args):
    card = client.get_card_by_id(args.card_id)
    if card is None:
        not_found(f"Card {args.card_id}")
    fields = merge_fields_with_stdin(args)
    items = fields.pop("items", None)
    checklist = client.create_checklist(card.boardId, args.card_id, args.title, items)
    output(checklist, args.format)


def handle_create_checklist_item(client, args):
    card = client.get_card_by_id(args.card_id)
    if card is None:
        not_found(f"Card {args.card_id}")
    item = client.create_checklist_item(
        card.boardId, args.card_id, args.checklist_id, args.title
    )
    output(item, args.format)


def handle_create_swimlane(client, args):
    swimlane = client.create_swimlane(args.board_id, args.title)
    output(swimlane, args.format)
