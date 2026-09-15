# Architecture Decision Records

An ADR captures an important architectural decision along with its context
and consequences.

## Index

| ADR | Decision |
|-----|----------|
| [001](001-dependencies.md) | Dependencies: markdown-it-py and mrml |
| [002](002-email-structure-root.md) | Email Structure as the model root |
| [003](003-structured-output-not-regex.md) | Structured output instead of regex |
| [004](004-documentation-mkdocs.md) | Documentation: MkDocs + Material |
| [005](005-cli-optional-dependency.md) | CLI as optional dependency |
| [006](006-linting-verify-markdown.md) | Linting with verify_markdown() |
| [007](007-mjml-compilation-registry.md) | MJML Compilation via Registry Pattern |
| [008](008-linter-rule-engine.md) | Linter Rule Engine Pattern |
| [009](009-segmenter-registry.md) | Segmenter Registry Pattern |
| [010](010-generic-token.md) | Generic Token for Parser Independence |

## Format

Each ADR follows this template:

1. **Status** — Proposed / Accepted / Deprecated / Superseded
2. **Date** — When decided
3. **Context** — What is the issue that motivates a decision
4. **Decision** — What is the change being proposed or decided
5. **Consequences** — What are the resulting trade-offs
