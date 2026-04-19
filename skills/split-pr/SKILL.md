---
name: split-pr
description: Splits a large branch into smaller, reviewable PRs and executes the full workflow — creating branches, commits, and PRs with chained bases. Use when the user wants to break down a large changeset and actually ship the split PRs, not just plan them. Triggers on "split my PR", "split this branch into PRs", "break this into smaller PRs", or any request to divide a large changeset into reviewable chunks.
---

# Split PR and Execute

Break a large branch into smaller, reviewable PRs — and actually create them.

## Workflow

### 1. Gather context

Before touching the diff, look for design docs that explain *why* the changes exist:
- OpenSpec proposals/designs (`openspec/changes/`)
- ADRs, JIRA tickets, or proposal files linked from commit messages
- Archived specs that superseded earlier decisions

Read them. PR descriptions that explain intent ("why") are far more valuable than ones that just restate the diff ("what"). When one spec supersedes another, note this — it affects how you frame the description.

### 2. Analyse the diff

```bash
git diff main...HEAD --stat
git diff main...HEAD --name-only
git log main...HEAD --oneline
```

Group files by natural boundaries:

- **By layer**: shared libs → internal libs → application code
- **By concern**: new types/interfaces → implementations → consumers
- **By dependency**: identify what must exist before something else can compile/pass tests

### 3. Propose the split

Present a plan in chat before doing anything. For each PR:

- **Title**: `JIRA-KEY: short description (PRN of M)`
- **Purpose**: what it does and why — drawn from the design docs
- **Files**: list source + test files together (they travel as pairs)
- **Size**: approximate lines changed
- **Base branch**: which PR it branches off (chains, not all from `main`)
- **Dependencies**: what must be merged first

Show the dependency chain clearly:

```
PR1 (foundation) → main
PR2 (layer 2)    → PR1
PR3 (consumers)  → PR2
Merge order: PR1 → rebase PR2 → rebase PR3
```

Wait for user approval before proceeding.

### 4. Create branches and commits

**Branch strategy — chain, don't fork from main:**
```bash
git checkout -b pr1-branch main
git checkout -b pr2-branch pr1-branch   # bases off PR1, not main
git checkout -b pr3-branch pr2-branch   # bases off PR2, not main
```

**Checking out files from the feature branch:**
```bash
git checkout <feature-branch> -- path/to/files
```

> **Important:** `git checkout <branch> -- <dir>` does NOT remove files deleted on the source branch. Manually `rm` those files after checkout.

**Staging — always pair source with tests:**

Stage implementation and its tests in the same commit. Never commit source without tests or tests without source. Unstage everything first, then add selectively:

```bash
git reset HEAD
git add src/foo.py tests/test_foo.py
git commit -m "..."
```

**Commit message format** — ask the user for their project convention before committing if not already known. A common format used here:

```
type(prefix:scope): description
```

Where `prefix` identifies the library/project and `scope` identifies the layer (e.g. `refactor(common:models): ...`, `feat(inference:services): ...`).

**Deleted files** — after checking out from a branch where files were deleted, they still exist locally. Delete them explicitly:
```bash
rm path/to/deleted_file.py
git add path/to/deleted_file.py   # stages the deletion
```

### 5. Draft PR description in chat — get approval before pushing

For each PR, draft the description in chat and wait for explicit approval before running `gh pr create`. Corrections are cheap at draft stage, awkward after the PR is open.

**PR description template:**

```markdown
## Summary

Part N of M for [JIRA-KEY].

**Why:**
[Explain the motivation — drawn from design docs, not just the diff.]

**What changed:**
- `path/to/file.py` — [what changed and why]
- `path/to/other.py` — [what changed and why]
- `deleted_file.py` *(deleted)* — [why it was removed]
- Tests updated.

## Review order

Merge PR 1 first, then rebase and merge PR 2, then PR 3.
Each PR bases off the previous — do not merge out of order.
```

**PR description style:**
- Focus on *what changed and why* — from the perspective of a reviewer who hasn't seen the design doc
- Skip "Why X over Y" implementation rationale unless the user asks — that belongs in design docs
- Do include the merge order in every description so reviewers know the chain

### 6. Create PRs

```bash
git push -u origin <branch>
gh pr create \
  --base <previous-pr-branch-or-main> \
  --head <this-branch> \
  --title "JIRA-KEY: description (PRN of M)" \
  --body "..."
```

### 7. Verify parity

After all branches are created, confirm the final PR branch is identical to the original feature branch:

```bash
git diff <original-feature-branch> <last-pr-branch>
# Expected: no output
```

If there is a diff, something was missed during selective staging. Investigate before declaring done.

---

## Splitting principles

- **Foundation before consumers**: shared types/interfaces go in PR 1; code that uses them follows
- **Tests travel with source**: never split them into separate PRs
- **Don't artificially split atomic changes**: a rename touching 40 files is one commit, one PR
- **Deleted files need manual cleanup**: `git checkout` won't remove them for you
- **Each PR must pass CI independently**: don't create a PR that breaks tests until the next one merges

## What NOT to split

- Atomic refactorings (renames, moves touching many files)
- Generated code updates (keep with the change that triggered them)
- Tightly coupled changes that don't make sense independently
