## ADDED Requirements

### Requirement: Universal frontmatter schema
The system SHALL define a canonical universal frontmatter schema with fields: trigger, name, description, patterns. The patterns field SHALL be a YAML list of file pattern strings.

#### Scenario: Universal rule with glob trigger
- **WHEN** a universal rule file contains trigger: glob and patterns: ["**/*.py"]
- **THEN** the system SHALL parse the frontmatter and extract these canonical fields

#### Scenario: Universal rule with model_decision trigger
- **WHEN** a universal rule file contains trigger: model_decision
- **THEN** the system SHALL parse the frontmatter and extract trigger, name, description, patterns fields

### Requirement: Provider-specific syntax mapping
The system SHALL convert universal frontmatter to provider-specific syntax according to documented mappings for claude-code, windsurf, copilot-vscode, and copilot-jetbrains.

#### Scenario: Convert to claude-code syntax
- **WHEN** porting to claude-code with trigger: glob and patterns: ["**/*.py", "pyproject.toml"]
- **THEN** the system SHALL output globs as a YAML list (one pattern per line)

#### Scenario: Convert to windsurf syntax
- **WHEN** porting to windsurf with trigger: glob and patterns: ["**/*.py", "**/conftest.py"]
- **THEN** the system SHALL output trigger: glob and globs as a comma-separated string (e.g. `globs: **/*.py, **/conftest.py`)

#### Scenario: Convert to copilot-vscode syntax (single pattern)
- **WHEN** porting to copilot-vscode with name: "API" and patterns: ["**/*.py"]
- **THEN** the system SHALL output name, description, and applyTo: "**/*.py"

#### Scenario: Convert to copilot-vscode syntax (multiple patterns)
- **WHEN** porting to copilot-vscode with patterns: ["**/*.py", "**/*.ts"]
- **THEN** the system SHALL output applyTo as a comma-separated string and print a warning that multi-pattern applyTo has a known bug in Copilot VSCode and may not work reliably

#### Scenario: Convert to copilot-jetbrains syntax
- **WHEN** porting to copilot-jetbrains with any trigger mode
- **THEN** the system SHALL output no frontmatter (plain markdown)

### Requirement: Unsupported mode conversion
The system SHALL convert unsupported activation modes (model_decision, manual) to always-on by omitting pattern fields.

#### Scenario: Model_decision to claude-code
- **WHEN** porting to claude-code with trigger: model_decision
- **THEN** the system SHALL output no globs field (always-on)

#### Scenario: Manual to copilot-vscode
- **WHEN** porting to copilot-vscode with trigger: manual
- **THEN** the system SHALL output no applyTo field (always-on)

### Requirement: Interactive mode
The system SHALL support interactive mode where users select source and target via questionary prompts when no arguments provided.

#### Scenario: Interactive source selection
- **WHEN** user runs `rules port` without arguments
- **THEN** the system SHALL display available sources from universal/ directory and prompt for selection

#### Scenario: Interactive target selection
- **WHEN** user selects a source
- **THEN** the system SHALL display available providers and prompt for target selection

#### Scenario: Interactive confirmation
- **WHEN** user completes selections
- **THEN** the system SHALL display preview and prompt for confirmation before writing

### Requirement: Idempotency
The system SHALL silently overwrite existing provider-specific files when porting. The generated-file header serves as sufficient indication that the file is managed.

#### Scenario: Re-porting an already-ported file
- **WHEN** a provider-specific file already exists at the output path
- **THEN** the system SHALL overwrite it silently without prompting

### Requirement: Explicit mode
The system SHALL support explicit mode where source and target are provided as command-line arguments.

#### Scenario: Explicit single file port
- **WHEN** user runs `rules port universal/oms-ml-semantics/architecture.md --to claude-code`
- **THEN** the system SHALL port that specific file to the specified provider without prompting

#### Scenario: Explicit directory port
- **WHEN** user runs `rules port universal/oms-ml-semantics --to windsurf`
- **THEN** the system SHALL port all files in that directory to the specified provider

#### Scenario: Port to all providers
- **WHEN** user runs `rules port universal/oms-ml-semantics --to all`
- **THEN** the system SHALL port to claude-code, windsurf, copilot-vscode, and copilot-jetbrains

### Requirement: Dry run mode
The system SHALL support --dry-run flag to preview changes without writing files.

#### Scenario: Dry run preview
- **WHEN** user runs `rules port universal/architecture.md --to claude-code --dry-run`
- **THEN** the system SHALL display the conversion preview but not write any files

### Requirement: Type-safe constants
The system SHALL use StrEnums for Provider, TriggerMode, and Scope constants.

#### Scenario: Provider enum usage
- **WHEN** referencing a provider in code
- **THEN** the system SHALL use Provider.CLAUDE_CODE, Provider.WINDSURF, etc.

#### Scenario: TriggerMode enum usage
- **WHEN** referencing a trigger mode in code
- **THEN** the system SHALL use TriggerMode.GLOB, TriggerMode.MODEL_DECISION, etc.

### Requirement: Missing frontmatter handling
The system SHALL warn and prompt for confirmation when a universal rule file contains no YAML frontmatter. If confirmed, the file SHALL be ported as an always-on rule (no pattern fields). If declined, the port operation SHALL halt.

#### Scenario: Universal rule with no frontmatter — confirmed
- **WHEN** a universal rule file contains no `---` frontmatter block and the user confirms the prompt
- **THEN** the system SHALL port the file as an always-on rule, omitting all pattern fields, and continue the port operation

#### Scenario: Universal rule with no frontmatter — declined
- **WHEN** a universal rule file contains no `---` frontmatter block and the user declines the prompt
- **THEN** the system SHALL halt without writing any output files

### Requirement: Generated-file header
The system SHALL insert an HTML comment immediately after the closing frontmatter delimiter (or at line 1 for copilot-jetbrains) referencing the universal source path, to enable round-trip identification and discourage direct edits to provider-specific files.

#### Scenario: Header in frontmatter-bearing providers
- **WHEN** porting to claude-code, windsurf, or copilot-vscode
- **THEN** the system SHALL insert `<!-- AUTO-GENERATED by rules port — edit universal/<source> instead -->` on the first line after the closing `---`

#### Scenario: Header in copilot-jetbrains (no frontmatter)
- **WHEN** porting to copilot-jetbrains
- **THEN** the system SHALL insert `<!-- AUTO-GENERATED by rules port — edit universal/<source> instead -->` as the first line of the file

#### Scenario: Round-trip source identification
- **WHEN** reading a provider-specific file with a generated-file header
- **THEN** the system SHALL be able to extract the universal source path from the header comment

### Requirement: Class-based architecture
The system SHALL encapsulate all file operations and conversions in a RulesManager class.

#### Scenario: RulesManager initialization
- **WHEN** creating a RulesManager instance
- **THEN** the system SHALL accept an optional rules_dir parameter defaulting to Path("rules")

#### Scenario: File scanning
- **WHEN** calling get_available_sources()
- **THEN** the system SHALL scan universal/ directory and return list of available rules

#### Scenario: Port operation
- **WHEN** calling port_rule(source, target, dry_run)
- **THEN** the system SHALL perform the conversion and write files (unless dry_run)
