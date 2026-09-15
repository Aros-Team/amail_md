"""
Tests for Divider builder.

These tests verify that GenericToken → Divider conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.divider import build_divider


class TestDividerBuilder:
    """Tests for build_divider function."""

    def test_build_divider_returns_divider_instance(self) -> None:
        """build_divider must return a Divider instance."""
        from amail_md.email_structure import Divider

        token = GenericToken(type="hr")
        result = build_divider(token)
        assert isinstance(result, Divider)

    def test_build_divider_no_fields(self) -> None:
        """build_divider must create Divider with no fields."""
        token = GenericToken(type="hr")
        result = build_divider(token)
        assert type(result).__name__ == "Divider"


class TestDividerBuilderRegistry:
    """Tests that build_divider is registered in BUILDER_REGISTRY."""

    def test_divider_builder_is_registered(self) -> None:
        """hr builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "hr" in BUILDER_REGISTRY

    def test_registered_builder_is_build_divider(self) -> None:
        """Registered hr builder must be build_divider."""
        from amail_md.core.services.segmenter.builders.divider import build_divider
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["hr"] is build_divider
