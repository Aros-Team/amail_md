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

"""Rule: relative_urls — checks that URLs are absolute."""

from __future__ import annotations

from typing import Any

from amail_md.core.models.email_structure.button import Button
from amail_md.core.models.lint.errors import ValidationError


def check(elements: list[Any]) -> list[ValidationError]:
    """
    Check that Button elements use absolute URLs.

    Email clients do not resolve relative URLs. All hrefs must start
    with ``http://`` or ``https://``.

    Args:
        elements: List of EmailStructure instances to validate.

    Returns:
        List of ValidationError for buttons with relative URLs.

    """
    errors: list[ValidationError] = []

    for elem in elements:
        if (
            isinstance(elem, Button)
            and elem.href
            and not elem.href.startswith(("http://", "https://"))
        ):
            errors.append(
                ValidationError(
                    line=0,
                    column=0,
                    code="BUTTON_RELATIVE_URL",
                    message=f"Button '{elem.text}' uses relative URL: {elem.href}",
                    suggestion="Use an absolute URL: https://example.com/page",
                    severity="warning",
                )
            )

    return errors
