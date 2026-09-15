"""
Tests for Link builder.

These tests verify that GenericToken → Link conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Note: link_open tokens with button class are handled by the Button builder.
This builder handles regular links (no button class).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.link import build_link


class TestLinkBuilder:
    """Tests for build_link function."""

    def test_build_link_returns_link_instance(self) -> None:
        """build_link must return a Link instance."""
        from amail_md.email_structure import Link

        token = GenericToken(
            type="link_open",
            content="Click here",
            attrs={"href": "https://example.com"},
        )
        result = build_link(token)
        assert isinstance(result, Link)

    def test_build_link_extracts_href(self) -> None:
        """build_link must extract href from attrs."""
        token = GenericToken(
            type="link_open",
            content="Click here",
            attrs={"href": "https://example.com"},
        )
        result = build_link(token)
        assert result.href == "https://example.com"

    def test_build_link_extracts_text(self) -> None:
        """build_link must extract text from token content."""
        token = GenericToken(
            type="link_open",
            content="Click here",
            attrs={"href": "https://example.com"},
        )
        result = build_link(token)
        assert result.text == "Click here"

    def test_build_link_empty_href(self) -> None:
        """build_link must handle empty href."""
        token = GenericToken(type="link_open", content="Link", attrs={})
        result = build_link(token)
        assert result.href == ""


class TestLinkBuilderRegistry:
    """Tests that build_link is registered in BUILDER_REGISTRY."""

    def test_link_builder_is_registered(self) -> None:
        """link_open builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "link_open" in BUILDER_REGISTRY

    def test_registered_builder_is_build_link(self) -> None:
        """Registered link_open builder must be build_link."""
        from amail_md.core.services.segmenter.builders.link import build_link
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["link_open"] is build_link
