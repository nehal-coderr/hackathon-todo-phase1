# Quickstart: CLI Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app

## Prerequisites

- Python 3.10+ installed
- UV package manager installed (for running the project)
- Terminal with UTF-8/Unicode support (for Urdu text)

## Setup

```bash
# Clone/navigate to project
cd hackathon-todo

# Initialize UV project (if not already done)
uv init

# No dependencies to install - stdlib only!
```

## Running the Application

```bash
# Using UV
uv run python todo.py <command> [args]

# Or directly with Python
python todo.py <command> [args]

# Or install as a script and use
todo <command> [args]
```

## Usage

### Adding Tasks

```bash
# Add a simple task
todo add "Buy groceries"
# Output: Task created with ID: 1

# Add task with description
todo add "Finish report" -d "Q4 financial summary"
# Output: Task created with ID: 2

# Add task with due date
todo add "Submit taxes" --due 2025-04-15
# Output: Task created with ID: 3

# Add task with all options
todo add "Complete project" -d "Final deliverables" --due 2025-01-31
# Output: Task created with ID: 4

# Add task in Urdu
todo add "کام مکمل کریں" -d "اردو میں وضاحت"
# Output: Task created with ID: 5
```

### Viewing Tasks

```bash
todo list

# Output:
# ID  Status      Title                Due Date
# --  ------      -----                --------
# 1   [ ]         Buy groceries        -
# 2   [ ]         Finish report        -
# 3   [ ]         Submit taxes         2025-04-15
# 4   [ ]         Complete project     2025-01-31
# 5   [ ]         کام مکمل کریں         -

# When no tasks exist:
# No tasks found. Use 'todo add <title>' to create one.
```

### Marking Tasks Complete

```bash
todo complete 1
# Output: Task 1 marked as completed.

todo list
# Output:
# ID  Status      Title                Due Date
# --  ------      -----                --------
# 1   [x]         Buy groceries        -
# 2   [ ]         Finish report        -
# ...
```

### Updating Tasks

```bash
# Update title
todo update 1 -t "Buy organic groceries"
# Output: Task 1 updated.

# Update description
todo update 2 -d "Updated description"
# Output: Task 2 updated.

# Update due date
todo update 3 --due 2025-05-01
# Output: Task 3 updated.

# Update multiple fields
todo update 4 -t "New title" -d "New description" --due 2025-02-15
# Output: Task 4 updated.
```

### Deleting Tasks

```bash
todo delete 5
# Output: Task 5 deleted.
```

### Getting Help

```bash
# General help
todo --help

# Command-specific help
todo add --help
todo update --help
```

## Error Handling Examples

### Task Not Found

```bash
todo complete 999
# Error: Task 999 not found
```

### Invalid Task ID

```bash
todo complete abc
# Error: Invalid task ID
```

### Empty Title

```bash
todo add ""
# Error: Title is required
```

### Invalid Date Format

```bash
todo add "Task" --due "tomorrow"
# Error: Invalid date format. Use YYYY-MM-DD
```

### No Update Options

```bash
todo update 1
# Error: No update options provided. Use -t, -d, or --due
```

## Data Storage

- Tasks are stored in `~/.todo/tasks.json`
- File is created automatically on first use
- Human-readable JSON format
- Supports Unicode text (including Urdu)

### Example JSON Structure

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": null,
    "due_date": null,
    "status": "completed",
    "created_at": "2025-12-31T10:30:00"
  }
]
```

## Testing

```bash
# Run unittest tests (if implemented)
uv run python -m unittest tests/test_todo.py

# Or directly
python -m unittest tests/test_todo.py
```

## Notes

- Data persists between sessions (stored in JSON file)
- All commands are atomic (success or error, no partial updates)
- Unicode/Urdu text works natively in Python 3.10+
- CLI interface is in English; task content supports any Unicode text
