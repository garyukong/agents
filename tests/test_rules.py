"""Tests for scripts/rules.py."""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from rules import Provider, RulesManager


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
    def test_glob_trigger_produces_paths_list(self, tmp_path):
        # Given: a rule with trigger: glob and multiple patterns
        mgr = _manager(tmp_path)
        fm = {
            "trigger": "glob",
            "patterns": ["**/*.py", "pyproject.toml"],
            "description": "desc",
        }

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, fm, "body", "universal/rule.md")

        # Then: each pattern appears as a YAML list item under paths:
        assert "paths:" in result
        assert "  - **/*.py" in result
        assert "  - pyproject.toml" in result

    def test_model_decision_no_frontmatter(self, tmp_path):
        # Given: a rule with trigger: model_decision (unsupported mode)
        mgr = _manager(tmp_path)
        fm = {"trigger": "model_decision", "patterns": ["**/*.py"]}

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, fm, "body", "universal/rule.md")

        # Then: no frontmatter is emitted at all
        assert not result.startswith("---")

    def test_manual_no_frontmatter(self, tmp_path):
        # Given: a rule with trigger: manual (unsupported mode)
        mgr = _manager(tmp_path)
        fm = {"trigger": "manual", "patterns": ["**/*.py"]}

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, fm, "body", "universal/rule.md")

        # Then: no frontmatter is emitted at all
        assert not result.startswith("---")

    def test_generated_header_present(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, {}, "body", "universal/rule.md")

        # Then: the AUTO-GENERATED header appears after the closing ---
        assert RulesManager._generated_header("universal/rule.md") in result

    def test_description_not_included(self, tmp_path):
        # Given: a rule with a description field and glob patterns
        mgr = _manager(tmp_path)
        fm = {"trigger": "glob", "patterns": ["**/*.py"], "description": "My desc"}

        # When: converted to claude-code
        result = mgr._convert(Provider.CLAUDE_CODE, fm, "body", "universal/rule.md")

        # Then: description is NOT included (claude-code only supports paths:)
        assert "description" not in result


# ---------------------------------------------------------------------------
# _convert — windsurf
# ---------------------------------------------------------------------------


class TestConvertWindsurf:
    def test_glob_trigger_comma_separated(self, tmp_path):
        # Given: a rule with trigger: glob, patterns, and description
        mgr = _manager(tmp_path)
        fm = {
            "trigger": "glob",
            "patterns": ["**/*.py", "**/conftest.py"],
            "description": "Test rule",
        }

        # When: converted to windsurf
        result = mgr._convert(Provider.WINDSURF, fm, "body", "universal/rule.md")

        # Then: trigger, description, and globs appear with comma-separated patterns
        assert "trigger: glob" in result
        assert "description: Test rule" in result
        assert "globs: **/*.py, **/conftest.py" in result

    def test_always_on_empty_globs(self, tmp_path):
        # Given: a rule with trigger: always_on and description
        mgr = _manager(tmp_path)
        fm = {"trigger": "always_on", "description": "My rule"}

        # When: converted to windsurf
        result = mgr._convert(Provider.WINDSURF, fm, "body", "universal/rule.md")

        # Then: trigger, description, and empty globs are emitted
        assert "trigger: always_on" in result
        assert "description: My rule" in result
        assert "globs:" in result

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
    def test_single_pattern_apply_to(self, tmp_path):
        # Given: a rule with a single glob pattern and a name
        mgr = _manager(tmp_path)
        fm = {"trigger": "glob", "name": "API", "patterns": ["**/*.py"]}

        # When: converted to copilot-vscode
        result = mgr._convert(Provider.COPILOT_VSCODE, fm, "body", "universal/rule.md")

        # Then: applyTo and name are present
        assert 'applyTo: "**/*.py"' in result
        assert "name: API" in result

    def test_multi_pattern_warning(self, tmp_path, capsys):
        # Given: a rule with multiple glob patterns
        mgr = _manager(tmp_path)
        fm = {"trigger": "glob", "patterns": ["**/*.py", "**/*.ts"]}

        # When: converted to copilot-vscode
        mgr._convert(Provider.COPILOT_VSCODE, fm, "body", "universal/rule.md")

        # Then: a warning about the known multi-pattern bug is printed to stderr
        assert "known bug" in capsys.readouterr().err

    def test_manual_trigger_omits_apply_to(self, tmp_path):
        # Given: a rule with trigger: manual (unsupported mode)
        mgr = _manager(tmp_path)
        fm = {"trigger": "manual", "patterns": ["**/*.py"]}

        # When: converted to copilot-vscode
        result = mgr._convert(Provider.COPILOT_VSCODE, fm, "body", "universal/rule.md")

        # Then: applyTo is omitted (always-on)
        assert "applyTo" not in result

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
    def test_no_frontmatter_block(self, tmp_path):
        # Given: a rule with glob patterns
        mgr = _manager(tmp_path)
        fm = {"trigger": "glob", "patterns": ["**/*.py"]}

        # When: converted to copilot-jetbrains
        result = mgr._convert(
            Provider.COPILOT_JETBRAINS, fm, "body text", "universal/rule.md"
        )

        # Then: no YAML frontmatter block is present
        assert not result.startswith("---")

    def test_header_is_first_line(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to copilot-jetbrains
        result = mgr._convert(
            Provider.COPILOT_JETBRAINS, {}, "body text", "universal/rule.md"
        )

        # Then: the AUTO-GENERATED header is the very first line
        assert result.startswith(RulesManager._generated_header("universal/rule.md"))

    def test_body_preserved(self, tmp_path):
        # Given: any frontmatter
        mgr = _manager(tmp_path)

        # When: converted to copilot-jetbrains
        result = mgr._convert(
            Provider.COPILOT_JETBRAINS, {}, "body text", "universal/rule.md"
        )

        # Then: the rule body is preserved in the output
        assert "body text" in result


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
            "rules.questionary.confirm", return_value=mocker.Mock(ask=lambda: True)
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
            "rules.questionary.confirm", return_value=mocker.Mock(ask=lambda: False)
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
