## Tasks

### Phase 1: Create new directory skeleton

- [x] Create `skills/` directory
- [x] Create `rules/universal/`, `rules/claude-code/`, `rules/windsurf/`, `rules/copilot/` directories
- [x] Create `agents/claude-code/` directory
- [x] Create `commands/claude-code/openspec/` directory
- [x] Create `plugins/claude-code/` directory
- [x] **Commit**: `chore(structure): scaffold content-type directory skeleton`
- [x] **Checkpoint**: review directory tree before any content is moved

---

### Phase 2: Move skills into canonical locations

- [x] Move `plugins/python-development/skills/*` → `skills/python-development/`
- [x] Move `plugins/llm-application-dev/skills/*` → `skills/llm-application-dev/`
- [x] Move `plugins/machine-learning-ops/skills/*` → `skills/machine-learning-ops/`
- [x] Move `plugins/openspec/skills/*` → `skills/openspec/`
- [x] Move `plugins/unit-testing/skills/*` → `skills/unit-testing/`
- [x] Move standalone `skills/windsurf-to-claude-rules/` → `skills/windsurf-to-claude-rules/`
- [x] Move standalone `skills/integration-test-suite/` → `skills/integration-test-suite/` (if exists)
- [x] Verify all skill `SKILL.md` files are present in new locations
- [x] **Commit**: `feat(skills): move all skills into skills/ canonical locations`
- [x] **Checkpoint**: confirm `skills/` has all expected groups and no skills are missing

---

### Phase 3: Move agents

- [x] Move `plugins/llm-application-dev/agents/*` → `agents/claude-code/`
- [x] Move `plugins/machine-learning-ops/agents/*` → `agents/claude-code/`
- [x] Move any remaining `plugins/*/agents/*` → `agents/claude-code/`
- [x] **Commit**: `feat(agents): move all agents into agents/claude-code/`
- [x] **Checkpoint**: confirm `agents/claude-code/` contains all agent definitions

---

### Phase 4: Move commands

- [x] Move `plugins/openspec/commands/*` → `commands/claude-code/openspec/`
- [x] Move any remaining `plugins/*/commands/*` → `commands/claude-code/` (appropriate subdir)
- [x] **Commit**: `feat(commands): move all commands into commands/claude-code/`
- [x] **Checkpoint**: confirm commands are present and frontmatter is intact

---

### Phase 5: Move rules

- [x] Move `rules/global_rules.md` → `rules/universal/global.md`
- [x] Move Claude-specific content from `rules/CLAUDE.md` (or equivalent) → `rules/claude-code/context-mode.md`
- [x] **Commit**: `feat(rules): move rules into rules/ with universal/ and claude-code/ split`
- [x] **Checkpoint**: open both moved files and confirm content is intact and correctly categorised

---

### Phase 6: Rebuild plugins as thin manifests

- [x] Create `plugins/claude-code/python-development/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `skills/python-development/` into `plugins/claude-code/python-development/skills/`
- [x] Create `plugins/claude-code/llm-application-dev/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `skills/llm-application-dev/` into `plugins/claude-code/llm-application-dev/skills/`
- [x] Create `plugins/claude-code/machine-learning-ops/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `skills/machine-learning-ops/` into `plugins/claude-code/machine-learning-ops/skills/`
- [x] Create `plugins/claude-code/openspec/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `skills/openspec/` into `plugins/claude-code/openspec/skills/`
- [x] Create `plugins/claude-code/unit-testing/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `skills/unit-testing/` into `plugins/claude-code/unit-testing/skills/`
- [x] Verify each `plugin.json` lists only skills present in its own `skills/` subdirectory
- [x] **Commit**: `feat(plugins): rebuild plugins as thin manifests with physical skill copies`
- [x] **Checkpoint**: spot-check one plugin — install it locally and confirm skills load correctly

---

### Phase 7: Remove deprecated directories

- [x] Delete `plugin-skill-ports/` directory
- [x] Delete old `plugins/` root (now replaced by `plugins/`)
- [x] Delete old `skills/` root (now replaced by `skills/`)
- [x] Delete old `rules/` root (now replaced by `rules/`)
- [x] Delete old `commands/` root if present (now replaced by `commands/`)
- [x] **Commit**: `chore(cleanup): remove deprecated plugins/, skills/, rules/, plugin-skill-ports/ roots`
- [x] **Checkpoint**: confirm repo has no orphaned content outside content directories

---

### Phase 8: Verify

- [x] Run `npx skills install garyukong/agents` (dry-run or sandbox) — confirm skills resolve from new paths
- [x] Confirm `skills-lock.json` is unaffected (tracks installed skills, not source paths)
- [x] Confirm no broken symlinks remain in working tree
- [x] Browse `skills/python-development/` — all Python skills present
- [x] Browse `plugins/claude-code/python-development/skills/` — physical copies present, no symlinks
- [x] Confirm `plugin-skill-ports/` no longer exists
- [x] **Commit**: `chore(verify): post-restructure verification complete`
- [x] **Checkpoint**: sign off that the new structure matches the design before adding documentation

---

### Phase 9: Write repo-level documentation

- [x] Write `AGENTS.md` at repo root describing intended use: this repo is a content library for skills, agents, commands, and rules — not a deployment tool; content is distributed via `npx skills`, rulesync, and the Claude plugin system
- [x] Document the content-type organization and provider-specific conventions
- [x] Document provider-specific subdirectory conventions (`claude-code/`, `windsurf/`, `copilot/`)
- [x] Create `CLAUDE.md` at repo root as a hard link to `AGENTS.md` (`ln AGENTS.md CLAUDE.md`) so both Claude Code and AGENTS.md-compatible tools read the same file
- [x] Verify both files have identical inode (confirm hard link, not copy)
- [x] **Commit**: `docs(repo): add AGENTS.md and CLAUDE.md hard link with repo intent and structure guide`
- [x] **Checkpoint**: read both files and confirm they reflect the final structure accurately
