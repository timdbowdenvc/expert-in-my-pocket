import pytest
from unittest.mock import MagicMock, patch
import os

# Assuming google_slides_client.py is in the same package
from mcp_server.slides_mcp.google_slides_client import (
    get_slides_service,
    get_drive_service,
    create_presentation,
    get_file_by_name,
    batch_update_presentation,
    apply_layout_to_slide,
    get_available_layouts,
    add_text_to_slide,
    add_image_to_slide
)

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/mock_creds.json",
        "GOOGLE_DRIVE_SHARED_FOLDER_ID": "mock_shared_folder_id",
        "GOOGLE_SLIDES_TEMPLATE_FOLDER_ID": "mock_template_folder_id",
    }):
        yield

# Mock googleapiclient.discovery.build
@pytest.fixture
def mock_build():
    with patch('mcp_server.slides_mcp.google_slides_client.build') as mock_build_func:
        yield mock_build_func

# Test get_slides_service
def test_get_slides_service(mock_build):
    mock_service = MagicMock()
    mock_build.return_value = mock_service
    service = get_slides_service()
    assert service == mock_service
    mock_build.assert_called_once_with('slides', 'v1', credentials=service.credentials)

# Test get_drive_service
def test_get_drive_service(mock_build):
    mock_service = MagicMock()
    mock_build.return_value = mock_service
    service = get_drive_service()
    assert service == mock_service
    mock_build.assert_called_once_with('drive', 'v3', credentials=service.credentials)

# Test create_presentation (blank)
def test_create_presentation_blank(mock_build):
    mock_slides_service = MagicMock()
    mock_drive_service = MagicMock()
    mock_slides_service.presentations.return_value.create.return_value.execute.return_value = {'presentationId': 'new_pres_id'}
    mock_drive_service.files.return_value.get.return_value.execute.return_value = {'parents': ['root']}
    mock_drive_service.files.return_value.update.return_value.execute.return_value = {}

    result = create_presentation("Test Title", mock_drive_service, mock_slides_service, "parent_folder_id")
    assert result['presentationId'] == 'new_pres_id'
    mock_slides_service.presentations.return_value.create.assert_called_once()
    mock_drive_service.files.return_value.update.assert_called_once()

# Test create_presentation (from source)
def test_create_presentation_from_source(mock_build):
    mock_slides_service = MagicMock()
    mock_drive_service = MagicMock()
    mock_drive_service.files.return_value.copy.return_value.execute.return_value = {'id': 'copied_pres_id'}
    mock_slides_service.presentations.return_value.get.return_value.execute.return_value = {'presentationId': 'copied_pres_id'}
    mock_drive_service.files.return_value.get.return_value.execute.return_value = {'parents': ['root']}
    mock_drive_service.files.return_value.update.return_value.execute.return_value = {}

    result = create_presentation("Copied Title", mock_drive_service, mock_slides_service, "parent_folder_id", source_presentation_id="source_pres_id")
    assert result['presentationId'] == 'copied_pres_id'
    mock_drive_service.files.return_value.copy.assert_called_once()
    mock_slides_service.presentations.return_value.get.assert_called_once()
    mock_drive_service.files.return_value.update.assert_called_once()

# Test get_file_by_name
def test_get_file_by_name(mock_build):
    mock_drive_service = MagicMock()
    mock_drive_service.files.return_value.list.return_value.execute.return_value = {'files': [{'id': 'file_id', 'name': 'test_file'}]}
    result = get_file_by_name("test_file", mock_drive_service, "folder_id")
    assert result['id'] == 'file_id'
    mock_drive_service.files.return_value.list.assert_called_once()

# Test batch_update_presentation
def test_batch_update_presentation(mock_build):
    mock_slides_service = MagicMock()
    mock_slides_service.presentations.return_value.batchUpdate.return_value.execute.return_value = {'replies': []}
    result = batch_update_presentation("pres_id", [{}], mock_slides_service)
    assert result == {'replies': []}
    mock_slides_service.presentations.return_value.batchUpdate.assert_called_once()

# Test apply_layout_to_slide
def test_apply_layout_to_slide(mock_build):
    mock_slides_service = MagicMock()
    mock_slides_service.presentations.return_value.batchUpdate.return_value.execute.return_value = {'replies': []}
    result = apply_layout_to_slide("pres_id", "slide_id", "layout_id", mock_slides_service)
    assert result == {'replies': []}
    mock_slides_service.presentations.return_value.batchUpdate.assert_called_once()

# Test get_available_layouts
def test_get_available_layouts(mock_build):
    mock_slides_service = MagicMock()
    mock_slides_service.presentations.return_value.get.return_value.execute.return_value = {
        'layouts': [
            {'objectId': 'layout1_id', 'displayName': 'Layout 1'},
            {'objectId': 'layout2_id', 'displayName': 'Layout 2'},
        ]
    }
    result = get_available_layouts("pres_id", mock_slides_service)
    assert result == {'Layout 1': 'layout1_id', 'Layout 2': 'layout2_id'}
    mock_slides_service.presentations.return_value.get.assert_called_once()

# Test add_text_to_slide
def test_add_text_to_slide(mock_build):
    mock_slides_service = MagicMock()
    mock_slides_service.presentations.return_value.batchUpdate.return_value.execute.return_value = {'replies': []}
    result = add_text_to_slide("pres_id", "slide_id", "Some Text", mock_slides_service)
    assert result == {'replies': []}
    mock_slides_service.presentations.return_value.batchUpdate.assert_called_once()

# Test add_image_to_slide
def test_add_image_to_slide(mock_build):
    mock_slides_service = MagicMock()
    mock_slides_service.presentations.return_value.batchUpdate.return_value.execute.return_value = {'replies': []}
    result = add_image_to_slide("pres_id", "slide_id", "http://example.com/image.png", mock_slides_service)
    assert result == {'replies': []}
    mock_slides_service.presentations.return_value.batchUpdate.assert_called_once()
