# Architecture

> What "good work" means in this project.

---

## 1. Project Overview

amail-md is a Python **library** that converts **Markdown to email-safe HTML**.
It is consumed as a package (`amail_md`) by other code, and it also ships a thin
`amail-md` console entry point for convenience. The core value is a deterministic,
pure-function pipeline: Markdown in → HTML + text/plain out, tuned for email
clients (not web browsers).

Design goals:
- **Deterministic** — the same Markdown always produces the same HTML.
- **Email-first** — output works in limited email renderers (inline styles,
  tables, no external resources).
- **Safe** — escapes user input; no raw HTML injection.
- **Minimal** — small dependency footprint, no state.

Dependencies (see ADR-0001):
- **markdown-it-py** — Markdown → AST parser (Python)
- **mrml** — MJML → email-safe HTML compiler (Rust)

---

## 2. Core Pipeline (pure functions)

The package exposes a small set of **pure functions** (no I/O, no global state).
The canonical entry points:

```python
from amail_md import markdown_to_email, verify_markdown

# Convert to email HTML
result = markdown_to_email(md_text)
# result.html  — email-safe HTML
# result.text  — text/plain fallback
# result.meta  — extracted metadata
# result.warnings?  — optional warnings

# Validate markdown
errors = verify_markdown(md_text)
# errors — list of ValidationError (empty if valid)
```

Pipeline stages (each a pure function that feeds the next):

| Stage | Responsibility |
|-------|---------------|
| **Configuration** | Parse YAML frontmatter, resolve and merge Theme |
| **Parse** | Turn Markdown source into AST via markdown-it-py |
| **Segment** | Walk AST, classify blocks → Email Structure (Paragraph, Button, Heading…) |
| **Wrap** | Wrap Email Structure into MJML (head + body → `<mjml>`) |
| **Compile** | MJML → email-safe HTML via mrml |

The orchestrators (`markdown_to_email()` and `verify_markdown()`) drive this pipeline and collect warnings/errors. Plaintext generation is part of `markdown_to_email()`, not a separate stage.

### Render Pipeline Sequence

<img src="../../diagrams/svg/Sequence_Pipelines.svg" alt="Render Pipeline Sequence Diagram" width="100%">

Rules:
- Functions are **pure**: same input → same output, no hidden state.
- No network, no filesystem, no randomness inside the pipeline.
- Each stage is independently testable.
- Keep stages one-way. No backward dependencies or circular imports.
- **No regex over HTML** — transformations happen on the structured model
  (see ADR-0003).

---

## 3. Layering

```
amail_md/
├── __init__.py           # public API (markdown_to_email, verify_markdown)
├── cli.py                # CLI entry point (typer)
├── exceptions.py         # typed error hierarchy
└── core/
    ├── __init__.py
    ├── orchestrator.py    # drives the pipeline, returns RenderResult
    ├── ports/
    │   ├── __init__.py
    │   ├── markdown_parser.py   # MarkdownParser Protocol
    │   └── mjml_compiler.py     # MjmlCompiler Protocol
    ├── services/
    │   ├── __init__.py
    │   ├── configurer.py  # frontmatter parsing, Theme resolution/merging
    │   ├── segmenter/
    │   │   ├── __init__.py
    │   │   ├── engine.py   # The motor with the `while` loop (clean)
    │   │   ├── registry.py # BUILDER_REGISTRY dictionary
    │   │   └── builders/   # One file per Markdown element
    │   │       ├── __init__.py
    │   │       ├── paragraph.py
    │   │       ├── heading.py
    │   │       └── button.py
    │   ├── renderer.py    # assembles EmailStructure → MJML → HTML
    │   └── linter/
    │       ├── __init__.py
    │       ├── engine.py   # Executes rules (NEVER MODIFIED)
    │       └── rules/      # One file per rule
    │           ├── __init__.py
    │           ├── no_empty_urls.py
    │           └── max_one_h1.py
    └── models/
        ├── email_structure/
        │   ├── __init__.py
        │   ├── paragraph.py
        │   ├── button.py
        │   └── heading.py
        └── lint/
            ├── __init__.py
            └── errors.py
└── infrastructure/
    ├── __init__.py
    └── adapters/
        ├── __init__.py
        ├── markdown_parser.py   # MarkdownItParser (markdown-it-py)
        └── mjml/                # MJML adapter (Registry pattern)
            ├── __init__.py
            ├── compiler.py      # MrmlCompiler (NEVER MODIFIED)
            ├── registry.py      # @register_node decorator
            └── nodes/           # One file per EmailStructure model
                ├── __init__.py  # Auto-discovers node files
                ├── button.py
                └── paragraph.py
```

Architecture pattern: **Ports & Adapters** (hexagonal).

- `ports/` defines Protocol interfaces (MarkdownParser, MjmlCompiler).
- `adapters/` implements them using external libs (markdown-it-py, mrml).
- The core only depends on Ports, never on Adapters directly.

Pattern rules:
- Only `__init__.py` exposes the public API surface; internal modules import
  freely but are not part of the public contract.
- **Public API is stable and tiny** — think carefully before adding to it.
- Internal modules never import from `__init__.py` (avoids circular imports).
- No I/O in the core pipeline; anything that touches disk/network/clock lives
  behind an explicit seam (e.g. the CLI entry point).

### Adding a New EmailStructure Element (3-File Pattern)

Each EmailStructure element requires **3 files**:

| File | Location | Responsibility |
|------|----------|----------------|
| Model | `core/models/email_structure/<element>.py` | Data definition |
| Builder | `core/services/segmenter/builders/<element>.py` | AST → Model |
| MJML Node | `infrastructure/adapters/mjml/nodes/<element>.py` | Model → MJML |

**Why separate?**

- **Single Responsibility** — Model defines data; Builder handles parsing; MJML Node handles rendering.
- **Dependency Inversion** — Core models have zero dependencies on parsers or renderers.
- **Open/Closed** — Adding a new element never modifies existing files.
- **Testability** — Each layer can be tested independently.

Example for Button:

```
1. core/models/email_structure/button.py      → Button(text, url, variant)
2. core/services/segmenter/builders/button.py  → Token + attrs{button} → Button
3. infrastructure/adapters/mjml/nodes/button.py → Button → <mj-button>
```

### Parser Plugins (Adapter Layer)

Plugins are loaded by the `MarkdownItParser` adapter, not by core.

| Plugin | Package | For Element |
|--------|---------|-------------|
| `attrs_plugin` | `mdit-py-plugins` | Button, Image (`{button}`, `{width}`) |
| `container_plugin` | `mdit-py-plugins` | Spacer, Columns, Hero (`::: name`) |
| `front_matter_plugin` | `mdit-py-plugins` | Frontmatter (`---`) |
| `tasklists_plugin` | `mdit-py-plugins` | Task lists (`- [x]`) |

Core never imports these plugins. The adapter loads them to produce the AST tokens that builders expect.

### Parser Independence (Generic Token)

Builders depend on `GenericToken`, not on markdown-it's specific format. Each parser adapter converts its AST to `GenericToken`:

```
markdown-it → MarkdownItParser → GenericToken → Builder
remark      → RemarkParser     → GenericToken → Builder
pandoc      → PandocParser     → GenericToken → Builder
```

This means changing parsers only requires updating the adapter, not builders.

```python
# core/ports/generic_token.py
@dataclass
class GenericToken:
    type: str
    content: str = ""
    attrs: dict = field(default_factory=dict)
    children: list["GenericToken"] = field(default_factory=list)
```

---

## 4. Error Handling Pattern

Use a typed error hierarchy rooted at `amail_md.exceptions.AmailError`.

- `ParseError` — invalid / unrepresentable Markdown input.
- `RenderError` — a stage failure that is the library's fault, not the caller's.
- `ConfigurationError` — invalid frontmatter or theme configuration.
- `CompilerError` — mrml compilation failure.

Boundary rules: the **public API** validates input and raises only typed,
documented exceptions. Callers never see raw library-internal exceptions.

Do **not** swallow exceptions silently — always let typed errors propagate so
the caller can decide.

---

## 5. Configuration

Configuration is driven by **YAML frontmatter** embedded in the Markdown document,
not by function arguments.

```markdown
---
subject: "Monthly Newsletter"
preheader: "Preview text here"
theme:
  primary_color: "#007bff"
  font_family: "Arial, sans-serif"
---

# Hello World

Your email content here.
```

The configurer stage:
1. Extracts the YAML frontmatter block (delimited by `---`).
2. Parses it into a `Frontmatter` dataclass.
3. Resolves the `Theme` (22 properties: colors, typography, layout).
4. Merges with defaults; sanitizes the result.

The `Theme` dataclass defines the visual identity:

| Category | Properties |
|----------|------------|
| Colors | primary, secondary, background, text, link, button_text, border |
| Typography | font_family, heading_font, font_size, line_height |
| Layout | content_width, padding, button_radius, button_style |
| Dark mode | dark_background, dark_text, dark_primary, dark_secondary |

Rules:
- Options are explicit, never global variables.
- No `os.getenv` / env-driven behavior inside the library pipeline.
- Theme is **not** an `EmailStructure` — it is configuration passed separately.

---

## 6. Email-Safe Rendering

Rendering targets **email clients**, which differ from browsers:

- **MJML** is the internal format — mrml compiles it to email-safe HTML.
- **Inline styles** over classes/external CSS — many clients strip `<style>` and
  `<link>`.
- **Tables** (`<table>`) for anything tabular — div-based layout is unreliable.
- **No JavaScript**, no external images/fonts by default.
- Links use absolute `href`; relative/`data:`/`javascript:` URLs are neutralized.
- **Dual output**: HTML (for the email body) + text/plain (fallback).
- Sanitization is defensive: even if an earlier stage slips through raw HTML,
  the sanitizer contains it.

Responsive behavior (via MJML):
- Fluid widths, media queries injected by mrml.
- Tested against Gmail, Outlook, Apple Mail.

---

## 7. Public API Surface

Everything in `src/amail_md/__init__.py` is the public contract:

- `markdown_to_email(source, **options) -> RenderResult` — converts Markdown to email-safe HTML.
- `verify_markdown(source) -> list[ValidationError]` — validates Markdown and returns detailed errors.
- Typed exceptions in `amail_md.exceptions`.
- Domain types in `amail_md.email_structure` (Paragraph, Button, Heading, etc.)
  for advanced usage and extension.

`RenderResult` dataclass:

| Field | Type | Description |
|-------|------|-------------|
| `html` | `str` | Email-safe HTML |
| `text` | `str` | text/plain fallback |
| `meta` | `dict` | Extracted metadata (subject, preheader…) |
| `warnings` | `list[str]?` | Optional conversion warnings |

`ValidationError` dataclass:

| Field | Type | Description |
|-------|------|-------------|
| `line` | `int` | Line number where the error occurred |
| `column` | `int` | Column number (0 if not applicable) |
| `code` | `str` | Error code (e.g., BUTTON_MISSING_HREF) |
| `message` | `str` | Human-readable error description |
| `suggestion` | `str` | How to fix the issue |
| `severity` | `str` | Error severity (error, warning, info) |

`main()` backs the `amail-md` console script; it reads input and prints HTML.
It is thin and contains no conversion logic beyond calling the public API.

---

## 8. Email Structure (Domain Model)

The intermediate model between the parser and the compiler is **`EmailStructure`**,
an abstract base class that every piece of an email implements (see ADR-0002).

Why "Email Structure" instead of "IR" or "data model": it points at *how the
email is composed* — the pieces that make it up and how they nest.

Concrete subclasses:

| Type | Role |
|------|------|
| `Paragraph` | Plain text block (the **fallback** when nothing specific matches) |
| `Heading` | Section标题 (h1–h6) |
| `Button` | CTA: href, text, variant?, color?, width? |
| `Columns` | Multi-column layout container |
| `ColumnCell` | One column within a Columns block |
| `List` | Ordered or unordered list |
| `Quote` | Blockquote |
| `Image` | Image with alt text, src, width? |
| `Divider` | Horizontal rule / separator |
| `Spacer` | Vertical spacing element |

Rules:
- The core only knows these domain elements.
- `Theme` is **not** an `EmailStructure` — it is configuration.
- `RenderResult` (html, text, meta, warnings) is assembled by the orchestrator.
- Each `EmailStructure` component implements `to_mjml(theme)` to render itself.
- Adding a new element means adding a new subclass with `to_mjml()`.

---

## 9. Logging Pattern

The library itself is silent by default (pure functions, no logging). If any
component needs diagnostic output, use stdlib `logging`:

```python
log = logging.getLogger(__name__)
```

Rules:
- The library must not configure the root logger (the host application owns
  logging configuration).
- No secrets or large payloads logged.

---

## 10. Testing Pattern

- `pytest`, fixtures in `tests/conftest.py`.
- The core pipeline is deterministic, so tests assert **exact** HTML output for
  known inputs (see `docs/testing.md`).
- Sanitization tests assert escaping on injection payloads.
- The harness (`scripts/harness.py`) is the quality gate: env, base files,
  activities.json, ruff, compile, pytest.

---

## 11. Project Goals

Every decision must contribute to building:

> **"A small, deterministic, email-safe Markdown-to-HTML library that is
> predictable and easy to use."**

This means:
- **Deterministic**: pure functions, exact-output tests, no hidden state.
- **Email-first**: output that actually renders in email clients.
- **Safe**: sanitized output, escaped user input, no injection.
- **Simple**: tiny public API, no configuration plumbing, minimal deps.

---

## 12. Architecture Diagrams

### System Context

How amail-md fits into the bigger picture:

<img src="../../diagrams/svg/C4_Context.svg" alt="System Context Diagram" width="100%">

### Containers

The main containers inside amail-md:

<img src="../../diagrams/svg/C4_Container.svg" alt="Container Diagram" width="100%">

### Components

Internal components of the core container:

<img src="../../diagrams/svg/C4_Component.svg" alt="Component Diagram" width="100%">

### Render Pipeline

Sequence diagram showing how `markdown_to_email()` and `verify_markdown()` drive the conversion pipeline:

<img src="../../diagrams/svg/Sequence_Pipelines.svg" alt="Render Pipeline Sequence Diagram" width="100%">
