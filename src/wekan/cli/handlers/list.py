"""
Handlers for the 'list' action.
"""

from ._helpers import output


def handle_list_boards(client, args):
    if args.user_id:
        boards = client.get_boards_for_user(args.user_id)
    else:
        boards = client.get_boards()
    output(boards, args.format)


def handle_list_lists(client, args):
    lists = client.get_lists(args.board_id)
    output(lists, args.format)


def handle_list_swimlanes(client, args):
    swimlanes = client.get_swimlanes(args.board_id)
    output(swimlanes, args.format)


def handle_list_cards(client, args):
    swimlane_id = getattr(args, "swimlane_id", None)
    if swimlane_id:
        cards = client.get_swimlane_cards(args.board_id, swimlane_id)
    else:
        cards = client.get_cards(args.board_id, args.list_id)
    output(cards, args.format)


def handle_list_users(client, args):
    users = client.get_users()
    output(users, args.format)


def handle_list_comments(client, args):
    comments = client.get_comments(args.board_id, args.card_id)
    output(comments, args.format)


def handle_list_checklists(client, args):
    checklists = client.get_checklists(args.board_id, args.card_id)
    output(checklists, args.format)
