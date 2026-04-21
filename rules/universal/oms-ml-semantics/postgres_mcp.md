---
trigger: model_decision
name: Postgres MCP
description: Use this when i ask to query Postgres
---

## Postgres MCP
- Default: `query` via `postgres-local` unless I say staging/prod.
- Staging: `query` via `postgres-staging` when I say staging.
- Prod: `query` via `postgres-prod` when I say prod/production.

## Permissions
- Read-only; no writes/DDL.

## Invoke
- If env not stated and impact is possible, ask.
- If env stated, don't fall back to local; if not, assume local.
