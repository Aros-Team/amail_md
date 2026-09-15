"""
Tests for Table builder.

These tests verify that GenericToken → Table conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.table import build_table


class TestTableBuilder:
    """Tests for build_table function."""

    def test_build_table_returns_table_instance(self) -> None:
        """build_table must return a Table instance."""
        from amail_md.email_structure import Table

        token = GenericToken(type="table_open")
        token.children = [
            GenericToken(type="thead_open"),
            GenericToken(type="tr_open"),
            GenericToken(type="th_open", content="Name"),
            GenericToken(type="th_close"),
            GenericToken(type="tr_close"),
            GenericToken(type="thead_close"),
            GenericToken(type="tbody_open"),
            GenericToken(type="tr_open"),
            GenericToken(type="td_open", content="Alice"),
            GenericToken(type="td_close"),
            GenericToken(type="tr_close"),
            GenericToken(type="tbody_close"),
        ]
        result = build_table(token)
        assert isinstance(result, Table)

    def test_build_table_extracts_headers(self) -> None:
        """build_table must extract headers from thead tokens."""
        token = GenericToken(type="table_open")
        token.children = [
            GenericToken(type="thead_open"),
            GenericToken(type="tr_open"),
            GenericToken(type="th_open", content="Name"),
            GenericToken(type="th_close"),
            GenericToken(type="tr_close"),
            GenericToken(type="thead_close"),
        ]
        result = build_table(token)
        assert result.headers == ["Name"]

    def test_build_table_extracts_rows(self) -> None:
        """build_table must extract rows from tbody tokens."""
        token = GenericToken(type="table_open")
        token.children = [
            GenericToken(type="thead_open"),
            GenericToken(type="tr_open"),
            GenericToken(type="th_open", content="Name"),
            GenericToken(type="th_close"),
            GenericToken(type="tr_close"),
            GenericToken(type="thead_close"),
            GenericToken(type="tbody_open"),
            GenericToken(type="tr_open"),
            GenericToken(type="td_open", content="Alice"),
            GenericToken(type="td_close"),
            GenericToken(type="tr_close"),
            GenericToken(type="tbody_close"),
        ]
        result = build_table(token)
        assert result.rows == [["Alice"]]

    def test_build_table_empty(self) -> None:
        """build_table must handle empty table."""
        token = GenericToken(type="table_open")
        token.children = []
        result = build_table(token)
        assert result.headers == []
        assert result.rows == []


class TestTableBuilderRegistry:
    """Tests that build_table is registered in BUILDER_REGISTRY."""

    def test_table_builder_is_registered(self) -> None:
        """table_open builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "table_open" in BUILDER_REGISTRY

    def test_registered_builder_is_build_table(self) -> None:
        """Registered table_open builder must be build_table."""
        from amail_md.core.services.segmenter.builders.table import build_table
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["table_open"] is build_table
