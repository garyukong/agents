# Global Rules

Project rules override conflicts.
Persona: `python-pro`.
Apply skills: `python-code-style`, `python-design-patterns`, `python-project-structure`. Relevant tasks:
`python-configuration`, `python-error-handling`, `python-anti-patterns`. Unit tests: `python-testing-patterns`.

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
- Config: `pydantic_settings.BaseSettings` + `@lru_cache` singleton.
- Pydantic tools: `Field(validation_alias=...)`, `AliasGenerator` (camelCase ↔ snake_case).
- `BaseModel` subclasses for validation/DTOs sharing `model_config`.
- Use `@field_validator`, `@model_validator`, `@computed_field`.

## Rules & Practices

- NEVER hard-code secrets/API keys.
- NEVER use non-parameterized queries.
- NEVER leak domain exceptions past routers. Custom exception hierarchies per domain.
- NEVER commit changes directly to main branch. Always create a feature branch with the format
  `<JIRA-KEY>-<kebab-description>`.
- Logging: structured via `loguru`; mask sensitive data.
- Async context managers for connection lifecycles. Async generators for scoped resources (DB commit/rollback).
- `async/await` for all I/O.
- Standard library > extra dependencies.

## Testing

- `pytest` (fixtures/mocks), >90% coverage. 1 test file per module mirroring source dir.
- Unit tests: mock interfaces (`Mock(spec=IService)`). Integration: real impls.
- `@pytest.mark.asyncio` for async; `AsyncMock(spec=...)` for async contracts.
- Hierarchical `conftest.py`; session scope for expensive setup.
- Parametrized tests: no conditionals in bodies. Split if needed.
- Structure comments: `# Given`, `# When`, `# Then` only.
- Keep mock setup/requests outside `patch` blocks (only side effects & call inside).
- Top imports only. No imports within tests.

## Tool Guidelines

**Fail fast:** If a tool fails, state reason briefly, switch to fallback immediately. DO NOT retry exact same failing
call.

**JetBrains MCP vs. Built-in Cascade tools**

**File Management:** Always prefer Windsurf's built-in tools (`read_file`, `edit`, `multi_edit`, `write_to_file`,
`grep_search`, `find_by_name`, `list_dir`) for file operations. These allow the user to see changes being made.

**Code Structure:** Prefer JetBrains MCP tools when they understand code structure better than text:

| Task                                | Instead of (built-ins) | Preferred (JetBrains)                                                      |
|-------------------------------------|------------------------|----------------------------------------------------------------------------|
| Renaming a symbol (var, fn, class)  | `grep_search` + `edit` | `<mcp_jetbrains>_rename_refactoring` (scope-aware, updates all references) |
| Checking a file for errors/warnings | No built-in equivalent | `<mcp_jetbrains>_get_file_problems` (runs IntelliJ inspections)            |
| Formatting a file                   | `edit` (manual)        | `<mcp_jetbrains>_reformat_file` (applies project code style)               |

**Docs/Integrations**

- Lib Docs: ``mcp_context7_**resolve-library-id` -> `mcp_context7_**_query-docs` -> `search_web` / context-mode tools
- Web: `search_web` / context-mode tools.
- Jira: `mcp_atlassian_*_get_issue` / `mcp_atlassian_*_get_epic_issues` -> `mcp_atlassian_*_search`.
- Confluence: `mcp_atlassian_*_get_page` -> `mcp_atlassian_*_search`.

# context-mode — MANDATORY routing rules

You have context-mode MCP tools available. These rules are NOT optional — they protect your context window from
flooding. A single unrouted command can dump 56 KB into context and waste the entire session. Cascade does not yet
support context-mode hooks, so these instructions are your ONLY enforcement mechanism. Follow them strictly.

## BLOCKED commands — do NOT use these

### curl / wget — FORBIDDEN

Do NOT use `curl` or `wget` via `bash` directly. They dump raw HTTP responses directly into your context window.
Instead use:

- `mcp__context-mode__ctx_fetch_and_index(url, source)` to fetch and index web pages
- `mcp__context-mode__ctx_execute(language: "javascript", code: "const r = await fetch(...)")` to run HTTP calls in
  sandbox

### Inline HTTP — FORBIDDEN

Do NOT run inline HTTP calls via `bash` with `node -e "fetch(..."`, `python -c "requests.get(..."`, or similar patterns.
They bypass the sandbox and flood context.
Instead use:

- `mcp__context-mode__ctx_execute(language, code)` to run HTTP calls in sandbox — only stdout enters context

### Direct web fetching — FORBIDDEN

Do NOT use `read_url_content` for large pages. Raw HTML can exceed 100 KB.
Instead use:

- `mcp__context-mode__ctx_fetch_and_index(url, source)` then `mcp__context-mode__ctx_search(queries)` to query the
  indexed content

## REDIRECTED tools — use sandbox equivalents

### Shell (>20 lines output)

`bash` is ONLY for: `git`, `mkdir`, `rm`, `mv`, `cd`, `ls`, `npm install`, `pip install`, and other short-output
commands.
For everything else, use:

- `mcp__context-mode__ctx_batch_execute(commands, queries)` — run multiple commands + search in ONE call
- `mcp__context-mode__ctx_execute(language: "shell", code: "...")` — run in sandbox, only stdout enters context

### File reading (for analysis)

If you are reading a file to **edit** it → `view_file` / `replace_file_content` is correct (edit needs content in
context).
If you are reading to **analyze, explore, or summarize** → use
`mcp__context-mode__ctx_execute_file(path, language, code)` instead. Only your printed summary enters context. The raw
file stays in the sandbox.

### Search (large results)

Search results can flood context. Use `mcp__context-mode__ctx_execute(language: "shell", code: "grep ...")` to run
searches in sandbox. Only your printed summary enters context.

## Tool selection hierarchy

1. **GATHER**: `mcp__context-mode__ctx_batch_execute(commands, queries)` — Primary tool. Runs all commands, auto-indexes
   output, returns search results. ONE call replaces 30+ individual calls.
2. **FOLLOW-UP**: `mcp__context-mode__ctx_search(queries: ["q1", "q2", ...])` — Query indexed content. Pass ALL
   questions as array in ONE call.
3. **PROCESSING**: `mcp__context-mode__ctx_execute(language, code)` |
   `mcp__context-mode__ctx_execute_file(path, language, code)` — Sandbox execution. Only stdout enters context.
4. **WEB**: `mcp__context-mode__ctx_fetch_and_index(url, source)` then `mcp__context-mode__ctx_search(queries)` — Fetch,
   chunk, index, query. Raw HTML never enters context.
5. **INDEX**: `mcp__context-mode__ctx_index(content, source)` — Store content in FTS5 knowledge base for later search.

## Output constraints

- Keep responses under 500 words.
- Write artifacts (code, configs) to FILES — never return them as inline text. Return only: file path + 1-line
  description.
- When indexing content, use descriptive source labels so others can `search(source: "label")` later.
