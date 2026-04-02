---
auto_execution_mode: 0
description: Resumes the agentic state for a specific JIRA ticket using OpenSpec.
---
**Context**: I am resuming work on JIRA ticket **[INSERT TICKET ID]**.

**Instructions**:

1. **Git Sync**: Identify the active branch in `PRIMARY_REPO`.
2. **Fast-Forward**: Run `/opsx:ff` in the `CONTEXT_REPO` to synchronize your understanding of the current `tasks.md`, `design.md`, and the state of the codebase.
3. **Status**: Report back with the current task you are working on and the immediate next step.
