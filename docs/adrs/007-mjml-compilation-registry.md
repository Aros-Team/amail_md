# ADR-007: MJML Compilation via Registry Pattern

## Status

Accepted (supersedes previous "distributed rendering" approach)

## Context

We need to define how EmailStructure components (Paragraph, Button, Heading, etc.) are converted to MJML for email rendering. There are three main approaches:

1. **Centralized renderer** — A single renderer service knows how to convert each EmailStructure type to MJML
2. **Distributed rendering** — Each EmailStructure component knows how to render itself to MJML via a `to_mjml(theme)` method
3. **Registry pattern** — MJML rendering logic lives in the infrastructure adapter, with each component registering its own renderer

## Decision

We will use the **Registry pattern**. EmailStructure models remain pure data classes with no MJML knowledge. MJML rendering logic lives in `infrastructure/adapters/mjml/nodes/`, with each node file registering its renderer via a `@register_node` decorator.

### Structure

```
infrastructure/adapters/mjml/
├── __init__.py           # Exposes the compiler
├── compiler.py           # The compiler class (NEVER MODIFIED)
├── registry.py           # Registry dict mapping Model -> Renderer
└── nodes/                # One file per EmailStructure model
    ├── __init__.py       # Auto-discovers node files
    ├── button.py
    └── paragraph.py
```

### Registry (registry.py)

```python
from collections.abc import Callable
from typing import Any

RENDER_REGISTRY: dict[type, Callable[[Any], str]] = {}

RendererFunc = Callable[[Any], str]
DecoratorType = Callable[[RendererFunc], RendererFunc]


def register_node(model_class: type) -> DecoratorType:
    """Register a render function for an EmailStructure type."""
    def decorator(func: RendererFunc) -> RendererFunc:
        RENDER_REGISTRY[model_class] = func
        return func
    return decorator
```

### Node Example (nodes/button.py)

```python
from amail_md.core.models.email_structure import Button
from ..registry import register_node

@register_node(Button)
def render_button(element: Button) -> str:
    return f'<mj-button href="{element.href}">{element.text}</mj-button>'
```

### Compiler (compiler.py)

```python
import mrml
from .registry import RENDER_REGISTRY
from . import nodes  # Forces decorator execution

class MrmlCompiler:
    def compile(self, elements: list) -> str:
        mjml_lines = ["<mjml><mj-body>"]
        
        for element in elements:
            model_type = type(element)
            
            if model_type not in RENDER_REGISTRY:
                raise NotImplementedError(
                    f"No MJML renderer for {model_type}"
                )
            
            render_func = RENDER_REGISTRY[model_type]
            mjml_lines.append(render_func(element))
            
        mjml_lines.append("</mj-body></mjml>")
        
        return mrml.to_html("".join(mjml_lines))
```

### Auto-discovery (nodes/__init__.py)

```python
import pkgutil
import importlib

for _, module_name, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module_name}")
```

## Consequences

### Positive

- **Open/Closed Principle** — Adding a new EmailStructure type requires only creating a new file in `nodes/`. The compiler and registry remain unchanged.
- **Single Responsibility** — EmailStructure models are pure data. MJML rendering is isolated in the adapter.
- **Technology Decoupling** — The core library has zero MJML knowledge. Swapping to a different template engine means replacing only `infrastructure/adapters/mjml/`.
- **Testability** — Each node's renderer can be tested independently. Models can be tested without any rendering logic.
- **Scalability** — Adding 5 or 500 components never modifies existing files.

### Negative

- **Indirection** — Finding where a component renders requires looking in `nodes/`, not on the model itself.
- **Registration依赖** — If a node file is not imported, its decorator won't execute. Auto-discovery mitigates this.
- **Two-layer abstraction** — The registry adds a layer between the model and its MJML output.
