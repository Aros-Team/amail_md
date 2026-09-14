# API Reference

!!! note "Work in Progress"
    API reference will be auto-generated once the public functions are
    implemented. For now, see the [Architecture](contributing/architecture.md) page
    for the planned API surface.

---

## Functions

### `markdown_to_email`

```python
def markdown_to_email(source: str, **options: Any) -> RenderResult:
    """Convert Markdown to email-safe HTML.

    Takes a Markdown document with optional YAML frontmatter and returns
    a RenderResult containing email-safe HTML, plain text, metadata,
    and optional warnings.

    Args:
        source: Markdown source with optional YAML frontmatter.
        **options: Configuration overrides (reserved for future use).

    Returns:
        RenderResult with html, text, meta, and optional warnings.

    Raises:
        ParseError: If input contains unparseable Markdown.
        ConfigurationError: If frontmatter is invalid.
        RenderError: If a pipeline stage fails.
        CompilerError: If mrml compilation fails.

    Example:
        ```python
        from amail_md import markdown_to_email

        result = markdown_to_email("# Hello\\n\\nWorld")
        print(result.html)  # email-safe HTML
        print(result.text)  # text/plain fallback
        ```
    """
```

### `verify_markdown`

```python
def verify_markdown(source: str) -> list[ValidationError]:
    """Validate Markdown and return detailed errors with suggestions.

    Parses the Markdown, builds the Email Structure, and runs validation
    rules. Returns a list of ValidationError objects with line numbers,
    error codes, and actionable suggestions.

    Args:
        source: Markdown source with optional YAML frontmatter.

    Returns:
        List of ValidationError (empty if valid).

    Example:
        ```python
        from amail_md import verify_markdown

        errors = verify_markdown("# Hello\\n\\n[Click](/relative)")
        for e in errors:
            print(f"Line {e.line}: {e.message}")
            print(f"  → {e.suggestion}")
        ```
    """
```

---

## Data Classes

### `ValidationError`

```python
@dataclass(frozen=True)
class ValidationError:
    """Detailed validation error with actionable suggestion.

    Attributes:
        line: Line number where the error occurred.
        column: Column number (0 if not applicable).
        code: Error code (e.g., BUTTON_MISSING_HREF).
        message: Human-readable error description.
        suggestion: How to fix the issue.
        severity: Error severity (error, warning, info).
    """
    line: int
    column: int
    code: str
    message: str
    suggestion: str
    severity: str  # "error" | "warning" | "info"
```

### `RenderResult`

```python
@dataclass(frozen=True)
class RenderResult:
    """Final output from the render pipeline.

    Attributes:
        html: Email-safe HTML (responsive, inline styles).
        text: text/plain fallback for email clients.
        meta: Extracted metadata (subject, preheader, etc.).
        warnings: Optional conversion warnings.
    """
    html: str
    text: str
    meta: dict[str, str]
    warnings: list[str] | None = None
```

### `Frontmatter`

```python
@dataclass(frozen=True)
class Frontmatter:
    """Configuration parsed from YAML frontmatter.

    Attributes:
        subject: Email subject line.
        preheader: Preview text shown in inbox.
        theme: Visual theme configuration.
    """
    subject: str | None = None
    preheader: str | None = None
    theme: Theme | None = None
```

### `Theme`

```python
@dataclass(frozen=True)
class Theme:
    """Visual theme with 22 properties for email styling.

    Categories:
        - Colors: primary, secondary, background, text, link, button_text, border
        - Typography: font_family, heading_font, font_size, line_height
        - Layout: content_width, padding, button_radius, button_style
        - Dark mode: dark_background, dark_text, dark_primary, dark_secondary
    """
    # Colors
    primary_color: str = "#007bff"
    secondary_color: str = "#6c757d"
    background_color: str = "#ffffff"
    text_color: str = "#333333"
    link_color: str = "#007bff"
    button_text_color: str = "#ffffff"
    border_color: str = "#dee2e6"

    # Typography
    font_family: str = "Arial, sans-serif"
    heading_font: str | None = None
    font_size: str = "16px"
    line_height: str = "1.5"

    # Layout
    content_width: str = "600px"
    padding: str = "20px"
    button_radius: str = "8px"
    button_style: str = "primary"

    # Dark mode
    dark_background: str = "#1a1a1a"
    dark_text: str = "#ffffff"
    dark_primary: str = "#3399ff"
    dark_secondary: str = "#999999"
```

---

## Email Structure Types

### Base

```python
from abc import ABC

class EmailStructure(ABC):
    """Abstract base for all email structure elements.

    Every email piece (paragraph, heading, button, etc.) inherits from
    this class. The segmenter produces EmailStructure instances from
    the markdown-it-py AST.
    """
```

### `Paragraph`

```python
@dataclass
class Paragraph(EmailStructure):
    """Plain text block. Fallback when no specific element matches.

    Attributes:
        text: Content of the paragraph (supports inline Markdown).
    """
    text: str
```

### `Heading`

```python
@dataclass
class Heading(EmailStructure):
    """Section heading (h1-h6).

    Attributes:
        level: Heading level (1-6).
        text: Heading text.
    """
    level: int
    text: str
```

### `Button`

```python
@dataclass
class Button(EmailStructure):
    """Call-to-action button.

    Attributes:
        href: Destination URL.
        text: Button text.
        variant: Style variant (primary, secondary, success, danger, warning).
        color: Custom color (hex).
        width: Button width ("full" for 100%).
        border_radius: Border radius CSS value.
    """
    href: str
    text: str
    variant: str = "primary"
    color: str | None = None
    width: str | None = None
    border_radius: str = "8px"
```

### `List`

```python
@dataclass
class List(EmailStructure):
    """Ordered or unordered list.

    Attributes:
        items: List of text items.
        ordered: True if ordered list (1, 2, 3...).
    """
    items: list[str]
    ordered: bool = False
```

### `Quote`

```python
@dataclass
class Quote(EmailStructure):
    """Blockquote for cited content.

    Attributes:
        text: Quote content.
    """
    text: str
```

### `Image`

```python
@dataclass
class Image(EmailStructure):
    """Responsive email image.

    Attributes:
        src: Image URL.
        alt: Alternative text.
        width: Rendered width.
        height: Rendered height.
        alignment: Image alignment (left, center, right).
        border_radius: Border radius CSS value.
    """
    src: str
    alt: str = ""
    width: str | None = None
    height: str | None = None
    alignment: str = "center"
    border_radius: str | None = None
```

### `Divider`

```python
@dataclass
class Divider(EmailStructure):
    """Horizontal rule / separator. No fields."""
```

### `Spacer`

```python
@dataclass
class Spacer(EmailStructure):
    """Vertical spacing element.

    Attributes:
        height: Spacer height (CSS value).
    """
    height: str = "24px"
```

### `Columns`

```python
@dataclass
class Columns(EmailStructure):
    """Multi-column layout container.

    Attributes:
        columns: List of ColumnCell elements.
        gap: Space between columns (CSS value).
    """
    columns: list[ColumnCell]
    gap: str = "16px"
```

### `ColumnCell`

```python
@dataclass
class ColumnCell(EmailStructure):
    """Individual column within a Columns block.

    Attributes:
        children: Elements inside this column.
    """
    children: list[EmailStructure]
```

### `Table`

```python
@dataclass
class Table(EmailStructure):
    """GFM table with column alignment.

    Attributes:
        headers: Column headers.
        rows: Table data rows.
        alignment: Per-column alignment (left, center, right).
    """
    headers: list[str]
    rows: list[list[str]]
    alignment: list[str] | None = None
```

### `Code`

```python
@dataclass
class Code(EmailStructure):
    """Code block with syntax highlighting.

    Attributes:
        code: Code content.
        language: Programming language for highlighting.
    """
    code: str
    language: str | None = None
```

### `Link`

```python
@dataclass
class Link(EmailStructure):
    """Hyperlink.

    Attributes:
        href: Destination URL.
        text: Link text.
    """
    href: str
    text: str
```

---

## Exceptions

```python
class AmailError(Exception):
    """Base exception for all amail-md errors."""

class ParseError(AmailError):
    """Invalid or unrepresentable Markdown input."""

class RenderError(AmailError):
    """Pipeline stage failure (library's fault, not caller's)."""

class ConfigurationError(AmailError):
    """Invalid frontmatter or theme configuration."""

class CompilerError(AmailError):
    """mrml compilation failure."""
```

---

## CLI

```bash
amail-md [input.md] [-o output.html] [--text]
```

| Flag | Description |
|------|-------------|
| `-o`, `--output` | Output file (default: stdout) |
| `--text` | Output text/plain only |

**Examples:**

```bash
# Render to stdout
amail-md input.md

# Write to file
amail-md input.md -o output.html

# Plain text only
amail-md input.md --text

# Pipe from stdin
echo "# Hello" | amail-md
```
