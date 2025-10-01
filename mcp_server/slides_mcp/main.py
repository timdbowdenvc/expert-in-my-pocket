from fastapi import FastAPI, HTTPException, status
from pydantic import ValidationError
from .models import PresentationRequest
from .google_slides_client import get_slides_service, get_drive_service, create_presentation, get_file_by_name, apply_layout_to_slide, get_available_layouts, add_text_to_slide, add_image_to_slide
import os
from datetime import datetime
from googleapiclient.errors import HttpError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

@app.get("/health")
async def health_check():
    logging.info("Health check requested.")
    return {"status": "ok"}

@app.post("/create-presentation", status_code=status.HTTP_200_OK)
async def create_presentation_endpoint(request: PresentationRequest):
    logging.info(f"Received request to create presentation: {request.title}")
    try:
        slides_service = get_slides_service()
        drive_service = get_drive_service()

        # Naming convention: Supplied title suffixed with date.
        current_date = datetime.now().strftime("%Y-%m-%d")
        presentation_title = f"{request.title} {current_date}"

        # Get shared Google Drive folder ID from environment variable
        shared_folder_id = os.getenv("GOOGLE_DRIVE_SHARED_FOLDER_ID")
        if not shared_folder_id:
            logging.error("GOOGLE_DRIVE_SHARED_FOLDER_ID environment variable not configured.")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GOOGLE_DRIVE_SHARED_FOLDER_ID not configured.")

        template_folder_id = os.getenv("GOOGLE_SLIDES_TEMPLATE_FOLDER_ID")
        if not template_folder_id:
            logging.error("GOOGLE_SLIDES_TEMPLATE_FOLDER_ID environment variable not configured.")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GOOGLE_SLIDES_TEMPLATE_FOLDER_ID not configured.")

        # T012.1: Search for template presentation by human-readable template_id
        template_file = get_file_by_name(request.template_id, drive_service, template_folder_id)
        if not template_file:
            logging.warning(f"Template '{request.template_id}' not found in the specified template folder.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Template '{request.template_id}' not found in the specified template folder.")
        template_presentation_id = template_file['id']
        logging.info(f"Found template '{request.template_id}' with ID: {template_presentation_id}")

        new_presentation = create_presentation(presentation_title, drive_service, slides_service, shared_folder_id, source_presentation_id=template_presentation_id)
        presentation_id = new_presentation.get('presentationId')
        logging.info(f"Created new presentation with ID: {presentation_id}")

        # Get the object IDs of the slides in the new presentation
        slides = new_presentation.get('slides')

        # Get available layouts from the template presentation
        available_layouts = get_available_layouts(template_presentation_id, slides_service)

        for i, slide_request in enumerate(request.slides):
            target_layout_id = slide_request.layout_id
            if target_layout_id:
                if target_layout_id not in available_layouts.keys():
                    logging.warning(f"Layout '{target_layout_id}' not found in the template presentation.")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Layout '{target_layout_id}' not found in the template presentation.")
                target_layout_id = available_layouts[target_layout_id] # Get the objectId
            else:
                # T012.4: Handle default layout application if layout_id is not provided.
                # For now, use the first available layout as default if none specified.
                if available_layouts:
                    target_layout_id = list(available_layouts.values())[0] # Get the objectId of the first layout
                    logging.info(f"Using default layout: {target_layout_id}")
                else:
                    logging.warning("No layouts available in template and no layout_id provided. Skipping layout application for this slide.")
                    continue # Skip layout application for this slide

            if i < len(slides):
                slide_id = slides[i].get('objectId')
                apply_layout_to_slide(presentation_id, slide_id, target_layout_id, slides_service)
                logging.info(f"Applied layout '{target_layout_id}' to slide {slide_id}")

                # T013.1: Add text elements to slides
                for element in slide_request.elements:
                    if element.type == "text" and element.content:
                        add_text_to_slide(
                            presentation_id, 
                            slide_id, 
                            element.content, 
                            slides_service, 
                            x=element.position.x if element.position else None,
                            y=element.position.y if element.position else None,
                            width=element.position.width if element.position else None,
                            height=element.position.height if element.position else None
                        )
                        logging.info(f"Added text to slide {slide_id}")
                    elif element.type == "image" and element.image_url:
                        add_image_to_slide(
                            presentation_id,
                            slide_id,
                            element.image_url,
                            slides_service,
                            x=element.position.x if element.position else None,
                            y=element.position.y if element.position else None,
                            width=element.position.width if element.position else None,
                            height=element.position.height if element.position else None
                        )
                        logging.info(f"Added image to slide {slide_id}")
            else:
                logging.warning(f"Request has more slides ({len(request.slides)}) than initial presentation ({len(slides)}). Skipping content for extra slides.")
                pass

        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}"
        logging.info(f"Presentation successfully created at: {presentation_url}")

        return {"message": "Presentation created successfully.", "presentation_url": presentation_url}
    except ValidationError as e:
        logging.error(f"Validation error: {e.errors()}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
    except HttpError as e:
        if e.resp.status in [401, 403]:
            logging.error(f"Google API authentication/permission error: {e.resp.status} - {e.resp.reason}. Check service account credentials and permissions.")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Google API authentication/permission error: {e.resp.status} - {e.resp.reason}. Check service account credentials and permissions.")
        else:
            logging.error(f"Google API error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Google API error: {e}")
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create presentation: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/create-presentation", status_code=status.HTTP_200_OK)
async def create_presentation_endpoint(request: PresentationRequest):
    try:
        slides_service = get_slides_service()
        drive_service = get_drive_service()

        # Naming convention: Supplied title suffixed with date.
        current_date = datetime.now().strftime("%Y-%m-%d")
        presentation_title = f"{request.title} {current_date}"

        # Get shared Google Drive folder ID from environment variable
        shared_folder_id = os.getenv("GOOGLE_DRIVE_SHARED_FOLDER_ID")
        if not shared_folder_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GOOGLE_DRIVE_SHARED_FOLDER_ID not configured.")

        template_folder_id = os.getenv("GOOGLE_SLIDES_TEMPLATE_FOLDER_ID")
        if not template_folder_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GOOGLE_SLIDES_TEMPLATE_FOLDER_ID not configured.")

        # T012.1: Search for template presentation by human-readable template_id
        template_file = get_file_by_name(request.template_id, drive_service, template_folder_id)
        if not template_file:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Template '{request.template_id}' not found in the specified template folder.")
        template_presentation_id = template_file['id']

        new_presentation = create_presentation(presentation_title, drive_service, slides_service, shared_folder_id, source_presentation_id=template_presentation_id)
        presentation_id = new_presentation.get('presentationId')
        # Get the object IDs of the slides in the new presentation
        slides = new_presentation.get('slides')

        # Get available layouts from the template presentation
        available_layouts = get_available_layouts(template_presentation_id, slides_service)

        for i, slide_request in enumerate(request.slides):
            target_layout_id = slide_request.layout_id
            if target_layout_id:
                if target_layout_id not in available_layouts.keys():
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Layout '{target_layout_id}' not found in the template presentation.")
                target_layout_id = available_layouts[target_layout_id] # Get the objectId
            else:
                # T012.4: Handle default layout application if layout_id is not provided.
                # For now, use the first available layout as default if none specified.
                if available_layouts:
                    target_layout_id = list(available_layouts.values())[0] # Get the objectId of the first layout
                else:
                    # If no layouts are available, we can't apply a default.
                    # This might indicate an issue with the template or a need for a blank slide.
                    continue # Skip layout application for this slide

            if i < len(slides):
                slide_id = slides[i].get('objectId')
                apply_layout_to_slide(presentation_id, slide_id, target_layout_id, slides_service)

                # T013.1: Add text elements to slides
                for element in slide_request.elements:
                    if element.type == "text" and element.content:
                        add_text_to_slide(
                            presentation_id, 
                            slide_id, 
                            element.content, 
                            slides_service, 
                            x=element.position.x if element.position else None,
                            y=element.position.y if element.position else None,
                            width=element.position.width if element.position else None,
                            height=element.position.height if element.position else None
                        )
                    elif element.type == "image" and element.image_url:
                        add_image_to_slide(
                            presentation_id,
                            slide_id,
                            element.image_url,
                            slides_service,
                            x=element.position.x if element.position else None,
                            y=element.position.y if element.position else None,
                            width=element.position.width if element.position else None,
                            height=element.position.height if element.position else None
                        )
            else:
                # Handle case where request has more slides than template, or create new slides
                # This will be handled in T013
                pass

        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}"

        return {"message": "Presentation created successfully.", "presentation_url": presentation_url}
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
    except HttpError as e:
        if e.resp.status in [401, 403]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Google API authentication/permission error: {e.resp.status} - {e.resp.reason}. Check service account credentials and permissions.")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Google API error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create presentation: {e}")
