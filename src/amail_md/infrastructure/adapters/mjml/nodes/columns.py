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

"""Columns MJML node: renders Columns EmailStructure to ``<mj-section>``."""

from amail_md.core.models.email_structure.column_cell import ColumnCell
from amail_md.core.models.email_structure.columns import Columns

from ..registry import register_node


@register_node(Columns)
def render_columns(element: Columns) -> str:
    """
    Render a Columns to an MJML ``<mj-section>`` element.

    Args:
        element: The Columns EmailStructure to render.

    Returns:
        An MJML string ``<mj-section><mj-column>...</mj-column></mj-section>``.

    """
    padding = f' padding="{element.gap}"' if element.gap else ""
    cols_html = "".join(
        f"<mj-column>{_render_cell(c)}</mj-column>" for c in element.columns
    )
    return f"<mj-section{padding}>{cols_html}</mj-section>"


def _render_cell(cell: ColumnCell) -> str:
    """
    Render a ColumnCell's children to MJML content.

    Args:
        cell: The ColumnCell to render.

    Returns:
        MJML content string.

    """
    # For now, render children as mj-text elements
    parts: list[str] = []
    for child in cell.children:
        parts.append(f"<mj-text>{child}</mj-text>")
    return "".join(parts)
