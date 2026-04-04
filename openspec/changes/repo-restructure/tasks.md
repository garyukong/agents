## Tasks

### Phase 1: Create new directory skeleton

- [x] Create `global/skills/` directory
- [x] Create `global/rules/universal/`, `global/rules/claude-code/`, `global/rules/windsurf/`, `global/rules/copilot/` directories
- [x] Create `global/agents/claude-code/` directory
- [x] Create `global/commands/claude-code/openspec/` directory
- [x] Create `global/plugins/claude-code/` directory
- [x] Create `project/skills/`, `project/rules/universal/`, `project/rules/claude-code/`, `project/rules/windsurf/`, `project/rules/copilot/` directories
- [x] Create `project/agents/claude-code/`, `project/commands/claude-code/`, `project/plugins/claude-code/` directories
- [x] **Commit**: `chore(structure): scaffold global/ and project/ directory skeleton`
- [x] **Checkpoint**: review directory tree before any content is moved

---

### Phase 2: Move skills into canonical locations

- [x] Move `plugins/python-development/skills/*` → `global/skills/python-development/`
- [x] Move `plugins/llm-application-dev/skills/*` → `global/skills/llm-application-dev/`
- [x] Move `plugins/machine-learning-ops/skills/*` → `global/skills/machine-learning-ops/`
- [x] Move `plugins/openspec/skills/*` → `global/skills/openspec/`
- [x] Move `plugins/unit-testing/skills/*` → `global/skills/unit-testing/`
- [x] Move standalone `skills/windsurf-to-claude-rules/` → `global/skills/windsurf-to-claude-rules/`
- [x] Move standalone `skills/integration-test-suite/` → `global/skills/integration-test-suite/` (if exists)
- [x] Verify all skill `SKILL.md` files are present in new locations
- [x] **Commit**: `feat(skills): move all skills into global/skills/ canonical locations`
- [x] **Checkpoint**: confirm `global/skills/` has all expected groups and no skills are missing

---

### Phase 3: Move agents

- [x] Move `plugins/llm-application-dev/agents/*` → `global/agents/claude-code/`
- [x] Move `plugins/machine-learning-ops/agents/*` → `global/agents/claude-code/`
- [x] Move any remaining `plugins/*/agents/*` → `global/agents/claude-code/`
- [x] **Commit**: `feat(agents): move all agents into global/agents/claude-code/`
- [x] **Checkpoint**: confirm `global/agents/claude-code/` contains all agent definitions

---

### Phase 4: Move commands

- [x] Move `plugins/openspec/commands/*` → `global/commands/claude-code/openspec/`
- [x] Move any remaining `plugins/*/commands/*` → `global/commands/claude-code/` (appropriate subdir)
- [x] **Commit**: `feat(commands): move all commands into global/commands/claude-code/`
- [x] **Checkpoint**: confirm commands are present and frontmatter is intact

---

### Phase 5: Move rules

- [x] Move `rules/global_rules.md` → `global/rules/universal/global.md`
- [x] Move Claude-specific content from `rules/CLAUDE.md` (or equivalent) → `global/rules/claude-code/context-mode.md`
- [x] **Commit**: `feat(rules): move rules into global/rules/ with universal/ and claude-code/ split`
- [x] **Checkpoint**: open both moved files and confirm content is intact and correctly categorised

---

### Phase 6: Rebuild plugins as thin manifests

- [x] Create `global/plugins/claude-code/python-development/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `global/skills/python-development/` into `global/plugins/claude-code/python-development/skills/`
- [x] Create `global/plugins/claude-code/llm-application-dev/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `global/skills/llm-application-dev/` into `global/plugins/claude-code/llm-application-dev/skills/`
- [x] Create `global/plugins/claude-code/machine-learning-ops/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `global/skills/machine-learning-ops/` into `global/plugins/claude-code/machine-learning-ops/skills/`
- [x] Create `global/plugins/claude-code/openspec/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `global/skills/openspec/` into `global/plugins/claude-code/openspec/skills/`
- [x] Create `global/plugins/claude-code/unit-testing/` with `.claude-plugin/plugin.json`
- [x] Copy canonical skills from `global/skills/unit-testing/` into `global/plugins/claude-code/unit-testing/skills/`
- [x] Verify each `plugin.json` lists only skills present in its own `skills/` subdirectory
- [x] **Commit**: `feat(plugins): rebuild plugins as thin manifests with physical skill copies`
- [x] **Checkpoint**: spot-check one plugin — install it locally and confirm skills load correctly

---

### Phase 7: Remove deprecated directories

- [x] Delete `plugin-skill-ports/` directory
- [x] Delete old `plugins/` root (now replaced by `global/plugins/`)
- [x] Delete old `skills/` root (now replaced by `global/skills/`)
- [x] Delete old `rules/` root (now replaced by `global/rules/`)
- [x] Delete old `commands/` root if present (now replaced by `global/commands/`)
- [x] **Commit**: `chore(cleanup): remove deprecated plugins/, skills/, rules/, plugin-skill-ports/ roots`
- [x] **Checkpoint**: confirm repo has no orphaned content outside `global/`, `project/`, `openspec/`

---

### Phase 8: Verify

- [x] Run `npx skills install garyukong/agents` (dry-run or sandbox) — confirm skills resolve from new paths
- [x] Confirm `skills-lock.json` is unaffected (tracks installed skills, not source paths)
- [x] Confirm no broken symlinks remain in working tree
- [x] Browse `global/skills/python-development/` — all Python skills present
- [x] Browse `global/plugins/claude-code/python-development/skills/` — physical copies present, no symlinks
- [x] Confirm `plugin-skill-ports/` no longer exists
- [x] Confirm `project/` directory skeleton is present (empty is expected)
- [x] **Commit**: `chore(verify): post-restructure verification complete`
- [x] **Checkpoint**: sign off that the new structure matches the design before adding documentation

---

### Phase 9: Write repo-level documentation

- [x] Write `AGENTS.md` at repo root describing intended use: this repo is a content library for skills, agents, commands, and rules — not a deployment tool; content is distributed via `npx skills`, rulesync, and the Claude plugin system
- [x] Document the `global/` vs `project/` scope split and what each is for
- [x] Document provider-specific subdirectory conventions (`claude-code/`, `windsurf/`, `copilot/`)
- [x] Create `CLAUDE.md` at repo root as a hard link to `AGENTS.md` (`ln AGENTS.md CLAUDE.md`) so both Claude Code and AGENTS.md-compatible tools read the same file
- [x] Verify both files have identical inode (confirm hard link, not copy)
- [x] **Commit**: `docs(repo): add AGENTS.md and CLAUDE.md hard link with repo intent and structure guide`
- [x] **Checkpoint**: read both files and confirm they reflect the final structure accurately
