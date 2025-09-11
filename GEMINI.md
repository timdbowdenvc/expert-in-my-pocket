# Gemini Code Assistant Context

This document provides context for the Gemini Code Assistant to understand the project structure, technologies, and development conventions.

## Project Overview

This is a full-stack application with a Python backend and a Next.js frontend.

*   **Backend:** The backend is a Python application using the Google ADK (Agent Development Kit) to create a goal-planning LLM agent. It uses `vertexai` for interacting with Google Cloud's AI services and `python-dotenv` for managing environment variables.
*   **Frontend:** The frontend is a Next.js 15 application with React 19. It uses TailwindCSS for styling and `shadcn/ui` for UI components. It provides a chat interface to interact with the backend agent.
*   **Architecture:** The frontend communicates with the backend via a streaming SSE endpoint. The application can be configured to run against a local backend or a deployed Vertex AI Agent Engine.

## Building and Running

### Prerequisites

*   Python 3.10–3.12
*   Node.js 18+
*   `uv` (installed automatically by the Makefile if missing)
*   Google Cloud SDK (for cloud deployment)

### Installation

```bash
make install
```

This will install both the Python dependencies from `pyproject.toml` and the Node.js dependencies from `nextjs/package.json`.

### Development

To run both the backend and frontend development servers:

```bash
make dev
```

The frontend will be available at `http://localhost:3000` and the backend at `http://127.0.0.1:8000`.

To run the backend and frontend separately:

```bash
# Run the Python backend
make dev-backend

# Run the Next.js frontend
make dev-frontend
```

### Testing

*   **Python:**
    ```bash
    make lint
    ```
    This will run `ruff` for linting and `mypy` for type-checking.

*   **Next.js:**
    ```bash
    npm --prefix nextjs run lint
    npm --prefix nextjs run test
    ```

## Deployment

### Backend (Vertex AI Agent Engine)

To deploy the Python agent to Vertex AI Agent Engine:

```bash
make deploy-adk
```

This will package the application and deploy it using the `app/agent_engine_app.py` script.

### Frontend (Vercel)

The frontend is designed to be deployed to Vercel. See `NEXTJS_VERCEL_DEPLOYMENT_GUIDE.md` for detailed instructions.

## Development Conventions

*   **Python:**
    *   The Python code is located in the `app` directory.
    *   The main agent logic is in `app/agent.py`.
    *   Configuration is handled in `app/config.py`.
    *   The project uses `ruff` for formatting and linting, and `mypy` for type checking.

*   **Next.js:**
    *   The frontend code is in the `nextjs` directory.
    *   The main application page is `nextjs/src/app/page.tsx`.
    *   API routes are in `nextjs/src/app/api`.
    *   The project uses ESLint for linting and Jest for testing.
