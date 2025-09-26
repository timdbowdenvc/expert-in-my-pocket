import pytest
from unittest.mock import patch, MagicMock
from app.agent.root_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

@pytest.mark.asyncio
@patch('app.agent.seo_agent.tools.analyze_url.analyze_url_for_seo')
async def test_seo_agent_integration(mock_analyze_url_for_seo):
    mock_analyze_url_for_seo.return_value = """# SEO Analysis Report\n\n## Summary\nThis is a mock summary."""

    session_service = InMemorySessionService()
    runner = Runner(app_name="test_app", agent=root_agent, session_service=session_service)

    # Simulate user input
    user_id = "test_user_id"
    session_id = "test_session_id"
    user_input_text = "/seo https://www.example.com"
    text_part = Part(text=user_input_text)
    new_message = Content(role="user", parts=[text_part])

    # Create a session
    await session_service.create_session(app_name="test_app", user_id=user_id, session_id=session_id)

    # Run the agent with the simulated input and iterate over the results
    response_text = ""
    async for chunk in runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message):
        if chunk.text: # Assuming the response chunks have a 'text' attribute
            response_text += chunk.text

    # Assert that the seo_agent's tool was called with the correct URL
    mock_analyze_url_for_seo.assert_called_once_with(url="https://www.example.com")

    # Assert that the root_agent set the response with the mock analysis report
    assert "This is a mock summary." in response_text
