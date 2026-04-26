## ADDED Requirements

### Requirement: Remove installed symlink
The system SHALL remove a symlink previously created by `rules install`.

#### Scenario: Explicit project remove
- **WHEN** `rules remove rules/claude-code/my-rule.md --from ~/projects/my-repo` is run
- **THEN** the system SHALL remove the symlink at `~/projects/my-repo/.claude/rules/my-rule.md`

#### Scenario: Interactive scope selection
- **WHEN** `rules remove rules/windsurf/my-rule.md` is run without `--from`
- **THEN** the system SHALL prompt the user to select global or project scope
- **THEN** remove the corresponding symlink

#### Scenario: Symlink not found
- **WHEN** no symlink exists at the resolved target path
- **THEN** the system SHALL print an error and exit with a non-zero code

#### Scenario: Remove directory of rules
- **WHEN** `rules remove rules/claude-code/my-dir/ --from ~/projects/my-repo` is run
- **THEN** the system SHALL remove symlinks for all `.md` files in the directory
