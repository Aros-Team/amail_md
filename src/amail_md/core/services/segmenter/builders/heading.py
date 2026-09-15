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

"""Heading builder: converts GenericToken to Heading EmailStructure."""

from amail_md.core.models.email_structure.heading import Heading
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


def _parse_level(tag: str) -> int:
    """
    Extract heading level from tag name (h1 → 1, h2 → 2, etc.).

    Args:
        tag: HTML tag name (e.g. 'h1', 'h2').

    Returns:
        The heading level (1-6), defaults to 1.

    """
    if tag and tag.startswith("h") and tag[1:].isdigit():
        level = int(tag[1:])
        if 1 <= level <= 6:
            return level
    return 1


@register_builder("heading_open")
def build_heading(token: GenericToken) -> Heading:
    """
    Build a Heading from a heading_open token.

    Args:
        token: A GenericToken of type ``heading_open``.

    Returns:
        A Heading EmailStructure instance.

    """
    level = _parse_level(token.tag)
    return Heading(level=level, text=token.content)
