## Why

The repo is heavily Claude Code-centric — skills, agents, and commands live inside plugin directories with no coverage for Windsurf or VS Code Copilot. There is no consistent organisational model, making it unclear where to add new content or how to deploy to each environment without drift.

## What Changes

- Introduce a consistent top-level structure: `skills/`, `agents/`, `commands/`, `rules/`, `plugins/`
- Within each directory, root-level items are universal; environment-specific adaptations go in `claude-code/`, `windsurf/`, `copilot/` subdirectories
- Extract skill/agent/command content out of `plugins/` into canonical root-level locations
- Reduce `plugins/` to thin manifests with symlinks pointing into canonical locations
- Add `global/skills/deploy/` — a new skill (created via skill-creator) for deploying content to `.claude/`, `.windsurf/`, `.github/` at project or global level
- **BREAKING**: Remove `plugin-skill-ports/` (content moves to `agents/` and `commands/`)
- `skills/windsurf-to-claude-rules` stays as a standalone skill in `skills/` (file conversion logic is distinct from deployment)

## New Directory Structure

```
agents/                              (repo root)
│
├── global/                          ← deploy to ~/.claude/ ~/.windsurf/ global ~/.github/
│   ├── skills/
│   │   ├── python-development/      ← group
│   │   │   ├── python-pro-agent/    ← from skills/
│   │   │   ├── python-code-style/   ← from plugins/python-development/skills/
│   │   │   └── ...
│   │   ├── llm-application-dev/     ← group
│   │   │   ├── embedding-strategies/← from plugins/llm-application-dev/skills/
│   │   │   ├── langchain-architecture/←
│   │   │   └── ...
│   │   ├── machine-learning-ops/    ← group
│   │   │   └── ml-pipeline-workflow/←
│   │   ├── openspec/                ← group
│   │   │   ├── openspec-explore/    ← from plugins/openspec/skills/
│   │   │   └── ...                  (compatibility: claude-code where needed)
│   │   ├── windsurf-to-claude-rules/← standalone
│   │   └── integration-test-suite/ ← standalone
│   ├── rules/
│   │   ├── universal/               ← AGENTS.md-compatible (all providers)
│   │   │   └── global.md            ← from rules/global_rules.md
│   │   ├── claude-code/
│   │   │   └── context-mode.md      ← from CLAUDE.md
│   │   ├── windsurf/                ← (populate)
│   │   └── copilot/                 ← (populate)
│   ├── agents/
│   │   └── claude-code/             ← only Claude Code has file-based agent definitions
│   │       ├── ai-engineer/         ← from plugins/llm-application-dev/agents/
│   │       ├── data-scientist/      ← from plugins/machine-learning-ops/agents/
│   │       └── ...
│   ├── commands/
│   ├── deploy/                      ← NEW skill (created via skill-creator)
│   │   ├── claude-code/
│   │   │   └── openspec/            ← group (Claude-specific frontmatter)
│   │   │       ├── apply/           ← from plugins/openspec/commands/
│   │   │       └── ...
│   │   ├── windsurf/                ← (populate)
│   │   └── copilot/                 ← (populate)
│   └── plugins/
│       ├── claude-code/
│       │   ├── llm-application-dev/ ← thin manifest + symlinks into global/skills/
│       │   ├── machine-learning-ops/←
│       │   ├── openspec/            ←
│       │   ├── python-development/  ←
│       │   └── unit-testing/        ←
│       └── copilot/                 ← (populate)
│
├── project/                         ← deploy to .claude/ .windsurf/ .github/ in target project
│   ├── skills/                      ← (populate with project-scoped skill templates)
│   ├── rules/
│   │   ├── universal/
│   │   ├── claude-code/
│   │   ├── windsurf/
│   │   └── copilot/
│   ├── agents/
│   │   └── claude-code/
│   ├── commands/
│   │   ├── claude-code/
│   │   ├── windsurf/
│   │   └── copilot/
│   └── plugins/
│       ├── claude-code/
│       └── copilot/
│
└── openspec/                        ← stays (manages this repo)
```

## Capabilities

### New Capabilities

- `directory-structure`: The standard layout — content type directories at root, env-specific subdirs within each
- `plugin-decomposition`: How existing plugins are decomposed into canonical content + thin manifests with symlinks
- `deployment-workflow`: How content from this repo is synced to `.claude/`, `.windsurf/`, `.github/` at project or global level

### Modified Capabilities

(none)

## Impact

- New top-level `global/` and `project/` scope directories replace current flat structure
- All existing content moves into `global/` (current content is all global-scoped)
- `plugins/*/skills/` content moves to `global/skills/<group>/` (grouped by domain)
- `plugins/*/agents/` content moves to `global/agents/claude-code/`
- `plugins/*/commands/` content moves to `global/commands/claude-code/openspec/`
- `plugin-skill-ports/` deleted
- `rules/global_rules.md` moves to `global/rules/universal/global.md`
- `plugins/` becomes `global/plugins/` with env-specific packaging only
- `project/` starts mostly empty — populated as project-scoped templates are identified
- `skills-lock.json` and installed copies in `.claude/`, `.agents/` are unaffected (runtime artifacts)
