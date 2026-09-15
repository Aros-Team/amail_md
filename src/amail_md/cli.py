# Copyright 2026 Aros Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
CLI entry point for amail-md.

Supports ``lint`` and ``render`` subcommands. Can read from files or stdin.
"""

from __future__ import annotations

import argparse
import sys


def _read_input(file_arg: str) -> str:
    """
    Read markdown from a file or stdin.

    Args:
        file_arg: File path, or ``-`` for stdin.

    Returns:
        The markdown content as a string.

    Raises:
        SystemExit: If the file does not exist.

    """
    if file_arg == "-":
        return sys.stdin.read()

    from pathlib import Path

    path = Path(file_arg)
    if not path.exists():
        print(f"Error: file not found: {file_arg}", file=sys.stderr)
        sys.exit(2)

    return path.read_text(encoding="utf-8")


def cmd_lint(args: argparse.Namespace) -> None:
    """
    Run the linter on markdown input.

    Args:
        args: Parsed CLI arguments with ``file`` attribute.

    """
    from amail_md import verify_markdown

    source = _read_input(args.file)
    errors = verify_markdown(source)

    if not errors:
        print("\u2713 no errors found")
        sys.exit(0)

    print(f"\u2717 {len(errors)} error(s) found\n")
    for err in errors:
        print(f"  Line {err.line}: [{err.code}] {err.message}")
        print(f"    \u2192 {err.suggestion}\n")

    sys.exit(1)


def cmd_render(args: argparse.Namespace) -> None:
    """
    Render markdown to email HTML.

    Args:
        args: Parsed CLI arguments with ``file``, ``output``, ``text``, ``html``.

    """
    from amail_md import markdown_to_email

    source = _read_input(args.file)
    result = markdown_to_email(source)

    output = result["text"] if args.text else result["html"]

    if args.output:
        from pathlib import Path

        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


def main() -> None:
    """Parse arguments and dispatch to the appropriate subcommand."""
    parser = argparse.ArgumentParser(
        prog="amail-md",
        description="Markdown to email HTML converter",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # lint subcommand
    lint_parser = subparsers.add_parser("lint", help="Validate markdown email template")
    lint_parser.add_argument("file", help="Markdown file (or - for stdin)")
    lint_parser.set_defaults(func=cmd_lint)

    # render subcommand
    render_parser = subparsers.add_parser("render", help="Convert markdown to HTML")
    render_parser.add_argument("file", help="Markdown file (or - for stdin)")
    render_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    render_parser.add_argument(
        "--text", action="store_true", help="Output text/plain only"
    )
    render_parser.add_argument("--html", action="store_true", help="Output HTML only")
    render_parser.set_defaults(func=cmd_render)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
