import os

import requests
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def generate_presentation(
    title: str, slides: list[dict], email: str, tool_context: ToolContext
) -> str:
    """
    Generates a Google Slides presentation.

    Args:
        title (str): The title of the presentation.
        slides (list[dict]): A list of slides to create. Each slide should be a dictionary with "title" and "content" keys.
        email (str): The user's email address to share the presentation with.
        tool_context (ToolContext): The tool context, which contains user information.
    """
    mcp_server_url = os.environ.get("MCP_SERVER_URL", "http://localhost:8001")

    response = requests.post(
        f"{mcp_server_url}/generate_slides",
        json={"title": title, "slides": slides, "email": email},
    )
    response.raise_for_status()
    return response.json()["presentation_url"]


slides_agent = Agent(
    name="slides_agent",
    model="gemini-2.5-flash",
    description="An agent that can create Google Slides presentations.",
    tools=[generate_presentation],
    instruction="""
    You are an agent that can create Google Slides presentations.
    Use the `generate_presentation` tool to create a presentation with the given title and slides.
    You must ask the user for their email address before using the tool.
    The tool will return the URL of the created presentation.
    """,
)
