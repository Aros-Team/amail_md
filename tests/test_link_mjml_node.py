"""
Tests for Link MJML node.

These tests verify that Link → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.link import Link
from amail_md.infrastructure.adapters.mjml.nodes.link import render_link


class TestLinkMjmlNode:
    """Tests for render_link function."""

    def test_render_link_returns_string(self) -> None:
        """render_link must return a string."""
        link = Link(href="https://example.com", text="Click here")
        result = render_link(link)
        assert isinstance(result, str)

    def test_render_link_contains_mj_text_tag(self) -> None:
        """render_link must produce <mj-text> element."""
        link = Link(href="https://example.com", text="Click here")
        result = render_link(link)
        assert result.startswith("<mj-text>")
        assert result.endswith("</mj-text>")

    def test_render_link_includes_anchor_tag(self) -> None:
        """render_link must include <a> tag."""
        link = Link(href="https://example.com", text="Click here")
        result = render_link(link)
        assert "<a" in result
        assert "</a>" in result

    def test_render_link_includes_href(self) -> None:
        """render_link must include href attribute."""
        link = Link(href="https://example.com", text="Click here")
        result = render_link(link)
        assert 'href="https://example.com"' in result

    def test_render_link_includes_text(self) -> None:
        """render_link must include link text."""
        link = Link(href="https://example.com", text="Click here")
        result = render_link(link)
        assert "Click here" in result


class TestLinkMjmlNodeRegistry:
    """Tests that render_link is registered in RENDER_REGISTRY."""

    def test_link_node_is_registered(self) -> None:
        """Link must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.link import Link
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Link in RENDER_REGISTRY

    def test_registered_node_is_render_link(self) -> None:
        """Registered Link renderer must be render_link."""
        from amail_md.core.models.email_structure.link import Link
        from amail_md.infrastructure.adapters.mjml.nodes.link import render_link
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Link] is render_link
