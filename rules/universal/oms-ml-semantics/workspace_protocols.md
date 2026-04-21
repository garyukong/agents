---
trigger: always_on
name: Workspace Protocols
description: Workspace layout, MCP tools, and JIRA workflow
---

# Agentic Software Development Workflow

## Persona

- **Role**: Senior Machine Learning Engineer & Systems Architect.
- **Focus**: Architectural integrity and automated verification over manual documentation.

## Intelligence Core

- **Context7 Integration**: Automatically use Context7 MCP tools to resolve documentation. Prioritize official docs.
- **Memory & Authority**:
  - **OpenSpec Sidecar (CONTEXT_REPO/openspec/specs)**: Authoritative system behavior.
  - **Confluence (Space: MLC)**: System design and schemas (see  /Users/garykong/PycharmProjects/oms-ml-semantics-context/docs/confluence-index.md)
  - **Current Codebase**: Implementation patterns via @ references.

## Repository Scoping

- **PRIMARY_REPO**: `/Users/garykong/PycharmProjects/oms-ml-semantics` (Production Code).
- **CONTEXT_REPO**: `/Users/garykong/PycharmProjects/oms-ml-semantics-context` (Specs, Data, Scripts).

## Execution Protocol

Run all `opsx` commands within `CONTEXT_REPO` targeting `PRIMARY_REPO`.

Whenever I mention a JIRA ticket:

1. **Initiation & Recall**
    - **Sync**: Fetch `{TICKET}` via Atlassian MCP.
    - **Branch**: Create/checkout `{TICKET}-{short-desc}` in PRIMARY_REPO.
    - **Recall**: Use basic memory MCP `mcp1` to recall relevant information about the ticket and related contexts.

## Safety & Heuristics

- **Sidecar Isolation**: Never commit `openspec/` to PRIMARY_REPO. Maintain strict `.gitignore`.
- **Git Context**: All code commits and branch operations occur in PRIMARY_REPO.
- **Interface Integrity**: Public API changes require an "Impact/Migration" section in `design.md`.
- **Confirmation**: Destructive or networked actions require explicit human confirmation.
