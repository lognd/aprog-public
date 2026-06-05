from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from aprog.utils.repo import find_public_root

console = Console()


def cmd_verify(
    slug: str,
    public_repo: Optional[Path] = None,
    private_repo: Optional[Path] = None,
) -> None:
    public_root = public_repo or find_public_root()

    if not private_repo:
        console.print("[red]Error:[/red] --private is required")
        raise typer.Exit(2)

    # Public validation
    from aprog.commands.validate_cmd import cmd_validate

    code = cmd_validate(slug, public_root=public_root)
    if code not in (0, 4):
        console.print(f"[red]Public validation failed for '{slug}'[/red]")
        raise typer.Exit(1)

    sol_dir = private_repo / "solutions" / slug
    if not sol_dir.exists():
        console.print(
            f"[red]Error:[/red] Solution directory missing: solutions/{slug}/"
        )
        raise typer.Exit(4)

    grader_file = private_repo / "grader" / slug / "pipeline.py"
    if not grader_file.exists():
        console.print(
            f"[red]Error:[/red] Grader pipeline missing: grader/{slug}/pipeline.py"
        )
        raise typer.Exit(5)

    ht_dir = private_repo / "hidden-tests" / slug
    if not ht_dir.exists():
        console.print(f"[dim]Note:[/dim] No hidden-tests directory found (optional)")

    # Run grader against reference solution
    import sys

    sys.path.insert(0, str(private_repo / "grader" / slug))

    try:
        from lograder.pipeline.config import config
        from pipeline import make_pipeline  # type: ignore[import-not-found]
    except ImportError as e:
        console.print(f"[red]Import error:[/red] {e}")
        raise typer.Exit(1)

    console.print(f"Running grader against reference solution for '{slug}'...")

    try:
        with config(root_directory=sol_dir):
            pipeline = make_pipeline()
            score = pipeline()
    except Exception as e:
        console.print(f"[red]Pipeline error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        sys.path.pop(0)

    total = score.total()
    passed = total.earned >= total.possible

    console.print(
        f"Score: {total.earned}/{total.possible}"
        + (f" + {total.extra_credit} extra credit" if total.extra_credit else "")
    )

    if passed:
        console.print(f"[green][OK][/green] Verification passed for '{slug}'")
        _update_verification_state(private_repo, slug, "verified")
    else:
        console.print(
            f"[red][FAIL][/red] Verification failed: reference solution did not earn full points"
        )
        raise typer.Exit(1)


def _update_verification_state(private_repo: Path, slug: str, state: str) -> None:
    vc_path = (
        private_repo / "generated" / "assignments" / slug / "verification-config.json"
    )
    if not vc_path.exists():
        return
    try:
        data = json.loads(vc_path.read_text())
        data["verification_state"] = state
        vc_path.write_text(json.dumps(data, indent=2) + "\n")
    except Exception:
        pass


def cmd_package_gradescope(
    slug: str,
    public_repo: Optional[Path] = None,
    private_repo: Optional[Path] = None,
    output_dir: Optional[Path] = None,
) -> None:
    public_root = public_repo or find_public_root()
    if not private_repo:
        console.print("[red]Error:[/red] --private is required")
        raise typer.Exit(2)

    from aprog.utils.repo import load_assignment_config

    try:
        cfg = load_assignment_config(public_root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    import zipfile

    gen_dir = public_root / "generated" / "assignments" / slug

    # Fail early if required generated files are missing rather than silently
    # producing a broken zip that Gradescope accepts but cannot run.
    missing_generated = [
        name
        for name in ("run_autograder", "run_autograder.py")
        if not (gen_dir / name).exists()
    ]
    if missing_generated:
        console.print(
            f"[red]Error:[/red] Generated files missing for '{slug}': "
            + ", ".join(missing_generated)
        )
        console.print(f"  Run: aprog generate-config {slug} --force")
        raise typer.Exit(1)

    if not (private_repo / "grader" / slug / "pipeline.py").exists():
        console.print(
            f"[red]Error:[/red] Grader pipeline missing: grader/{slug}/pipeline.py"
        )
        raise typer.Exit(1)

    dist = (output_dir or public_root / "dist").resolve()
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{slug}-gradescope.zip"

    # Unix permission bits stored in the high 16 bits of external_attr.
    _EXEC = 0o100755 << 16  # rwxr-xr-x executable
    _DATA = 0o100644 << 16  # rw-r--r-- non-executable

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        # setup.sh -- must be executable so Gradescope can run it
        deps = cfg.grader.dependencies
        _LOGRADER_GITHUB = "git+https://github.com/lognd/lograder.git"
        lograder_req = (
            f"{_LOGRADER_GITHUB}@{deps.lograder}" if deps.lograder else _LOGRADER_GITHUB
        )
        extra = " ".join(deps.extra)
        setup_sh = (
            f"#!/usr/bin/env bash\nset -e\npip install '{lograder_req}' {extra}\n"
        )
        info = zipfile.ZipInfo("setup.sh")
        info.external_attr = _EXEC
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, setup_sh)

        # run_autograder (shell shim) and run_autograder.py -- both executable
        for name in ("run_autograder", "run_autograder.py"):
            src = gen_dir / name
            info = zipfile.ZipInfo(name)
            info.external_attr = _EXEC
            info.compress_type = zipfile.ZIP_DEFLATED
            info.file_size = src.stat().st_size
            zf.writestr(info, src.read_bytes())

        # full grader directory (pipeline.py + any driver files like main.cpp)
        grader_dir = private_repo / "grader" / slug
        for path in sorted(grader_dir.rglob("*")):
            if path.is_file():
                arc = f"grader/{path.relative_to(grader_dir)}"
                info = zipfile.ZipInfo(arc)
                info.external_attr = _DATA
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())

        # hidden tests
        ht_dir = private_repo / "hidden-tests" / slug
        if ht_dir.exists():
            for path in sorted(ht_dir.rglob("*")):
                if path.is_file():
                    arc = f"hidden-tests/{path.relative_to(ht_dir)}"
                    info = zipfile.ZipInfo(arc)
                    info.external_attr = _DATA
                    info.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(info, path.read_bytes())

    console.print(f"[green][OK][/green] {out}")
