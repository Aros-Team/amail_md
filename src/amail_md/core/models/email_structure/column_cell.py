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

"""ColumnCell email structure element."""

from dataclasses import dataclass, field

from .base import EmailStructure


@dataclass
class ColumnCell(EmailStructure):
    """
    A single column inside a Columns layout.

    Attributes:
        children: EmailStructure elements inside this column.
        width: Column width (e.g. ``"50%"``).

    """

    children: list[EmailStructure] = field(default_factory=list)
    width: str | None = None
