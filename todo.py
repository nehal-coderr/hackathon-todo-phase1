#!/usr/bin/env python3
"""
CLI Todo Application

A command-line todo application with JSON file persistence.
Supports Unicode text including Urdu in task content.

Usage:
    todo add <title> [-d <description>] [--due <YYYY-MM-DD>]
    todo list
    todo complete <id>
    todo update <id> [-t <title>] [-d <description>] [--due <YYYY-MM-DD>]
    todo delete <id>

Examples:
    todo add "Buy groceries"
    todo add "Finish report" -d "Q4 financial summary" --due 2025-01-15
    todo add "کام مکمل کریں" -d "اردو میں وضاحت"
    todo list
    todo complete 1
    todo update 1 -t "Buy organic groceries"
    todo delete 2

Storage:
    Tasks are stored in ~/.todo/tasks.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Storage location
TASKS_FILE = Path.home() / ".todo" / "tasks.json"


def load_tasks() -> list[dict]:
    """Load tasks from JSON file. Returns empty list if file doesn't exist."""
    if not TASKS_FILE.exists():
        return []
    try:
        content = TASKS_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {TASKS_FILE}. Please fix or delete the file.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading {TASKS_FILE}", file=sys.stderr)
        sys.exit(1)


def save_tasks(tasks: list[dict]) -> None:
    """Save tasks to JSON file. Creates directory if missing."""
    try:
        TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
        TASKS_FILE.write_text(
            json.dumps(tasks, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except PermissionError:
        print(f"Error: Permission denied writing to {TASKS_FILE}", file=sys.stderr)
        sys.exit(1)


def generate_id(tasks: list[dict]) -> int:
    """Generate next sequential task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def validate_date(date_str: str) -> bool:
    """Validate date format is YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_task(title: str, description: str | None = None, due_date: str | None = None) -> int:
    """Add a new task. Returns the task ID."""
    # Validate title
    if not title or not title.strip():
        print("Error: Title is required", file=sys.stderr)
        sys.exit(1)

    title = title.strip()
    if len(title) > 200:
        print("Error: Title must be 1-200 characters", file=sys.stderr)
        sys.exit(1)

    # Validate due date if provided
    if due_date and not validate_date(due_date):
        print("Error: Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    # Load existing tasks and generate ID
    tasks = load_tasks()
    task_id = generate_id(tasks)

    # Create task
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds")
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task created with ID: {task_id}")
    return task_id


def find_task_by_id(tasks: list[dict], task_id: int) -> dict | None:
    """Find a task by ID. Returns task dict or None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def list_tasks() -> None:
    """Display all tasks in tabular format."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks found. Use 'todo add <title>' to create one.")
        return

    # Print header
    print(f"{'ID':<4} {'Status':<8} {'Title':<40} {'Due Date':<12}")
    print(f"{'--':<4} {'------':<8} {'-----':<40} {'--------':<12}")

    # Print each task
    for task in tasks:
        status = "[x]" if task["status"] == "completed" else "[ ]"
        title = task["title"][:37] + "..." if len(task["title"]) > 40 else task["title"]
        due_date = task.get("due_date") or "-"
        print(f"{task['id']:<4} {status:<8} {title:<40} {due_date:<12}")


def complete_task(task_id: int) -> None:
    """Mark a task as completed."""
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    if task["status"] == "completed":
        print(f"Task {task_id} is already completed.")
        return

    task["status"] = "completed"
    save_tasks(tasks)
    print(f"Task {task_id} marked as completed.")


def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    due_date: str | None = None
) -> None:
    """Update a task's title, description, or due date."""
    # Check at least one update option is provided
    if title is None and description is None and due_date is None:
        print("Error: No update options provided. Use -t, -d, or --due", file=sys.stderr)
        sys.exit(1)

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    # Validate and update title if provided
    if title is not None:
        title = title.strip()
        if not title:
            print("Error: Title cannot be empty", file=sys.stderr)
            sys.exit(1)
        if len(title) > 200:
            print("Error: Title must be 1-200 characters", file=sys.stderr)
            sys.exit(1)
        task["title"] = title

    # Update description if provided
    if description is not None:
        task["description"] = description

    # Validate and update due date if provided
    if due_date is not None:
        if not validate_date(due_date):
            print("Error: Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        task["due_date"] = due_date

    save_tasks(tasks)
    print(f"Task {task_id} updated.")


def delete_task(task_id: int) -> None:
    """Delete a task by ID."""
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="CLI Todo Application"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")

    # List command
    subparsers.add_parser("list", help="List all tasks")

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

    return parser


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    match args.command:
        case "add":
            add_task(args.title, args.description, args.due)
        case "list":
            list_tasks()
        case "complete":
            complete_task(args.id)
        case "update":
            update_task(args.id, args.title, args.description, args.due)
        case "delete":
            delete_task(args.id)


if __name__ == "__main__":
    main()
