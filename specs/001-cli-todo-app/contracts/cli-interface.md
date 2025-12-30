# CLI Interface Contract: Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app

## Overview

This document defines the command-line interface contract for the todo application. All commands follow the subcommand pattern: `todo <command> [arguments] [options]`.

## Commands

### `todo add <title> [options]`

Add a new task to the list.

**Arguments**:
- `title` (required): Task title (1-200 characters)

**Options**:
- `-d, --description <text>`: Task description
- `--due <date>`: Due date in YYYY-MM-DD format

**Output** (stdout):
```
Task created with ID: <id>
```

**Errors** (stderr, exit code 1):
```
Error: Title is required
Error: Title must be 1-200 characters
Error: Invalid date format. Use YYYY-MM-DD
```

**Examples**:
```bash
todo add "Buy groceries"
todo add "Finish report" -d "Q4 financial summary"
todo add "Submit taxes" --due 2025-04-15
todo add "کام مکمل کریں" -d "اردو میں وضاحت"
```

---

### `todo list`

Display all tasks.

**Arguments**: None

**Options**: None

**Output** (stdout):
```
ID  Status      Title                Due Date
--  ------      -----                --------
1   [ ]         Buy groceries        2025-01-05
2   [x]         کام مکمل کریں         -
3   [ ]         Call mom             2025-01-01
```

When no tasks exist:
```
No tasks found. Use 'todo add <title>' to create one.
```

**Errors**: None expected

**Examples**:
```bash
todo list
```

---

### `todo complete <id>`

Mark a task as completed.

**Arguments**:
- `id` (required): Task ID (positive integer)

**Options**: None

**Output** (stdout):
```
Task <id> marked as completed.
```

If already completed:
```
Task <id> is already completed.
```

**Errors** (stderr, exit code 1):
```
Error: Task <id> not found
Error: Invalid task ID
```

**Examples**:
```bash
todo complete 1
todo complete 42
```

---

### `todo update <id> [options]`

Update an existing task's title, description, or due date.

**Arguments**:
- `id` (required): Task ID (positive integer)

**Options**:
- `-t, --title <text>`: New title
- `-d, --description <text>`: New description
- `--due <date>`: New due date in YYYY-MM-DD format

**Output** (stdout):
```
Task <id> updated.
```

**Errors** (stderr, exit code 1):
```
Error: Task <id> not found
Error: No update options provided. Use -t, -d, or --due
Error: Title must be 1-200 characters
Error: Invalid date format. Use YYYY-MM-DD
```

**Examples**:
```bash
todo update 1 -t "Buy organic groceries"
todo update 2 -d "Updated description"
todo update 3 --due 2025-02-01
todo update 1 -t "New title" -d "New description" --due 2025-03-15
```

---

### `todo delete <id>`

Delete a task permanently.

**Arguments**:
- `id` (required): Task ID (positive integer)

**Options**: None

**Output** (stdout):
```
Task <id> deleted.
```

**Errors** (stderr, exit code 1):
```
Error: Task <id> not found
Error: Invalid task ID
```

**Examples**:
```bash
todo delete 1
todo delete 42
```

---

### `todo --help` / `todo -h`

Display help information.

**Output**:
```
usage: todo [-h] {add,list,complete,update,delete} ...

CLI Todo Application

positional arguments:
  {add,list,complete,update,delete}
    add                 Add a new task
    list                List all tasks
    complete            Mark task as complete
    update              Update a task
    delete              Delete a task

options:
  -h, --help            show this help message and exit
```

---

### `todo <command> --help`

Display help for a specific command.

**Example**:
```bash
todo add --help
```

**Output**:
```
usage: todo add [-h] [-d DESCRIPTION] [--due DUE] title

positional arguments:
  title                 Task title

options:
  -h, --help            show this help message and exit
  -d DESCRIPTION, --description DESCRIPTION
                        Task description
  --due DUE             Due date (YYYY-MM-DD)
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, task not found, etc.) |
| 2 | Command line syntax error (argparse default) |

## Output Format

- Success messages: stdout
- Error messages: stderr (prefixed with "Error: ")
- List output: stdout, tabular format with headers
- All output uses UTF-8 encoding for Unicode support
