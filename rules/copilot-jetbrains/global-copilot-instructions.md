---
name: "Global Copilot Instructions"
description: "Comprehensive coding standards and instructions for JetBrains IDEs"
---

# Context7 CLI

Use the `ctx7` CLI to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service -- even well-known ones like React, Next.js, Prisma, Express, Tailwind, Django, or Spring Boot. This includes API syntax, configuration, version migration, library-specific debugging, setup instructions, and CLI tool usage. Use even when you think you know the answer -- your training data may not reflect recent changes. Prefer this over web search for library docs.

Do not use for: refactoring, writing scripts from scratch, debugging business logic, code review, or general programming concepts.

## Steps

1. Resolve library: `npx ctx7@latest library <name> "<user's question>"`
2. Pick the best match (ID format: `/org/project`) by: exact name match, description relevance, code snippet count, source reputation (High/Medium preferred), and benchmark score (higher is better). If results don't look right, try alternate names or queries (e.g., "next.js" not "nextjs", or rephrase the question)
3. Fetch docs: `npx ctx7@latest docs <libraryId> "<user's question>"`
4. Answer using the fetched documentation

You MUST call `library` first to get a valid ID unless the user provides one directly in `/org/project` format. Use the user's full question as the query -- specific and detailed queries return better results than vague single words. Do not run more than 3 commands per question. Do not include sensitive information (API keys, passwords, credentials) in queries.

For version-specific docs, use `/org/project/version` from the `library` output (e.g., `/vercel/next.js/v14.3.0`).

If a command fails with a quota error, inform the user and suggest `npx ctx7@latest login` or setting `CONTEXT7_API_KEY` env var for higher limits. Do not silently fall back to training data.

# Python Standards

Always apply skills: `python-code-style`, `python-design-patterns`, `python-project-structure`.
Relevant tasks: `python-configuration`, `python-error-handling`, `python-anti-patterns`.
Unit tests: `python-testing-patterns`.

## Code & Arch Standards

- Python 3.13+, 4-space indent, no tabs, line length 99.
- Follow PEP8 style guide
- Top imports; built-in generics (`list[str]`, `dict[str, Any]`); pipe unions (`str | None`).
- Docstrings: Google-style, `"""` on separate lines. Include `Args`, `Returns`, `Raises`. Mirror module's existing
  docstring structure/phrasing.
- Naming:
    - Classes: `PascalCase` (e.g., `InferenceGateway`).
    - Methods: verb-first `snake_case` (e.g., `extract_models`).
    - Constants: `UPPER_SNAKE_CASE` + `Final`.
    - Private vars/methods: leading `_`.
    - Interfaces: `I` prefix + `ABC` + `@abstractmethod`.
    - Enums: `(str, Enum)`, custom `__new__` + `@property` for multi-value.
- Full type hints; `@override` on overrides.
- SOLID, Zen of Python. Composition > inheritance.
- `@dataclass` > `TypedDict` for structured data with behavior.
- Dependency injection via constructors/interfaces.
- Functions must be class methods (`@staticmethod`/`@classmethod` as needed).
- Group related logic; 1 primary class/file.
- DRY: extract duplicate logic only; split large classes.

## Structure & Config

- Layers: routers → services → gateways (DB/inference/external).
- Contracts: `ABC` + `@abstractmethod` (`I` prefix); `Protocol` for lightweight.
- Routers: group by domain; shared error responses at router. Error boundary maps to HTTP status.
- Models: Pydantic `requests/` & `responses/` per domain; routes need `response_model=`.
- Endpoint docs: Markdown docstrings (renders OpenAPI). Include workflow pos, field desc, examples, return shape.

## Pydantic

- Config: `pydantic_settings.BaseSettings` + `@lru_cache` singleton.
- Pydantic tools: `Field(validation_alias=...)`, `AliasGenerator` (camelCase ↔ snake_case).
- `BaseModel` subclasses for validation/DTOs sharing `model_config`.
- Use `@field_validator`, `@model_validator`, `@computed_field`.

# Python Testing

## Testing

- `pytest` (fixtures/mocks), >90% coverage. 1 test file per module mirroring source dir.
- Unit tests: mock interfaces (`Mock(spec=IService)`). Integration: real implementations.
- `@pytest.mark.asyncio` for async; `AsyncMock(spec=...)` for async contracts.
- Hierarchical `conftest.py`; session scope for expensive setup.
- Parametrized tests: no conditionals in bodies. Split if needed.
- Structure comments: `# Given`, `# When`, `# Then` only.
- Keep mock setup/requests outside `patch` blocks (only side effects & call inside).
- Top imports only. No imports within tests.