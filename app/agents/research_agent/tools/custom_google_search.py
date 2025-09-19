import logging
from google.adk.tools import google_search
from vertexai import rag

def custom_google_search(query: str) -> dict:
    """
    A wrapper around the built-in google_search tool that adds logging and a dummy RAG API call.
    """
    logging.info(f"Executing custom_google_search with query: {query}")
    try:
        # Dummy call to the RAG API to ensure the agent works in the cloud.
        rag.list_corpora(page_size=1)
        logging.info("Successfully made a dummy call to the RAG API.")

        # Real call to the google_search tool.
        result = google_search(query=query)
        logging.info(f"custom_google_search result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error in custom_google_search: {e}", exc_info=True)
        raise
