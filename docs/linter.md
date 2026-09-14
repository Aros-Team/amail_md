# Linter

Validate Markdown email templates and get actionable feedback.

---

## Overview

The linter parses your Markdown, builds the Email Structure, and runs validation
rules. It returns a list of `ValidationError` objects with line numbers, error
codes, and suggestions for fixing issues.

```python
from amail_md import verify_markdown

errors = verify_markdown("# Hello\n\n[Click](/relative)")
for e in errors:
    print(f"Line {e.line}: {e.message}")
    print(f"  → {e.suggestion}")
```

---

## API

### `verify_markdown(source: str) -> list[ValidationError]`

Validate Markdown and return detailed errors.

**Args:**
- `source`: Markdown source with optional YAML frontmatter.

**Returns:**
- List of `ValidationError` (empty if valid).

**Example:**
```python
from amail_md import verify_markdown

errors = verify_markdown("""
---
subject: Test
---

# Hello

{{button href="/page" text="Click"}}
""")

# errors = [
#     ValidationError(
#         line=6, column=1,
#         code="BUTTON_RELATIVE_URL",
#         message="Button href uses relative URL",
#         suggestion="Use absolute URL: https://example.com/page",
#         severity="warning"
#     )
# ]
```

---

## ValidationError

```python
@dataclass(frozen=True)
class ValidationError:
    line: int        # Line number where the error occurred
    column: int      # Column number (0 if not applicable)
    code: str        # Error code (e.g., BUTTON_MISSING_HREF)
    message: str     # Human-readable error description
    suggestion: str  # How to fix the issue
    severity: str    # "error" | "warning" | "info"
```

### Severity levels

| Level | Meaning |
|-------|---------|
| `error` | Must fix. The email will not render correctly. |
| `warning` | Should fix. May cause issues in some email clients. |
| `info` | Suggestion. Best practice recommendation. |

---

## Error Codes

### Syntax errors

| Code | Message | Severity |
|------|---------|----------|
| `BUTTON_MISSING_HREF` | Button missing href field | error |
| `BUTTON_MISSING_TEXT` | Button missing text field | error |
| `IMAGE_MISSING_SRC` | Image missing src field | error |
| `HEADING_INVALID_LEVEL` | Heading level must be 1-6 | error |
| `TABLE_EMPTY` | Table has no headers or rows | error |

### Email compatibility

| Code | Message | Severity |
|------|---------|----------|
| `LINK_RELATIVE_URL` | Link uses relative URL | warning |
| `BUTTON_RELATIVE_URL` | Button href uses relative URL | warning |
| `IMAGE_RELATIVE_URL` | Image src uses relative URL | warning |
| `CODE_BLOCK_UNSUPPORTED` | Code blocks not supported in Outlook | info |

### Accessibility

| Code | Message | Severity |
|------|---------|----------|
| `IMAGE_MISSING_ALT` | Image missing alt text | warning |
| `LINK_EMPTY_TEXT` | Link has empty text | warning |

### Best practices

| Code | Message | Severity |
|------|---------|----------|
| `BUTTON_TEXT_LONG` | Button text too long (>25 chars) | info |
| `HEADING_EMPTY` | Heading has empty text | warning |
| `PARAGRAPH_EMPTY` | Paragraph has empty text | info |

---

## Integration with render

`verify_markdown()` is also called internally by `markdown_to_email()`. In this
mode, only `error` severity issues cause failure; `warning` and `info` are
collected in the `warnings` field of `RenderResult`.

```python
from amail_md import markdown_to_email

result = markdown_to_email("# Hello\n\n[Click](/relative)")
# result.warnings = ["Line 3: Link uses relative URL"]
```

---

## Extending rules

Rules are check functions registered in the `LinterEngine`. To add a new rule:

1. Create a check function in `src/amail_md/lint/rules/`
2. Register it in the rule registry
3. Add tests in `tests/test_linter.py`

```python
def check_button_missing_href(elements: list[EmailStructure]) -> list[ValidationError]:
    """Check that all buttons have an href field."""
    errors = []
    for el in elements:
        if isinstance(el, Button) and not el.href:
            errors.append(ValidationError(
                line=getattr(el, '_line', 0),
                column=0,
                code="BUTTON_MISSING_HREF",
                message="Button missing href field",
                suggestion="Add href: {{button href='https://...' text='...'}}",
                severity="error"
            ))
    return errors
```
