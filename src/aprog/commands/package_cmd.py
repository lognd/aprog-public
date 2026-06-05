from __future__ import annotations

import json
import os
import tarfile
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from aprog.models.manifest import PackageManifest
from aprog.utils.repo import find_public_root, load_assignment_config

console = Console()


def cmd_package_public(
    slug: str,
    output_dir: Optional[Path] = None,
    public_root: Optional[Path] = None,
) -> Path:
    root = public_root or find_public_root()
    try:
        cfg = load_assignment_config(root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    dist = (output_dir or root / "dist").resolve()
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{slug}-public.tar.gz"

    assignment_root = root / "assignments" / slug
    gen_dir = root / "generated" / "assignments" / slug
    manifest_path = gen_dir / "assignment-manifest.json"

    with tarfile.open(out, "w:gz") as tar:
        for path in sorted(assignment_root.rglob("*")):
            if path.is_file():
                tar.add(path, arcname=f"{slug}/{path.relative_to(assignment_root)}")
        if manifest_path.exists():
            tar.add(manifest_path, arcname=f"{slug}/generated/assignment-manifest.json")

    console.print(f"[green]✓[/green] {out}")
    return out


def cmd_package_private(
    slug: str,
    solution: Optional[Path] = None,
    hidden_tests: Optional[Path] = None,
    grader: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    created_by: str = "",
    public_root: Optional[Path] = None,
) -> Path:
    root = public_root or find_public_root()

    # Resolve paths from staging dir if not provided
    if not solution or not hidden_tests or not grader:
        from aprog.utils.repo import resolve_staging_dir

        staging = resolve_staging_dir(None)
        if staging:
            staging_slug = staging / slug
            solution = solution or (staging_slug / "solution")
            hidden_tests = hidden_tests or (staging_slug / "hidden-tests")
            grader = grader or (staging_slug / "grader")

    missing = []
    if not solution or not solution.exists():
        missing.append("--solution")
    if not grader or not grader.exists():
        missing.append("--grader")
    if missing:
        console.print(f"[red]Error:[/red] Missing required paths: {', '.join(missing)}")
        raise typer.Exit(1)

    assert solution is not None
    assert grader is not None

    dist = (output_dir or root / "dist").resolve()
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{slug}-private.tar.gz"

    has_hidden = hidden_tests is not None and hidden_tests.exists()
    pipeline_file = grader / "pipeline.py"
    if not pipeline_file.exists():
        console.print(f"[red]Error:[/red] grader/pipeline.py not found in {grader}")
        raise typer.Exit(1)

    manifest = PackageManifest(
        assignment_slug=slug,
        contains_solution=True,
        contains_hidden_tests=has_hidden,
        contains_grader=True,
        created_by=created_by,
    )

    with tarfile.open(out, "w:gz") as tar:
        _add_string_to_tar(
            tar,
            json.dumps(manifest.model_dump(), indent=2) + "\n",
            f"{slug}/package-manifest.json",
        )
        _add_dir_to_tar(tar, solution, f"{slug}/solution")
        if has_hidden and hidden_tests is not None:
            _add_dir_to_tar(tar, hidden_tests, f"{slug}/hidden-tests")
        _add_dir_to_tar(tar, grader, f"{slug}/grader")

    console.print(f"[green]✓[/green] {out}")
    return out


def _add_dir_to_tar(tar: tarfile.TarFile, src: Path, arcname_prefix: str) -> None:
    for path in sorted(src.rglob("*")):
        if path.is_file():
            tar.add(path, arcname=f"{arcname_prefix}/{path.relative_to(src)}")


def _add_string_to_tar(tar: tarfile.TarFile, content: str, arcname: str) -> None:
    import io

    data = content.encode()
    info = tarfile.TarInfo(name=arcname)
    info.size = len(data)
    tar.addfile(info, io.BytesIO(data))
