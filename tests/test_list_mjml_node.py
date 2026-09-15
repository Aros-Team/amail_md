"""
Tests for List MJML node.

These tests verify that List → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.list import List
from amail_md.infrastructure.adapters.mjml.nodes.list import render_list


class TestListMjmlNode:
    """Tests for render_list function."""

    def test_render_list_returns_string(self) -> None:
        """render_list must return a string."""
        lst = List(items=["Item 1", "Item 2"])
        result = render_list(lst)
        assert isinstance(result, str)

    def test_render_list_contains_mj_text_tag(self) -> None:
        """render_list must produce <mj-text> element."""
        lst = List(items=["Item 1"])
        result = render_list(lst)
        assert result.startswith("<mj-text>")
        assert result.endswith("</mj-text>")

    def test_render_unordered_list(self) -> None:
        """render_list must render <ul> for unordered list."""
        lst = List(items=["Item 1", "Item 2"], ordered=False)
        result = render_list(lst)
        assert "<ul>" in result
        assert "</ul>" in result

    def test_render_ordered_list(self) -> None:
        """render_list must render <ol> for ordered list."""
        lst = List(items=["Step 1", "Step 2"], ordered=True)
        result = render_list(lst)
        assert "<ol>" in result
        assert "</ol>" in result

    def test_render_list_includes_items(self) -> None:
        """render_list must include all items."""
        lst = List(items=["Alpha", "Beta", "Gamma"])
        result = render_list(lst)
        assert "Alpha" in result
        assert "Beta" in result
        assert "Gamma" in result

    def test_render_list_empty(self) -> None:
        """render_list must handle empty list."""
        lst = List(items=[])
        result = render_list(lst)
        assert "<mj-text>" in result


class TestListMjmlNodeRegistry:
    """Tests that render_list is registered in RENDER_REGISTRY."""

    def test_list_node_is_registered(self) -> None:
        """List must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.list import List
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert List in RENDER_REGISTRY

    def test_registered_node_is_render_list(self) -> None:
        """Registered List renderer must be render_list."""
        from amail_md.core.models.email_structure.list import List
        from amail_md.infrastructure.adapters.mjml.nodes.list import render_list
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[List] is render_list
