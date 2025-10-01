# Research: Schedule MCP Server

## Google Calendar API Interaction

### 1. Authentication
-   **Method**: OAuth 2.0 for accessing individual user calendars, requiring user consent (as per clarification).
-   **Details**: 
    1.  **Google Cloud Project Setup**: Requires a GCP project, enabling the Google Calendar API.
    2.  **OAuth Consent Screen**: Configure the OAuth consent screen with application name, user support email, and developer contact information.
    3.  **Credentials**: Create OAuth 2.0 Client IDs (Web application type) to obtain `client_id` and `client_secret`.
    4.  **Authorization Flow**: Implement the Authorization Code Grant flow:
        -   User is redirected to Google's authorization server.
        -   User grants consent for the application to access their calendar.
        -   Google redirects back to the application with an authorization code.
        -   The application exchanges the authorization code for `access_token` and `refresh_token`.
        -   `access_token` is used for API calls; `refresh_token` is used to obtain new access tokens when the current one expires.
    5.  **Token Storage**: Securely store `refresh_token` associated with the user.

### 2. Creating a New Event
-   **API Endpoint**: `events.insert`
-   **Request Body**: Requires event details such as `summary` (title), `start` (datetime), `end` (datetime), `calendarId`.
-   **Minimum Required Fields**: `title`, `start_time`, `end_time`, `calendar_id` (as per clarification).

### 3. Identifying the Target Calendar
-   **Method**: By its unique Calendar ID (e.g., `user@example.com` or a long alphanumeric string) (as per clarification).
-   **Details**: The `calendarId` parameter in `events.insert` will be populated with this ID.

### 4. Handling Event Details
-   **Title**: Maps to `summary` field in Google Calendar Event.
-   **Start Time**: Maps to `start.dateTime` (or `start.date` for all-day events).
-   **End Time**: Maps to `end.dateTime` (or `end.date` for all-day events).
-   **Attendees**: Can be specified in the `attendees` field (array of email addresses).

### 5. Handling Conflicting Appointments
-   **Behavior**: Create the new appointment regardless of conflicts (as per clarification).
-   **Details**: No pre-check for overlaps is required before inserting the event. The Google Calendar API will simply create the event.

### 6. Error Handling
-   **Types of Errors**: API rate limits, authentication failures (invalid tokens, expired tokens), invalid calendar IDs, malformed input data, network issues.
-   **Strategy**: Implement robust `try-except` blocks, log errors, and return meaningful error messages to the calling agent (as per FR-004).

## Technical Context

-   **Language**: Python (consistent with existing ADK agents and MCP servers).
-   **Framework**: FastAPI for the MCP server endpoint.
-   **Google Cloud Libraries**: `google-api-python-client` for Google Calendar API, `google-auth-oauthlib` for OAuth 2.0 flow.
-   **Deployment**: Google Cloud Run (consistent with Cloud-Native Deployment principle).
-   **Authentication**: OAuth 2.0 Authorization Code Grant flow for web applications. Secure storage of refresh tokens will be critical.
-   **Google Calendar API Usage**: Utilize `events.insert` for creating events.