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

- Lib Docs: `mcp_context7_**resolve-library-id` -> `mcp_context7_**_query-docs` -> `search_web`.
- Jira: `mcp_atlassian_*_get_issue` / `mcp_atlassian_*_get_epic_issues` -> `mcp_atlassian_*_search`.
- Confluence: `mcp_atlassian_*_get_page` -> `mcp_atlassian_*_search`.

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
