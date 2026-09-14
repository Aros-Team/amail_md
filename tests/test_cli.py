"""
Tests for amail-md CLI.

These tests define the contract for the CLI module.
They should FAIL until the module is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

import subprocess
import sys


class TestCLILintCommand:
    """Tests for amail-md lint command."""

    def test_lint_valid_file_returns_zero(self) -> None:
        """Lint of valid markdown should exit with code 0."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint", "-"],
            input="# Hello World",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_lint_invalid_file_returns_one(self) -> None:
        """Lint of invalid markdown should exit with code 1."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint", "-"],
            input="[Click](/relative)",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1

    def test_lint_shows_errors(self) -> None:
        """Lint should show error details."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint", "-"],
            input="[Click](/relative)",
            capture_output=True,
            text=True,
        )
        assert (
            "LINK_RELATIVE_URL" in result.stdout or "relative" in result.stdout.lower()
        )

    def test_lint_shows_success_message(self) -> None:
        """Lint should show success message for valid markdown."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint", "-"],
            input="# Hello World",
            capture_output=True,
            text=True,
        )
        assert "no errors" in result.stdout.lower() or "✓" in result.stdout

    def test_lint_nonexistent_file_returns_two(self) -> None:
        """Lint of nonexistent file should exit with code 2."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint", "nonexistent.md"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2

    def test_lint_no_arguments_returns_error(self) -> None:
        """Lint without arguments should show usage."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0


class TestCLIRenderCommand:
    """Tests for amail-md render command."""

    def test_render_valid_file_returns_zero(self) -> None:
        """Render of valid markdown should exit with code 0."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render", "-"],
            input="# Hello World",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_render_produces_html(self) -> None:
        """Render should produce HTML output."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render", "-"],
            input="# Hello World",
            capture_output=True,
            text=True,
        )
        assert "<html" in result.stdout.lower() or "<h1" in result.stdout.lower()

    def test_render_text_flag(self) -> None:
        """Render with --text should produce text/plain only."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render", "-", "--text"],
            input="# Hello World",
            capture_output=True,
            text=True,
        )
        assert "<html" not in result.stdout.lower()

    def test_render_html_flag(self) -> None:
        """Render with --html should produce HTML only."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render", "-", "--html"],
            input="# Hello World",
            capture_output=True,
            text=True,
        )
        assert "<html" in result.stdout.lower() or "<h1" in result.stdout.lower()

    def test_render_output_flag(self) -> None:
        """Render with -o should write to file."""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "amail_md.cli",
                    "render",
                    "-",
                    "-o",
                    output_path,
                ],
                input="# Hello World",
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
            with open(output_path) as f:
                content = f.read()
            assert "<html" in content.lower() or "<h1" in content.lower()
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_nonexistent_file_returns_error(self) -> None:
        """Render of nonexistent file should exit with error."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render", "nonexistent.md"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_render_no_arguments_returns_error(self) -> None:
        """Render without arguments should show usage."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0


class TestCLIHelp:
    """Tests for CLI help output."""

    def test_help_shows_commands(self) -> None:
        """Help should show available commands."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "--help"],
            capture_output=True,
            text=True,
        )
        assert "lint" in result.stdout.lower()
        assert "render" in result.stdout.lower()

    def test_lint_help_shows_options(self) -> None:
        """Lint help should show available options."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "lint", "--help"],
            capture_output=True,
            text=True,
        )
        assert "file" in result.stdout.lower() or "input" in result.stdout.lower()

    def test_render_help_shows_options(self) -> None:
        """Render help should show available options."""
        result = subprocess.run(
            [sys.executable, "-m", "amail_md.cli", "render", "--help"],
            capture_output=True,
            text=True,
        )
        assert "output" in result.stdout.lower() or "-o" in result.stdout
