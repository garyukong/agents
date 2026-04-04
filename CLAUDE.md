# Agents Repository

This repository is a content library for skills, agents, commands, and rules for AI development tools. It is **not** a
deployment tool - content is distributed through external tools:

- **Skills**: Distributed via `npx skills`
- **Plugins**: Distributed via Claude Code plugin installer
- **Rules, Agents & Commands**: Manual deployment to target directories

## Repository Structure

### Content-Type Organization

The repository is organized by content type at the root level. All content is meant for distribution - there's no
meaningful distinction between global and project scope for this content library.

**`skills/`** - Universal skill content using the `SKILL.md` format from agentskills.io, supported by Claude Code,
Windsurf, and Copilot.

**`rules/`** - Provider-specific rules with incompatible frontmatter schemas:

- `universal/` - AGENTS.md-compatible content (all providers)
- `claude-code/`, `windsurf/`, `copilot/` - Provider-specific rules

**`agents/`** - File-based agent definitions (Claude Code only), organized by domain group. No provider subdirectory —
all agents are Claude Code-specific.

**`commands/`** - Provider-specific commands with different frontmatter, organized by domain group within each provider:

- `universal/` - Provider-agnostic commands
- `claude-code/`, `windsurf/`, `copilot/` - Provider-specific commands

**`plugins/`** - Compiled plugin bundles, one directory per domain group. Each bundles the corresponding agents,
commands, and skills from the matching domain group, plus a `.claude-plugin/plugin.json` manifest.

> **Domain alignment**: `agents/`, `commands/`, and `skills/` all use the same domain group names. This alignment is
> what makes plugin compilation possible — the `package-plugin` skill uses the group name to locate and bundle all three
> artifact types into a single plugin directory.

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

Skills use the universal `SKILL.md` format from agentskills.io, supported by Claude Code, Windsurf, and Copilot. Install
via:

```bash
npx skills install garyukong/agents
```

### Rules Distribution

Rules are provider-specific due to incompatible frontmatter schemas.

### Plugin Distribution

Plugins are thin manifests that reference skills. Install via Claude Code plugin installer using the marketplace at
`.claude-plugin/marketplace.json`.

## Development Workflow

1. **Skills**: Edit in `skills/<group>/<skill>/`
2. **Rules**: Edit in `rules/<provider>/`
3. **Agents**: Edit in `agents/<group>/`
4. **Commands**: Edit in `commands/claude-code/<group>/` or `commands/universal/<group>/`
5. **Plugins**: After updating agents, commands, or skills, run the `package-plugin` skill to sync changes into
   `plugins/<name>/` and update `marketplace.json`