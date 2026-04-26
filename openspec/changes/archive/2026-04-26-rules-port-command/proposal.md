## Why

Current rules are manually duplicated across providers (claude-code, windsurf, copilot) with different frontmatter syntaxes, making maintenance error-prone. A port command is needed to automatically convert universal rules to provider-specific syntax, reducing duplication and ensuring consistency.

## What Changes

- Create Python CLI script (`scripts/rules.py`) with a `port` command
- Implement universal frontmatter schema with canonical fields (trigger, name, description, patterns)
- Add provider-specific syntax mapping for claude-code, windsurf, copilot-vscode, copilot-jetbrains
- Support interactive and explicit command modes using questionary
- Use StrEnums for type-safe constants (Provider, TriggerMode, Scope)
- Class-based design with RulesManager encapsulating operations
- Dependencies: click, pyyaml, questionary

**Future phases** (not in this change):
- install/remove/list commands for symlinking rules to projects
- Lock file tracking for installed rules

## Capabilities

### New Capabilities

- `rules-port`: Command-line tool to port universal rules to provider-specific syntax with automatic frontmatter conversion

### Modified Capabilities

None

## Impact

- New script: `scripts/rules.py`
- New dependencies: click, pyyaml, questionary (added via uv)
- Rules directory restructuring required before implementation (universal + provider subdirectories matching windsurf pattern)
- No breaking changes to existing rules workflow
