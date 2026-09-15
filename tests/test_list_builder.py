"""
Tests for List builder.

These tests verify that GenericToken → List conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.list import build_list


class TestListBuilder:
    """Tests for build_list function."""

    def test_build_list_returns_list_instance(self) -> None:
        """build_list must return a List instance."""
        from amail_md.email_structure import List

        token = GenericToken(type="bullet_list_open")
        token.children = [
            GenericToken(type="list_item_open"),
            GenericToken(type="paragraph_open", content="Item 1"),
            GenericToken(type="list_item_close"),
            GenericToken(type="list_item_open"),
            GenericToken(type="paragraph_open", content="Item 2"),
            GenericToken(type="list_item_close"),
        ]
        result = build_list(token)
        assert isinstance(result, List)

    def test_build_list_extracts_items(self) -> None:
        """build_list must extract items from children tokens."""
        token = GenericToken(type="bullet_list_open")
        token.children = [
            GenericToken(type="list_item_open"),
            GenericToken(type="paragraph_open", content="Item 1"),
            GenericToken(type="list_item_close"),
            GenericToken(type="list_item_open"),
            GenericToken(type="paragraph_open", content="Item 2"),
            GenericToken(type="list_item_close"),
        ]
        result = build_list(token)
        assert result.items == ["Item 1", "Item 2"]

    def test_build_list_unordered_by_default(self) -> None:
        """build_list must default ordered to False for bullet_list_open."""
        token = GenericToken(type="bullet_list_open")
        token.children = []
        result = build_list(token)
        assert result.ordered is False

    def test_build_list_ordered(self) -> None:
        """build_list must set ordered to True for ordered_list_open."""
        token = GenericToken(type="ordered_list_open")
        token.children = [
            GenericToken(type="list_item_open"),
            GenericToken(type="paragraph_open", content="Step 1"),
            GenericToken(type="list_item_close"),
        ]
        result = build_list(token)
        assert result.ordered is True

    def test_build_list_empty(self) -> None:
        """build_list must handle empty list."""
        token = GenericToken(type="bullet_list_open")
        token.children = []
        result = build_list(token)
        assert result.items == []


class TestListBuilderRegistry:
    """Tests that build_list is registered in BUILDER_REGISTRY."""

    def test_bullet_list_builder_is_registered(self) -> None:
        """bullet_list_open builder must be registered."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "bullet_list_open" in BUILDER_REGISTRY

    def test_ordered_list_builder_is_registered(self) -> None:
        """ordered_list_open builder must be registered."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "ordered_list_open" in BUILDER_REGISTRY
