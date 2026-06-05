from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from rich.console import Console

from aprog.utils.hashing import hash_assignment_public
from aprog.utils.repo import (
    all_assignment_slugs,
    find_public_root,
    load_assignment_config,
    load_root_config,
    load_template_config,
)

console = Console()

_PROHIBITED_NAMES = {
    "solution",
    "solutions",
    "hidden",
    "hidden-tests",
    "hidden_tests",
    "private",
    "private-notes.md",
    "answer-key.md",
    "grader",
    "pipeline.py",
}
_PROHIBITED_PATTERNS = [
    "solution.",
    "answer.",
    "reference-solution.",
    "reference_solution.",
]
_PRIVATE_DIRS = {
    "solution",
    "solutions",
    "hidden",
    "hidden-tests",
    "hidden_tests",
    "private",
    "grader",
}
_SAFE_DIRS = {"visible-tests", "assets", "expected"}


def _scan_public_violations(assignment_root: Path) -> list[str]:
    violations = []
    for path in assignment_root.rglob("*"):
        rel = path.relative_to(assignment_root)
        parts = rel.parts
        name = path.name

        if name in _PROHIBITED_NAMES:
            violations.append(f"{rel} -- prohibited name")
            continue

        for part in parts[:-1]:
            if part in _PRIVATE_DIRS:
                violations.append(f"{rel} -- '{part}/' directory is private")
                break

        if path.is_file():
            for pat in _PROHIBITED_PATTERNS:
                if name.startswith(pat) or name == pat.rstrip("."):
                    violations.append(f"{rel} -- matches prohibited pattern '{pat}*'")
                    break

    return violations


def cmd_validate(
    slug: str,
    private_repo: Optional[Path] = None,
    public_root: Optional[Path] = None,
) -> int:
    root = public_root or find_public_root()
    errors: list[str] = []

    # Load root config
    try:
        root_cfg = load_root_config(root)
    except Exception as e:
        console.print(f"[red]Error loading aprog.toml:[/red] {e}")
        raise typer.Exit(1)

    # Load assignment config
    try:
        cfg = load_assignment_config(root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except ValidationError as e:
        console.print(f"[red]Validation error in assignment.toml:[/red]")
        for err in e.errors():
            console.print(f"  {'.'.join(str(x) for x in err['loc'])}: {err['msg']}")
        raise typer.Exit(1)

    a = cfg.assignment
    c = cfg.classification

    # Slug matches directory name
    if a.slug != slug:
        errors.append(
            f"Slug mismatch: assignment.toml has '{a.slug}', directory is '{slug}'"
        )

    # Classification values exist in root config
    if c.language not in root_cfg.classification.languages:
        errors.append(f"Unknown language: '{c.language}'")
    if c.difficulty not in root_cfg.classification.difficulties:
        errors.append(f"Unknown difficulty: '{c.difficulty}'")
    for t in c.topics:
        if t not in root_cfg.classification.topics:
            errors.append(f"Unknown topic: '{t}'")
    for concept in c.concepts:
        if concept not in root_cfg.classification.concepts:
            errors.append(f"Unknown concept: '{concept}'")
    for label in c.labels:
        if label not in root_cfg.labels:
            errors.append(f"Unknown label: '{label}'")

    # Template exists
    tpl_dir = root / "templates" / cfg.template.slug
    if not tpl_dir.exists():
        errors.append(f"Template not found: templates/{cfg.template.slug}/")

    assignment_root = root / "assignments" / slug

    # README exists
    if not (assignment_root / "README.md").exists():
        errors.append("Missing README.md")

    # Visible tests exist
    vt_dir = assignment_root / "visible-tests"
    if not vt_dir.exists() or not any(vt_dir.iterdir()):
        errors.append("Missing or empty visible-tests/")

    # Public/private boundary scan
    violations = _scan_public_violations(assignment_root)
    for v in violations:
        errors.append(f"Boundary violation: {v}")

    # Generated files currency
    manifest_path = (
        root / "generated" / "assignments" / slug / "assignment-manifest.json"
    )
    stale = False
    if not manifest_path.exists():
        errors.append(
            "Generated manifest missing -- run: aprog generate-config " + slug
        )
        stale = True
    else:
        import json

        try:
            data = json.loads(manifest_path.read_text())
            current_hash = hash_assignment_public(root, slug)
            if data.get("source_hash") != current_hash:
                errors.append(
                    "Generated files are stale -- run: aprog generate-config " + slug
                )
                stale = True
        except Exception:
            errors.append("Could not read generated manifest")
            stale = True

    # Private validation
    if private_repo:
        sol_dir = private_repo / "solutions" / slug
        if not sol_dir.exists():
            errors.append(f"Private: missing solution directory")
        grader_file = private_repo / "grader" / slug / "pipeline.py"
        if not grader_file.exists():
            errors.append(f"Private: missing grader/pipeline.py")

    if errors:
        console.print(f"[red]Validation failed for '{slug}':[/red]")
        for msg in errors:
            console.print(f"  [red][FAIL][/red] {msg}")
        return 4 if stale and len(errors) == 1 else 1
    else:
        console.print(f"[green][OK][/green] {slug} -- valid")
        return 0


def cmd_validate_all(
    private_repo: Optional[Path] = None,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    slugs = all_assignment_slugs(root)
    failed = []
    for slug in slugs:
        code = cmd_validate(slug, private_repo=private_repo, public_root=root)
        if code != 0:
            failed.append(slug)
    if failed:
        raise typer.Exit(1)
