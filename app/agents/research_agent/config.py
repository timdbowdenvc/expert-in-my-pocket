from dataclasses import dataclass

@dataclass
class DeploymentConfig:
    project: str
    location: str
    staging_bucket: str
    requirements_file: str

def get_deployment_config() -> DeploymentConfig:
    """Returns the deployment configuration."""
    return DeploymentConfig(
        project="t-level-assistant",
        location="europe-west4",
        staging_bucket="t-level-assistant-adk-staging",
        requirements_file=".requirements.txt",
    )
