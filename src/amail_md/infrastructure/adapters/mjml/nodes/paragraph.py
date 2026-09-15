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

"""Paragraph MJML node: renders Paragraph EmailStructure to ``<mj-text>``."""

from amail_md.core.models.email_structure.paragraph import Paragraph

from ..registry import register_node


@register_node(Paragraph)
def render_paragraph(element: Paragraph) -> str:
    """
    Render a Paragraph to an MJML ``<mj-text>`` element.

    Args:
        element: The Paragraph EmailStructure to render.

    Returns:
        An MJML string ``<mj-text><p>text</p></mj-text>``.

    """
    return f"<mj-text><p>{element.text}</p></mj-text>"
