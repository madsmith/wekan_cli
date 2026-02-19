"""
Handlers for the 'get' action.
"""

from ._helpers import not_found, output


def handle_get_board(client, args):
    result = client.get_board(args.board_id)
    if result is None:
        not_found("Board")
    output(result, args.format)


def handle_get_list(client, args):
    result = client.get_list(args.board_id, args.list_id)
    if result is None:
        not_found("List")
    output(result, args.format)


def handle_get_swimlane(client, args):
    result = client.get_swimlane(args.board_id, args.swimlane_id)
    if result is None:
        not_found("Swimlane")
    output(result, args.format)


def handle_get_card(client, args):
    result = client.get_card_by_id(args.card_id)
    if result is None:
        not_found("Card")
    output(result, args.format)


def _resolve_card(client, card_id):
    """Fetch card by ID or exit if not found."""
    card = client.get_card_by_id(card_id)
    if card is None:
        not_found(f"Card {card_id}")
    return card


def handle_get_checklist(client, args):
    card = _resolve_card(client, args.card_id)
    result = client.get_checklist(card.boardId, args.card_id, args.checklist_id)
    if result is None:
        not_found("Checklist")
    output(result, args.format)


def handle_get_checklist_item(client, args):
    card = _resolve_card(client, args.card_id)
    result = client.get_checklist_item(
        card.boardId, args.card_id, args.checklist_id, args.item_id
    )
    if result is None:
        not_found("Checklist item")
    output(result, args.format)


def handle_get_comment(client, args):
    card = _resolve_card(client, args.card_id)
    result = client.get_comment(card.boardId, args.card_id, args.comment_id)
    if result is None:
        not_found("Comment")
    output(result, args.format)
