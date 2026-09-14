# API Reference

!!! note "Work in Progress"
    API reference will be auto-generated once the public functions are
    implemented. For now, see the [Architecture](contributing/architecture.md) page
    for the planned API surface.

## Planned API

### `markdown_to_email_html`

```python
def markdown_to_email_html(source: str, **options: Any) -> RenderResult:
    """Convert Markdown to email-safe HTML.

    Args:
        source: Markdown source with optional YAML frontmatter.
        **options: Configuration overrides.

    Returns:
        RenderResult with html, text, meta, and optional warnings.

    Raises:
        ParseError: If input contains unparseable Markdown.
        ConfigurationError: If frontmatter is invalid.
    """
```

### `RenderResult`

```python
@dataclass
class RenderResult:
    html: str          # Email-safe HTML
    text: str          # text/plain fallback
    meta: dict         # Extracted metadata
    warnings: list[str]  # Optional conversion warnings
```

### Exceptions

```python
class AmailError(Exception): ...
class ParseError(AmailError): ...
class RenderError(AmailError): ...
class ConfigurationError(AmailError): ...
class CompilerError(AmailError): ...
```
