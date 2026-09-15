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

"""List builder: converts GenericToken to List EmailStructure."""

from amail_md.core.models.email_structure.list import List
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


def _extract_items(token: GenericToken) -> list[str]:
    """
    Extract text items from list token children.

    Walks children looking for paragraph_open tokens that follow
    list_item_open tokens, collecting their content.

    Args:
        token: A GenericToken of type bullet_list_open or ordered_list_open.

    Returns:
        List of text items.

    """
    items: list[str] = []
    in_item = False
    for child in token.children:
        if child.type == "list_item_open":
            in_item = True
        elif child.type == "list_item_close":
            in_item = False
        elif in_item and child.content:
            items.append(child.content)
    return items


def build_list(token: GenericToken) -> List:
    """
    Build a List from a bullet_list_open or ordered_list_open token.

    Args:
        token: A GenericToken of type ``bullet_list_open`` or ``ordered_list_open``.

    Returns:
        A List EmailStructure instance.

    """
    ordered = token.type == "ordered_list_open"
    return List(items=_extract_items(token), ordered=ordered)


@register_builder("bullet_list_open")
def build_bullet_list(token: GenericToken) -> List:
    """Build a List from a bullet_list_open token (registered builder)."""
    return build_list(token)


@register_builder("ordered_list_open")
def build_ordered_list(token: GenericToken) -> List:
    """Build a List from an ordered_list_open token (registered builder)."""
    return build_list(token)
