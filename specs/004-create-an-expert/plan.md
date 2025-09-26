# Implementation Plan: Expert SEO Sub-Agent

**Branch**: `004-create-an-expert` | **Date**: 2025-09-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-create-an-expert/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
The feature is to create an expert SEO sub-agent that can take a URL, analyse the page and suggest SEO optimisations. The agent will be a sub-agent of the `root_agent` and will be located in `app/agent/seo_agent`. The `root_agent` will need to be updated to delegate tasks to this new agent. The agent will be integrated into the existing Next.js frontend and Python backend. The agent will analyze on-page, technical, and content SEO aspects and provide a human-readable Markdown report.

## Technical Context
**Language/Version**: Python 3.11, TypeScript 5.x
**Primary Dependencies**: ADK (Agent Development Kit), Next.js, React
**Storage**: N/A for this feature
**Testing**: pytest, Jest
**Target Platform**: Web Browser, Google Cloud Run
**Project Type**: Web application
**Performance Goals**: Standard web application performance
**Constraints**: No specific constraints identified
**Scale/Scope**: Single user initially, scalable to multiple users

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Modular Architecture**: Compliant. The new agent will be a new module in the agent-based backend.
- **User-Centric Design**: Compliant. The feature is user-facing and aims to provide value to the user.
- **Test-Driven Development (TDD)**: Compliant. The plan includes creating tests before implementation.
- **Cloud-Native Deployment**: Compliant. The feature will be deployed as part of the existing cloud-native application.
- **Clear and Concise Code**: Compliant. Will adhere to existing coding standards.
- **Agent-Driven Development**: Compliant. This workflow is being followed.
- **Infrastructure as Code (IaC)**: Compliant. No new infrastructure is required for this feature.

## Project Structure

### Documentation (this feature)
```
specs/004-create-an-expert/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 2: Web application (when "frontend" + "backend" detected)
app/
├── agent/
│   ├── root_agent/
│   └── seo_agent/      # New agent
├── agent_engine_app.py
└── tests/

nextjs/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: Option 2: Web application

### Agent Architecture
The new `seo_agent` will be a sub-agent of the `root_agent`. The `root_agent` will be responsible for receiving user requests and delegating SEO-related tasks to the `seo_agent`. This maintains a clear separation of concerns and allows for the independent development and testing of each agent.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context**: None.
2. **Generate and dispatch research agents**: No research needed as the technical context is clear and based on the existing project structure.
3. **Consolidate findings** in `research.md`: No research was conducted.

**Output**: research.md

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - SEO Analysis Request (URL)
   - SEO Optimisation Report (List of suggestions, analysis summary)
2. **Generate API contracts** from functional requirements:
   - A new endpoint will be created for the SEO agent.
   - The endpoint will accept a URL and return a Markdown report.
3. **Generate contract tests** from contracts:
   - A test will be created for the new endpoint.
4. **Extract test scenarios** from user stories:
   - Integration tests will be created to cover the user stories.
5. **Update agent file incrementally**:
   - Run `.specify/scripts/bash/update-agent-context.sh gemini`

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P]
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 10-15 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [X] Phase 0: Research complete (/plan command)
- [X] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [X] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [X] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v1.1.0 - See `/.specify/memory/constitution.md`*
