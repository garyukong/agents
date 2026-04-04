# Global Rules

Project rules override conflicts.
Persona: `python-pro`.
Apply skills: `python-code-style`, `python-design-patterns`, `python-project-structure`. Relevant tasks: `python-configuration`, `python-error-handling`, `python-anti-patterns`. Unit tests: `python-testing-patterns`.

## Code & Arch Standards

- Python 3.13+, 4-space indent, no tabs, line length 99.
- Top imports; built-in generics (`list[str]`, `dict[str, Any]`); pipe unions (`str | None`).
- Docstrings: Google-style, `"""` on separate lines. Include `Args`, `Returns`, `Raises`. Mirror module's existing docstring structure/phrasing.
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
- Logging: structured via `loguru`; mask sensitive data.
- Async context managers for connection lifecycles. Async generators for scoped resources (DB commit/rollback).
- `async/await` for all I/O.
- Standard library > extra dependencies.
- Branching: <JIRA-KEY>-<kebab-description>.
- Commits: conventional commit format — `type(scope): description` (e.g., `feat(tracing): add prompt identifiers`).

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

**Docs/Integrations**

- Lib Docs: ``mcp_docs_**resolve-library-id` -> `mcp_docs**_query-docs` -> `search_web`.`
- Web: `search_web`. Alt: `read_url_content` (needs approval).
- Jira: `mcp_atlassian_*_get_issue` / `mcp_atlassian_*_get_epic_issues` -> `mcp_atlassian_*_search`.
- Confluence: `mcp_atlassian_*_get_page` -> `mcp_atlassian_*_search`.

**JetBrains MCP — use over built-ins when semantics matter** *(only when running inside a JetBrains IDE)*

When Claude Code is running inside a JetBrains IDE (IntelliJ, PyCharm, etc.), prefer these tools because they understand code structure, not just text. Skip this section entirely if not in a JetBrains IDE.

| Task | Use instead of |
|------|---------------|
| Renaming a symbol (var, fn, class) | Grep + Edit — use `mcp__jetbrains__rename_refactoring` (scope-aware, updates all references) |
| Checking a file for errors/warnings | Nothing — use `mcp__jetbrains__get_file_problems` (runs IntelliJ inspections) |
| Getting a symbol's type/signature/docs | Grep — use `mcp__jetbrains__get_symbol_info` (semantic Quick Docs) |
| Formatting a file | Manual edit — use `mcp__jetbrains__reformat_file` (applies project code style) |
| Finding a file by name fragment | Glob — use `mcp__jetbrains__find_files_by_name_keyword` (IDE-indexed, faster) |

Always use the absolute path as `projectPath` parameter.

# context-mode — MANDATORY routing rules

You have context-mode MCP tools available. These rules are NOT optional — they protect your context window from flooding. A single unrouted command can dump 56 KB into context and waste the entire session.

## BLOCKED commands — do NOT attempt these

### curl / wget — BLOCKED

Any Bash command containing `curl` or `wget` is intercepted and replaced with an error message. Do NOT retry.
Instead use:

- `ctx_fetch_and_index(url, source)` to fetch and index web pages
- `ctx_execute(language: "javascript", code: "const r = await fetch(...)")` to run HTTP calls in sandbox

### Inline HTTP — BLOCKED

Any Bash command containing `fetch('http`, `requests.get(`, `requests.post(`, `http.get(`, or `http.request(` is intercepted and replaced with an error message. Do NOT retry with Bash.
Instead use:

- `ctx_execute(language, code)` to run HTTP calls in sandbox — only stdout enters context

### WebFetch — BLOCKED

WebFetch calls are denied entirely. The URL is extracted and you are told to use `ctx_fetch_and_index` instead.
Instead use:

- `ctx_fetch_and_index(url, source)` then `ctx_search(queries)` to query the indexed content

## REDIRECTED tools — use sandbox equivalents

### Bash (>20 lines output)

Bash is ONLY for: `git`, `mkdir`, `rm`, `mv`, `cd`, `ls`, `npm install`, `pip install`, and other short-output commands.
For everything else, use:

- `ctx_batch_execute(commands, queries)` — run multiple commands + search in ONE call
- `ctx_execute(language: "shell", code: "...")` — run in sandbox, only stdout enters context

### Read (for analysis)

If you are reading a file to **Edit** it → Read is correct (Edit needs content in context).
If you are reading to **analyze, explore, or summarize** → use `ctx_execute_file(path, language, code)` instead. Only your printed summary enters context. The raw file content stays in the sandbox.

### Grep (large results)

Grep results can flood context. Use `ctx_execute(language: "shell", code: "grep ...")` to run searches in sandbox. Only your printed summary enters context.

## Tool selection hierarchy

1. **GATHER**: `ctx_batch_execute(commands, queries)` — Primary tool. Runs all commands, auto-indexes output, returns search results. ONE call replaces 30+ individual calls.
2. **FOLLOW-UP**: `ctx_search(queries: ["q1", "q2", ...])` — Query indexed content. Pass ALL questions as array in ONE call.
3. **PROCESSING**: `ctx_execute(language, code)` | `ctx_execute_file(path, language, code)` — Sandbox execution. Only stdout enters context.
4. **WEB**: `ctx_fetch_and_index(url, source)` then `ctx_search(queries)` — Fetch, chunk, index, query. Raw HTML never enters context.
5. **INDEX**: `ctx_index(content, source)` — Store content in FTS5 knowledge base for later search.

## Subagent routing

When spawning subagents (Agent/Task tool), the routing block is automatically injected into their prompt. Bash-type subagents are upgraded to general-purpose so they have access to MCP tools. You do NOT need to manually instruct subagents about context-mode.

## Output constraints

- Keep responses under 500 words.
- Write artifacts (code, configs, PRDs) to FILES — never return them as inline text. Return only: file path + 1-line description.
- When indexing content, use descriptive source labels so others can `ctx_search(source: "label")` later.

## ctx commands

| Command | Action |
|---------|--------|
| `ctx stats` | Call the `ctx_stats` MCP tool and display the full output verbatim |
| `ctx doctor` | Call the `ctx_doctor` MCP tool, run the returned shell command, display as checklist |
| `ctx upgrade` | Call the `ctx_upgrade` MCP tool, run the returned shell command, display as checklist |
