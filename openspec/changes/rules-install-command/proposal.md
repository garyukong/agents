## Why

Rules are ported to `rules/<provider>/` but there is no way to deploy them into target repos. Developers must manually copy or link files, which is error-prone and breaks when the agents repo moves.

## What Changes

- Add `rules install` subcommand — creates symlinks from provider-specific rule files into target repo (or global config dir)
- Add `rules check` subcommand — verifies installed symlinks are not broken
- Add `rules remove` subcommand — removes installed symlinks

## Capabilities

### New Capabilities

- `rules-install`: Install provider-specific rules into a target repo or global config dir via symlink, with interactive scope selection (global vs project)
- `rules-check`: Scan known install locations and report symlink health (OK / broken / missing)
- `rules-remove`: Remove installed symlinks by source and scope

### Modified Capabilities

## Impact

- `scripts/rules.py` — new CLI subcommands added; no changes to existing `port` logic
- Target repos — symlinks written to `.claude/rules/`, `.windsurf/rules/`, or `.github/instructions/` depending on provider
- Installed rules are a local dev concern and should not be committed (`.gitignore` recommended per provider)
