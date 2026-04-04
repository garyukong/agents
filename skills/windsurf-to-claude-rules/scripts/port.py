#!/usr/bin/env python3
"""Port .windsurf/rules/*.md files to .claude/rules/ format.

Usage:
    python port.py <project_dir> [--file <filename>] [--overwrite]

Arguments:
    project_dir   Root of the project (contains .windsurf/ and .claude/)
    --file        Port a single file by name (e.g. unit-testing.md)
    --overwrite   Overwrite existing .claude/rules/ files (default: skip)
"""

import argparse
import re
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from a markdown file.

    Args:
        text: Full file content including optional frontmatter block.

    Returns:
        A tuple of (frontmatter_dict, body) where frontmatter_dict contains
        key-value pairs from the YAML block and body is the remaining content.
        If no frontmatter is present, returns ({}, text).
    """
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return {}, text

    body = text[match.end():]
    fm: dict = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body


def convert(fm: dict, body: str) -> str:
    """
    Build Claude-format file content from parsed Windsurf frontmatter.

    Windsurf's `trigger: always` and `trigger: model_decision` map to no
    frontmatter in Claude (rules load unconditionally). `trigger: glob` maps
    to a `paths` list. `trigger: manual` has no Claude equivalent — it is
    ported as no frontmatter with a warning. All other Windsurf fields are
    dropped.

    Args:
        fm: Parsed frontmatter dict from a Windsurf rules file.
        body: File body content after the closing frontmatter delimiter.

    Returns:
        A tuple of (file_content, warning). `file_content` is the full Claude
        rules file string. `warning` is non-empty when the trigger type has no
        exact Claude equivalent (e.g. `manual`), otherwise an empty string.
    """
    trigger = fm.get("trigger", "")
    globs = fm.get("globs", "").strip()
    warning = ""

    if trigger == "manual":
        warning = (
            "trigger: manual has no Claude equivalent — ported as always-load. "
            "Consider converting to a skill instead."
        )
        return body.lstrip("\n"), warning

    if trigger in ("always", "model_decision") or not globs:
        # No frontmatter — loads unconditionally
        return body.lstrip("\n"), warning

    # trigger: glob — convert globs to paths list
    patterns = [g.strip() for g in globs.split(",") if g.strip()]
    paths_yaml = "\n".join(f'  - "{p}"' for p in patterns)
    return f"---\npaths:\n{paths_yaml}\n---\n{body}", warning


def port_file(src: Path, dst: Path, overwrite: bool) -> str:
    """
    Convert and write a single Windsurf rules file to Claude rules format.

    Args:
        src: Path to the source `.windsurf/rules/*.md` file.
        dst: Path to write the converted `.claude/rules/*.md` file.
        overwrite: If False, skip files that already exist at dst.

    Returns:
        A status line string indicating SKIP, PORT, or ERROR.
    """
    if dst.exists() and not overwrite:
        return f"  SKIP  {dst.name} (already exists, use --overwrite)"

    fm, body = parse_frontmatter(src.read_text())
    content, warning = convert(fm, body)
    dst.write_text(content)

    trigger = fm.get("trigger", "none")
    globs = fm.get("globs", "").strip()
    if trigger in ("always", "model_decision", "manual") or not globs:
        detail = "no frontmatter (always loads)"
    else:
        detail = f"paths: {globs}"

    line = f"  PORT  {src.name} → {detail}"
    if warning:
        line += f"\n  WARN  {src.name}: {warning}"
    return line


def main() -> None:
    """
    Parse CLI arguments and port Windsurf rules files to Claude rules format.

    Reads from `<project_dir>/.windsurf/rules/` and writes to
    `<project_dir>/.claude/rules/`, creating the target directory if needed.
    Prints a status line for each file processed.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--file", help="Port a single file by name")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    src_dir = args.project_dir / ".windsurf" / "rules"
    dst_dir = args.project_dir / ".claude" / "rules"

    if not src_dir.exists():
        print(f"ERROR: {src_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    dst_dir.mkdir(parents=True, exist_ok=True)

    files = [src_dir / args.file] if args.file else sorted(src_dir.glob("*.md"))
    if not files:
        print("No .md files found in .windsurf/rules/")
        return

    for src in files:
        if not src.exists():
            print(f"  ERROR {src.name} not found")
            continue
        print(port_file(src, dst_dir / src.name, args.overwrite))


if __name__ == "__main__":
    main()
