# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependency management files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN pip install uv
RUN uv sync --all-extras

# Copy the MCP server code
COPY mcp_server/ ./mcp_server

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["uv", "run", "uvicorn", "mcp_server.main:app", "--host", "0.0.0.0", "--port", "8080"]
