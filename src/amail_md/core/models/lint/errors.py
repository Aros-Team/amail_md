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

"""ValidationError: detailed lint error with actionable suggestion."""

from dataclasses import dataclass


@dataclass
class ValidationError:
    """
    Detailed validation error with actionable suggestion.

    Attributes:
        line: Line number where the error occurred.
        column: Column number (0 if not applicable).
        code: Error code (e.g. BUTTON_MISSING_HREF).
        message: Human-readable error description.
        suggestion: How to fix the issue.
        severity: Error severity (error, warning, info).

    """

    line: int
    column: int
    code: str
    message: str
    suggestion: str
    severity: str
