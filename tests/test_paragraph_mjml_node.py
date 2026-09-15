"""
Tests for Paragraph MJML node.

These tests verify that Paragraph → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.paragraph import Paragraph
from amail_md.infrastructure.adapters.mjml.nodes.paragraph import render_paragraph


class TestParagraphMjmlNode:
    """Tests for render_paragraph function."""

    def test_render_paragraph_returns_string(self) -> None:
        """render_paragraph must return a string."""
        p = Paragraph(text="Hello world")
        result = render_paragraph(p)
        assert isinstance(result, str)

    def test_render_paragraph_contains_mj_text_tag(self) -> None:
        """render_paragraph must produce <mj-text> element."""
        p = Paragraph(text="Hello world")
        result = render_paragraph(p)
        assert result.startswith("<mj-text>")
        assert result.endswith("</mj-text>")

    def test_render_paragraph_includes_text(self) -> None:
        """render_paragraph must include paragraph text."""
        p = Paragraph(text="Hello world")
        result = render_paragraph(p)
        assert "Hello world" in result

    def test_render_paragraph_wraps_in_p_tag(self) -> None:
        """render_paragraph must wrap text in <p> tag."""
        p = Paragraph(text="Hello world")
        result = render_paragraph(p)
        assert "<p>Hello world</p>" in result

    def test_render_paragraph_empty_text(self) -> None:
        """render_paragraph must handle empty text."""
        p = Paragraph(text="")
        result = render_paragraph(p)
        assert "<mj-text>" in result


class TestParagraphMjmlNodeRegistry:
    """Tests that render_paragraph is registered in RENDER_REGISTRY."""

    def test_paragraph_node_is_registered(self) -> None:
        """Paragraph must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.paragraph import Paragraph
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Paragraph in RENDER_REGISTRY

    def test_registered_node_is_render_paragraph(self) -> None:
        """Registered Paragraph renderer must be render_paragraph."""
        from amail_md.core.models.email_structure.paragraph import Paragraph
        from amail_md.infrastructure.adapters.mjml.nodes.paragraph import (
            render_paragraph,
        )
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Paragraph] is render_paragraph
