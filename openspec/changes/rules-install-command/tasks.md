## 1. Shared Infrastructure — tests then implementation

- [ ] 1.1 Write tests for `_infer_provider_from_source()` — each provider path prefix
- [ ] 1.2 Implement `_infer_provider_from_source()` — parse provider from `rules/<provider>/...`
- [ ] 1.3 Write tests for `_infer_scope_from_source()` — `global/` → GLOBAL, named subdir → PROJECT, root file → None
- [ ] 1.4 Implement `_infer_scope_from_source()` — return `Scope.GLOBAL`, `Scope.PROJECT`, or `None`
- [ ] 1.5 Write tests for `_install_target_dir()` — each provider × scope combination
- [ ] 1.6 Implement `_install_target_dir()` — map (provider, scope, repo_path) → target directory
- [ ] 1.7 Write tests for `_install_target_name()` — copilot rename, others unchanged
- [ ] 1.8 Implement `_install_target_name()` — `.md` → `.instructions.md` for copilot providers
- [ ] 1.9 Implement `_resolve_scope_interactively()` — questionary prompt, no global option for copilot

## 2. `rules install` command — tests then implementation

- [ ] 2.1 Write test: install single file from `global/` creates symlink at global target without prompt
- [ ] 2.2 Write test: install single file from named project subdir prompts for repo path only
- [ ] 2.3 Write test: install single file with `--to` creates symlink at project target
- [ ] 2.4 Write test: install copilot file renames to `.instructions.md`
- [ ] 2.5 Write test: install directory creates symlinks for all `.md` files
- [ ] 2.6 Write test: install creates target directory if missing
- [ ] 2.7 Implement `install` click command with `source` arg, `--to` option, `--provider` option
- [ ] 2.8 Implement single-file install: infer scope → resolve target dir + name → create parent dirs → create symlink
- [ ] 2.9 Implement directory install: glob `.md` files in source dir, install each
- [ ] 2.10 Wire scope fallback: call `_resolve_scope_interactively()` when scope ambiguous and `--to` omitted

## 3. `rules check` command — tests then implementation

- [ ] 3.1 Write test: check reports OK for valid symlinks
- [ ] 3.2 Write test: check reports broken for dangling symlinks
- [ ] 3.3 Write test: check exits non-zero when any broken symlinks exist
- [ ] 3.4 Write test: check prints message when no installed rules found
- [ ] 3.5 Implement `check` click command
- [ ] 3.6 Implement scan of global provider dirs (`~/.claude/rules/`, `~/.windsurf/rules/`)
- [ ] 3.7 Implement scan of project dirs — walk `.claude/rules/`, `.windsurf/rules/`, `.github/instructions/` under base path

## 4. `rules remove` command — tests then implementation

- [ ] 4.1 Write test: remove deletes symlink at resolved path
- [ ] 4.2 Write test: remove directory removes symlinks for all `.md` files
- [ ] 4.3 Write test: remove errors and exits non-zero when symlink not found
- [ ] 4.4 Implement `remove` click command with `source` arg, `--from` option
- [ ] 4.5 Implement single-file remove: infer scope → resolve target path → verify symlink exists → unlink
- [ ] 4.6 Implement directory remove: glob `.md` files in source dir, remove each symlink
- [ ] 4.7 Wire scope fallback: call `_resolve_scope_interactively()` when ambiguous and `--from` omitted
