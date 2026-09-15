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

"""Divider MJML node: renders Divider EmailStructure to ``<mj-divider>``."""

from amail_md.core.models.email_structure.divider import Divider

from ..registry import register_node


@register_node(Divider)
def render_divider(_element: Divider) -> str:
    """
    Render a Divider to an MJML ``<mj-divider>`` element.

    Args:
        _element: The Divider EmailStructure to render (unused).

    Returns:
        An MJML string ``<mj-divider />``.

    """
    return "<mj-divider />"
