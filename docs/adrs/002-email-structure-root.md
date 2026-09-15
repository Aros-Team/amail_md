# ADR 0002 — `EmailStructure` as the model root

## Status

Accepted

## Date

2026-08-09

## Context

`amail-md` converts Markdown to email-safe HTML through an intermediate model
that sits between the parser (markdown-it-py) and the compiler (mrml). This is
what the core pipeline builds and manipulates before handing it to the renderer.

By "intermediate model" we mean: the structured representation of the email
that the core owns — independent of both the Markdown syntax (in) and the MJML
(internal to mrml, out). The core works only with this model; the adapters
translate into and out of it.

We needed a name and a shape for this model that reflect the domain.

- "IR" (intermediate representation) is accurate but purely technical — it
  says nothing about what the model represents.
- "Email Data Structure" focuses on the *data* (names, numbers, fields), not on
  how the email is composed, which is exactly what our library is about.

## Decision

- The model is **`EmailStructure`**, a **base class** that every piece
  of an email implements. "Email Structure" points at *how the email is
  composed* — the pieces that make it up and how they nest.
- Every element the parser reports and that we support is modeled as a concrete
  subclass of `EmailStructure`: `Paragraph`, `Button`, `ColumnCell`, `Heading`,
  `List`, `Quote`, `Image`, `Divider`, `Spacer`, …
- `Paragraph` is the **fallback** block when nothing more specific matches.
- The core only knows these domain elements. `Theme` is **not** an
  `EmailStructure` — it is configuration (light/dark palette, typography,
  layout) passed separately, not a piece of the email tree. `RenderResult`
  (the final output: html, text, meta, warnings) is assembled by the orchestrator.

## Consequences

- The domain is explicit: reading the model tells you what an email is made of.
- A common contract (`EmailStructure`) enables polymorphism instead of
  `type`-switching.
- The core stays independent of both markdown-it-py and mrml.
- More classes to maintain, and a schema change for each newly supported
  element.
