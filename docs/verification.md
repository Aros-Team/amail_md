# Verification

> How to verify that work is correct.

---

## 1. Before declaring a task `done`

1. Run `uv run python scripts/harness.py` — all blocks must pass (exit code 0).
2. Verify lint: `uv run ruff check .` — no errors.
3. Verify format: `uv run ruff format --check .` — formatted.
4. Verify types: `uv run mypy src` — no type errors.
5. Verify tests: `uv run pytest` — all green.
6. Review `docs/CHECKPOINTS.md` — all applicable checkboxes marked.

---

## 2. Manual Verification Steps

### Code Quality
- No `print()` or debug statements left behind
- No TODOs without context
- Type hints on all signatures (enforced by ruff `ANN`)
- Docstrings on all public modules/classes/functions/methods (enforced by ruff `D`)
- No unused imports or dead code

### Architecture Compliance
- Modules live only where `docs/architecture.md` describes them
- Dependencies flow top-down (no circular imports)

### Logging
- Events logged via `logging.getLogger(__name__)`
- No sensitive data (API keys, secrets) in logs

### Tests
- New functionality has tests in `tests/`
- Tests pass independently and follow `docs/testing.md`

---

## 3. Reviewer Checklist

The reviewer agent must verify:

- [ ] Harness passes (`uv run python scripts/harness.py` exits 0)
- [ ] Ruff check passes (`uv run ruff check .`)
- [ ] Ruff format clean (`uv run ruff format --check .`)
- [ ] All tests pass (`uv run pytest`)
- [ ] Layering respected (no circular imports, modules where described)
- [ ] No `print()`, TODOs without context, unused imports
- [ ] Type hints on every signature and docstrings on public modules/classes/functions/methods (`uv run ruff check .` enforces this)
- [ ] Logs structured, no secrets
- [ ] Tests added and follow `docs/testing.md` (mutation mindset, exact asserts, negative/edge paths, no tautologies)
- [ ] No real credentials committed

---

## 4. Git Hygiene

Before closing a session:

- [ ] No temp files (`.pyc`, `__pycache__`, `*.tmp`)
- [ ] `progress/current.md` emptied to template
- [ ] Summary moved to `progress/history.md`
- [ ] `activities.json` status updated
- [ ] `docs/CHECKPOINTS.md` reflects the final state
