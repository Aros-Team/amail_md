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

"""Table email structure element."""

from dataclasses import dataclass, field

from .base import EmailStructure


@dataclass
class Table(EmailStructure):
    """
    GFM table with column alignment.

    Attributes:
        headers: Column headers.
        rows: Table data rows.
        alignment: Per-column alignment (left, center, right).

    """

    headers: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    alignment: list[str] | None = None
