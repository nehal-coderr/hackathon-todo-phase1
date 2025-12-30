# Implementation Plan: CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Build a command-line todo application in Python 3.10+ using only stdlib. Features include add, list, update, delete, and complete operations with JSON file persistence at `~/.todo/tasks.json`. Supports Unicode text including Urdu in task content. Uses argparse for subcommand-style CLI interface.

## Technical Context

**Language/Version**: Python 3.10+ (stdlib only)
**Primary Dependencies**: None (stdlib: argparse, json, pathlib, datetime)
**Storage**: JSON file at `~/.todo/tasks.json`
**Testing**: unittest (stdlib) or manual testing
**Target Platform**: Cross-platform (Linux, macOS, Windows with Python)
**Project Type**: Single project (single-file implementation)
**Performance Goals**: <5s for any operation, <2s for list (up to 100 tasks)
**Constraints**: No external dependencies, stdlib only
**Scale/Scope**: Single user, up to 10,000 tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Simplicity First | PASS | Single-file implementation, no patterns |
| II. JSON File Storage | PASS | Using `~/.todo/tasks.json` per constitution v2.0.0 |
| III. Subcommand CLI Interface | PASS | Using argparse subcommands per constitution v2.0.0 |
| IV. Minimal Dependencies | PASS | stdlib only (argparse, json, pathlib, datetime) |

**Constitution Version**: 2.0.0 (amended 2025-12-31)

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── plan.md              # This file
├── research.md          # Technical decisions
├── data-model.md        # Task entity definition
├── quickstart.md        # Usage guide
├── contracts/           # CLI interface contract
│   └── cli-interface.md
├── checklists/          # Quality checklists
│   └── requirements.md
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
todo.py                  # Main application (single file)
tests/
└── test_todo.py         # Unit tests (optional)
```

**Structure Decision**: Single-file implementation per Constitution Principle I (Simplicity First). The entire application fits in one file (~200-300 lines) with no need for modules or packages.

## Implementation Approach

### Phase 1: Core Storage Layer

1. Define `TASKS_FILE` path (`~/.todo/tasks.json`)
2. Implement `load_tasks()` - read JSON, return list, handle missing file
3. Implement `save_tasks()` - write JSON with proper formatting and Unicode

### Phase 2: CRUD Operations

1. `add_task(title, description, due_date)` - validate, generate ID, append, save
2. `list_tasks()` - load and display in tabular format
3. `update_task(id, title, description, due_date)` - find, update, save
4. `delete_task(id)` - find, remove, save
5. `complete_task(id)` - find, set status, save

### Phase 3: CLI Interface

1. Set up argparse with subcommands
2. Wire each subcommand to its operation
3. Handle errors with proper exit codes
4. Add help text for all commands

### Phase 4: Testing & Validation

1. Manual testing of all commands
2. Test Unicode/Urdu support
3. Test error cases
4. Optional: unittest coverage

## Complexity Tracking

No constitution violations. Single-file implementation follows all four core principles.

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| File permission errors | Medium | Graceful error message with path |
| Concurrent writes | Low | Document single-user design; not handled in Phase I |
| Large task lists | Low | Test with 100+ tasks; warn if performance degrades |
| Terminal Unicode support | Low | User responsibility; document in quickstart |

## Next Steps

Run `/sp.tasks` to generate implementation task list.
