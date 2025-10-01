import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta

# Define a base URL for the API, assuming it runs locally for testing
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
@patch('mcp_server.schedule_mcp.google_calendar_client.build') # Mock the Google API client build function
async def test_create_appointment_integration_success(mock_build):
    """Verifies the integration for successful appointment creation."""
    # Mock Google Calendar API responses
    mock_events_insert = AsyncMock()
    mock_events_insert.execute.return_value = {
        'id': 'mock_event_id',
        'htmlLink': 'https://www.google.com/calendar/event?eid=mock_event_id'
    }

    mock_build.return_value.events.return_value.insert.return_value = mock_events_insert

    async with AsyncClient(base_url=BASE_URL) as client:
        now = datetime.now()
        start_time = (now + timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=2)).isoformat()

        request_body = {
            "title": "Integration Test Appointment",
            "start_time": start_time,
            "end_time": end_time,
            "calendar_id": "primary",
            "description": "This is an integration test appointment.",
            "attendees": ["test@example.com"]
        }
        headers = {"Authorization": "Bearer mock_access_token"}

        response = await client.post("/create-appointment", json=request_body, headers=headers)

        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "event_url" in response_json
        assert response_json["message"] == "Appointment created successfully."
        assert response_json["event_url"] == "https://www.google.com/calendar/event?eid=mock_event_id"

        # Verify that Google Calendar API calls were made
        mock_events_insert.assert_called_once()

@pytest.mark.asyncio
@patch('mcp_server.schedule_mcp.google_calendar_client.build')
async def test_create_appointment_integration_calendar_not_found(mock_build):
    """Verifies handling of calendar not found in integration."""
    # Mock Google Calendar API to simulate calendar not found
    from googleapiclient.errors import HttpError
    mock_events_insert = AsyncMock()
    mock_events_insert.execute.side_effect = HttpError(resp=MagicMock(status=404, reason="Not Found"), content=b'')

    mock_build.return_value.events.return_value.insert.return_value = mock_events_insert

    async with AsyncClient(base_url=BASE_URL) as client:
        now = datetime.now()
        start_time = (now + timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=2)).isoformat()

        request_body = {
            "title": "Integration Test Calendar Not Found",
            "start_time": start_time,
            "end_time": end_time,
            "calendar_id": "non_existent_calendar_id"
        }
        headers = {"Authorization": "Bearer mock_access_token"}

        response = await client.post("/create-appointment", json=request_body, headers=headers)

        assert response.status_code == 404
        response_json = response.json()
        assert "detail" in response_json
        assert "Calendar 'non_existent_calendar_id' not found or inaccessible." in response_json["detail"]

        mock_events_insert.assert_called_once()

# More integration tests for other edge cases (e.g., auth errors, malformed data) will be added as implementation progresses.
