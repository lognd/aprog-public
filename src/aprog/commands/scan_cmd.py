from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from aprog.utils.hashing import hash_assignment_public
from aprog.utils.repo import (
    all_assignment_slugs,
    find_public_root,
    load_assignment_config,
)

console = Console()

_PRIVATE_DIRS = {
    "solution",
    "solutions",
    "hidden",
    "hidden-tests",
    "hidden_tests",
    "private",
    "grader",
}
_PROHIBITED_NAMES = {
    "solution",
    "solutions",
    "hidden",
    "hidden-tests",
    "hidden_tests",
    "private",
    "private-notes.md",
    "answer-key.md",
    "pipeline.py",
}
_PROHIBITED_PREFIXES = (
    "solution.",
    "answer.",
    "reference-solution.",
    "reference_solution.",
)


def _scan_one(assignment_root: Path) -> list[str]:
    violations = []
    for path in assignment_root.rglob("*"):
        rel = path.relative_to(assignment_root)
        parts = rel.parts
        name = path.name

        if name in _PROHIBITED_NAMES:
            violations.append(
                f"ERROR: {assignment_root.name}/{rel} — prohibited name '{name}'"
            )
            continue

        for part in parts[:-1]:
            if part in _PRIVATE_DIRS:
                violations.append(
                    f"ERROR: {assignment_root.name}/{rel} — '{part}/' directory is private"
                )
                break

        if path.is_file():
            for prefix in _PROHIBITED_PREFIXES:
                if name.startswith(prefix) or name == prefix.rstrip("."):
                    violations.append(
                        f"ERROR: {assignment_root.name}/{rel} — matches prohibited pattern '{prefix}*'"
                    )
                    break

    return violations


def cmd_scan_public(
    slug: Optional[str] = None,
    all_assignments: bool = False,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    slugs = all_assignment_slugs(root) if all_assignments else ([slug] if slug else [])

    if not slugs:
        console.print("[red]Error:[/red] Provide a slug or --all")
        raise typer.Exit(2)

    all_violations = []
    for s in slugs:
        assignment_root = root / "assignments" / s
        if not assignment_root.exists():
            console.print(f"[red]Error:[/red] Assignment not found: assignments/{s}/")
            raise typer.Exit(2)
        all_violations.extend(_scan_one(assignment_root))

    if all_violations:
        for v in all_violations:
            console.print(v)
        raise typer.Exit(1)
    else:
        console.print("[green]✓[/green] No boundary violations found.")


def cmd_check_generated(
    slug: Optional[str] = None,
    all_assignments: bool = False,
    private_repo: Optional[Path] = None,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    slugs = all_assignment_slugs(root) if all_assignments else ([slug] if slug else [])

    if not slugs:
        console.print("[red]Error:[/red] Provide a slug or --all")
        raise typer.Exit(2)

    any_stale = False
    for s in slugs:
        gen_dir = root / "generated" / "assignments" / s
        manifest = gen_dir / "assignment-manifest.json"
        autograder = gen_dir / "run_autograder.py"

        if not manifest.exists():
            console.print(
                f"MISSING: generated/assignments/{s}/assignment-manifest.json"
            )
            console.print(f"  Run: aprog generate-config {s}")
            any_stale = True
            continue

        try:
            data = json.loads(manifest.read_text())
            current = hash_assignment_public(root, s)
            stored = data.get("source_hash", "")
            if current != stored:
                console.print(
                    f"STALE: generated/assignments/{s}/assignment-manifest.json"
                )
                if not autograder.exists():
                    console.print(f"STALE: generated/assignments/{s}/run_autograder.py")
                console.print(f"  Run: aprog generate-config {s}")
                any_stale = True
        except Exception as e:
            console.print(f"ERROR: Could not read manifest for {s}: {e}")
            any_stale = True

    if any_stale:
        raise typer.Exit(1)
    else:
        console.print("[green]✓[/green] All generated files current.")
