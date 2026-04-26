#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["click", "pyyaml", "questionary"]
# ///
"""CLI for managing and porting rules between providers."""

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Final

import click
import questionary
import yaml


class Provider(StrEnum):
    """Supported rule provider targets."""

    CLAUDE_CODE = "claude-code"
    WINDSURF = "windsurf"
    COPILOT_VSCODE = "copilot-vscode"
    COPILOT_JETBRAINS = "copilot-jetbrains"
    UNIVERSAL = "universal"
    ALL = "all"


class TriggerMode(StrEnum):
    """Activation modes for a rule."""

    ALWAYS_ON = "always_on"
    MODEL_DECISION = "model_decision"
    GLOB = "glob"
    MANUAL = "manual"


class Scope(StrEnum):
    """Deployment scope for a rule."""

    GLOBAL = "global"
    PROJECT = "project"


@dataclass
class _ConvertArgs:
    """Parsed fields passed to each per-provider converter."""

    trigger: TriggerMode
    name: str
    description: str
    patterns: list[str]
    header: str
    body: str

    @property
    def use_glob(self) -> bool:
        """Return True when glob trigger is active and patterns are present."""
        return self.trigger == TriggerMode.GLOB and bool(self.patterns)


class RulesManager:
    """Manages discovery, conversion, and porting of universal rules to provider-specific formats."""

    PORTABLE_PROVIDERS: Final[list[Provider]] = [
        Provider.CLAUDE_CODE,
        Provider.WINDSURF,
        Provider.COPILOT_VSCODE,
        Provider.COPILOT_JETBRAINS,
    ]

    def __init__(self, rules_dir: Path = Path("rules")) -> None:
        """Initialize RulesManager.

        Args:
            rules_dir: Root directory containing provider subdirectories.
        """
        self.rules_dir = rules_dir

    def port_interactive(self, dry_run: bool = False) -> None:
        """Run interactive porting mode.

        Args:
            dry_run: When True, print the converted content without writing.
        """
        source_path = self.select_source_interactively()
        if source_path is None:
            click.echo("No source selected.")
            raise click.Abort()

        selected_target = RulesManager.select_target_interactively()
        if selected_target is None:
            click.echo("No target selected.")
            raise click.Abort()

        if not questionary.confirm("Proceed with port?").ask():
            click.echo("Aborted.")
            raise click.Abort()

        self.port_rule(source_path, selected_target, dry_run=dry_run)

    def port_direct(self, source: str, target: str, dry_run: bool = False) -> None:
        """Port with explicit source and target arguments.

        Args:
            source: Source file or directory path.
            target: Target provider string.
            dry_run: When True, print converted content without writing.
        """
        source_path = Path(source)
        if not source_path.exists():
            raise click.ClickException(f"Error: Source not found at {source_path}")

        if source_path.is_dir():
            self.port_directory(source_path, target, dry_run=dry_run)
        else:
            self.port_rule(source_path, target, dry_run=dry_run)

    def port_directory(
        self, source_dir: Path, target: str, dry_run: bool = False
    ) -> None:
        """Port all .md files in a directory to one or more providers.

        Args:
            source_dir: Directory containing universal rule files.
            target: Provider string or 'all'.
            dry_run: When True, print converted content without writing.
        """
        files = list(source_dir.rglob("*.md"))
        if not files:
            click.echo(f"Error: No .md files found in {source_dir}", err=True)
            return

        prefix = "[DRY RUN] " if dry_run else ""
        click.echo(
            f"{prefix}Porting {len(files)} files from {source_dir} to {target}..."
        )

        for f in files:
            self.port_rule(f, target, dry_run=dry_run)

        click.echo(
            f"{prefix}Successfully ported {len(files)} files from {source_dir} to {target}"
        )

    def port_rule(self, source: Path, target: str, dry_run: bool = False) -> None:
        """Port a single universal rule file to one or more providers.

        Prompts for confirmation when the source file has no frontmatter.
        Silently overwrites existing provider-specific files.

        Args:
            source: Path to the universal source .md file.
            target: Provider string or 'all'.
            dry_run: When True, print the converted content without writing.
        """
        providers = (
            RulesManager.PORTABLE_PROVIDERS
            if target == Provider.ALL
            else [Provider(target)]
        )
        prefix = "[DRY RUN] " if dry_run else ""

        content = source.read_text()
        fm, body = self._parse_frontmatter(content)

        if not content.startswith("---"):
            confirmed = questionary.confirm(
                f"{source} has no frontmatter — port as always-on rule?"
            ).ask()
            if not confirmed:
                click.echo("Aborted.")
                return

        source_rel = str(source.relative_to(self.rules_dir / "universal"))
        count = 0

        for provider in providers:
            out_content = self._convert(provider, fm, body, f"universal/{source_rel}")
            out_path = self._output_path(source, provider)

            if dry_run:
                click.echo(f"\n{prefix}Would write: {out_path}")
                click.echo(out_content)
            else:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(out_content)
                click.echo(f"{prefix}Written: {out_path}")
            count += 1

        click.echo(
            f"{prefix}Successfully ported {source.name} to {', '.join(str(p) for p in providers)}"
        )

    @staticmethod
    def get_available_providers() -> list[str]:
        """Return the list of portable provider names.

        Returns:
            List of provider string values (excludes 'universal' and 'all').
        """
        return [str(p) for p in RulesManager.PORTABLE_PROVIDERS]

    def get_available_sources(self) -> list[Path]:
        """Scan the universal/ directory and return all rule file paths.

        Returns:
            Sorted list of .md file paths under rules_dir/universal/.
        """
        universal_dir = self.rules_dir / "universal"
        if not universal_dir.exists():
            return []
        return sorted(universal_dir.rglob("*.md"))

    def select_source_interactively(self) -> Path | None:
        """Prompt the user to select a source rule from universal/.

        Returns:
            Absolute path to the selected rule file, or None if cancelled.
        """
        sources = self.get_available_sources()
        if not sources:
            click.echo("Error: No universal rules found.", err=True)
            return None
        universal_dir = self.rules_dir / "universal"
        choices = [str(p.relative_to(universal_dir)) for p in sources]
        selected = questionary.select("Select source rule:", choices=choices).ask()
        if selected is None:
            return None
        return universal_dir / selected

    @staticmethod
    def select_target_interactively() -> str | None:
        """Prompt the user to select a target provider.

        Returns:
            Provider string (e.g. 'claude-code', 'all'), or None if cancelled.
        """
        providers = RulesManager.get_available_providers() + [str(Provider.ALL)]
        return questionary.select("Select target provider:", choices=providers).ask()

    @staticmethod
    def _convert(provider: Provider, fm: dict, body: str, source_rel: str) -> str:
        """Convert universal frontmatter to provider-specific syntax.

        Unsupported activation modes (model_decision, manual) are silently
        downgraded to always-on by omitting pattern fields.

        Args:
            provider: Target provider.
            fm: Parsed universal frontmatter dict.
            body: Rule body (markdown content after frontmatter).
            source_rel: Relative path used in the generated-file header comment.

        Returns:
            Full file content ready to write for the given provider.

        Raises:
            ValueError: If provider is not a known portable provider.
        """
        args = _ConvertArgs(
            trigger=TriggerMode(fm["trigger"])
            if fm.get("trigger")
            else TriggerMode.ALWAYS_ON,
            name=fm.get("name", ""),
            description=fm.get("description", ""),
            patterns=fm.get("patterns") or [],
            header=RulesManager._generated_header(source_rel),
            body=body,
        )
        converter = RulesManager._get_converters().get(provider)
        if converter is None:
            raise ValueError(f"Unknown provider: {provider}")
        return converter(args)

    @staticmethod
    def _convert_claude_code(args: _ConvertArgs) -> str:
        """Render claude-code frontmatter with paths as YAML list, or no frontmatter.

        Claude Code only supports paths: — no description or other fields.
        Non-glob triggers produce no frontmatter at all.

        Args:
            args: Parsed conversion arguments.

        Returns:
            Full file content for claude-code.
        """
        # For always_on and model_decision, no frontmatter at all
        if not args.use_glob:
            return f"{args.header}\n{args.body}"

        # For glob triggers, use paths: YAML list only
        fm_lines: list[str] = ["---"]
        fm_lines.append("paths:")
        for p in args.patterns:
            fm_lines.append(f"  - {p}")
        fm_lines.append("---")
        return "\n".join(fm_lines) + f"\n{args.header}\n{args.body}"

    @staticmethod
    def _convert_windsurf(args: _ConvertArgs) -> str:
        """Render windsurf frontmatter with optional trigger and comma-separated globs.

        Args:
            args: Parsed conversion arguments.

        Returns:
            Full file content for windsurf.
        """
        fm_lines: list[str] = ["---"]
        if args.use_glob:
            fm_lines.append("trigger: glob")
        elif args.trigger and args.trigger != "glob":
            fm_lines.append(f"trigger: {args.trigger}")
        if args.description:
            fm_lines.append(f"description: {args.description}")
        if args.use_glob:
            fm_lines.append(f"globs: {', '.join(args.patterns)}")
        else:
            fm_lines.append("globs:")
        fm_lines.append("---")
        return "\n".join(fm_lines) + f"\n{args.header}\n{args.body}"

    @staticmethod
    def _convert_copilot_vscode(args: _ConvertArgs) -> str:
        """Render copilot-vscode frontmatter with name, description, and applyTo.

        Args:
            args: Parsed conversion arguments.

        Returns:
            Full file content for copilot-vscode.
        """
        fm_lines: list[str] = ["---"]
        if args.name:
            fm_lines.append(f"name: {args.name}")
        if args.description:
            fm_lines.append(f"description: {args.description}")
        if args.use_glob:
            apply_to = ", ".join(args.patterns)
            fm_lines.append(f'applyTo: "{apply_to}"')
            if len(args.patterns) > 1:
                click.echo(
                    "Warning: multi-pattern applyTo has a known bug in Copilot VSCode"
                    " and may not work reliably.",
                    err=True,
                )
        fm_lines.append("---")
        return "\n".join(fm_lines) + f"\n{args.header}\n{args.body}"

    @staticmethod
    def _convert_copilot_jetbrains(args: _ConvertArgs) -> str:
        """Render copilot-jetbrains output with no frontmatter.

        Args:
            args: Parsed conversion arguments.

        Returns:
            Full file content for copilot-jetbrains (header + body only).
        """
        return f"{args.header}\n{args.body}"

    @staticmethod
    def _get_converters() -> dict[Provider, Callable[[_ConvertArgs], str]]:
        """Return the mapping of providers to their converter functions."""
        return {
            Provider.CLAUDE_CODE: RulesManager._convert_claude_code,
            Provider.WINDSURF: RulesManager._convert_windsurf,
            Provider.COPILOT_VSCODE: RulesManager._convert_copilot_vscode,
            Provider.COPILOT_JETBRAINS: RulesManager._convert_copilot_jetbrains,
        }

    @staticmethod
    def _parse_frontmatter(content: str) -> tuple[dict, str]:
        """Parse YAML frontmatter from a markdown file.

        Args:
            content: Full file content.

        Returns:
            Tuple of (frontmatter dict, body string). Returns ({}, content)
            when no valid frontmatter block is found.
        """
        if not content.startswith("---"):
            return {}, content
        end = content.find("\n---", 3)
        if end == -1:
            return {}, content
        fm_text = content[3:end].strip()
        body = content[end + 4 :].lstrip("\n")
        fm = yaml.safe_load(fm_text) or {}
        return fm, body

    def _output_path(self, source: Path, provider: Provider) -> Path:
        """Compute the output path for a ported rule file.

        Args:
            source: Absolute path to the universal source file.
            provider: Target provider.

        Returns:
            Destination path under rules_dir/<provider>/.
        """
        return (
            self.rules_dir
            / str(provider)
            / source.relative_to(self.rules_dir / "universal")
        )

    @staticmethod
    def _generated_header(source_rel: str) -> str:
        """Return the AUTO-GENERATED HTML comment for a given source path.

        Args:
            source_rel: Relative path to the universal source file.

        Returns:
            HTML comment string pointing back to the universal source.
        """
        return f"<!-- AUTO-GENERATED by rules port — edit {source_rel} instead -->"


@click.group()
def cli() -> None:
    """Rules management CLI."""


@cli.command()
@click.argument("source", required=False)
@click.option("--to", "target", default=None, help="Target provider (or 'all')")
@click.option("--dry-run", is_flag=True, help="Preview without writing files")
def port(source: str | None, target: str | None, dry_run: bool) -> None:
    """Port a universal rule to one or more providers.

    \b
    Examples:
      rules port                                          # interactive
      rules port universal/my-rule.md --to claude-code
      rules port universal/my-dir --to all
      rules port universal/my-rule.md --to windsurf --dry-run
    """
    manager = RulesManager()

    match (source is None, target is None):
        case (True, True):
            manager.port_interactive(dry_run=dry_run)
        case (False, False):
            manager.port_direct(source, target, dry_run=dry_run)
        case (True, False):
            raise click.ClickException("Provide a source when specifying --to.")
        case (False, True):
            raise click.ClickException("Provide --to when specifying a source.")


if __name__ == "__main__":
    cli()
