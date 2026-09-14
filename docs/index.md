# amail-md

Markdown to email-safe HTML. No Node.js. No MJML to write. Just Markdown.

## Install

```bash
pip install amail-md
```

## Quick Start

```python
from amail_md import markdown_to_email_html

md = """
---
subject: Newsletter
---

# Hello World

This is **bold** and this is *italic*.

- Item 1
- Item 2
"""

result = markdown_to_email_html(md)
print(result.html)   # email-safe HTML
print(result.text)   # text/plain fallback
```

## Features

- **Deterministic** — same input, same output, always.
- **Email-first** — inline styles, tables, responsive via MJML.
- **Dual output** — HTML + text/plain in one call.
- **Themeable** — YAML frontmatter + customizable Theme.
- **Safe** — escaped input, no injection.

## Links

- [Getting Started](getting-started.md)
- [API Reference](api-reference.md)
- [Architecture](contributing/architecture.md)
