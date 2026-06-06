from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Optional

import typer
from jinja2 import StrictUndefined
from rich.console import Console

from aprog.utils.repo import find_public_root, load_template_config, resolve_staging_dir

console = Console()

_SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def _render_jinja(source: str, variables: dict) -> str:
    from jinja2 import Template

    return Template(source, undefined=StrictUndefined).render(**variables)


def cmd_new(
    slug: str,
    template: str,
    difficulty: Optional[str] = None,
    topics: Optional[list[str]] = None,
    staging_dir: Optional[Path] = None,
    force: bool = False,
    public_root: Optional[Path] = None,
) -> None:
    if not _SLUG_RE.match(slug):
        console.print(f"[red]Error:[/red] Slug must be kebab-case, got {slug!r}")
        raise typer.Exit(2)

    root = public_root or find_public_root()

    try:
        tpl_cfg = load_template_config(root, template)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(2) from e

    assignment_root = root / "assignments" / slug
    if assignment_root.exists() and not force:
        console.print(
            f"[red]Error:[/red] Assignment already exists: {assignment_root}\n"
            "Pass --force to overwrite."
        )
        raise typer.Exit(1) from None

    staging = resolve_staging_dir(staging_dir) or (root.parent / "aprog-staging")
    staging_slug_dir = staging / slug

    variables = {
        "slug": slug,
        "template_slug": template,
        "difficulty": difficulty or tpl_cfg.classification.default_difficulty,
        "topics": topics or tpl_cfg.classification.recommended_topics,
        "assignment_name": slug.replace("-", " ").title(),
        "artifact_name": slug,
        "language": tpl_cfg.classification.language,
    }

    tpl_dir = root / "templates" / template
    public_tpl_dir = tpl_dir / "public"
    private_tpl_dir = tpl_dir / "private"

    # Render public files
    if public_tpl_dir.exists():
        _render_tree(public_tpl_dir, assignment_root, variables)
    else:
        assignment_root.mkdir(parents=True, exist_ok=True)
        _write_default_public(assignment_root, variables)

    # Render private staging files
    if private_tpl_dir.exists():
        _render_tree(private_tpl_dir, staging_slug_dir, variables)
    else:
        _write_default_private(staging_slug_dir, variables)

    console.print(f"[green]Created:[/green] assignments/{slug}/")
    console.print(
        f"[green]Staging:[/green] {staging_slug_dir}   (private working directory)"
    )
    console.print()
    console.print("Next steps:")
    console.print(f"  1. Edit assignments/{slug}/README.md")
    console.print(f"  2. Fill in assignments/{slug}/assignment.toml")
    console.print(f"  3. Add visible tests to assignments/{slug}/visible-tests/")
    console.print(f"  4. Fill in {staging_slug_dir}/grader/pipeline.py")
    console.print(f"  5. Run: aprog validate {slug}")


def _render_tree(src: Path, dst: Path, variables: dict) -> None:
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        rendered_name = str(rel)
        if rendered_name.endswith(".j2"):
            rendered_name = rendered_name[:-3]
        dest_path = dst / rendered_name
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        if item.suffix == ".j2" or item.name.endswith(".j2"):
            content = _render_jinja(item.read_text(), variables)
            dest_path.write_text(content)
        else:
            shutil.copy2(item, dest_path)


def _write_default_public(dst: Path, v: dict) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    topics_toml = "\n".join(f'  "{t}",' for t in v["topics"])
    (dst / "assignment.toml").write_text(
        f"[assignment]\n"
        f'slug = "{v["slug"]}"\n'
        f'name = "{v["assignment_name"]}"\n'
        f'author = "your-github-handle"\n'
        f'description = "TODO: describe this assignment."\n'
        f'version = "0.1.0"\n'
        f'status = "draft"\n\n'
        f"[classification]\n"
        f'language = "{v["language"]}"\n'
        f'difficulty = "{v["difficulty"]}"\n'
        f"topics = [\n{topics_toml}\n]\n\n"
        f"[template]\n"
        f'slug = "{v["template_slug"]}"\n\n'
        f"[grader]\n"
        f'visibility = "after_due_date"\n'
        f'stdout_visibility = "after_due_date"\n'
    )
    (dst / "README.md").write_text(
        f"# {v['assignment_name']}\n\nTODO: write the assignment statement.\n"
    )
    (dst / "visible-tests").mkdir(exist_ok=True)
    (dst / "visible-tests" / "test_visible.py").write_text(
        "# Add visible tests here.\n"
    )
    (dst / "expected").mkdir(exist_ok=True)
    (dst / "expected" / ".gitkeep").touch()
    (dst / "assets").mkdir(exist_ok=True)
    (dst / "assets" / ".gitkeep").touch()


def _write_default_private(dst: Path, v: dict) -> None:
    (dst / "solution").mkdir(parents=True, exist_ok=True)
    (dst / "hidden-tests" / "tests").mkdir(parents=True, exist_ok=True)
    (dst / "grader").mkdir(parents=True, exist_ok=True)
    (dst / "grader" / "pipeline.py").write_text(
        "from lograder.pipeline.input.local_directory import LocalDirectory\n"
        "from lograder.pipeline.pipeline import Pipeline\n"
        "from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase\n"
        "from lograder.pipeline.score import TestCaseScorer\n\n"
        "# FILL IN: Add test cases.\n"
        "_CASES = [\n"
        "    OutputCompareCase(\n"
        '        name="test_example",\n'
        "        args=[],\n"
        '        stdin="",\n'
        '        expected_stdout="",\n'
        "    ),\n"
        "]\n\n"
        "# FILL IN: Assign point values.\n"
        "_SCORER = TestCaseScorer(\n"
        '    points_per_case={"test_example": 10.0},\n'
        f'    label="{v["assignment_name"]} Correctness",\n'
        ")\n\n\n"
        "def make_pipeline() -> Pipeline:\n"
        "    step = LocalDirectory()\n"
        f'    tests = OutputCompareTest("{v["artifact_name"]}", _CASES)\n'
        "    tests.scorer = _SCORER\n"
        "    return Pipeline([step, tests])\n"
    )
