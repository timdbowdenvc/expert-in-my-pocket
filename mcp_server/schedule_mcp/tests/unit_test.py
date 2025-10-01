import pytest
from unittest.mock import MagicMock, patch
import os
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# Assuming google_calendar_client.py is in the same package
from mcp_server.schedule_mcp.google_calendar_client import (
    get_credentials,
    get_calendar_service,
    create_calendar_event,
    get_calendar_details,
    save_credentials,
    TOKEN_STORAGE_PATH
)

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        "GOOGLE_CLIENT_ID": "mock_client_id",
        "GOOGLE_CLIENT_SECRET": "mock_client_secret",
        "REDIRECT_URI": "http://localhost:8000/oauth2callback",
        "REFRESH_TOKEN": "mock_refresh_token",
    }):
        yield

# Mock googleapiclient.discovery.build
@pytest.fixture
def mock_build():
    with patch('mcp_server.schedule_mcp.google_calendar_client.build') as mock_build_func:
        yield mock_build_func

# Mock os.path.exists for token.json
@pytest.fixture
def mock_token_exists():
    with patch('os.path.exists', return_value=False) as mock_exists:
        yield mock_exists

# Mock Credentials.from_authorized_user_file
@pytest.fixture
def mock_from_authorized_user_file():
    with patch('google.oauth2.credentials.Credentials.from_authorized_user_file') as mock_from_file:
        yield mock_from_file

# Mock Credentials.refresh
@pytest.fixture
def mock_creds_refresh():
    with patch('google.oauth2.credentials.Credentials.refresh') as mock_refresh:
        yield mock_refresh

# Mock save_credentials
@pytest.fixture
def mock_save_credentials():
    with patch('mcp_server.schedule_mcp.google_calendar_client.save_credentials') as mock_save:
        yield mock_save

# Test get_credentials - no token.json, uses refresh token
def test_get_credentials_from_refresh_token(mock_token_exists, mock_from_authorized_user_file, mock_creds_refresh, mock_save_credentials):
    mock_token_exists.return_value = False
    mock_from_authorized_user_file.return_value = None

    creds = get_credentials()
    assert creds is not None
    mock_creds_refresh.assert_called_once()
    mock_save_credentials.assert_called_once()

# Test get_credentials - token.json exists and is valid
def test_get_credentials_from_file_valid(mock_token_exists, mock_from_authorized_user_file):
    mock_token_exists.return_value = True
    mock_creds = MagicMock(spec=Credentials, valid=True)
    mock_from_authorized_user_file.return_value = mock_creds

    creds = get_credentials()
    assert creds == mock_creds
    mock_from_authorized_user_file.assert_called_once()

# Test get_credentials - token.json exists, expired, refreshes
def test_get_credentials_from_file_expired_refreshes(mock_token_exists, mock_from_authorized_user_file, mock_creds_refresh, mock_save_credentials):
    mock_token_exists.return_value = True
    mock_creds = MagicMock(spec=Credentials, valid=False, expired=True, refresh_token="some_refresh")
    mock_from_authorized_user_file.return_value = mock_creds

    creds = get_credentials()
    assert creds == mock_creds
    mock_creds_refresh.assert_called_once()
    mock_save_credentials.assert_called_once()

# Test get_calendar_service
def test_get_calendar_service(mock_build):
    mock_creds = MagicMock(spec=Credentials, valid=True)
    with patch('mcp_server.schedule_mcp.google_calendar_client.get_credentials', return_value=mock_creds):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        service = get_calendar_service()
        assert service == mock_service
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_creds)

# Test create_calendar_event
def test_create_calendar_event(mock_build):
    mock_service = MagicMock()
    mock_service.events.return_value.insert.return_value.execute.return_value = {'id': 'event_id'}
    result = create_calendar_event("calendar_id", {'summary': 'Test'}, mock_service)
    assert result['id'] == 'event_id'
    mock_service.events.return_value.insert.assert_called_once()

# Test get_calendar_details
def test_get_calendar_details(mock_build):
    mock_service = MagicMock()
    mock_service.calendars.return_value.get.return_value.execute.return_value = {'id': 'calendar_id'}
    result = get_calendar_details("calendar_id", mock_service)
    assert result['id'] == 'calendar_id'
    mock_service.calendars.return_value.get.assert_called_once()
