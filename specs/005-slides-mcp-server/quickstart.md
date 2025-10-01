# Quickstart: Slides MCP Server

This guide will help you set up and run the Slides MCP Server locally.

## Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.10+**
-   **`uv`** (or `pip` for dependency management)
-   **Google Cloud SDK**: For authenticating with Google Cloud services and managing service accounts.

## Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd expert-in-my-pocket
    ```

2.  **Install Dependencies**:
    Navigate to the `mcp_server` directory and install the required Python packages.
    ```bash
    cd mcp_server
    uv sync # or pip install -r requirements.txt
    ```

3.  **Google Cloud Service Account Setup**:
    The MCP Server uses a Google Cloud service account for authentication with the Google Slides and Google Drive APIs.

    a.  **Create a Service Account**: Follow the Google Cloud documentation to create a new service account in your GCP project.
    b.  **Enable APIs**: Ensure the **Google Slides API** and **Google Drive API** are enabled for your GCP project.
    c.  **Grant Permissions**: Grant the service account the necessary roles:
        -   `Google Slides Editor` (or a custom role with equivalent permissions for Slides)
        -   `Google Drive Editor` (or a custom role with equivalent permissions for Drive)
    d.  **Generate Key**: Create a new JSON key for the service account and download it. Save this file securely (e.g., `path/to/your-service-account-key.json`).

4.  **Environment Variables**:
    Create a `.env` file in the `mcp_server` directory with the following variables:

    ```dotenv
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account-key.json
    GOOGLE_DRIVE_SHARED_FOLDER_ID=<your-shared-google-drive-folder-id>
    GOOGLE_SLIDES_TEMPLATE_FOLDER_ID=<your-google-slides-template-folder-id>
    ```
    -   Replace `/path/to/your-service-account-key.json` with the absolute path to your downloaded service account key file.
    -   Replace `<your-shared-google-drive-folder-id>` with the ID of the Google Drive folder where generated presentations will be saved (as clarified in the spec).
    -   Replace `<your-google-slides-template-folder-id>` with the ID of the Google Drive folder containing your pre-saved style and layout templates (as clarified in the spec).

## Running the Server

From the `mcp_server` directory, start the FastAPI application:

```bash
uvicorn main:app --reload
```

The server will typically run on `http://127.0.0.1:8000`.

## Testing the Endpoint

You can test the `/create-presentation` endpoint using `curl` or a simple Python script.

### Example `curl` Command

```bash
curl -X POST \
  http://127.0.0.1:8000/create-presentation \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Test Presentation",
    "template_id": "<your-template-id>",
    "slides": [
      {
        "layout_id": "<your-layout-id>",
        "elements": [
          {
            "type": "text",
            "content": "Hello, World!"
          }
        ]
      }
    ]
  }'
```

-   Replace `<your-template-id>` with the ID or name of a template you want to use.
-   Replace `<your-layout-id>` with the ID or name of a layout within that template.

Upon success, you should receive a JSON response with a `presentation_url`.
