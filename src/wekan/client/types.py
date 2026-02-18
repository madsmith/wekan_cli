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


class BoardId(WeKanModel):
    boardId: str = Field(validation_alias="_id")


class BoardListing(BoardId):
    title: str


class BoardDetails(BoardId):
    title: str
    labels: list[Label] | None = None


class Swimlane(WeKanModel):
    swimlaneId: str = Field(validation_alias="_id")
    title: str


class ListId(WeKanModel):
    listId: str = Field(validation_alias="_id")


class List(ListId):
    title: str


class CardId(WeKanModel):
    cardId: str = Field(validation_alias="_id")


class CardSummary(CardId):
    title: str
    description: str | None = None


class CardDetails(CardId):
    title: str
    description: str | None = None
    boardId: str
    listId: str
    userId: str
    swimlaneId: str
    archived: bool
    sort: int
    cardNumber: int


class CommentId(WeKanModel):
    commentId: str = Field(validation_alias="_id")


class Comment(CommentId):
    comment: str
    authorId: str


class ChecklistId(WeKanModel):
    checklistId: str = Field(validation_alias="_id")


class Checklist(ChecklistId):
    title: str


class ChecklistItemId(WeKanModel):
    checklistItemId: str = Field(validation_alias="_id")


class ChecklistItem(ChecklistItemId):
    title: str
    isFinished: bool


class ChecklistItemDetails(ChecklistItemId):
    title: str
    sort: int | None = None
    isFinished: bool | None = None
    checklistId: str | None = None
    cardId: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None


class ChecklistDetails(ChecklistId):
    cardId: str | None = None
    title: str
    finishedAt: str | None = None
    createdAt: str | None = None
    sort: int | None = None
    items: list[ChecklistItem] | None = None
