# WeKan REST API — Editable Fields by Entity

## Board

There is no general-purpose PUT for boards. Title and labels have separate endpoints.

### `PUT /api/boards/:boardId/title`

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Required |

### `PUT /api/boards/:boardId/labels`

| Field | Type | Notes |
|-------|------|-------|
| `label` | object | Required. Contains `name` (string) and `color` (string) |

> Note: No way to archive, update description, change color, or change permission via REST.

---

## Swimlane

### `PUT /api/boards/:boardId/swimlanes/:swimlaneId`

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Required |

> Note: No archive/unarchive via REST.

---

## List

### `PUT /api/boards/:boardId/lists/:listId`

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | |
| `color` | string | |
| `wipLimit` | object | WIP limit configuration |
| `starred` | boolean | |

> Note: No archive/unarchive via REST.

---

## Card

### `PUT /api/boards/:boardId/lists/:listId/cards/:cardId`

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Truncated to 1000 chars |
| `sort` | number | Sort position |
| `parentId` | string | |
| `description` | string | |
| `color` | string | Card color |
| `vote` | object | `{ question: string, public: boolean, allowNonBoardMembers: boolean }` |
| `poker` | object | `{ question: string, allowNonBoardMembers: boolean }` |
| `labelIds` | string or string[] | Empty string clears labels |
| `requestedBy` | string | |
| `assignedBy` | string | |
| `receivedAt` | datetime | |
| `startAt` | datetime | |
| `dueAt` | datetime | |
| `endAt` | datetime | |
| `spentTime` | number | |
| `isOverTime` | boolean | |
| `customFields` | object[] | `[{ _id: string, value: any }]` |
| `members` | string or string[] | Empty string clears members |
| `assignees` | string or string[] | Empty string clears assignees |
| `swimlaneId` | string | Move to different swimlane (same board) |
| `listId` | string | Move to different list (same board) |
| `archive` | string | `"true"` to archive, `"false"` to unarchive. Only affects this card, not children. Does not set `archivedAt`. |
| `newBoardId` | string | Cross-board move (requires all three: `newBoardId`, `newSwimlaneId`, `newListId`) |
| `newSwimlaneId` | string | Cross-board move |
| `newListId` | string | Cross-board move |

> Note: For archiving with child cards and proper timestamps, use `POST .../cards/:cardId/archive` and `POST .../cards/:cardId/unarchive` instead.

---

## Checklist

No PUT endpoint. Checklists can only be created (`POST`) and deleted (`DELETE`). Title cannot be edited via REST.

---

## Checklist Item

### `PUT /api/boards/:boardId/cards/:cardId/checklists/:checklistId/items/:itemId`

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | |
| `isFinished` | boolean | |

---

## Comment

No PUT endpoint. Comments can only be created (`POST`) and deleted (`DELETE`). Text cannot be edited via REST.
