# Getting Started

## Prerequisites

- Python 3.13+

## Installation

```bash
pip install amail-md
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add amail-md
```

## Basic Usage

### From Python

```python
from amail_md import markdown_to_email

result = markdown_to_email("# Hello\n\nWorld")
print(result.html)
```

### From the CLI

```bash
echo "# Hello\n\nWorld" | amail-md
```

### With Theme

```python
from amail_md import markdown_to_email

md = """
---
subject: Monthly Update
theme:
  primary_color: "#e63946"
  font_family: "Helvetica, sans-serif"
---

# Welcome

Your content here.
"""

result = markdown_to_email(md)
```

## What You Get

| Field | Description |
|-------|-------------|
| `result.html` | Email-safe HTML (responsive, inline styles) |
| `result.text` | text/plain fallback |
| `result.meta` | Extracted metadata (subject, preheader…) |
| `result.warnings` | Optional conversion warnings |
