"""
Pydantic models for WeKan API responses.
"""

from enum import Enum
from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field

UserID: TypeAlias = str


class Color(str, Enum):
    WHITE = "white"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    PURPLE = "purple"
    BLUE = "blue"
    SKY = "sky"
    LIME = "lime"
    PINK = "pink"
    BLACK = "black"
    SILVER = "silver"
    PEACHPUFF = "peachpuff"
    CRIMSON = "crimson"
    PLUM = "plum"
    DARKGREEN = "darkgreen"
    SLATEBLUE = "slateblue"
    MAGENTA = "magenta"
    GOLD = "gold"
    NAVY = "navy"
    GRAY = "gray"
    SADDLEBROWN = "saddlebrown"
    PALETURQUOISE = "paleturquoise"
    MISTYROSE = "mistyrose"
    INDIGO = "indigo"


class BoardColor(str, Enum):
    BELIZE = "belize"
    NEPHRITIS = "nephritis"
    POMEGRANATE = "pomegranate"
    PUMPKIN = "pumpkin"
    WISTERIA = "wisteria"
    MODERATEPINK = "moderatepink"
    STRONGCYAN = "strongcyan"
    LIMEGREEN = "limegreen"
    MIDNIGHT = "midnight"
    DARK = "dark"
    RELAX = "relax"
    CORTEZA = "corteza"
    CLEARBLUE = "clearblue"
    NATURAL = "natural"
    MODERN = "modern"
    MODERNDARK = "moderndark"
    EXODARK = "exodark"
    CLEANDARK = "cleandark"
    CLEANLIGHT = "cleanlight"


class BoardPermission(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class WeKanModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class APIError(WeKanModel):
    error: str
    reason: str
    message: str
    statusCode: int


class User(WeKanModel):
    userId: UserID = Field(validation_alias="_id")
    username: str


class LoginResponse(WeKanModel):
    userId: UserID = Field(validation_alias="id")
    token: str
    tokenExpires: str


class BoardLabel(WeKanModel):
    labelId: str = Field(validation_alias="_id")
    name: str
    color: str


class BoardTeam(WeKanModel):
    teamId: str
    teamDisplayName: str
    isActive: bool | None = None


class BoardOrg(WeKanModel):
    orgId: str
    orgDisplayName: str
    isActive: bool | None = None


class BoardId(WeKanModel):
    boardId: str = Field(validation_alias="_id")


class BoardInfo(BoardId):
    title: str


class BoardMember(WeKanModel):
    userId: UserID
    isAdmin: bool | None = None
    isActive: bool | None = None
    isNoComments: bool | None = None
    isCommentOnly: bool | None = None
    isWorker: bool | None = None


class BoardDetails(BoardId):
    title: str
    description: str | None = None
    color: BoardColor | None = None
    permission: BoardPermission | None = None
    archived: bool | None = None
    archivedAt: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
    sort: int | None = None
    subtasksDefaultBoardId: str | None = None
    subtasksDefaultListId: str | None = None
    presentParentTask: str | None = None
    receivedAt: str | None = None
    startAt: str | None = None
    dueAt: str | None = None
    labels: list[BoardLabel] | None = None
    members: list[BoardMember] | None = None
    teams: list[BoardTeam] | None = None
    orgs: list[BoardOrg] | None = None


class SwimlaneId(WeKanModel):
    swimlaneId: str = Field(validation_alias="_id")


class SwimlaneInfo(SwimlaneId):
    title: str


class SwimlaneDetails(SwimlaneId):
    title: str
    archived: bool | None = None
    archivedAt: str | None = None
    boardId: str | None = None
    createdAt: str | None = None
    sort: int | None = None
    color: Color | None = None
    updatedAt: str | None = None
    modifiedAt: str | None = None
    collapsed: bool | None = None


class ListId(WeKanModel):
    listId: str = Field(validation_alias="_id")


class ListInfo(ListId):
    title: str


class WIPLimit(WeKanModel):
    value: int | None = None
    enabled: bool | None = None
    soft: bool | None = None


class ListDetails(ListId):
    title: str
    starred: bool | None = None
    archived: bool | None = None
    archivedAt: str | None = None
    boardId: str | None = None
    swimlaneId: str | None = None
    sort: int | None = None
    color: Color | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    modifiedAt: str | None = None
    wipLimit: WIPLimit | None = None
    collapsed: bool | None = None


class CardId(WeKanModel):
    cardId: str = Field(validation_alias="_id")


class CardInfo(CardId):
    title: str
    description: str | None = None


class Vote(WeKanModel):
    question: str | None = None
    positive: list[UserID] | None = None
    negative: list[UserID] | None = None
    end: str | None = None
    public: bool | None = None
    allowNonBoardMembers: bool | None = None


class CardDetails(CardId):
    title: str
    description: str | None = None
    color: Color | None = None
    archived: bool | None = None
    archivedAt: str | None = None
    listId: str | None = None
    swimlaneId: str | None = None
    boardId: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
    assignedBy: UserID | None = None
    requestedBy: UserID | None = None
    labelIds: list[str] | None = None
    members: list[UserID] | None = None
    assignees: list[UserID] | None = None
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
    authorId: UserID


class CommentDetails(CommentId):
    boardId: str | None = None
    cardId: str | None = None
    text: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
    userId: UserID | None = None


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
