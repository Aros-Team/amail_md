# ADR-008: Linter Rule Engine Pattern

## Status

Accepted

## Context

We need to define how the linter validates EmailStructure components against email rules. There are two main approaches:

1. **Monolithic linter** — A single `linter.py` file contains all validation logic
2. **Rule Engine pattern** — Each rule is isolated in its own file, discovered automatically

### Registry vs Rule Engine

These are different patterns with different relationship models:

| Pattern | Relationship | Example |
|---------|--------------|---------|
| **Registry** | 1:1 | One model → one renderer/builder |
| **Rule Engine** | 1:N | One engine → executes many rules |

- **Registry** (MJML nodes, Segmenter builders): Each model type maps to exactly one function. `Button → render_button`, `heading_open → build_heading`.
- **Rule Engine** (Linter): One engine executes multiple independent rules. Each rule validates the entire structure and returns errors.

## Decision

We will use the **Rule Engine pattern**. Each lint rule is a standalone function in `core/services/linter/rules/`, registered via a list or auto-discovered. The engine executes all active rules without modification.

### Structure

```
core/services/linter/
├── __init__.py
├── engine.py         # Executes rules (NEVER MODIFIED)
└── rules/            # One file per rule
    ├── __init__.py   # LintRule Protocol + auto-discovery
    ├── no_empty_urls.py
    └── max_one_h1.py
```

### Rule Contract (rules/__init__.py)

```python
from typing import Protocol, List, Any
from amail_md.core.models.lint.errors import LintError

class LintRule(Protocol):
    def check(self, elements: List[Any]) -> List[LintError]:
        ...
```

### Rule Example (rules/no_empty_urls.py)

```python
from amail_md.core.models.email_structure import Button
from amail_md.core.models.lint.errors import LintError

def check(elements: list) -> list[LintError]:
    errors = []
    for elem in elements:
        if isinstance(elem, Button) and not elem.url.startswith("http"):
            errors.append(
                LintError(f"Button '{elem.text}' has invalid URL: {elem.url}")
            )
    return errors
```

### Engine (engine.py)

```python
from .rules import no_empty_urls, max_one_h1
from amail_md.core.models.lint.errors import LintError

ACTIVE_RULES = [
    no_empty_urls.check,
    max_one_h1.check,
]

class Linter:
    def run(self, elements: list) -> list[LintError]:
        all_errors = []
        
        for rule in ACTIVE_RULES:
            errors = rule(elements)
            all_errors.extend(errors)
            
        return all_errors
```

### Auto-discovery (optional alternative)

```python
import pkgutil
import importlib

# Auto-discover all rule files
for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name != "__init__":
        importlib.import_module(f"{__name__}.{module_name}")
```

## Consequences

### Positive

- **Open/Closed Principle** — Adding a new rule requires only creating a new file in `rules/`. The engine remains unchanged.
- **Single Responsibility** — Each rule encapsulates one validation concern. The engine only orchestrates.
- **Testability** — Each rule can be tested independently in isolation.
- **Scalability** — 5 or 500 rules never modifies existing files.
- **Maintainability** — Easy to find, understand, and modify individual rules.

### Negative

- **Indirection** — Finding which rules exist requires looking in `rules/`, not a single file.
- **Registration dependency** — Rules must be registered or auto-discovered to execute.
- **Two-layer abstraction** — The engine adds a layer between the caller and rule execution.
