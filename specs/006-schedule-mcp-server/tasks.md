# Tasks: Schedule MCP Server Implementation

This document outlines the detailed, dependency-ordered tasks required to implement the Schedule MCP Server.

## Phase 1: Setup & Environment

- [X] **T001**: Create the directory structure for the Schedule MCP Server: `mcp_server/schedule_mcp/`.
    - **File Path**: `mcp_server/schedule_mcp/`
    - **Command**: `mkdir -p mcp_server/schedule_mcp`
- [X] **T002**: Add `schedule_mcp` as a package entry in `pyproject.toml` to ensure it's recognized as a Python module.
    - **File Path**: `pyproject.toml`
- [X] **T003**: Configure `.env` variables for Google OAuth credentials as specified in `quickstart.md`.
    - **File Path**: `mcp_server/.env`
- [X] **T004**: Set up Google Cloud OAuth 2.0 Client ID (Web application type) and obtain `client_id` and `client_secret`.
    - **Dependency**: T003 (for `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`)

## Phase 2: Testing (TDD Approach)

- [X] **T005 [P]**: Write a contract test for the `/create-appointment` endpoint based on `contracts/openapi.yml`.
    - **File Path**: `mcp_server/schedule_mcp/tests/contract_test.py`
    - **Description**: This test should verify the request/response structure and status codes as defined in the OpenAPI spec.
- [X] **T006 [P]**: Write an integration test for the core appointment creation flow, simulating a request and verifying the creation of an event in Google Calendar.
    - **File Path**: `mcp_server/schedule_mcp/tests/integration_test.py`
    - **Description**: This test will require mocking Google API calls initially, then can be updated to use real credentials.

## Phase 3: Core Implementation

- [X] **T007**: Implement Pydantic models for `AppointmentRequest` based on `data-model.md` and `openapi.yml`.
    - **File Path**: `mcp_server/schedule_mcp/models.py`
    - **Dependency**: T002
- [X] **T008**: Create the FastAPI application instance in `mcp_server/schedule_mcp/main.py`.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T002
- [X] **T009**: Implement the Google Calendar API client, including OAuth 2.0 authentication flow and functions for event creation.
    - **File Path**: `mcp_server/schedule_mcp/google_calendar_client.py`
    - **Dependency**: T004
- [X] **T010**: Implement the `POST /create-appointment` endpoint in `main.py`, using the Pydantic models for request validation.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T007, T008
- [X] **T011**: Integrate the Google Calendar API client into the `/create-appointment` endpoint to handle appointment creation.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T009, T010
- [X] **T012**: Implement logic to handle OAuth 2.0 token management (e.g., refreshing access tokens).
    - **File Path**: `mcp_server/schedule_mcp/main.py` or `google_calendar_client.py`
    - **Dependency**: T011
    - [X] **T012.1**: Implement function to store and retrieve user tokens (access and refresh tokens) securely.
    - [X] **T012.2**: Implement function to refresh expired access tokens using the refresh token.
    - [X] **T012.3**: Implement middleware or decorator to ensure authenticated requests have a valid access token, refreshing if necessary.
- [X] **T013**: Implement logic to verify the existence and accessibility of the specified `calendar_id`.
    - **File Path**: `mcp_server/schedule_mcp/main.py` or `google_calendar_client.py`
    - **Dependency**: T011
    - [X] **T013.1**: Implement function to check if a given `calendar_id` exists and is accessible to the authenticated user.
    - [X] **T013.2**: Integrate calendar verification into the `/create-appointment` endpoint.

## Phase 4: Integration & Error Handling

- [X] **T014**: Implement comprehensive error handling for API calls, input validation, and other potential issues within the `/create-appointment` endpoint.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T013
- [X] **T014.1**: Implement input validation for `AppointmentRequest` to handle malformed or incomplete data, returning `400 Bad Request` with a descriptive error message.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T014
- [X] **T014.2**: Implement specific error handling for Google Calendar API unavailability or network issues, returning `500 Internal Server Error`.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T014
- [X] **T014.3**: Implement specific error handling for scenarios where the specified `calendar_id` does not exist or is inaccessible, returning `404 Not Found`.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T014
- [X] **T015**: Add logging for key operations and errors within the MCP server.
    - **File Path**: `mcp_server/schedule_mcp/main.py`
    - **Dependency**: T014

## Phase 5: Polish & Deployment

- [X] **T016**: Write unit tests for the `google_calendar_client.py` functions, mocking external API calls.
    - **File Path**: `mcp_server/schedule_mcp/tests/unit_test.py`
    - **Dependency**: T009
- [X] **T017**: Update `mcp_server/Dockerfile` to include dependencies and configuration for the `schedule_mcp` service.
    - **File Path**: `mcp_server/Dockerfile`
- [X] **T018**: Document deployment steps for the Schedule MCP Server to Google Cloud Run.
    - **File Path**: `mcp_server/README.md` (or similar documentation)

## Parallel Execution Examples

- **Initial Setup (can run in parallel)**:
    - `T001`: `mkdir -p mcp_server/schedule_mcp`
    - `T002`: Update `pyproject.toml`
    - `T003`: Configure `mcp_server/.env`

- **Early Development (can run in parallel after setup)**:
    - `T005 [P]`: Write contract test
    - `T006 [P]`: Write integration test
    - `T007`: Implement Pydantic models
    - `T008`: Create FastAPI app

- **API Client & Endpoint (can run in parallel after models/app)**:
    - `T009`: Implement Google Calendar API client
    - `T010`: Implement `/create-appointment` endpoint