# Architecture

> What "good work" means in this project.

---

## 1. Project Overview

amail-md is a Python **library** that converts **Markdown to email-safe HTML**.
It is consumed as a package (`amail_md`) by other code, and it also ships a thin
`amail-md` console entry point for convenience. The core value is a deterministic,
pure-function pipeline: Markdown in → HTML out, tuned for email clients (not web
browsers).

Design goals:
- **Deterministic** — the same Markdown always produces the same HTML.
- **Email-first** — output works in limited email renderers (inline styles,
  tables, no external resources).
- **Safe** — escapes user input; no raw HTML injection.
- **Minimal** — small dependency footprint, no state.

---

## 2. Core Pipeline (pure functions)

The package exposes a small set of **pure functions** (no I/O, no global state).
The canonical entry point:

```python
from amail_md import markdown_to_email_html

html = markdown_to_email_html(md_text)
```

Pipeline stages (each a pure function that feeds the next):

| Stage | Responsibility |
|-------|---------------|
| Parse | Turn Markdown source into an intermediate AST / block list |
| Transform | Apply email-specific rewrites (tables, links, code, emphasis) |
| Render | Emit HTML string with inline styles |
| Sanitize | Escape/neutralize anything unsafe before returning |

Rules:
- Functions are **pure**: same input → same output, no hidden state.
- No network, no filesystem, no randomness inside the pipeline.
- Each stage is independently testable.
- Keep stages one-way: parse → transform → render → sanitize. No backward
  dependencies or circular imports.

---

## 3. Layering

```
amail_md/
  markdown/    # Markdown parsing and AST model
  render/      # HTML rendering (email-safe), inline styles
  sanitize/    # output hardening / escaping
  __init__.py  # public API (the functions users import) + main()
```

Pattern rules:
- Only `__init__.py` exposes the public API surface; internal modules import
  freely but are not part of the public contract.
- **Public API is stable and tiny** — think carefully before adding to it.
- Internal modules never import from `__init__.py` (avoids circular imports).
- No I/O in the core pipeline; anything that touches disk/network/clock lives
  behind an explicit seam (e.g. the CLI entry point).

---

## 4. Error Handling Pattern

Use a typed error hierarchy rooted at `amail_md.exceptions.MarkdownError`.

- A `ParseError` (invalid / unrepresentable input) is raised on input that
  cannot be converted.
- `RenderError` signals a stage failure that is the library's fault, not the
  caller's.
- Boundary rules: the **public API** validates input and raises only typed,
  documented exceptions. Callers never see raw library-internal exceptions.

Do **not** swallow exceptions silently — always let typed errors propagate so
the caller can decide.

---

## 5. Configuration

The core pipeline is **configuration-free** by default. If options are needed
(e.g. max heading level, table styling, base URL for links), pass them as
keyword arguments to the public function — do not rely on ambient/env state.

```python
html = markdown_to_email_html(md_text, heading_style="simple", max_depth=3)
```

Rules:
- Options are explicit arguments with safe defaults, never global variables.
- No `os.getenv` / env-driven behavior inside the library pipeline.

---

## 6. Email-Safe Rendering

Rendering targets **email clients**, which differ from browsers:

- **Inline styles** over classes/external CSS — many clients strip `<style>` and
  `<link>`.
- **Tables** (`<table>`) for anything tabular — div-based layout is unreliable.
- **No JavaScript**, no external images/fonts by default.
- Links use absolute `href`; relative/`data:`/`javascript:` URLs are neutralized.
- Sanitization is applied **last** and is defensive: even if an earlier stage
  slips through raw HTML, the sanitizer contains it.

---

## 7. Public API Surface

Everything in `src/amail_md/__init__.py` is the public contract:

- `markdown_to_email_html(source, **options) -> str` — the primary function.
- Typed exceptions in `amail_md.exceptions`.
- Optional helper types (e.g. an options dataclass) if they aid discoverability.

`main()` backs the `amail-md` console script; it reads input and prints HTML.
It is thin and contains no conversion logic beyond calling the public API.

---

## 8. Logging Pattern

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

## 9. Testing Pattern

- `pytest`, fixtures in `tests/conftest.py`.
- The core pipeline is deterministic, so tests assert **exact** HTML output for
  known inputs (see `docs/testing.md`).
- Sanitization tests assert escaping on injection payloads.
- The harness (`scripts/harness.py`) is the quality gate: env, base files,
  activities.json, ruff, compile, pytest.

---

## 10. Project Goals

Every decision must contribute to building:

> **"A small, deterministic, email-safe Markdown-to-HTML library that is
> predictable and easy to use."**

This means:
- **Deterministic**: pure functions, exact-output tests, no hidden state.
- **Email-first**: output that actually renders in email clients.
- **Safe**: sanitized output, escaped user input, no injection.
- **Simple**: tiny public API, no configuration plumbing, minimal deps.
