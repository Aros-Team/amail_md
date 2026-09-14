# ADR 0004 — Documentation: Zensical (MkDocs-compatible)

## Status

Accepted

## Date

2026-09-11 (revised 2026-09-13)

## Context

`amail-md` needs a documentation site that covers:
- Getting started guide
- API reference (auto-generated from docstrings)
- Architecture explanation
- Examples

The options were:
- **Sphinx** + reStructuredText — the classic, used by NumPy/Django
- **MkDocs** + Material — modern, Markdown-native
- **Zensical** — MkDocs-compatible SSG by the Material for MkDocs team
- **pdoc** — minimal, docstring-only

## Decision

**Zensical** with **mkdocstrings-python** for API reference.

Zensical is a drop-in replacement for MkDocs 1.x built by the creators of
Material for MkDocs. It reads the same `mkdocs.yml` configuration, uses the
same Material theme, and supports the same plugins — but is written in Rust
(faster builds) and avoids the upcoming MkDocs 2.0 breaking changes (no plugin
system, no Material compatibility, closed contribution model).

Reasons:

- **Markdown-native** — no reStructuredText learning curve. Docs files
  (`docs/architecture.md`, ADRs) can be reused directly.
- **mkdocstrings** auto-generates API reference from Google-style docstrings.
- **Material theme** — built-in search, dark mode, responsive, tabs, instant
  navigation. No custom CSS needed.
- **Fast rebuilds** — Rust core, faster than Python-based MkDocs.
- **GitHub Pages** deployment with zero cost.
- **Future-proof** — avoids MkDocs 2.0 deprecation (no plugins, no Material
  compatibility, unlicensed). Zensical is MIT-licensed and actively maintained.
- **Drop-in compatible** — same `mkdocs.yml`, same `serve`/`build` commands,
  same plugin ecosystem. Zero migration cost.

MkDocs + Material was rejected because:
- MkDocs 2.0 removes plugin system, breaks Material compatibility.
- MkDocs 1.x is unmaintained (no releases in 18+ months).
- Unclear security posture going forward.

Sphinx was rejected because:
- reStructuredText is harder to write and maintain than Markdown.
- Overkill for a small-to-medium library.
- Configuration is more complex.

pdoc was rejected because:
- Too minimal — no navigation, no theming, no site structure.

## Consequences

- Dev dependency: `zensical` + `mkdocstrings-python`.
- Docs live in `docs/` (already exists), served by `zensical serve`.
- API reference is auto-generated — docstrings are the source of truth.
- Deployment: GitHub Actions → GitHub Pages on push to `main`.
- ADRs (`docs/adrs/`) can be included in the site via nav config.
- Same `mkdocs.yml` works with both `mkdocs` and `zensical` commands.
