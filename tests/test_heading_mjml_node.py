"""
Tests for Heading MJML node.

These tests verify that Heading → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.heading import Heading
from amail_md.infrastructure.adapters.mjml.nodes.heading import render_heading


class TestHeadingMjmlNode:
    """Tests for render_heading function."""

    def test_render_heading_returns_string(self) -> None:
        """render_heading must return a string."""
        h = Heading(level=1, text="Title")
        result = render_heading(h)
        assert isinstance(result, str)

    def test_render_heading_contains_mj_text_tag(self) -> None:
        """render_heading must produce <mj-text> element."""
        h = Heading(level=1, text="Title")
        result = render_heading(h)
        assert result.startswith("<mj-text>")
        assert result.endswith("</mj-text>")

    def test_render_heading_level_1(self) -> None:
        """render_heading must render h1 for level 1."""
        h = Heading(level=1, text="Title")
        result = render_heading(h)
        assert "<h1>Title</h1>" in result

    def test_render_heading_level_2(self) -> None:
        """render_heading must render h2 for level 2."""
        h = Heading(level=2, text="Subtitle")
        result = render_heading(h)
        assert "<h2>Subtitle</h2>" in result

    def test_render_heading_level_3(self) -> None:
        """render_heading must render h3 for level 3."""
        h = Heading(level=3, text="Section")
        result = render_heading(h)
        assert "<h3>Section</h3>" in result


class TestHeadingMjmlNodeRegistry:
    """Tests that render_heading is registered in RENDER_REGISTRY."""

    def test_heading_node_is_registered(self) -> None:
        """Heading must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.heading import Heading
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Heading in RENDER_REGISTRY

    def test_registered_node_is_render_heading(self) -> None:
        """Registered Heading renderer must be render_heading."""
        from amail_md.core.models.email_structure.heading import Heading
        from amail_md.infrastructure.adapters.mjml.nodes.heading import render_heading
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Heading] is render_heading
