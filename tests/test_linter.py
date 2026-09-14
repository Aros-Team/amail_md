"""
Tests for verify_markdown() linter.

These tests define the contract for the linter module.
They should FAIL until the module is implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""


class TestVerifyMarkdownImport:
    """Tests for verify_markdown import."""

    def test_verify_markdown_can_be_imported(self) -> None:
        """verify_markdown must be importable from amail_md."""
        from amail_md import verify_markdown

        assert callable(verify_markdown)

    def test_verify_markdown_returns_list(self) -> None:
        """verify_markdown must return a list."""
        from amail_md import verify_markdown

        result = verify_markdown("# Hello")
        assert isinstance(result, list)


class TestVerifyMarkdownValid:
    """Tests for valid markdown input."""

    def test_valid_heading_returns_empty(self) -> None:
        """Valid heading should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("# Hello World")
        assert errors == []

    def test_valid_paragraph_returns_empty(self) -> None:
        """Valid paragraph should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("This is a paragraph.")
        assert errors == []

    def test_valid_link_returns_empty(self) -> None:
        """Valid link with absolute URL should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](https://example.com)")
        assert errors == []

    def test_valid_button_returns_empty(self) -> None:
        """Valid button should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown('{{button href="https://example.com" text="Click"}}')
        assert errors == []

    def test_valid_image_returns_empty(self) -> None:
        """Valid image with alt text should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("![Alt text](https://example.com/photo.jpg)")
        assert errors == []

    def test_emptymarkdown_returns_empty(self) -> None:
        """Empty markdown should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("")
        assert errors == []


class TestVerifyMarkdownInvalid:
    """Tests for invalid markdown input."""

    def test_link_relative_url_returns_warning(self) -> None:
        """Link with relative URL should return warning."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) == 1
        assert errors[0].code == "LINK_RELATIVE_URL"
        assert errors[0].severity == "warning"

    def test_button_relative_url_returns_warning(self) -> None:
        """Button with relative URL should return warning."""
        from amail_md import verify_markdown

        errors = verify_markdown('{{button href="/page" text="Click"}}')
        assert len(errors) == 1
        assert errors[0].code == "BUTTON_RELATIVE_URL"
        assert errors[0].severity == "warning"

    def test_image_relative_url_returns_warning(self) -> None:
        """Image with relative URL should return warning."""
        from amail_md import verify_markdown

        errors = verify_markdown("![Alt](/photo.jpg)")
        assert len(errors) == 1
        assert errors[0].code == "IMAGE_RELATIVE_URL"
        assert errors[0].severity == "warning"

    def test_image_missing_alt_returns_warning(self) -> None:
        """Image without alt text should return warning."""
        from amail_md import verify_markdown

        errors = verify_markdown("![](https://example.com/photo.jpg)")
        assert len(errors) == 1
        assert errors[0].code == "IMAGE_MISSING_ALT"
        assert errors[0].severity == "warning"

    def test_multiple_errors_returns_all(self) -> None:
        """Multiple issues should return all errors."""
        from amail_md import verify_markdown

        md = """
[Link1](/page1)
[Link2](/page2)
"""
        errors = verify_markdown(md)
        assert len(errors) == 2
        assert all(e.code == "LINK_RELATIVE_URL" for e in errors)


class TestValidationError:
    """Tests for ValidationError structure."""

    def test_error_has_required_fields(self) -> None:
        """ValidationError must have all required fields."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) > 0
        error = errors[0]
        assert hasattr(error, "line")
        assert hasattr(error, "column")
        assert hasattr(error, "code")
        assert hasattr(error, "message")
        assert hasattr(error, "suggestion")
        assert hasattr(error, "severity")

    def test_error_line_is_positive_int(self) -> None:
        """ValidationError.line must be a positive integer."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) > 0
        assert isinstance(errors[0].line, int)
        assert errors[0].line > 0

    def test_error_severity_is_valid(self) -> None:
        """ValidationError.severity must be error, warning, or info."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) > 0
        assert errors[0].severity in ("error", "warning", "info")

    def test_error_code_is_string(self) -> None:
        """ValidationError.code must be a string."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) > 0
        assert isinstance(errors[0].code, str)

    def test_error_message_is_string(self) -> None:
        """ValidationError.message must be a string."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) > 0
        assert isinstance(errors[0].message, str)

    def test_error_suggestion_is_string(self) -> None:
        """ValidationError.suggestion must be a string."""
        from amail_md import verify_markdown

        errors = verify_markdown("[Click](/page)")
        assert len(errors) > 0
        assert isinstance(errors[0].suggestion, str)


class TestVerifyMarkdownEdgeCases:
    """Tests for edge cases."""

    def test_whitespace_only_returns_empty(self) -> None:
        """Whitespace-only markdown should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("   \n\n   ")
        assert errors == []

    def test_frontmatter_only_returns_empty(self) -> None:
        """Frontmatter-only markdown should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("---\nsubject: Test\n---")
        assert errors == []

    def test_unicode_text_returns_empty(self) -> None:
        """Unicode text should return no errors."""
        from amail_md import verify_markdown

        errors = verify_markdown("# Héllo Wörld 🌍")
        assert errors == []
