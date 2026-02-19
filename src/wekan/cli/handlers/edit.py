"""
Handlers for the 'edit' action.
"""

import sys

from ._helpers import merge_fields_with_stdin, output


def handle_edit_card(client, args):
    fields = merge_fields_with_stdin(args)
    if not fields:
        print(
            "Error: No fields to update. Use -f key=value or --json.", file=sys.stderr
        )
        sys.exit(1)
    card = client.edit_card(args.board_id, args.list_id, args.card_id, **fields)
    output(card, args.format)


def handle_edit_checklist_item(client, args):
    fields = merge_fields_with_stdin(args)
    if not fields:
        print(
            "Error: No fields to update. Use -f key=value or --json.", file=sys.stderr
        )
        sys.exit(1)
    item = client.edit_checklist_item(
        args.board_id, args.card_id, args.checklist_id, args.item_id, **fields
    )
    output(item, args.format)
