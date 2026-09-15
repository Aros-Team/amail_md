"""
Tests for Code builder.

These tests verify that GenericToken → Code conversion works correctly.
They should FAIL until the builder is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.ports.generic_token import GenericToken
from amail_md.core.services.segmenter.builders.code import build_code


class TestCodeBuilder:
    """Tests for build_code function."""

    def test_build_code_returns_code_instance(self) -> None:
        """build_code must return a Code instance."""
        from amail_md.email_structure import Code

        token = GenericToken(type="fence", content="print('hello')")
        result = build_code(token)
        assert isinstance(result, Code)

    def test_build_code_extracts_code(self) -> None:
        """build_code must extract code from token content."""
        token = GenericToken(type="fence", content="print('hello')")
        result = build_code(token)
        assert result.code == "print('hello')"

    def test_build_code_extracts_language(self) -> None:
        """build_code must extract language from token info."""
        token = GenericToken(type="fence", content="x = 1", info="python")
        result = build_code(token)
        assert result.language == "python"

    def test_build_code_language_defaults_to_none(self) -> None:
        """build_code must default language to None."""
        token = GenericToken(type="fence", content="x = 1")
        result = build_code(token)
        assert result.language is None

    def test_build_code_preserves_content(self) -> None:
        """build_code must preserve code content as-is."""
        code = "def foo():\n    return 42"
        token = GenericToken(type="fence", content=code)
        result = build_code(token)
        assert result.code == code


class TestCodeBuilderRegistry:
    """Tests that build_code is registered in BUILDER_REGISTRY."""

    def test_code_builder_is_registered(self) -> None:
        """Fence builder must be registered in BUILDER_REGISTRY."""
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert "fence" in BUILDER_REGISTRY

    def test_registered_builder_is_build_code(self) -> None:
        """Registered fence builder must be build_code."""
        from amail_md.core.services.segmenter.builders.code import build_code
        from amail_md.core.services.segmenter.registry import BUILDER_REGISTRY

        assert BUILDER_REGISTRY["fence"] is build_code
