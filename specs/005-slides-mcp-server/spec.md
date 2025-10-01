# Feature Specification: Slides MCP Server

**Feature Branch**: `005-slides-mcp-server`
**Created**: 2025-09-30
**Status**: Draft
**Input**: User description: "I want an MCP server that will create a presentation in Google slides when fed with data from the slides agent. The slides can be built from pre-saved styles and layouts and will get persisted somewhere."

## Clarifications

### Session 2025-09-30
- Q: Where should the generated Google Slides presentation be persisted? → A: In a shared Google Drive folder owned by a service account.
- Q: From where should the MCP server source the pre-saved styles and layouts for new presentations? → A: From a dedicated Google Drive folder containing multiple approved layout/style templates.
- Q: What naming convention should be used for the generated presentation files? → A: Supplied title suffixed with date.
- Q: How should the specific template and layout be identified in the incoming Presentation Request data from the slides agent? → A: By a human-readable name (e.g., "Company Standard Template") for the template presentation.

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "login system" without auth method), mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
4. **Common underspecified areas**:
   - User types and permissions
   - Data retention/deletion policies
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a user of the slides agent, I want to generate a Google Slides presentation from data so that I can have a structured document created automatically.

### Acceptance Scenarios
1. **Given** the slides agent has structured data for a presentation, **When** it sends this data to the Slides MCP Server, **Then** a new presentation is created in Google Slides.
2. **Given** a presentation has been successfully created, **When** I check the designated persistence location, **Then** I can access the newly created Google Slides presentation.

### Edge Cases
- What happens if the data from the slides agent is malformed or incomplete?
- How does the system handle authentication errors with the Google Slides API?
- What is the expected behavior if a specified pre-saved layout does not exist?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST expose an endpoint to receive presentation data from the slides agent.
- **FR-002**: The system MUST use the received data to create a new presentation in Google Slides.
- **FR-003**: The system MUST support creating slides based on pre-saved styles and layouts sourced from a dedicated Google Drive folder containing multiple approved layout/style templates, identified by a human-readable name in the incoming data.
- **FR-004**: The system MUST persist the created presentation in a shared Google Drive folder owned by a service account, using the supplied title suffixed with the date as the file name.
- **FR-005**: The system MUST handle errors gracefully and provide meaningful feedback to the calling agent (e.g., API errors, data validation failures).

### Key Entities *(include if feature involves data)*
- **Presentation Request**: Represents the data sent from the slides agent. It should contain all necessary information for creating the presentation, such as slide content, desired layouts, and presentation title.
- **Google Slides Presentation**: The final output document created in the user's or a service account's Google Slides.

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [X] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [X] User description parsed
- [X] Key concepts extracted
- [X] Ambiguities marked
- [X] User scenarios defined
- [X] Requirements generated
- [X] Entities identified
- [ ] Review checklist passed

---
