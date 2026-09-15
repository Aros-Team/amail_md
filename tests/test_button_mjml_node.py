"""
Tests for Button MJML node.

These tests verify that Button → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.button import Button
from amail_md.infrastructure.adapters.mjml.nodes.button import render_button


class TestButtonMjmlNode:
    """Tests for render_button function."""

    def test_render_button_returns_string(self) -> None:
        """render_button must return a string."""
        btn = Button(href="https://example.com", text="Click")
        result = render_button(btn)
        assert isinstance(result, str)

    def test_render_button_contains_mj_button_tag(self) -> None:
        """render_button must produce <mj-button> element."""
        btn = Button(href="https://example.com", text="Click")
        result = render_button(btn)
        assert result.startswith("<mj-button")
        assert result.endswith("</mj-button>")

    def test_render_button_includes_href(self) -> None:
        """render_button must include href attribute."""
        btn = Button(href="https://example.com", text="Click")
        result = render_button(btn)
        assert 'href="https://example.com"' in result

    def test_render_button_includes_text(self) -> None:
        """render_button must include button text content."""
        btn = Button(href="https://example.com", text="Click me")
        result = render_button(btn)
        assert ">Click me</mj-button>" in result

    def test_render_button_default_border_radius(self) -> None:
        """render_button must include default border-radius of 8px."""
        btn = Button(href="https://example.com", text="Click")
        result = render_button(btn)
        assert 'border-radius="8px"' in result

    def test_render_button_custom_border_radius(self) -> None:
        """render_button must include custom border-radius."""
        btn = Button(href="https://example.com", text="Click", border_radius="16px")
        result = render_button(btn)
        assert 'border-radius="16px"' in result

    def test_render_button_with_color(self) -> None:
        """render_button must include color attribute when set."""
        btn = Button(href="https://example.com", text="Click", color="#dc2626")
        result = render_button(btn)
        assert 'color="#dc2626"' in result

    def test_render_button_without_color(self) -> None:
        """render_button must not include color attribute when None."""
        btn = Button(href="https://example.com", text="Click")
        result = render_button(btn)
        assert "color=" not in result

    def test_render_button_width_full(self) -> None:
        """render_button must convert width='full' to 100%."""
        btn = Button(href="https://example.com", text="Click", width="full")
        result = render_button(btn)
        assert 'width="100%"' in result

    def test_render_button_width_custom(self) -> None:
        """render_button must include custom width."""
        btn = Button(href="https://example.com", text="Click", width="200px")
        result = render_button(btn)
        assert 'width="200px"' in result

    def test_render_button_without_width(self) -> None:
        """render_button must not include width attribute when None."""
        btn = Button(href="https://example.com", text="Click")
        result = render_button(btn)
        assert "width=" not in result


class TestButtonMjmlNodeRegistry:
    """Tests that render_button is registered in RENDER_REGISTRY."""

    def test_button_node_is_registered(self) -> None:
        """Button must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.button import Button
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Button in RENDER_REGISTRY

    def test_registered_node_is_render_button(self) -> None:
        """Registered Button renderer must be render_button."""
        from amail_md.core.models.email_structure.button import Button
        from amail_md.infrastructure.adapters.mjml.nodes.button import render_button
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Button] is render_button
