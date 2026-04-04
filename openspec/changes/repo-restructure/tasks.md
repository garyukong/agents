## Tasks

### Phase 1: Create new directory skeleton

- [ ] Create `global/skills/` directory
- [ ] Create `global/rules/universal/`, `global/rules/claude-code/`, `global/rules/windsurf/`, `global/rules/copilot/` directories
- [ ] Create `global/agents/claude-code/` directory
- [ ] Create `global/commands/claude-code/openspec/` directory
- [ ] Create `global/plugins/claude-code/` directory
- [ ] Create `project/skills/`, `project/rules/universal/`, `project/rules/claude-code/`, `project/rules/windsurf/`, `project/rules/copilot/` directories
- [ ] Create `project/agents/claude-code/`, `project/commands/claude-code/`, `project/plugins/claude-code/` directories
- [ ] **Commit**: `chore(structure): scaffold global/ and project/ directory skeleton`
- [ ] **Checkpoint**: review directory tree before any content is moved

---

### Phase 2: Move skills into canonical locations

- [ ] Move `plugins/python-development/skills/*` → `global/skills/python-development/`
- [ ] Move `plugins/llm-application-dev/skills/*` → `global/skills/llm-application-dev/`
- [ ] Move `plugins/machine-learning-ops/skills/*` → `global/skills/machine-learning-ops/`
- [ ] Move `plugins/openspec/skills/*` → `global/skills/openspec/`
- [ ] Move `plugins/unit-testing/skills/*` → `global/skills/unit-testing/`
- [ ] Move standalone `skills/windsurf-to-claude-rules/` → `global/skills/windsurf-to-claude-rules/`
- [ ] Move standalone `skills/integration-test-suite/` → `global/skills/integration-test-suite/` (if exists)
- [ ] Verify all skill `SKILL.md` files are present in new locations
- [ ] **Commit**: `feat(skills): move all skills into global/skills/ canonical locations`
- [ ] **Checkpoint**: confirm `global/skills/` has all expected groups and no skills are missing

---

### Phase 3: Move agents

- [ ] Move `plugins/llm-application-dev/agents/*` → `global/agents/claude-code/`
- [ ] Move `plugins/machine-learning-ops/agents/*` → `global/agents/claude-code/`
- [ ] Move any remaining `plugins/*/agents/*` → `global/agents/claude-code/`
- [ ] **Commit**: `feat(agents): move all agents into global/agents/claude-code/`
- [ ] **Checkpoint**: confirm `global/agents/claude-code/` contains all agent definitions

---

### Phase 4: Move commands

- [ ] Move `plugins/openspec/commands/*` → `global/commands/claude-code/openspec/`
- [ ] Move any remaining `plugins/*/commands/*` → `global/commands/claude-code/` (appropriate subdir)
- [ ] **Commit**: `feat(commands): move all commands into global/commands/claude-code/`
- [ ] **Checkpoint**: confirm commands are present and frontmatter is intact

---

### Phase 5: Move rules

- [ ] Move `rules/global_rules.md` → `global/rules/universal/global.md`
- [ ] Move Claude-specific content from `rules/CLAUDE.md` (or equivalent) → `global/rules/claude-code/context-mode.md`
- [ ] **Commit**: `feat(rules): move rules into global/rules/ with universal/ and claude-code/ split`
- [ ] **Checkpoint**: open both moved files and confirm content is intact and correctly categorised

---

### Phase 6: Rebuild plugins as thin manifests

- [ ] Create `global/plugins/claude-code/python-development/` with `.claude-plugin/plugin.json`
- [ ] Copy canonical skills from `global/skills/python-development/` into `global/plugins/claude-code/python-development/skills/`
- [ ] Create `global/plugins/claude-code/llm-application-dev/` with `.claude-plugin/plugin.json`
- [ ] Copy canonical skills from `global/skills/llm-application-dev/` into `global/plugins/claude-code/llm-application-dev/skills/`
- [ ] Create `global/plugins/claude-code/machine-learning-ops/` with `.claude-plugin/plugin.json`
- [ ] Copy canonical skills from `global/skills/machine-learning-ops/` into `global/plugins/claude-code/machine-learning-ops/skills/`
- [ ] Create `global/plugins/claude-code/openspec/` with `.claude-plugin/plugin.json`
- [ ] Copy canonical skills from `global/skills/openspec/` into `global/plugins/claude-code/openspec/skills/`
- [ ] Create `global/plugins/claude-code/unit-testing/` with `.claude-plugin/plugin.json`
- [ ] Copy canonical skills from `global/skills/unit-testing/` into `global/plugins/claude-code/unit-testing/skills/`
- [ ] Verify each `plugin.json` lists only skills present in its own `skills/` subdirectory
- [ ] **Commit**: `feat(plugins): rebuild plugins as thin manifests with physical skill copies`
- [ ] **Checkpoint**: spot-check one plugin — install it locally and confirm skills load correctly

---

### Phase 7: Remove deprecated directories

- [ ] Delete `plugin-skill-ports/` directory
- [ ] Delete old `plugins/` root (now replaced by `global/plugins/`)
- [ ] Delete old `skills/` root (now replaced by `global/skills/`)
- [ ] Delete old `rules/` root (now replaced by `global/rules/`)
- [ ] Delete old `commands/` root if present (now replaced by `global/commands/`)
- [ ] **Commit**: `chore(cleanup): remove deprecated plugins/, skills/, rules/, plugin-skill-ports/ roots`
- [ ] **Checkpoint**: confirm repo has no orphaned content outside `global/`, `project/`, `openspec/`

---

### Phase 8: Verify

- [ ] Run `npx skills install garyukong/agents` (dry-run or sandbox) — confirm skills resolve from new paths
- [ ] Confirm `skills-lock.json` is unaffected (tracks installed skills, not source paths)
- [ ] Confirm no broken symlinks remain in working tree
- [ ] Browse `global/skills/python-development/` — all Python skills present
- [ ] Browse `global/plugins/claude-code/python-development/skills/` — physical copies present, no symlinks
- [ ] Confirm `plugin-skill-ports/` no longer exists
- [ ] Confirm `project/` directory skeleton is present (empty is expected)
- [ ] **Commit**: `chore(verify): post-restructure verification complete`
- [ ] **Checkpoint**: sign off that the new structure matches the design before adding documentation

---

### Phase 9: Write repo-level documentation

- [ ] Write `AGENTS.md` at repo root describing intended use: this repo is a content library for skills, agents, commands, and rules — not a deployment tool; content is distributed via `npx skills`, rulesync, and the Claude plugin system
- [ ] Document the `global/` vs `project/` scope split and what each is for
- [ ] Document provider-specific subdirectory conventions (`claude-code/`, `windsurf/`, `copilot/`)
- [ ] Create `CLAUDE.md` at repo root as a hard link to `AGENTS.md` (`ln AGENTS.md CLAUDE.md`) so both Claude Code and AGENTS.md-compatible tools read the same file
- [ ] Verify both files have identical inode (confirm hard link, not copy)
- [ ] **Commit**: `docs(repo): add AGENTS.md and CLAUDE.md hard link with repo intent and structure guide`
- [ ] **Checkpoint**: read both files and confirm they reflect the final structure accurately
