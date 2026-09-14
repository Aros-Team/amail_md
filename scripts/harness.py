#!/usr/bin/env python3
"""
Verification harness for the amail-md project.

Run with: uv run python scripts/harness.py

Checks, in order:
  1. Environment (uv / python present)
  2. Base harness files exist (AGENTS.md, activities.json, progress/, docs/)
  3. activities.json is valid (schema, statuses, types, one in_progress at most)
  4. Session sync (activities ↔ progress/current.md, freshness, git diff)
  5. Code quality (ruff check + ruff format --check)
  6. Type checking (mypy)
  7. Compilation (python -m compileall)
  8. License headers (src/)
  9. Tests (pytest)
  10. Docstrings & doc-first policy

Exit code 0 only when every block passes.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RED = "\x1b[0;31m"
GREEN = "\x1b[0;32m"
YELLOW = "\x1b[0;33m"
NC = "\x1b[0m"

exit_code = 0

SESSION_STALE_DAYS = 3

REQUIRED_ACTIVITY_FIELDS = {"id", "name", "type", "status", "tasks"}
REQUIRED_TASK_FIELDS = {"id", "description", "status"}


def ok(msg: str) -> None:
    """Print a success message in green."""
    print(f"{GREEN}[OK]{NC}    {msg}")


def warn(msg: str) -> None:
    """Print a warning message in yellow."""
    print(f"{YELLOW}[WARN]{NC}  {msg}")


def fail(msg: str) -> None:
    """Print an error message in red and mark the run as failed."""
    global exit_code
    print(f"{RED}[FAIL]{NC}  {msg}")
    exit_code = 1


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run a command in the project root and return the completed process."""
    return subprocess.run(cmd, cwd=cwd or PROJECT_ROOT)


def command_exists(cmd: str) -> bool:
    """Return True when the command is available on the PATH."""
    return shutil.which(cmd) is not None


def check_license_headers() -> bool:
    """Verify every source file in src/ starts with the Apache 2.0 header."""
    copyright_re = re.compile(r"^# Copyright \d{4} Aros Team")
    src_dir = PROJECT_ROOT / "src"
    missing: list[Path] = []
    for path in sorted(src_dir.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if not copyright_re.match(text):
            missing.append(path)
    if missing:
        for path in missing:
            fail(f"Missing license header: {path.relative_to(PROJECT_ROOT)}")
        return False
    ok(f"All {len(list(src_dir.rglob('*.py')))} source files have a license header")
    return True


def check_docstrings() -> bool:
    """Verify all public functions in src/ have docstrings."""
    src_dir = PROJECT_ROOT / "src"
    missing: list[str] = []

    for path in sorted(src_dir.rglob("*.py")):
        if path.name == "__pycache__":
            continue
        try:
            import ast

            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                    # Skip private functions (starting with _)
                    if node.name.startswith("_"):
                        continue
                    # Check if it has a docstring
                    if (
                        not node.body
                        or not isinstance(node.body[0], ast.Expr)
                        or not isinstance(node.body[0].value, ast.Constant)
                        or not isinstance(node.body[0].value.value, str)
                    ):
                        rel = path.relative_to(PROJECT_ROOT)
                        missing.append(f"{rel}:{node.lineno} {node.name}()")
        except Exception:
            pass

    if missing:
        for m in missing:
            warn(f"Missing docstring: {m}")
        ok(f"Docstrings checked ({len(missing)} warnings)")
    else:
        ok("All public functions have docstrings")
    return True


def check_doc_first_policy() -> bool:
    """Verify docs exist before code: api-reference.md lists public functions."""
    src_dir = PROJECT_ROOT / "src"
    api_ref = PROJECT_ROOT / "docs" / "api-reference.md"

    # Collect all public functions from src/
    public_funcs: list[str] = []
    for path in sorted(src_dir.rglob("*.py")):
        if "__pycache__" in str(path) or path.name.startswith("_"):
            continue
        try:
            import ast

            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(
                    node, ast.FunctionDef | ast.AsyncFunctionDef
                ) and not node.name.startswith("_"):
                    public_funcs.append(node.name)
        except Exception:
            pass

    if not public_funcs:
        ok("Doc-first check skipped (no public functions yet)")
        return True

    # Check if api-reference.md exists and is not just a placeholder
    if api_ref.exists():
        content = api_ref.read_text(encoding="utf-8")
        # Check if it has real content (not just placeholder)
        if ":::" in content or "def " in content:
            ok("Doc-first check passed (api-reference.md has content)")
        else:
            warn("api-reference.md is a placeholder — update when implementing")
    else:
        warn("api-reference.md missing — create before implementing")

    return True


def check_activity_schema(activities: list[dict]) -> bool:
    """Verify each activity and task has all required fields."""
    has_missing = False
    for a in activities:
        missing = REQUIRED_ACTIVITY_FIELDS - set(a.keys())
        if missing:
            fail(
                f"Activity {a.get('id', '?')} missing required fields: "
                + ", ".join(sorted(missing))
            )
            has_missing = True
        for t in a.get("tasks", []):
            missing_t = REQUIRED_TASK_FIELDS - set(t.keys())
            if missing_t:
                fail(
                    f"Task {t.get('id', '?')} in activity {a.get('id')} "
                    f"missing: {', '.join(sorted(missing_t))}"
                )
                has_missing = True
    return not has_missing


def check_session_sync(activities: list[dict]) -> bool:
    """Verify consistency between activities.json and progress/current.md."""
    current_path = PROJECT_ROOT / "progress" / "current.md"
    current = current_path.read_text(encoding="utf-8")

    in_progress = [a for a in activities if a.get("status") == "in_progress"]

    # Template check: no in_progress → current.md should be empty/template
    if not in_progress:
        if "## Activity" in current:
            activity_section = current.split("## Activity")[1].split("##")[0]
            id_line = [
                line for line in activity_section.splitlines() if "- ID:" in line
            ]
            if id_line and id_line[0].split("- ID:")[1].strip():
                warn(
                    "No activity in_progress but progress/current.md has "
                    "an activity ID — reset to template"
                )
            else:
                ok("Session sync: no in_progress, current.md is clean")
        else:
            ok("Session sync: no in_progress, current.md is clean")
        return True

    # Cross-file consistency: in_progress activity must appear in current.md
    for a in in_progress:
        if a["id"] not in current:
            fail(
                f"Activity {a['id']} is in_progress in activities.json "
                "but not in progress/current.md"
            )
            return False

    # Session freshness: warn if current.md is too old
    mtime = datetime.fromtimestamp(current_path.stat().st_mtime)
    age_days = (datetime.now() - mtime).days
    if age_days > SESSION_STALE_DAYS:
        warn(
            f"progress/current.md is {age_days} days old "
            f"(>{SESSION_STALE_DAYS}-day limit) — update or close session"
        )
    else:
        ok(f"Session sync OK (activity {in_progress[0]['id']}, {age_days}d old)")

    return True


def check_git_diff_activity(activities: list[dict]) -> bool:
    """Warn if src/ has uncommitted changes with no activity in_progress."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=PROJECT_ROOT,
        capture_output=True,
    )
    # Also check staged files
    result_staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=PROJECT_ROOT,
        capture_output=True,
    )

    changed: list[str] = []
    if result.returncode == 0:
        changed.extend(
            f for f in result.stdout.decode().splitlines() if f.startswith("src/")
        )
    if result_staged.returncode == 0:
        changed.extend(
            f
            for f in result_staged.stdout.decode().splitlines()
            if f.startswith("src/")
        )

    # Deduplicate
    changed = list(dict.fromkeys(changed))

    if not changed:
        ok("Git diff: no uncommitted changes in src/")
        return True

    in_progress = [a for a in activities if a.get("status") == "in_progress"]
    if not in_progress:
        warn(
            f"src/ has {len(changed)} uncommitted change(s) but no "
            "activity is in_progress — create an activity first"
        )
    else:
        ok(f"Git diff: {len(changed)} file(s) match activity {in_progress[0]['id']}")

    return True


print("── 1. Environment Check ─────────────────────────────")

if not command_exists("uv"):
    fail("uv is not installed")
    sys.exit(1)
uv_result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
ok(f"uv -> {uv_result.stdout.strip()}")

if not command_exists("python3"):
    fail("python3 is not installed")
    sys.exit(1)
python_result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
ok(f"python3 -> {python_result.stdout.strip()}")

print("\n── 2. Base Harness Files ─────────────────────────────")

base_files = [
    "AGENTS.md",
    "activities.json",
    "progress/current.md",
    "progress/history.md",
    "docs/contributing/architecture.md",
    "docs/contributing/conventions.md",
    "docs/harness/verification.md",
    "docs/harness/CHECKPOINTS.md",
    "docs/contributing/testing.md",
]

for f in base_files:
    if (PROJECT_ROOT / f).exists():
        ok(f"Exists {f}")
    else:
        fail(f"Missing base file: {f}")

print("\n── 3. Validating activities.json ─────────────────────")

try:
    data = json.loads((PROJECT_ROOT / "activities.json").read_text(encoding="utf-8"))
    activities = data if isinstance(data, list) else data.get("activities", [])
    valid_statuses = {"pending", "in_progress", "done", "blocked"}
    valid_types = {"fix", "feat", "chore"}
    valid_task_statuses = {"pending", "in_progress", "done", "blocked"}
    valid_agents = {"implementer", "reviewer"}

    # Schema check (required fields)
    check_activity_schema(activities)

    in_progress = [a for a in activities if a.get("status") == "in_progress"]

    if len(in_progress) > 1:
        fail(f"Found {len(in_progress)} activities in in_progress (max 1)")

    for a in activities:
        if (
            a.get("status") == "done"
            and a.get("tasks")
            and any(t.get("status") != "done" for t in a["tasks"])
        ):
            warn(f"Activity {a.get('id')} is done but has tasks not done")

    for a in in_progress:
        if not a.get("tasks") or not any(
            t.get("status") == "in_progress" for t in a["tasks"]
        ):
            warn(f"Activity {a.get('id')} is in_progress but no task is in_progress")

    has_invalid = False
    for a in activities:
        if a.get("status") not in valid_statuses:
            fail(f"Invalid status in activity {a.get('id')}: {a.get('status')}")
            has_invalid = True
        if a.get("type") and a["type"] not in valid_types:
            fail(
                "Invalid type in activity "
                f"{a.get('id')}: {a.get('type')} "
                "(must be fix, feat, or chore)"
            )
            has_invalid = True
        if a.get("tasks") and isinstance(a["tasks"], list):
            for t in a["tasks"]:
                if t.get("status") and t["status"] not in valid_task_statuses:
                    fail(
                        "Invalid task status in activity "
                        f"{a.get('id')}: {t.get('status')}"
                    )
                    has_invalid = True
                if t.get("agent") and t["agent"] not in valid_agents:
                    fail(
                        "Invalid task agent in activity "
                        f"{a.get('id')}: {t.get('agent')} "
                        "(must be implementer or reviewer)"
                    )
                    has_invalid = True

    if not has_invalid:
        ok(f"activities.json valid ({len(activities)} activities)")
except Exception as e:
    fail(f"activities.json invalid: {e}")

print("\n── 4. Session Sync ──────────────────────────────────")

try:
    data = json.loads((PROJECT_ROOT / "activities.json").read_text(encoding="utf-8"))
    activities = data if isinstance(data, list) else data.get("activities", [])
    check_session_sync(activities)
    check_git_diff_activity(activities)
except Exception as e:
    warn(f"Session sync check skipped: {e}")

print("\n── 5. Code Quality (ruff) ────────────────────────────")

result = run(["uv", "run", "ruff", "check", "."])
if result.returncode == 0:
    ok("Ruff check passed")
else:
    fail("Ruff check errors found")

result = run(["uv", "run", "ruff", "format", "--check", "."])
if result.returncode == 0:
    ok("Ruff format clean")
else:
    fail("Ruff format drift (run 'uv run ruff format .')")

print("\n── 6. Type Checking (mypy) ───────────────────────────")

result = run(["uv", "run", "mypy", "src"])
if result.returncode == 0:
    ok("Mypy check passed")
else:
    fail("Mypy type errors found")

print("\n── 7. Compilation ─────────────────────────────────────")

result = run(["uv", "run", "python", "-m", "compileall", "-q", "src"])
if result.returncode == 0:
    ok("Compilation succeeded")
else:
    fail("Compilation failed")

print("\n── 8. License Headers (src/) ─────────────────────────")

check_license_headers()

print("\n── 9. Running Tests ───────────────────────────────────")

result = run(["uv", "run", "pytest"])
if result.returncode == 0:
    ok("All tests pass")
else:
    fail("Some tests are broken")

print("\n── 10. Docstrings & Doc-First ────────────────────────")

check_docstrings()
check_doc_first_policy()

print("\n── 11. Summary ───────────────────────────────────────")

if exit_code == 0:
    ok("Environment ready. You can start working.")
else:
    fail("Environment NOT ready. Resolve errors before advancing.")

sys.exit(exit_code)
