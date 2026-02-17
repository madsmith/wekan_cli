"""
WeKan REST API client module
"""

import requests

from .types import (
    APIError,
    BoardDetails,
    BoardListing,
    CardDetails,
    CardId,
    CardSummary,
    Checklist,
    ChecklistDetails,
    Comment,
    List,
    LoginResponse,
    Swimlane,
    User,
)


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

    def get_boards_for_user(self, user_id: str) -> list[BoardListing]:
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

    def get_board(self, board_id: str) -> BoardDetails:
        """
        Get details of a specific board

        Args:
            board_id: ID of the board

        Returns:
            Board details
        """
        url = f"{self.base_url}/api/boards/{board_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return BoardDetails.model_validate(response.json())

    def get_lists(self, board_id: str) -> list[List]:
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
        return [List.model_validate(list) for list in response.json()]

    def get_swimlanes(self, board_id: str) -> list[Swimlane]:
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
        return [Swimlane.model_validate(s) for s in response.json()]

    def get_cards(self, board_id: str, list_id: str) -> list[CardSummary]:
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
        return [CardSummary.model_validate(card) for card in response.json()]

    def get_card(self, board_id: str, list_id: str, card_id: str) -> CardDetails:
        """
        Get details of a specific card

        Args:
            board_id: ID of the board
            list_id: ID of the list
            card_id: ID of the card

        Returns:
            Card details
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards/{card_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return CardDetails.model_validate(response.json())

    def create_board(self, title: str, **kwargs) -> BoardListing:
        """
        Create a new board

        Args:
            title: Title of the board
            **kwargs: Additional board properties

        Returns:
            Created board details
        """
        url = f"{self.base_url}/api/boards"
        payload = {"title": title, **kwargs}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return BoardListing.model_validate(response.json())

    def create_list(self, board_id: str, title: str) -> List:
        """
        Create a new list in a board

        Args:
            board_id: ID of the board
            title: Title of the list

        Returns:
            Created list details
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists"
        payload = {"title": title}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return List.model_validate(response.json())

    def create_card(
        self,
        board_id: str,
        list_id: str,
        title: str,
        author_id: str,
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

    def edit_card(
        self, board_id: str, list_id: str, card_id: str, **kwargs
    ) -> CardDetails:
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
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards/{card_id}"
        response = self.session.put(url, json=kwargs, timeout=self.timeout)
        self._check_response(response)
        return CardDetails.model_validate(response.json())

    def delete_card(self, board_id: str, list_id: str, card_id: str) -> None:
        """
        Delete a card

        Args:
            board_id: ID of the board
            list_id: ID of the list
            card_id: ID of the card
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards/{card_id}"
        response = self.session.delete(url, timeout=self.timeout)
        self._check_response(response)

    def get_swimlane_cards(self, board_id: str, swimlane_id: str) -> list[CardSummary]:
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
        return [CardSummary.model_validate(card) for card in response.json()]

    def get_card_by_id(self, card_id: str) -> CardDetails:
        """
        Get card details by card ID only

        Args:
            card_id: ID of the card

        Returns:
            Card details
        """
        url = f"{self.base_url}/api/cards/{card_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
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
        self, board_id: str, card_id: str, author_id: str, comment: str
    ) -> Comment:
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
        return Comment.model_validate(response.json())

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
    ) -> Checklist:
        """
        Create a checklist on a card

        Args:
            board_id: ID of the board
            card_id: ID of the card
            title: Title of the checklist
            items: Comma-separated list of checklist items

        Returns:
            Created checklist
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists"
        payload = {"title": title}
        if items:
            payload["items"] = items
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._check_response(response)
        return Checklist.model_validate(response.json())

    def get_checklist(
        self, board_id: str, card_id: str, checklist_id: str
    ) -> ChecklistDetails:
        """
        Get details of a specific checklist

        Args:
            board_id: ID of the board
            card_id: ID of the card
            checklist_id: ID of the checklist

        Returns:
            Checklist details with items
        """
        url = f"{self.base_url}/api/boards/{board_id}/cards/{card_id}/checklists/{checklist_id}"
        response = self.session.get(url, timeout=self.timeout)
        self._check_response(response)
        return ChecklistDetails.model_validate(response.json())
