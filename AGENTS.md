# Agents Repository

Content library for skills, agents, commands, rules for AI dev tools. Not deployment tool - content distributed via external tools:

- **Skills**: Distributed via `npx skills`
- **Plugins**: Distributed via Claude Code plugin installer
- **Rules, Agents & Commands**: Manual deployment to target directories

## Repository Structure

### Content-Type Organization

Organized by content type at root level. All content for distribution - no meaningful distinction between global and project scope.

**`skills/`** - Universal skill content using `SKILL.md` format from agentskills.io, supported by Claude Code, Windsurf, Copilot.

**`rules/`** - Provider-specific rules with incompatible frontmatter schemas:

- `universal/` - AGENTS.md-compatible content (all providers)
- `claude-code/`, `windsurf/`, `copilot/` - Provider-specific rules

**`agents/`** - File-based agent definitions (Claude Code only), organized by domain group. No provider subdirectory - all agents Claude Code-specific.

**`commands/`** - Provider-specific commands with different frontmatter, organized by domain group within each provider:

- `universal/` - Provider-agnostic commands
- `claude-code/`, `windsurf/`, `copilot/` - Provider-specific commands

**`plugins/`** - Compiled plugin bundles, one directory per domain group. Each bundles corresponding agents, commands, skills from matching domain group, plus `.claude-plugin/plugin.json` manifest.

> **Domain alignment**: `agents/`, `commands/`, `skills/` use same domain group names. Alignment enables plugin compilation - `package-plugin` skill uses group name to locate and bundle all three artifact types into single plugin directory.

### Directory Layout

```
skills/                    # Universal skill content, domain-grouped
│   └── <group>/
│       └── <skill>/SKILL.md

rules/                     # Provider-specific rules
├── universal/             # AGENTS.md-compatible (all providers)
└── <provider>/            # claude-code, windsurf, copilot

agents/                    # Agent definitions (Claude Code only)
└── <group>/               # Matches plugin domain group name

commands/                  # Command definitions
├── claude-code/
│   └── <group>/           # Matches plugin domain group name
└── universal/
    └── <group>/           # e.g. opsx

plugins/                   # Compiled plugin bundles
└── <group>/               # Matches agents/commands/skills group name
    ├── .claude-plugin/plugin.json
    ├── agents/
    ├── commands/
    └── skills/

openspec/                  # OpenSpec change management
└── changes/
```

## Content Distribution

### Skills Distribution

Skills use universal `SKILL.md` format from agentskills.io, supported by Claude Code, Windsurf, Copilot. Install via:

```bash
npx skills install garyukong/agents
```

### Rules Distribution

Rules provider-specific due to incompatible frontmatter schemas.

#### Rules Port Command

Use the `rules` CLI to port universal rules to provider-specific formats. The `rules` entrypoint is registered in `pyproject.toml`, so invoke it directly via `uv run rules`:

```bash
# Interactive mode
uv run rules port

# Port to specific provider
uv run rules port universal/my-rule.md --to claude-code

# Port to all providers
uv run rules port universal/my-rule.md --to all

# Dry run preview
uv run rules port universal/my-rule.md --to windsurf --dry-run

# Port entire directory
uv run rules port universal/my-dir --to all
```

#### Universal Frontmatter Schema

Universal rules use a canonical frontmatter schema:

```yaml
---
trigger: glob | always_on | model_decision | manual
name: "Rule Name"
description: "Rule description"
patterns:
  - "**/*.py"
  - "pyproject.toml"
---
Rule body content here
```

- `trigger`: Activation mode (glob for pattern-based, always_on for constant)
- `patterns`: YAML list of file glob patterns (required for glob trigger)
- `name`, `description`: Optional metadata fields

**Provider-Specific Mappings**

- **claude-code**: Converts patterns to `paths:` YAML list (glob trigger only; always_on/model_decision/manual produce no frontmatter)
- **windsurf**: Converts patterns to space-separated `globs:` string with `trigger:`
- **copilot-vscode**: Converts to `applyTo:` with `name:` and `description:`
- **copilot-jetbrains**: Strips all frontmatter (plain markdown only)

Unsupported modes (model_decision, manual) convert to always-on (no pattern fields).

#### Common Use Cases

**Port a Python-related rule to all providers:**

```bash
uv run rules port universal/python-standards.md --to all
```

**Port all rules in a directory:**

```bash
uv run rules port universal/ --to claude-code
```

**Preview before porting:**

```bash
uv run rules port universal/my-rule.md --to windsurf --dry-run
```

**Interactive selection:**

```bash
uv run rules port
# Follow prompts to select source and target
```

### Plugin Distribution

Plugins thin manifests referencing skills. Install via Claude Code plugin installer using marketplace at `.claude-plugin/marketplace.json`.

## Development Workflow

1. **Skills**: Edit in `skills/<group>/<skill>/`
2. **Rules**: Edit in `rules/<provider>/`
3. **Agents**: Edit in `agents/<group>/`
4. **Commands**: Edit in `commands/claude-code/<group>/` or `commands/universal/<group>/`
5. **Plugins**: After updating agents, commands, or skills, run `package-plugin` skill to sync changes into `plugins/<name>/` and update `marketplace.json`