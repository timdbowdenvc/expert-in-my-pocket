# Schedule MCP Server

This is a Microservice Control Plane (MCP) server responsible for inserting appointments into Google Calendar based on requests.

## API Endpoint

-   **POST `/create-appointment`**: Creates a new Google Calendar appointment.

## Local Development

Refer to `quickstart.md` in the feature specification directory for local setup and testing instructions.

## Deployment to Google Cloud Run

This service is designed to be deployed on Google Cloud Run.

### Prerequisites

-   Google Cloud SDK installed and configured.
-   A GCP project with billing enabled.
-   **Google Calendar API** enabled in your GCP project.
-   OAuth 2.0 Client ID (Web application type) with `client_id` and `client_secret`.
-   Authorized Redirect URIs configured for your OAuth client.

### Steps

1.  **Build the Docker Image**:
    Navigate to the `mcp_server` directory and build the Docker image:
    ```bash
    gcloud builds submit --tag gcr.io/<your-gcp-project-id>/schedule-mcp-server
    ```
    Replace `<your-gcp-project-id>` with your actual GCP project ID.

2.  **Deploy to Cloud Run**:
    Deploy the built image to Google Cloud Run:
    ```bash
    gcloud run deploy schedule-mcp-server \
      --image gcr.io/<your-gcp-project-id>/schedule-mcp-server \
      --platform managed \
      --region <your-gcp-region> \
      --allow-unauthenticated \
      --set-env-vars GOOGLE_CLIENT_ID=<your-client-id>,GOOGLE_CLIENT_SECRET=<your-client-secret>,REDIRECT_URI=<your-redirect-uri> \
      --update-secrets=refresh-token=<path-to-local-refresh-token-file>
    ```
    -   Replace `<your-gcp-project-id>` with your GCP project ID.
    -   Replace `<your-gcp-region>` with your desired GCP region (e.g., `us-central1`).
    -   Replace `<your-client-id>`, `<your-client-secret>`, and `<your-redirect-uri>` with your OAuth client credentials.
    -   Replace `<path-to-local-refresh-token-file>` with the path to a file containing the user's refresh token on your local machine. Cloud Run will securely mount this as a secret.

3.  **Verify Deployment**:
    After deployment, Cloud Run will provide a service URL. You can access the `/health` endpoint to verify the service is running:
    ```bash
    curl <cloud-run-service-url>/health
    ```
    You should receive `{"status": "ok"}`.