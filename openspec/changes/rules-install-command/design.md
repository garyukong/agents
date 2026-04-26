## Context

The `rules port` command produces provider-specific rule files in `rules/<provider>/`. Getting these into a target repo currently requires manual file management. Each provider expects rules in a different directory, and copilot requires a filename extension change (`.md` → `.instructions.md`).

Symlinks are preferred over copies so edits in the agents repo propagate immediately without re-running install.

## Goals / Non-Goals

**Goals:**
- Create symlinks from ported rule files into target repo or global config dirs
- Interactive scope selection (global vs project) when `--to` is omitted
- Verify symlink health across all known install locations
- Remove installed symlinks cleanly

**Non-Goals:**
- Installing from universal sources (port first)
- Committing installed symlinks to target repos (local dev concern)
- Lock file or install tracking (check scans known dirs directly)
- Windows support (symlinks not reliable on Windows)

## Decisions

**Symlinks over copies**
Edits in the agents repo reflect immediately in all installed locations. The downside (break if agents repo moves) is mitigated by `rules check`.
Alternative considered: copy on install, but this means re-running install after every port — defeats the purpose.

**Provider inferred from source path**
`rules/claude-code/` → claude-code, `rules/windsurf/` → windsurf, etc. `--provider` flag only needed if source is ambiguous (shouldn't happen in practice given the directory structure).

**Copilot filename transformation at install time**
Source stays `name.md`; symlink target becomes `name.instructions.md`. Transformation is provider-specific logic in `_install_target_name()`.

**No global equivalent for copilot**
`.github/copilot-instructions.md` is repo-scoped by definition. Copilot install is project-only; prompt skips global option for copilot providers.

**`rules check` scans known dirs, no lock file**
Check walks all provider global dirs and any `.claude/rules/`, `.windsurf/rules/`, `.github/instructions/` dirs found under a user-supplied search path (defaults to `~/`). Simple and requires no state.

**Interactive UX mirrors `npx skills`**
When `--to` is omitted: questionary prompt asks global vs project; if project, asks for repo path with path autocomplete.

## Risks / Trade-offs

**Symlinks break if agents repo moves** → Mitigated by `rules check` which surfaces broken links clearly.

**Copilot-vscode and copilot-jetbrains share `.github/instructions/`** → Installing both for the same repo would produce duplicate files. Users should pick one copilot provider per repo (or accept duplicates are identical content).

**`rules check` scan scope** → Without a lock file, check must scan a directory tree to find installed symlinks. Could be slow on large home directories. Mitigated by defaulting scan to known provider dirs only, not arbitrary paths.
