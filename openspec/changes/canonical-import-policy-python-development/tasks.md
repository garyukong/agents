## 1. Policy and Scope Alignment

- [ ] 1.1 Add explicit import-policy statement to plugins/python-development command and skill artifacts: absolute imports preferred, explicit relative imports allowed only in package-internal contexts
- [ ] 1.2 Enumerate allowed relative-import contexts (for example __init__.py re-exports and same-package sibling imports) and disallowed contexts
- [ ] 1.3 Ensure anti-pattern examples are clearly labeled and never presented as recommended output

## 2. Command Template Normalization

- [ ] 2.1 Update plugins/python-development/commands/python-scaffold.md so generated FastAPI examples use absolute imports by default
- [ ] 2.2 Add command-level guidance text describing when relative imports are acceptable under the bounded exception policy
- [ ] 2.3 Verify scaffold examples no longer contain ambiguous or contradictory import guidance

## 3. Skill Documentation Consistency

- [ ] 3.1 Update plugins/python-development/skills/python-project-structure/SKILL.md to align all preferred examples with the absolute-preferred policy
- [ ] 3.2 Preserve canonical package-internal relative examples only in allowed contexts and annotate them as allowed exceptions
- [ ] 3.3 Validate plugins/python-development/skills/python-code-style/SKILL.md remains consistent with the same policy language

## 4. Validation and Regression Guardrails

- [ ] 4.1 Add a repeatable audit step (regex plus classification) for from . and from .. occurrences within plugins/python-development
- [ ] 4.2 Confirm every remaining relative-import occurrence is either an allowed exception or an explicitly marked anti-pattern
- [ ] 4.3 Document the validation checklist in change notes so future edits preserve policy consistency
