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

"""Code MJML node: renders Code EmailStructure to ``<mj-text>``."""

from amail_md.core.models.email_structure.code import Code

from ..registry import register_node


@register_node(Code)
def render_code(element: Code) -> str:
    """
    Render a Code to an MJML ``<mj-text>`` element.

    Args:
        element: The Code EmailStructure to render.

    Returns:
        An MJML string ``<mj-text><pre><code>...</code></pre></mj-text>``.

    """
    lang_attr = f' class="{element.language}"' if element.language else ""
    return (
        f"<mj-text><pre><code{lang_attr}>" f"{element.code}" f"</code></pre></mj-text>"
    )
