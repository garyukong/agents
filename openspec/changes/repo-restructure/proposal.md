## Why

The repo is heavily Claude Code-centric — skills, agents, and commands live inside plugin directories with no coverage for Windsurf or VS Code Copilot. There is no consistent organisational model, making it unclear where to add new content or how to deploy to each environment without drift.

## What Changes

- Introduce a consistent top-level structure: `skills/`, `agents/`, `commands/`, `rules/`, `plugins/`
- Within each directory, root-level items are universal; environment-specific adaptations go in `claude-code/`, `windsurf/`, `copilot/` subdirectories
- Extract skill/agent/command content out of `plugins/` into canonical root-level locations
- Reduce `plugins/` to thin manifests with physical copies pointing into canonical locations
- **BREAKING**: Remove `plugin-skill-ports/` (content moves to `agents/` and `commands/`)
- `skills/windsurf-to-claude-rules` stays as a standalone skill in `skills/` (file conversion logic is distinct from deployment)

## New Directory Structure

```
agents/                              (repo root)
│
├── skills/                          ← canonical skill content
│   ├── python-development/          ← group
│   │   ├── python-pro-agent/        ← from skills/
│   │   ├── python-code-style/       ← from plugins/python-development/skills/
│   │   └── ...
│   ├── llm-application-dev/         ← group
│   │   ├── embedding-strategies/   ← from plugins/llm-application-dev/skills/
│   │   ├── langchain-architecture/  ←
│   │   └── ...
│   ├── machine-learning-ops/        ← group
│   │   └── ml-pipeline-workflow/     ←
│   ├── openspec/                    ← group
│   │   ├── openspec-explore/        ← from plugins/openspec/skills/
│   │   └── ...                      (compatibility: claude-code where needed)
│   ├── windsurf-to-claude-rules/    ← standalone
│   └── integration-test-suite/       ← standalone
├── rules/
│   ├── universal/                   ← AGENTS.md-compatible (all providers)
│   │   └── global.md                ← from rules/global_rules.md
│   ├── claude-code/
│   │   └── context-mode.md          ← from CLAUDE.md
│   ├── windsurf/                    ← (populate)
│   └── copilot/                     ← (populate)
├── agents/
│   └── claude-code/                 ← only Claude Code has file-based agent definitions
│       ├── ai-engineer/             ← from plugins/llm-application-dev/agents/
│       ├── data-scientist/          ← from plugins/machine-learning-ops/agents/
│       └── ...
├── commands/
│   └── claude-code/
│       ├── openspec/                ← group (Claude-specific frontmatter)
│       │   ├── apply/               ← from plugins/openspec/commands/
│       │   └── ...
│       └── ...
└── plugins/
    ├── claude-code/
    │   ├── llm-application-dev/     ← thin manifest + physical copies
    │   ├── machine-learning-ops/    ←
    │   ├── openspec/                 ←
    │   ├── python-development/       ←
    │   └── unit-testing/             ←
    └── copilot/                     ← (populate)

└── openspec/                        ← stays (manages this repo)
```

## Capabilities

### New Capabilities

- `directory-structure`: The standard layout — content type directories at root, env-specific subdirs within each
- `plugin-decomposition`: How existing plugins are decomposed into canonical content + thin manifests with physical copies

### Modified Capabilities

(none)

## Impact

- New top-level content directories replace current flat structure
- All existing content moves to root-level directories
- `plugins/*/skills/` content moves to `skills/<group>/` (grouped by domain)
- `plugins/*/agents/` content moves to `agents/claude-code/`
- `plugins/*/commands/` content moves to `commands/claude-code/openspec/`
- `plugin-skill-ports/` deleted
- `rules/global_rules.md` moves to `rules/universal/global.md`
- `plugins/` becomes `plugins/` with env-specific packaging only
- `skills-lock.json` and installed copies in `.claude/`, `.agents/` are unaffected (runtime artifacts)
