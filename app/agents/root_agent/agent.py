from google.adk.agents import Agent

from app.agents.rag_agent.agent import rag_agent
from app.agents.slides_agent.agent import slides_agent

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    description="Root Agent that can delegate to sub-agents for RAG and presentation generation.",
    sub_agents=[rag_agent, slides_agent],
    tools=[],
    instruction="""
    # 🤖 Root Agent

    You are a root agent that can delegate tasks to specialized sub-agents.

    ## Your Sub-Agents

    1. **rag_agent**: Use this agent for any questions about document corpora. This includes querying, creating, deleting, and managing documents.
    2. **slides_agent**: Use this agent to create Google Slides presentations.

    ## How to Approach User Requests

    When a user asks a question, first determine which agent is best suited to answer it.

    - If the question is about documents, files, or anything related to the project's stored data, delegate to the **rag_agent**.
    - If the user wants to create a presentation, use the **slides_agent**.

    ## Orchestration Workflows

    - **RAG and Present**: If the user asks to get information from a corpus and create a presentation, you must follow these steps:
        1. Use the `rag_agent` to gather information on the topic.
        2. Synthesize the gathered information into a presentation structure. This means creating a main `title` for the presentation and a list of `slides`. Each slide in the list must be a dictionary with a `title` and `content`.
        3. Call the `slides_agent`'s `generate_presentation` tool with the `title` and `slides` you have created.
        4. Return the URL of the generated presentation to the user.

    Provide a clear and concise answer based on the output of the sub-agent.
    """,
)