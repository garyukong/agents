## Context

The python-development plugin currently mixes import-style examples across command templates and skill content. The scaffold command includes relative imports in generated FastAPI examples, while style guidance elsewhere recommends absolute imports. This inconsistency causes generation drift and user confusion.

This change targets prompt artifacts under plugins/python-development only. The design must align with canonical Python guidance: absolute imports are preferred, and explicit relative imports remain acceptable for package-internal usage when concise and clear, especially in __init__.py re-export patterns.

## Goals / Non-Goals

**Goals:**
- Establish one plugin-wide import policy that is clear, testable, and canonical.
- Ensure generator templates prefer absolute imports by default.
- Allow explicit relative imports only in narrowly defined package-internal contexts.
- Remove contradictory examples across command and skill documents.
- Add lightweight validation so future edits preserve policy consistency.

**Non-Goals:**
- Refactor runtime Python application code outside this plugin.
- Enforce organization-wide linting rules across unrelated plugins.
- Ban relative imports globally in all contexts.

## Decisions

1. Policy model: Absolute-preferred with bounded relative allowances.
- Decision: Use absolute imports for all generated and recommended examples by default.
- Allowed exception: explicit relative imports may be used in package-internal examples where this is canonical and concise, primarily __init__.py re-export patterns and sibling imports inside the same package.
- Rationale: Matches PEP 8 guidance while minimizing generator ambiguity.
- Alternatives considered:
  - Strict absolute-only policy: simpler enforcement but diverges from canonical package practices.
  - Unrestricted relative imports: too ambiguous for scaffold generation and quality control.

2. Enforce policy in both command templates and skills.
- Decision: Update both python-scaffold command examples and python-project-structure/python-code-style skill examples.
- Rationale: Command templates are highest-impact for output; skills influence surrounding generation behavior.
- Alternatives considered:
  - Command-only edits: leaves contradictory skill examples that can reintroduce drift.
  - Skill-only edits: does not fix direct scaffold output.

3. Validation strategy based on pattern audit plus semantic classification.
- Decision: Add a repeatable check that scans for relative imports and verifies they only remain in explicitly allowed contexts.
- Rationale: Pattern scanning is fast and catches regressions; manual classification keeps policy nuance.
- Alternatives considered:
  - No validation: high regression risk.
  - Full static policy toolchain: overkill for prompt content repository.

## Risks / Trade-offs

- [Risk] Policy nuance may be interpreted differently by contributors. -> Mitigation: Add explicit policy language with examples of allowed and disallowed relative-import contexts.
- [Risk] Over-normalization may remove useful canonical __init__.py patterns. -> Mitigation: Preserve a clearly labeled allowed-relative subsection for package-internal exports.
- [Risk] Future docs may add unlabelled relative imports. -> Mitigation: Add validation checklist to change review tasks.
- [Trade-off] Absolute-preferred policy may increase verbosity in deep package paths. -> Mitigation: Permit explicit relative imports only where readability clearly improves within package boundaries.
