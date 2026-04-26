"""Tests for scripts/rules.py."""

import pytest
from pathlib import Path

from scripts.rules import Provider, RulesManager

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_universal(tmp_path: Path, filename: str, content: str) -> Path:
    """Write a universal rule file and return its path."""
    p = tmp_path / "rules" / "universal" / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


def _manager(tmp_path: Path) -> RulesManager:
    return RulesManager(rules_dir=tmp_path / "rules")


# ---------------------------------------------------------------------------
# _parse_frontmatter
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    def test_valid_frontmatter(self, tmp_path):
        # Given: a file with valid YAML frontmatter
        mgr = _manager(tmp_path)
        content = "---\ntrigger: glob\npatterns:\n  - '**/*.py'\n---\nbody text"

        # When: parsed
        fm, body = mgr._parse_frontmatter(content)

        # Then: the fields and body are extracted correctly
        assert fm["trigger"] == "glob"
        assert fm["patterns"] == ["**/*.py"]
        assert body == "body text"

    def test_no_frontmatter(self, tmp_path):
        # Given: a file with no frontmatter delimiter
        mgr = _manager(tmp_path)
        content = "just markdown"

        # When: parsed
        fm, body = mgr._parse_frontmatter(content)

        # Then: frontmatter is empty and body is the full content
        assert fm == {}
        assert body == content

    def test_unclosed_frontmatter(self, tmp_path):
        # Given: a file whose opening --- has no closing ---
        mgr = _manager(tmp_path)
        content = "---\ntrigger: glob\n"

        # When: parsed
        fm, body = mgr._parse_frontmatter(content)

        # Then: it is treated as no frontmatter
        assert fm == {}
        assert body == content


# ---------------------------------------------------------------------------
# _convert — claude-code
# ---------------------------------------------------------------------------


class TestConvertClaudeCode:
    @pytest.mark.parametrize(
        "fm, expected_frontmatter",
        [
            (
                {"trigger": "glob", "patterns": ["**/*.py", "pyproject.toml"], "description": "desc"},
                "---\npaths:\n  - **/*.py\n  - pyproject.toml\n---",
            ),
            (
                {"trigger": "model_decision", "patterns": ["**/*.py"]},
                None,
            ),
            (
                {"trigger": "manual", "patterns": ["**/*.py"]},
                None,
            ),
            (
                {"trigger": "always_on"},
                None,
            ),
        ],
        ids=["glob-paths-list", "model_decision-no-frontmatter", "manual-no-frontmatter", "always_on-no-frontmatter"],
    )
    def test_frontmatter_output(self, tmp_path, fm, expected_frontmatter):
        # Given: universal frontmatter
        mgr = _manager(tmp_path)

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, fm, "body", "universal/rule.md")

        # Then: output starts with expected frontmatter (or has none)
        if expected_frontmatter is None:
            assert not result.startswith("---")
        else:
            assert result.startswith(expected_frontmatter)

    def test_generated_header_present(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, {}, "body", "universal/rule.md")

        # Then: the AUTO-GENERATED header is present
        assert RulesManager._generated_header("universal/rule.md") in result


# ---------------------------------------------------------------------------
# _convert — windsurf
# ---------------------------------------------------------------------------


class TestConvertWindsurf:
    @pytest.mark.parametrize(
        "fm, expected_frontmatter",
        [
            (
                {"trigger": "glob", "patterns": ["**/*.py", "**/conftest.py"], "description": "Test rule"},
                "---\ntrigger: glob\ndescription: Test rule\nglobs: **/*.py, **/conftest.py\n---",
            ),
            (
                {"trigger": "always_on", "description": "My rule"},
                "---\ntrigger: always_on\ndescription: My rule\nglobs:\n---",
            ),
            (
                {"trigger": "model_decision", "description": "Use when querying"},
                "---\ntrigger: model_decision\ndescription: Use when querying\nglobs:\n---",
            ),
        ],
        ids=["glob-with-patterns", "always_on-empty-globs", "model_decision-empty-globs"],
    )
    def test_frontmatter_output(self, tmp_path, fm, expected_frontmatter):
        # Given: universal frontmatter
        mgr = _manager(tmp_path)

        # When: converted to windsurf
        result = mgr._convert(Provider.WINDSURF, fm, "body", "universal/rule.md")

        # Then: the frontmatter block matches the expected windsurf format exactly
        assert result.startswith(expected_frontmatter)

    def test_generated_header_present(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to windsurf
        result = mgr._convert(Provider.WINDSURF, {}, "body", "universal/rule.md")

        # Then: the AUTO-GENERATED header is present
        assert RulesManager._generated_header("universal/rule.md") in result


# ---------------------------------------------------------------------------
# _convert — copilot-vscode
# ---------------------------------------------------------------------------


class TestConvertCopilotVscode:
    @pytest.mark.parametrize(
        "fm, expected_frontmatter",
        [
            (
                {"trigger": "glob", "patterns": ["**/*.py"]},
                '---\napplyTo: "**/*.py"\n---',
            ),
            (
                # multi-pattern: comma-separated, no space (per GitHub docs)
                {"trigger": "glob", "patterns": ["**/*.py", "**/*.ts"]},
                '---\napplyTo: "**/*.py,**/*.ts"\n---',
            ),
            (
                # name/description are not valid copilot-vscode frontmatter fields — ignored
                {"trigger": "glob", "name": "API", "description": "My desc", "patterns": ["**/*.py"]},
                '---\napplyTo: "**/*.py"\n---',
            ),
            (
                # always_on: catch-all glob per GitHub docs
                {"trigger": "always_on"},
                '---\napplyTo: "**"\n---',
            ),
            (
                # manual: no copilot equivalent, falls back to catch-all
                {"trigger": "manual"},
                '---\napplyTo: "**"\n---',
            ),
        ],
        ids=["glob-single-pattern", "glob-multi-pattern", "glob-ignores-name-description", "always_on-catch-all", "manual-catch-all"],
    )
    def test_frontmatter_output(self, tmp_path, fm, expected_frontmatter):
        # Given: universal frontmatter
        mgr = _manager(tmp_path)

        # When: converted to copilot-vscode
        result = mgr._convert(Provider.COPILOT_VSCODE, fm, "body", "universal/rule.md")

        # Then: the frontmatter block matches the expected copilot-vscode format exactly
        assert result.startswith(expected_frontmatter)

    def test_generated_header_present(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to copilot-vscode
        result = mgr._convert(Provider.COPILOT_VSCODE, {}, "body", "universal/rule.md")

        # Then: the AUTO-GENERATED header is present
        assert RulesManager._generated_header("universal/rule.md") in result


# ---------------------------------------------------------------------------
# _convert — copilot-jetbrains
# ---------------------------------------------------------------------------


class TestConvertCopilotJetbrains:
    @pytest.mark.parametrize(
        "fm, expected_frontmatter",
        [
            (
                {"trigger": "glob", "patterns": ["**/*.py"]},
                '---\napplyTo: "**/*.py"\n---',
            ),
            (
                {"trigger": "glob", "patterns": ["**/*.py", "**/*.ts"]},
                '---\napplyTo: "**/*.py,**/*.ts"\n---',
            ),
            (
                {"trigger": "always_on"},
                '---\napplyTo: "**"\n---',
            ),
            (
                {"trigger": "manual"},
                '---\napplyTo: "**"\n---',
            ),
        ],
        ids=["glob-single-pattern", "glob-multi-pattern", "always_on-catch-all", "manual-catch-all"],
    )
    def test_frontmatter_output(self, tmp_path, fm, expected_frontmatter):
        # Given: universal frontmatter
        mgr = _manager(tmp_path)

        # When: converted to copilot-jetbrains
        result = mgr._convert(Provider.COPILOT_JETBRAINS, fm, "body", "universal/rule.md")

        # Then: frontmatter matches expected copilot format exactly
        assert result.startswith(expected_frontmatter)

    def test_generated_header_present(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to copilot-jetbrains
        result = mgr._convert(Provider.COPILOT_JETBRAINS, {}, "body", "universal/rule.md")

        # Then: AUTO-GENERATED header present
        assert RulesManager._generated_header("universal/rule.md") in result


# ---------------------------------------------------------------------------
# port_rule
# ---------------------------------------------------------------------------


class TestPortRule:
    GLOB_CONTENT = "---\ntrigger: glob\npatterns:\n  - '**/*.py'\n---\nrule body\n"

    def test_writes_output_file(self, tmp_path):
        # Given: a universal rule with glob patterns
        src = _make_universal(tmp_path, "my-rule.md", self.GLOB_CONTENT)
        mgr = _manager(tmp_path)

        # When: ported to claude-code
        mgr.port_rule(src, "claude-code")

        # Then: the output file is written with paths
        out = tmp_path / "rules" / "claude-code" / "my-rule.md"
        assert out.exists()
        assert "paths:" in out.read_text()

    def test_dry_run_does_not_write(self, tmp_path, capsys):
        # Given: a universal rule and dry_run=True
        src = _make_universal(tmp_path, "my-rule.md", self.GLOB_CONTENT)
        mgr = _manager(tmp_path)

        # When: ported with dry_run
        mgr.port_rule(src, "claude-code", dry_run=True)

        # Then: no file is written but a preview is printed
        out = tmp_path / "rules" / "claude-code" / "my-rule.md"
        assert not out.exists()
        assert "DRY RUN" in capsys.readouterr().out

    def test_port_to_all_writes_all_providers(self, tmp_path):
        # Given: a universal rule
        src = _make_universal(tmp_path, "my-rule.md", self.GLOB_CONTENT)
        mgr = _manager(tmp_path)

        # When: ported to "all"
        mgr.port_rule(src, "all")

        # Then: an output file exists for every portable provider
        for provider in RulesManager.PORTABLE_PROVIDERS:
            out = tmp_path / "rules" / str(provider) / "my-rule.md"
            assert out.exists(), f"Missing output for {provider}"

    def test_overwrites_existing_silently(self, tmp_path):
        # Given: a rule already ported once
        src = _make_universal(tmp_path, "my-rule.md", self.GLOB_CONTENT)
        mgr = _manager(tmp_path)
        mgr.port_rule(src, "claude-code")

        # When: ported again
        mgr.port_rule(src, "claude-code")

        # Then: the file is overwritten without error
        assert (tmp_path / "rules" / "claude-code" / "my-rule.md").exists()

    def test_no_frontmatter_confirmed(self, tmp_path, mocker):
        # Given: a rule with no frontmatter and user confirms
        src = _make_universal(tmp_path, "plain.md", "just markdown\n")
        mocker.patch(
            "scripts.rules.questionary.confirm", return_value=mocker.Mock(ask=lambda: True)
        )
        mgr = _manager(tmp_path)

        # When: ported
        mgr.port_rule(src, "claude-code")

        # Then: the file is written as always-on
        assert (tmp_path / "rules" / "claude-code" / "plain.md").exists()

    def test_no_frontmatter_declined(self, tmp_path, mocker):
        # Given: a rule with no frontmatter and user declines
        src = _make_universal(tmp_path, "plain.md", "just markdown\n")
        mocker.patch(
            "scripts.rules.questionary.confirm", return_value=mocker.Mock(ask=lambda: False)
        )
        mgr = _manager(tmp_path)

        # When: ported
        mgr.port_rule(src, "claude-code")

        # Then: no file is written
        assert not (tmp_path / "rules" / "claude-code" / "plain.md").exists()


# ---------------------------------------------------------------------------
# port_directory
# ---------------------------------------------------------------------------


class TestPortDirectory:
    def test_ports_all_files_in_dir(self, tmp_path):
        # Given: a directory with two universal rules
        for name in ("a.md", "b.md"):
            _make_universal(
                tmp_path,
                name,
                "---\ntrigger: glob\npatterns:\n  - '**/*.py'\n---\nbody\n",
            )
        mgr = _manager(tmp_path)

        # When: the directory is ported to windsurf
        mgr.port_directory(tmp_path / "rules" / "universal", "windsurf")

        # Then: both files exist in the windsurf directory
        for name in ("a.md", "b.md"):
            assert (tmp_path / "rules" / "windsurf" / name).exists()

    def test_empty_directory_prints_error(self, tmp_path, capsys):
        # Given: an empty universal directory
        empty = tmp_path / "rules" / "universal"
        empty.mkdir(parents=True)
        mgr = _manager(tmp_path)

        # When: port_directory is called
        mgr.port_directory(empty, "windsurf")

        # Then: an error is printed to stderr
        assert "No .md files" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# get_available_sources
# ---------------------------------------------------------------------------


class TestGetAvailableSources:
    def test_returns_sorted_paths(self, tmp_path):
        # Given: two rules added in reverse alphabetical order
        for name in ("z.md", "a.md"):
            _make_universal(tmp_path, name, "body")
        mgr = _manager(tmp_path)

        # When: sources are retrieved
        sources = mgr.get_available_sources()

        # Then: they are returned in sorted order
        names = [p.name for p in sources]
        assert names == sorted(names)

    def test_empty_when_no_universal_dir(self, tmp_path):
        # Given: no universal/ directory exists
        mgr = _manager(tmp_path)

        # When: sources are retrieved

        # Then: an empty list is returned
        assert mgr.get_available_sources() == []
