## 1. Shared Infrastructure

- [ ] 1.1 Add `_infer_provider_from_source()` static method — parse provider from source path prefix (`rules/<provider>/...`)
- [ ] 1.2 Add `_infer_scope_from_source()` static method — return `Scope.GLOBAL` if path contains `global/` segment, `Scope.PROJECT` if a named project subdir is present, `None` if ambiguous
- [ ] 1.3 Add `_install_target_dir()` static method — map (provider, scope, repo_path) → target directory
- [ ] 1.4 Add `_install_target_name()` static method — handle `.md` → `.instructions.md` rename for copilot providers
- [ ] 1.5 Add `_resolve_scope_interactively()` static method — questionary prompt for global vs project, excluding global for copilot providers; only called when `_infer_scope_from_source()` returns `None`

## 2. `rules install` command

- [ ] 2.1 Add `install` click command with `source` arg, `--to` option, `--provider` option
- [ ] 2.2 Implement single-file install: resolve target dir + name, create parent dirs, create symlink
- [ ] 2.3 Implement directory install: glob all `.md` files in source dir, install each
- [ ] 2.4 Wire scope resolution: infer from source path via `_infer_scope_from_source()`; fall back to `_resolve_scope_interactively()` only when ambiguous and `--to` omitted
- [ ] 2.5 Print install summary (symlink path created)

## 3. `rules check` command

- [ ] 3.1 Add `check` click command (no required args)
- [ ] 3.2 Implement scan of all global provider dirs (`~/.claude/rules/`, `~/.windsurf/rules/`)
- [ ] 3.3 Implement scan of project dirs — walk `.claude/rules/`, `.windsurf/rules/`, `.github/instructions/` under a base path (default `~/`)
- [ ] 3.4 For each symlink found: resolve and report OK or broken
- [ ] 3.5 Exit non-zero if any broken symlinks found

## 4. `rules remove` command

- [ ] 4.1 Add `remove` click command with `source` arg, `--from` option
- [ ] 4.2 Implement single-file remove: resolve target path, verify symlink exists, unlink
- [ ] 4.3 Implement directory remove: glob `.md` files in source dir, remove each symlink
- [ ] 4.4 Wire scope resolution: infer from source path; fall back to `_resolve_scope_interactively()` when ambiguous and `--from` omitted
- [ ] 4.5 Error and exit non-zero if symlink not found at resolved path

## 5. Tests

- [ ] 5.1 Test `_infer_provider_from_source()` for each provider path prefix
- [ ] 5.2 Test `_infer_scope_from_source()` — `global/` → GLOBAL, named subdir → PROJECT, root file → None
- [ ] 5.3 Test `_install_target_dir()` for each provider × scope combination
- [ ] 5.4 Test `_install_target_name()` — copilot rename, others unchanged
- [ ] 5.5 Test install single file from `global/` installs to global target without prompt
- [ ] 5.6 Test install single file from named project subdir prompts for repo path only
- [ ] 5.7 Test install directory creates symlinks for all `.md` files
- [ ] 5.8 Test install creates target directory if missing
- [ ] 5.9 Test check reports OK for valid symlinks
- [ ] 5.10 Test check reports broken for dangling symlinks
- [ ] 5.11 Test check exits non-zero when broken symlinks exist
- [ ] 5.12 Test remove deletes symlink at resolved path
- [ ] 5.13 Test remove errors when symlink not found
