# ADR-009: Segmenter Registry Pattern

## Status

Accepted

## Context

We need to define how the segmenter converts markdown-it-py AST tokens into EmailStructure objects. There are two main approaches:

1. **Monolithic segmenter** — A single `engine.py` file contains all conversion logic with if/elif chains
2. **Registry pattern** — Each builder is isolated in its own file, discovered automatically

## Decision

We will use the **Registry pattern**. Each builder function converts a specific AST token type to an EmailStructure object, registered via a `@register_builder` decorator. The engine executes all builders without modification.

### Structure

```
core/services/segmenter/
├── __init__.py        # Exposes the Segmenter class
├── engine.py          # The motor with the `while` loop (clean, no giant ifs)
├── registry.py        # BUILDER_REGISTRY dictionary
└── builders/          # One file per Markdown element
    ├── __init__.py    # Auto-discovers builder files
    ├── paragraph.py
    ├── heading.py
    └── button.py
```

### Registry (registry.py)

```python
from typing import Callable, Dict, Type, Any
from amail_md.core.models.email_structure import EmailStructure

BUILDER_REGISTRY: Dict[str, Callable[[Any], EmailStructure]] = {}

def register_builder(token_type: str):
    """Decorator to register a builder for a specific AST token type."""
    def decorator(func: Callable[[Any], EmailStructure]):
        BUILDER_REGISTRY[token_type] = func
        return func
    return decorator
```

### Builder Example (builders/heading.py)

```python
from amail_md.core.models.email_structure import Heading
from ..registry import register_builder

@register_builder("heading_open")
def build_heading(token: dict) -> Heading:
    return Heading(
        text=token["content"],
        level=token["tag"].replace("h", "")
    )
```

### Engine (engine.py)

```python
from .registry import BUILDER_REGISTRY
from . import builders  # Forces decorator execution
from amail_md.core.models.email_structure import EmailStructure

class Segmenter:
    def segment(self, tokens: list) -> list[EmailStructure]:
        elements = []
        
        for token in tokens:
            token_type = token["type"]
            
            if token_type in BUILDER_REGISTRY:
                builder = BUILDER_REGISTRY[token_type]
                element = builder(token)
                elements.append(element)
                
        return elements
```

### Auto-discovery (builders/__init__.py)

```python
import pkgutil
import importlib

for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name != "__init__":
        importlib.import_module(f"{__name__}.{module_name}")
```

## Consequences

### Positive

- **Open/Closed Principle** — Adding a new element type requires only creating a new file in `builders/`. The engine remains unchanged.
- **Single Responsibility** — Each builder encapsulates one conversion concern. The engine only orchestrates.
- **Testability** — Each builder can be tested independently in isolation.
- **Scalability** — 5 or 500 builders never modifies existing files.
- **Maintainability** — Easy to find, understand, and modify individual builders.

### Negative

- **Indirection** — Finding which builders exist requires looking in `builders/`, not a single file.
- **Registration dependency** — Builders must be registered or auto-discovered to execute.
- **Two-layer abstraction** — The engine adds a layer between the caller and builder execution.
