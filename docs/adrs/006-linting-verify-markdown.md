# ADR 0006 — Linting with verify_markdown()

## Status

Accepted

## Date

2026-09-14

## Context

Users need to validate their Markdown email templates before conversion. The
existing error handling (`ParseError`, `ConfigurationError`) provides minimal
information — it tells *that* something failed, not *what* failed or *how* to
fix it.

We need a linter that provides actionable feedback: line numbers, error codes,
and suggestions.

## Decision

Create a `verify_markdown()` function that validates Markdown and returns
detailed `ValidationError` objects.

### API

```python
from amail_md import verify_markdown

errors = verify_markdown("# Hello\n\n[Click](/relative)")
# errors = [
#     ValidationError(
#         line=3, column=1,
#         code="LINK_RELATIVE_URL",
#         message="Link uses relative URL",
#         suggestion="Use absolute URL: https://example.com/...",
#         severity="warning"
#     )
# ]
```

### ValidationError format

| Field | Type | Description |
|-------|------|-------------|
| `line` | `int` | Line number where the error occurred |
| `column` | `int` | Column number (0 if not applicable) |
| `code` | `str` | Error code (e.g., BUTTON_MISSING_HREF) |
| `message` | `str` | Human-readable error description |
| `suggestion` | `str` | How to fix the issue |
| `severity` | `str` | "error", "warning", or "info" |

### Rule categories

| Category | Examples |
|----------|----------|
| **Syntax** | Missing required fields (BUTTON_MISSING_HREF) |
| **Email compatibility** | Relative URLs (IMAGE_RELATIVE_URL), unsupported elements |
| **Accessibility** | Missing alt text (IMAGE_MISSING_ALT) |
| **Best practices** | Long button text (BUTTON_TEXT_LONG) |

### Implementation

- `verify_markdown()` reuses the existing `segmenter` to build `EmailStructure`
- A `LinterEngine` applies rules to the `EmailStructure`
- Rules are a registry of check functions
- No new dependencies required

## Consequences

- Users get actionable feedback before conversion
- The linter reuses existing infrastructure (segmenter, EmailStructure)
- No new dependencies — the linter is pure Python
- Rules can be extended incrementally
- `verify_markdown()` can be called independently or before `markdown_to_email()`
