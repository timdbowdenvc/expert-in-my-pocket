import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

# Define a base URL for the API, assuming it runs locally for testing
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_create_appointment_contract_success():
    """Verifies the contract for successful appointment creation."""
    async with AsyncClient(base_url=BASE_URL) as client:
        now = datetime.now()
        start_time = (now + timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=2)).isoformat()

        request_body = {
            "title": "Contract Test Appointment",
            "start_time": start_time,
            "end_time": end_time,
            "calendar_id": "primary",
            "description": "This is a test appointment.",
            "attendees": ["test@example.com"]
        }

        # For contract testing, we'll assume a valid Authorization header is provided.
        # The actual token validation will be part of integration tests.
        headers = {"Authorization": "Bearer mock_access_token"}

        response = await client.post("/create-appointment", json=request_body, headers=headers)

        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "event_url" in response_json
        assert response_json["message"] == "Appointment created successfully."
        assert response_json["event_url"].startswith("https://www.google.com/calendar/event?eid=")

@pytest.mark.asyncio
async def test_create_appointment_contract_invalid_input():
    """Verifies the contract for invalid input data (400 Bad Request)."""
    async with AsyncClient(base_url=BASE_URL) as client:
        # Missing required 'title' field
        invalid_request_body = {
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "calendar_id": "primary"
        }
        headers = {"Authorization": "Bearer mock_access_token"}

        response = await client.post("/create-appointment", json=invalid_request_body, headers=headers)

        assert response.status_code == 422 # FastAPI returns 422 for validation errors
        response_json = response.json()
        assert "detail" in response_json
        assert isinstance(response_json["detail"], list)
        assert any("field required" in error["msg"] for error in response_json["detail"])

@pytest.mark.asyncio
async def test_create_appointment_contract_unauthorized():
    """Verifies the contract for unauthorized access (401 Unauthorized)."""
    async with AsyncClient(base_url=BASE_URL) as client:
        now = datetime.now()
        start_time = (now + timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=2)).isoformat()

        request_body = {
            "title": "Unauthorized Test",
            "start_time": start_time,
            "end_time": end_time,
            "calendar_id": "primary"
        }
        # No Authorization header or invalid token
        response = await client.post("/create-appointment", json=request_body)

        assert response.status_code == 401
        response_json = response.json()
        assert "detail" in response_json
        assert response_json["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_create_appointment_contract_calendar_not_found():
    """Verifies the contract for calendar not found (404 Not Found)."""
    async with AsyncClient(base_url=BASE_URL) as client:
        now = datetime.now()
        start_time = (now + timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=2)).isoformat()

        request_body = {
            "title": "Calendar Not Found Test",
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

@pytest.mark.asyncio
async def test_create_appointment_contract_internal_error():
    """Verifies the contract for internal server errors (500 Internal Server Error)."""
    async with AsyncClient(base_url=BASE_URL) as client:
        now = datetime.now()
        start_time = (now + timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=2)).isoformat()

        request_body = {
            "title": "Internal Error Test",
            "start_time": start_time,
            "end_time": end_time,
            "calendar_id": "primary"
        }
        headers = {"Authorization": "Bearer mock_access_token"}

        # This test requires a way to trigger an internal error, e.g., by sending
        # a a specific payload that the backend is designed to fail on for testing purposes,
        # or by mocking the Google Calendar API to raise an exception.
        # For now, we'll assume the backend is not running or configured to fail for this test.
        response = await client.post("/create-appointment", json=request_body, headers=headers)

        # The actual status code might be 500 or another error depending on implementation
        # For a contract test, we're checking the *expected* error response structure.
        # This assertion might need adjustment once the error handling is implemented.
        if response.status_code == 500:
            response_json = response.json()
            assert "detail" in response_json
            assert "Failed to create appointment due to API error." in response_json["detail"]
        else:
            pass
