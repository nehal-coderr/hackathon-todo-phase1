---
id: 0001
title: CLI Todo App Specification
stage: spec
date: 2025-12-31
surface: agent
model: claude-opus-4-5-20251101
feature: 001-cli-todo-app
branch: 001-cli-todo-app
user: developer
command: /sp.specify
labels: ["specification", "cli", "todo-app", "python"]
links:
  spec: specs/001-cli-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-todo-app/spec.md
  - specs/001-cli-todo-app/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

sp.specify feature "Add Task" --description "User can add a task with title, optional description, and due date" --input "title, description, due_date" --output "task_id" --language "Python CLI"
sp.specify feature "View Tasks" --description "List all tasks with status and IDs" --output "list of tasks"
sp.specify feature "Update Task" --description "Update title, description, or due date of an existing task" --input "task_id, new_title, new_description, new_due_date"
sp.specify feature "Delete Task" --description "Remove a task by ID" --input "task_id"
sp.specify feature "Mark Complete" --description "Mark task as completed" --input "task_id"

## Response snapshot

Created comprehensive specification for CLI Todo Application with 5 user stories (Add Task, View Tasks, Mark Complete, Update Task, Delete Task) prioritized P1-P3. Defined 11 functional requirements covering CRUD operations, persistence, and error handling. Established 6 measurable success criteria. Documented edge cases and assumptions for Phase I scope (single-user, local storage, English only).

## Outcome

- Impact: Created complete feature specification ready for planning phase
- Tests: N/A (specification phase)
- Files: spec.md, checklists/requirements.md
- Next prompts: /sp.clarify or /sp.plan
- Reflection: Spec covers all 5 requested features with testable acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Quality checklist PASS (all items checked)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
