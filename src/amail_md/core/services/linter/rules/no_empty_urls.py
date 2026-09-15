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

"""Rule: no_empty_urls — checks that URLs are not empty."""

from __future__ import annotations

from typing import Any

from amail_md.core.models.email_structure.button import Button
from amail_md.core.models.lint.errors import ValidationError


def check(elements: list[Any]) -> list[ValidationError]:
    """
    Check that Button elements have non-empty href values.

    Args:
        elements: List of EmailStructure instances to validate.

    Returns:
        List of ValidationError for buttons with empty or missing URLs.

    """
    errors: list[ValidationError] = []

    for elem in elements:
        if isinstance(elem, Button) and (not elem.href or not elem.href.strip()):
            errors.append(
                ValidationError(
                    line=0,
                    column=0,
                    code="BUTTON_MISSING_HREF",
                    message=f"Button '{elem.text}' is missing a URL",
                    suggestion="Add a URL: [text](https://example.com){button}",
                    severity="error",
                )
            )

    return errors
