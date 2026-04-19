## Context

Current rules directory has provider-specific frontmatter syntaxes that must be manually maintained:
- claude-code: uses `globs:` with comma-separated unquoted patterns
- windsurf: uses `trigger:` and `globs:` with space-separated patterns
- copilot-vscode: uses `name:`, `description:`, `applyTo:`
- copilot-jetbrains: no frontmatter (plain markdown)

This manual duplication is error-prone. The windsurf directory already has the target structure (global_rules.md + project subdirs), but other providers need restructuring.

## Goals / Non-Goals

**Goals:**
- Create a canonical universal frontmatter schema that works for all providers
- Implement automatic conversion from universal to provider-specific syntax
- Support both interactive and explicit CLI modes
- Provide type-safe constants using StrEnums
- Encapsulate operations in a RulesManager class

**Non-Goals:**
- Symlinking rules to projects (future phase: install/remove/list commands)
- Lock file tracking (future phase)
- Automatic re-porting when universal rules change (manual trigger only)

## Decisions

**Universal frontmatter schema:**
- Use `trigger`, `name`, `description`, `patterns` as canonical fields
- `patterns` is a YAML list for consistency, converted to provider-specific formats during port
- Chosen over separate `globs`/`paths`/`applyTo` fields because they represent the same concept (file patterns)

**Provider mapping strategy:**
- Unsupported activation modes (model_decision, manual) convert to always-on (no pattern fields)
- This keeps implementation simple and avoids complex fallback logic
- Alternative considered: skip unsupported modes, but this would silently drop rules

**CLI framework:**
- Use click for CLI structure (familiar, well-documented)
- Use questionary for interactive prompts (better UX than click's built-in prompts)
- Chosen over pure click because questionary provides fuzzy search, nicer styling

**Class-based design:**
- RulesManager class encapsulates all file operations and conversions
- StrEnums for Provider, TriggerMode, Scope provide type safety
- Chosen over functional design to keep related operations organized and testable

**Dependencies:**
- click: CLI framework
- pyyaml: YAML frontmatter parsing
- questionary: Interactive prompts
- All added via uv for Python package management

## Risks / Trade-offs

**Risk:** Universal frontmatter may not perfectly map to all provider capabilities
- **Mitigation:** Document unsupported mode conversions clearly; users can manually edit provider-specific rules if needed

**Risk:** Rules directory restructuring required before port command works
- **Mitigation:** Add clear error message if expected structure not found; document restructuring steps in AGENTS.md

**Trade-off:** Unsupported modes convert to always-on rather than skipping
- **Rationale:** Better to have rule present than silently dropped; users can manually remove if unwanted

## Open Questions

None
