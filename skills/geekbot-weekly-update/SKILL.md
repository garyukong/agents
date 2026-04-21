---
name: geekbot-weekly-update
description: This skill should be used when the user asks to "fill in my geekbot", "geekbot update", "weekly update", "standup update", "write my weekly update", "prepare my geekbot", or "what did I achieve this week". Gathers data from git logs, GitHub PR activity, and Jira, then drafts a structured Geekbot weekly standup update. Use this skill whenever the user wants to summarise their week, prepare a team review brief, or answer "what were your key achievements in the past week?"
version: 0.2.0
---

# Geekbot Weekly Update

Automate the weekly Geekbot standup update by gathering data from git history, GitHub PR activity, and Jira, then prompting for manual sections that require human judgement.

## Output Format

The final output must follow this exact structure:

```
A) What were your key achievements in the past week?
<generated from git + GH PRs + closed Jira tickets>

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

### Step 1b: Gather GitHub PR Activity

Use the `gh` CLI to fetch PRs the user authored in the past 7 days. Run both commands together via `ctx_batch_execute`:

```shell
# PRs merged in the last 7 days
gh search prs --author="@me" --merged --limit 30 --json title,number,mergedAt,repository,url \
  | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta
cutoff = datetime.now(timezone.utc) - timedelta(days=7)
prs = json.load(sys.stdin)
recent = [p for p in prs if datetime.fromisoformat(p['mergedAt'].replace('Z','+00:00')) >= cutoff]
print(json.dumps(recent, indent=2))
"

# PRs opened in the last 7 days (open or merged)
gh search prs --author="@me" --state=open --limit 30 --json title,number,createdAt,repository,url \
  | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta
cutoff = datetime.now(timezone.utc) - timedelta(days=7)
prs = json.load(sys.stdin)
recent = [p for p in prs if datetime.fromisoformat(p['createdAt'].replace('Z','+00:00')) >= cutoff]
print(json.dumps(recent, indent=2))
"
```

Collect: PR title, repo name, and status (merged vs still open). If `gh` is not authenticated or returns an error, note it and continue with the other data sources.

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

From the gathered data, synthesize a concise bullet list of key achievements. Combine all three signals:

**GitHub PRs** (highest signal — use as primary achievements):
- PRs **merged**: frame as shipped work (e.g. "Shipped: <PR title> [repo]")
- PRs **opened**: frame as work-in-progress delivered to review (e.g. "Put up for review: <PR title> [repo]")
- If a PR title is too terse, infer context from the repo name

**Git commits**: use to fill gaps not covered by PRs — e.g. commits to repos where PRs aren't used, or config/infra changes. Don't duplicate work already covered by a PR.

**Closed/resolved Jira tickets**: include as achievements, grouped with related commits/PRs where possible.

Formatting rules:
- Group bullets under themes when 3+ items share a theme (e.g. "ML model work", "tooling", "infra")
- Keep each bullet to one line
- Lead with the outcome, not the implementation (what changed, not how)

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

- Use `ctx_batch_execute` for all shell commands (git + gh) to avoid flooding context
- Use Atlassian MCP tools for all Jira queries — do not construct raw HTTP calls
- Sections B, C, D require explicit user confirmation before finalising
- If either repo does not exist or has no commits, note it and continue
- If `gh` is not authenticated or unavailable, skip Step 1b and rely on git + Jira
- If Jira returns no tickets, say so and still prompt the user for manual input
- GH PRs are the primary signal for Section A; git commits are supplementary
