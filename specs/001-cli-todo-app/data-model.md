# Data Model: CLI Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app
**Storage**: JSON file at `~/.todo/tasks.json`

## Entity: Task

The sole entity in this application. Stored in a JSON file as a list of objects.

### Structure

```python
# JSON file structure:
[
    {
        "id": int,           # Unique identifier (sequential, starting at 1)
        "title": str,        # Task title (required, 1-200 characters)
        "description": str,  # Task description (optional, can be empty/null)
        "due_date": str,     # Due date in YYYY-MM-DD format (optional, can be null)
        "status": str,       # "pending" or "completed"
        "created_at": str    # ISO 8601 timestamp when task was created
    }
]
```

### Field Definitions

| Field | Type | Required | Default | Validation | Description |
|-------|------|----------|---------|------------|-------------|
| `id` | `int` | Yes | Auto-generated | Positive integer, unique | Sequential identifier |
| `title` | `str` | Yes | N/A | 1-200 characters, non-empty | Task name/title |
| `description` | `str` | No | `null` | Any string or null | Task description |
| `due_date` | `str` | No | `null` | YYYY-MM-DD format or null | Due date |
| `status` | `str` | Yes | `"pending"` | "pending" or "completed" | Task status |
| `created_at` | `str` | Yes | Auto-generated | ISO 8601 format | Creation timestamp |

### ID Generation Rules

1. If task list is empty: new ID = 1
2. Otherwise: new ID = `max(task["id"] for task in tasks) + 1`
3. IDs are never reused (even after deletion)
4. IDs persist across application restarts

### State Transitions

```
┌─────────────┐     complete(id)         ┌─────────────┐
│   Pending   │ ─────────────────────────► │  Completed  │
│  status=    │                            │  status=    │
│  "pending"  │                            │ "completed" │
└─────────────┘                            └─────────────┘
```

Note: Phase I does not support reverting a completed task to pending.

### Operations

| Operation | Input | Output | Side Effect |
|-----------|-------|--------|-------------|
| **Add** | title, description?, due_date? | task dict with ID | Append to file |
| **List** | - | list of all tasks | None |
| **Update** | id, title?, description?, due_date? | updated task or error | Modify in file |
| **Delete** | id | success message or error | Remove from file |
| **Complete** | id | updated task or error | Set status="completed" |

### Example Data

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "due_date": "2025-01-05",
    "status": "pending",
    "created_at": "2025-12-31T10:30:00"
  },
  {
    "id": 2,
    "title": "کام مکمل کریں",
    "description": "اردو میں وضاحت",
    "due_date": null,
    "status": "completed",
    "created_at": "2025-12-31T11:00:00"
  },
  {
    "id": 3,
    "title": "Call mom",
    "description": null,
    "due_date": "2025-01-01",
    "status": "pending",
    "created_at": "2025-12-31T11:30:00"
  }
]
```

### Unicode Support

- `title` and `description` fields accept any Unicode string
- Urdu, Arabic, and other RTL scripts supported natively
- JSON file uses `ensure_ascii=False` for proper Unicode storage
- Display rendering depends on terminal capabilities

## Storage Details

### File Location

- Path: `~/.todo/tasks.json` (user's home directory)
- Directory created automatically on first write
- File created automatically on first write

### File Format

- Indented JSON (2 spaces) for human readability
- UTF-8 encoding for Unicode support
- Array of task objects at root level

### Error Handling

| Scenario | Behavior |
|----------|----------|
| File doesn't exist | Return empty list, create on first write |
| Directory doesn't exist | Create directory on first write |
| Invalid JSON | Display error, suggest manual fix or delete |
| Permission denied | Display error with path |

## No Relationships

This is a single-entity model. No foreign keys, no joins, no relationships.
