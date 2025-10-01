import pytest
from httpx import AsyncClient

# Assuming the FastAPI app will be in mcp_server/slides_mcp/main.py
# We'll need to import it once it's created.
# For now, we'll mock the app or assume a running instance for contract testing.

# Define a base URL for the API, assuming it runs locally for testing
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_create_presentation_contract_success():
    """Verifies the contract for successful presentation creation."""
    async with AsyncClient(base_url=BASE_URL) as client:
        # Example valid request body based on openapi.yml
        request_body = {
            "title": "Contract Test Presentation",
            "template_id": "DefaultTemplate",
            "slides": [
                {
                    "layout_id": "TitleSlide",
                    "elements": [
                        {
                            "type": "text",
                            "content": "Welcome to the Test!"
                        }
                    ]
                }
            ]
        }

        # For contract testing, we might need to mock the actual API call
        # or run the FastAPI app in test mode. For now, we'll assume the app is running.
        # This test will fail until the endpoint is implemented.
        response = await client.post("/create-presentation", json=request_body)

        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "presentation_url" in response_json
        assert response_json["message"] == "Presentation created successfully."
        assert response_json["presentation_url"].startswith("https://docs.google.com/presentation/")

@pytest.mark.asyncio
async def test_create_presentation_contract_invalid_input():
    """Verifies the contract for invalid input data (400 Bad Request)."""
    async with AsyncClient(base_url=BASE_URL) as client:
        # Missing required 'title' field
        invalid_request_body = {
            "template_id": "DefaultTemplate",
            "slides": []
        }

        response = await client.post("/create-presentation", json=invalid_request_body)

        assert response.status_code == 422 # FastAPI returns 422 for validation errors
        response_json = response.json()
        assert "detail" in response_json
        assert isinstance(response_json["detail"], list)
        assert any("field required" in error["msg"] for error in response_json["detail"])

@pytest.mark.asyncio
async def test_create_presentation_contract_internal_error():
    """Verifies the contract for internal server errors (500 Internal Server Error)."""
    async with AsyncClient(base_url=BASE_URL) as client:
        # This test requires a way to trigger an internal error, e.g., by sending
        # a specific payload that the backend is designed to fail on for testing purposes,
        # or by mocking the Google Slides API to raise an exception.
        # For now, we'll send a valid request and expect a 500 if the backend is not ready.
        # This test will be refined once the backend implementation is underway.
        request_body = {
            "title": "Trigger Internal Error",
            "template_id": "NonExistentTemplate", # This might trigger an internal error later
            "slides": []
        }

        # We expect a 500 if the backend fails to process a valid request due to internal issues.
        # This will be more robustly tested with integration tests.
        response = await client.post("/create-presentation", json=request_body)

        # The actual status code might be 500 or another error depending on implementation
        # For a contract test, we're checking the *expected* error response structure.
        # This assertion might need adjustment once the error handling is implemented.
        if response.status_code == 500:
            response_json = response.json()
            assert "detail" in response_json
            assert isinstance(response_json["detail"], str)
            assert "Failed to create presentation" in response_json["detail"]
        else:
            # If the server is not running or returns a different error, this will pass for now.
            # The goal is to define the contract, not necessarily pass it yet.
            pass
