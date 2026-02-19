"""
Handlers for the 'list' action.
"""

from ._helpers import output


def handle_list_boards(client, args):
    if args.user_id:
        output(client.get_boards_for_user(args.user_id), args.format)
    else:
        output(client.get_boards(), args.format)


def handle_list_lists(client, args):
    output(client.get_lists(args.board_id), args.format)


def handle_list_swimlanes(client, args):
    output(client.get_swimlanes(args.board_id), args.format)


def handle_list_cards(client, args):
    swimlane_id = getattr(args, "swimlane_id", None)
    if swimlane_id:
        output(client.get_swimlane_cards(args.board_id, swimlane_id), args.format)
    else:
        output(client.get_cards(args.board_id, args.list_id), args.format)


def handle_list_users(client, args):
    output(client.get_users(), args.format)


def handle_list_comments(client, args):
    output(client.get_comments(args.board_id, args.card_id), args.format)


def handle_list_checklists(client, args):
    output(client.get_checklists(args.board_id, args.card_id), args.format)
