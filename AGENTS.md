# Agents Repository

This repository is a content library for skills, agents, commands, and rules for AI development tools. It is **not** a deployment tool - content is distributed through external tools:

- **Skills**: Distributed via `npx skills install garyukong/agents`
- **Rules**: Distributed via rulesync across 10+ providers  
- **Plugins**: Distributed via Claude Code plugin installer
- **Agents & Commands**: Manual deployment to target directories

## Repository Structure

### Scope Split: `global/` vs `project/`

**`global/`** - Content for machine-wide installation:
- Deploys to `~/.claude/`, `~/.windsurf/`, `~/.github/` 
- Use for shared tools, common patterns, and utilities
- Example: Global Python development standards

**`project/`** - Content for project-specific installation:
- Deploys to `.claude/`, `.windsurf/`, `.github/` in target projects
- Use for project-specific conventions and workflows
- Currently empty - populated as project templates are identified

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
global/
├── skills/                    # Universal skill content
│   ├── python-development/    # Domain-grouped skills
│   ├── llm-application-dev/
│   ├── machine-learning-ops/
│   ├── openspec/
│   ├── unit-testing/
│   ├── windsurf-to-claude-rules/  # Standalone conversion skill
│   └── integration-test-suite/   # Standalone testing skill
├── rules/                     # Provider-specific rules
│   ├── universal/             # AGENTS.md-compatible (all providers)
│   ├── claude-code/           # Claude-specific rules
│   ├── windsurf/              # Windsurf rules (placeholder)
│   └── copilot/               # Copilot rules (placeholder)
├── agents/                    # Agent definitions
│   └── claude-code/           # Claude Code only (file-based)
├── commands/                  # Command definitions  
│   └── claude-code/           # Claude-specific commands
│       └── openspec/          # OpenSpec command group
└── plugins/                   # Plugin manifests with skill copies
    └── claude-code/           # Claude plugin manifests
        ├── python-development/
        ├── llm-application-dev/
        ├── machine-learning-ops/
        ├── openspec/
        └── unit-testing/

project/                       # Project-scoped content (currently empty)
├── skills/
├── rules/
├── agents/
├── commands/
└── plugins/

openspec/                      # OpenSpec change management
└── changes/                   # Change artifacts and workflows
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
/plugin install garyukong/agents/global/plugins/claude-code/python-development
```

## Development Workflow

1. **Skills**: Edit in `global/skills/<group>/<skill>/`
2. **Rules**: Edit in `global/rules/<provider>/`  
3. **Agents**: Edit in `global/agents/claude-code/`
4. **Commands**: Edit in `global/commands/claude-code/`
5. **Plugins**: Update skill lists in `.claude-plugin/plugin.json`

Plugin skill copies are kept in sync manually (automated sync deferred to follow-on change).

## Migration Notes

This repository was restructured from a flat plugin-centric layout to the current scoped structure. All content has been preserved:

- Skills moved from `plugins/*/skills/` → `global/skills/<group>/`
- Agents moved from `plugins/*/agents/` → `global/agents/claude-code/`  
- Commands moved from `plugins/*/commands/` → `global/commands/claude-code/`
- Rules moved from `rules/` → `global/rules/` with provider split
- Plugins rebuilt as thin manifests in `global/plugins/claude-code/`

The `npx skills` installation path remains unchanged - only the source organization has been updated.
