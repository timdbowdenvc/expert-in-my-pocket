import logging
import os

import google.auth
from fastapi import FastAPI, HTTPException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pydantic import BaseModel

# --- Configuration ---
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive.file",
]

# --- FastAPI App ---
app = FastAPI(
    title="MCP Server for Google Slides",
    description="A server to generate Google Slides presentations.",
)


# --- Pydantic Models ---
class Slide(BaseModel):
    title: str
    content: str


class PresentationRequest(BaseModel):
    title: str
    slides: list[Slide]
    email: str


class PresentationResponse(BaseModel):
    presentation_url: str


# --- Helper Functions ---
def get_credentials() -> Credentials:
    """Gets the Google credentials for the application."""
    # For Cloud Run, use Application Default Credentials
    if os.environ.get("K_SERVICE"):
        creds, project = google.auth.default(scopes=SCOPES)
        return creds
    else:
        # For local development, use user's gcloud credentials
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # This will trigger the OAuth flow in a local environment
                # if no token.json is present.
                from google_auth_oauthlib.flow import InstalledAppFlow

                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds


# --- API Endpoints ---
@app.post("/generate_slides", response_model=PresentationResponse)
def generate_slides(request: PresentationRequest) -> PresentationResponse:
    """Generates a Google Slides presentation."""
    try:
        creds = get_credentials()
        slides_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)

        # Create the presentation
        presentation = (
            slides_service.presentations()
            .create(body={"title": request.title})
            .execute()
        )
        presentation_id = presentation.get("presentationId")
        presentation_url = (
            f"https://docs.google.com/presentation/d/{presentation_id}/edit"
        )

        # Share the presentation with the user
        permission = {"type": "user", "role": "writer", "emailAddress": request.email}
        drive_service.permissions().create(
            fileId=presentation_id, body=permission, fields="id"
        ).execute()

        # Add slides
        requests = []
        for i, slide_data in enumerate(request.slides):
            # Title slide
            if i == 0:
                requests.append(
                    {
                        "createSlide": {
                            "slideLayoutReference": {"predefinedLayout": "TITLE"},
                            "placeholderIdMappings": [
                                {
                                    "layoutPlaceholder": {"type": "CENTERED_TITLE"},
                                    "objectId": f"title_{i}",
                                },
                                {
                                    "layoutPlaceholder": {"type": "SUBTITLE"},
                                    "objectId": f"subtitle_{i}",
                                },
                            ],
                        }
                    }
                )
                requests.append(
                    {
                        "insertText": {
                            "objectId": f"title_{i}",
                            "text": slide_data.title,
                        }
                    }
                )
                requests.append(
                    {
                        "insertText": {
                            "objectId": f"subtitle_{i}",
                            "text": slide_data.content,
                        }
                    }
                )
            else:
                # Content slide
                requests.append(
                    {
                        "createSlide": {
                            "slideLayoutReference": {
                                "predefinedLayout": "TITLE_AND_BODY"
                            },
                            "placeholderIdMappings": [
                                {
                                    "layoutPlaceholder": {"type": "TITLE"},
                                    "objectId": f"title_{i}",
                                },
                                {
                                    "layoutPlaceholder": {"type": "BODY"},
                                    "objectId": f"body_{i}",
                                },
                            ],
                        }
                    }
                )
                requests.append(
                    {
                        "insertText": {
                            "objectId": f"title_{i}",
                            "text": slide_data.title,
                        }
                    }
                )
                requests.append(
                    {
                        "insertText": {
                            "objectId": f"body_{i}",
                            "text": slide_data.content,
                        }
                    }
                )

        if requests:
            slides_service.presentations().batchUpdate(
                presentationId=presentation_id, body={"requests": requests}
            ).execute()

        return PresentationResponse(presentation_url=presentation_url)

    except Exception as e:
        logging.error(f"Error generating slides: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) from e
