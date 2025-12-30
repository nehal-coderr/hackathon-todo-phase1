---
id: 001
title: Hackathon Todo App Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "hackathon", "todo-app", "phase-1"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

# Hackathon II Phase I - Console Todo App
## Scope: Basic Level CRUD ONLY
- Add Task (title + description)
- View Tasks (status indicators)
- Update Task (title/desc)
- Delete Task (by ID)
- Mark Complete/Incomplete
## Tech: Python 3.13, UV, in-memory list
## NO: DB, files, web, auth, AI
## Data: tasks = [{"id":1, "title":"", "desc":"", "completed":False}]

## Response snapshot

Created constitution v1.0.0 for Hackathon II Phase I Console Todo App with 4 core principles:

1. **Simplicity First** - Minimum viable code, no unnecessary abstractions
2. **In-Memory Only** - Data stored in Python list, no persistence
3. **Console Interface** - stdin/stdout menu-driven interaction
4. **Minimal Dependencies** - Python stdlib only, no external packages

Added Technology Constraints section defining Python 3.13, UV, and stdlib-only requirements.

Added Explicit Non-Goals section listing database, file persistence, web interface, auth, AI, and other out-of-scope features.

Governance section establishes constitution authority, amendment process, and compliance requirements.

## Outcome

- Impact: Established foundational governance document for Phase I development
- Tests: N/A (constitution document)
- Files: .specify/memory/constitution.md created
- Next prompts: /sp.specify to create feature spec, /sp.plan for implementation planning
- Reflection: Constitution scoped appropriately for hackathon constraints with clear non-goals

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
