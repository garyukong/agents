## 1. Setup

- [ ] 1.1 Add dependencies (click, pyyaml, questionary) via uv
- [ ] 1.2 Create scripts/rules.py file with basic CLI structure
- [ ] 1.3 Add shebang for uvx execution

## 2. Core Types and Constants

- [ ] 2.1 Implement Provider StrEnum (claude-code, windsurf, copilot-vscode, copilot-jetbrains, universal, all)
- [ ] 2.2 Implement TriggerMode StrEnum (always_on, model_decision, glob, manual)
- [ ] 2.3 Implement Scope StrEnum (global, project)

## 3. RulesManager Class

- [ ] 3.1 Implement RulesManager.__init__ with rules_dir parameter
- [ ] 3.2 Implement get_available_providers() method
- [ ] 3.3 Implement get_available_sources() method to scan universal/ directory
- [ ] 3.4 Implement select_source_interactively() using questionary
- [ ] 3.5 Implement select_target_interactively() using questionary

## 4. Frontmatter Parsing and Conversion

- [ ] 4.1 Implement parse_universal_frontmatter() to extract trigger, name, description, patterns
- [ ] 4.2 Implement convert_to_claude_code() with globs comma-separated format
- [ ] 4.3 Implement convert_to_windsurf() with trigger and globs space-separated format
- [ ] 4.4 Implement convert_to_copilot_vscode() with name, description, applyTo format
- [ ] 4.5 Implement convert_to_copilot_jetbrains() to strip all frontmatter
- [ ] 4.6 Implement unsupported mode conversion (model_decision/manual → always-on)

## 5. Port Command Implementation

- [ ] 5.1 Implement port_rule() method with source, target, dry_run parameters
- [ ] 5.2 Implement single file porting logic
- [ ] 5.3 Implement directory porting logic
- [ ] 5.4 Implement "all providers" porting logic
- [ ] 5.5 Implement dry-run preview mode
- [ ] 5.6 Implement file writing with error handling

## 6. CLI Integration

- [ ] 6.1 Implement click CLI group structure
- [ ] 6.2 Implement port command with --to and --dry-run options
- [ ] 6.3 Wire interactive mode (no args) to RulesManager methods
- [ ] 6.4 Wire explicit mode (with args) to RulesManager.port_rule()
- [ ] 6.5 Add help text and usage examples

## 7. Testing and Validation

- [ ] 7.1 Test porting universal rule to claude-code
- [ ] 7.2 Test porting universal rule to windsurf
- [ ] 7.3 Test porting universal rule to copilot-vscode
- [ ] 7.4 Test porting universal rule to copilot-jetbrains
- [ ] 7.5 Test interactive mode with questionary
- [ ] 7.6 Test dry-run mode
- [ ] 7.7 Test unsupported mode conversion

## 8. Documentation

- [ ] 8.1 Update AGENTS.md with rules port command usage
- [ ] 8.2 Document universal frontmatter schema
- [ ] 8.3 Document provider-specific syntax mappings
- [ ] 8.4 Add examples for common use cases
