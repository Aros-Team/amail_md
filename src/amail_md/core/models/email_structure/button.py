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

"""Button email structure element."""

from dataclasses import dataclass

from .base import EmailStructure


@dataclass
class Button(EmailStructure):
    """
    Call-to-action button for email.

    Attributes:
        href: Destination URL.
        text: Button text.
        variant: Style variant (primary, secondary, success, danger, warning).
        color: Custom color (hex).
        width: Button width ('full' for 100%).
        border_radius: Border radius CSS value.

    """

    href: str
    text: str
    variant: str = "primary"
    color: str | None = None
    width: str | None = None
    border_radius: str = "8px"
