---
name: package-plugin
description: Package a plugin by syncing agents, commands, and skills from their source directories into the plugin's directory under plugins/claude-code/. Use this skill whenever the user wants to package, update, or sync a plugin, mentions that a plugin is missing its agents or commands, or asks to "package" a plugin based on the repo conventions.
---

# Package Plugin

Sync the source artifacts for a plugin into its packaged form under `plugins/claude-code/<plugin-name>/`.

## Directory conventions

The repo separates *source* from *packaged* artifacts:

| Artifact type | Source location | Packaged location |
|---|---|---|
| Agents | `agents/claude-code/<plugin>/` | `plugins/claude-code/<plugin>/agents/` |
| Commands | `commands/claude-code/<plugin>/` | `plugins/claude-code/<plugin>/commands/` |
| Skills | `skills/<plugin>/` | `plugins/claude-code/<plugin>/skills/` |
| Manifest | — | `plugins/claude-code/<plugin>/.claude-plugin/plugin.json` |

Skills use a subdirectory-per-skill layout (`<skill-name>/SKILL.md` plus optional `assets/`, `references/`, `scripts/`). Agents and commands are flat `.md` files.

## Steps

### 1. Identify the plugin

Determine the plugin name from the user's request or the current working context. Confirm if ambiguous.

### 2. Audit what exists

For the target plugin, check all four source locations and the plugin directory:

```shell
find agents/claude-code/<plugin> commands/claude-code/<plugin> skills/<plugin> \
     plugins/claude-code/<plugin> -type f 2>/dev/null | sort
```

Build a mental diff:
- Which source agents/commands are absent from the plugin's `agents/` and `commands/` dirs?
- Which skills are absent from the plugin's `skills/` dir?
- Are there stale files in the plugin that no longer exist in source?

### 3. Sync agents

```shell
mkdir -p plugins/claude-code/<plugin>/agents
cp agents/claude-code/<plugin>/*.md plugins/claude-code/<plugin>/agents/
```

Only copy if the source directory exists and contains `.md` files.

### 4. Sync commands

```shell
mkdir -p plugins/claude-code/<plugin>/commands
cp commands/claude-code/<plugin>/*.md plugins/claude-code/<plugin>/commands/
```

### 5. Sync skills

Skills include subdirectories with assets; use recursive copy:

```shell
cp -r skills/<plugin>/. plugins/claude-code/<plugin>/skills/
```

Preserve the full `<skill-name>/` subdirectory structure including any `assets/`, `references/`, and `scripts/` folders.

### 6. Verify the manifest

Check that `plugins/claude-code/<plugin>/.claude-plugin/plugin.json` exists and its `"skills"` array lists all skills now present in `plugins/claude-code/<plugin>/skills/`. Update the array if skills were added or removed.

The manifest shape:

```json
{
  "name": "<plugin>",
  "version": "x.y.z",
  "description": "...",
  "author": { "name": "...", "email": "..." },
  "license": "MIT",
  "skills": ["skill-name-1", "skill-name-2"]
}
```

### 7. Update marketplace.json

Check `agents/.claude-plugin/marketplace.json`. This file is the repo-level registry for plugin discovery.

- If the plugin is **new** (not yet listed): add an entry to the `"plugins"` array with the following shape:

```json
{
  "name": "<plugin>",
  "description": "...",
  "version": "1.0.0",
  "author": { "name": "Gary Kong" },
  "source": "./plugins/claude-code/<plugin>",
  "category": "<ai-ml|languages|testing|workflows>",
  "homepage": "https://github.com/garyukong/agents",
  "license": "MIT"
}
```

- If the plugin **already exists**: verify the `source` path is correct and bump `version` if skills, agents, or commands were added or removed.
- Also bump the top-level `metadata.version` to reflect the change.

### 8. Report

Summarise what changed:
- Files added to `agents/`
- Files added to `commands/`
- Skill directories added/updated in `skills/`
- Manifest changes (if any)

If a source directory doesn't exist for a given artifact type (e.g. no agents exist for `machine-learning-ops`), note it but treat it as expected — not every plugin has all three artifact types.

## Packaging all plugins

If the user asks to package *all* plugins, iterate over every subdirectory in `plugins/claude-code/` (excluding `.gitkeep`) and run the steps above for each one.

## Frontmatter standards reminder

Before copying, verify the `.md` files have correct Claude frontmatter:

- **Agent files** (`agents/claude-code/<plugin>/*.md`): require `name`, `description` (and optionally `model`) in YAML frontmatter.
- **Command files** (`commands/claude-code/<plugin>/*.md`): require `description` in YAML frontmatter; optionally `argument-hint` and `allowed-tools`. Non-standard fields (e.g. `auto_execution_mode`) should be removed.
- **Skill files** (`skills/<plugin>/<skill-name>/SKILL.md`): require `name` and `description` in YAML frontmatter.

Flag any files missing required frontmatter and offer to fix them before packaging.
