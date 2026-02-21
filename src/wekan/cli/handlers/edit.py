"""
Handlers for the 'edit' action.
"""

import argparse

from wekan.client import WeKanClient

from ._helpers import error_exit, merge_fields_with_stdin, output, resolve_card


def handle_edit_card(client: WeKanClient, args: argparse.Namespace) -> None:
    fields = merge_fields_with_stdin(args)
    if not fields:
        error_exit("No fields to update. Use -f key=value or --json.")
    card = resolve_card(client, args.card_id)
    result = client.edit_card(card.boardId, card.listId, args.card_id, **fields)
    output(result, args.format)


def handle_edit_checklist_item(client: WeKanClient, args: argparse.Namespace) -> None:
    fields = merge_fields_with_stdin(args)
    if not fields:
        error_exit("No fields to update. Use -f key=value or --json.")
    card = resolve_card(client, args.card_id)
    item = client.edit_checklist_item(
        card.boardId, args.card_id, args.checklist_id, args.item_id, **fields
    )
    output(item, args.format)
