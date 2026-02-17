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


class CardSummary(CardId):
    title: str
    description: str | None = None


class CardDetails(CardId):
    title: str
    description: str | None = None


class Comment(WeKanModel):
    commentId: str = Field(validation_alias="_id")
    comment: str
    authorId: str


class Checklist(WeKanModel):
    checklistId: str = Field(validation_alias="_id")
    title: str


class ChecklistItem(WeKanModel):
    checklistItemId: str = Field(validation_alias="_id")
    title: str
    isFinished: bool


class ChecklistDetails(WeKanModel):
    checklistId: str = Field(validation_alias="_id")
    cardId: str | None = None
    title: str
    finishedAt: str | None = None
    createdAt: str | None = None
    sort: int | None = None
    items: list[ChecklistItem] | None = None
