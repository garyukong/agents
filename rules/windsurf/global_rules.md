# Global Rules

Project rules override conflicts.
Persona: `python-pro`.
Apply skills: `python-code-style`, `python-design-patterns`, `python-project-structure`. Relevant tasks:
`python-configuration`, `python-error-handling`, `python-anti-patterns`. Unit tests: `python-testing-patterns`.

## Rules & Practices

- Avoid hard-coded secrets/API keys.
- Avoid non-parameterised queries.
- Logging: structured via `loguru`; mask sensitive data.
- Async context managers for connection lifecycles. Async generators for scoped resources (DB commit/rollback).
- `async/await` for all I/O.
- Standard library > extra dependencies.

## Tool Guidelines

**Fail fast:** Tool fails → state reason briefly, switch fallback immediately. Avoid retrying same failing call.

**JetBrains MCP vs. Built-in Cascade tools**

**File Management:** Prefer Windsurf built-ins (`read_file`, `edit`, `multi_edit`, `write_to_file`, `grep`, `find_by_name`, `list_dir`). User sees changes.

**Code Structure:** Prefer JetBrains MCP when structure matters over text:

| Task                                   | Instead of (built-ins) | Preferred (JetBrains)                                                      |
|----------------------------------------|------------------------|----------------------------------------------------------------------------|
| Renaming a symbol (var, fn, class)     | `Grep` + `edit` | `<mcp_jetbrains>_rename_refactoring` (scope-aware, updates all references) |
| Formatting a file                      | `edit` (manual)        | `<mcp_jetbrains>_reformat_file` (applies project code style)               |
| Finding a file by name fragment        | `find_by_name` (glob)  | `<mcp_jetbrains>_find_files_by_name_keyword` (IDE-indexed, fuzzy, faster)  |
| Finding a class/function definition    | `Grep`          | `<mcp_jetbrains>_search_symbol` (semantic, IDE-indexed)                    |
| Checking a file for errors/warnings    | No built-in equivalent | `<mcp_jetbrains>_get_file_problems` (runs IntelliJ inspections)            |

**Docs/Integrations**

- Lib Docs: ``mcp_context7_**resolve-library-id` -> `mcp_context7_**_query-docs` -> `search_web` / context-mode tools
- Web: `search_web` / context-mode tools.
- Jira: `mcp_atlassian_*_get_issue` / `mcp_atlassian_*_get_epic_issues` -> `mcp_atlassian_*_search`.
- Confluence: `mcp_atlassian_*_get_page` -> `mcp_atlassian_*_search`.

# context-mode — MANDATORY routing rules

Context-mode MCP tools protect context window. Single unrouted command dumps 56 KB, wastes session. No hooks in Cascade — these rules only enforcement. Follow strictly.

## BLOCKED commands — do NOT use these

### curl / wget — FORBIDDEN

Avoid `curl`/`wget` via `bash`. Raw HTTP floods context.

Instead use:

- `mcp*__ctx_fetch_and_index(url, source)` — fetch + index web pages
- `mcp*__ctx_execute(language: "javascript", code: "const r = await fetch(...)")` — HTTP in sandbox

### Inline HTTP — FORBIDDEN

Avoid inline HTTP via `bash` with `node -e "fetch(..."`, `python -c "requests.get(..."`. Bypasses sandbox, floods context.

Use:

- `mcp*__ctx_execute(language, code)` — only stdout enters context

### Direct web fetching — FORBIDDEN

Avoid `read_url_content` for large pages. Raw HTML can exceed 100 KB.

Use:

- `mcp*__ctx_fetch_and_index(url, source)` then `mcp*__ctx_search(queries)` to query indexed content

## REDIRECTED tools — use sandbox equivalents

### Shell (>20 lines output)

`bash` ONLY for: `git`, `mkdir`, `rm`, `mv`, `cd`, `ls`, `npm install`, `pip install`, short-output commands.
All else:

- `mcp*__ctx_batch_execute(commands, queries)` — multiple commands + search in ONE call
- `mcp*__ctx_execute(language: "shell", code: "...")` — sandbox, only stdout enters context

### File reading (for analysis)

If reading file to:
- **edit** → `read_file` / `edit` or `multi_edit` (content needed in context).
- **analyse/explore/summarise** → `mcp*__ctx_execute_file(path, language, code)`. Only printed summary enters context.

### Search (large results)

Use `mcp*__ctx_execute(language: "shell", code: "grep ...")`. Only printed summary enters context.

## Tool selection hierarchy

1. **GATHER**: `mcp*__ctx_batch_execute(commands, queries)` — primary. Runs commands, auto-indexes, returns search results. ONE call replaces 30+.
2. **FOLLOW-UP**: `mcp*__ctx_search(queries: ["q1", "q2", ...])` — query indexed content. All questions in ONE call.
3. **PROCESSING**: `mcp*__ctx_execute(language, code)` | `mcp*__ctx_execute_file(path, language, code)` — sandbox. Only stdout enters context.
4. **WEB**: `mcp*__ctx_fetch_and_index(url, source)` then `mcp*__ctx_search(queries)` — raw HTML never enters context.
5. **INDEX**: `mcp*__ctx_index(content, source)` — store in FTS5 knowledge base for later search.

## Output constraints

- Responses under 500 words.
- Artifacts (code, configs) to FILES — never inline. Return: file path + 1-line description.
- Use descriptive source labels when indexing so others can `search(source: "label")` later.

# RTK - Rust Token Killer (Windsurf)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Prefix all shell commands with `rtk`.

Examples:

```bash
rtk git <command>
rtk gh <command>
rtk uv <command>
rtk poetry <command>
rtk ls
rtk grep
rtk bats
rtk cat
rtk find
rtk tree
rtk npx
rtk openspec
```

## Meta-Commands

```bash
rtk gain              # Show token savings
rtk gain --history    # Command history with savings
rtk discover          # Find missed RTK opportunities
rtk proxy <cmd>       # Run raw (no filtering, for debugging)
```

## Why

RTK filters + compresses command output before LLM context. Saves 60-90% tokens on common ops. Use `rtk <cmd>` over raw commands.