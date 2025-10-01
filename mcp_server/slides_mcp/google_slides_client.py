import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive'
]

def get_slides_service():
    """Authenticates and returns a Google Slides service object."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    service = build('slides', 'v1', credentials=creds)
    return service

def get_drive_service():
    """Authenticates and returns a Google Drive service object."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def create_presentation(title: str, drive_service, slides_service, parent_folder_id: str = None, source_presentation_id: str = None):
    """Creates a new presentation with the given title in the specified folder."""
    if source_presentation_id:
        # Copy the source presentation
        copied_file = drive_service.files().copy(fileId=source_presentation_id, body={'name': title}).execute()
        presentation_id = copied_file.get('id')
        new_presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
    else:
        # Create a new blank presentation
        presentation = {
            'title': title
        }
        new_presentation = slides_service.presentations().create(body=presentation).execute()
        presentation_id = new_presentation.get('presentationId')

        # Move to the specified folder if parent_folder_id is provided
        if parent_folder_id:
            file_id = presentation_id
            # Retrieve the existing parents to remove them
            file = drive_service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            drive_service.files().update(
                fileId=file_id,
                addParents=parent_folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()

        return new_presentation
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise

def batch_update_presentation(presentation_id: str, requests: list, slides_service):
    """Performs a batch update on the presentation."""
    body = {
        'requests': requests
    }
    try:
        response = slides_service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise

def get_file_by_name(name: str, drive_service, parent_folder_id: str = None):
    """Searches for a file by name within a specific folder."""
    query = f"name = '{name}' and trashed = false"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"

    try:
        response = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = response.get('files', [])
        if files:
            return files[0] # Return the first match
        return None
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise

def add_image_to_slide(presentation_id: str, slide_id: str, image_url: str, slides_service, x: float = None, y: float = None, width: float = None, height: float = None):
    """Adds an image to a slide."""
    requests = [
        {
            'createImage': {
                'url': image_url,
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': width or 200, 'unit': 'PT'},
                        'height': {'magnitude': height or 200, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x or 100,
                        'translateY': y or 100,
                        'unit': 'PT'
                    }
                }
            }
        }
    ]
    return batch_update_presentation(presentation_id, requests, slides_service)

def add_text_to_slide(presentation_id: str, slide_id: str, text: str, slides_service, object_id: str = None, x: float = None, y: float = None, width: float = None, height: float = None):
    """Adds a text box to a slide and inserts text."""
    requests = []
    if not object_id:
        # Create a new text box if no object_id is provided
        object_id = f'textBox_{slide_id}_{len(text)}' # Generate a unique ID
        create_shape_request = {
            'createShape': {
                'objectId': object_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': width or 200, 'unit': 'PT'},
                        'height': {'magnitude': height or 50, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x or 100,
                        'translateY': y or 100,
                        'unit': 'PT'
                    }
                }
            }
        }
        requests.append(create_shape_request)

    insert_text_request = {
        'insertText': {
            'objectId': object_id,
            'insertionIndex': 0,
            'text': text
        }
    }
    requests.append(insert_text_request)

    return batch_update_presentation(presentation_id, requests, slides_service)

def get_available_layouts(presentation_id: str, slides_service):
    """Retrieves available layouts from a presentation."""
    try:
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        layouts = presentation.get('layouts', [])
        return {layout['displayName']: layout['objectId'] for layout in layouts}
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise

def apply_layout_to_slide(presentation_id: str, slide_id: str, layout_id: str, slides_service):
    """Applies a specific layout to a given slide."""
    requests = [
        {
            'updateSlideProperties': {
                'objectId': slide_id,
                'slideProperties': {
                    'slideLayoutObjectId': layout_id
                },
                'fields': 'slideLayoutObjectId'
            }
        }
    ]
    return batch_update_presentation(presentation_id, requests, slides_service)

def copy_file(file_id: str, new_title: str, drive_service, parent_folder_id: str = None):
    """Copies a file in Google Drive."""
    copy_body = {'title': new_title}
    if parent_folder_id:
        copy_body['parents'] = [{'id': parent_folder_id}]

    try:
        copied_file = drive_service.files().copy(fileId=file_id, body=copy_body).execute()
        return copied_file
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise
