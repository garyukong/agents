---
name: integration-test-suite
description: Guide for creating and running integration tests in the oms-ml-semantics integration test suite
version: 1.0.0
tags:
  - testing
  - integration-testing
  - pytest
  - docker
---

# Integration Test Suite Skill

## When to Use This Skill

Use this skill when you need to:
- Create new integration tests for the oms-ml-semantics ML system
- Run the integration test suite locally or understand how CI runs it
- Debug a failed integration test run
- Understand the replica infrastructure and test environment
- Work with fixtures, database state, or the message queue in tests

**Trigger keywords:** `integration-test`, `integration test suite`, `create integration test`, `run integration tests`

---

## Overview

The integration test suite builds a **replica of the production ML infrastructure** using Docker Compose. It tests the Semantics API and Batch Processing API end-to-end with real Postgres, RabbitMQ, and AWS Cognito authentication (via VPN).

**Why replica, not staging?** Staging does not support safe write operations during tests (no delete endpoints, no isolation). The replica approach gives us a clean, controlled database on every run without affecting shared environments.

**Infrastructure components:**
- **Postgres** (port 5433): populated from a staging database dump (`db.dump`)
- **RabbitMQ** (port 5673): pulled from public Docker Hub
- **Semantics API** (port 8081): built from source
- **Batch Processing API** (port 8082): built from source
- **AWS Cognito**: real authentication via VPN (not mocked)
- **Label Studio**: excluded — requires manual API key creation, cannot be automated

**Cost controls:** `scripts/set_variables.sh` overrides utterance/evaluation counts to 1 to minimise LLM spend. Model names are also overridden to `gemini-2.5-flash-lite` via an `autouse` fixture. Edit `scripts/set_variables.sh` to change these defaults.

---

## Test Structure Conventions

Tests follow the **Given / When / Then** pattern and use `pytest-asyncio` for async operations.

```python
@pytest.mark.asyncio
async def test_<what>_<expected_outcome>(
    settings,
    api_token,
    http_client,
    test_db_async_session,
):
    # Given
    payload = { ... }

    # When
    response = await http_client.post(
        f"http://{settings.api_domain}:{settings.semantics_api_port}/...",
        headers={"Authorization": f"Bearer {api_token}"},
        json=payload,
    )

    # Then
    assert response.status_code == 201
```

See `references/test-example.md` for a fully annotated example.

---

## Available Fixtures

All fixtures are defined in `projects/integration-test-suite/tests/conftest.py`.

| Fixture | Scope | Description |
|---|---|---|
| `settings` | session | Loads `.env` into a `Settings` object |
| `api_token` | session | Cognito JWT access token via VPN |
| `test_db_async_session` | function | Async SQLAlchemy session to the test Postgres |
| `mq_client` | function | Connected `MqClient` to test RabbitMQ |
| `http_client` | function | `httpx.AsyncClient` for API requests |

The `override_sub_task_model_name` fixture is **autouse** — it forces all sub_tasks to use `gemini-2.5-flash-lite` before every test to control model cost.

See `references/fixtures.md` for detailed usage examples.

---

## Database Interaction Patterns

Use `test_db_async_session` with SQLAlchemy async queries:

```python
from sqlalchemy import select
from db.models import Task

@pytest.mark.asyncio
async def test_example(test_db_async_session):
    # Query
    stmt = select(Task.name).where(Task.name == "my_task").limit(1)
    result = await test_db_async_session.execute(stmt)
    task_name = result.scalar()

    # Skip gracefully when preconditions are not met
    if not task_name:
        pytest.skip("No tasks found in database")
```

Use `pytest.skip()` to skip tests gracefully when required data does not exist rather than failing with an assertion error.

---

## HTTP Client Usage

All API requests use `http_client` (an `httpx.AsyncClient`) with Bearer token auth:

```python
response = await http_client.post(
    f"http://{settings.api_domain}:{settings.semantics_api_port}/tasks/task",
    headers={"Authorization": f"Bearer {api_token}"},
    json=payload,
)
assert response.status_code == 201
```

The `settings` fixture provides `api_domain`, `semantics_api_port`, and `batch_api_port`.

---

## RabbitMQ Testing Patterns

Use the `mq_client` fixture for tests that interact with the message queue:

```python
@pytest.mark.asyncio
async def test_message_published(mq_client, ...):
    # mq_client is already connected
    await mq_client.publish(queue="my_queue", message={"key": "value"})
    # ... assert downstream effects
```

The `mq_client` fixture connects and disconnects automatically (see `conftest.py`).

---

## Parametrized Test Guidelines

Use `pytest.mark.parametrize` with explicit `ids` for readable test output:

```python
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code, payload",
    [
        (201, {"valid": "data"}),
        (422, {"invalid": "data"}),
    ],
    ids=["valid_payload_creates", "invalid_payload_rejected"],
)
async def test_endpoint(status_code, payload, settings, api_token, http_client):
    response = await http_client.post(
        f"http://{settings.api_domain}:{settings.semantics_api_port}/...",
        headers={"Authorization": f"Bearer {api_token}"},
        json=payload,
    )
    assert response.status_code == status_code
```

---

## Setup and Execution

### Working directory

All commands must be run from `projects/integration-test-suite/`:

```bash
cd projects/integration-test-suite/
```

### 1. Configure environment variables

```bash
bash scripts/set_variables.sh          # staging (default)
bash scripts/set_variables.sh production  # production
```

### 2. Pull secrets (requires VPN)

```bash
bash scripts/get_secrets.sh
```

This creates `.env`, `.env.semantics_api`, and `.env.batch_processing_api` from AWS Secrets Manager.

### 3. Install dependencies

```bash
bash ./scripts/setup.sh -v poetry
```

### 4. Run the full test suite

```bash
bash ./scripts/complete.sh -v poetry
```

This runs `pre_run.sh` (starts Docker Compose, restores DB), pytest, then `post_run.sh` (tears down).

### Developer mode (keep containers running)

```bash
bash scripts/complete.sh -v poetry -d
```

The `-d` flag skips pytest and teardown so you can inspect running containers and logs.

### Manual cleanup

If the test suite fails, containers remain running. Tear them down manually:

```bash
bash ./scripts/post_run.sh
```

If running repeatedly locally, prune the Docker build cache to reclaim disk space:

```bash
docker builder prune
```

---

## Infrastructure and Architecture

### Replica approach

The suite creates an isolated replica of the full ML system stack so tests can:
- Write to Postgres (tasks, action codes, utterances, scenarios) without polluting staging
- Use real RabbitMQ message passing
- Authenticate via real AWS Cognito (requires VPN)
- Run completely in parallel without affecting other environments

### Test data management

The test database is populated from `db.dump` — a dump of the staging database. This provides realistic data (scenarios, tasks, action codes) without manual seeding.

To produce a fresh dump:
```bash
bash scripts/db_dump.sh -p <db_password>
```

To restore locally without running the full suite:
```bash
bash scripts/db_restore.sh
```

### Label Studio exclusion

Label Studio requires a manually created API key (via its UI) and cannot be automated at startup. The `connect_to_label_studio` flag is set to `false` in the API configuration to disable that integration during test runs.

### Authentication

Tests authenticate with real AWS Cognito using credentials fetched from Secrets Manager by `get_secrets.sh`. VPN is required. The `api_token` fixture (session-scoped) fetches the token once per test run.

### Cost-control mechanisms

Two layers of cost control prevent excessive LLM spend during test runs:

1. **Utterance/evaluation count overrides** — `scripts/set_variables.sh` sets all generation counts to `1`, injected into both APIs via Docker Compose environment variables.
2. **Model override fixture** — `override_sub_task_model_name` (autouse) updates all `SubTask` rows to use `gemini-2.5-flash-lite` before each test.

To change the model or counts, edit `scripts/set_variables.sh` — it is the source of truth.

---

## File Path References

| Path | Description |
|---|---|
| `projects/integration-test-suite/tests/conftest.py` | All shared fixtures |
| `projects/integration-test-suite/tests/test_tasks/` | Task endpoint tests |
| `projects/integration-test-suite/tests/test_scenarios/` | Scenario endpoint tests |
| `projects/integration-test-suite/tests/test_evaluations/` | Evaluation tests |
| `projects/integration-test-suite/tests/test_inference/` | Inference tests |
| `projects/integration-test-suite/tests/test_utterances/` | Utterance tests |
| `projects/integration-test-suite/tests/test_action_codes/` | Action code tests |
| `projects/integration-test-suite/scripts/` | All setup and execution scripts |
| `projects/integration-test-suite/scripts/set_variables.sh` | Infrastructure env vars and cost controls |
| `projects/integration-test-suite/scripts/get_secrets.sh` | Pulls secrets from AWS |
| `projects/integration-test-suite/README.md` | Additional context and rationale |
