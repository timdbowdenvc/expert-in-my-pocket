# Feature Specification: Expert SEO Sub-Agent

**Feature Branch**: `004-create-an-expert`  
**Created**: 2025-09-25
**Status**: Draft  
**Input**: User description: "Create an expert SEO sub-agent that can take a URL, analyse the page and suggest SEO optimistations as if it was an SEO expert with a 180IQ and 15 years experience in the industry. The site is for a supplier of green energy solutions"

## Clarifications
### Session 2025-09-25
- Q: Which specific SEO aspects should the agent analyze? → A: All of the above (Core on-page, Technical SEO, Content analysis)
- Q: What is the expected output format for the SEO optimisations? → A: A human-readable Markdown report with explanations for each suggestion.
- Q: How should the agent respond when given a URL for a page that is NOT related to green energy solutions? → A: Analyze the page and include a warning that the advice may not be optimal due to the lack of industry context.
- Q: How should the agent handle a URL that is behind a login or paywall? → A: State that it cannot access content behind a login and abort the analysis.

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
As a user, I want to provide a URL to an SEO agent, so that I can receive expert recommendations to optimize the page's SEO for a green energy solutions website.

### Acceptance Scenarios
1. **Given** a user provides a valid URL for a page on a green energy solutions website, **When** they trigger the SEO analysis, **Then** the agent returns a list of specific, actionable SEO optimisations.
2. **Given** a user provides an invalid URL, **When** they trigger the SEO analysis, **Then** the system returns an error message indicating the URL is not reachable or invalid.

### Edge Cases
- When the URL is for a page not related to green energy, the agent will analyze it and include a warning that the advice may not be optimal.
- If the URL leads to a login page or paywall, the agent will state that it cannot access the content and abort the analysis.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST accept a URL as input from the user.
- **FR-002**: The system MUST be able to fetch and analyse the content of the provided URL.
- **FR-003**: The system MUST generate SEO optimisation suggestions based on the analysed content.
- **FR-004**: The suggestions MUST be tailored for a website in the green energy solutions industry.
- **FR-005**: The system MUST present the suggestions to the user.
- **FR-006**: The system MUST handle invalid or unreachable URLs gracefully by providing an error message.
- **FR-007**: The output format for the suggestions MUST be a human-readable Markdown report with explanations for each suggestion.
- **FR-008**: The agent's analysis MUST consider Core on-page elements (titles, meta descriptions, headers, keyword density), Technical SEO (page speed, mobile-friendliness, structured data, crawlability), and Content analysis (readability, originality, semantic relevance).
- **FR-009**: The system MUST include a warning in the report if the analyzed URL does not appear to be related to the green energy solutions industry.
- **FR-010**: The system MUST detect pages that require a login or are behind a paywall and inform the user that it cannot proceed with the analysis.

### Key Entities *(include if feature involves data)*
- **SEO Analysis Request**: Represents a user's request for an SEO analysis.
  - Attributes: URL
- **SEO Optimisation Report**: Represents the output of the analysis.
  - Attributes: List of suggestions, analysis summary.

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [X] No [NEEDS CLARIFICATION] markers remain (Note: Markers added as part of the process)
- [ ] Requirements are testable and unambiguous  
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Review checklist passed

---
