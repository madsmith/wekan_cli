"""
WeKan REST API client module
"""

from typing import Any, Dict

import requests


class WeKanClient:
    """Client for interacting with WeKan REST API"""

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

    def login(self) -> Dict[str, Any]:
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
        response.raise_for_status()

        data = response.json()
        if "token" in data:
            self.token = data["token"]
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

        return data

    def get_boards(self) -> list:
        """
        Get all boards accessible to the user

        Returns:
            List of boards
        """
        url = f"{self.base_url}/api/boards"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        Get details of a specific board

        Args:
            board_id: ID of the board

        Returns:
            Board details
        """
        url = f"{self.base_url}/api/boards/{board_id}"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_lists(self, board_id: str) -> list:
        """
        Get all lists in a board

        Args:
            board_id: ID of the board

        Returns:
            List of lists in the board
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_cards(self, board_id: str, list_id: str) -> list:
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
        response.raise_for_status()
        return response.json()

    def create_board(self, title: str, **kwargs) -> Dict[str, Any]:
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
        response.raise_for_status()
        return response.json()

    def create_list(self, board_id: str, title: str) -> Dict[str, Any]:
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
        response.raise_for_status()
        return response.json()

    def create_card(
        self,
        board_id: str,
        list_id: str,
        title: str,
        description: str | None = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new card in a list

        Args:
            board_id: ID of the board
            list_id: ID of the list
            title: Title of the card
            description: Description of the card
            **kwargs: Additional card properties

        Returns:
            Created card details
        """
        url = f"{self.base_url}/api/boards/{board_id}/lists/{list_id}/cards"
        payload = {"title": title, **kwargs}
        if description:
            payload["description"] = description

        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
