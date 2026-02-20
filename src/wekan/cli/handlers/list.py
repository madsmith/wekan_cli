"""
Handlers for the 'list' action.
"""

from ._helpers import not_found, output, resolve_card


def handle_list_labels(client, args):
    board = client.get_board(args.board_id)
    if board is None:
        not_found(f"Board {args.board_id}")
    output(board.labels or [], args.format)


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
    card = resolve_card(client, args.card_id)
    comments = client.get_comments(card.boardId, args.card_id)
    output(comments, args.format)


def handle_list_checklists(client, args):
    card = resolve_card(client, args.card_id)
    checklists = client.get_checklists(card.boardId, args.card_id)
    output(checklists, args.format)
