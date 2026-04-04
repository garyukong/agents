# Integration Test Fixtures Reference

All shared fixtures are defined in `projects/integration-test-suite/tests/conftest.py`.

---

## `settings` — session scope

Loads environment variables from `.env` into a typed `Settings` object.

```python
@pytest.fixture(scope="session", name="settings")
def load_environment_settings():
    ...
```

**Provides:**
- `settings.api_domain` — hostname for API requests (e.g., `localhost`)
- `settings.semantics_api_port` — port for the Semantics API (e.g., `8081`)
- `settings.batch_api_port` — port for the Batch Processing API (e.g., `8082`)
- `settings.cognito_*` — Cognito credentials for the `api_token` fixture
- `settings.mq_*` — RabbitMQ connection details for the `mq_client` fixture
- `settings.log_level` — logging level

**Usage:**
```python
async def test_something(settings, http_client):
    response = await http_client.get(
        f"http://{settings.api_domain}:{settings.semantics_api_port}/health"
    )
```

---

## `api_token` — session scope

Fetches a Cognito JWT access token once per test session. Requires VPN to reach AWS Cognito.

```python
@pytest.fixture(scope="session")
def api_token(settings):
    ...
```

**Usage:**
```python
async def test_protected_endpoint(settings, api_token, http_client):
    response = await http_client.get(
        f"http://{settings.api_domain}:{settings.semantics_api_port}/...",
        headers={"Authorization": f"Bearer {api_token}"},
    )
```

---

## `test_db_async_session` — function scope

Creates a fresh async SQLAlchemy session per test function connected to the test Postgres instance.

```python
@pytest_asyncio.fixture
async def test_db_async_session(test_db_async_pgurl):
    ...
```

**Connection details** (set by `scripts/set_variables.sh`):
- Host: `localhost:5433`
- Database: `voice_test`
- User: `user` / Password: `password`

**Usage — querying:**
```python
from sqlalchemy import select
from db.models import Task

async def test_query(test_db_async_session):
    stmt = select(Task.name).where(Task.name == "my_task").limit(1)
    result = await test_db_async_session.execute(stmt)
    name = result.scalar()
```

**Usage — writing:**
```python
from db.models.tasks import Model

async def test_write(test_db_async_session):
    new_model = Model(name="new_model")
    test_db_async_session.add(new_model)
    await test_db_async_session.commit()
```

---

## `mq_client` — function scope

Creates a connected `MqClient` instance per test. Disconnects automatically after the test.

```python
@pytest_asyncio.fixture
async def mq_client(settings):
    ...
```

**Connection details:**
- Host: `localhost`, Port: `5673`
- User: `guest` / Password: `guest`

**Usage:**
```python
async def test_message_queue(mq_client):
    await mq_client.publish(queue="my_queue", message={"key": "value"})
    # assert downstream effects
```

---

## `http_client` — function scope

Provides an `httpx.AsyncClient` for making HTTP requests to the APIs.

```python
@pytest_asyncio.fixture
async def http_client():
    async with httpx.AsyncClient() as client:
        yield client
```

**Usage:**
```python
async def test_get(settings, api_token, http_client):
    response = await http_client.get(
        f"http://{settings.api_domain}:{settings.semantics_api_port}/tasks",
        headers={"Authorization": f"Bearer {api_token}"},
    )
    assert response.status_code == 200
```

---

## `override_sub_task_model_name` — autouse, function scope

Automatically runs before every test. Updates all `SubTask` rows in the database to use `gemini-2.5-flash-lite` to minimise LLM cost during test runs.

**You do not need to request this fixture** — it applies to every test automatically.

If a test requires a specific model, override the model after this fixture runs, or adjust the model name in this fixture (but be careful about cost impact).

---

## Creating local fixtures

Define test-file-local fixtures in the test file itself (not in `conftest.py`) unless they are reused across multiple test files.

```python
@pytest_asyncio.fixture(scope="function")
async def existing_model(test_db_async_session):
    """Skip the test if no models exist; otherwise return the first model name."""
    stmt = select(Model.name).limit(1)
    result = await test_db_async_session.execute(stmt)
    model = result.scalar()
    if not model:
        pytest.skip("No models found in database")
    return model
```