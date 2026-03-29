## Why

The python-development plugin currently gives mixed guidance on import style, causing generated scaffolds and examples to drift toward inconsistent behavior. We need one canonical policy so generated output is predictable while still aligned with mainstream Python guidance.

## What Changes

- Define and enforce a canonical import policy across all command and skill content under plugins/python-development.
- Standardize generator templates to prefer absolute imports in generated project files.
- Allow explicit relative imports only for package-internal contexts where they are canonical and concise, especially package re-export patterns in __init__.py.
- Normalize examples in skill documentation so recommended examples and anti-pattern examples are clearly separated.
- Add validation checks so future prompt updates do not reintroduce ambiguous import guidance.

## Capabilities

### New Capabilities
- `python-import-policy`: Establishes plugin-wide import policy and validation rules for generated examples and scaffold templates.

### Modified Capabilities
- None.

## Impact

- Affected content:
  - plugins/python-development/commands/python-scaffold.md
  - plugins/python-development/skills/python-project-structure/SKILL.md
  - plugins/python-development/skills/python-code-style/SKILL.md
- No runtime Python application code changes; this is prompt/schema behavior and documentation consistency.
- Downstream effect: generated scaffolds become more consistent and policy-compliant without removing canonical package-relative patterns where appropriate.
