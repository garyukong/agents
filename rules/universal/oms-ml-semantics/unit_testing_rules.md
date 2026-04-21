---
trigger: glob
name: Unit Testing Rules
description: Unit test structure, mocking patterns, and assertion rules for pytest
patterns:
  - "libs/**/tests/**/*.py"
  - "projects/**/tests/**/*.py"
  - "**/test_*.py"
  - "**/conftest.py"
---

# Unit Testing Rules (pytest)

## Core Principle

Each test isolates its target class/function from **all** dependencies via mocks/patches. Test behaviour, not dependencies.

For `libs/db`: add both unit tests (`tests/unit/gateway/`) and integration tests (`tests/database/gateway/`) for new DB gateway methods.

## Structure & Style

- Every test body uses **exactly three** comments: `# Given`, `# When`, `# Then` — no other inline comments. For error tests using `pytest.raises`, combine as `# When / Then`.
- No docstrings inside test functions.
- No typing annotations in test functions or fixtures.
- Setup data, mocks, and request construction go **outside** `with patch(...)` blocks.
- Only side effects and the call under test go **inside** `with patch(...)` blocks.
- Assertions and mock verifications go **outside** `with patch(...)` blocks.
- Use `@pytest.mark.parametrize` with lists of tuples; always include `ids=[...]` on the decorator for readability. Avoid `pytest.param` wrappers.
- Test execution: use `poetry run pytest` (not uv run pytest).
- Group new tests next to existing tests for the same function/method, not at end of file.
- Async tests: mark with `@pytest.mark.asyncio`.
- Prefer parametrized tests over duplication.
- Mock external dependencies to keep tests fast/reliable.

## Naming

- Pattern: `test_<method>_<behavior>` — should read like a sentence.
- Shared fixtures live in `conftest.py`. Reuse or update existing fixtures before creating new ones.

## Mocking

- Prefer `Mock(spec=...)` / `AsyncMock(spec=...)` to enforce interface contracts.
- Mock Pydantic objects with `Mock(spec=PydanticClass)` to decouple from model changes.
- Use `@patch.object` or `@patch` for external functions. Never put mocks in production code.

## Assertions

- Assert behaviour and outcomes, never error message text.
- For error cases: `pytest.raises(ExceptionType)` — do not assert `str(error)` content.
