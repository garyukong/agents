## ADDED Requirements

### Requirement: Canonical import policy in python-development plugin artifacts
The python-development plugin SHALL define a single canonical import policy for command and skill artifacts: absolute imports are preferred for generated and recommended code examples, while explicit relative imports are allowed only in package-internal contexts where they are canonical and concise.

#### Scenario: Absolute imports used in generated scaffold examples
- **WHEN** a command template under plugins/python-development/commands emits Python code examples
- **THEN** recommended and generated imports use absolute module paths by default

#### Scenario: Relative imports constrained to allowed package-internal contexts
- **WHEN** a skill or command includes a relative import example
- **THEN** the example is limited to package-internal contexts such as __init__.py re-exports or same-package sibling references

#### Scenario: Disallowed relative examples are labeled as anti-patterns
- **WHEN** documentation includes relative-import forms outside allowed contexts
- **THEN** those forms are explicitly marked as avoid/anti-pattern examples and are not presented as preferred output

### Requirement: Consistent policy wording across command and skill docs
The plugin SHALL keep import-policy language consistent across scaffold command templates and Python skill documents so that generation guidance does not conflict.

#### Scenario: Policy text alignment
- **WHEN** command and skill files are reviewed for import-style guidance
- **THEN** they communicate the same absolute-preferred policy and the same bounded exception cases

### Requirement: Regression checks for import-policy drift
The change workflow SHALL include a validation step that audits relative-import occurrences and confirms they appear only in allowed or explicitly anti-pattern contexts.

#### Scenario: Validation catches policy violations
- **WHEN** a new or modified plugin artifact introduces a relative import example
- **THEN** the audit identifies whether the example is allowed, anti-pattern-labeled, or non-compliant
