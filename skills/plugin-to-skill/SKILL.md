---
name: plugin-to-skill
description: >
  Convert a full Claude plugin into Agent Skills–compliant skill directories. Supports
  commands/skills/agents from the plugin; hooks/MCP/LSP are documented as compatibility
  notes only (not converted). Use when you need to emit validated SKILL.md files plus any
  referenced scripts/references/assets for Agent Skills clients.
license: MIT
compatibility: Requires local filesystem access; recommends git, jq, and Python 3.11+ if scripts are used.
metadata:
  author: internal
  version: "0.2.0"
allowed-tools: Read Bash(jq:*) Bash(python3:*) Bash(git:*)
---

# Reference
- See [skill_spec.md](references/skill_spec.md) for the full Agent Skills specification.

# Goal
Transform a full Claude plugin (commands/, skills/, agents/, optional hooks/MCP/LSP, optional
manifest) into one or more validated Agent Skills (each SKILL.md + optional
scripts/references/assets) aligned with the Agent Skills specification.

# When to use
- You have a Claude plugin and must ship Agent Skills for Agent Skills clients.
- You need a reproducible workflow to convert commands/skills/agents into SKILL.md + assets.
- You must document hooks/MCP/LSP expectations as compatibility notes without converting them.
- You want pushy, intent-focused trigger descriptions and evals for quality gates.

# Inputs
- Claude plugin root (may include .claude-plugin/plugin.json, commands/, skills/, agents/, hooks/, .mcp.json, .lsp.json)
- Target Agent Skill name(s) per naming convention
- Optional license and metadata (author/version)
- Optional llms.txt index (https://code.claude.com/docs/llms.txt) to locate canonical docs

# Outputs
```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

# Naming convention
- Converted agents: `agent-<plugin-name>-<agent-name>`
- Converted commands: `<plugin-name>-<command-name>`
- Existing skills: `<plugin-name>-<skill-name>`
- All names: lowercase, hyphen-separated, 1–64 chars, must match the folder name.

# Workflow
1) Discover documentation
   - Fetch https://code.claude.com/docs/llms.txt if needed to locate component pages.
   - Note default paths: commands/ or skills/ for user commands, agents/ for subagents, hooks/hooks.json, .mcp.json, .lsp.json, .claude-plugin/plugin.json for manifest.

2) Inventory plugin components
   - List commands/, skills/, agents/, hooks/, MCP, LSP, manifest fields, settings.json.
   - For each command/skill directory, capture purpose, inputs, outputs, workflows.
   - For agents, capture role/when-to-invoke; decide if they become separate skills or enrich one skill’s “When to use”.
   - For hooks, capture events/matchers; surface only as optional safeguards/post-steps (do not convert).
   - For MCP/LSP configs, extract runtime needs into compatibility; do not embed external binaries.

3) Derive Agent Skill identity
   - Apply naming convention for commands/agents/existing skills.
   - Write an imperative description (≤1024 chars): “Use this skill when … even if the user …”.
   - Carry license/metadata; add compatibility only when non-default requirements exist or when noting hooks/MCP/LSP expectations.

4) Build SKILL.md frontmatter
   - Populate name, description, license (MIT if absent), compatibility (env/runtime/binaries/hooks/MCP/LSP expectations), metadata.
   - Omit allowed-tools if not relevant; include when safe defaults help.

5) Build SKILL.md body (procedural)
   - Purpose: 1–3 sentences.
   - When to use: 3–6 concrete triggers including implicit intents.
   - Inputs/Outputs: bullets for files, arguments, artifacts produced.
   - Workflow: numbered, reproducible steps distilled from commands/skills; prefer defaults over menus.
   - Edge cases & safeguards: missing files, oversized inputs, secrets, network/offline expectations.
   - Compatibility notes: mention hooks/MCP/LSP expectations and how to approximate manually if needed.
   - Quality bar: acceptance checks and success criteria.
   - Available scripts: list and show invocation examples if scripts/ exist.

6) Scripts and references (optional)
   - Move executable blocks into scripts/ with pinned deps or PEP 723 headers; avoid interactive prompts, add --help, structured JSON output, clear exit codes.
   - Place long-form material into references/*.md and link from body.

7) Tune description triggers
   - Make description pushy and intent-focused; include domain keywords and near-miss phrasing to improve triggering.
   - Keep concise to preserve context budget.

8) Seed evals (optional but recommended)
   - Add evals/evals.json with 2–3 should_trigger and 2 should_not_trigger prompts mirroring plugin tasks and near-misses.
   - Include expected_output and assertions (e.g., “produces mermaid diagram”, “runs formatter-style post-step if noted”).

9) Validate
   - Run `skills-ref validate ./<skill-name>` for Agent Skills compliance.
   - Ensure paths remain relative and inside plugin root (no ../ traversal).

# Safeguards & scope constraints
- Only commands/*.md, skills/*/SKILL.md, and agents/*.md become Agent Skills.
- Hooks, MCP servers, and LSP configs are *not* supported by the Agent Skills spec; capture them as compatibility notes, safeguards, or post-steps but do not attempt to convert.
- If multiple agents/commands are unrelated, emit multiple skills; avoid omnibus skills.
- Commands/skills that are purely instructional stay as workflow steps; executable flows move to scripts/.
- MCP/LSP binaries are not bundled; describe requirements in compatibility and keep paths relative.
- Hooks are informational only; document as optional post-steps; do not assume automation.
- Strip marketing fluff; keep actionable, procedural content.
- If no license is given, use MIT or point to LICENSE.txt if provided.

# Quality bar (success means)
- SKILL.md passes `skills-ref validate`.
- Description is ≤1024 chars, imperative, intent-focused, and clearly states when to use.
- Workflow steps are reproducible and non-interactive.
- Scripts (if any) are documented with usage, pinned deps, structured output, and no interactive prompts.
- Evals (if present) are realistic and cover should/should-not trigger.

# Few-shot mapping examples
- Plugin `code-documentation`, command `doc-generate.md` → skill folder `code-documentation-generate/` with SKILL.md capturing generation workflow; hooks (if any) noted in compatibility only.
- Plugin `code-documentation`, agent `code-reviewer.md` → skill folder `agent-code-documentation-code-reviewer/`; preserve purpose/when-to-use, add workflow from agent prompt; note no hooks/MCP conversion.
- Plugin `pdf-processor`, existing skill `skills/pdf-processor/SKILL.md` → skill folder `pdf-processor/` (keep original skill name); carry over scripts/references as-is, add compatibility if MCP/LSP expectations exist.
