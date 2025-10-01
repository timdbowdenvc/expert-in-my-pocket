
# Implementation Plan: Slides MCP Server

**Branch**: `005-slides-mcp-server` | **Date**: 2025-09-30 | **Spec**: /specs/005-slides-mcp-server/spec.md

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
[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

-   **Language**: Python (consistent with existing ADK agents and MCP servers).
-   **Framework**: FastAPI for the MCP server endpoint.
-   **Google Cloud Libraries**: `google-api-python-client` for Google Slides and Google Drive APIs, `google-auth` for authentication.
-   **Deployment**: Google Cloud Run (consistent with Cloud-Native Deployment principle).
-   **Authentication**: Service account with JSON key file, granting `Editor` roles for Google Slides and Google Drive.
-   **Google Slides API Usage**: Utilize `presentations.create` for new presentations, `presentations.batchUpdate` for content manipulation, and Google Drive API for folder management.

## Progress Tracking

- [X] Phase 0: Research & Technical Context
- [X] Phase 1: Design Artifacts
- [X] Phase 2: Task Breakdown

**Status**: Ready for Implementation
---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
