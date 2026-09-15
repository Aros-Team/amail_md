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

"""Button MJML node: renders Button EmailStructure to ``<mj-button>``."""

from amail_md.core.models.email_structure.button import Button

from ..registry import register_node


@register_node(Button)
def render_button(element: Button) -> str:
    """
    Render a Button to an MJML ``<mj-button>`` element.

    Args:
        element: The Button EmailStructure to render.

    Returns:
        An MJML string ``<mj-button href="..." ...>text</mj-button>``.

    """
    attrs = [f'href="{element.href}"']

    if element.color:
        attrs.append(f'color="{element.color}"')

    if element.width == "full":
        attrs.append('width="100%"')
    elif element.width:
        attrs.append(f'width="{element.width}"')

    attrs.append(f'border-radius="{element.border_radius}"')

    attrs_str = " ".join(attrs)
    return f"<mj-button {attrs_str}>{element.text}</mj-button>"
