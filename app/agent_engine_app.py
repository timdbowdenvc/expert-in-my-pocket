"""
Agent Engine App - Deploy your agent to Google Cloud

This file contains the logic to deploy your agent to Vertex AI Agent Engine.
"""

import copy
import datetime
import json
import os
from pathlib import Path
from typing import Any, TypedDict

import vertexai
from google.adk.artifacts import GcsArtifactService
from google.cloud import logging as google_cloud_logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

from app.agents.rag_agent.agent import root_agent as rag_agent
from app.agents.research_agent.agent import root_agent as research_agent
from app.agents.research_agent.config import get_deployment_config
from app.utils.gcs import create_bucket_if_not_exists
from app.utils.tracing import CloudTraceLoggingSpanExporter
from app.utils.typing import Feedback


class AgentDeploymentConfig(TypedDict):
    agent: Any
    name: str
    description: str
    packages: list[str]


class AgentEngineApp(AdkApp):
    """
    ADK Application wrapper for Agent Engine deployment.

    This class extends the base ADK app with logging, tracing, and feedback capabilities.
    """

    def set_up(self) -> None:
        """Set up logging and tracing for the agent engine app."""
        super().set_up()
        logging_client = google_cloud_logging.Client()
        self.logger = logging_client.logger(__name__)
        provider = TracerProvider()
        processor = export.BatchSpanProcessor(
            CloudTraceLoggingSpanExporter(
                project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
                service_name=f"{config.deployment_name}-service",
            )
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        self.enable_tracing = True

    def register_feedback(self, feedback: dict[str, Any]) -> None:
        """Collect and log feedback from users."""
        feedback_obj = Feedback.model_validate(feedback)
        self.logger.log_struct(feedback_obj.model_dump(), severity="INFO")

    def register_operations(self) -> dict[str, list[str]]:
        """Register available operations for the agent."""
        operations = super().register_operations()
        operations[""] = operations[""] + ["register_feedback"]
        return operations

    def clone(self) -> "AgentEngineApp":
        """Create a copy of this application."""
        template_attributes = self._tmpl_attrs

        return self.__class__(
            agent=copy.deepcopy(template_attributes["agent"]),
            enable_tracing=bool(template_attributes.get("enable_tracing", False)),
            session_service_builder=template_attributes.get("session_service_builder"),
            artifact_service_builder=template_attributes.get(
                "artifact_service_builder"
            ),
            env_vars=template_attributes.get("env_vars"),
        )


def deploy_agent(
    agent: Any, agent_name: str, agent_description: str, extra_packages: list[str]
) -> agent_engines.AgentEngine:
    """
    Deploy a single agent to Vertex AI Agent Engine.

    Args:
        agent: The agent instance to deploy.
        agent_name: The display name for the agent.
        agent_description: A description for the agent.
        extra_packages: A list of extra packages to include in the deployment.

    Returns:
        The deployed agent engine instance.
    """
    print(f"🚀 Starting deployment for agent: {agent_name}...")

    # Step 1: Get deployment configuration
    deployment_config = get_deployment_config()
    print(f"📋 Project: {deployment_config.project}")
    print(f"📋 Location: {deployment_config.location}")
    print(f"📋 Staging bucket: {deployment_config.staging_bucket}")

    # Step 2: Set up environment variables for the deployed agent
    env_vars = {"NUM_WORKERS": "1"}

    # Step 3: Create required Google Cloud Storage buckets
    artifacts_bucket_name = f"{deployment_config.project}-{agent_name}-logs-data"
    print(f"📦 Creating artifacts bucket: {artifacts_bucket_name}")
    create_bucket_if_not_exists(
        bucket_name=artifacts_bucket_name,
        project=deployment_config.project,
        location=deployment_config.location,
    )

    # Step 4: Initialize Vertex AI for deployment
    vertexai.init(
        project=deployment_config.project,
        location=deployment_config.location,
        staging_bucket=f"gs://{deployment_config.staging_bucket}",
    )

    # Step 5: Read requirements file
    with open(deployment_config.requirements_file) as f:
        requirements = f.read().strip().split("\n")

    # Step 6: Create the agent engine app
    agent_engine = AgentEngineApp(
        agent=agent,
        artifact_service_builder=lambda: GcsArtifactService(
            bucket_name=artifacts_bucket_name
        ),
    )

    # Step 7: Configure the agent for deployment
    agent_config = {
        "agent_engine": agent_engine,
        "display_name": agent_name,
        "description": agent_description,
        "extra_packages": extra_packages,
        "env_vars": env_vars,
        "requirements": requirements,
    }

    # Step 8: Deploy or update the agent
    existing_agents = list(agent_engines.list(filter=f"display_name='{agent_name}'"))

    if existing_agents:
        print(f"🔄 Updating existing agent: {agent_name}")
        remote_agent = existing_agents[0].update(**agent_config)
    else:
        print(f"🆕 Creating new agent: {agent_name}")
        remote_agent = agent_engines.create(**agent_config)

    # Step 9: Save deployment metadata
    metadata = {
        "remote_agent_engine_id": remote_agent.resource_name,
        "deployment_timestamp": datetime.datetime.now().isoformat(),
        "agent_name": agent_name,
        "project": deployment_config.project,
        "location": deployment_config.location,
    }

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    metadata_file = logs_dir / f"deployment_metadata_{agent_name}.json"

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Agent {agent_name} deployed successfully!")
    print(f"📄 Deployment metadata saved to: {metadata_file}")
    print(f"🆔 Agent Engine ID: {remote_agent.resource_name}")

    return remote_agent


def deploy_all_agents() -> None:
    """Deploys all agents defined in the application."""
    agents_to_deploy: list[AgentDeploymentConfig] = [
        {
            "agent": research_agent,
            "name": "research-agent",
            "description": "A research agent that can browse the web and generate reports.",
            "packages": ["./app/agents/research_agent", "./app/utils"],
        },
        {
            "agent": rag_agent,
            "name": "rag-agent",
            "description": "A RAG agent that can answer questions about documents.",
            "packages": ["./app/agents/rag_agent", "./app/utils"],
        },
    ]

    for agent_config in agents_to_deploy:
        deploy_agent(
            agent=agent_config["agent"],
            agent_name=agent_config["name"],
            agent_description=agent_config["description"],
            extra_packages=agent_config["packages"],
        )


if __name__ == "__main__":
    print(
        """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🤖 DEPLOYING AGENT TO VERTEX AI AGENT ENGINE 🤖         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    )

    deploy_all_agents()
