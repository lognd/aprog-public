# mypy: ignore-errors
"""
Unit tests for all templates in templates/.

Checks:
  - template.toml exists for each template
  - private/grader/pipeline.py.j2 exists
  - every .j2 file renders without Jinja2 errors
  - pipeline.py.j2 renders to valid Python syntax
"""

from __future__ import annotations

import ast
from pathlib import Path

import jinja2
import pytest

_TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
_RENDER_VARS = {
    "assignment_name": "Widget Assignment",
    "artifact_name": "widget",
    "slug": "widget-assignment",
    "assignment_slug": "widget-assignment",
    "difficulty": "medium",
    "topics": ["data-structures"],
}


def _all_template_slugs() -> list[str]:
    if not _TEMPLATES_DIR.exists():
        return []
    return sorted(
        d.name
        for d in _TEMPLATES_DIR.iterdir()
        if d.is_dir() and (d / "template.toml").exists()
    )


def _all_j2_files(slug: str) -> list[Path]:
    return sorted((_TEMPLATES_DIR / slug).rglob("*.j2"))


@pytest.mark.parametrize("slug", _all_template_slugs())
def test_template_toml_exists(slug: str) -> None:
    assert (_TEMPLATES_DIR / slug / "template.toml").exists()


@pytest.mark.parametrize("slug", _all_template_slugs())
def test_pipeline_j2_exists(slug: str) -> None:
    assert (_TEMPLATES_DIR / slug / "private" / "grader" / "pipeline.py.j2").exists()


@pytest.mark.parametrize("slug", _all_template_slugs())
def test_all_j2_files_render_without_error(slug: str) -> None:
    env = jinja2.Environment(
        undefined=jinja2.StrictUndefined, keep_trailing_newline=True
    )
    for j2_path in _all_j2_files(slug):
        source = j2_path.read_text(encoding="utf-8")
        rendered = env.from_string(source).render(**_RENDER_VARS)
        assert rendered is not None, f"{j2_path.name} rendered None"


@pytest.mark.parametrize("slug", _all_template_slugs())
def test_pipeline_j2_renders_valid_python(slug: str) -> None:
    env = jinja2.Environment(
        undefined=jinja2.StrictUndefined, keep_trailing_newline=True
    )
    j2_path = _TEMPLATES_DIR / slug / "private" / "grader" / "pipeline.py.j2"
    source = j2_path.read_text(encoding="utf-8")
    rendered = env.from_string(source).render(**_RENDER_VARS)
    try:
        ast.parse(rendered)
    except SyntaxError as exc:
        pytest.fail(f"{slug}/pipeline.py.j2 rendered invalid Python: {exc}")
