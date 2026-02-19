"""
Handlers for the 'delete' action.
"""

import sys

from ._helpers import not_implemented


def handle_delete_card(client, args):
    client.delete_card(args.board_id, args.list_id, args.card_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_board(client, args):
    client.delete_board(args.board_id)
    print("Deleted.", file=sys.stderr)


def handle_delete_list(client, args):
    not_implemented("delete list")


def handle_delete_swimlane(client, args):
    not_implemented("delete swimlane")


def handle_delete_comment(client, args):
    not_implemented("delete comment")


def handle_delete_checklist(client, args):
    not_implemented("delete checklist")


def handle_delete_checklist_item(client, args):
    not_implemented("delete checklist-item")
