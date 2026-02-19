"""
Integration tests for board and list lifecycle.
"""

import pytest

from wekan.client import WeKanClient


@pytest.mark.integration
@pytest.mark.dependency()
def test_board_lifecycle(client: WeKanClient):
    assert client.user_id is not None, "User ID is not available"

    # Create
    result = client.create_board("Test Board - Integration", client.user_id)
    assert result.boardId
    board_id = result.boardId

    # List
    boards = client.get_boards_for_user(client.user_id)
    assert any(b.boardId == board_id for b in boards)

    # Get
    board = client.get_board(board_id)
    assert board.boardId == board_id
    assert board.title == "Test Board - Integration"

    # Delete
    client.delete_board(board_id)
    boards = client.get_boards()
    assert not any(b.boardId == board_id for b in boards)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_board_lifecycle"])
def test_list_lifecycle(client: WeKanClient):
    assert client.user_id is not None, "User ID is not available"

    # Create a board to hold our lists
    board = client.create_board("Test Board - List Lifecycle", client.user_id)
    board_id = board.boardId

    try:
        # Create
        result = client.create_list(board_id, "Test List - Integration")
        assert result.listId
        list_id = result.listId

        # List
        lists = client.get_lists(board_id)
        assert any(list.listId == list_id for list in lists)

        # Get
        lst = client.get_list(board_id, list_id)
        assert lst.listId == list_id
        assert lst.title == "Test List - Integration"

        # Delete
        client.delete_list(board_id, list_id)
        lists = client.get_lists(board_id)
        assert not any(list.listId == list_id for list in lists)
    finally:
        client.delete_board(board_id)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_list_lifecycle"])
def test_card_lifecycle(client: WeKanClient):
    assert client.user_id is not None, "User ID is not available"

    # Set up board and list
    board = client.create_board("Test Board - Card Lifecycle", client.user_id)
    board_id = board.boardId

    try:
        lst = client.create_list(board_id, "Test List - Card Lifecycle")
        list_id = lst.listId

        swimlanes = client.get_swimlanes(board_id)
        assert swimlanes, "Board has no default swimlane"
        swimlane_id = swimlanes[0].swimlaneId

        # Create
        result = client.create_card(
            board_id,
            list_id,
            "Test Card - Integration",
            author_id=client.user_id,
            swimlane_id=swimlane_id,
        )
        assert result.cardId
        card_id = result.cardId

        # List
        cards = client.get_cards(board_id, list_id)
        assert any(c.cardId == card_id for c in cards)

        # Get
        card = client.get_card(board_id, list_id, card_id)
        assert card.cardId == card_id
        assert card.title == "Test Card - Integration"

        # Edit
        client.edit_card(board_id, list_id, card_id, title="Test Card - Edited")
        card = client.get_card(board_id, list_id, card_id)
        assert card.title == "Test Card - Edited"

        # Delete
        client.delete_card(board_id, list_id, card_id)
        cards = client.get_cards(board_id, list_id)
        assert not any(c.cardId == card_id for c in cards)
    finally:
        client.delete_board(board_id)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_card_lifecycle"])
def test_checklist_lifecycle(client: WeKanClient):
    assert client.user_id is not None, "User ID is not available"

    # Set up board, list, card
    board = client.create_board("Test Board - Checklist Lifecycle", client.user_id)
    board_id = board.boardId

    try:
        lst = client.create_list(board_id, "Test List - Checklist Lifecycle")
        list_id = lst.listId

        swimlanes = client.get_swimlanes(board_id)
        assert swimlanes, "Board has no default swimlane"
        swimlane_id = swimlanes[0].swimlaneId

        card = client.create_card(
            board_id,
            list_id,
            "Test Card - Checklist Lifecycle",
            author_id=client.user_id,
            swimlane_id=swimlane_id,
        )
        card_id = card.cardId

        # Create checklist
        result = client.create_checklist(board_id, card_id, "Test Checklist")
        assert result.checklistId
        checklist_id = result.checklistId

        # List checklists
        checklists = client.get_checklists(board_id, card_id)
        assert any(c.checklistId == checklist_id for c in checklists)

        # Get checklist
        checklist = client.get_checklist(board_id, card_id, checklist_id)
        assert checklist.checklistId == checklist_id
        assert checklist.title == "Test Checklist"

        # --- Checklist item lifecycle (nested) ---

        # Create item
        item_result = client.create_checklist_item(
            board_id,
            card_id,
            checklist_id,
            "Test Item",
        )
        assert item_result.checklistItemId
        item_id = item_result.checklistItemId

        # Get item
        item = client.get_checklist_item(board_id, card_id, checklist_id, item_id)
        assert item.checklistItemId == item_id
        assert item.title == "Test Item"

        # Edit item
        client.edit_checklist_item(
            board_id,
            card_id,
            checklist_id,
            item_id,
            title="Test Item - Edited",
            isFinished=True,
        )
        item = client.get_checklist_item(board_id, card_id, checklist_id, item_id)
        assert item.title == "Test Item - Edited"
        assert item.isFinished is True

        # Delete item
        client.delete_checklist_item(board_id, card_id, checklist_id, item_id)
        checklist = client.get_checklist(board_id, card_id, checklist_id)
        items = getattr(checklist, "items", []) or []
        assert not any(i.checklistItemId == item_id for i in items)

        # --- End checklist item lifecycle ---

        # Delete checklist
        client.delete_checklist(board_id, card_id, checklist_id)
        checklists = client.get_checklists(board_id, card_id)
        assert not any(c.checklistId == checklist_id for c in checklists)
    finally:
        client.delete_board(board_id)


CLEANUP_BOARDS = []


@pytest.mark.manual
@pytest.mark.parametrize("board_id", CLEANUP_BOARDS)
def test_delete_board_oneoff(client, board_id):
    client.delete_board(board_id)
    boards = client.get_boards()
    assert not any(b.boardId == board_id for b in boards)
