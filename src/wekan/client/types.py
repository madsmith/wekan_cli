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


class SwimlaneId(WeKanModel):
    swimlaneId: str = Field(validation_alias="_id")


class Swimlane(SwimlaneId):
    title: str


class SwimlaneDetails(SwimlaneId):
    title: str
    archived: bool | None = None
    archivedAt: str | None = None
    boardId: str | None = None
    createdAt: str | None = None
    sort: int | None = None
    color: str | None = None
    updatedAt: str | None = None
    modifiedAt: str | None = None
    type: str | None = None
    collapsed: bool | None = None


class ListId(WeKanModel):
    listId: str = Field(validation_alias="_id")


class ListInfo(ListId):
    title: str


class ListDetails(ListId):
    title: str
    archived: bool | None = None
    boardId: str | None = None
    swimlaneId: str | None = None
    sort: int | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    modifiedAt: str | None = None


class CardId(WeKanModel):
    cardId: str = Field(validation_alias="_id")


class CardInfo(CardId):
    title: str
    description: str | None = None


class Vote(WeKanModel):
    question: str | None = None
    positive: list[str] | None = None
    negative: list[str] | None = None
    end: str | None = None
    public: bool | None = None
    allowNonBoardMembers: bool | None = None


class CardDetails(CardId):
    title: str
    description: str | None = None
    archived: bool | None = None
    archivedAt: str | None = None
    listId: str | None = None
    swimlaneId: str | None = None
    boardId: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
    assignedBy: str | None = None
    requestedBy: str | None = None
    labelIds: list[str] | None = None
    members: list[str] | None = None
    assignees: list[str] | None = None
    receivedAt: str | None = None
    dueAt: str | None = None
    endsAt: str | None = None
    cardNumber: int | None = None
    sort: int | None = None
    customFields: list[dict] | None = None
    dateLastActivity: str | None = None
    startAt: str | None = None
    vote: Vote | None = None


class CommentId(WeKanModel):
    commentId: str = Field(validation_alias="_id")


class Comment(CommentId):
    comment: str
    authorId: str


class CommentDetails(CommentId):
    boardId: str | None = None
    cardId: str | None = None
    text: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
    userId: str | None = None


class ChecklistId(WeKanModel):
    checklistId: str = Field(validation_alias="_id")


class Checklist(ChecklistId):
    title: str


class ChecklistItemId(WeKanModel):
    checklistItemId: str = Field(validation_alias="_id")


class ChecklistItem(ChecklistItemId):
    title: str
    isFinished: bool


class ChecklistDetails(ChecklistId):
    cardId: str | None = None
    title: str
    finishedAt: str | None = None
    createdAt: str | None = None
    sort: int | None = None
    items: list[ChecklistItem] | None = None


class ChecklistItemDetails(ChecklistItemId):
    title: str
    sort: int | None = None
    isFinished: bool | None = None
    checklistId: str | None = None
    cardId: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
