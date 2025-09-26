install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $HOME/.local/bin/env; }
	uv sync --all-extras && npm --prefix nextjs install

dev:
	make -j 3 dev-backend & make dev-frontend & make dev-mcp

dev-backend:
	uv run adk api_server . --allow_origins="*"

dev-frontend:
	npm --prefix nextjs run dev

dev-mcp:
	uvicorn mcp_server.main:app --reload --port 8001

adk-web:
	uv run adk web app/agent --port 8501

adk-web-test:
	make adk-web & make dev-mcp

lint:
	uv run codespell
	uv run ruff check . --fix
	uv run ruff format .
	uv run mypy .

# Deploy the agent remotely
deploy-adk:
	# Export dependencies to requirements file using uv export.
	uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > .requirements.txt 2>/dev/null || \
	uv export --no-hashes --no-header --no-dev --no-emit-project > .requirements.txt && uv run app/agent_engine_app.py
