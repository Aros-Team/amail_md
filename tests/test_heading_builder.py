"""
Tests for Heading builder.

These tests verify that GenericToken → Heading conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.heading import build_heading


class TestHeadingBuilder:
    """Tests for build_heading function."""

    def test_build_heading_returns_heading_instance(self) -> None:
        """build_heading must return a Heading instance."""
        from amail_md.email_structure import Heading

        token = GenericToken(type="heading_open", content="Title", tag="h1")
        result = build_heading(token)
        assert isinstance(result, Heading)

    def test_build_heading_extracts_text(self) -> None:
        """build_heading must extract text from token content."""
        token = GenericToken(type="heading_open", content="Title", tag="h1")
        result = build_heading(token)
        assert result.text == "Title"

    def test_build_heading_extracts_level_from_tag(self) -> None:
        """build_heading must extract level from tag (h1 → 1, h2 → 2, etc.)."""
        for level in range(1, 7):
            token = GenericToken(
                type="heading_open", content=f"H{level}", tag=f"h{level}"
            )
            result = build_heading(token)
            assert result.level == level

    def test_build_heading_default_level(self) -> None:
        """build_heading must default level to 1 when tag is missing."""
        token = GenericToken(type="heading_open", content="Title")
        result = build_heading(token)
        assert result.level == 1


class TestHeadingBuilderRegistry:
    """Tests that build_heading is registered in BUILDER_REGISTRY."""

    def test_heading_builder_is_registered(self) -> None:
        """heading_open builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "heading_open" in BUILDER_REGISTRY

    def test_registered_builder_is_build_heading(self) -> None:
        """Registered heading_open builder must be build_heading."""
        from amail_md.core.services.segmenter.builders.heading import build_heading
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["heading_open"] is build_heading
