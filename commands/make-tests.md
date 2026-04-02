---
auto_execution_mode: 0
description: "Create or update unit tests for the PR"
---
## Goal

Create or update unit tests for this PR using an **80/20** approach: cover the key behaviours and regression risks introduced by the diff, without over-indexing on exhaustive edge cases.

## Operating Rules

- **Work from the diff first** (not assumptions).
- **One test file at a time** (one `test_*.py` file = one checklist item).
- **Approval gate**: propose test cases → wait for my approval → implement.
- **Debug transparently**: when tests fail, explain **what failed and why** before changing code.
- Prefer **stable tests** (deterministic, minimal mocking, avoid brittle string-matching unless necessary).
- Follow the **unit testing guidelines** set out in my rules

---

## Step 1 — Identify Changed Files (Diff vs main)

1. Ensure `main` is up to date:
   - `git fetch origin`
2. Diff branch vs main:
   - `git diff --name-status origin/main...HEAD`
3. Also gather contextual diff for code review:
   - `git diff origin/main...HEAD`

**Outputs to capture**

- List of changed files (added/modified/deleted)
- High-level summary of what each change does (1–2 lines per file)

---

## Step 2 — Audit the Changes and Infer Test Impact

For each changed file:

1. Categorise it:
   - **New feature / behaviour**
   - **Refactor (no intended behaviour change)**
   - **Bug fix**
   - **Config / wiring / plumbing**
2. Decide test impact:
   - **New tests needed**
   - **Existing tests need updating**
   - **No test changes required** (must justify)
3. Identify risk areas:
   - Logic branches introduced/changed
   - Boundary conditions (inputs/outputs)
   - Integration points (DB/network/adapters)
   - Error handling / exceptions
   - Public API surface (functions/classes used elsewhere)

**Deliverable**

- A compact audit summary mapping: `changed file → behaviour change → test action`

---

## Step 3 — Create a Unit Test Checklist Markdown

Create a checklist `.md` file and save it in your context folder.

### Checklist Requirements

- Organise by **project/library** then **test file**.
- Each checklist item corresponds to exactly **one** `test_*.py` file.
- Each item includes:
  - Target test file path
  - What it covers (1 line)
  - Status checkbox

### Template (to generate and save)

Use this structure:

## Unit Test Checklist

### <project_or_library_name>

- [ ] `<path/to/tests/test_some_module.py>` — Covers: <brief scope>

### <another_project_or_library_name>

- [ ] `<path/to/tests/test_other_module.py>` — Covers: <brief scope>

---

## Step 4 — Implement Tests One File at a Time (Approval-Gated)

### 4A — Propose Test Cases (80/20)

For the next checklist item only:

1. Identify the SUT (system under test):
   - Function/class/module + key behaviours
2. Propose **3–8 test cases** max (typical sweet spot).
3. For each test case, provide:
   - **Name** (pytest-style, descriptive)
   - **Intent** (what behaviour it validates)
   - **Setup notes** (fixtures/mocks needed, if any)
   - **Key assertion(s)**

**STOP HERE and wait for approval.**
Do not write code until I confirm.

---

### 4B — Implement the Approved Test Cases

When approved:

1. Add/modify tests in the specified `test_*.py`.
2. Prefer:
   - `pytest` fixtures
   - minimal mocking
   - clear Arrange/Act/Assert separation
3. Keep tests readable and deterministic.
4. If you need new fixtures/utilities:
   - Add them in the most appropriate `conftest.py` or local file
   - Explain why

---

### 4C — Run Tests and Debug (Explain Before Fixing)

Run the most relevant tests first:

- `pytest <path/to/tests/test_file.py> -q`

If passing, run a broader subset:

- `pytest -q`

If failures occur:

1. Report:
   - failing test(s)
   - error message + traceback highlights
   - root cause explanation (in plain terms)
2. Propose a fix:
   - test fix vs production fix
   - why the chosen fix is correct
3. Apply fix
4. Re-run the same command to confirm

---

## Step 5 — Update Checklist as You Go

After completing each test file (green tests):

- Mark its checkbox as completed: `- [x] ...`
- Add a short note under it if useful:
  - e.g., “Added coverage for X; updated fixture Y; verified bug regression.”

Then move to the next checklist item and repeat Step 4.

---

## Definition of Done

- Checklist created in the ticket folder and maintained throughout.
- Each changed behaviour has at least one meaningful test (80/20 coverage).
- All tests pass locally for the targeted scope and ideally full suite (time permitting).
- No unexplained skips/xfails; if used, they include justification and a follow-up note.

---

## Interaction Contract (Cascade ↔ Gary)

- You will **always**:
  - start from the diff
  - propose test cases and wait for approval per file
  - explain failures before correcting them
  - keep the checklist updated as the source of truth
