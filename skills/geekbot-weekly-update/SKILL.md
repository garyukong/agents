---
name: geekbot-weekly-update
description: This skill should be used when the user asks to "fill in my geekbot", "geekbot update", "weekly update", "standup update", "write my weekly update", or "prepare my geekbot". Gathers data from git logs and Jira, then drafts a structured Geekbot weekly standup update.
version: 0.1.0
---

# Geekbot Weekly Update

Automate the weekly Geekbot standup update by gathering data from git history and Jira, then prompting for manual sections that require human judgement.

## Output Format

The final output must follow this exact structure:

```
A) What were your key achievements in the past week?
<generated from git + closed Jira tickets>

B) What challenges did you face?
<inferred from blocked/stuck Jira tickets, confirmed by user>

C) What's top of mind for you next week?
<inferred from open/in-progress Jira tickets, confirmed by user>

D) Anything else to highlight?
<provided by user>
```

## Workflow

Execute the following steps in order.

### Step 1: Gather Git Commits

Run git log for both repos, filtered to the current user's commits in the past 7 days:

```shell
git -C ~/PycharmProjects/oms-ml-semantics log --oneline --since="7 days ago" --author="$(git config user.email)" 2>/dev/null
git -C ~/PycharmProjects/poc-authoring-tool log --oneline --since="7 days ago" --author="$(git config user.email)" 2>/dev/null
```

Use `ctx_batch_execute` to run both commands together. Collect commit messages from both repos, labelling which repo each came from.

### Step 2: Gather Jira Tickets

Use the Atlassian MCP tools to:
1. Resolve the current user's identity (email/accountId)
2. Query for all `MLC-*` tickets assigned to the user that were **updated or resolved in the past 7 days**

JQL to use:
```
project = MLC AND assignee = currentUser() AND updated >= -7d ORDER BY updated DESC
```

Collect: ticket key, summary, status, and any labels/blockers.

### Step 3: Draft Section A — Achievements

From the gathered data, synthesize a concise bullet list of key achievements:
- Group related commits under themes (e.g. "ML model improvements", "tooling", "bug fixes")
- Include closed/resolved Jira tickets as achievements
- Keep bullets concise (one line each)
- Focus on impact, not implementation detail

### Step 4: Draft Section B — Challenges (with user confirmation)

From Jira data, identify tickets that are:
- Flagged as blocked
- In "In Progress" status for more than a few days without recent commits
- Have comments indicating impediments

Draft a short bullet list of inferred challenges, then **ask the user**:
> "Here's my draft for B) Challenges — does this look right, or would you like to edit it?"

Wait for confirmation or edits before proceeding.

### Step 5: Draft Section C — Next Week (with user confirmation)

From Jira data, identify tickets that are:
- In "To Do" or "In Progress" status
- Highest priority or recently updated

Draft a short bullet list of what's planned, then **ask the user**:
> "Here's my draft for C) Next week — does this look right, or would you like to edit it?"

Wait for confirmation or edits before proceeding.

### Step 6: Prompt for Section D

Ask the user directly:
> "Is there anything else you'd like to highlight in section D? (Press Enter to skip)"

### Step 7: Output Final Draft

Assemble all four sections into the final formatted output. Present it cleanly so the user can copy-paste directly into Geekbot.

## Notes

- Use `ctx_batch_execute` for git commands to avoid flooding context
- Use Atlassian MCP tools for all Jira queries — do not construct raw HTTP calls
- Sections B, C, D require explicit user confirmation before finalising
- If either repo does not exist or has no commits, note it and continue
- If Jira returns no tickets, say so and still prompt the user for manual input
