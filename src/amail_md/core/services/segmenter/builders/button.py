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
Button builder: converts GenericToken to Button EmailStructure.

Handles the markdown syntax::

    [Click me](https://example.com){.button}
    [Learn More](https://example.com){.button-secondary}
    [Shop Sale](https://example.com){.button color="#dc2626"}

The ``attrs_plugin`` from ``mdit-py-plugins`` injects ``class`` attribute
into the link token's attrs dictionary (e.g. ``class="button"``).
"""

from amail_md.core.models.email_structure.button import Button
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


def _is_button(attrs: dict[str, str]) -> bool:
    """
    Check if attrs indicate a button element.

    The attrs_plugin produces ``class: button`` for ``{.button}`` syntax.

    Args:
        attrs: The attrs dictionary from the GenericToken.

    Returns:
        True if the element is a button.

    """
    css_class = attrs.get("class", "")
    return "button" in css_class.split()


def _parse_variant(attrs: dict[str, str]) -> str:
    """
    Extract the variant from attrs dict.

    The attrs_plugin may produce ``class: button-secondary`` etc.
    The variant is the part after ``button-``.

    Args:
        attrs: The attrs dictionary from the GenericToken.

    Returns:
        The variant name (e.g. 'primary', 'secondary', 'success').

    """
    css_class = attrs.get("class", "")
    for part in css_class.split():
        if part == "button":
            return "primary"
        if part.startswith("button-"):
            return part[7:]
    return "primary"


def _parse_color(attrs: dict[str, str]) -> str | None:
    """
    Extract a custom color from attrs dict.

    The ``color`` attribute may appear as a separate key when the markdown
    uses ``{.button color="#dc2626"}``.

    Args:
        attrs: The attrs dictionary from the GenericToken.

    Returns:
        The hex color string, or None if not specified.

    """
    return attrs.get("color")


@register_builder("link_open")
def build_button(token: GenericToken) -> Button:
    """
    Build a Button from a link_open token.

    Args:
        token: A GenericToken of type ``link_open``.

    Returns:
        A Button EmailStructure instance.

    """
    href = token.attrs.get("href", token.tag)
    text = token.content
    variant = _parse_variant(token.attrs)
    color = _parse_color(token.attrs)
    border_radius = token.attrs.get("border-radius", "8px")
    width = token.attrs.get("width")

    return Button(
        href=href,
        text=text,
        variant=variant,
        color=color,
        width=width,
        border_radius=border_radius,
    )
