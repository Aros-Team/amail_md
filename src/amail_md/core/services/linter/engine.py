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
Linter engine: executes all active lint rules.

See ADR-008 for the design rationale.
"""

from __future__ import annotations

from typing import Any

from amail_md.core.models.lint.errors import ValidationError

from .rules import ACTIVE_RULES


class Linter:
    """
    Execute all active lint rules against EmailStructure elements.

    The engine never changes when new rules are added — rules are
    registered in ``rules/__init__.py`` via ``ACTIVE_RULES``.
    """

    def run(self, elements: list[Any]) -> list[ValidationError]:
        """
        Run all active rules and collect errors.

        Args:
            elements: List of EmailStructure instances to validate.

        Returns:
            List of ValidationError from all rules (may be empty).

        """
        all_errors: list[ValidationError] = []

        for rule in ACTIVE_RULES:
            errors = rule(elements)
            all_errors.extend(errors)

        return all_errors
