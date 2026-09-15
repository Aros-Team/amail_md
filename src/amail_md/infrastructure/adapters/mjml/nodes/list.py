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

"""List MJML node: renders List EmailStructure to ``<mj-text>``."""

from amail_md.core.models.email_structure.list import List

from ..registry import register_node


@register_node(List)
def render_list(element: List) -> str:
    """
    Render a List to an MJML ``<mj-text>`` element.

    Args:
        element: The List EmailStructure to render.

    Returns:
        An MJML string ``<mj-text><ul>...</ul></mj-text>`` or
        ``<mj-text><ol>...</ol></mj-text>``.

    """
    tag = "ol" if element.ordered else "ul"
    items_html = "".join(f"<li>{item}</li>" for item in element.items)
    return f"<mj-text><{tag}>{items_html}</{tag}></mj-text>"
