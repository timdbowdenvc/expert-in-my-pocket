from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class AppointmentRequest(BaseModel):
    title: str = Field(..., description="The title/summary of the calendar event.")
    start_time: datetime = Field(..., description="The start date and time of the event in ISO 8601 format.")
    end_time: datetime = Field(..., description="The end date and time of the event in ISO 8601 format.")
    calendar_id: str = Field(..., description="The unique identifier of the Google Calendar.")
    description: Optional[str] = Field(None, description="A detailed description of the event.")
    attendees: Optional[List[EmailStr]] = Field(None, description="List of email addresses for attendees.")
