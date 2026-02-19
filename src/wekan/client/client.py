"""
WeKan REST API client module
"""

import os

import requests

from .types import (
    APIError,
    BoardDetails,
    BoardId,
    BoardListing,
    CardDetails,
    CardId,
    CardInfo,
    Checklist,
    ChecklistDetails,
    ChecklistId,
    ChecklistItemDetails,
    ChecklistItemId,
    Comment,
    CommentDetails,
    CommentId,
    ListDetails,
    ListId,
    ListInfo,
    LoginResponse,
    SwimlaneDetails,
    SwimlaneId,
    SwimlaneInfo,
    User,
    UserID,
)

DEBUG = os.getenv("WEKAN_DEBUG", False)


class WeKanAPIError(Exception):
    """Raised when the WeKan API returns an error response."""

    def __init__(self, error: APIError):
        self.error = error
        super().__init__(error.message)


class WeKanClient:
    """Client for interacting with WeKan REST API"""

    @staticmethod
    def _check_response(response: requests.Response) -> None:
        """Raise WeKanApiError if the response contains an API error."""
        try:
            if DEBUG:
                print(response.content)
            data = response.json()
            if "error" in data:
                raise WeKanAPIError(APIError.model_validate(data))
        except (ValueError, KeyError):
            pass
        response.raise_for_status()

    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        timeout: int = 30,
    ):
        """
        Initialize WeKan client

        Args:
            base_url: Base URL of the WeKan instance (e.g., https://wekan.example.com)
            username: Username for authentication
            password: Password for authentication
            token: Authentication token (alternative to username/password)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.token = token
        self.user_id: UserID | None = None
        self.timeout = timeout
        self.session = requests.Session()

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def login(self) -> LoginResponse:
        """
        Login to WeKan and get authentication token

        Returns:
            Response containing authentication token
        """
        if not self.username or not self.password:
            raise ValueError("Username and password required for login")

        url = f"{self.base_url}/users/login"
        payload = {"username": self.username, "password": self.password}

        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)

        result = LoginResponse.model_validate(response.json())
        if result.token:
            self.token = result.token
            self.user_id = result.userId
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

        return result

    def get_users(self) -> list[User]:
        """
        Get all users

        Returns:
            List of users
        """
        url = f"{self.base_url}/api/users"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [User.model_validate(user) for user in response.json()]

    def get_boards(self) -> list[BoardListing]:
        """
        Get all boards accessible to the user

        Returns:
            List of boards
        """
        url = f"{self.base_url}/api/boards"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [BoardListing.model_validate(board) for board in response.json()]

    def get_boards_for_user(self, user_id: UserID) -> list[BoardListing]:
        """
        Get all boards accessible to a specific user

        Args:
            user_id: ID of the user

        Returns:
            List of boards accessible to the user
        """
        url = f"{self.base_url}/api/users/{user_id}/boards"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [BoardListing.model_validate(board) for board in response.json()]

    def get_board(self, board_id: str) -> BoardDetails | None:
        """
        Get details of a specific board

        Args:
            board_id: ID of the board

        Returns:
            Board details, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return BoardDetails.model_validate(response.json())

    def get_lists(self, board_id: str) -> list[ListInfo]:
        """
        Get all lists in a board

        Args:
            board_id: ID of the board

        Returns:
            List of lists in the board
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [ListInfo.model_validate(lst) for lst in response.json()]

    def get_swimlanes(self, board_id: str) -> list[SwimlaneInfo]:
        """
        Get all swimlanes in a board

        Args:
            board_id: ID of the board

        Returns:
            List of swimlanes in the board
        """
        url = f"{self.base_url}/api/boards/{board_id}/swimlanes"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [SwimlaneInfo.model_validate(s) for s in response.json()]

    def get_swimlane(self, board_id: str, swimlane_id: str) -> SwimlaneDetails | None:
        """
        Get details of a specific swimlane

        Args:
            board_id: ID of the board
            swimlane_id: ID of the swimlane

        Returns:
            Swimlane details, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}/swimlanes/{swimlane_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return SwimlaneDetails.model_validate(response.json())

    def create_swimlane(self, board_id: str, title: str) -> SwimlaneId:
        """
        Create a new swimlane in a board

        Args:
            board_id: ID of the board
            title: Title of the swimlane

        Returns:
            Created swimlane ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/swimlanes"
        payload = {"title": title}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return SwimlaneId.model_validate(response.json())

    def delete_swimlane(self, board_id: str, swimlane_id: str) -> SwimlaneId:
        """
        Delete a swimlane

        Args:
            board_id: ID of the board
            swimlane_id: ID of the swimlane

        Returns:
            Deleted swimlane ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/swimlanes/{swimlane_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return SwimlaneId.model_validate(response.json())

    def get_cards(self, board_id: str, list_id: str) -> list[CardInfo]:
        """
        Get all cards in a list

        Args:
            board_id: ID of the board
            list_id: ID of the list

        Returns:
            List of cards
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [CardInfo.model_validate(card) for card in response.json()]

    def get_card(self, board_id: str, list_id: str, card_id: str) -> CardDetails | None:
        """
        Get details of a specific card

        Args:
            board_id: ID of the board
            list_id: ID of the list
            card_id: ID of the card

        Returns:
            Card details, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards/{card_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return CardDetails.model_validate(response.json())

    def create_board(self, title: str, owner_id: UserID, **kwargs) -> BoardId:
        """
        Create a new board

        Args:
            title: Title of the board
            owner_id: ID of the owner
            **kwargs: Additional board properties

        Returns:
            Created board ID
        """
        url = f"{self.base_url}/api/boards"
        payload = {"title": title, "owner": owner_id, **kwargs}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return BoardId.model_validate(response.json())

    def delete_board(self, board_id: str) -> BoardId:
        """
        Delete a board

        Args:
            board_id: ID of the board

        Returns:
            Deleted board ID
        """
        url = f"{self.base_url}/api/boards/{board_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return BoardId.model_validate(response.json())

    def create_list(self, board_id: str, title: str) -> ListId:
        """
        Create a new list in a board

        Args:
            board_id: ID of the board
            title: Title of the list

        Returns:
            Created list ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists"
        payload = {"title": title}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return ListId.model_validate(response.json())

    def get_list(self, board_id: str, list_id: str) -> ListDetails | None:
        """
        Get a specific list

        Args:
            board_id: ID of the board
            list_id: ID of the list

        Returns:
            List details, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return ListDetails.model_validate(response.json())

    def delete_list(self, board_id: str, list_id: str) -> ListId:
        """
        Delete a list

        Args:
            board_id: ID of the board
            list_id: ID of the list

        Returns:
            Deleted list ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return ListId.model_validate(response.json())

    def create_card(
        self,
        board_id: str,
        list_id: str,
        title: str,
        author_id: UserID,
        swimlane_id: str,
        description: str | None = None,
        **kwargs,
    ) -> CardId:
        """
        Create a new card in a list

        Args:
            board_id: ID of the board
            list_id: ID of the list
            title: Title of the card
            author_id: ID of the card author
            swimlane_id: ID of the swimlane
            description: Description of the card
            **kwargs: Additional card properties

        Returns:
            Created card details
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards"
        payload = {
            "title": title,
            "authorId": author_id,
            "swimlaneId": swimlane_id,
            **kwargs,
        }
        if description:
            payload["description"] = description

        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return CardId.model_validate(response.json())

    def edit_card(self, board_id: str, list_id: str, card_id: str, **kwargs) -> CardId:
        """
        Edit a card

        Args:
            board_id: ID of the board
            list_id: ID of the list
            card_id: ID of the card
            **kwargs: Fields to update (title, description, color, etc.)

        Returns:
            Updated card details
        """

        previous_card = self.get_card(board_id, list_id, card_id)
        if previous_card is None:
            raise ValueError(f"Card {card_id} not found")

        if "newBoardId" not in kwargs:
            kwargs["newBoardId"] = board_id
        if "newListId" not in kwargs:
            kwargs["newListId"] = list_id
        if "newSwimlaneId" not in kwargs:
            kwargs["newSwimlaneId"] = previous_card.swimlaneId
        # Archive is listed as a required arg but the code does not require it
        # Leaving this commented out for now
        # if "archive" not in kwargs:
        #    kwargs["archive"] = False

        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards/{card_id}"
        response = self.session.put(url, json=kwargs, timeout=self.timeout)
        self._check_response(response)
        return CardId.model_validate(response.json())

    def delete_card(self, board_id: str, list_id: str, card_id: str) -> CardId:
        """
        Delete a card

        Args:
            board_id: ID of the board
            list_id: ID of the list
            card_id: ID of the card

        Returns:
            Deleted card ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards/{card_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return CardId.model_validate(response.json())

    def get_swimlane_cards(self, board_id: str, swimlane_id: str) -> list[CardInfo]:
        """
        Get all cards in a swimlane

        Args:
            board_id: ID of the board
            swimlane_id: ID of the swimlane

        Returns:
            List of cards
        """
        url = f"{self.base_url}/api/boards/{board_id}/swimlanes/{swimlane_id}/cards"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [CardInfo.model_validate(card) for card in response.json()]

    def get_card_by_id(self, card_id: str) -> CardDetails | None:
        """
        Get card details by card ID only

        Args:
            card_id: ID of the card

        Returns:
            Card details, or None if not found
        """
        url = f"{self.base_url}/api/cards/{card_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return CardDetails.model_validate(response.json())

    def get_comments(self, board_id: str, card_id: str) -> list[Comment]:
        """
        Get all comments on a card

        Args:
            board_id: ID of the board
            card_id: ID of the card

        Returns:
            List of comments
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/comments"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [Comment.model_validate(c) for c in response.json()]

    def create_comment(
        self, board_id: str, card_id: str, author_id: UserID, comment: str
    ) -> CommentId:
        """
        Add a comment to a card

        Args:
            board_id: ID of the board
            card_id: ID of the card
            author_id: ID of the comment author
            comment: The comment text

        Returns:
            Created comment
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/comments"
        payload = {"authorId": author_id, "comment": comment}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return CommentId.model_validate(response.json())

    def get_comment(
        self, board_id: str, card_id: str, comment_id: str
    ) -> CommentDetails | None:
        """
        Get a specific comment

        Args:
            board_id: ID of the board
            card_id: ID of the card
            comment_id: ID of the comment

        Returns:
            Comment details, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/comments/{comment_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return CommentDetails.model_validate(response.json())

    def delete_comment(self, board_id: str, card_id: str, comment_id: str) -> CommentId:
        """
        Delete a comment

        Args:
            board_id: ID of the board
            card_id: ID of the card
            comment_id: ID of the comment

        Returns:
            Deleted comment ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/comments/{comment_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return CommentId.model_validate(response.json())

    def get_checklists(self, board_id: str, card_id: str) -> list[Checklist]:
        """
        Get all checklists on a card

        Args:
            board_id: ID of the board
            card_id: ID of the card

        Returns:
            List of checklists
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return [Checklist.model_validate(c) for c in response.json()]

    def create_checklist(
        self, board_id: str, card_id: str, title: str, items: str | None = None
    ) -> ChecklistId:
        """
        Create a checklist on a card

        Args:
            board_id: ID of the board
            card_id: ID of the card
            title: Title of the checklist
            items: Comma-separated list of checklist items

        Returns:
            Created checklist ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists"
        payload = {"title": title}
        if items:
            payload["items"] = items
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return ChecklistId.model_validate(response.json())

    def get_checklist(
        self, board_id: str, card_id: str, checklist_id: str
    ) -> ChecklistDetails | None:
        """
        Get details of a specific checklist

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist

        Returns:
            Checklist details with items, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return ChecklistDetails.model_validate(response.json())

    def create_checklist_item(
        self, board_id: str, card_id: str, checklist_id: str, title: str
    ) -> ChecklistItemId:
        """
        Add a new item to a checklist

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist
            title: Title of the new item

        Returns:
            Created checklist item ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}/items"
        payload = {"title": title}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return ChecklistItemId.model_validate(response.json())

    def delete_checklist(
        self, board_id: str, card_id: str, checklist_id: str
    ) -> ChecklistId:
        """
        Delete a checklist

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist

        Returns:
            Deleted checklist ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return ChecklistId.model_validate(response.json())

    def delete_checklist_item(
        self, board_id: str, card_id: str, checklist_id: str, item_id: str
    ) -> ChecklistItemId:
        """
        Delete a checklist item

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist
            item_id: ID of the item

        Returns:
            Deleted checklist item ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}/items/{item_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)
        return ChecklistItemId.model_validate(response.json())

    def get_checklist_item(
        self, board_id: str, card_id: str, checklist_id: str, item_id: str
    ) -> ChecklistItemDetails | None:
        """
        Get a checklist item

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist
            item_id: ID of the item

        Returns:
            Checklist item details, or None if not found
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}/items/{item_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        if not response.text:
            return None
        return ChecklistItemDetails.model_validate(response.json())

    def edit_checklist_item(
        self, board_id: str, card_id: str, checklist_id: str, item_id: str, **kwargs
    ) -> ChecklistItemId:
        """
        Edit a checklist item

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist
            item_id: ID of the item
            **kwargs: Fields to update (title, isFinished)

        Returns:
            Updated checklist item ID
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}/items/{item_id}"
        response = self.session.put(url, json=kwargs, timeout=self.timeout)
        self._check_response(response)
        return ChecklistItemId.model_validate(response.json())
