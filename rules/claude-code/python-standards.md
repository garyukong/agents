---
paths:
  - "**/*.py"
  - "pyproject.toml"
  - "requirements*.txt"
  - "setup.py"
  - "Pipfile"
  - "poetry.lock"
  - "uv.lock"
---

Always apply skills: `python-code-style`, `python-design-patterns`, `python-project-structure`.
Relevant tasks: `python-configuration`, `python-error-handling`, `python-anti-patterns`.
Unit tests: `python-testing-patterns`.

## Code & Arch Standards

- Python 3.13+, 4-space indent, no tabs, line length 99.
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