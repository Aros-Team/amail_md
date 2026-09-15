"""
Tests for Spacer MJML node.

These tests verify that Spacer → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.spacer import Spacer
from amail_md.infrastructure.adapters.mjml.nodes.spacer import render_spacer


class TestSpacerMjmlNode:
    """Tests for render_spacer function."""

    def test_render_spacer_returns_string(self) -> None:
        """render_spacer must return a string."""
        s = Spacer()
        result = render_spacer(s)
        assert isinstance(result, str)

    def test_render_spacer_contains_mj_spacer_tag(self) -> None:
        """render_spacer must produce <mj-spacer> element."""
        s = Spacer()
        result = render_spacer(s)
        assert result.startswith("<mj-spacer")
        assert result.endswith(" />")

    def test_render_spacer_default_height(self) -> None:
        """render_spacer must include default height of 24px."""
        s = Spacer()
        result = render_spacer(s)
        assert 'height="24px"' in result

    def test_render_spacer_custom_height(self) -> None:
        """render_spacer must include custom height."""
        s = Spacer(height="48px")
        result = render_spacer(s)
        assert 'height="48px"' in result


class TestSpacerMjmlNodeRegistry:
    """Tests that render_spacer is registered in RENDER_REGISTRY."""

    def test_spacer_node_is_registered(self) -> None:
        """Spacer must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.spacer import Spacer
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Spacer in RENDER_REGISTRY

    def test_registered_node_is_render_spacer(self) -> None:
        """Registered Spacer renderer must be render_spacer."""
        from amail_md.core.models.email_structure.spacer import Spacer
        from amail_md.infrastructure.adapters.mjml.nodes.spacer import render_spacer
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Spacer] is render_spacer
