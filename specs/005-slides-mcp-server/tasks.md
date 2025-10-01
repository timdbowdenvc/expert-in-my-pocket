# Tasks: Slides MCP Server Implementation

This document outlines the detailed, dependency-ordered tasks required to implement the Slides MCP Server.

## Phase 1: Setup & Environment

- [X] **T001**: Create the directory structure for the Slides MCP Server: `mcp_server/slides_mcp/`.
    - **File Path**: `mcp_server/slides_mcp/`
    - **Command**: `mkdir -p mcp_server/slides_mcp`
- [X] **T002**: Add `slides_mcp` as a package entry in `pyproject.toml` to ensure it's recognized as a Python module.
    - **File Path**: `pyproject.toml`
- [X] **T003**: Configure `.env` variables for Google Cloud credentials and folder IDs as specified in `quickstart.md`.
    - **File Path**: `mcp_server/.env`
- [X] **T004**: Set up a Google Cloud service account with `Google Slides Editor` and `Google Drive Editor` roles, and download the JSON key file.
    - **Dependency**: T003 (for `GOOGLE_APPLICATION_CREDENTIALS`)

## Phase 2: Testing (TDD Approach)

- [X] **T005 [P]**: Write a contract test for the `/create-presentation` endpoint based on `contracts/openapi.yml`.
    - **File Path**: `mcp_server/slides_mcp/tests/contract_test.py`
    - **Description**: This test should verify the request/response structure and status codes as defined in the OpenAPI spec.
- [X] **T006 [P]**: Write an integration test for the core presentation creation flow, simulating a request from the slides agent and verifying the creation of a presentation in Google Drive.
    - **File Path**: `mcp_server/slides_mcp/tests/integration_test.py`
    - **Description**: This test will require mocking Google API calls initially, then can be updated to use real credentials.

## Phase 3: Core Implementation

- [X] **T007**: Implement Pydantic models for `PresentationRequest`, `Slide`, and `Element` based on `data-model.md` and `openapi.yml`.
    - **File Path**: `mcp_server/slides_mcp/models.py`
    - **Dependency**: T002
- [X] **T008**: Create the FastAPI application instance in `mcp_server/slides_mcp/main.py`.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T002
- [X] **T009**: Implement the Google Slides API client, including authentication and basic API interaction functions (e.g., `create_presentation`, `batch_update`).
    - **File Path**: `mcp_server/slides_mcp/google_slides_client.py`
    - **Dependency**: T004
- [X] **T010**: Implement the `POST /create-presentation` endpoint in `main.py`, using the Pydantic models for request validation.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T007, T008
- [X] **T011**: Integrate the Google Slides API client into the `/create-presentation` endpoint to handle presentation creation.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T009, T010
- [X] **T012**: Implement logic to apply layouts and styles from the dedicated Google Drive template folder.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T011
    - [X] **T012.1**: Implement function to search for template presentation by human-readable `template_id` in `GOOGLE_SLIDES_TEMPLATE_FOLDER_ID`.
    - [X] **T012.2**: Implement function to copy the identified template presentation to create a new presentation.
    - [X] **T012.3**: Implement function to apply a specific `layout_id` from the copied template to new slides.
    - [X] **T012.4**: Implement logic to handle default layout application if `layout_id` is not provided.
- [X] **T013**: Implement logic to add content (text, images) to slides based on the `elements` in the request.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T012
    - [X] **T013.1**: Implement function to add text elements to slides using `presentations.batchUpdate` with `InsertText` or `ReplaceAllText` requests.
    - [X] **T013.2**: Implement function to add image elements to slides using `presentations.batchUpdate` with `CreateImage` requests.
    - [X] **T013.3**: Implement logic to interpret `position` and `style` attributes for elements.
- [X] **T014**: Implement persistence of the created presentation to the shared Google Drive folder with the specified naming convention.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T013

## Phase 4: Integration & Error Handling

- [X] **T015**: Implement comprehensive error handling for API calls, input validation, and other potential issues within the `/create-presentation` endpoint.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T014
- [X] **T015.1**: Implement input validation for `PresentationRequest` to handle malformed or incomplete data, returning `400 Bad Request` with a descriptive error message.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T015
- [X] **T015.2**: Implement specific error handling for Google Slides API authentication failures, returning `500 Internal Server Error` with appropriate detail.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T015
- [X] **T015.3**: Implement error handling for scenarios where a specified `template_id` or `layout_id` does not exist, returning `400 Bad Request` with a clear message.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T015
- [X] **T016**: Add logging for key operations and errors within the MCP server.
    - **File Path**: `mcp_server/slides_mcp/main.py`
    - **Dependency**: T015

## Phase 5: Polish & Deployment

- [X] **T017**: Write unit tests for the `google_slides_client.py` functions, mocking external API calls.
    - **File Path**: `mcp_server/slides_mcp/tests/unit_test.py`
    - **Dependency**: T009
- [X] **T018**: Update `mcp_server/Dockerfile` to include dependencies and configuration for the `slides_mcp` service.
    - **File Path**: `mcp_server/Dockerfile`
- [X] **T019**: Document deployment steps for the Slides MCP Server to Google Cloud Run.
    - **File Path**: `mcp_server/README.md` (or similar documentation)

## Parallel Execution Examples

- **Initial Setup (can run in parallel)**:
    - `T001`: `mkdir -p mcp_server/slides_mcp`
    - `T002`: Update `pyproject.toml`
    - `T003`: Configure `mcp_server/.env`

- **Early Development (can run in parallel after setup)**:
    - `T005 [P]`: Write contract test
    - `T006 [P]`: Write integration test
    - `T007`: Implement Pydantic models
    - `T008`: Create FastAPI app

- **API Client & Endpoint (can run in parallel after models/app)**:
    - `T009`: Implement Google Slides API client
    - `T010`: Implement `/create-presentation` endpoint