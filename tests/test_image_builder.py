"""
Tests for Image builder.

These tests verify that GenericToken → Image conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.image import build_image


class TestImageBuilder:
    """Tests for build_image function."""

    def test_build_image_returns_image_instance(self) -> None:
        """build_image must return an Image instance."""
        from amail_md.email_structure import Image

        token = GenericToken(
            type="image", attrs={"src": "https://example.com/photo.jpg"}
        )
        result = build_image(token)
        assert isinstance(result, Image)

    def test_build_image_extracts_src(self) -> None:
        """build_image must extract src from attrs."""
        token = GenericToken(
            type="image", attrs={"src": "https://example.com/photo.jpg"}
        )
        result = build_image(token)
        assert result.src == "https://example.com/photo.jpg"

    def test_build_image_extracts_alt(self) -> None:
        """build_image must extract alt from token content."""
        token = GenericToken(
            type="image",
            content="A photo",
            attrs={"src": "https://example.com/photo.jpg"},
        )
        result = build_image(token)
        assert result.alt == "A photo"

    def test_build_image_alt_defaults_to_empty(self) -> None:
        """build_image must default alt to empty string."""
        token = GenericToken(
            type="image", attrs={"src": "https://example.com/photo.jpg"}
        )
        result = build_image(token)
        assert result.alt == ""

    def test_build_image_extracts_width(self) -> None:
        """build_image must extract width from attrs."""
        token = GenericToken(
            type="image",
            attrs={"src": "https://example.com/photo.jpg", "width": "400"},
        )
        result = build_image(token)
        assert result.width == "400"

    def test_build_image_extracts_height(self) -> None:
        """build_image must extract height from attrs."""
        token = GenericToken(
            type="image",
            attrs={"src": "https://example.com/photo.jpg", "height": "300"},
        )
        result = build_image(token)
        assert result.height == "300"

    def test_build_image_alignment_defaults_to_center(self) -> None:
        """build_image must default alignment to 'center'."""
        token = GenericToken(
            type="image", attrs={"src": "https://example.com/photo.jpg"}
        )
        result = build_image(token)
        assert result.alignment == "center"

    def test_build_image_extracts_border_radius(self) -> None:
        """build_image must extract border-radius from attrs."""
        token = GenericToken(
            type="image",
            attrs={
                "src": "https://example.com/photo.jpg",
                "border-radius": "50%",
            },
        )
        result = build_image(token)
        assert result.border_radius == "50%"


class TestImageBuilderRegistry:
    """Tests that build_image is registered in BUILDER_REGISTRY."""

    def test_image_builder_is_registered(self) -> None:
        """image builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "image" in BUILDER_REGISTRY

    def test_registered_builder_is_build_image(self) -> None:
        """Registered image builder must be build_image."""
        from amail_md.core.services.segmenter.builders.image import build_image
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["image"] is build_image
