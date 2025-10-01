FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock to leverage uv's caching
COPY pyproject.toml uv.lock ./ 

# Install dependencies
RUN uv sync

# Copy the rest of the application code
COPY mcp_server/schedule_mcp ./mcp_server/schedule_mcp

# Set environment variables for Google OAuth credentials
# In a production environment, consider using Workload Identity or similar secure methods
ENV GOOGLE_CLIENT_ID=<your-google-client-id>
ENV GOOGLE_CLIENT_SECRET=<your-google-client-secret>
ENV REDIRECT_URI=http://localhost:8000/oauth2callback

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "mcp_server.schedule_mcp.main:app", "--host", "0.0.0.0", "--port", "8000"]