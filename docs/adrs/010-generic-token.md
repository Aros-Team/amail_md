# ADR-010: Generic Token for Parser Independence

## Status

Accepted

## Context

We need to define how the segmenter processes AST tokens from the markdown parser. There are two approaches:

1. **Direct coupling** — Builders depend on markdown-it's specific token format
2. **Generic token** — Adapter converts parser-specific tokens to a generic format

## Decision

We will use a **Generic Token** pattern. Each parser adapter converts its specific AST format to a `GenericToken` dataclass that builders consume.

### Structure

```
core/ports/
└── generic_token.py      # GenericToken dataclass

infrastructure/adapters/
└── markdown_parser.py    # Converts markdown-it tokens → GenericToken
```

### GenericToken (core/ports/generic_token.py)

```python
from dataclasses import dataclass, field

@dataclass
class GenericToken:
    """Parser-agnostic token for segmenter consumption."""
    type: str
    content: str = ""
    attrs: dict = field(default_factory=dict)
    children: list["GenericToken"] = field(default_factory=list)
    tag: str = ""
    nesting: int = 0
```

### Adapter Conversion (infrastructure/adapters/markdown_parser.py)

```python
from amail_md.core.ports.generic_token import GenericToken

class MarkdownItParser:
    def parse(self, source: str) -> list[GenericToken]:
        raw_tokens = self.md.parse(source)
        return [self._convert(t) for t in raw_tokens]
    
    def _convert(self, token) -> GenericToken:
        return GenericToken(
            type=token["type"],
            content=token.get("content", ""),
            attrs=dict(token.get("attrs", [])),
            tag=token.get("tag", ""),
            nesting=token.get("nesting", 0),
        )
```

### Builder Consumption

```python
@register_builder("paragraph")
def build_paragraph(token: GenericToken) -> Paragraph:
    return Paragraph(text=token.content)
```

## Consequences

### Positive

- **Parser Independence** — Changing parsers only requires updating the adapter, not builders.
- **Testability** — Builders can be tested with generic tokens, no parser needed.
- **Clarity** — Builders use a simple, consistent interface.

### Negative

- **Conversion overhead** — One extra step to convert tokens.
- **Field mapping** — Must map all needed fields from parser format to generic.
