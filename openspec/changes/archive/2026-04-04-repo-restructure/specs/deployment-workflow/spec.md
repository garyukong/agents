## ADDED Requirements

### Requirement: Skills are deployed via npx skills
Skills SHALL be deployed to target environments using `npx skills install <source>`. This repo SHALL remain compatible with `npx skills install garyukong/agents`.

#### Scenario: Skills install to universal discovery path
- **WHEN** a user runs `npx skills install garyukong/agents`
- **THEN** skills SHALL be installed into `.agents/skills/` at the target scope (global or project)

#### Scenario: skills-lock.json tracks installed skills
- **WHEN** skills are installed
- **THEN** `skills-lock.json` SHALL be updated to reflect installed skill sources and hashes

---

### Requirement: Rules are deployed via rulesync
> **TBD** — rulesync integration approach not yet decided.

#### Scenario: TBD
- **WHEN** TBD
- **THEN** TBD

---

### Requirement: Scope determines deploy destination
> **TBD** — deploy tooling for agents/commands not yet decided (deferred to deploy skill follow-on change).

#### Scenario: TBD
- **WHEN** TBD
- **THEN** TBD

---

### Requirement: Plugin deployment uses the Claude plugin installer
Claude plugins SHALL be installed using the Claude Code plugin system (marketplace or `/plugin install`). Plugins SHALL NOT require a separate deploy step.

#### Scenario: Plugin installs without external tooling
- **WHEN** a user installs a plugin from `plugins/claude-code/`
- **THEN** Claude Code SHALL install it via its native plugin mechanism without requiring rulesync or npx skills
