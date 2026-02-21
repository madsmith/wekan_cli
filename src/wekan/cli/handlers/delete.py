"""
Handlers for the 'delete' action.
"""

import argparse
import sys

from wekan.client import WeKanClient

from ._helpers import resolve_card


def handle_delete_board(client: WeKanClient, args: argparse.Namespace) -> None:
    client.delete_board(args.board_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_list(client: WeKanClient, args: argparse.Namespace) -> None:
    client.delete_list(args.board_id, args.list_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_swimlane(client: WeKanClient, args: argparse.Namespace) -> None:
    client.delete_swimlane(args.board_id, args.swimlane_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_card(client: WeKanClient, args: argparse.Namespace) -> None:
    card = resolve_card(client, args.card_id)
    client.delete_card(card.boardId, card.listId, args.card_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_comment(client: WeKanClient, args: argparse.Namespace) -> None:
    card = resolve_card(client, args.card_id)
    client.delete_comment(card.boardId, args.card_id, args.comment_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_checklist(client: WeKanClient, args: argparse.Namespace) -> None:
    card = resolve_card(client, args.card_id)
    client.delete_checklist(card.boardId, args.card_id, args.checklist_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_checklist_item(client: WeKanClient, args: argparse.Namespace) -> None:
    card = resolve_card(client, args.card_id)
    client.delete_checklist_item(
        card.boardId, args.card_id, args.checklist_id, args.item_id
    )
    print("Deleted.", file=sys.stderr)
