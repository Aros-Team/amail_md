"""
Tests for Quote MJML node.

These tests verify that Quote → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.quote import Quote
from amail_md.infrastructure.adapters.mjml.nodes.quote import render_quote


class TestQuoteMjmlNode:
    """Tests for render_quote function."""

    def test_render_quote_returns_string(self) -> None:
        """render_quote must return a string."""
        q = Quote(text="Great quote")
        result = render_quote(q)
        assert isinstance(result, str)

    def test_render_quote_contains_mj_text_tag(self) -> None:
        """render_quote must produce <mj-text> element."""
        q = Quote(text="Great quote")
        result = render_quote(q)
        assert result.startswith("<mj-text>")
        assert result.endswith("</mj-text>")

    def test_render_quote_includes_blockquote(self) -> None:
        """render_quote must include <blockquote> tag."""
        q = Quote(text="Great quote")
        result = render_quote(q)
        assert "<blockquote>" in result
        assert "</blockquote>" in result

    def test_render_quote_includes_text(self) -> None:
        """render_quote must include quote text."""
        q = Quote(text="The best way to predict the future")
        result = render_quote(q)
        assert "The best way to predict the future" in result


class TestQuoteMjmlNodeRegistry:
    """Tests that render_quote is registered in RENDER_REGISTRY."""

    def test_quote_node_is_registered(self) -> None:
        """Quote must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.quote import Quote
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Quote in RENDER_REGISTRY

    def test_registered_node_is_render_quote(self) -> None:
        """Registered Quote renderer must be render_quote."""
        from amail_md.core.models.email_structure.quote import Quote
        from amail_md.infrastructure.adapters.mjml.nodes.quote import render_quote
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Quote] is render_quote
