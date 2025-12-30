# Research: CLI Todo Application

**Feature**: 001-cli-todo-app
**Date**: 2025-12-31
**Status**: Complete

## Research Summary

All technical decisions have been resolved through the specification clarification process and constitution amendment (v1.0.0 → v2.0.0). Implementation uses Python standard library only.

## Technical Decisions

### 1. Storage Format

**Decision**: JSON file at `~/.todo/tasks.json`

**Rationale**:
- Human-readable format for debugging and manual inspection
- Python `json` module is in stdlib (no external dependencies)
- Supports Unicode natively (required for Urdu text)
- Simple read/write operations with `json.load()` / `json.dump()`

**Alternatives Considered**:
- SQLite: Rejected - overkill for simple CRUD, adds complexity
- CSV: Rejected - poor support for nested data, escaping issues with commas in text
- Pickle: Rejected - not human-readable, security concerns with untrusted data
- In-memory only: Rejected - clarification session determined persistence required

### 2. CLI Framework

**Decision**: Python `argparse` module with subcommand pattern

**Rationale**:
- Part of Python stdlib (no external dependencies)
- Built-in support for subcommands via `add_subparsers()`
- Automatic help generation
- Type validation for arguments

**Alternatives Considered**:
- Click: Rejected - external dependency violates constitution
- Typer: Rejected - external dependency violates constitution
- Manual sys.argv parsing: Rejected - reinventing the wheel, error-prone
- Menu loop with input(): Rejected - clarification session chose subcommand style

### 3. Python Version

**Decision**: Python 3.10+ minimum

**Rationale**:
- Match expressions available (3.10+) for cleaner command dispatch
- Improved error messages in 3.10+
- Union type syntax `X | Y` available (3.10+)
- Wide adoption - most modern systems have 3.10+

**Alternatives Considered**:
- Python 3.8: Rejected - missing modern features, approaching EOL
- Python 3.12/3.13 only: Rejected - unnecessarily limits compatibility

### 4. Data Structure

**Decision**: List of dictionaries with extended fields

**Rationale**:
- Constitution v2.0.0 structure: `[{"id": int, "title": str, "description": str, "due_date": str|null, "status": str, "created_at": str}]`
- Native Python data type, no imports needed beyond json
- Direct index/filter operations for CRUD
- Status as string ("pending"/"completed") for readability

**Alternatives Considered**:
- `dataclass`: Adds complexity, requires custom JSON encoder
- `namedtuple`: Immutable, makes updates awkward
- Custom class: Violates Simplicity First principle

### 5. Unicode/Urdu Support

**Decision**: Native Python string handling with UTF-8 encoding

**Rationale**:
- Python 3 strings are Unicode by default
- JSON module handles UTF-8 encoding automatically with `ensure_ascii=False`
- No special libraries needed for Urdu text
- Terminal must support UTF-8 (user responsibility)

**Alternatives Considered**:
- Explicit encoding handling: Rejected - Python 3 handles this automatically
- Arabic/Urdu text shaping libraries: Rejected - external dependency, console display is terminal's responsibility

### 6. Project Structure

**Decision**: Single-file implementation with separate test file

**Rationale**:
- Constitution mandates "single-file implementation preferred when feasible"
- CLI todo app is simple enough for single file (~200-300 lines)
- Easier to understand and maintain
- Reduces import complexity

**Alternatives Considered**:
- Multi-module structure (models/, services/, cli/): Rejected - over-engineering for this scope
- Package structure with __init__.py: Rejected - unnecessary for single-file app

### 7. ID Generation

**Decision**: Sequential ID = `max(task["id"] for task in tasks) + 1` or `1` if empty

**Rationale**:
- Simple, predictable numbering
- Persists correctly in JSON
- User-friendly for command-line reference (`todo complete 3`)

**Alternatives Considered**:
- UUID: Overkill, hard to type on command line
- Timestamp-based: Unnecessary complexity
- Random: Potential collisions, harder to reference

### 8. Error Handling

**Decision**: Print to stderr with exit codes

**Rationale**:
- Errors to stderr, success to stdout (Unix convention)
- Non-zero exit code for errors (scriptability)
- Clear, actionable error messages

**Alternatives Considered**:
- Exceptions without messages: Poor UX
- Logging module: Overkill for simple CLI
- Custom exception classes: Violates Simplicity First

## Implementation Patterns

### JSON File Handling

```python
from pathlib import Path
import json

TASKS_FILE = Path.home() / ".todo" / "tasks.json"

def load_tasks() -> list[dict]:
    if not TASKS_FILE.exists():
        return []
    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))

def save_tasks(tasks: list[dict]) -> None:
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASKS_FILE.write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
```

### Argparse Subcommand Pattern

```python
import argparse

parser = argparse.ArgumentParser(prog="todo", description="CLI Todo Application")
subparsers = parser.add_subparsers(dest="command", required=True)

# Add command
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("title", help="Task title")
add_parser.add_argument("-d", "--description", help="Task description")
add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")

# List command
list_parser = subparsers.add_parser("list", help="List all tasks")

# Complete command
complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
complete_parser.add_argument("id", type=int, help="Task ID")

# Update command
update_parser = subparsers.add_parser("update", help="Update a task")
update_parser.add_argument("id", type=int, help="Task ID")
update_parser.add_argument("-t", "--title", help="New title")
update_parser.add_argument("-d", "--description", help="New description")
update_parser.add_argument("--due", help="New due date (YYYY-MM-DD)")

# Delete command
delete_parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("id", type=int, help="Task ID")
```

## Open Questions

None - all technical decisions resolved.

## References

- Python 3.10+ Documentation: https://docs.python.org/3/
- Python Match Statement: https://docs.python.org/3/reference/compound_stmts.html#match
- Python Unicode HOWTO: https://docs.python.org/3/howto/unicode.html
- argparse Documentation: https://docs.python.org/3/library/argparse.html
- json Documentation: https://docs.python.org/3/library/json.html
