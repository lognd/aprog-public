"""
Structural tests for every activity in activities/.

For each slug:
  1. launch.py exists and is valid Python (ast.parse).
  2. README.md exists.
  3. launch.py defines a main() function.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_PUBLIC_ROOT = Path(__file__).resolve().parents[2]
_ACTIVITIES_DIR = _PUBLIC_ROOT / "activities"


def _activity_slugs() -> list[str]:
    if not _ACTIVITIES_DIR.exists():
        return []
    return sorted(
        d.name
        for d in _ACTIVITIES_DIR.iterdir()
        if d.is_dir() and (d / "launch.py").exists()
    )


@pytest.mark.parametrize("slug", _activity_slugs())
def test_activity_has_launch_py(slug: str) -> None:
    assert (_ACTIVITIES_DIR / slug / "launch.py").is_file()


@pytest.mark.parametrize("slug", _activity_slugs())
def test_activity_has_readme(slug: str) -> None:
    assert (_ACTIVITIES_DIR / slug / "README.md").is_file(), (
        f"activities/{slug}/README.md is missing"
    )


@pytest.mark.parametrize("slug", _activity_slugs())
def test_launch_py_is_valid_python(slug: str) -> None:
    src = (_ACTIVITIES_DIR / slug / "launch.py").read_text(encoding="utf-8")
    try:
        ast.parse(src)
    except SyntaxError as exc:
        pytest.fail(f"activities/{slug}/launch.py has a syntax error: {exc}")


@pytest.mark.parametrize("slug", _activity_slugs())
def test_launch_py_defines_main(slug: str) -> None:
    src = (_ACTIVITIES_DIR / slug / "launch.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    }
    assert "main" in names, f"activities/{slug}/launch.py has no main() function"
