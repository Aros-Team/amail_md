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

"""Table MJML node: renders Table EmailStructure to ``<mj-table>``."""

from amail_md.core.models.email_structure.table import Table

from ..registry import register_node


@register_node(Table)
def render_table(element: Table) -> str:
    """
    Render a Table to an MJML ``<mj-table>`` element.

    Args:
        element: The Table EmailStructure to render.

    Returns:
        An MJML string ``<mj-table>...</mj-table>``.

    """
    lines = ["<mj-table>"]

    # Header row
    if element.headers:
        lines.append("  <tr>")
        for i, header in enumerate(element.headers):
            style = ""
            if element.alignment and i < len(element.alignment):
                style = f' style="text-align: {element.alignment[i]}"'
            lines.append(f"    <th{style}>{header}</th>")
        lines.append("  </tr>")

    # Data rows
    for row in element.rows:
        lines.append("  <tr>")
        for i, cell in enumerate(row):
            style = ""
            if element.alignment and i < len(element.alignment):
                style = f' style="text-align: {element.alignment[i]}"'
            lines.append(f"    <td{style}>{cell}</td>")
        lines.append("  </tr>")

    lines.append("</mj-table>")
    return "\n".join(lines)
