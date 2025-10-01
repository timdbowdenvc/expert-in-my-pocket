# Data Model: Schedule MCP Server

## Appointment Request

This is the primary data structure that the Schedule MCP Server will receive to create a new Google Calendar event.

```json
{
  "title": "string",
  "start_time": "datetime",
  "end_time": "datetime",
  "calendar_id": "string",
  "description": "string",
  "attendees": [
    "string"
  ]
}
```

### Fields:

-   **`title`** (string, required):
    -   The title/summary of the calendar event.

-   **`start_time`** (datetime, required):
    -   The start date and time of the event in ISO 8601 format (e.g., `2025-10-26T10:00:00-07:00`).

-   **`end_time`** (datetime, required):
    -   The end date and time of the event in ISO 8601 format (e.g., `2025-10-26T11:00:00-07:00`).

-   **`calendar_id`** (string, required):
    -   The unique identifier of the Google Calendar to which the event will be added (e.g., `primary` or an email address).

-   **`description`** (string, optional):
    -   A detailed description of the event.

-   **`attendees`** (array of strings, optional):
    -   A list of email addresses for attendees to be invited to the event.

## Google Calendar Event

-   The output of the MCP server, a standard Google Calendar event created via the Google Calendar API.
-   Inserted into the specified `calendar_id`.
-   Conflicting appointments will be created regardless of overlap.