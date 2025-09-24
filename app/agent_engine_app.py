# Agent Engine App - Deploy your agent to Google Cloud

# This file contains the logic to deploy your agent to Vertex AI Agent Engine.

import copy
import datetime
import json
import os
import logging
from pathlib import Path
from typing import Any, TypedDict

import vertexai
from dotenv import load_dotenv
from google.adk.artifacts import GcsArtifactService
from google.cloud import logging as google_cloud_logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
from google.cloud.iam_admin_v1 import IAMClient
from google.cloud.iam_admin_v1.types import ServiceAccount, CreateServiceAccountRequest
from google.iam.v1.iam_policy_pb2 import SetIamPolicyRequest
from google.api_core.exceptions import AlreadyExists
from google.iam.v1.policy_pb2 import Binding
from google.api_core.exceptions import NotFound

from app.agent.research_agent.config import get_deployment_config
from app.agent.root_agent.agent import root_agent
from app.utils.gcs import create_bucket_if_not_exists
from app.utils.tracing import CloudTraceLoggingSpanExporter
from app.utils.typing import Feedback

from google.cloud import resourcemanager_v3
from google.api_core.exceptions import NotFound
from google.iam.v1 import policy_pb2



# Load environment variables from .env file in the project root
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


class AgentDeploymentConfig(TypedDict):
    agent: Any
    name: str
    description: str
    packages: list[str]
    agent_id: str | None


class AgentEngineApp(AdkApp):
    """
    ADK Application wrapper for Agent Engine deployment.

    This class extends the base ADK app with logging, tracing, and feedback capabilities.
    """

    def __init__(self, agent_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.agent_name = agent_name

    def set_up(self) -> None:
        """Set up logging and tracing for the agent engine app."""
        super().set_up()
        logging_client = google_cloud_logging.Client()
        self.logger = logging_client.logger(__name__)
        # provider = TracerProvider()
        # processor = export.BatchSpanProcessor(
        #     CloudTraceLoggingSpanExporter(
        #         project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        #         service_name=f"{self.agent_name}-service",
        #     )
        # )
        # provider.add_span_processor(processor)
        # trace.set_tracer_provider(provider)
        self.enable_tracing = False

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
            agent_name=self.agent_name,
            agent=copy.deepcopy(template_attributes["agent"]),
            enable_tracing=bool(template_attributes.get("enable_tracing", False)),
            session_service_builder=template_attributes.get("session_service_builder"),
            artifact_service_builder=template_attributes.get(
                "artifact_service_builder"
            ),
            env_vars=template_attributes.get("env_vars"),
        )



def _create_service_account(project_id: str, service_account_id: str) -> str:
    """
    Creates a service account in the given project if it doesn't already exist.
    
    Args:
        project_id: GCP project ID.
        service_account_id: Unique service account ID (without domain).
        
    Returns:
        The email address of the created or existing service account.
    """
    client = IAMClient()
    parent = f"projects/{project_id}"

    try:
        # Create service account
        request = CreateServiceAccountRequest(
            name=parent,
            account_id=service_account_id,
            service_account=ServiceAccount(display_name=service_account_id),
        )
        service_account = client.create_service_account(request=request)
        print(f"✅ Created service account: {service_account.email}")
        return service_account.email

    except AlreadyExists:
        # If it already exists, fetch the existing service account
        sa_name = f"projects/{project_id}/serviceAccounts/{service_account_id}@{project_id}.iam.gserviceaccount.com"
        existing_sa = client.get_service_account(name=sa_name)
        print(f"ℹ️ Service account already exists: {existing_sa.email}")
        return existing_sa.email


def _grant_service_account_roles(project_id: str, service_account_email: str, roles: list[str]):
    """
    Grants project-level roles to a service account using Cloud Resource Manager API.
    """
    client = resourcemanager_v3.ProjectsClient()
    project_name = f"projects/{project_id}"

    try:
        policy = client.get_iam_policy(request={"resource": project_name})
    except NotFound:
        raise ValueError(f"Project {project_id} not found. Cannot grant roles.")

    modified = False
    member = f"serviceAccount:{service_account_email}"

    # Convert bindings to dict-like lookup by role
    bindings_by_role = {b.role: b for b in policy.bindings}

    for role in roles:
        if role in bindings_by_role:
            if member not in bindings_by_role[role].members:
                bindings_by_role[role].members.append(member)
                modified = True
        else:
            new_binding = policy_pb2.Binding(role=role, members=[member])
            policy.bindings.append(new_binding)
            modified = True

    if modified:
        client.set_iam_policy(request={"resource": project_name, "policy": policy})
        print(f"✅ Granted roles {roles} to {service_account_email}")
    else:
        print(f"ℹ️ {service_account_email} already has all requested roles.")

def deploy_agent(
    agent: Any,
    agent_name: str,
    agent_description: str,
    extra_packages: list[str],
    agent_id: str | None = None,
) -> agent_engines.AgentEngine:
    """
    Deploy a single agent to Vertex AI Agent Engine.

    Args:
        agent: The agent instance to deploy.
        agent_name: The display name for the agent.
        agent_description: A description for the agent.
        extra_packages: A list of extra packages to include in the deployment.
        agent_id: The resource name of the agent to update.

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
    mcp_server_url = os.environ.get("REMOTE_MCP_SERVER_URL")
    if not mcp_server_url:
        raise ValueError(
            "REMOTE_MCP_SERVER_URL environment variable not set in .env file."
        )

    env_vars = {
        "NUM_WORKERS": "1",
        "MCP_SERVER_URL": mcp_server_url,
        "ENVIRONMENT": "cloud",
        "SERVICE_ACCOUNT_EMAIL": "ai-agent-account@timberyard-brain.iam.gserviceaccount.com",
    }

    # Step 3: Create required Google Cloud Storage buckets
    artifacts_bucket_name = f"{deployment_config.project}-{agent_name}-logs-data"
    print(f"📦 Creating artifacts bucket: {artifacts_bucket_name}")
    create_bucket_if_not_exists(
        bucket_name=artifacts_bucket_name,
        project=deployment_config.project,
        location=deployment_config.location,
    )

    # Create and configure service account for the agent
    service_account_id = f"ai-agent-account"
    service_account_email = _create_service_account(
        deployment_config.project, service_account_id
    )
    _grant_service_account_roles(
        deployment_config.project,
        service_account_email,
        [
            "roles/aiplatform.user",
        ],
    )
    print(f"Using service account: {service_account_email} for agent deployment.")

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
        agent_name=agent_name,
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
    if agent_id:
        print(f"🔄 Updating existing agent by ID: {agent_id}")
        agent_to_update = agent_engines.get(agent_id)
        remote_agent = agent_to_update.update(**agent_config)
    else:
        existing_agents = list(
            agent_engines.list(filter=f"display_name='{agent_name}'")
        )

        if existing_agents:
            print(f"🔄 Updating existing agent by name: {agent_name}")
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
            "agent": root_agent,
            "name": "root_agent",
            "description": "A root agent that orchestrates sub-agents.",
            "packages": [
                "./app/agent/root_agent",
                "./app/agent/rag_agent",
                "./app/agent/slides_agent",
                "./app/utils",
            ],
            "agent_id": None,
        },
    ]

    for agent_config in agents_to_deploy:
        deploy_agent(
            agent=agent_config["agent"],
            agent_name=agent_config["name"],
            agent_description=agent_config["description"],
            extra_packages=agent_config["packages"],
            agent_id=agent_config.get("agent_id"),
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
