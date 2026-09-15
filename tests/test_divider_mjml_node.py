"""
Tests for Divider MJML node.

These tests verify that Divider → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.divider import Divider
from amail_md.infrastructure.adapters.mjml.nodes.divider import render_divider


class TestDividerMjmlNode:
    """Tests for render_divider function."""

    def test_render_divider_returns_string(self) -> None:
        """render_divider must return a string."""
        d = Divider()
        result = render_divider(d)
        assert isinstance(result, str)

    def test_render_divider_contains_mj_divider_tag(self) -> None:
        """render_divider must produce <mj-divider> element."""
        d = Divider()
        result = render_divider(d)
        assert result.startswith("<mj-divider")
        assert result.endswith(" />")


class TestDividerMjmlNodeRegistry:
    """Tests that render_divider is registered in RENDER_REGISTRY."""

    def test_divider_node_is_registered(self) -> None:
        """Divider must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.divider import Divider
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Divider in RENDER_REGISTRY

    def test_registered_node_is_render_divider(self) -> None:
        """Registered Divider renderer must be render_divider."""
        from amail_md.core.models.email_structure.divider import Divider
        from amail_md.infrastructure.adapters.mjml.nodes.divider import render_divider
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Divider] is render_divider
