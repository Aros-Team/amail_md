# ADR 0005 — CLI as Optional Dependency

## Status

Accepted

## Date

2026-09-14

## Context

amail-md is primarily a **library** (`import amail_md`). The CLI (`amail-md lint/render`) is a convenience layer for content authors, not the core product.

We need to decide: should `typer` (CLI framework) be a required dependency or optional?

## Decision

`typer` is an **optional dependency** under the `[cli]` extra.

```toml
[project.optional-dependencies]
cli = ["typer>=0.9.0"]
```

Users install:
- `pip install amail-md` — library only (no typer)
- `pip install amail-md[cli]` — library + CLI (with typer)

## Consequences

- Library users don't pay the cost of an unused dependency.
- CLI users opt-in explicitly.
- The `amail_md` package must guard CLI imports with `try/except ImportError`.
- The CLI entry point (`amail-md` console script) is only available with `[cli]`.
