"""Unit tests for CLI Todo Application."""

import json
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import todo


class TestLoadTasks(unittest.TestCase):
    """Tests for load_tasks() function."""

    def test_load_tasks_missing_file(self):
        """Returns empty list when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(todo, 'TASKS_FILE', Path(tmpdir) / "tasks.json"):
                result = todo.load_tasks()
                self.assertEqual(result, [])

    def test_load_tasks_valid_json(self):
        """Returns tasks list when file contains valid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "Test", "status": "pending"}]
            tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                result = todo.load_tasks()
                self.assertEqual(result, tasks)

    def test_load_tasks_invalid_json(self):
        """Exits with error on invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks_file.write_text("not valid json", encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with self.assertRaises(SystemExit) as ctx:
                    todo.load_tasks()
                self.assertEqual(ctx.exception.code, 1)


class TestSaveTasks(unittest.TestCase):
    """Tests for save_tasks() function."""

    def test_save_tasks_creates_directory(self):
        """Creates parent directory if missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "subdir" / "tasks.json"
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                todo.save_tasks([{"id": 1, "title": "Test"}])
                self.assertTrue(tasks_file.exists())

    def test_save_tasks_writes_json(self):
        """Writes tasks as formatted JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "Test"}]
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                todo.save_tasks(tasks)
                content = tasks_file.read_text(encoding="utf-8")
                self.assertEqual(json.loads(content), tasks)

    def test_save_tasks_unicode(self):
        """Preserves Unicode characters (Urdu)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "کام مکمل کریں"}]
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                todo.save_tasks(tasks)
                content = tasks_file.read_text(encoding="utf-8")
                self.assertIn("کام مکمل کریں", content)


class TestGenerateId(unittest.TestCase):
    """Tests for generate_id() function."""

    def test_generate_id_empty_list(self):
        """Returns 1 for empty task list."""
        self.assertEqual(todo.generate_id([]), 1)

    def test_generate_id_with_tasks(self):
        """Returns max ID + 1."""
        tasks = [{"id": 1}, {"id": 5}, {"id": 3}]
        self.assertEqual(todo.generate_id(tasks), 6)


class TestValidateDate(unittest.TestCase):
    """Tests for validate_date() function."""

    def test_valid_date(self):
        """Returns True for valid YYYY-MM-DD format."""
        self.assertTrue(todo.validate_date("2025-01-15"))

    def test_invalid_date_format(self):
        """Returns False for invalid format."""
        self.assertFalse(todo.validate_date("01-15-2025"))
        self.assertFalse(todo.validate_date("invalid"))
        self.assertFalse(todo.validate_date("2025/01/15"))


class TestAddTask(unittest.TestCase):
    """Tests for add_task() function."""

    def test_add_task_basic(self):
        """Creates task with title and returns ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with patch('sys.stdout', new=StringIO()):
                    task_id = todo.add_task("Test Task")
                    self.assertEqual(task_id, 1)
                    tasks = json.loads(tasks_file.read_text())
                    self.assertEqual(len(tasks), 1)
                    self.assertEqual(tasks[0]["title"], "Test Task")

    def test_add_task_empty_title(self):
        """Exits with error on empty title."""
        with self.assertRaises(SystemExit) as ctx:
            todo.add_task("")
        self.assertEqual(ctx.exception.code, 1)

    def test_add_task_with_due_date(self):
        """Creates task with due date."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with patch('sys.stdout', new=StringIO()):
                    todo.add_task("Test", due_date="2025-01-15")
                    tasks = json.loads(tasks_file.read_text())
                    self.assertEqual(tasks[0]["due_date"], "2025-01-15")


class TestListTasks(unittest.TestCase):
    """Tests for list_tasks() function."""

    def test_list_tasks_empty(self):
        """Shows empty message when no tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(todo, 'TASKS_FILE', Path(tmpdir) / "tasks.json"):
                with patch('sys.stdout', new=StringIO()) as mock_out:
                    todo.list_tasks()
                    output = mock_out.getvalue()
                    self.assertIn("No tasks found", output)

    def test_list_tasks_with_tasks(self):
        """Shows tabular format with tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "Test", "status": "pending", "due_date": None}]
            tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with patch('sys.stdout', new=StringIO()) as mock_out:
                    todo.list_tasks()
                    output = mock_out.getvalue()
                    self.assertIn("ID", output)
                    self.assertIn("Test", output)
                    self.assertIn("[ ]", output)


class TestCompleteTask(unittest.TestCase):
    """Tests for complete_task() function."""

    def test_complete_task_success(self):
        """Marks task as completed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "Test", "status": "pending"}]
            tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with patch('sys.stdout', new=StringIO()):
                    todo.complete_task(1)
                    updated = json.loads(tasks_file.read_text())
                    self.assertEqual(updated[0]["status"], "completed")

    def test_complete_task_not_found(self):
        """Exits with error when task not found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks_file.write_text("[]", encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with self.assertRaises(SystemExit) as ctx:
                    todo.complete_task(999)
                self.assertEqual(ctx.exception.code, 1)


class TestUpdateTask(unittest.TestCase):
    """Tests for update_task() function."""

    def test_update_task_title(self):
        """Updates task title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "Old", "description": None, "due_date": None, "status": "pending"}]
            tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with patch('sys.stdout', new=StringIO()):
                    todo.update_task(1, title="New")
                    updated = json.loads(tasks_file.read_text())
                    self.assertEqual(updated[0]["title"], "New")

    def test_update_task_no_options(self):
        """Exits with error when no options provided."""
        with self.assertRaises(SystemExit) as ctx:
            todo.update_task(1)
        self.assertEqual(ctx.exception.code, 1)


class TestDeleteTask(unittest.TestCase):
    """Tests for delete_task() function."""

    def test_delete_task_success(self):
        """Removes task from list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks = [{"id": 1, "title": "Test", "status": "pending"}]
            tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with patch('sys.stdout', new=StringIO()):
                    todo.delete_task(1)
                    updated = json.loads(tasks_file.read_text())
                    self.assertEqual(len(updated), 0)

    def test_delete_task_not_found(self):
        """Exits with error when task not found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks_file = Path(tmpdir) / "tasks.json"
            tasks_file.write_text("[]", encoding="utf-8")
            with patch.object(todo, 'TASKS_FILE', tasks_file):
                with self.assertRaises(SystemExit) as ctx:
                    todo.delete_task(999)
                self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
