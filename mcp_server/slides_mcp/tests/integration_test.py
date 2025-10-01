import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

# Assuming the FastAPI app will be in mcp_server/slides_mcp/main.py
# We'll need to import it once it's created.
# For now, we'll mock the app or assume a running instance for testing.

# Define a base URL for the API, assuming it runs locally for testing
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
@patch('mcp_server.slides_mcp.google_slides_client.build') # Mock the Google API client build function
async def test_create_presentation_integration_success(mock_build):
    """Verifies the integration for successful presentation creation."""
    # Mock Google Slides API responses
    mock_presentations_create = AsyncMock()
    mock_presentations_create.execute.return_value = {
        'presentationId': 'mock_presentation_id',
        'slides': [{'objectId': 'mock_slide_id'}]
    }

    mock_presentations_batch_update = AsyncMock()
    mock_presentations_batch_update.execute.return_value = {}

    mock_drive_files_create = AsyncMock()
    mock_drive_files_create.execute.return_value = {
        'id': 'mock_file_id',
        'webViewLink': 'https://docs.google.com/presentation/d/mock_file_id'
    }

    mock_build.return_value.presentations.return_value.create.return_value = mock_presentations_create
    mock_build.return_value.presentations.return_value.batchUpdate.return_value = mock_presentations_batch_update
    mock_build.return_value.files.return_value.create.return_value = mock_drive_files_create

    async with AsyncClient(base_url=BASE_URL) as client:
        request_body = {
            "title": "Integration Test Presentation",
            "template_id": "TestTemplate",
            "slides": [
                {
                    "layout_id": "TestLayout",
                    "elements": [
                        {
                            "type": "text",
                            "content": "Integration Test Content"
                        }
                    ]
                }
            ]
        }

        response = await client.post("/create-presentation", json=request_body)

        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "presentation_url" in response_json
        assert response_json["message"] == "Presentation created successfully."
        assert response_json["presentation_url"] == "https://docs.google.com/presentation/d/mock_file_id"

        # Verify that Google Slides API calls were made
        mock_presentations_create.assert_called_once()
        mock_presentations_batch_update.assert_called_once()
        mock_drive_files_create.assert_called_once()

@pytest.mark.asyncio
@patch('mcp_server.slides_mcp.google_slides_client.build')
async def test_create_presentation_integration_invalid_template(mock_build):
    """Verifies handling of invalid template_id in integration."""
    # Mock Google Slides API to simulate template not found
    mock_presentations_create = AsyncMock()
    mock_presentations_create.execute.return_value = {
        'presentationId': 'mock_presentation_id',
        'slides': [{'objectId': 'mock_slide_id'}]
    }
    mock_build.return_value.presentations.return_value.create.return_value = mock_presentations_create

    async with AsyncClient(base_url=BASE_URL) as client:
        request_body = {
            "title": "Integration Test Invalid Template",
            "template_id": "NonExistentTemplate",
            "slides": []
        }

        response = await client.post("/create-presentation", json=request_body)

        assert response.status_code == 400
        response_json = response.json()
        assert "detail" in response_json
        assert "Template 'NonExistentTemplate' not found" in response_json["detail"]

        mock_presentations_create.assert_called_once()

# More integration tests for other edge cases (e.g., auth errors, malformed data) will be added as implementation progresses.
