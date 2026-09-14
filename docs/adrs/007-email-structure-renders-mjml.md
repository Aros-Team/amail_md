# ADR-0007: EmailStructure components render MJML

## Status

Accepted

## Context

We need to define how EmailStructure components (Paragraph, Button, Heading, etc.) are converted to MJML for email rendering. There are two main approaches:

1. **Centralized renderer** — A single renderer service knows how to convert each EmailStructure type to MJML
2. **Distributed rendering** — Each EmailStructure component knows how to render itself to MJML via a `to_mjml(theme)` method

## Decision

We will use **distributed rendering**. Each EmailStructure component implements a `to_mjml(theme: Theme) -> str` method that returns its MJML representation.

```python
class EmailStructure(ABC):
    @abstractmethod
    def to_mjml(self, theme: Theme) -> str: ...

class Paragraph(EmailStructure):
    def to_mjml(self, theme: Theme) -> str:
        return f"<mj-text>{self.text}</mj-text>"

class Button(EmailStructure):
    def to_mjml(self, theme: Theme) -> str:
        return f"<mj-button href='{self.href}'>{self.text}</mj-button>"
```

The `renderer` service assembles the complete MJML document by calling `to_mjml()` on each component, then passes the result to `MjmlCompiler`.

## Consequences

### Positive

- **Open/Closed Principle** — Adding a new EmailStructure type requires only adding a new class with `to_mjml()`. The renderer and compiler remain unchanged.
- **Single Responsibility** — Each component encapsulates its own rendering logic. The renderer only handles assembly and compilation.
- **Testability** — Each component's `to_mjml()` can be tested independently.
- **Encapsulation** — Rendering knowledge lives with the data it operates on.

### Negative

- **Scattered logic** — MJML rendering logic is distributed across multiple files instead of centralized.
- **Theme coupling** — Each component depends on the Theme dataclass for styling.
- **No global optimization** — Cannot easily optimize MJML output across multiple components (e.g., merging adjacent `<mj-text>` elements).
