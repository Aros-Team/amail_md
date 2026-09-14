# Development Workflow

> How we build features: Docs → Test → Implement.

---

## The Pipeline

Every feature follows this order. No exceptions.

```
1. DOCUMENT   →  What does it do? API shape? Edge cases?
2. TEST       →  Write tests that fail (red)
3. IMPLEMENT  →  Write code that passes (green)
4. REFACTOR   →  Clean up (tests stay green)
```

### 1. Document First

Before writing any code, update the relevant docs:

- **Architecture** (`docs/contributing/architecture.md`) — if adding a new module,
  layer, or changing the pipeline.
- **API Reference** (`docs/api-reference.md`) — if adding/changing public API.
- **Examples** (`docs/examples.md`) — if the feature has user-facing usage.
- **Changelog** (`docs/changelog.md`) — add an entry under `[Unreleased]`.

Documentation must describe:
- **What** the feature does (behavior, not implementation).
- **API shape** — function signatures, parameters, return types.
- **Edge cases** — what happens with empty input, invalid config, etc.
- **Examples** — at least one working code snippet.

### 2. Test Second

Write tests that **validate the documentation**:

- Tests assert **exact output** for known inputs (deterministic).
- Tests cover **happy path + error paths + edge cases**.
- Tests are written **before** the implementation exists.
- If the feature has no tests, it is not implemented yet.

See `docs/contributing/testing.md` for the testing philosophy.

### 3. Implement Third

Now write the code to make the tests pass:

- Follow `docs/contributing/conventions.md` for style.
- Follow `docs/contributing/architecture.md` for placement.
- Do not add functionality not described in the docs.
- Do not skip tests to ship faster.

---

## Why This Order

| Benefit | Explanation |
|---------|-------------|
| **Design clarity** | Forces you to think about the API before coding |
| **Living documentation** | Docs are written when context is fresh, not after |
| **Regression safety** | Tests exist from day one |
| **Smaller diffs** | Each step is a focused commit |

---

## Exceptions

- **Bug fixes**: may start with a failing test (the bug report), then document
  the fix, then implement.
- **Refactors**: if behavior doesn't change, tests + docs may already exist.
  Update docs only if the internal structure changes.
- **Research spikes**: temporary code in `scripts/` or notebooks. No doc/test
  requirement until the spike becomes a real feature.

---

## Verification

The harness (`scripts/harness.py`) checks that:

- Public functions have docstrings.
- `docs/api-reference.md` is not stale (lists all public functions).
- New modules appear in `docs/contributing/architecture.md` layering section.

If any of these are missing, the harness fails.
