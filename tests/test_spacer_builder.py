"""
Tests for Spacer builder.

These tests verify that GenericToken → Spacer conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.spacer import build_spacer


class TestSpacerBuilder:
    """Tests for build_spacer function."""

    def test_build_spacer_returns_spacer_instance(self) -> None:
        """build_spacer must return a Spacer instance."""
        from amail_md.email_structure import Spacer

        token = GenericToken(type="spacer")
        result = build_spacer(token)
        assert isinstance(result, Spacer)

    def test_build_spacer_height_defaults_to_24px(self) -> None:
        """build_spacer must default height to '24px'."""
        token = GenericToken(type="spacer")
        result = build_spacer(token)
        assert result.height == "24px"

    def test_build_spacer_extracts_height(self) -> None:
        """build_spacer must extract height from attrs."""
        token = GenericToken(type="spacer", attrs={"height": "48px"})
        result = build_spacer(token)
        assert result.height == "48px"


class TestSpacerBuilderRegistry:
    """Tests that build_spacer is registered in BUILDER_REGISTRY."""

    def test_spacer_builder_is_registered(self) -> None:
        """Spacer builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "spacer" in BUILDER_REGISTRY

    def test_registered_builder_is_build_spacer(self) -> None:
        """Registered spacer builder must be build_spacer."""
        from amail_md.core.services.segmenter.builders.spacer import build_spacer
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["spacer"] is build_spacer
