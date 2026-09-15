"""
Tests for Columns MJML node.

These tests verify that Columns → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.column_cell import ColumnCell
from amail_md.core.models.email_structure.columns import Columns
from amail_md.infrastructure.adapters.mjml.nodes.columns import render_columns


class TestColumnsMjmlNode:
    """Tests for render_columns function."""

    def test_render_columns_returns_string(self) -> None:
        """render_columns must return a string."""
        c = Columns(columns=[ColumnCell(children=[])])
        result = render_columns(c)
        assert isinstance(result, str)

    def test_render_columns_contains_mj_section(self) -> None:
        """render_columns must produce <mj-section> element."""
        c = Columns(columns=[ColumnCell(children=[])])
        result = render_columns(c)
        assert result.startswith("<mj-section")
        assert result.endswith("</mj-section>")

    def test_render_columns_contains_mj_column(self) -> None:
        """render_columns must include <mj-column> elements."""
        c = Columns(columns=[ColumnCell(children=[]), ColumnCell(children=[])])
        result = render_columns(c)
        assert result.count("<mj-column") == 2

    def test_render_columns_with_gap(self) -> None:
        """render_columns must include padding for gap."""
        c = Columns(columns=[ColumnCell(children=[])], gap="24px")
        result = render_columns(c)
        assert "padding" in result


class TestColumnsMjmlNodeRegistry:
    """Tests that render_columns is registered in RENDER_REGISTRY."""

    def test_columns_node_is_registered(self) -> None:
        """Columns must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.columns import Columns
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Columns in RENDER_REGISTRY

    def test_registered_node_is_render_columns(self) -> None:
        """Registered Columns renderer must be render_columns."""
        from amail_md.core.models.email_structure.columns import Columns
        from amail_md.infrastructure.adapters.mjml.nodes.columns import render_columns
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Columns] is render_columns
