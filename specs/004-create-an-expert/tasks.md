# Tasks: Expert SEO Sub-Agent

**Input**: Design documents from `/specs/004-create-an-expert/`
**Prerequisites**: plan.md, data-model.md, contracts/

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

## Phase 3.1: Setup
- [X] T001 Create directory structure for the new agent in `app/agent/seo_agent`.

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [X] T002 [P] Create contract test for `POST /api/seo-agent` in `app/tests/contract/test_seo_agent_post.py`.
- [X] T003 [P] Create integration test for the SEO agent workflow in `app/tests/integration/test_seo_agent.py` based on `quickstart.md`.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [X] T004 [P] Implement `SEOAnalysisRequest` and `SEOOtimisationReport` data models in `app/agent/seo_agent/models.py`.
- [X] T005 Implement the core logic for the `seo_agent` in `app/agent/seo_agent/agent.py`, using BeautifulSoup to parse the webpage data.
- [X] T006 Implement the `POST /api/seo-agent` endpoint in the main Flask/FastAPI app which calls the `seo_agent`.
- [X] T007 Update `root_agent` to delegate requests starting with `/seo` to the `seo_agent`.

## Phase 3.4: Polish
- [X] T008 [P] Add unit tests for the `seo_agent` logic in `app/tests/unit/test_seo_agent.py`.
- [X] T009 [P] Update documentation to include the new `/seo` command.

## Dependencies
- T001 must be completed before all other tasks.
- T002 and T003 must be completed before T005, T006, and T007.
- T004 must be completed before T005.

## Parallel Example
```
# Launch T002 and T003 together:
Task: "Create contract test for POST /api/seo-agent in app/tests/contract/test_seo_agent_post.py"
Task: "Create integration test for the SEO agent workflow in app/tests/integration/test_seo_agent.py based on quickstart.md"
```
