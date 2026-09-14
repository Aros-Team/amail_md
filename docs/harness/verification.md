# Verification

> How to verify that work is correct.

---

## 0. Development Workflow Check

Before code exists, verify the pipeline was followed:

1. **Docs exist** — `docs/contributing/architecture.md` describes the module/function.
2. **API documented** — `docs/api-reference.md` lists the public function.
3. **Tests exist** — `tests/test_*.py` has tests for the new functionality.
4. **Tests fail** — before implementation, tests should fail (red phase).
5. **Then implement** — code exists and tests pass (green phase).

If code exists without docs or tests, the task is **not done**.

See `docs/contributing/development.md` for the full policy.

---

## 1. Before declaring a task `done`

1. Run `uv run python scripts/harness.py` — all blocks must pass (exit code 0).
2. Verify lint: `uv run ruff check .` — no errors.
3. Verify format: `uv run ruff format --check .` — formatted.
4. Verify types: `uv run mypy src` — no type errors.
5. Verify tests: `uv run pytest` — all green.
6. Review `docs/harness/CHECKPOINTS.md` — all applicable checkboxes marked.
7. **Doc-first verified** — harness checks that docs and tests exist before code.

---

## 2. Harness Checks (automated)

The harness (`scripts/harness.py`) runs these checks in order:

### 2.1 Environment
- `uv` installed
- `python3` installed

### 2.2 Base Files
All required files exist: AGENTS.md, activities.json, progress/*, docs/*

### 2.3 activities.json Validation
- **Schema**: each activity has `id`, `name`, `type`, `status`, `tasks`
- **Tasks**: each task has `id`, `description`, `status`
- **Statuses**: valid values (`pending`, `in_progress`, `done`, `blocked`)
- **Types**: valid values (`fix`, `feat`, `chore`)
- **Max 1** activity `in_progress`
- **Consistency**: done activity should have all tasks done
- **Agent**: valid values (`implementer`, `reviewer`)

### 2.4 Session Sync
- **Cross-file**: if activity is `in_progress` in activities.json, it must appear in `progress/current.md`
- **Template check**: if no activity is `in_progress`, `progress/current.md` should be empty/template
- **Freshness**: warn if `progress/current.md` is older than 3 days with active work
- **Git diff**: warn if `src/` has uncommitted changes with no activity `in_progress`

### 2.5 Code Quality
- `ruff check` passes
- `ruff format --check` passes

### 2.6 Type Checking
- `mypy src` passes

### 2.7 Compilation
- `python -m compileall` succeeds

### 2.8 License Headers
- All `src/*.py` files start with Apache 2.0 header

### 2.9 Tests
- `pytest` passes

### 2.10 Docstrings & Doc-First
- All public functions have docstrings
- `docs/api-reference.md` is not stale

---

## 3. Manual Verification Steps

### Code Quality
- No `print()` or debug statements left behind
- No TODOs without context
- Type hints on all signatures (enforced by ruff `ANN`)
- Docstrings on all public modules/classes/functions/methods (enforced by ruff `D`)
- No unused imports or dead code

### Architecture Compliance
- Modules live only where `docs/contributing/architecture.md` describes them
- Dependencies flow top-down (no circular imports)

### Logging
- Events logged via `logging.getLogger(__name__)`
- No sensitive data (API keys, secrets) in logs

### Tests
- New functionality has tests in `tests/`
- Tests pass independently and follow `docs/contributing/testing.md`

---

## 4. Reviewer Checklist

The reviewer agent must verify:

- [ ] Harness passes (`uv run python scripts/harness.py` exits 0)
- [ ] Ruff check passes (`uv run ruff check .`)
- [ ] Ruff format clean (`uv run ruff format --check .`)
- [ ] All tests pass (`uv run pytest`)
- [ ] Layering respected (no circular imports, modules where described)
- [ ] No `print()`, TODOs without context, unused imports
- [ ] Type hints on every signature and docstrings on public modules/classes/functions/methods
- [ ] Logs structured, no secrets
- [ ] Tests added and follow `docs/contributing/testing.md`
- [ ] No real credentials committed
- [ ] Session sync: activities.json ↔ progress/current.md consistent

---

## 5. Git Hygiene

Before closing a session:

- [ ] No temp files (`.pyc`, `__pycache__`, `*.tmp`)
- [ ] `progress/current.md` emptied to template
- [ ] Summary moved to `progress/history.md`
- [ ] `activities.json` status updated
- [ ] `docs/harness/CHECKPOINTS.md` reflects the final state
