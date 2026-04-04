## ADDED Requirements

### Requirement: Scope-first top-level hierarchy
The repo SHALL organise all content under two top-level scope directories: `global/` for machine-wide configs and `project/` for project-scoped configs.

#### Scenario: Global content is findable
- **WHEN** a user wants to deploy configs to `~/.claude/`, `~/.windsurf/`, or global `~/.github/`
- **THEN** all relevant content SHALL be located under `global/`

#### Scenario: Project content is findable
- **WHEN** a user wants to deploy configs to a project's `.claude/`, `.windsurf/`, or `.github/`
- **THEN** all relevant content SHALL be located under `project/`

---

### Requirement: Content type as second-level hierarchy
Within each scope directory, content SHALL be organised by type: `skills/`, `rules/`, `agents/`, `commands/`, `plugins/`.

#### Scenario: All skills are co-located
- **WHEN** a user browses `global/skills/`
- **THEN** they SHALL find all global-scoped skills, grouped by domain

#### Scenario: All rules are co-located
- **WHEN** a user browses `global/rules/`
- **THEN** they SHALL find all global-scoped rules, separated by provider

---

### Requirement: Skills are flat with domain grouping
Skills SHALL be organised as `skills/<group>/<skill-name>/SKILL.md`. Provider scoping SHALL be expressed via the `compatibility` frontmatter field, not via subdirectories.

#### Scenario: Universal skill is accessible to all providers
- **WHEN** a skill has no `compatibility` frontmatter field
- **THEN** it SHALL be treated as compatible with all agentskills.io-supporting providers

#### Scenario: Provider-specific skill is scoped via frontmatter
- **WHEN** a skill has `compatibility: claude-code` in frontmatter
- **THEN** non-Claude providers SHALL ignore it without requiring a separate directory

#### Scenario: Skills within a group are co-located
- **WHEN** a user browses `global/skills/python-development/`
- **THEN** they SHALL find all Python development skills together

---

### Requirement: Rules have universal and provider-specific subdirs
Rules SHALL be organised as `rules/universal/` for AGENTS.md-compatible content and `rules/<provider>/` for provider-specific rules with incompatible frontmatter.

#### Scenario: Universal rules have no frontmatter
- **WHEN** a rule file is placed in `rules/universal/`
- **THEN** it SHALL be plain markdown with no provider-specific frontmatter

#### Scenario: Provider rules use provider-specific frontmatter
- **WHEN** a rule file is placed in `rules/claude-code/`
- **THEN** it MAY use Claude Code-specific frontmatter fields (`paths:`)

#### Scenario: Windsurf rules use Windsurf frontmatter
- **WHEN** a rule file is placed in `rules/windsurf/`
- **THEN** it MAY use Windsurf-specific frontmatter fields (`trigger:`, `globs:`, `description:`)

---

### Requirement: Agents are Claude Code-only
Agents SHALL be organised under `agents/claude-code/` only. No universal agent directory SHALL exist until a cross-provider agent file format is established.

#### Scenario: Agent files are Claude Code scoped
- **WHEN** a user adds a new agent definition
- **THEN** it SHALL be placed under `agents/claude-code/<agent-name>/`

---

### Requirement: Commands are provider-scoped
Commands SHALL be organised under `commands/<provider>/` subdirectories. No universal commands directory SHALL exist as command frontmatter schemas differ per provider.

#### Scenario: OpenSpec commands are Claude-scoped
- **WHEN** a user browses `commands/claude-code/openspec/`
- **THEN** they SHALL find all OpenSpec workflow commands with Claude-specific frontmatter

---

### Requirement: Plugins are provider-scoped
Plugins SHALL be organised under `plugins/<provider>/` subdirectories only.

#### Scenario: Claude plugins are co-located
- **WHEN** a user browses `plugins/claude-code/`
- **THEN** they SHALL find all Claude plugin manifests

#### Scenario: Copilot plugins are co-located
- **WHEN** a user browses `plugins/copilot/`
- **THEN** they SHALL find all Copilot plugin manifests
