"""
Tests for Image MJML node.

These tests verify that Image → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.image import Image
from amail_md.infrastructure.adapters.mjml.nodes.image import render_image


class TestImageMjmlNode:
    """Tests for render_image function."""

    def test_render_image_returns_string(self) -> None:
        """render_image must return a string."""
        img = Image(src="https://example.com/photo.jpg")
        result = render_image(img)
        assert isinstance(result, str)

    def test_render_image_contains_mj_image_tag(self) -> None:
        """render_image must produce <mj-image> element."""
        img = Image(src="https://example.com/photo.jpg")
        result = render_image(img)
        assert result.startswith("<mj-image")
        assert result.endswith(" />")

    def test_render_image_includes_src(self) -> None:
        """render_image must include src attribute."""
        img = Image(src="https://example.com/photo.jpg")
        result = render_image(img)
        assert 'src="https://example.com/photo.jpg"' in result

    def test_render_image_includes_alt(self) -> None:
        """render_image must include alt attribute."""
        img = Image(src="https://example.com/photo.jpg", alt="A photo")
        result = render_image(img)
        assert 'alt="A photo"' in result

    def test_render_image_with_width(self) -> None:
        """render_image must include width when set."""
        img = Image(src="https://example.com/photo.jpg", width="400")
        result = render_image(img)
        assert 'width="400"' in result

    def test_render_image_without_width(self) -> None:
        """render_image must not include width when None."""
        img = Image(src="https://example.com/photo.jpg")
        result = render_image(img)
        assert "width=" not in result

    def test_render_image_with_border_radius(self) -> None:
        """render_image must include border-radius when set."""
        img = Image(src="https://example.com/photo.jpg", border_radius="50%")
        result = render_image(img)
        assert 'border-radius="50%"' in result


class TestImageMjmlNodeRegistry:
    """Tests that render_image is registered in RENDER_REGISTRY."""

    def test_image_node_is_registered(self) -> None:
        """Image must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.image import Image
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Image in RENDER_REGISTRY

    def test_registered_node_is_render_image(self) -> None:
        """Registered Image renderer must be render_image."""
        from amail_md.core.models.email_structure.image import Image
        from amail_md.infrastructure.adapters.mjml.nodes.image import render_image
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Image] is render_image
