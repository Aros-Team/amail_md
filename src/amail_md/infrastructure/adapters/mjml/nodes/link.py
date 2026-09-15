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

"""Link MJML node: renders Link EmailStructure to ``<mj-text>``."""

from amail_md.core.models.email_structure.link import Link

from ..registry import register_node


@register_node(Link)
def render_link(element: Link) -> str:
    """
    Render a Link to an MJML ``<mj-text>`` element.

    Args:
        element: The Link EmailStructure to render.

    Returns:
        An MJML string ``<mj-text><a href="...">text</a></mj-text>``.

    """
    return f'<mj-text><a href="{element.href}">{element.text}</a></mj-text>'
