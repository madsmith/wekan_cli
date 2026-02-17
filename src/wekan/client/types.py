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


class User(WeKanModel):
    userId: str = Field(validation_alias="_id")
    username: str


class LoginResponse(WeKanModel):
    userId: str = Field(validation_alias="id")
    token: str
    tokenExpires: str


class Label(WeKanModel):
    labelId: str = Field(validation_alias="_id")
    name: str
    color: str


class BoardListing(WeKanModel):
    boardId: str = Field(validation_alias="_id")
    title: str


class BoardDetails(WeKanModel):
    boardId: str = Field(validation_alias="_id")
    title: str
    labels: list[Label] | None = None


class Swimlane(WeKanModel):
    swimlaneId: str = Field(validation_alias="_id")
    title: str


class List(WeKanModel):
    listId: str = Field(validation_alias="_id")
    title: str


class CardId(WeKanModel):
    cardId: str = Field(validation_alias="_id")


class Card(CardId):
    title: str
    description: str | None = None
