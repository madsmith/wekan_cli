"""
Handlers for the 'create' action.
"""

from ._helpers import merge_fields, output


def handle_create_board(client, args):
    fields = merge_fields(args)
    output(client.create_board(args.title, args.owner_id, **fields), args.format)


def handle_create_list(client, args):
    output(client.create_list(args.board_id, args.title), args.format)


def handle_create_card(client, args):
    fields = merge_fields(args)
    description = fields.pop("description", None)
    output(
        client.create_card(
            args.board_id,
            args.list_id,
            args.title,
            args.author_id,
            args.swimlane_id,
            description=description,
            **fields,
        ),
        args.format,
    )


def handle_create_comment(client, args):
    output(
        client.create_comment(
            args.board_id, args.card_id, args.author_id, args.comment
        ),
        args.format,
    )


def handle_create_checklist(client, args):
    fields = merge_fields(args)
    items = fields.pop("items", None)
    output(
        client.create_checklist(args.board_id, args.card_id, args.title, items),
        args.format,
    )


def handle_create_checklist_item(client, args):
    output(
        client.create_checklist_item(
            args.board_id, args.card_id, args.checklist_id, args.title
        ),
        args.format,
    )


def handle_create_swimlane(client, args):
    output(client.create_swimlane(args.board_id, args.title), args.format)
