# Expert In My Pocket Full-Stack Agent Constitution

## Core Principles

### I. Modular Architecture
- The system is divided into clear, independent components: a Next.js frontend, ADK Agents, and MCP Servers. This promotes a strong separation of concerns, making the system easier to understand, develop, and maintain.

### II. User-Centric Design
- The application shall be intuitive, responsive, and provide a seamless user experience. The primary goal of the frontend is to be a clear and effective interface to the power of the backend agents.

### III. Test-Driven Development (TDD) - NON-NEGOTIABLE
- All new features and bug fixes must begin with the creation of tests that verify the desired functionality or replicate the bug. The "Red-Green-Refactor" cycle is to be strictly followed. No production code is written without a failing test.

### IV. Cloud-Native Deployment
- The application is designed for and deployed on modern cloud platforms: Netlify for the frontend, and Google Cloud (Vertex AI, Cloud Run) for the backend services. All development practices should align with this deployment strategy.

### V. Clear and Concise Code
- Code should be easy to read, understand, and maintain. Follow the established coding style and conventions of the framework and language being used. Add comments only to explain *why* something is done, not *what* is being done.

## Design Principles

- **Modern and Clean UI:** The user interface will adhere to a modern design aesthetic with a clean and uncluttered layout. We will leverage TailwindCSS and shadcn/ui to ensure a consistent and professional look and feel.
- **Responsive First:** The application must be fully responsive and designed to work seamlessly on all screen sizes, from mobile to desktop.
- **Real-time Interaction:** The chat interface must provide real-time feedback to the user. This includes streaming responses from agents and clear loading and thinking indicators.
- **Accessibility:** We will follow WCAG guidelines to ensure the application is usable by everyone.

## Frontend (Next.js)

- **Component-Based Architecture:** All UI elements will be built as React components. Components should be small, reusable, and have a single, well-defined responsibility.
- **State Management:** We will use React hooks for local component state and React Context (`ChatProvider`) for global chat-related state. This keeps our state management predictable and easy to trace.
- **Streaming with React 19:** We will leverage the latest React 19 features, such as the `use` hook, for handling streaming data from the backend. This is the standard for ensuring a smooth and responsive user experience.
- **Styling:** All styling will be done using TailwindCSS. Custom CSS should be avoided unless absolutely necessary.
- **Testing:** All new components must have corresponding tests written using Jest and React Testing Library. User interactions should be tested where applicable.

## Backend (ADK Agents & MCP Servers)

- **Agent Architecture:** We will follow a modular, multi-agent architecture. A `root_agent` will act as an orchestrator, delegating tasks to specialized sub-agents (e.g., `rag_agent`, `slides_agent`).
- **MCP Servers for External Services:** Interactions with external APIs (e.g., Google Slides) will be encapsulated within MCP servers. This decouples the agents from the external services and promotes reusability.
- **Environment-aware Configuration:** We will use `.env` files to manage environment-specific configurations. A clear distinction must be maintained between local development (`.env.local`) and cloud deployment (`.env`) variables.
- **Authentication and Authorization:** Service accounts with the principle of least privilege will be used for all cloud deployments. OAuth will be used for user-facing authentication when required.
- **Testing:** All Python code, including agent tools and MCP server endpoints, must be tested using `pytest`. Integration tests are required for the interaction between agents and MCP servers.

## Development Workflow

- **TDD is Mandatory:**
    1.  Write a failing test that clearly defines the new feature or bug.
    2.  Write the minimum amount of code required to make the test pass.
    3.  Refactor the code to improve its quality and maintainability, ensuring the tests still pass.
- **Git Workflow:**
    1.  Create a new feature branch for every new feature or bug fix.
    2.  Submit a pull request for code review.
    3.  Ensure all automated tests (linting, unit, integration) pass before requesting a review.
- **Code Reviews:** All pull requests must be reviewed and approved by at least one other developer before being merged into the main branch.

## Governance

- This constitution is the single source of truth for all development practices in this project. It supersedes all previous conventions.
- Any amendments to this constitution must be proposed in writing, documented, and approved by the project lead.

**Version**: 1.0.0 | **Ratified**: 2025-09-19 | **Last Amended**: 2025-09-19
