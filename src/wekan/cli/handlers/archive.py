"""
Handlers for the 'archive' action.
"""

import argparse
import sys

from wekan.client import WeKanClient

from ._helpers import resolve_card


def handle_archive_card(client: WeKanClient, args: argparse.Namespace) -> None:
    card = resolve_card(client, args.card_id)
    if args.restore:
        client.restore_card(card.boardId, card.listId, args.card_id)
        print("Restored.", file=sys.stderr)
    else:
        client.archive_card(card.boardId, card.listId, args.card_id)
        print("Archived.", file=sys.stderr)
