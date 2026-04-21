## 1. Setup

- [x] 1.1 Add dependencies (click, pyyaml, questionary) via uv
- [x] 1.2 Create scripts/rules.py file with basic CLI structure
- [x] 1.3 Add shebang for uvx execution

## 2. Core Types and Constants

- [x] 2.1 Implement Provider StrEnum (claude-code, windsurf, copilot-vscode, copilot-jetbrains, universal, all)
- [x] 2.2 Implement TriggerMode StrEnum (always_on, model_decision, glob, manual)
- [x] 2.3 Implement Scope StrEnum (global, project)

## 3. RulesManager Class

- [x] 3.1 Implement RulesManager.__init__ with rules_dir parameter
- [x] 3.2 Implement get_available_providers() method
- [x] 3.3 Implement get_available_sources() method to scan universal/ directory
- [x] 3.4 Implement select_source_interactively() using questionary
- [x] 3.5 Implement select_target_interactively() using questionary

## 4. Frontmatter Parsing and Conversion

- [x] 4.1 Implement parse_universal_frontmatter() to extract trigger, name, description, patterns
- [ ] 4.2 Implement convert_to_claude_code() with paths YAML list OR no frontmatter
- [x] 4.3 Implement convert_to_windsurf() with trigger and globs space-separated format
- [x] 4.4 Implement convert_to_copilot_vscode() with name, description, applyTo format
- [x] 4.5 Implement convert_to_copilot_jetbrains() to strip all frontmatter
- [x] 4.6 Implement unsupported mode conversion (model_decision/manual → always-on)

## 4.1. Fix Claude-Code Converter

- [ ] 4.1.1 Fix convert_to_claude_code() to use paths: for glob triggers, no frontmatter for always_on/model_decision
- [ ] 4.1.2 Update tests to expect paths: format or no frontmatter
- [ ] 4.1.3 Run tests to verify fix

## 5. Port Command Implementation

- [x] 5.1 Implement port_rule() method with source, target, dry_run parameters
- [x] 5.2 Implement single file porting logic
- [x] 5.3 Implement directory porting logic
- [x] 5.4 Implement "all providers" porting logic
- [x] 5.5 Implement dry-run preview mode
- [x] 5.6 Implement file writing with error handling

## 6. CLI Integration

- [x] 6.1 Implement click CLI group structure
- [x] 6.2 Implement port command with --to and --dry-run options
- [x] 6.3 Wire interactive mode (no args) to RulesManager methods
- [x] 6.4 Wire explicit mode (with args) to RulesManager.port_rule()
- [x] 6.5 Add help text and usage examples

## 7. Testing and Validation

- [x] 7.1 Test porting universal rule to claude-code
- [x] 7.2 Test porting universal rule to windsurf
- [x] 7.3 Test porting universal rule to copilot-vscode
- [x] 7.4 Test porting universal rule to copilot-jetbrains
- [x] 7.5 Test interactive mode with questionary
- [x] 7.6 Test dry-run mode
- [x] 7.7 Test unsupported mode conversion

## 8. Documentation

- [x] 8.1 Update AGENTS.md with rules port command usage
- [x] 8.2 Document universal frontmatter schema
- [ ] 8.3 Update provider-specific syntax mappings for claude-code (paths: vs globs:)
- [x] 8.4 Add examples for common use cases
