# Data Model for Agent Deployment with Service Account

## System Architecture
- The existing deployment script (`app/agent_engine_app.py`) will be modified.
- A new function or modification to `deploy_agent` will handle service account creation/specification.
- Google Cloud IAM API will be used for service account management.

## Data Model
- No new complex data models are required. The existing `DeploymentConfig` will be extended to include service account information.

## API Contracts
- No new external API contracts are needed. The existing Google Cloud IAM API will be used.
