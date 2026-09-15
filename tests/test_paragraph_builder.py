"""
Tests for Paragraph builder.

These tests verify that GenericToken → Paragraph conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.paragraph import build_paragraph


class TestParagraphBuilder:
    """Tests for build_paragraph function."""

    def test_build_paragraph_returns_paragraph_instance(self) -> None:
        """build_paragraph must return a Paragraph instance."""
        from amail_md.email_structure import Paragraph

        token = GenericToken(type="paragraph_open", content="Hello world")
        result = build_paragraph(token)
        assert isinstance(result, Paragraph)

    def test_build_paragraph_extracts_text(self) -> None:
        """build_paragraph must extract text from token content."""
        token = GenericToken(type="paragraph_open", content="Hello world")
        result = build_paragraph(token)
        assert result.text == "Hello world"

    def test_build_paragraph_empty_text(self) -> None:
        """build_paragraph must handle empty content."""
        token = GenericToken(type="paragraph_open", content="")
        result = build_paragraph(token)
        assert result.text == ""

    def test_build_paragraph_with_inline_markdown(self) -> None:
        """build_paragraph must preserve inline markdown."""
        token = GenericToken(
            type="paragraph_open", content="**bold** and *italic*"
        )
        result = build_paragraph(token)
        assert result.text == "**bold** and *italic*"


class TestParagraphBuilderRegistry:
    """Tests that build_paragraph is registered in BUILDER_REGISTRY."""

    def test_paragraph_builder_is_registered(self) -> None:
        """paragraph_open builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "paragraph_open" in BUILDER_REGISTRY

    def test_registered_builder_is_build_paragraph(self) -> None:
        """Registered paragraph_open builder must be build_paragraph."""
        from amail_md.core.services.segmenter.builders.paragraph import (
            build_paragraph,
        )
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["paragraph_open"] is build_paragraph
