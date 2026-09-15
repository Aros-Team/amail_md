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
amail-md: Markdown to email HTML converter.

Public API:
    - ``verify_markdown(source)`` — validate markdown and return errors.
    - ``markdown_to_email(source)`` — convert markdown to email-safe HTML.
"""

from __future__ import annotations

import re
from typing import Any

from amail_md.core.models.lint.errors import ValidationError


def _is_relative_url(url: str) -> bool:
    """
    Check whether a URL is relative (no scheme).

    Args:
        url: The URL string to check.

    Returns:
        True if the URL does not start with ``http://`` or ``https://``.

    """
    return bool(url) and not url.startswith(("http://", "https://", "mailto:", "tel:"))


def verify_markdown(source: str) -> list[ValidationError]:
    """
    Validate markdown and return detailed errors with suggestions.

    Scans the markdown source for common email pitfalls: relative URLs
    in links, buttons, and images, and missing alt text on images.

    Args:
        source: Markdown source with optional YAML frontmatter.

    Returns:
        List of ValidationError (empty if valid).

    """
    errors: list[ValidationError] = []
    lines = source.splitlines()

    for line_num, line in enumerate(lines, start=1):
        # Links: [text](url) — but NOT images ![alt](url)
        for match in re.finditer(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)", line):
            url = match.group(2)
            if _is_relative_url(url):
                errors.append(
                    ValidationError(
                        line=line_num,
                        column=match.start(),
                        code="LINK_RELATIVE_URL",
                        message=f"Link uses relative URL: {url}",
                        suggestion="Use an absolute URL: https://example.com/page",
                        severity="warning",
                    )
                )

        # Images: ![alt](url)
        for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            alt = match.group(1)
            url = match.group(2)
            if _is_relative_url(url):
                errors.append(
                    ValidationError(
                        line=line_num,
                        column=match.start(),
                        code="IMAGE_RELATIVE_URL",
                        message=f"Image uses relative URL: {url}",
                        suggestion="Use an absolute URL: https://example.com/photo.jpg",
                        severity="warning",
                    )
                )
            if not alt.strip():
                errors.append(
                    ValidationError(
                        line=line_num,
                        column=match.start(),
                        code="IMAGE_MISSING_ALT",
                        message="Image is missing alt text",
                        suggestion="Add description for accessibility",
                        severity="warning",
                    )
                )

        # Buttons: {{button href="url" text="text"}}  or  {{button href='url'}}
        for match in re.finditer(r"\{\{button\s+([^}]*)\}\}", line):
            attrs_str = match.group(1)
            href_match = re.search(r'href="([^"]*)"', attrs_str)
            if href_match:
                url = href_match.group(1)
                if _is_relative_url(url):
                    errors.append(
                        ValidationError(
                            line=line_num,
                            column=match.start(),
                            code="BUTTON_RELATIVE_URL",
                            message=f"Button uses relative URL: {url}",
                            suggestion="Use an absolute URL: https://example.com/page",
                            severity="warning",
                        )
                    )

    return errors


def markdown_to_email(source: str) -> dict[str, Any]:
    """
    Convert markdown to email-safe HTML.

    Takes a markdown document and returns a dict with html, text, meta,
    and optional warnings.

    Args:
        source: Markdown source with optional YAML frontmatter.

    Returns:
        Dict with 'html', 'text', 'meta', and optional 'warnings' keys.

    """
    from amail_md.core.orchestrator import markdown_to_email_parts

    result = markdown_to_email_parts(source)
    return {
        "html": result["html"],
        "text": source,
        "meta": {},
        "warnings": [],
    }


def main() -> None:
    """Run the amail-md command-line tool."""
    from amail_md.cli import main as cli_main

    cli_main()
