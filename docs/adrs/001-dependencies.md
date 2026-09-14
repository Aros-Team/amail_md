# ADR 0001 — Dependencies: markdown-it-py and mrml

## Status

Accepted

## Date

2026-08-09

## Context

`amail-md` is a Python library that converts Markdown to email-safe HTML. We
based the project on **emailmd** and analyzed its flow and dependencies to
decide which libraries to adopt.

The pipeline is a two-step conversion: Markdown → email structure → email-safe
HTML. Each step has a natural candidate. We had to pick a Markdown parser and
an HTML email compiler.

## Decision

- **markdown-it-py** for parsing Markdown.
- **mrml** for compiling to email-safe HTML.

Reasons:

- **mrml** — this is the computational **bottleneck** of the pipeline (the
  step that produces the final, client-compatible HTML). Choosing a fast,
  well-tested Rust implementation here matters most, because it dominates the
  time and correctness of the whole conversion.
- **markdown-it-py** — a well-maintained, spec-compliant Python implementation
  of CommonMark. Its AST is a good fit for our intermediate model, and an
  active project means fewer maintenance concerns.

Both libraries keep the core free of our own fragile parsing/rendering logic.

## Consequences

- The heavy rendering work lives in a compiled dependency (mrml), not in our
  Python code.
- We depend on two external projects; version compatibility must be tracked.
- markdown-it-py's AST is what our segmenter consumes to build the email
  structure.
