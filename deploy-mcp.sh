#!/bin/bash

# Exit on error
set -e

# Get the project ID from gcloud config
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="mcp-slides-server"
REGION="us-central1" # Or your preferred region

# Build the container image using Cloud Build
gcloud builds submit . --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Deploy the container to Cloud Run
gcloud run deploy "${SERVICE_NAME}" \
  --image="gcr.io/${PROJECT_ID}/${SERVICE_NAME}" \
  --platform="managed" \
  --region="${REGION}" \
  --allow-unauthenticated \
  --project="${PROJECT_ID}"

echo "✅ Deployment complete."
echo "🚀 Your service is available at: $(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)')"
