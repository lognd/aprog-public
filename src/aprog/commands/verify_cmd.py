from __future__ import annotations

import inspect
import json
import sys
import zipfile
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from aprog.commands.validate_cmd import cmd_validate
from aprog.paths import (
    assignment_dir,
    generated_assignment_dir,
    grader_dir,
    grader_hidden_tests_dir,
    grader_pipeline_file,
    sibling_hidden_tests_dir,
    solution_dir,
)
from aprog.utils.repo import (
    all_assignment_slugs,
    find_public_root,
    load_assignment_config,
)

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
    code = cmd_validate(slug, public_root=public_root)
    if code not in (0, 4):
        console.print(f"[red]Public validation failed for '{slug}'[/red]")
        raise typer.Exit(1)

    sol_dir = solution_dir(private_repo, slug)
    if not sol_dir.exists():
        console.print(
            f"[red]Error:[/red] Solution directory missing: solutions/assignments/{slug}/"
        )
        raise typer.Exit(4)

    grader_file = grader_pipeline_file(private_repo, slug)
    if not grader_file.exists():
        console.print(
            f"[red]Error:[/red] Grader pipeline missing: grader/{slug}/pipeline.py"
        )
        raise typer.Exit(5)

    ht_dir = grader_hidden_tests_dir(private_repo, slug)
    if (
        not ht_dir.exists()
        and not sibling_hidden_tests_dir(private_repo, slug).exists()
    ):
        console.print("[dim]Note:[/dim] No hidden-tests directory found (optional)")

    # Run grader against reference solution
    sys.path.insert(0, str(grader_dir(private_repo, slug)))

    try:
        from lograder.pipeline.config import config
        from pipeline import make_pipeline  # ty: ignore[unresolved-import]
    except ImportError as e:
        console.print(f"[red]Import error:[/red] {e}")
        raise typer.Exit(1) from e

    console.print(f"Running grader against reference solution for '{slug}'...")

    try:
        sig = inspect.signature(make_pipeline)
        kwargs = (
            {"submission_dir": sol_dir} if "submission_dir" in sig.parameters else {}
        )
        with config(root_directory=private_repo):
            pipeline = make_pipeline(**kwargs)
            score = pipeline()
    except Exception as e:
        console.print(f"[red]Pipeline error:[/red] {e}")
        raise typer.Exit(1) from e
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
            "[red][FAIL][/red] Verification failed: reference solution did not earn full points"
        )
        raise typer.Exit(1) from None


def cmd_verify_all(
    public_repo: Optional[Path] = None,
    private_repo: Optional[Path] = None,
) -> None:
    """Run `cmd_verify` for every assignment in the public repo, failing at the end
    if any of them failed (so CI sees one failure summarizing the whole run)."""
    public_root = public_repo or find_public_root()
    failed: list[str] = []
    for slug in all_assignment_slugs(public_root):
        try:
            cmd_verify(slug, public_repo=public_root, private_repo=private_repo)
        except typer.Exit as e:
            if e.exit_code != 0:
                failed.append(slug)
    if failed:
        console.print(f"[red]Verification failed for:[/red] {', '.join(failed)}")
        raise typer.Exit(1) from None


def _update_verification_state(private_repo: Path, slug: str, state: str) -> None:
    vc_path = generated_assignment_dir(private_repo, slug) / "verification-config.json"
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
        raise typer.Exit(2) from None

    try:
        cfg = load_assignment_config(public_root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    gen_dir = generated_assignment_dir(public_root, slug)

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
        raise typer.Exit(1) from None

    if not grader_pipeline_file(private_repo, slug).exists():
        console.print(
            f"[red]Error:[/red] Grader pipeline missing: grader/{slug}/pipeline.py"
        )
        raise typer.Exit(1) from None

    dist = (output_dir or public_root / "dist").resolve()
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{slug}-gradescope.zip"

    # Unix permission bits stored in the high 16 bits of external_attr.
    _EXEC = 0o100755 << 16  # rwxr-xr-x executable
    _DATA = 0o100644 << 16  # rw-r--r-- non-executable

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        # setup.sh -- must be executable so Gradescope can run it
        deps = cfg.grader.dependencies
        lograder_req = f"lograder{deps.lograder}" if deps.lograder else "lograder"
        extra = " ".join(deps.extra)
        lines = ["#!/usr/bin/env bash", "set -e"]
        if deps.system:
            pkgs = " ".join(deps.system)
            lines += [
                "apt-get update -qq",
                f"apt-get install -y --no-install-recommends {pkgs}",
            ]
        lines.append(f"pip install '{lograder_req}' {extra}")
        setup_sh = "\n".join(lines) + "\n"
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
        grader_src_dir = grader_dir(private_repo, slug)
        _SKIP_GRADER = {"__pycache__", "build", ".git"}
        for path in sorted(grader_src_dir.rglob("*")):
            if path.is_file() and not any(p in _SKIP_GRADER for p in path.parts):
                arc = f"grader/{path.relative_to(grader_src_dir)}"
                info = zipfile.ZipInfo(arc)
                info.external_attr = _DATA
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())

        # visible-tests from the public repo (needed by CMakeLists.txt at build time)
        visible_dir = assignment_dir(public_root, slug) / "visible-tests"
        if not visible_dir.exists():
            visible_dir = (
                public_root / "examples" / "assignments" / slug / "visible-tests"
            )
        if visible_dir.exists():
            for path in sorted(visible_dir.rglob("*")):
                if path.is_file():
                    arc = f"visible-tests/{path.relative_to(visible_dir)}"
                    info = zipfile.ZipInfo(arc)
                    info.external_attr = _DATA
                    info.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(info, path.read_bytes())

        # hidden tests (sibling location; embedded hidden-tests already rode
        # along with the grader directory above)
        ht_pkg_dir = sibling_hidden_tests_dir(private_repo, slug)
        if ht_pkg_dir.exists():
            for path in sorted(ht_pkg_dir.rglob("*")):
                if path.is_file():
                    arc = f"hidden-tests/{path.relative_to(ht_pkg_dir)}"
                    info = zipfile.ZipInfo(arc)
                    info.external_attr = _DATA
                    info.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(info, path.read_bytes())

    console.print(f"[green][OK][/green] {out}")
