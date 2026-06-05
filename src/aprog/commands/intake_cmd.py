from __future__ import annotations

import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from rich.console import Console

from aprog.models.manifest import PackageManifest
from aprog.utils.repo import find_public_root

console = Console()


def cmd_intake(
    bundle: Path,
    public_repo: Optional[Path] = None,
    private_repo: Optional[Path] = None,
    force: bool = False,
    validate: bool = False,
    generate: bool = False,
) -> None:
    public_root = public_repo or find_public_root()
    if not private_repo:
        console.print("[red]Error:[/red] --private is required")
        raise typer.Exit(2)

    if not bundle.exists():
        console.print(f"[red]Error:[/red] Bundle not found: {bundle}")
        raise typer.Exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # Decrypt if needed
        if bundle.suffix == ".gpg":
            decrypted = tmp_path / bundle.stem
            result = subprocess.run(
                ["gpg", "--output", str(decrypted), "--decrypt", str(bundle)],
                capture_output=True,
            )
            if result.returncode != 0:
                console.print(f"[red]GPG error:[/red] {result.stderr.decode()}")
                raise typer.Exit(1)
            bundle = decrypted

        with tarfile.open(bundle, "r:gz") as tar:
            tar.extractall(tmp_path)

        subdirs = [d for d in tmp_path.iterdir() if d.is_dir()]
        if not subdirs:
            console.print("[red]Error:[/red] Empty bundle")
            raise typer.Exit(1)
        slug_dir = subdirs[0]
        slug = slug_dir.name

        manifest_path = slug_dir / "package-manifest.json"
        if not manifest_path.exists():
            console.print("[red]Error:[/red] Missing package-manifest.json in bundle")
            raise typer.Exit(1)

        try:
            pkg_manifest = PackageManifest.model_validate_json(manifest_path.read_text())
        except ValidationError as e:
            console.print(f"[red]Invalid package manifest:[/red] {e}")
            raise typer.Exit(1)

        public_assignment = public_root / "assignments" / slug
        if not public_assignment.exists():
            console.print(f"[red]Error:[/red] Assignment '{slug}' not found in public repo")
            raise typer.Exit(1)

        if not pkg_manifest.contains_grader:
            console.print("[red]Error:[/red] Bundle does not contain grader/pipeline.py")
            raise typer.Exit(1)

        grader_file = slug_dir / "grader" / "pipeline.py"
        if not grader_file.exists():
            console.print("[red]Error:[/red] grader/pipeline.py missing from bundle")
            raise typer.Exit(1)

        _copy_dir(slug_dir / "solution", private_repo / "solutions" / slug, force)
        if pkg_manifest.contains_hidden_tests and (slug_dir / "hidden-tests").exists():
            _copy_dir(slug_dir / "hidden-tests", private_repo / "hidden-tests" / slug, force)
        _copy_dir(slug_dir / "grader", private_repo / "grader" / slug, force)

        console.print(f"[green]✓[/green] Intake complete for '{slug}'")

    if validate:
        from aprog.commands.validate_cmd import cmd_validate
        code = cmd_validate(slug, private_repo=private_repo, public_root=public_root)
        if code != 0:
            raise typer.Exit(code)

    if generate:
        from aprog.commands.generate_config_cmd import cmd_generate_config
        cmd_generate_config(slug, private_repo=private_repo, public_root=public_root)


def _copy_dir(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and not force:
        console.print(f"[red]Error:[/red] {dst} already exists. Use --force to overwrite.")
        raise typer.Exit(1)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    console.print(f"  Copied: {src.name}/ → {dst}")
