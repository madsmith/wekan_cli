# WeKan REST API Reference

Complete reference for the WeKan REST API (v8.33). All endpoints return JSON.

---

## Authentication

Most endpoints require two HTTP headers:

| Header | Description |
|--------|-------------|
| `X-User-Id` | User ID from login |
| `X-Auth-Token` | Token from login |

### Login

```bash
curl -X POST http://localhost:3000/users/login \
  -d "username=admin&password=secret"
```

Response:

```json
{ "id": "user-id", "token": "auth-token", "tokenExpires": "..." }
```

Use the returned `id` as `X-User-Id` and `token` as `X-Auth-Token` for subsequent requests.

### Register

```bash
curl -X POST http://localhost:3000/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"pass","email":"user@example.com"}'
```

---

## Users

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/user` | Get current user | User |
| `GET` | `/api/users` | Get all users | Admin |
| `GET` | `/api/users/:userId` | Get a user by ID or username | Admin |
| `PUT` | `/api/users/:userId` | Edit a user (actions: takeOwnership, disableLogin, enableLogin) | Admin |
| `POST` | `/api/users/` | Create a new user | Admin |
| `DELETE` | `/api/users/:userId` | Delete a user | Admin |
| `POST` | `/api/createtoken/:userId` | Create a login token for a user | Admin |
| `POST` | `/api/deletetoken` | Delete one or all user tokens | Admin |

### GET /api/user

Returns the currently authenticated user with board membership info.

**Response:** User object with `boards` array containing `{ boardId, isAdmin, isActive, ... }`.

### GET /api/users

Returns all users as `[{ _id, username }]`. Admin only.

### GET /api/users/:userId

Returns full user object. The `:userId` parameter accepts either a user ID or username. Admin only.

### PUT /api/users/:userId

**Body:**

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | **Required.** One of: `takeOwnership`, `disableLogin`, `enableLogin` |

- `takeOwnership` — Admin takes ownership of all boards where the user is admin.
- `disableLogin` — Disables user login and purges tokens.
- `enableLogin` — Re-enables login.

### POST /api/users/

**Body:**

| Field | Type | Required |
|-------|------|----------|
| `username` | string | Yes |
| `email` | string | Yes |
| `password` | string | Yes |

**Response:** `{ _id }`.

### DELETE /api/users/:userId

**Response:** `{ _id }`.

### POST /api/createtoken/:userId

Creates a login token for the specified user. Admin only.

**Response:** `{ _id, authToken }`.

### POST /api/deletetoken

**Body:**

| Field | Type | Description |
|-------|------|-------------|
| `userId` | string | **Required.** User ID |
| `token` | string | Specific hashed token to delete. Omit to delete all tokens. |

**Response:** `{ message }`.

---

## Boards

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/users/:userId/boards` | Get all boards for a user | User |
| `GET` | `/api/boards` | Get all public boards | Admin |
| `GET` | `/api/boards_count` | Get board counts (public/private) | Admin |
| `GET` | `/api/boards/:boardId` | Get a board | Board access |
| `POST` | `/api/boards` | Create a board | User |
| `DELETE` | `/api/boards/:boardId` | Delete a board | Admin |
| `PUT` | `/api/boards/:boardId/title` | Update board title | Board write |
| `PUT` | `/api/boards/:boardId/labels` | Add a label | Board write |
| `POST` | `/api/boards/:boardId/copy` | Copy a board | Board admin |
| `POST` | `/api/boards/:boardId/members/:memberId` | Set member permission | Admin |
| `POST` | `/api/boards/:boardId/members/:userId/add` | Add member to board | Admin |
| `POST` | `/api/boards/:boardId/members/:userId/remove` | Remove member from board | Admin |
| `GET` | `/api/boards/:boardId/attachments` | Get board attachments | Board access |

### GET /api/users/:userId/boards

Returns `[{ _id, title }]` of all non-archived boards the user belongs to.

### GET /api/boards

Returns `[{ _id, title }]` of all public boards. Admin only.

### GET /api/boards_count

**Response:** `{ private: number, public: number }`.

### GET /api/boards/:boardId

Returns the full board object.

### POST /api/boards

**Body:**

| Field | Type | Required | Default |
|-------|------|----------|---------|
| `title` | string | Yes | |
| `owner` | string | Yes | |
| `isAdmin` | boolean | No | `true` |
| `isActive` | boolean | No | `true` |
| `isNoComments` | boolean | No | `false` |
| `isCommentOnly` | boolean | No | `false` |
| `isWorker` | boolean | No | `false` |
| `permission` | string | No | `private` |
| `color` | string | No | `belize` |

Colors: `belize`, `nephritis`, `pomegranate`, `pumpkin`, `wisteria`, `moderatepink`, `strongcyan`, `limegreen`, `midnight`, `dark`, `relax`, `corteza`.

**Response:** `{ _id, defaultSwimlaneId }`.

### DELETE /api/boards/:boardId

**Response:** `{ _id }`.

### PUT /api/boards/:boardId/title

**Body:** `{ title }`.

**Response:** `{ _id, title }`.

### PUT /api/boards/:boardId/labels

**Body:** `{ label: { color, name } }`.

**Response:** Label ID string.

### POST /api/boards/:boardId/copy

**Body (optional):** `{ title }`.

**Response:** New board ID string.

### POST /api/boards/:boardId/members/:memberId

Sets permissions on an existing board member.

**Body:**

| Field | Type |
|-------|------|
| `isAdmin` | boolean |
| `isNoComments` | boolean |
| `isCommentOnly` | boolean |
| `isWorker` | boolean |
| `isNormalAssignedOnly` | boolean |
| `isCommentAssignedOnly` | boolean |
| `isReadOnly` | boolean |
| `isReadAssignedOnly` | boolean |

### POST /api/boards/:boardId/members/:userId/add

**Body:**

| Field | Type | Required |
|-------|------|----------|
| `action` | string | Yes (`"add"`) |
| `isAdmin` | string | No |
| `isNoComments` | string | No |
| `isCommentOnly` | string | No |
| `isWorker` | string | No |
| `isNormalAssignedOnly` | string | No |
| `isCommentAssignedOnly` | string | No |
| `isReadOnly` | string | No |
| `isReadAssignedOnly` | string | No |

**Response:** `[{ _id, title }]`.

### POST /api/boards/:boardId/members/:userId/remove

**Body:** `{ action: "remove" }`.

**Response:** `[{ _id, title }]`.

### GET /api/boards/:boardId/attachments

**Response:** Array of attachment objects:

```json
[{
  "attachmentId": "...",
  "attachmentName": "...",
  "attachmentType": "...",
  "url": "...",
  "urlDownload": "...",
  "boardId": "...",
  "swimlaneId": "...",
  "listId": "...",
  "cardId": "..."
}]
```

---

## Lists

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/lists` | Get all lists | Board access |
| `GET` | `/api/boards/:boardId/lists/:listId` | Get a list | Board access |
| `POST` | `/api/boards/:boardId/lists` | Create a list | Board write |
| `PUT` | `/api/boards/:boardId/lists/:listId` | Edit a list | Board write |
| `DELETE` | `/api/boards/:boardId/lists/:listId` | Delete a list | Board write |

### GET /api/boards/:boardId/lists

Returns `[{ _id, title }]` of non-archived lists.

### GET /api/boards/:boardId/lists/:listId

Returns the full list object.

### POST /api/boards/:boardId/lists

**Body:**

| Field | Type | Required |
|-------|------|----------|
| `title` | string | Yes |
| `swimlaneId` | string | No (defaults to board default) |

**Response:** `{ _id }`.

### PUT /api/boards/:boardId/lists/:listId

**Body:**

| Field | Type |
|-------|------|
| `title` | string |
| `color` | string |
| `wipLimit` | object |
| `starred` | boolean |

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/lists/:listId

**Response:** `{ _id }`.

---

## Swimlanes

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/swimlanes` | Get all swimlanes | Board access |
| `GET` | `/api/boards/:boardId/swimlanes/:swimlaneId` | Get a swimlane | Board access |
| `POST` | `/api/boards/:boardId/swimlanes` | Create a swimlane | Board write |
| `PUT` | `/api/boards/:boardId/swimlanes/:swimlaneId` | Edit a swimlane | Board write |
| `DELETE` | `/api/boards/:boardId/swimlanes/:swimlaneId` | Delete a swimlane | Board write |

### GET /api/boards/:boardId/swimlanes

Returns `[{ _id, title }]` of non-archived swimlanes.

### GET /api/boards/:boardId/swimlanes/:swimlaneId

Returns the full swimlane object.

### POST /api/boards/:boardId/swimlanes

**Body:** `{ title }`.

**Response:** `{ _id }`.

### PUT /api/boards/:boardId/swimlanes/:swimlaneId

**Body:** `{ title }`.

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/swimlanes/:swimlaneId

**Response:** `{ _id }`.

---

## Cards

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/swimlanes/:swimlaneId/cards` | Get cards in a swimlane | Board access |
| `GET` | `/api/boards/:boardId/lists/:listId/cards` | Get cards in a list | Board access |
| `GET` | `/api/cards/:cardId` | Get a card by ID | Board access |
| `GET` | `/api/boards/:boardId/lists/:listId/cards/:cardId` | Get a card | Board access |
| `POST` | `/api/boards/:boardId/lists/:listId/cards` | Create a card | Board write |
| `PUT` | `/api/boards/:boardId/lists/:listId/cards/:cardId` | Edit a card | Board write |
| `DELETE` | `/api/boards/:boardId/lists/:listId/cards/:cardId` | Delete a card | Board write |
| `GET` | `/api/boards/:boardId/cards_count` | Get board cards count | Board access |
| `GET` | `/api/boards/:boardId/lists/:listId/cards_count` | Get list cards count | Board access |
| `GET` | `/api/boards/:boardId/cardsByCustomField/:customFieldId/:customFieldValue` | Get cards by custom field | Board access |
| `POST` | `/api/boards/:boardId/lists/:listId/cards/:cardId/customFields/:customFieldId` | Edit card custom field value | Board write |
| `POST` | `/api/boards/:boardId/lists/:listId/cards/:cardId/archive` | Archive a card | Board write |
| `POST` | `/api/boards/:boardId/lists/:listId/cards/:cardId/unarchive` | Unarchive a card | Board write |

### GET /api/boards/:boardId/swimlanes/:swimlaneId/cards

Returns cards with `{ _id, title, description, listId, receivedAt, startAt, dueAt, endAt, assignees, sort }`.

### GET /api/boards/:boardId/lists/:listId/cards

Returns cards with `{ _id, title, description, swimlaneId, receivedAt, startAt, dueAt, endAt, assignees, sort }`.

### GET /api/cards/:cardId

Returns the full card object.

### GET /api/boards/:boardId/lists/:listId/cards/:cardId

Returns the full card object.

### POST /api/boards/:boardId/lists/:listId/cards

**Body:**

| Field | Type | Required |
|-------|------|----------|
| `title` | string | Yes |
| `authorId` | string | Yes |
| `swimlaneId` | string | Yes |
| `description` | string | No |
| `parentId` | string | No |
| `members` | string[] | No |
| `assignees` | string[] | No |

**Response:** `{ _id }`.

### PUT /api/boards/:boardId/lists/:listId/cards/:cardId

**Body (all fields optional):**

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | New title |
| `description` | string | New description |
| `sort` | number | Sort position |
| `listId` | string | Move to different list |
| `parentId` | string | Change parent |
| `authorId` | string | Change owner |
| `labelIds` | string[] | Label IDs |
| `swimlaneId` | string | Move to different swimlane |
| `members` | string[] | Member IDs |
| `assignees` | string[] | Assignee IDs |
| `requestedBy` | string | Requested by |
| `assignedBy` | string | Assigned by |
| `receivedAt` | datetime | Received date |
| `startAt` | datetime | Start date |
| `dueAt` | datetime | Due date |
| `endAt` | datetime | End date |
| `spentTime` | number | Time spent |
| `isOverTime` | boolean | Over time flag |
| `customFields` | object[] | Custom field values |
| `color` | string | Card color |
| `vote` | object | `{ question, public, allowNonBoardMembers }` |
| `poker` | object | `{ question, allowNonBoardMembers }` |

Card colors: `white`, `green`, `yellow`, `orange`, `red`, `purple`, `blue`, `sky`, `lime`, `pink`, `black`, `silver`, `peachpuff`, `crimson`, `plum`, `darkgreen`, `slateblue`, `magenta`, `gold`, `navy`, `gray`, `saddlebrown`, `paleturquoise`, `mistyrose`, `indigo`.

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/lists/:listId/cards/:cardId

**Response:** `{ _id }`.

### GET /api/boards/:boardId/cards_count

**Response:** `{ board_cards_count: number }`.

### GET /api/boards/:boardId/lists/:listId/cards_count

**Response:** `{ list_cards_count: number }`.

### GET /api/boards/:boardId/cardsByCustomField/:customFieldId/:customFieldValue

Returns full card objects that match the given custom field value.

### POST /api/boards/:boardId/lists/:listId/cards/:cardId/customFields/:customFieldId

**Body:** `{ value: <any> }`.

**Response:** `{ _id, customFields: [{ _id, value }] }`.

### POST /api/boards/:boardId/lists/:listId/cards/:cardId/archive

**Response:** `{ _id, archived: true, archivedAt: <datetime> }`.

### POST /api/boards/:boardId/lists/:listId/cards/:cardId/unarchive

**Response:** `{ _id, archived: false }`.

---

## Checklists

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/cards/:cardId/checklists` | Get all checklists | Board access |
| `GET` | `/api/boards/:boardId/cards/:cardId/checklists/:checklistId` | Get a checklist | Board access |
| `POST` | `/api/boards/:boardId/cards/:cardId/checklists` | Create a checklist | Board write |
| `DELETE` | `/api/boards/:boardId/cards/:cardId/checklists/:checklistId` | Delete a checklist | Board access |

### GET /api/boards/:boardId/cards/:cardId/checklists

Returns `[{ _id, title }]`.

### GET /api/boards/:boardId/cards/:cardId/checklists/:checklistId

Returns checklist with items: `{ cardId, title, finishedAt, createdAt, sort, items: [{ _id, title, isFinished }] }`.

### POST /api/boards/:boardId/cards/:cardId/checklists

**Body:**

| Field | Type | Required |
|-------|------|----------|
| `title` | string | Yes |
| `items` | string[] | No |

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/cards/:cardId/checklists/:checklistId

**Response:** `{ _id }`.

---

## Checklist Items

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/cards/:cardId/checklists/:checklistId/items/:itemId` | Get an item | Board access |
| `POST` | `/api/boards/:boardId/cards/:cardId/checklists/:checklistId/items` | Create an item | Board access |
| `PUT` | `/api/boards/:boardId/cards/:cardId/checklists/:checklistId/items/:itemId` | Edit an item | Board access |
| `DELETE` | `/api/boards/:boardId/cards/:cardId/checklists/:checklistId/items/:itemId` | Delete an item | Board access |

### GET .../items/:itemId

Returns the full checklist item object.

### POST .../items

**Body:** `{ title }`.

**Response:** `{ _id }`.

### PUT .../items/:itemId

**Body:**

| Field | Type |
|-------|------|
| `title` | string |
| `isFinished` | boolean |

**Response:** `{ _id }`.

### DELETE .../items/:itemId

**Response:** `{ _id }`.

---

## Card Comments

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/cards/:cardId/comments` | Get all comments | Board access |
| `GET` | `/api/boards/:boardId/cards/:cardId/comments/:commentId` | Get a comment | Board access |
| `POST` | `/api/boards/:boardId/cards/:cardId/comments` | Add a comment | Board access |
| `DELETE` | `/api/boards/:boardId/cards/:cardId/comments/:commentId` | Delete a comment | Board access |

### GET /api/boards/:boardId/cards/:cardId/comments

Returns `[{ _id, comment, authorId }]`.

### GET /api/boards/:boardId/cards/:cardId/comments/:commentId

Returns the full comment object.

### POST /api/boards/:boardId/cards/:cardId/comments

**Body:** `{ comment: "text" }`.

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/cards/:cardId/comments/:commentId

**Response:** `{ _id }`.

---

## Custom Fields

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/custom-fields` | Get all custom fields | Board access |
| `GET` | `/api/boards/:boardId/custom-fields/:customFieldId` | Get a custom field | Board access |
| `POST` | `/api/boards/:boardId/custom-fields` | Create a custom field | Board access |
| `PUT` | `/api/boards/:boardId/custom-fields/:customFieldId` | Edit a custom field | Board access |
| `DELETE` | `/api/boards/:boardId/custom-fields/:customFieldId` | Delete a custom field | Board access |
| `POST` | `/api/boards/:boardId/custom-fields/:customFieldId/dropdown-items` | Add dropdown items | Board access |
| `PUT` | `/api/boards/:boardId/custom-fields/:customFieldId/dropdown-items/:dropdownItemId` | Edit dropdown item | Board access |
| `DELETE` | `/api/boards/:boardId/custom-fields/:customFieldId/dropdown-items/:dropdownItemId` | Delete dropdown item | Board access |

### GET /api/boards/:boardId/custom-fields

Returns `[{ _id, name, type }]`.

### GET /api/boards/:boardId/custom-fields/:customFieldId

Returns the full custom field object.

### POST /api/boards/:boardId/custom-fields

**Body:**

| Field | Type | Required |
|-------|------|----------|
| `name` | string | Yes |
| `type` | string | Yes |
| `settings` | object | No |
| `showOnCard` | boolean | No |
| `automaticallyOnCard` | boolean | No |
| `showLabelOnMiniCard` | boolean | No |
| `showSumAtTopOfList` | boolean | No |
| `authorId` | string | No |

Field types: `text`, `number`, `date`, `dropdown`, `checkbox`, `currency`, `stringtemplate`.

**Response:** `{ _id }`.

### PUT /api/boards/:boardId/custom-fields/:customFieldId

**Body (all optional):** `name`, `type`, `settings`, `showOnCard`, `automaticallyOnCard`, `alwaysOnCard`, `showLabelOnMiniCard`, `showSumAtTopOfList`.

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/custom-fields/:customFieldId

**Response:** `{ _id }`.

### POST .../dropdown-items

**Body:** `{ items: ["Item 1", "Item 2"] }`.

**Response:** `{ _id }`.

### PUT .../dropdown-items/:dropdownItemId

**Body:** `{ name: "New Name" }`.

**Response:** `{ _id }`.

### DELETE .../dropdown-items/:dropdownItemId

**Response:** `{ _id }`.

---

## Integrations

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/integrations` | Get all integrations | Board access |
| `GET` | `/api/boards/:boardId/integrations/:intId` | Get an integration | Board access |
| `POST` | `/api/boards/:boardId/integrations` | Create an integration | Board access |
| `PUT` | `/api/boards/:boardId/integrations/:intId` | Edit an integration | Board access |
| `DELETE` | `/api/boards/:boardId/integrations/:intId` | Delete an integration | Board access |
| `POST` | `/api/boards/:boardId/integrations/:intId/activities` | Add subscribed activities | Board access |
| `DELETE` | `/api/boards/:boardId/integrations/:intId/activities` | Remove subscribed activities | Board access |

### GET /api/boards/:boardId/integrations

Returns array of integration objects (token field excluded).

### GET /api/boards/:boardId/integrations/:intId

Returns the integration object (token field excluded).

### POST /api/boards/:boardId/integrations

**Body:** `{ url: "https://..." }`.

**Response:** `{ _id }`.

### PUT /api/boards/:boardId/integrations/:intId

**Body (all optional):**

| Field | Type |
|-------|------|
| `enabled` | boolean |
| `title` | string |
| `url` | string |
| `token` | string |
| `activities` | string[] |

**Response:** `{ _id }`.

### DELETE /api/boards/:boardId/integrations/:intId

**Response:** `{ _id }`.

### POST .../activities

**Body:** `{ activities: ["all", "createCard", ...] }`.

**Response:** Updated integration with `{ _id, activities }`.

### DELETE .../activities

**Body:** `{ activities: ["createCard"] }`.

**Response:** Updated integration with `{ _id, activities }`.

---

## Export

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/api/boards/:boardId/export` | Export board as JSON | Token or public |
| `GET` | `/api/boards/:boardId/attachments/:attachmentId/export` | Export attachment as JSON | Token or public |

### GET /api/boards/:boardId/export

Export a complete board as JSON. Public boards require no auth. For private boards, pass `?authToken=<loginToken>`.

### GET /api/boards/:boardId/attachments/:attachmentId/export

Export a single attachment as JSON. Same auth rules as board export.

---

## Endpoint Count Summary

| Resource | Endpoints |
|----------|-----------|
| Authentication | 2 |
| Users | 8 |
| Boards | 13 |
| Lists | 5 |
| Swimlanes | 5 |
| Cards | 13 |
| Checklists | 4 |
| Checklist Items | 4 |
| Card Comments | 4 |
| Custom Fields | 8 |
| Integrations | 7 |
| Export | 2 |
| **Total** | **75** |
