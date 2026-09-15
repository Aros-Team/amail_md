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

"""Heading MJML node: renders Heading EmailStructure to ``<mj-text>``."""

from amail_md.core.models.email_structure.heading import Heading

from ..registry import register_node


@register_node(Heading)
def render_heading(element: Heading) -> str:
    """
    Render a Heading to an MJML ``<mj-text>`` element.

    Args:
        element: The Heading EmailStructure to render.

    Returns:
        An MJML string ``<mj-text><hN>text</hN></mj-text>``.

    """
    tag = f"h{element.level}"
    return f"<mj-text><{tag}>{element.text}</{tag}></mj-text>"
