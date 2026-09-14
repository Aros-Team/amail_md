# Conventions

> Style rules, naming, and structure. Follow exactly.

---

## 1. Python Style

- **Python 3.13+**, formatted and linted with `ruff`.
- Run `uv run ruff check .` — all checks must pass.
- Run `uv run ruff format .` before committing.
- Line length: 88 (ruff default `line-length`).
- **Type hints are mandatory** on every function/method signature, including
  parameters and return types (`from __future__ import annotations` where
  needed). Enforced by ruff rule group `ANN`.
- **Static type checking with `mypy`** must pass (`uv run mypy src`). All public
  functions are fully typed; no `Any` leaks across the public API surface.
- **Docstrings are mandatory** for every public module, class, function, and
  method (excluding magic methods and `__init__`). One-line docstring in
  imperative mood, capitalized, ending with a period. Enforced by ruff rule
  group `D`.
- `typing.Any` is discouraged: type the concrete contract instead.
  `self`/`cls` do not need annotations.
- No `print()` for debugging — use `logging`.
- No TODOs without context.
- No dead code, unused imports, or unused parameters.

---

## 2. File & Module Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Module | `snake_case.py` | `mail_parser.py` |
| Class | `PascalCase` | `MailParser` |
| Function/method | `snake_case` | `parse_message`, `build_report` |
| Constant | `UPPER_SNAKE_CASE` | `DEFAULT_OUTPUT` |

No `Service`/`Manager` suffixes on class names unless they describe a real role.

---

## 3. Project Layout

- **Package code** lives in `src/amail_md/`, split by responsibility (markdown,
  render, sanitize) per `docs/architecture.md`.
- **Public API** is exported from `src/amail_md/__init__.py`.
- **Tests** live in `tests/`, mirroring the package structure.
- **Scripts** (harness) live in `scripts/` and are not shipped as part of the
  installed package.
- Add new modules only if described in `docs/architecture.md`.

---

## 4. Public API & CLI

- The **public API** is everything exported from `src/amail_md/__init__.py` —
  the functions users import. Keep it tiny and stable.
- The core pipeline is **pure functions**: same input → same output, no I/O, no
  hidden state.
- The `amail-md` console script (`main()` in `__init__.py`) is a thin wrapper:
  it reads input, calls the public API, and prints HTML. No conversion logic
  lives there.
- Exit codes are meaningful (0 = success, non-zero = failure).
- Errors are reported on stderr; stdout carries the command output only.
- Raise only typed, documented exceptions from the public API (see
  `docs/architecture.md` §4).

---

## 5. Logging

- Use the stdlib `logging` module, `log = logging.getLogger(__name__)`.
- Event name first, then key=value context.
- Log durations (`duration_ms`) for external calls.
- No sensitive data in logs (never log full secrets/keys).

---

## 6. Tests

- Follow `docs/testing.md` (Testing Policy) — a test's value is its ability to
  fail when the code is wrong (**mutation mindset**).
- `pytest`; fixtures in `tests/conftest.py`.
- Name test functions `test_<unit>_<behavior>_<condition>` in `tests/test_*.py`.
- New functionality must have tests (happy + error + edge paths); run
  `uv run pytest` before declaring done.
- **Tests are written before implementation** — see `docs/development.md`.

---

## 7. Development Workflow

**Docs → Test → Implement** — the mandatory order for every feature:

1. **Document** — update architecture, API reference, examples, changelog.
2. **Test** — write tests that validate the documentation (they should fail).
3. **Implement** — write code that makes tests pass.

See `docs/development.md` for the full policy and rationale.

---

## 7. License Header

Every source file under `src/` must start with the Apache 2.0 license header.
The header is enforced by the harness (`uv run python scripts/harness.py`).
Tests, scripts, and config files do not need it.

```python
# Copyright 2026 Aros Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

Rules:
- Place it as the first lines of the file, before any docstring or code.
- Update the year to the current year when modifying the file.
- Only `src/` Python files are checked.

---

## 8. What is NOT Allowed

- `print()` for debugging
- TODOs without context
- Unused imports / dead code
- Swallowing exceptions with no log
- Real credentials committed
- Logic in `main()` / CLI that belongs in the library pipeline
- Global mutable state or hidden configuration in the core pipeline
