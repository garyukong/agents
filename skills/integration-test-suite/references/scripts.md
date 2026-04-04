# Integration Test Scripts Reference

All scripts are in `projects/integration-test-suite/scripts/`. Run them from `projects/integration-test-suite/`.

---

## `set_variables.sh` — environment and cost configuration

Sets environment variables used by Docker Compose and the test suite.

```bash
bash scripts/set_variables.sh           # target staging (default)
bash scripts/set_variables.sh production  # target production
```

**What it sets:**
- Database connection details (host, port, name, credentials)
- RabbitMQ connection details
- API ports and domain
- AWS account ID and DB dump location (staging or production)
- **Cost-control overrides**: utterance and evaluation counts set to `1` for both APIs

> This file is the source of truth for cost controls. Edit it to change utterance limits or switch environments.

---

## `get_secrets.sh` — pull secrets from AWS (requires VPN)

Fetches credentials from AWS Secrets Manager and writes them to local env files.

```bash
bash scripts/get_secrets.sh
```

**Creates:**
- `.env` — Cognito, DB, MQ, and API settings for the test suite
- `.env.semantics_api` — settings injected into the Semantics API container
- `.env.batch_processing_api` — settings injected into the Batch Processing API container

> VPN must be active. Run after `set_variables.sh` so AWS account variables are set.

---

## `setup.sh` — install Python dependencies

```bash
bash ./scripts/setup.sh -v poetry
```

**Flags:**
- `-v <poetry_command>` (required): the Poetry command to use (e.g., `poetry`)

---

## `complete.sh` — full test run

Runs the entire workflow: pre-run setup → pytest → post-run teardown.

```bash
bash ./scripts/complete.sh -v poetry             # run against staging
bash ./scripts/complete.sh -v poetry -e production  # run against production
bash ./scripts/complete.sh -v poetry -d          # developer mode (no tests, no teardown)
```

**Flags:**
- `-v <poetry_command>` (required)
- `-e staging|production` (optional, default: `staging`)
- `-d` (optional): developer mode — starts containers but skips tests and teardown

**Internally calls:**
1. `pre_run.sh` — starts Docker Compose, restores DB
2. `pytest ./tests` with live logging
3. `post_run.sh` — tears down containers

---

## `pre_run.sh` — start containers and restore database

Called automatically by `complete.sh`. Starts Docker Compose services and restores the database from `db.dump`.

---

## `post_run.sh` — tear down containers

Tears down all containers, volumes, and locally built images.

```bash
bash ./scripts/post_run.sh
```

Run this manually if the test suite failed and containers are still running.

---

## `db_dump.sh` — create a new database dump

Creates a fresh dump of the staging (or production) database for use as test data.

```bash
bash scripts/db_dump.sh -p <db_password>
```

Requires VPN and valid credentials. The dump is saved as `db.dump`.

---

## `db_restore.sh` — restore the database locally

Restores `db.dump` into the local test Postgres container without running the full suite.

```bash
bash scripts/db_restore.sh
```

Useful when iterating locally and you don't want to run `docker compose up/down` repeatedly.

---

## `db_migrate.sh` — run database migrations

Runs any pending Alembic migrations against the test database.

```bash
bash scripts/db_migrate.sh
```

---

## Execution order (full local run)

```bash
cd projects/integration-test-suite/

bash scripts/set_variables.sh       # 1. set env vars
bash scripts/get_secrets.sh         # 2. pull secrets (VPN required)
bash ./scripts/setup.sh -v poetry   # 3. install dependencies
bash ./scripts/complete.sh -v poetry  # 4. run the suite
```

If the suite fails and you want to inspect containers:
```bash
bash ./scripts/complete.sh -v poetry -d   # developer mode
# ... inspect, debug ...
docker compose down -v --remove-orphans --rmi local  # manual teardown
docker builder prune                                 # clear build cache
```