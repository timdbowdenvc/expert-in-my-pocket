from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


@dataclass
class DeploymentConfig:
    project: str
    location: str
    staging_bucket: str
    requirements_file: str


def get_deployment_config() -> DeploymentConfig:
    """Returns the deployment configuration."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT not found in environment variables.")
    return DeploymentConfig(
        project=project_id,
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4"),
        staging_bucket=f"{project_id}-adk-staging",
        requirements_file=".requirements.txt",
    )
