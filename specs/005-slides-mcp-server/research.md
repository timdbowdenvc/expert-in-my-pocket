# Research: Slides MCP Server

## Google Slides API Interaction

### 1. Authentication
-   **Method**: Service Account authentication (as per clarification).
-   **Details**: Requires a Google Cloud Platform (GCP) project, enabling the Google Slides API and Google Drive API, creating a service account, generating a JSON key file, and granting the service account appropriate roles (e.g., `Editor` for Google Slides and Google Drive).

### 2. Creating a New Presentation
-   **API Endpoint**: `presentations.create`
-   **Request Body**: Can specify title. Initial slides and layouts can be added during creation or subsequently.

### 3. Applying Layouts and Styles from Templates
-   **Source**: Dedicated Google Drive folder containing multiple approved layout/style templates (as per clarification).
-   **Process**: 
    1.  Identify the template presentation(s) in the specified Google Drive folder.
    2.  Copy a template presentation to create a new presentation, or extract layouts/masters from a template and apply them to the new presentation.
    3.  The Google Slides API allows copying slides from one presentation to another, or applying a master slide from an existing presentation.
    4.  Need to determine how the incoming data from the slides agent will specify which template/layout to use.

### 4. Adding Content to Slides
-   **API Endpoints**: `presentations.batchUpdate` with various requests:
    -   `CreateSlide`: Add new slides.
    -   `CreateShape`: Add text boxes, images, etc.
    -   `InsertText`: Add text to shapes.
    -   `ReplaceAllText`: Find and replace placeholders.
    -   `CreateImage`: Insert images.

### 5. Persisting the Presentation
-   **Location**: Shared Google Drive folder owned by a service account (as per clarification).
-   **Process**: 
    1.  The `presentations.create` method can specify the parent folder ID in Google Drive.
    2.  Ensure the service account has appropriate permissions (`Editor` or `Writer`) for the target shared folder.
-   **Naming Convention**: Supplied title suffixed with date (as per clarification).
    -   Example: `My Presentation Title 2025-09-30`

### 6. Error Handling
-   **Types of Errors**: API rate limits, authentication failures, invalid template IDs, malformed input data, network issues.
-   **Strategy**: Implement robust `try-except` blocks, log errors, and return meaningful error messages to the calling slides agent (as per FR-005).

## Technical Context

-   **Language**: Python (consistent with existing ADK agents and MCP servers).
-   **Framework**: FastAPI for the MCP server endpoint.
-   **Google Cloud Libraries**: `google-api-python-client` for Google Slides and Google Drive APIs, `google-auth` for authentication.
-   **Deployment**: Google Cloud Run (consistent with Cloud-Native Deployment principle).