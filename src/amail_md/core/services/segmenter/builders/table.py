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

"""Table builder: converts GenericToken to Table EmailStructure."""

from amail_md.core.models.email_structure.table import Table
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


def _extract_headers(token: GenericToken) -> list[str]:
    """
    Extract header cells from table token children.

    Walks flat children:
    thead_open -> tr_open -> th_open(content) -> th_close -> tr_close -> thead_close.

    Args:
        token: A GenericToken of type table_open.

    Returns:
        List of header strings.

    """
    headers: list[str] = []
    in_thead = False
    in_row = False
    for child in token.children:
        if child.type == "thead_open":
            in_thead = True
        elif child.type == "thead_close":
            in_thead = False
        elif in_thead:
            if child.type == "tr_open":
                in_row = True
            elif child.type == "tr_close":
                in_row = False
            elif in_row and child.type == "th_open" and child.content:
                headers.append(child.content)
    return headers


def _extract_rows(token: GenericToken) -> list[list[str]]:
    """
    Extract data rows from table token children.

    Walks flat children:
    tbody_open -> tr_open -> td_open(content) -> td_close -> tr_close -> tbody_close.

    Args:
        token: A GenericToken of type table_open.

    Returns:
        List of rows, each row being a list of cell strings.

    """
    rows: list[list[str]] = []
    in_tbody = False
    in_row = False
    current_row: list[str] = []
    for child in token.children:
        if child.type == "tbody_open":
            in_tbody = True
        elif child.type == "tbody_close":
            in_tbody = False
        elif in_tbody:
            if child.type == "tr_open":
                in_row = True
                current_row = []
            elif child.type == "tr_close":
                in_row = False
                rows.append(current_row)
            elif in_row and child.type == "td_open" and child.content:
                current_row.append(child.content)
    return rows


@register_builder("table_open")
def build_table(token: GenericToken) -> Table:
    """
    Build a Table from a table_open token.

    Args:
        token: A GenericToken of type ``table_open``.

    Returns:
        A Table EmailStructure instance.

    """
    return Table(
        headers=_extract_headers(token),
        rows=_extract_rows(token),
    )
