---
name: "Python Testing"
description: "Python testing standards"
applyTo:
  - "**/tests/**/*"
  - "**/test_*.py"
  - "**/_test.py"
  - "conftest.py"
  - "pytest.ini"
  - "tox.ini"
---

## Testing

- `pytest` (fixtures/mocks), >90% coverage. 1 test file per module mirroring source dir.
- Unit tests: mock interfaces (`Mock(spec=IService)`). Integration: real implementations.
- `@pytest.mark.asyncio` for async; `AsyncMock(spec=...)` for async contracts.
- Hierarchical `conftest.py`; session scope for expensive setup.
- Parametrized tests: no conditionals in bodies. Split if needed.
- Structure comments: `# Given`, `# When`, `# Then` only.
- Keep mock setup/requests outside `patch` blocks (only side effects & call inside).
- Top imports only. No imports within tests.