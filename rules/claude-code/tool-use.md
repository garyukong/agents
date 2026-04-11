## Tool Guidelines

**Docs/Integrations**

- Lib Docs: ``mcp_docs_**resolve-library-id` -> `mcp_docs**_query-docs` -> `search_web`.`
- Web: `search_web`. Alt: `read_url_content` (needs approval).
- Jira: `mcp_atlassian_*_get_issue` / `mcp_atlassian_*_get_epic_issues` -> `mcp_atlassian_*_search`.
- Confluence: `mcp_atlassian_*_get_page` -> `mcp_atlassian_*_search`.

**JetBrains MCP — use over built-ins when semantics matter** *(only when running inside a JetBrains IDE)*

When Claude Code is running inside a JetBrains IDE, prefer these tools because they understand code structure, not just
text. Skip this if not in a JetBrains IDE.

| Task                                   | Use instead of                                                                               |
|----------------------------------------|----------------------------------------------------------------------------------------------|
| Renaming a symbol (var, fn, class)     | Grep + Edit — use `mcp__jetbrains__rename_refactoring` (scope-aware, updates all references) |
| Checking a file for errors/warnings    | Nothing — use `mcp__jetbrains__get_file_problems` (runs IntelliJ inspections)                |
| Getting a symbol's type/signature/docs | Grep — use `mcp__jetbrains__get_symbol_info` (semantic Quick Docs)                           |
| Formatting a file                      | Manual edit — use `mcp__jetbrains__reformat_file` (applies project code style)               |
| Finding a file by name fragment        | Glob — use `mcp__jetbrains__find_files_by_name_keyword` (IDE-indexed, fuzzy, faster)         |

Always use the absolute path as `projectPath` parameter.