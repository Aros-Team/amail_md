"""
Tests for Columns builder.

These tests verify that GenericToken → Columns conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.columns import build_columns


class TestColumnsBuilder:
    """Tests for build_columns function."""

    def test_build_columns_returns_columns_instance(self) -> None:
        """build_columns must return a Columns instance."""
        from amail_md.email_structure import Columns

        token = GenericToken(type="columns")
        token.children = [
            GenericToken(type="column"),
            GenericToken(type="column"),
        ]
        result = build_columns(token)
        assert isinstance(result, Columns)

    def test_build_columns_extracts_columns(self) -> None:
        """build_columns must extract columns from children tokens."""
        token = GenericToken(type="columns")
        token.children = [
            GenericToken(type="column"),
            GenericToken(type="column"),
        ]
        result = build_columns(token)
        assert len(result.columns) == 2

    def test_build_columns_gap_defaults_to_16px(self) -> None:
        """build_columns must default gap to '16px'."""
        token = GenericToken(type="columns")
        token.children = []
        result = build_columns(token)
        assert result.gap == "16px"

    def test_build_columns_extracts_gap(self) -> None:
        """build_columns must extract gap from attrs."""
        token = GenericToken(type="columns", attrs={"gap": "24px"})
        token.children = []
        result = build_columns(token)
        assert result.gap == "24px"

    def test_build_columns_empty(self) -> None:
        """build_columns must handle empty columns list."""
        token = GenericToken(type="columns")
        token.children = []
        result = build_columns(token)
        assert result.columns == []


class TestColumnsBuilderRegistry:
    """Tests that build_columns is registered in BUILDER_REGISTRY."""

    def test_columns_builder_is_registered(self) -> None:
        """Columns builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "columns" in BUILDER_REGISTRY

    def test_registered_builder_is_build_columns(self) -> None:
        """Registered columns builder must be build_columns."""
        from amail_md.core.services.segmenter.builders.columns import build_columns
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["columns"] is build_columns
