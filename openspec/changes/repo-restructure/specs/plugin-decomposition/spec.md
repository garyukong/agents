## ADDED Requirements

### Requirement: Skill content lives canonically outside plugins
All skill content SHALL reside in `global/skills/<group>/<skill-name>/`. Plugin directories SHALL NOT contain original skill content.

#### Scenario: Skill is findable without opening a plugin
- **WHEN** a user wants to read or edit a skill
- **THEN** they SHALL find it under `global/skills/` without navigating into any plugin directory

#### Scenario: Plugin does not duplicate skill content
- **WHEN** a plugin directory is inspected
- **THEN** its `skills/` subdirectory SHALL contain only copies referencing the canonical source, not original content

---

### Requirement: Plugin directories are thin manifests
A plugin directory SHALL contain only: a `.claude-plugin/plugin.json` manifest, and a `skills/` directory with physical copies of skills sourced from `global/skills/`.

#### Scenario: Plugin is self-contained for installation
- **WHEN** Claude Code installs a plugin via `/plugin install` using `git-subdir` sparse clone
- **THEN** all required skill files SHALL be present within the plugin directory without requiring access to paths outside it

#### Scenario: Plugin manifest references correct skills
- **WHEN** `plugin.json` is inspected
- **THEN** it SHALL list only skills that exist as physical copies within the plugin's `skills/` subdirectory

---

### Requirement: Plugin-skill-ports directory is removed
The `plugin-skill-ports/` directory SHALL be deleted. Its content SHALL be relocated to `global/agents/claude-code/` or `global/commands/claude-code/` as appropriate.

#### Scenario: No orphaned skill ports remain
- **WHEN** the repo is browsed after restructure
- **THEN** no `plugin-skill-ports/` directory SHALL exist

---

### Requirement: Plugin group names match skill group names
The plugin name under `plugins/claude-code/<name>/` SHALL match the corresponding skill group name under `global/skills/<name>/`.

#### Scenario: Plugin-to-skills relationship is discoverable
- **WHEN** a user finds `plugins/claude-code/python-development/`
- **THEN** the corresponding canonical skills SHALL be at `global/skills/python-development/`
