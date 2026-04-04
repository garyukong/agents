# Agents Repository

This repository is a content library for skills, agents, commands, and rules for AI development tools. It is **not** a deployment tool - content is distributed through external tools:

- **Skills**: Distributed via `npx skills install garyukong/agents`
- **Rules**: Distributed via rulesync across 10+ providers  
- **Plugins**: Distributed via Claude Code plugin installer
- **Agents & Commands**: Manual deployment to target directories

## Repository Structure

### Content-Type Organization

The repository is organized by content type at the root level. All content is meant for distribution - there's no meaningful distinction between global and project scope for this content library.

**`skills/`** - Universal skill content using the `SKILL.md` format from agentskills.io, supported by Claude Code, Windsurf, and Copilot.

**`rules/`** - Provider-specific rules with incompatible frontmatter schemas:
- `universal/` - AGENTS.md-compatible content (all providers)
- `claude-code/`, `windsurf/`, `copilot/` - Provider-specific rules

**`agents/`** - File-based agent definitions (Claude Code only):
- `claude-code/` - Claude Code agent definitions

**`commands/`** - Provider-specific commands with different frontmatter:
- `claude-code/` - Claude-specific commands
  - `openspec/` - OpenSpec command group

**`plugins/`** - Thin manifests that reference skills:
- `claude-code/` - Claude plugin manifests with skill copies
- `copilot/` - Copilot extensions (placeholder)

### Provider-Specific Conventions

**`claude-code/`** - Claude Code specific content:
- Skills: Universal `SKILL.md` format (compatible across providers)
- Rules: Claude-specific frontmatter and configuration
- Agents: File-based agent definitions (Claude Code only)
- Commands: Claude-specific command frontmatter
- Plugins: Claude plugin manifests with skill references

**`windsurf/`** - Windsurf specific content (placeholder):
- Skills: Universal `SKILL.md` format
- Rules: Windsurf-specific frontmatter
- Commands: Windsurf-specific commands
- Plugins: Windsurf extensions

**`copilot/`** - GitHub Copilot specific content (placeholder):
- Skills: Universal `SKILL.md` format  
- Rules: Copilot-specific frontmatter
- Commands: Copilot-specific commands
- Plugins: Copilot extensions

### Directory Layout

```
skills/                    # Universal skill content
├── python-development/    # Domain-grouped skills
├── llm-application-dev/
├── machine-learning-ops/
├── openspec/
├── unit-testing/
├── windsurf-to-claude-rules/  # Standalone conversion skill
└── integration-test-suite/   # Standalone testing skill

rules/                     # Provider-specific rules
├── universal/             # AGENTS.md-compatible (all providers)
├── claude-code/           # Claude-specific rules
├── windsurf/              # Windsurf rules (placeholder)
└── copilot/               # Copilot rules (placeholder)

agents/                    # Agent definitions
└── claude-code/           # Claude Code only (file-based)

commands/                  # Command definitions  
└── claude-code/           # Claude-specific commands
    └── openspec/          # OpenSpec command group

plugins/                   # Plugin manifests with skill copies
└── claude-code/           # Claude plugin manifests
    ├── python-development/
    ├── llm-application-dev/
    ├── machine-learning-ops/
    ├── openspec/
    └── unit-testing/

openspec/                  # OpenSpec change management
└── changes/               # Change artifacts and workflows
```

## Content Distribution

### Skills Distribution
Skills use the universal `SKILL.md` format from agentskills.io, supported by Claude Code, Windsurf, and Copilot. Install via:

```bash
npx skills install garyukong/agents
```

### Rules Distribution  
Rules are provider-specific due to incompatible frontmatter schemas. Use rulesync for deployment:

```bash
rulesync install universal/global.md --global
rulesync install claude-code/context-mode.md --global --provider claude-code
```

### Plugin Distribution
Plugins are thin manifests that reference skills. Install via Claude Code:

```bash
/plugin install garyukong/agents/plugins/claude-code/python-development
```

## Development Workflow

1. **Skills**: Edit in `skills/<group>/<skill>/`
2. **Rules**: Edit in `rules/<provider>/`  
3. **Agents**: Edit in `agents/claude-code/`
4. **Commands**: Edit in `commands/claude-code/`
5. **Plugins**: Update skill lists in `.claude-plugin/plugin.json`

Plugin skill copies are kept in sync manually (automated sync deferred to follow-on change).

## Migration Notes

This repository was restructured from a flat plugin-centric layout to the current content-type-focused structure. All content has been preserved:

- Skills moved from `plugins/*/skills/` → `skills/<group>/`
- Agents moved from `plugins/*/agents/` → `agents/claude-code/`  
- Commands moved from `plugins/*/commands/` → `commands/claude-code/`
- Rules moved from `rules/` → `rules/` with provider split
- Plugins rebuilt as thin manifests in `plugins/claude-code/`

The `npx skills` installation path remains unchanged - only the source organization has been updated.
