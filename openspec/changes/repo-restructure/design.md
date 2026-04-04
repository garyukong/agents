## Context

The repo currently has no consistent organisational model. Skills, agents, and commands are buried inside plugin directories, with no coverage for Windsurf or Copilot. Deployment is handled by separate tools (`npx skills` for skills, Claude plugin installer for plugins) with no mechanism for rules, agents, or commands.

Key constraints discovered during exploration:
- **agentskills.io** is a universal spec supported by Claude Code, Windsurf, and Copilot — skills use `SKILL.md` format identically across all providers
- **Rules** differ by provider (incompatible frontmatter schemas) but share a universal format via AGENTS.md
- **Agents** are Claude Code-only (file-based); no equivalent in Windsurf or Copilot
- **Commands** differ by provider (different frontmatter, paths, extensions)
- **Plugins** differ by provider (Claude plugin manifest vs Copilot extensions)
- `npx skills` already handles skill deployment — this repo is content, not a deployment tool

## Goals / Non-Goals

**Goals:**
- Consistent, predictable directory structure navigable without prior knowledge
- Clear separation of universal vs provider-specific content
- Clear separation of global (machine-wide) vs project-scoped content
- Skills remain deployable via `npx skills install garyukong/agents`
- Plugins remain thin manifests that symlink into canonical skill locations
- Eliminate `plugin-skill-ports/` as a concept

**Non-Goals:**
- Building a new deployment/sync tool (existing tools handle this)
- Migrating Windsurf or Copilot content (starts empty, structure is ready)
- Changing skill content or behaviour

## Decisions

### D1: Scope as top-level axis (`global/` vs `project/`)

**Decision:** `global/` and `project/` are the top-level directories.

**Rationale:** The primary use case is deployment — "set up this machine" or "initialise this project". Scope-first makes the deploy command trivially simple: grab everything under `global/` or `project/`. Content-type-first would require traversing all subtrees per deployment.

**Alternative considered:** Content-type first (`skills/`, `rules/`, etc. at root with scope as inner dirs). Rejected because deploy logic becomes more complex and the browsing use case is secondary to deployment.

---

### D2: Skills are flat within their group (`skills/python-development/*.SKILL.md`)

**Decision:** Skills have no provider subdirectories. Provider scoping is expressed via the `compatibility` frontmatter field per the agentskills.io spec.

**Rationale:** agentskills.io defines a universal `SKILL.md` format. All three providers consume it identically. Adding `claude-code/` subdirs would be redundant — the spec's `compatibility` field already handles this without structural overhead.

**Alternative considered:** `skills/claude-code/openspec-*/` for Claude-specific skills. Rejected once confirmed all providers support the same spec.

---

### D3: Skills are grouped by domain (`skills/python-development/python-code-style/`)

**Decision:** Skills are nested one level under a group directory matching their plugin/domain.

**Rationale:** A flat `skills/` with 30+ individual skills is hard to browse. Groups mirror the existing plugin structure (1:1 relationship: `skills/python-development/` ↔ `plugins/claude-code/python-development/`), making the symlink relationship obvious.

**Alternative considered:** Flat naming with prefixes (`python-development-code-style/`). Rejected as unscalable.

---

### D4: Rules have both `universal/` and provider subdirs

**Decision:** `rules/universal/` for AGENTS.md-compatible content; `rules/claude-code/`, `rules/windsurf/`, `rules/copilot/` for provider-specific rules.

**Rationale:** AGENTS.md is a universal format (plain markdown, no frontmatter) supported identically across all providers. Individual rule files have incompatible frontmatter schemas per provider — these must remain separated. The existing `windsurf-to-claude-rules` skill handles conversion between formats.

---

### D5: Plugins reference skills via a sync script, not symlinks

**Decision:** `plugins/claude-code/<name>/skills/` contains **physically copied files** kept in sync via a script, not symlinks. Symlinks are maintained in the working tree as the authoring convenience, but a pre-commit/CI step resolves them into copies before the plugin is published.

**Rationale:** Claude Code's `/plugin install` uses `git-subdir` sparse clone for individual plugin installs — it fetches only the plugin subdirectory. Symlinks pointing to `../../../../global/skills/` land broken because `global/skills/` is never fetched. Symlinks DO resolve when the full repo is cloned via the marketplace (since `.claude-plugin/marketplace.json` triggers a full clone), but relying on this is fragile.

**For now:** Plugin `skills/` directories contain physical copies of skill files. A sync script to automate this is deferred to a follow-on change.

**Alternative considered:** Relying on full-repo marketplace clone (symlinks work in this path). Rejected — fragile; breaks for any `git-subdir` install path and for any future distribution outside this repo's marketplace.

---

### D6: Agents are Claude Code-only for now

**Decision:** `agents/` contains only `claude-code/` subdir. No `universal/` level.

**Rationale:** No universal file-based agent format exists. Windsurf and Copilot do not support user-defined agent definitions in a comparable file format. Adding empty `windsurf/` and `copilot/` dirs would be speculative.

---

### D7: Deployment tooling stays external

**Decision:** No new deployment tool is built. `npx skills` handles skills; rulesync handles rules; Claude plugin installer handles plugins.

**Rationale:** `npx skills` already works for skill distribution from this repo. Rulesync covers rules across 10+ providers with global/project modes. Building custom deployment for rules would duplicate well-maintained OSS tooling.

**A `deploy` skill** (created via skill-creator) will cover agents and commands deployment — the gap not covered by `npx skills` or rulesync. This is deferred to a follow-on change.

## Risks / Trade-offs

- **Symlink resolution on deploy** → Use `cp -rL` or `rsync -L` when copying plugins to target projects. Document in deploy command.
- **`global/` nesting adds path depth** → `global/skills/python-development/python-code-style/SKILL.md` is longer than before. Acceptable given the clarity gain.
- **`npx skills` discovery path** → The agentskills spec discovers from `.agents/skills/`. After restructure, `global/skills/` is the source; installed copies still land in `.agents/skills/` via `npx skills`. No change to discovery behaviour.
- **`project/` starts empty** → Content is placeholders only. Team must populate project-scoped templates over time.

## Migration Plan

1. Create new `global/` and `project/` directory skeletons
2. Move all content from `plugins/*/skills/` → `global/skills/<group>/`
3. Move all content from `plugins/*/agents/` → `global/agents/claude-code/`
4. Move all content from `plugins/*/commands/` → `global/commands/claude-code/openspec/`
5. Move `rules/global_rules.md` → `global/rules/universal/global.md`
6. Move `rules/CLAUDE.md` content → `global/rules/claude-code/context-mode.md`
7. Move existing `skills/*` standalone skills → `global/skills/<appropriate-group-or-standalone>/`
8. Rebuild `plugins/` as `global/plugins/claude-code/<name>/` with symlinks
9. Delete `plugin-skill-ports/` and old `plugins/`, `skills/`, `rules/`, `commands/` roots
10. Verify `npx skills` still resolves correctly from new paths

**Rollback:** All moves are git-tracked. `git revert` restores previous structure.

## Open Questions

- ~~Should `commands/deploy/` be implemented now or deferred?~~ **Deferred.** Out of scope for this restructure.
- ~~Sync script for plugin symlink resolution~~ **Deferred.** Plugins ship with physical copies for now; sync script is a follow-on change.
- ~~Should `global/rules/universal/global.md` be renamed `AGENTS.md`?~~ **No.** Filename stays `global.md`; AGENTS.md is a deploy-time output, not a source file name.
- ~~Should `skills-lock.json` path change?~~ **No.** `skills-lock.json` tracks installed skills, not source paths — no change needed.
