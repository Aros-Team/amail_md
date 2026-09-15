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

"""Spacer MJML node: renders Spacer EmailStructure to ``<mj-spacer>``."""

from amail_md.core.models.email_structure.spacer import Spacer

from ..registry import register_node


@register_node(Spacer)
def render_spacer(element: Spacer) -> str:
    """
    Render a Spacer to an MJML ``<mj-spacer>`` element.

    Args:
        element: The Spacer EmailStructure to render.

    Returns:
        An MJML string ``<mj-spacer height="24px" />``.

    """
    return f'<mj-spacer height="{element.height}" />'
