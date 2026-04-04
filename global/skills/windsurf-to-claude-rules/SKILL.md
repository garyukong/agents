---
name: windsurf-to-claude-rules
description: Ports .windsurf/rules/*.md files to .claude/rules/ format by converting Windsurf frontmatter to Claude frontmatter. Use this skill whenever the user wants to migrate, port, sync, or convert Windsurf rules to Claude rules, or asks to set up .claude/rules from existing .windsurf/rules files.
---

# Port Windsurf Rules to Claude Rules

Convert `.windsurf/rules/*.md` files to `.claude/rules/` format. The only change is frontmatter — body content is copied verbatim.

## Frontmatter conversion rules

| Windsurf frontmatter | Claude equivalent |
|---|---|
| `trigger: always` | No frontmatter — Claude loads unconditionally |
| `trigger: model_decision` | No frontmatter — Claude loads unconditionally |
| `trigger: glob` + `globs: "pattern"` | `paths:\n  - "pattern"` |
| `description: ...` | Drop entirely — not a Claude field |

Claude rules support only one frontmatter field: `paths` (a YAML list of glob patterns).
Rules without `paths` frontmatter load every session unconditionally.

## Steps

.Run the bundled script via `ctx_execute` (keeps output out of context):

```python
import subprocess, sys
result = subprocess.run(
    [sys.executable, "<skill_dir>/scripts/port.py", "<project_dir>"],
    capture_output=True, text=True
)
print(result.stdout or result.stderr)
```

To port a single file, add `--file <filename>`. To overwrite existing files, add `--overwrite`.

Report the script's output to the user — each line shows `PORT`, `SKIP`, or `ERROR` per file.

## Example

**Input** (`.windsurf/rules/testing.md`):
```
---
trigger: glob
description: Unit test conventions
globs: tests/**/*
---

# Testing Rules
See tests/AGENTS.md.
```

**Output** (`.claude/rules/testing.md`):
```
---
paths:
  - "tests/**/*"
---

# Testing Rules
See tests/AGENTS.md.
```

**Input** (`.windsurf/rules/architecture.md`):
```
---
trigger: always
description: Architecture overview
globs:
---

# Architecture
...
```

**Output** (`.claude/rules/architecture.md`):
```
# Architecture
...
```
