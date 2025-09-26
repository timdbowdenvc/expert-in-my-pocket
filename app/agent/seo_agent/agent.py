from google.adk.agents import Agent
from app.agent.seo_agent.tools.analyze_url import analyze_url_for_seo

def create_seo_agent():
    return Agent(
        name="seo_agent",
        model="gemini-2.5-flash",
        description="An agent that can analyze a URL for SEO optimizations.",
        tools=[analyze_url_for_seo],
        instruction="""
        # 📈 SEO Agent

        You are an expert SEO agent.
        Your goal is to analyze a given URL and provide a report with SEO optimization suggestions.

        ## How to Approach User Requests

        When a user provides a URL, use the `analyze_url_for_seo` tool to perform the analysis.
        Present the returned markdown report to the user.
        """,
    )

seo_agent = create_seo_agent()