import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

# This is a placeholder for secure token storage. In a real application,
# tokens should be stored securely (e.g., in a database associated with a user).
TOKEN_STORAGE_PATH = os.path.join(os.path.dirname(__file__), "token.json")

def save_credentials(creds: Credentials):
    """Saves user credentials to a file."""
    with open(TOKEN_STORAGE_PATH, 'w') as token_file:
        token_file.write(creds.to_json())

def get_credentials(user_id: str = "default_user") -> Credentials:
    """Retrieves or refreshes user credentials."""
    creds = None
    if os.path.exists(TOKEN_STORAGE_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_STORAGE_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_credentials(creds) # Save refreshed token
        else:
            # This part of the flow is typically handled by a frontend or a separate auth service.
            # For an MCP server, we expect to receive a refresh token or have it pre-configured.
            # For local testing, you might need to manually generate token.json.
            # If running locally for the first time, you'd need to run an OAuth flow.
            # For this MCP, we'll assume token.json is pre-generated or REFRESH_TOKEN is set.
            # If REFRESH_TOKEN is set in .env, use it to create initial credentials.
            refresh_token = os.getenv("REFRESH_TOKEN")
            if refresh_token:
                creds = Credentials(
                    token=None,
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.getenv("GOOGLE_CLIENT_ID"),
                    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
                    scopes=SCOPES
                )
                creds.refresh(Request())
                save_credentials(creds)
            else:
                raise ValueError("No valid credentials found. Please ensure token.json exists or REFRESH_TOKEN is set in .env.")
    return creds

def get_calendar_service(user_id: str = "default_user"):
    """Authenticates and returns a Google Calendar service object."""
    creds = get_credentials(user_id)
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(calendar_id: str, event_body: dict, service):
    """Creates a new event in the specified Google Calendar."""
    try:
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
        return event
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise

def get_calendar_details(calendar_id: str, service):
    """Retrieves details for a specific calendar."""
    try:
        calendar = service.calendars().get(calendarId=calendar_id).execute()
        return calendar
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise

# Placeholder for Request object for refresh token flow
class Request:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("REDIRECT_URI")

    def post(self, url, data=None, headers=None):
        import requests
        return requests.post(url, data=data, headers=headers)

    def get(self, url, headers=None):
        import requests
        return requests.get(url, headers=headers)
