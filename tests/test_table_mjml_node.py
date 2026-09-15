"""
Tests for Table MJML node.

These tests verify that Table → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.table import Table
from amail_md.infrastructure.adapters.mjml.nodes.table import render_table


class TestTableMjmlNode:
    """Tests for render_table function."""

    def test_render_table_returns_string(self) -> None:
        """render_table must return a string."""
        t = Table(headers=["Name"], rows=[["Alice"]])
        result = render_table(t)
        assert isinstance(result, str)

    def test_render_table_contains_mj_table_tag(self) -> None:
        """render_table must produce <mj-table> element."""
        t = Table(headers=["Name"], rows=[["Alice"]])
        result = render_table(t)
        assert result.startswith("<mj-table")
        assert result.endswith("</mj-table>")

    def test_render_table_includes_headers(self) -> None:
        """render_table must include header cells."""
        t = Table(headers=["Name", "Role"], rows=[])
        result = render_table(t)
        assert "Name" in result
        assert "Role" in result

    def test_render_table_includes_rows(self) -> None:
        """render_table must include data cells."""
        t = Table(headers=["Name"], rows=[["Alice"], ["Bob"]])
        result = render_table(t)
        assert "Alice" in result
        assert "Bob" in result

    def test_render_table_empty(self) -> None:
        """render_table must handle empty table."""
        t = Table(headers=[], rows=[])
        result = render_table(t)
        assert "<mj-table" in result


class TestTableMjmlNodeRegistry:
    """Tests that render_table is registered in RENDER_REGISTRY."""

    def test_table_node_is_registered(self) -> None:
        """Table must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.table import Table
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Table in RENDER_REGISTRY

    def test_registered_node_is_render_table(self) -> None:
        """Registered Table renderer must be render_table."""
        from amail_md.core.models.email_structure.table import Table
        from amail_md.infrastructure.adapters.mjml.nodes.table import render_table
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Table] is render_table
