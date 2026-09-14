# ADR 0003 — Structured output instead of HTML-then-regex

## Status

Accepted

## Date

2026-08-09

## Context

`amail-md` is inspired by **emailmd**. We analyzed its flow and found a
difference in how it produces the final HTML that we deliberately did not
follow.

emailmd's approach:
1. Parse the Markdown.
2. Render the parser output **directly to HTML**.
3. Apply **regular expressions** over that HTML to inject email components
   (buttons, sections, columns, styling) by string matching.
4. Use **marker tricks** such as HTML comment tags (`<!-- ... -->`) as
   placeholders in the generated HTML, and later scan for those markers with
   regex to re-locate and re-position the elements in the document.

## Problem with that approach

Applying regex over generated HTML is fragile and **computationally risky**:

- Regex matches are error-prone and break on small markup changes (whitespace,
  attribute order, nesting).
- Relying on **comment-tag markers** as placeholders is especially fragile: the
  position of an element is only implicit in where the marker sits in the HTML
  text, so every re-positioning is another regex scan to find it again.
- Every regex scan is a second pass over the whole document; with many
  components this multiplies the work, and at scale the string scanning becomes
  a bottleneck.
- The HTML becomes a shared, lossy intermediate: by the time we are doing
  regex, the structure (blocks, nesting, semantics) is already baked into text,
  so it is hard to reason about and modify.

## Decision

`amail-md` does not go Markdown → HTML → regex. Instead it keeps a **structured
intermediate model** and does the transformation there:

1. Parse the Markdown with markdown-it-py into an AST.
2. Build our **`EmailStructure`** model (ADR 0002) from that AST — the semantic
   email elements and their nesting.
3. Compile the `EmailStructure` with **mrml** into the final email-safe HTML.

Transformations (adding a button, styling, sections) happen by manipulating the
structured model, not by matching strings or markers. Only the final step
produces HTML, once, with no regex post-processing and no placeholder markers.

## Consequences

- **No regex** over generated HTML — eliminates that whole class of fragility.
- The HTML is emitted once, so there is no costly string re-scanning; the
  transformation cost is bounded by the AST/structure size, not by document
  re-scans.
- Changes are safer and easier to test because we transform structured data,
  not text.
- We pay the cost of maintaining an intermediate model (ADR 0002) in exchange
  for that safety and clarity.
