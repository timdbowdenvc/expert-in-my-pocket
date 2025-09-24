# Implementation Plan: Agent Deployment with Service Account

**Feature Branch**: `002-to-use-agents`
**Created**: 2025-09-23
**Status**: In Progress
**Input Spec**: /Users/timbo/Dev/expert-in-my-pocket/specs/002-to-use-agents/spec.md

---

## 🚀 Technical Context
*(No specific user-provided details for this phase)*

## 💡 Research & Exploration (Phase 0)
*(Generate `research.md` in this phase)*

### Key Questions
- How to create a service account using `gcloud` commands or Python client libraries?
- How to grant roles to a service account using `gcloud` commands or Python client libraries?
- How to specify a service account for a deployed Vertex AI Agent Engine agent?
- How to log the service account used by the deployed agent?

### Research Tasks
- Investigate `gcloud iam service-accounts create` command.
- Investigate `gcloud projects add-iam-policy-binding` command.
- Review Vertex AI Agent Engine deployment documentation for service account configuration.
- Explore logging mechanisms in Python for agent deployment.

### Expected Outcome
- Clear understanding of `gcloud` commands/Python APIs for service account management.
- Identified method for configuring service account during agent deployment.
- Strategy for logging service account usage.

---

## 🏗️ Design & Data Modeling (Phase 1)
*(Generate `data-model.md`, `contracts/`, `quickstart.md` in this phase)*

### System Architecture
- The existing deployment script (`app/agent_engine_app.py`) will be modified.
- A new function or modification to `deploy_agent` will handle service account creation/specification.
- Google Cloud IAM API will be used for service account management.

### Data Model
- No new complex data models are required. The existing `DeploymentConfig` will be extended to include service account information.

### API Contracts
- No new external API contracts are needed. The existing Google Cloud IAM API will be used.

### Quickstart Guide
- Update the deployment instructions to include steps for service account creation/specification.

---

## 📋 Task Breakdown (Phase 2)
*(Generate `tasks.md` in this phase)*

### High-Level Tasks
- [Break down the implementation into major, independent tasks]

### Detailed Tasks
- [Further decompose high-level tasks into actionable, smaller units]

---

## ✅ Verification & Testing
*(Integrate with existing test strategy)*

### Unit Tests
- Outline critical components requiring unit tests
    - Test service account creation logic.
    - Test role granting logic.
    - Test service account specification in deployment.

### Integration Tests
- Describe scenarios for integration testing
    - Deploy an agent with a specified service account and verify it runs with that identity.
    - Deploy an agent without a specified service account and verify a new one is created and used.

### End-to-End Tests
- Define user-facing test cases
    - Deploy an agent with a service account, grant it a specific role (e.g., Storage Object Viewer), and verify the agent can access a GCS bucket.

---

## 📈 Progress Tracking
*(Updated by main() during processing)*

- [x] Phase 0: Research & Exploration
- [x] Phase 1: Design & Data Modeling
- [x] Phase 2: Task Breakdown
- [x] Verification & Testing

---

## Review & Acceptance Checklist
*(Automated checks run during main() execution)*

### Plan Quality
- [ ] Technical context is clear and concise
- [ ] Research questions are well-defined
- [ ] Design decisions are justified
- [ ] Data model is consistent and complete
- [ ] API contracts are clear and versioned
- [ ] Task breakdown is granular and actionable
- [ ] Testing strategy is comprehensive

### Alignment
- [ ] Plan aligns with feature specification
- [ ] Constitutional requirements are met
- [ ] Dependencies and assumptions are identified

---