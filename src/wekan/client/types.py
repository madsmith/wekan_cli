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


class LabelId(WeKanModel):
    labelId: str = Field(validation_alias="_id", description="Label ID")


class BoardLabel(LabelId):
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


class Email(WeKanModel):
    address: str = Field(description="Email address")
    verified: bool = Field(description="Whether the email is verified")


class UserDetails(User):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})

    # --- All fields are read-only ---
    # PUT /api/users/:userId only accepts action (disableLogin/enableLogin/takeOwnership)
    # No field-level editing via REST API
    username: str = Field(
        description="Username",
        json_schema_extra={"editable": False},
    )
    createdAt: str = Field(
        description="Date user was created",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date user was last modified",
        json_schema_extra={"editable": False},
    )
    authenticationMethod: str = Field(
        description="Authentication method",
        json_schema_extra={"editable": False},
    )
    emails: list[Email] | None = Field(
        default=None,
        description="List of email addresses",
        json_schema_extra={"editable": False},
    )
    isAdmin: bool | None = Field(
        default=None,
        description="Whether the user is an Admin",
        json_schema_extra={"editable": False},
    )
    # Computed field: injected by GET endpoint, not a Mongo schema field
    boards: list[BoardMembership] | None = Field(
        default=None,
        description="List of board memberships",
        json_schema_extra={"editable": False},
    )


class BoardDetails(BoardId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})

    # --- Editable fields ---
    # Only title has a REST PUT endpoint: PUT /api/boards/:id/title
    title: str = Field(description="Board title")
    # No REST PUT endpoint for these; editable via Meteor UI only
    description: str | None = Field(default=None, description="Board description")
    color: BoardColor | None = Field(default=None, description="Board theme color")
    permission: BoardPermission | None = Field(
        default=None, description="Board permission (public/private)"
    )

    # --- Managed via dedicated endpoints (read-only on board object) ---
    # Labels: add-only via PUT /api/boards/:id/labels; no edit/delete REST API
    labels: list[BoardLabel] = Field(
        default_factory=list,
        description="List of board labels",
        json_schema_extra={"editable": False},
    )
    # Members: managed via /api/boards/:id/members endpoints
    members: list[BoardMember] = Field(
        default_factory=list,
        description="List of board members",
        json_schema_extra={"editable": False},
    )
    teams: list[BoardTeam] | None = Field(
        default=None,
        description="List of board teams",
        json_schema_extra={"editable": False},
    )
    orgs: list[BoardOrg] | None = Field(
        default=None,
        description="List of board organizations",
        json_schema_extra={"editable": False},
    )

    # --- Server-maintained (read-only) ---
    archived: bool = Field(
        default=False,
        description="Whether the board is archived",
        json_schema_extra={"editable": False},
    )
    archivedAt: str | None = Field(
        default=None,
        description="Date board was archived",
        json_schema_extra={"editable": False},
    )
    createdAt: str = Field(
        description="Date board was created",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date board was last modified",
        json_schema_extra={"editable": False},
    )
    sort: int = Field(
        default=-1,
        description="Sort order",
        json_schema_extra={"editable": False},
    )

    # --- Esoteric config (no REST API) ---
    subtasksDefaultBoardId: str | None = Field(
        default=None,
        description="Default board ID for subtasks",
        json_schema_extra={"editable": False},
    )
    subtasksDefaultListId: str | None = Field(
        default=None,
        description="Default list ID for subtasks",
        json_schema_extra={"editable": False},
    )
    presentParentTask: str | None = Field(
        default=None,
        description="Parent task display mode",
        json_schema_extra={"editable": False},
    )
    receivedAt: str | None = Field(
        default=None,
        description="Date board was received",
        json_schema_extra={"editable": False},
    )
    startAt: str | None = Field(
        default=None,
        description="Start date",
        json_schema_extra={"editable": False},
    )
    dueAt: str | None = Field(
        default=None,
        description="Due date",
        json_schema_extra={"editable": False},
    )


# ---------------------------------------------------------------------------
# Swimlane types
# ---------------------------------------------------------------------------


class SwimlaneId(WeKanModel):
    swimlaneId: str = Field(validation_alias="_id", description="Swimlane ID")


class SwimlaneInfo(SwimlaneId):
    title: str = Field(description="Swimlane title")


class SwimlaneDetails(SwimlaneId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})

    # --- Foreign key ---
    boardId: str = Field(
        description="Board ID the swimlane belongs to",
        json_schema_extra={"editable": False},
    )

    # --- Editable fields ---
    # PUT /api/boards/:boardId/swimlanes/:swimlaneId accepts only title
    title: str = Field(description="Swimlane title")
    color: Color | None = Field(default=None, description="Swimlane color")

    # --- Server-maintained (read-only) ---
    archived: bool = Field(
        default=False,
        description="Whether the swimlane is archived",
        json_schema_extra={"editable": False},
    )
    archivedAt: str | None = Field(
        default=None,
        description="Date swimlane was archived",
        json_schema_extra={"editable": False},
    )
    createdAt: str = Field(
        description="Date swimlane was created",
        json_schema_extra={"editable": False},
    )
    updatedAt: str = Field(
        description="Date swimlane was last updated",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date swimlane was last modified",
        json_schema_extra={"editable": False},
    )
    sort: int | None = Field(
        default=None,
        description="Sort order",
        # No REST API to reorder swimlanes (UI-only via Meteor DDP)
        json_schema_extra={"editable": False},
    )

    # --- Esoteric (read-only) ---
    type: str = Field(
        default="swimlane",
        description="Swimlane type",
        json_schema_extra={"editable": False},
    )
    height: int = Field(
        default=-1,
        description="Swimlane height in pixels (-1 = auto)",
        json_schema_extra={"editable": False},
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
    value: int = Field(default=1, description="WIP limit value")
    enabled: bool = Field(default=False, description="Whether WIP limit is enabled")
    soft: bool = Field(default=False, description="Whether the limit is a soft limit")


class ListDetails(ListId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})

    # --- Foreign keys ---
    boardId: str = Field(
        description="Board ID the list belongs to",
        json_schema_extra={"editable": False},
    )
    swimlaneId: str = Field(
        default="",
        description="Swimlane ID the list belongs to",
        json_schema_extra={"editable": False},
    )

    # --- Editable fields ---
    # PUT /api/boards/:boardId/lists/:listId accepts title, color, starred, wipLimit
    title: str = Field(description="List title")
    color: Color | None = Field(default=None, description="List color")
    starred: bool = Field(default=False, description="Whether the list is starred")
    wipLimit: WIPLimit | None = Field(
        default=None, description="Work-in-progress limit"
    )

    # --- Server-maintained (read-only) ---
    archived: bool = Field(
        default=False,
        description="Whether the list is archived",
        # No REST archive/unarchive endpoint for lists (UI-only via Meteor DDP)
        json_schema_extra={"editable": False},
    )
    archivedAt: str | None = Field(
        default=None,
        description="Date list was archived",
        json_schema_extra={"editable": False},
    )
    createdAt: str = Field(
        description="Date list was created",
        json_schema_extra={"editable": False},
    )
    updatedAt: str = Field(
        description="Date list was last updated",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date list was last modified",
        json_schema_extra={"editable": False},
    )
    sort: int | None = Field(
        default=None,
        description="Sort order",
        # No REST API to reorder lists (UI-only via Meteor DDP)
        json_schema_extra={"editable": False},
    )

    # --- Esoteric (read-only) ---
    type: str = Field(
        default="list",
        description="List type",
        json_schema_extra={"editable": False},
    )
    width: int = Field(
        default=272,
        description="List width in pixels",
        json_schema_extra={"editable": False},
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
    question: str = Field(default="", description="Vote question text")
    positive: list[UserID] = Field(
        default_factory=list, description="User IDs who voted in favor"
    )
    negative: list[UserID] = Field(
        default_factory=list, description="User IDs who voted against"
    )
    end: str | None = Field(default=None, description="Vote end date")
    public: bool = Field(default=False, description="Whether the vote is public")
    allowNonBoardMembers: bool = Field(
        default=False, description="Allow non-board members to vote"
    )


class Poker(WeKanModel):
    question: bool | None = Field(default=None, description="Whether poker estimation is active")
    allowNonBoardMembers: bool | None = Field(default=None, description="Allow non-board members")
    estimation: int | None = Field(default=None, description="Final estimation value")
    end: str | None = Field(default=None, description="Poker end date")
    # Vote arrays: each contains user IDs who selected that card value
    one: list[UserID] | None = Field(default=None, description="Users who voted 1")
    two: list[UserID] | None = Field(default=None, description="Users who voted 2")
    three: list[UserID] | None = Field(default=None, description="Users who voted 3")
    five: list[UserID] | None = Field(default=None, description="Users who voted 5")
    eight: list[UserID] | None = Field(default=None, description="Users who voted 8")
    thirteen: list[UserID] | None = Field(default=None, description="Users who voted 13")
    twenty: list[UserID] | None = Field(default=None, description="Users who voted 20")
    forty: list[UserID] | None = Field(default=None, description="Users who voted 40")
    oneHundred: list[UserID] | None = Field(default=None, description="Users who voted 100")
    unsure: list[UserID] | None = Field(default=None, description="Users who voted unsure")


class CardDetails(CardId):
    model_config = ConfigDict(json_schema_extra={"partial_field_def": True})

    # --- Foreign keys (editable for moving cards) ---
    boardId: str = Field(description="Board ID the card belongs to")
    listId: str = Field(description="List ID the card belongs to")
    swimlaneId: str = Field(description="Swimlane ID the card belongs to")

    # --- Core editable fields ---
    title: str = Field(description="Card title")
    description: str = Field(default="", description="Card description (markdown)")
    color: Color | None = Field(default=None, description="Card color")
    sort: int = Field(default=0, description="Sort order")
    labelIds: list[str] = Field(default_factory=list, description="List of label IDs")
    members: list[UserID] = Field(
        default_factory=list, description="List of member user IDs"
    )
    assignees: list[UserID] = Field(
        default_factory=list, description="List of assignee user IDs"
    )

    # --- Date fields (editable) ---
    receivedAt: str | None = Field(default=None, description="Date card was received")
    startAt: str | None = Field(default=None, description="Start date")
    dueAt: str | None = Field(default=None, description="Due date")
    endsAt: str | None = Field(
        default=None,
        description="End date",
        json_schema_extra={"edit_key": "endAt"},
    )

    # --- Advanced editable fields (hidden from default --help) ---
    requestedBy: str = Field(
        default="", description="User ID who requested the card",
        json_schema_extra={"advanced": True},
    )
    assignedBy: str = Field(
        default="", description="User ID who assigned the card",
        json_schema_extra={"advanced": True},
    )
    customFields: list[dict] = Field(
        default_factory=list, description="Custom field values",
        json_schema_extra={"advanced": True},
    )
    spentTime: float = Field(
        default=0, description="Time spent on card",
        json_schema_extra={"advanced": True},
    )
    isOverTime: bool = Field(
        default=False, description="Whether card is over time",
        json_schema_extra={"advanced": True},
    )
    parentId: str = Field(
        default="", description="Parent card ID (for subtasks)",
        json_schema_extra={"advanced": True},
    )
    vote: Vote | None = Field(
        default=None, description="Vote object",
        json_schema_extra={"advanced": True},
    )
    poker: Poker | None = Field(
        default=None, description="Poker estimation object",
        json_schema_extra={"advanced": True},
    )

    # --- Server-maintained (read-only) ---
    # autoValue fields — guaranteed present in every GET response
    archived: bool = Field(
        default=False,
        description="Whether the card is archived",
        json_schema_extra={"edit_key": "archive", "editable": False},
    )
    createdAt: str = Field(
        description="Date card was created",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date card was last modified",
        json_schema_extra={"editable": False},
    )
    dateLastActivity: str = Field(
        description="Date of last activity",
        json_schema_extra={"editable": False},
    )
    # defaultValue fields
    cardNumber: int = Field(
        default=0,
        description="Card number",
        json_schema_extra={"editable": False},
    )
    # truly optional — only present when archived
    archivedAt: str | None = Field(
        default=None,
        description="Date card was archived",
        json_schema_extra={"editable": False},
    )


# ---------------------------------------------------------------------------
# Comment types
# ---------------------------------------------------------------------------


class CommentId(WeKanModel):
    commentId: str = Field(validation_alias="_id", description="Comment ID")


class Comment(CommentId):
    comment: str = Field(description="Comment text")
    authorId: UserID = Field(description="Author user ID")


class CommentDetails(CommentId):
    # --- Foreign keys ---
    boardId: str = Field(
        description="Board ID",
        json_schema_extra={"editable": False},
    )
    cardId: str = Field(
        description="Card ID",
        json_schema_extra={"editable": False},
    )

    # --- Content ---
    text: str = Field(description="Comment text")

    # --- Server-maintained (read-only) ---
    createdAt: str = Field(
        description="Date comment was created",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date comment was last modified",
        json_schema_extra={"editable": False},
    )
    userId: UserID = Field(
        description="Author user ID",
        json_schema_extra={"editable": False},
    )


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

    # --- Foreign keys ---
    cardId: str = Field(
        description="Card ID",
        json_schema_extra={"editable": False},
    )

    # --- Editable fields ---
    # No REST PUT endpoint exists for checklists; title is only editable via Meteor UI
    title: str = Field(description="Checklist title")

    # --- Server-maintained (read-only) ---
    # sort is set on creation; no REST API to reorder checklists (UI-only)
    sort: int = Field(
        description="Sort order",
        json_schema_extra={"editable": False},
    )
    finishedAt: str | None = Field(
        default=None,
        description="Date checklist was completed",
        json_schema_extra={"editable": False},
    )
    createdAt: str = Field(
        description="Date checklist was created",
        json_schema_extra={"editable": False},
    )
    items: list[ChecklistItem] | None = Field(
        default=None,
        description="List of checklist items",
        json_schema_extra={"editable": False},
    )


class ChecklistItemDetails(ChecklistItemId):
    # --- Foreign keys ---
    checklistId: str = Field(
        description="Checklist ID",
        json_schema_extra={"editable": False},
    )
    cardId: str = Field(
        description="Card ID",
        json_schema_extra={"editable": False},
    )

    # --- Editable fields (accepted by PUT) ---
    title: str = Field(description="Item title")
    isFinished: bool = Field(default=False, description="Whether the item is finished")

    # --- Server-maintained (read-only) ---
    # sort is set on creation; no REST API to reorder checklist items (UI-only)
    sort: int = Field(
        description="Sort order",
        json_schema_extra={"editable": False},
    )
    createdAt: str = Field(
        description="Date item was created",
        json_schema_extra={"editable": False},
    )
    modifiedAt: str = Field(
        description="Date item was last modified",
        json_schema_extra={"editable": False},
    )
