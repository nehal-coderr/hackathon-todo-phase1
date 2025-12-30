<!--
Sync Impact Report
==================
Version change: 1.0.0 → 2.0.0 (MAJOR - Phase I scope update)
Changed sections:
  - II. In-Memory Only → II. JSON File Storage (persistence now allowed)
  - III. Console Interface → III. Subcommand CLI Interface (menu loop → subcommands)
  - IV. Minimal Dependencies (updated Python version to 3.10+)
  - Technology Constraints (updated storage and interface)
  - Explicit Non-Goals (removed file persistence and argparse from non-goals)
Rationale: Clarification session determined JSON persistence and subcommand CLI are required for Phase I
Templates requiring updates:
  - plan-template.md: ✅ No changes required
  - spec-template.md: ✅ No changes required
  - tasks-template.md: ✅ No changes required
Follow-up TODOs: None
-->

# Hackathon II Phase I - Console Todo App Constitution

## Core Principles

### I. Simplicity First

All features MUST be implemented with the minimum viable code. No abstractions, patterns, or indirection unless absolutely required for correctness.

- Single-file implementation preferred when feasible
- No design patterns (factory, repository, etc.) unless solving a concrete problem
- Direct list operations over service layers
- Inline validation over separate validator classes

**Rationale**: Hackathon constraints demand speed; unnecessary abstraction slows development and obscures logic.

### II. JSON File Storage

All data MUST be persisted to a local JSON file for durability across sessions.

- Data structure: `[{"id": int, "title": str, "description": str, "due_date": str|null, "status": str, "created_at": str}]`
- ID generation MUST be sequential (max existing ID + 1, or 1 if empty)
- Storage file: `~/.todo/tasks.json` (user's home directory)
- File MUST be created on first write if it doesn't exist
- File MUST be human-readable (indented JSON)
- Support Unicode text including Urdu in title and description fields

**Rationale**: Clarification session determined persistence is required for Phase I; JSON provides human-readable storage with stdlib support.

### III. Subcommand CLI Interface

All user interaction MUST occur via subcommand-style CLI (e.g., `todo add`, `todo list`).

- Subcommands: `add`, `list`, `update`, `delete`, `complete`
- Use Python's `argparse` module from stdlib for argument parsing
- Output MUST include status indicators for task completion state
- Errors MUST be displayed to stderr with actionable guidance
- Each command executes once and exits (no interactive loop)
- CLI interface messages in English; task content supports Unicode (including Urdu)

**Rationale**: Subcommand CLI is the modern standard (git, docker); clarification session confirmed this approach.

### IV. Minimal Dependencies

The project MUST use only Python standard library. No external packages.

- Python 3.10+ as the minimum runtime (3.10, 3.11, 3.12, or 3.13 acceptable)
- UV as the project/package manager (for running, not for dependencies)
- No pytest, click, rich, or other third-party packages
- Testing via manual console interaction or built-in unittest if needed

**Rationale**: External dependencies add complexity and potential compatibility issues; standard library suffices for CRUD operations.

## Technology Constraints

**Language/Version**: Python 3.10+
**Package Manager**: UV (for project management only)
**External Dependencies**: None (stdlib only)
**Storage**: JSON file (`~/.todo/tasks.json`)
**Interface**: Subcommand CLI (argparse)
**Testing**: Manual or unittest (stdlib)
**Unicode**: Full support including Urdu in task content

## Explicit Non-Goals

The following are explicitly OUT OF SCOPE for Phase I:

- Database integration (SQLite, PostgreSQL, etc.)
- Web interface (Flask, FastAPI, Django)
- Authentication or user management
- AI/ML features
- Multi-user support
- Task categories, tags, or priorities
- Reminders or notifications
- Search or filtering beyond basic list view
- Cloud sync or network features

**Rationale**: Scope creep is the enemy of hackathon success. Phase I delivers basic CRUD with local JSON persistence.

## Governance

1. **Constitution Authority**: This constitution supersedes all other project documentation for Phase I scope decisions.

2. **Amendments**: Any change to this constitution MUST be documented with:
   - Rationale for the change
   - Impact assessment on existing code
   - Version increment (MAJOR for scope changes, MINOR for additions, PATCH for clarifications)

3. **Compliance**: All code contributions MUST:
   - Satisfy the four core principles
   - Not introduce out-of-scope features
   - Use only permitted technologies

4. **Violations**: If a principle must be violated, document the justification in code comments and flag for review.

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-31
