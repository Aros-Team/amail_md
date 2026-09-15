"""
Tests for Quote builder.

These tests verify that GenericToken → Quote conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.quote import build_quote


class TestQuoteBuilder:
    """Tests for build_quote function."""

    def test_build_quote_returns_quote_instance(self) -> None:
        """build_quote must return a Quote instance."""
        from amail_md.email_structure import Quote

        token = GenericToken(type="blockquote_open")
        token.children = [
            GenericToken(type="paragraph_open", content="Great quote here")
        ]
        result = build_quote(token)
        assert isinstance(result, Quote)

    def test_build_quote_extracts_text(self) -> None:
        """build_quote must extract text from children tokens."""
        token = GenericToken(type="blockquote_open")
        token.children = [
            GenericToken(type="paragraph_open", content="Great quote here")
        ]
        result = build_quote(token)
        assert result.text == "Great quote here"

    def test_build_quote_empty_text(self) -> None:
        """build_quote must handle empty blockquote."""
        token = GenericToken(type="blockquote_open")
        token.children = []
        result = build_quote(token)
        assert result.text == ""


class TestQuoteBuilderRegistry:
    """Tests that build_quote is registered in BUILDER_REGISTRY."""

    def test_quote_builder_is_registered(self) -> None:
        """blockquote_open builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "blockquote_open" in BUILDER_REGISTRY

    def test_registered_builder_is_build_quote(self) -> None:
        """Registered blockquote_open builder must be build_quote."""
        from amail_md.core.services.segmenter.builders.quote import build_quote
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["blockquote_open"] is build_quote
