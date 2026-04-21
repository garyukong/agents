---
trigger: glob
name: API Architecture
description: API layer separation, dependency flow, and container hierarchy for project source code
patterns:
  - "projects/**/src/**/*.py"
---

# API Architecture Rules

## Layer Separation (MANDATORY)

| Layer | Location | Responsibility | Forbidden |
|---|---|---|---|
| **Dependencies** | `src/dependencies/` | Config, env vars, auth tokens | Business logic |
| **Containers** | `src/containers/` | DI wiring only | Business logic |
| **Gateways** | `src/gateways/` | External service interfaces (ABC + impl) | Business logic |
| **Services** | `src/services/` | Business logic & orchestration | HTTP concerns |
| **Managers** | `src/managers/` | Async context managers (DB sessions, app lifecycle) | Business logic |
| **Models** | `src/models/` | Pydantic models: `requests/`, `responses/`, `handlers/`, `services/` | Logic |
| **Routers** | `src/routers/` | HTTP request/response (FastAPI) | Business logic |
| **Handlers** | `src/handlers/` | MQ processing & background jobs (api, batch-processing-api only) | Direct DB access |
| **Utils** | `src/utils/` | Exceptions, validators, prompt builders | Business logic |

## Dependency Flow (MANDATORY)

```
Routers & Handlers → Services → Gateways → Core/Dependencies
```

- No circular dependencies — lower layers never import upper layers.
- Services depend on gateway **interfaces** (`IInferenceGateway`), not implementations.

## Container Hierarchy

```
Application (root)
├── Core        → Singleton: Database, Auth, MQ, NLP
├── Gateways    → Factory: Inference, Database
├── Services    → Factory: Scenario, Evaluation, Background
└── Models      → DTOs and request/response models
```

- `providers.Singleton` for shared resources; `providers.Factory` for stateless services.
- Wire cross-container deps via `providers.DependenciesContainer()`.

## Error Handling by Layer

- **Gateways**: Catch external errors → translate to domain exceptions
- **Services**: Enforce business rules → raise validation errors
- **Routers**: Map exceptions → HTTP status codes and response formatting
- **Handlers**: Handle MQ failures → retry/dead-letter as appropriate

## Cross-Project Consistency (MANDATORY)

**Structure**: Identical directory layout, naming patterns (`I*Gateway`, `*Service`, `*Manager`), DI patterns, and error handling across all projects.
**Logic**: Domain-specific implementations, test scenarios, and models per project.
**Principle**: Same structure and patterns, different business logic.

## Anti-Patterns

- No business logic in gateways or handlers
- No HTTP concerns in services
- No direct DB access outside gateways
- No hard-coded dependencies — use DI everywhere
- No structural drift between projects

## Important Patterns

- **Dependency Injection**: Uses `dependency-injector` with containers in `src/containers/`
- **Base Models**: `common/models/base_models.py` provides `InputBaseModel` and `OutputBaseModel` for camelCase conversion
- **Environment Variables**: Managed through Pydantic settings in `src/dependencies/config.py`
