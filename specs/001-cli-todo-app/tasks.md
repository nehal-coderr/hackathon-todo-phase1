# Tasks: CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md

**Tests**: Included per user request ("Test Phase I")

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single-file implementation**: `todo.py` at repository root
- **Tests**: `tests/test_todo.py`

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Create `todo.py` file with module docstring and imports (argparse, json, pathlib, datetime, sys)
- [x] T002 Define `TASKS_FILE` constant as `Path.home() / ".todo" / "tasks.json"`
- [x] T003 [P] Create `tests/` directory and empty `tests/test_todo.py` file

---

## Phase 2: Foundational (Storage Layer)

**Purpose**: Core storage infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement `load_tasks()` function in `todo.py` - read JSON file, return list, handle missing file with empty list
- [x] T005 Implement `save_tasks(tasks)` function in `todo.py` - create directory if missing, write JSON with indent=2 and ensure_ascii=False
- [x] T006 Implement `generate_id(tasks)` function in `todo.py` - return max(id)+1 or 1 if empty
- [x] T007 [P] Add error handling for file permission errors and invalid JSON in `todo.py`

**Checkpoint**: Storage layer ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1)

**Goal**: Allow users to add tasks with title, optional description, and optional due date. Supports Unicode (including Urdu) in task content.

**Independent Test**: Run `todo add "Test Task"` and verify task is created with unique ID and persisted to JSON file.

### Implementation for User Story 1

- [x] T008 [US1] Implement `add_task(title, description, due_date)` function in `todo.py` - validate title (1-200 chars), validate date format if provided, generate ID, create task dict, append to list, save
- [x] T009 [US1] Implement `validate_date(date_str)` helper in `todo.py` - check YYYY-MM-DD format, return bool
- [x] T010 [US1] Add `add` subcommand to argparse in `todo.py` - positional title, optional -d/--description, optional --due
- [x] T011 [US1] Wire `add` subcommand handler to `add_task()` function in `todo.py`
- [x] T012 [US1] Output success message "Task created with ID: {id}" to stdout in `todo.py`
- [x] T013 [US1] Output error messages to stderr with exit code 1 for validation failures in `todo.py`

**Checkpoint**: User Story 1 complete - `todo add` works with English and Urdu titles

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks in a tabular format showing ID, status, title, and due date. Supports Unicode display.

**Independent Test**: Add sample tasks, run `todo list`, verify all tasks appear with correct formatting.

### Implementation for User Story 2

- [x] T014 [US2] Implement `list_tasks()` function in `todo.py` - load tasks, format as table with columns (ID, Status, Title, Due Date)
- [x] T015 [US2] Implement status display as `[ ]` for pending and `[x]` for completed in `todo.py`
- [x] T016 [US2] Handle empty task list with message "No tasks found. Use 'todo add <title>' to create one." in `todo.py`
- [x] T017 [US2] Add `list` subcommand to argparse in `todo.py` - no arguments required
- [x] T018 [US2] Wire `list` subcommand handler to `list_tasks()` function in `todo.py`

**Checkpoint**: User Story 2 complete - `todo list` displays tasks with Unicode support

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P2)

**Goal**: Mark a task as completed by ID, updating its status from "pending" to "completed".

**Independent Test**: Add a task, run `todo complete {id}`, verify status changes to completed in list view.

### Implementation for User Story 3

- [x] T019 [US3] Implement `complete_task(task_id)` function in `todo.py` - find task by ID, check if already completed, update status, save
- [x] T020 [US3] Implement `find_task_by_id(tasks, task_id)` helper in `todo.py` - return task dict or None
- [x] T021 [US3] Add `complete` subcommand to argparse in `todo.py` - positional id (int)
- [x] T022 [US3] Wire `complete` subcommand handler to `complete_task()` function in `todo.py`
- [x] T023 [US3] Output "Task {id} marked as completed." or "Task {id} is already completed." to stdout in `todo.py`
- [x] T024 [US3] Output "Error: Task {id} not found" to stderr with exit code 1 in `todo.py`

**Checkpoint**: User Story 3 complete - `todo complete {id}` works correctly

---

## Phase 6: User Story 4 - Update an Existing Task (Priority: P2)

**Goal**: Update a task's title, description, or due date by ID. Supports partial updates.

**Independent Test**: Add a task, run `todo update {id} -t "New Title"`, verify title changes in list view.

### Implementation for User Story 4

- [x] T025 [US4] Implement `update_task(task_id, title, description, due_date)` function in `todo.py` - find task, update provided fields only, validate, save
- [x] T026 [US4] Add `update` subcommand to argparse in `todo.py` - positional id (int), optional -t/--title, optional -d/--description, optional --due
- [x] T027 [US4] Validate at least one update option is provided in `todo.py`
- [x] T028 [US4] Wire `update` subcommand handler to `update_task()` function in `todo.py`
- [x] T029 [US4] Output "Task {id} updated." to stdout or appropriate error to stderr in `todo.py`

**Checkpoint**: User Story 4 complete - `todo update {id}` works with partial updates

---

## Phase 7: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Delete a task permanently by ID.

**Independent Test**: Add a task, run `todo delete {id}`, verify task no longer appears in list view.

### Implementation for User Story 5

- [x] T030 [US5] Implement `delete_task(task_id)` function in `todo.py` - find task, remove from list, save
- [x] T031 [US5] Add `delete` subcommand to argparse in `todo.py` - positional id (int)
- [x] T032 [US5] Wire `delete` subcommand handler to `delete_task()` function in `todo.py`
- [x] T033 [US5] Output "Task {id} deleted." to stdout or "Error: Task {id} not found" to stderr in `todo.py`

**Checkpoint**: User Story 5 complete - `todo delete {id}` removes tasks

---

## Phase 8: CLI Entry Point & Help

**Purpose**: Complete the CLI interface with main() and help system

- [x] T034 Implement `main()` function in `todo.py` - parse args, dispatch to handlers based on command
- [x] T035 Add `if __name__ == "__main__": main()` block in `todo.py`
- [x] T036 Verify `todo --help` and `todo {command} --help` work correctly in `todo.py`
- [x] T037 Ensure all error messages print to stderr and success messages to stdout in `todo.py`

**Checkpoint**: CLI entry point complete - application is runnable

---

## Phase 9: Testing & Validation

**Purpose**: Verify all features work correctly with English and Urdu tasks

### Manual Testing

- [x] T038 Test `todo add "Buy groceries"` - verify ID returned and task persisted
- [x] T039 Test `todo add "کام مکمل کریں" -d "اردو میں وضاحت"` - verify Urdu text stored and displayed correctly
- [x] T040 Test `todo add "Task with date" --due 2025-01-15` - verify due date stored
- [x] T041 Test `todo add ""` - verify error message for empty title
- [x] T042 Test `todo add "Task" --due "invalid"` - verify error for invalid date format
- [x] T043 Test `todo list` with tasks - verify tabular format with columns
- [x] T044 Test `todo list` with no tasks - verify empty message
- [x] T045 Test `todo complete 1` - verify status changes
- [x] T046 Test `todo complete 999` - verify error for non-existent task
- [x] T047 Test `todo update 1 -t "New Title"` - verify title updates
- [x] T048 Test `todo update 1` (no options) - verify error message
- [x] T049 Test `todo delete 1` - verify task removed
- [x] T050 Test persistence - add task, exit, run list - verify task persists

### Unit Tests (Optional)

- [x] T051 [P] Write unit test for `load_tasks()` in `tests/test_todo.py`
- [x] T052 [P] Write unit test for `save_tasks()` in `tests/test_todo.py`
- [x] T053 [P] Write unit test for `generate_id()` in `tests/test_todo.py`
- [x] T054 [P] Write unit test for `validate_date()` in `tests/test_todo.py`
- [x] T055 [P] Write unit test for `add_task()` in `tests/test_todo.py`
- [x] T056 [P] Write unit test for `list_tasks()` output format in `tests/test_todo.py`
- [x] T057 [P] Write unit test for `complete_task()` in `tests/test_todo.py`
- [x] T058 [P] Write unit test for `update_task()` in `tests/test_todo.py`
- [x] T059 [P] Write unit test for `delete_task()` in `tests/test_todo.py`
- [x] T060 Run all unit tests with `python -m unittest tests/test_todo.py`

---

## Phase 10: Polish & Documentation

**Purpose**: Final cleanup and documentation

- [x] T061 Add module docstring to `todo.py` with usage examples
- [x] T062 Verify all functions have docstrings in `todo.py`
- [x] T063 [P] Update quickstart.md with actual command examples if needed
- [x] T064 Run through quickstart.md validation manually
- [x] T065 Verify JSON file is human-readable with proper formatting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - US1 (Add) and US2 (List) are both P1 - can start in parallel after Phase 2
  - US3 (Complete), US4 (Update), US5 (Delete) can start after Phase 2
  - All depend on `find_task_by_id()` from US3 T020 - implement first
- **CLI Entry Point (Phase 8)**: Depends on all user stories
- **Testing (Phase 9)**: Depends on CLI Entry Point
- **Polish (Phase 10)**: Depends on Testing

### User Story Dependencies

- **User Story 1 (Add)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (List)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 3 (Complete)**: Depends on T020 `find_task_by_id()` - implement this first
- **User Story 4 (Update)**: Uses `find_task_by_id()` from US3 - can start after T020
- **User Story 5 (Delete)**: Uses `find_task_by_id()` from US3 - can start after T020

### Parallel Opportunities

Since this is a single-file implementation, most tasks are sequential within `todo.py`. However:

- T003 (create tests dir) can run parallel to T001-T002
- T007 (error handling) can run parallel to T004-T006
- All unit tests (T051-T059) can be written in parallel
- T063 (update docs) can run parallel to T061-T062

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test add and list work with Urdu text
6. Deploy/demo if ready - users can add and view tasks

### Incremental Delivery

1. Complete Setup + Foundational → Storage layer ready
2. Add US1 (Add) + US2 (List) → Test independently → Demo (MVP!)
3. Add US3 (Complete) → Test independently → Demo
4. Add US4 (Update) → Test independently → Demo
5. Add US5 (Delete) → Test independently → Demo
6. Each story adds value without breaking previous stories

---

## Notes

- Single-file implementation: all code in `todo.py`
- [P] tasks = different files or independent within same file
- [US#] label maps task to specific user story
- Verify Urdu text works in both input and output
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
- Constitution v2.0.0: JSON storage, argparse CLI, Python 3.10+
