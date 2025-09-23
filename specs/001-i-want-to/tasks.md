# Tasks: Rebrand to Expert In My Pocket

**Input**: Design documents from `/Users/timbo/Dev/expert-in-my-pocket/specs/001-i-want-to/`
**Prerequisites**: plan.md (required), research.md, data-model.md, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `app/`, `nextjs/`
- Paths shown below assume web app structure.

## Phase 3.1: Setup
- [X] T001 [P] Create a new test file `nextjs/src/app/rebranding.test.tsx` to check for the presence of "T-Levet Assistant" in the UI.
- [X] T002 [P] Create a new test file `app/rebranding_test.py` to check for the presence of "T-Levet" in the backend code.

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T003 Run the tests and confirm they fail.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [X] T004 [P] Replace all instances of "T-Levet Assistant" with "Expert In My Pocket" in the `nextjs` directory.
- [X] T005 [P] Replace all instances of "T-Levet" with "Expert In My Pocket" in the `app` directory.
- [X] T006 [P] Replace all instances of "T-Levet" with "Expert In My Pocket" in the root directory files (e.g., `GEMINI.md`, `README.md`).

## Phase 3.4: Integration
- [X] T007 Run the tests and confirm they pass.

## Phase 3.5: Polish
- [X] T008 [P] Delete the test file `nextjs/src/app/rebranding.test.tsx`.
- [X] T009 [P] Delete the test file `app/rebranding_test.py`.
- [X] T010 Manually verify the rebranding by running the application and checking the UI.

## Dependencies
- Tests (T001-T002) before implementation (T004-T006)
- Implementation before integration (T007)
- Integration before polish (T008-T010)

## Parallel Example
```
# Launch T001 and T002 together:
Task: "Create a new test file `nextjs/src/app/rebranding.test.tsx` to check for the presence of 'T-Levet Assistant' in the UI."
Task: "Create a new test file `app/rebranding_test.py` to check for the presence of 'T-Levet' in the backend code."

# Launch T004, T005, and T006 together:
Task: "Replace all instances of 'T-Levet Assistant' with 'Expert In My Pocket' in the `nextjs` directory."
Task: "Replace all instances of 'T-Levet' with 'Expert In My Pocket' in the `app` directory."
Task: "Replace all instances of 'T-Levet' with 'Expert In My Pocket' in the root directory files (e.g., `GEMINI.md`, `README.md`)."

# Launch T008 and T009 together:
Task: "Delete the test file `nextjs/src/app/rebranding.test.tsx`."
Task: "Delete the test file `app/rebranding_test.py`."
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [X] All contracts have corresponding tests
- [X] All entities have model tasks
- [X] All tests come before implementation
- [X] Parallel tasks truly independent
- [X] Each task specifies exact file path
- [X] No task modifies same file as another [P] task
