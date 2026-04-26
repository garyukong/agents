## ADDED Requirements

### Requirement: Install rule via symlink
The system SHALL create a symlink from a ported provider-specific rule file into the appropriate target directory for the given provider and scope.

#### Scenario: Explicit project install
- **WHEN** `rules install rules/claude-code/my-rule.md --to ~/projects/my-repo` is run
- **THEN** the system SHALL create a symlink at `~/projects/my-repo/.claude/rules/my-rule.md` pointing to the source file

#### Scenario: Explicit project install for copilot provider
- **WHEN** `rules install rules/copilot-vscode/my-rule.md --to ~/projects/my-repo` is run
- **THEN** the system SHALL create a symlink at `~/projects/my-repo/.github/instructions/my-rule.instructions.md` pointing to the source file

#### Scenario: Target directory created if missing
- **WHEN** the target provider directory does not exist
- **THEN** the system SHALL create it before creating the symlink

#### Scenario: Scope inferred from global/ subdirectory
- **WHEN** source path contains a `global/` segment (e.g. `rules/claude-code/global/my-rule.md`)
- **THEN** the system SHALL infer scope as global and install without prompting

#### Scenario: Scope inferred from named project subdirectory
- **WHEN** source path contains a non-`global/` named subdirectory (e.g. `rules/claude-code/oms-ml-semantics/my-rule.md`) and `--to` is omitted
- **THEN** the system SHALL prompt for a target repo path only

#### Scenario: Interactive scope prompt when scope ambiguous
- **WHEN** source path has no subdirectory and `--to` is omitted
- **THEN** the system SHALL prompt the user to select global or project scope

#### Scenario: Interactive project scope
- **WHEN** the user selects project scope in the interactive prompt
- **THEN** the system SHALL prompt for a target repo path
- **THEN** the symlink SHALL be created at `<repo>/.claude/rules/my-rule.md`

#### Scenario: Copilot provider has no global scope
- **WHEN** installing a copilot-vscode or copilot-jetbrains rule interactively
- **THEN** the system SHALL NOT offer global as a scope option

#### Scenario: Install directory of rules
- **WHEN** `rules install rules/windsurf/global/ --to ~/projects/my-repo` is run
- **THEN** the system SHALL create symlinks for all `.md` files in the directory

#### Scenario: Provider inferred from source path
- **WHEN** source path begins with `rules/claude-code/`
- **THEN** the system SHALL infer provider as `claude-code` without requiring `--provider`

### Requirement: Install target paths per provider
The system SHALL map each provider to a fixed target directory structure.

#### Scenario: claude-code project target
- **WHEN** provider is `claude-code` and scope is project
- **THEN** target directory SHALL be `<repo>/.claude/rules/`

#### Scenario: windsurf project target
- **WHEN** provider is `windsurf` and scope is project
- **THEN** target directory SHALL be `<repo>/.windsurf/rules/`

#### Scenario: copilot project target
- **WHEN** provider is `copilot-vscode` or `copilot-jetbrains` and scope is project
- **THEN** target directory SHALL be `<repo>/.github/instructions/`

#### Scenario: claude-code global target
- **WHEN** provider is `claude-code` and scope is global
- **THEN** target directory SHALL be `~/.claude/rules/`

#### Scenario: windsurf global target
- **WHEN** provider is `windsurf` and scope is global
- **THEN** target directory SHALL be `~/.windsurf/rules/`
