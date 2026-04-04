# Annotated Integration Test Example

This is an annotated version of a real test from `projects/integration-test-suite/tests/test_tasks/test_post_task.py`.

---

## Module-level local fixtures

Local fixtures narrow down test preconditions and skip gracefully when data is missing. Prefer `scope="function"` unless the data is read-only.

```python
@pytest_asyncio.fixture(scope="function")
async def existing_model(test_db_async_session):
    """Return the first available model name or skip if none exist."""
    stmt = select(Model.name).limit(1)
    result = await test_db_async_session.execute(stmt)
    model = result.scalar()
    if not model:
        pytest.skip("No models found in database - cannot test task creation")
    return model
```

> Use `pytest.skip()` inside fixtures to skip the test if required data is not present —
> this is cleaner than asserting in the test body.

---

## A complete test

```python
@pytest.mark.asyncio
async def test_post_task_creates_new_single_task_successfully(
    settings,           # loads .env into Settings — provides api_domain, ports
    api_token,          # Cognito JWT token, fetched once per session via VPN
    test_db_async_session,  # async SQLAlchemy session to test Postgres
    existing_model,     # local fixture: first model in DB, or skip
    component_types,    # local fixture: first 5 scenario prompt component types, or skip
    next_task_version,  # local fixture: callable returning next version for a task name
    http_client,        # httpx.AsyncClient for making requests
):
    # Given — set up the request payload using real DB data
    task_name = "classifier_and_response"
    payload = {
        "taskName": task_name,
        "taskDescription": "Test task following real structure",
        "taskVersion": await next_task_version(task_name),  # avoids version conflicts
        "taskType": "inference",
        "strategy": None,
        "subTasks": [
            {
                "name": "classifier_and_response",
                "modelName": existing_model,          # must exist in DB
                "params": {"thinking_budget": 0},
                "promptComponents": [
                    {
                        "mlPromptComponentName": None,
                        "mlPromptComponentVersion": None,
                        "mlPromptComponentContent": None,
                        "scenarioPromptComponentType": component_types[0],
                        "componentPosition": 1,
                    },
                    {
                        "mlPromptComponentName": f"test_ml_component_{uuid4()}",  # unique name
                        "mlPromptComponentVersion": None,
                        "mlPromptComponentContent": "Test ML component content",
                        "scenarioPromptComponentType": None,
                        "componentPosition": 2,
                    },
                ],
            }
        ],
    }

    # When — make the HTTP request
    response = await http_client.post(
        f"http://{settings.api_domain}:{settings.semantics_api_port}/tasks/task",
        headers={"Authorization": f"Bearer {api_token}"},
        json=payload,
    )

    # Then — assert on the response
    assert response.status_code == 201

    response_data = response.json()
    assert "message" in response_data
    assert "mlPromptComponents" in response_data
```

---

## Key patterns to follow

| Pattern | Why |
|---|---|
| Use `await next_task_version(task_name)` | Avoids unique constraint violations when a task already exists |
| Use `uuid4()` for component names | Ensures uniqueness across test runs |
| Use `pytest.skip()` in fixtures | Skips gracefully instead of failing with a cryptic error |
| Assert specific fields in response | Verifies response shape, not just status code |
| Use `settings.api_domain` / `settings.semantics_api_port` | Never hardcode ports or hostnames |

---

## Source files

- Full test: `projects/integration-test-suite/tests/test_tasks/test_post_task.py`
- All fixtures: `projects/integration-test-suite/tests/conftest.py`
- Scenario tests: `projects/integration-test-suite/tests/test_scenarios/`