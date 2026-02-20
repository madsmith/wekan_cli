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
    userId: UserID = Field(validation_alias="_id", description="User ID")
    username: str = Field(description="Username")


class LoginResponse(WeKanModel):
    userId: UserID = Field(validation_alias="id", description="User ID")
    token: str = Field(description="Authentication token")
    tokenExpires: str = Field(description="Token expiration date")


# ---------------------------------------------------------------------------
# Board types
# ---------------------------------------------------------------------------


class BoardLabel(WeKanModel):
    labelId: str = Field(validation_alias="_id", description="Label ID")
    name: str = Field(description="Label name")
    color: str = Field(description="Label color")


class BoardTeam(WeKanModel):
    teamId: str = Field(description="Team ID")
    teamDisplayName: str = Field(description="Team display name")
    isActive: bool | None = Field(
        default=None, description="Whether the team is active"
    )


class BoardOrg(WeKanModel):
    model_config = ConfigDict(title="Board Organization")
    orgId: str = Field(description="Organization ID")
    orgDisplayName: str = Field(description="Organization display name")
    isActive: bool | None = Field(default=None, description="Whether the org is active")


class BoardId(WeKanModel):
    boardId: str = Field(validation_alias="_id", description="Board ID")


class BoardInfo(BoardId):
    title: str = Field(description="Board title")


class BoardMember(WeKanModel):
    userId: UserID = Field(description="User ID")
    isAdmin: bool | None = Field(
        default=None, description="Whether the user is an admin"
    )
    isActive: bool | None = Field(
        default=None, description="Whether the user is active"
    )
    isNoComments: bool | None = Field(
        default=None, description="Whether comments are disabled"
    )
    isCommentOnly: bool | None = Field(
        default=None, description="Whether user can only comment"
    )
    isWorker: bool | None = Field(default=None, description="Whether user is a worker")


class Email(WeKanModel):
    address: str = Field(description="Email address")
    verified: bool = Field(description="Whether the email is verified")


class BoardMembership(BoardId):
    isAdmin: bool | None = Field(
        default=None, description="Whether the user is an admin"
    )
    isActive: bool | None = Field(
        default=None, description="Whether the membership is active"
    )
    isWorker: bool | None = Field(
        default=None, description="Whether the user is a worker"
    )


class UserDetails(User):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})
    createdAt: str | None = Field(default=None, description="Date user was created")
    emails: list[Email] | None = Field(
        default=None, description="List of email addresses"
    )
    isAdmin: bool | None = Field(
        default=None, description="Whether the user is an Admin"
    )
    modifiedAt: str | None = Field(
        default=None, description="Date user was last modified"
    )
    authenticationMethod: str | None = Field(
        default=None, description="Authentication method"
    )
    boards: list[BoardMembership] | None = Field(
        default=None, description="List of board memberships"
    )


class BoardDetails(BoardId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})
    title: str = Field(description="Board title")
    description: str | None = Field(default=None, description="Board description")
    color: BoardColor | None = Field(default=None, description="Board theme color")
    permission: BoardPermission | None = Field(
        default=None, description="Board permission (public/private)"
    )
    archived: bool | None = Field(
        default=None, description="Whether the board is archived"
    )
    archivedAt: str | None = Field(default=None, description="Date board was archived")
    createdAt: str | None = Field(default=None, description="Date board was created")
    modifiedAt: str | None = Field(
        default=None, description="Date board was last modified"
    )
    sort: int | None = Field(default=None, description="Sort order")
    subtasksDefaultBoardId: str | None = Field(
        default=None, description="Default board ID for subtasks"
    )
    subtasksDefaultListId: str | None = Field(
        default=None, description="Default list ID for subtasks"
    )
    presentParentTask: str | None = Field(
        default=None, description="Parent task display mode"
    )
    receivedAt: str | None = Field(default=None, description="Date board was received")
    startAt: str | None = Field(default=None, description="Start date")
    dueAt: str | None = Field(default=None, description="Due date")
    labels: list[BoardLabel] | None = Field(
        default=None, description="List of board labels"
    )
    members: list[BoardMember] | None = Field(
        default=None, description="List of board members"
    )
    teams: list[BoardTeam] | None = Field(
        default=None, description="List of board teams"
    )
    orgs: list[BoardOrg] | None = Field(
        default=None, description="List of board organizations"
    )


# ---------------------------------------------------------------------------
# Swimlane types
# ---------------------------------------------------------------------------


class SwimlaneId(WeKanModel):
    swimlaneId: str = Field(validation_alias="_id", description="Swimlane ID")


class SwimlaneInfo(SwimlaneId):
    title: str = Field(description="Swimlane title")


class SwimlaneDetails(SwimlaneId):
    title: str = Field(description="Swimlane title")
    archived: bool | None = Field(
        default=None, description="Whether the swimlane is archived"
    )
    archivedAt: str | None = Field(
        default=None, description="Date swimlane was archived"
    )
    boardId: str | None = Field(
        default=None, description="Board ID the swimlane belongs to"
    )
    createdAt: str | None = Field(default=None, description="Date swimlane was created")
    sort: int | None = Field(default=None, description="Sort order")
    color: Color | None = Field(default=None, description="Swimlane color")
    updatedAt: str | None = Field(
        default=None, description="Date swimlane was last updated"
    )
    modifiedAt: str | None = Field(
        default=None, description="Date swimlane was last modified"
    )
    collapsed: bool | None = Field(
        default=None, description="Whether the swimlane is collapsed"
    )


# ---------------------------------------------------------------------------
# List types
# ---------------------------------------------------------------------------


class ListId(WeKanModel):
    listId: str = Field(validation_alias="_id", description="List ID")


class ListInfo(ListId):
    title: str = Field(description="List title")


class WIPLimit(WeKanModel):
    model_config = ConfigDict(title="Work In Progress Limit")
    value: int | None = Field(default=None, description="WIP limit value")
    enabled: bool | None = Field(
        default=None, description="Whether WIP limit is enabled"
    )
    soft: bool | None = Field(
        default=None, description="Whether the limit is a soft limit"
    )


class ListDetails(ListId):
    title: str = Field(description="List title")
    starred: bool | None = Field(
        default=None, description="Whether the list is starred"
    )
    archived: bool | None = Field(
        default=None, description="Whether the list is archived"
    )
    archivedAt: str | None = Field(default=None, description="Date list was archived")
    boardId: str | None = Field(
        default=None, description="Board ID the list belongs to"
    )
    swimlaneId: str | None = Field(
        default=None, description="Swimlane ID the list belongs to"
    )
    sort: int | None = Field(default=None, description="Sort order")
    color: Color | None = Field(default=None, description="List color")
    createdAt: str | None = Field(default=None, description="Date list was created")
    updatedAt: str | None = Field(
        default=None, description="Date list was last updated"
    )
    modifiedAt: str | None = Field(
        default=None, description="Date list was last modified"
    )
    wipLimit: WIPLimit | None = Field(
        default=None, description="Work-in-progress limit"
    )
    collapsed: bool | None = Field(
        default=None, description="Whether the list is collapsed"
    )


# ---------------------------------------------------------------------------
# Card types
# ---------------------------------------------------------------------------


class CardId(WeKanModel):
    cardId: str = Field(validation_alias="_id", description="Card ID")


class CardInfo(CardId):
    title: str = Field(description="Card title")
    description: str | None = Field(default=None, description="Card description")


class Vote(WeKanModel):
    question: str | None = Field(default=None, description="Vote question text")
    positive: list[UserID] | None = Field(
        default=None, description="User IDs who voted in favor"
    )
    negative: list[UserID] | None = Field(
        default=None, description="User IDs who voted against"
    )
    end: str | None = Field(default=None, description="Vote end date")
    public: bool | None = Field(default=None, description="Whether the vote is public")
    allowNonBoardMembers: bool | None = Field(
        default=None, description="Allow non-board members to vote"
    )


class CardDetails(CardId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})
    title: str = Field(description="Card title")
    description: str | None = Field(
        default=None, description="Card description (markdown)"
    )
    color: Color | None = Field(default=None, description="Card color")
    archived: bool | None = Field(
        default=None, description="Whether the card is archived"
    )
    archivedAt: str | None = Field(default=None, description="Date card was archived")
    listId: str | None = Field(default=None, description="List ID the card belongs to")
    swimlaneId: str | None = Field(
        default=None, description="Swimlane ID the card belongs to"
    )
    boardId: str | None = Field(
        default=None, description="Board ID the card belongs to"
    )
    createdAt: str | None = Field(default=None, description="Date card was created")
    modifiedAt: str | None = Field(
        default=None, description="Date card was last modified"
    )
    assignedBy: UserID | None = Field(
        default=None, description="User ID who assigned the card"
    )
    requestedBy: UserID | None = Field(
        default=None, description="User ID who requested the card"
    )
    labelIds: list[str] | None = Field(default=None, description="List of label IDs")
    members: list[UserID] | None = Field(
        default=None, description="List of member user IDs"
    )
    assignees: list[UserID] | None = Field(
        default=None, description="List of assignee user IDs"
    )
    receivedAt: str | None = Field(default=None, description="Date card was received")
    dueAt: str | None = Field(default=None, description="Due date")
    endsAt: str | None = Field(default=None, description="End date")
    cardNumber: int | None = Field(default=None, description="Card number (read-only)")
    sort: int | None = Field(default=None, description="Sort order")
    customFields: list[dict] | None = Field(
        default=None, description="Custom field values"
    )
    dateLastActivity: str | None = Field(
        default=None, description="Date of last activity (read-only)"
    )
    startAt: str | None = Field(default=None, description="Start date")
    vote: Vote | None = Field(default=None, description="Vote object")


# ---------------------------------------------------------------------------
# Comment types
# ---------------------------------------------------------------------------


class CommentId(WeKanModel):
    commentId: str = Field(validation_alias="_id", description="Comment ID")


class Comment(CommentId):
    comment: str = Field(description="Comment text")
    authorId: UserID = Field(description="Author user ID")


class CommentDetails(CommentId):
    boardId: str | None = Field(default=None, description="Board ID")
    cardId: str | None = Field(default=None, description="Card ID")
    text: str | None = Field(default=None, description="Comment text")
    createdAt: str | None = Field(default=None, description="Date comment was created")
    modifiedAt: str | None = Field(
        default=None, description="Date comment was last modified"
    )
    userId: UserID | None = Field(default=None, description="Author user ID")


# ---------------------------------------------------------------------------
# Checklist types
# ---------------------------------------------------------------------------


class ChecklistId(WeKanModel):
    checklistId: str = Field(validation_alias="_id", description="Checklist ID")


class Checklist(ChecklistId):
    title: str = Field(description="Checklist title")


class ChecklistItemId(WeKanModel):
    checklistItemId: str = Field(
        validation_alias="_id", description="Checklist item ID"
    )


class ChecklistItem(ChecklistItemId):
    title: str = Field(description="Item title")
    isFinished: bool = Field(description="Whether the item is finished")


class ChecklistDetails(ChecklistId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})
    cardId: str | None = Field(default=None, description="Card ID")
    title: str = Field(description="Checklist title")
    finishedAt: str | None = Field(
        default=None, description="Date checklist was completed"
    )
    createdAt: str | None = Field(
        default=None, description="Date checklist was created"
    )
    sort: int | None = Field(default=None, description="Sort order")
    items: list[ChecklistItem] | None = Field(
        default=None, description="List of checklist items"
    )


class ChecklistItemDetails(ChecklistItemId):
    title: str = Field(description="Item title")
    sort: int | None = Field(default=None, description="Sort order")
    isFinished: bool | None = Field(
        default=None, description="Whether the item is finished"
    )
    checklistId: str | None = Field(default=None, description="Checklist ID")
    cardId: str | None = Field(default=None, description="Card ID")
    createdAt: str | None = Field(default=None, description="Date item was created")
    modifiedAt: str | None = Field(
        default=None, description="Date item was last modified"
    )
