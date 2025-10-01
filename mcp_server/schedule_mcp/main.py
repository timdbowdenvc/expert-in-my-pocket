from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from .models import AppointmentRequest
from .google_calendar_client import get_calendar_service, create_calendar_event, get_calendar_details, get_credentials
from googleapiclient.errors import HttpError
import os
import logging
from google.oauth2.credentials import Credentials

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# OAuth2 scheme for FastAPI
security = HTTPBearer()

# Dependency to get OAuth credentials
async def get_current_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # The token from the Authorization header is the access token.
    # We need to ensure it's valid and associated with a user's refresh token.
    # For this MCP, we'll assume the access token is part of a pre-existing valid credential set.
    # In a full OAuth flow, you'd exchange an authorization code for tokens.
    # Here, we're relying on get_credentials to handle refresh if needed.
    try:
        creds = get_credentials() # This will load/refresh from token.json
        if creds.token != credentials.credentials: # Check if the provided token matches the current valid one
            # This is a simplified check. A real app would validate the incoming token.
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token provided.")
        return creds
    except ValueError as e:
        logging.error(f"Authentication error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected authentication error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")

@app.get("/health")
async def health_check():
    logging.info("Health check requested.")
    return {"status": "ok"}

@app.post("/create-appointment", status_code=status.HTTP_200_OK)
async def create_appointment_endpoint(request: AppointmentRequest, creds: Credentials = Depends(get_current_credentials)):
    logging.info(f"Received request to create appointment: {request.title} for calendar {request.calendar_id}")
    try:
        calendar_service = get_calendar_service() # This will use the token implicitly

        # T013.1: Implement function to check if a given calendar_id exists and is accessible.
        # T013.2: Integrate calendar verification into the /create-appointment endpoint.
        try:
            get_calendar_details(request.calendar_id, calendar_service)
            logging.info(f"Calendar '{request.calendar_id}' verified.")
        except HttpError as e:
            if e.resp.status == 404:
                logging.error(f"Calendar '{request.calendar_id}' not found or inaccessible.")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Calendar '{request.calendar_id}' not found or inaccessible.")
            else:
                raise

        event_body = {
            'summary': request.title,
            'start': {
                'dateTime': request.start_time.isoformat(),
                'timeZone': 'UTC', # Assuming UTC for now, can be made configurable
            },
            'end': {
                'dateTime': request.end_time.isoformat(),
                'timeZone': 'UTC', # Assuming UTC for now, can be made configurable
            },
        }

        if request.description:
            event_body['description'] = request.description
        if request.attendees:
            event_body['attendees'] = [{'email': email} for email in request.attendees]

        event = create_calendar_event(request.calendar_id, event_body, calendar_service)
        event_url = event.get('htmlLink')

        logging.info(f"Appointment created successfully: {event_url}")
        return {"message": "Appointment created successfully.", "event_url": event_url}
    except ValidationError as e:
        logging.error(f"Validation error: {e.errors()}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
    except HttpError as e:
        if e.resp.status == 401:
            logging.error(f"Google API authentication error: {e.resp.status} - {e.resp.reason}. Token might be invalid or expired.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed or token expired.")
        elif e.resp.status == 404:
            logging.error(f"Google Calendar not found or inaccessible: {e.resp.status} - {e.resp.reason}. Calendar ID: {request.calendar_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Calendar '{request.calendar_id}' not found or inaccessible.")
        else:
            logging.error(f"Google API error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Google API error: {e}")
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create appointment: {e}")
