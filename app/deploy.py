import os
import vertexai

from dotenv import load_dotenv

from agents.rag_agent.agent import root_agent as rag_agent
from agents.research_agent.agent import root_agent as research_agent
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "t-level-assistant")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")
STAGING_BUCKET = "gs://" + os.environ.get("GOOGLE_CLOUD_STAGING_BUCKET", "t-level-research-agent-bucket")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = reasoning_engines.AdkApp(
    agent=rag_agent,
    enable_tracing=True,
)
print(f"Deploying {app} to remote")

remote_app = agent_engines.create(
    agent_engine=app,
    display_name="t_level_agent",
    description="T Level RAG Agent",
    requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
            "vertexai"
    ],
    extra_packages=[
        "./agents/rag_agent",
        "./utils"
    ],
)

print(f"Deployed")