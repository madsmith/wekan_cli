"""
Pydantic models for WeKan API responses.
"""

from pydantic import BaseModel, ConfigDict, Field


class WeKanModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class APIError(WeKanModel):
    error: str
    reason: str
    message: str
    statusCode: int


class LoginResponse(WeKanModel):
    user_id: str = Field(validation_alias="id")
    token: str
    tokenExpires: str


class Board(WeKanModel):
    board_id: str = Field(validation_alias="_id")
    title: str


class List(WeKanModel):
    list_id: str = Field(validation_alias="_id")
    title: str


class Card(WeKanModel):
    card_id: str = Field(validation_alias="_id")
    title: str
    description: str | None = None
