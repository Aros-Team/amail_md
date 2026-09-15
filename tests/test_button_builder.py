"""
Tests for Button builder.

These tests verify that GenericToken → Button conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.button import build_button


class TestButtonBuilder:
    """Tests for build_button function."""

    def test_build_button_returns_button_instance(self) -> None:
        """build_button must return a Button instance."""
        from amail_md.email_structure import Button

        token = GenericToken(type="link_open", attrs={"href": "https://example.com"})
        result = build_button(token)
        assert isinstance(result, Button)

    def test_build_button_extracts_href(self) -> None:
        """build_button must extract href from attrs."""
        token = GenericToken(type="link_open", attrs={"href": "https://example.com"})
        result = build_button(token)
        assert result.href == "https://example.com"

    def test_build_button_extracts_text(self) -> None:
        """build_button must use token content as text."""
        token = GenericToken(
            type="link_open",
            content="Click me",
            attrs={"href": "https://example.com"},
        )
        result = build_button(token)
        assert result.text == "Click me"

    def test_build_button_default_variant_is_primary(self) -> None:
        """build_button must default variant to 'primary'."""
        token = GenericToken(type="link_open", attrs={"href": "https://example.com"})
        result = build_button(token)
        assert result.variant == "primary"

    def test_build_button_parses_secondary_variant(self) -> None:
        """build_button must parse 'button-secondary' variant from class attr."""
        token = GenericToken(
            type="link_open",
            attrs={"href": "https://example.com", "class": "button-secondary"},
        )
        result = build_button(token)
        assert result.variant == "secondary"

    def test_build_button_parses_success_variant(self) -> None:
        """build_button must parse 'button-success' variant from class attr."""
        token = GenericToken(
            type="link_open",
            attrs={"href": "https://example.com", "class": "button-success"},
        )
        result = build_button(token)
        assert result.variant == "success"

    def test_build_button_parses_color(self) -> None:
        """build_button must extract custom color from attrs."""
        token = GenericToken(
            type="link_open",
            attrs={"href": "https://example.com", "color": "#dc2626"},
        )
        result = build_button(token)
        assert result.color == "#dc2626"

    def test_build_button_color_defaults_to_none(self) -> None:
        """build_button must default color to None."""
        token = GenericToken(type="link_open", attrs={"href": "https://example.com"})
        result = build_button(token)
        assert result.color is None

    def test_build_button_parses_width(self) -> None:
        """build_button must extract width from attrs."""
        token = GenericToken(
            type="link_open",
            attrs={"href": "https://example.com", "width": "full"},
        )
        result = build_button(token)
        assert result.width == "full"

    def test_build_button_parses_border_radius(self) -> None:
        """build_button must extract border-radius from attrs."""
        token = GenericToken(
            type="link_open",
            attrs={"href": "https://example.com", "border-radius": "16px"},
        )
        result = build_button(token)
        assert result.border_radius == "16px"

    def test_build_button_border_radius_default(self) -> None:
        """build_button must default border-radius to '8px'."""
        token = GenericToken(type="link_open", attrs={"href": "https://example.com"})
        result = build_button(token)
        assert result.border_radius == "8px"

    def test_build_button_empty_href(self) -> None:
        """build_button must handle empty href gracefully."""
        token = GenericToken(type="link_open", attrs={})
        result = build_button(token)
        assert result.href == ""


class TestButtonBuilderRegistry:
    """Tests that build_button is registered in BUILDER_REGISTRY."""

    def test_button_builder_is_registered(self) -> None:
        """link_open builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "link_open" in BUILDER_REGISTRY

    def test_registered_builder_is_build_button(self) -> None:
        """Registered link_open builder must be build_button."""
        from amail_md.core.services.segmenter.builders.button import build_button
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["link_open"] is build_button
