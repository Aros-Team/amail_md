"""
Tests for Code MJML node.

These tests verify that Code → MJML conversion works correctly.
They should FAIL until the renderer is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

from amail_md.core.models.email_structure.code import Code
from amail_md.infrastructure.adapters.mjml.nodes.code import render_code


class TestCodeMjmlNode:
    """Tests for render_code function."""

    def test_render_code_returns_string(self) -> None:
        """render_code must return a string."""
        c = Code(code="print('hello')")
        result = render_code(c)
        assert isinstance(result, str)

    def test_render_code_contains_mj_text_tag(self) -> None:
        """render_code must produce <mj-text> element."""
        c = Code(code="print('hello')")
        result = render_code(c)
        assert result.startswith("<mj-text>")
        assert result.endswith("</mj-text>")

    def test_render_code_includes_pre_tag(self) -> None:
        """render_code must include <pre> tag."""
        c = Code(code="print('hello')")
        result = render_code(c)
        assert "<pre>" in result
        assert "</pre>" in result

    def test_render_code_includes_code_tag(self) -> None:
        """render_code must include <code> tag."""
        c = Code(code="print('hello')")
        result = render_code(c)
        assert "<code>" in result
        assert "</code>" in result

    def test_render_code_includes_content(self) -> None:
        """render_code must include code content."""
        c = Code(code="x = 42")
        result = render_code(c)
        assert "x = 42" in result

    def test_render_code_with_language(self) -> None:
        """render_code must include language class when set."""
        c = Code(code="x = 1", language="python")
        result = render_code(c)
        assert "python" in result


class TestCodeMjmlNodeRegistry:
    """Tests that render_code is registered in RENDER_REGISTRY."""

    def test_code_node_is_registered(self) -> None:
        """Code must be registered in RENDER_REGISTRY."""
        from amail_md.core.models.email_structure.code import Code
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert Code in RENDER_REGISTRY

    def test_registered_node_is_render_code(self) -> None:
        """Registered Code renderer must be render_code."""
        from amail_md.core.models.email_structure.code import Code
        from amail_md.infrastructure.adapters.mjml.nodes.code import render_code
        from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

        assert RENDER_REGISTRY[Code] is render_code
