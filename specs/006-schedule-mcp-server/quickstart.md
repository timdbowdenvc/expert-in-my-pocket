# Quickstart: Schedule MCP Server

This guide will help you set up and run the Schedule MCP Server locally.

## Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.10+**
-   **`uv`** (or `pip` for dependency management)
-   **Google Cloud SDK**: For managing OAuth 2.0 credentials.

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

3.  **Google Cloud OAuth 2.0 Setup**:
    The MCP Server uses OAuth 2.0 for authentication with the Google Calendar API.

    a.  **Google Cloud Project Setup**: Ensure you have a GCP project and the **Google Calendar API** is enabled.
    b.  **OAuth Consent Screen**: Configure your OAuth consent screen in the Google Cloud Console.
    c.  **Create OAuth 2.0 Client IDs**: Create a new OAuth 2.0 Client ID of type "Web application". You will get a `client_id` and `client_secret`.
    d.  **Authorized Redirect URIs**: Add `http://localhost:8000/oauth2callback` (or your server's redirect URI) to the "Authorized redirect URIs" for your Web application client ID.

4.  **Environment Variables**:
    Create a `.env` file in the `mcp_server` directory with the following variables:

    ```dotenv
    GOOGLE_CLIENT_ID=<your-google-client-id>
    GOOGLE_CLIENT_SECRET=<your-google-client-secret>
    REDIRECT_URI=http://localhost:8000/oauth2callback
    # For local testing, you might need to manually obtain and store tokens
    # REFRESH_TOKEN=<your-user-refresh-token>
    ```
    -   Replace `<your-google-client-id>` and `<your-google-client-secret>` with the credentials from your OAuth 2.0 Client ID.

5.  **Obtain User Tokens (Manual for Local Testing)**:
    For local development, you'll typically need to perform the OAuth flow once to get a `refresh_token` for a user. This can be done using a script or a tool like `oauth2l`.
    -   **Example using `oauth2l` (install via `go install github.com/google/oauth2l@latest`)**:
        ```bash
        oauth2l fetch --client-id <your-google-client-id> --client-secret <your-google-client-secret> --scope https://www.googleapis.com/auth/calendar --redirect-uri http://localhost:8000/oauth2callback
        ```
        Follow the prompts to authorize. The output will include a `refresh_token`. Add this to your `.env` file.

## Running the Server

From the `mcp_server` directory, start the FastAPI application:

```bash
uvicorn main:app --reload
```

The server will typically run on `http://127.0.0.1:8000`.

## Testing the Endpoint

You can test the `/create-appointment` endpoint using `curl` or a simple Python script. You will need a valid `access_token` for the user whose calendar you are modifying.

### Example `curl` Command

```bash
curl -X POST \
  http://127.0.0.1:8000/create-appointment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-user-access-token>" \
  -d 
'{'
    "title": "Project Sync",
    "start_time": "2025-10-26T10:00:00-07:00",
    "end_time": "2025-10-26T11:00:00-07:00",
    "calendar_id": "primary",
    "description": "Discuss Q4 strategy.",
    "attendees": ["user@example.com"]
  }'
```

-   Replace `<your-user-access-token>` with a valid access token for the user.
-   Replace `primary` with the actual calendar ID if not using the primary calendar.

Upon success, you should receive a JSON response with an `event_url`.

```