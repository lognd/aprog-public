from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from aprog.commands.package_cmd import cmd_package_private
from aprog.utils.repo import find_public_root

console = Console()


def cmd_submit(
    slug: str,
    solution: Optional[Path] = None,
    hidden_tests: Optional[Path] = None,
    grader: Optional[Path] = None,
    encrypt: bool = False,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()

    bundle = cmd_package_private(
        slug,
        solution=solution,
        hidden_tests=hidden_tests,
        grader=grader,
        public_root=root,
    )

    if encrypt:
        recipient = os.environ.get("APROG_GPG_RECIPIENT")
        if not recipient:
            console.print("[red]Error:[/red] APROG_GPG_RECIPIENT is not set")
            raise typer.Exit(1)
        encrypted = Path(str(bundle) + ".gpg")
        result = subprocess.run(
            [
                "gpg",
                "--recipient",
                recipient,
                "--output",
                str(encrypted),
                "--encrypt",
                str(bundle),
            ],
            capture_output=True,
        )
        if result.returncode != 0:
            console.print(f"[red]GPG error:[/red] {result.stderr.decode()}")
            raise typer.Exit(1)
        bundle.unlink()
        bundle = encrypted
        console.print(f"[green][OK][/green] Encrypted: {bundle}")

    intake_url = os.environ.get("APROG_INTAKE_URL")
    if intake_url:
        _upload(bundle, slug, intake_url)
    else:
        console.print(f"\nBundle: {bundle}")
        console.print(
            "\nSubmit this file to your maintainer using the process documented at:"
        )
        console.print(
            "  https://github.com/lognd/aprog-public/blob/main/docs/contributors/quickstart.md"
        )


def _upload(bundle: Path, slug: str, url: str) -> None:
    import httpx

    console.print(f"Uploading to {url}...")
    with open(bundle, "rb") as f:
        try:
            response = httpx.post(
                url,
                files={"bundle": (bundle.name, f, "application/gzip")},
                data={"assignment_slug": slug},
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            console.print(
                f"[green][OK][/green] Received -- id: {data.get('id', 'unknown')}"
            )
        except httpx.HTTPStatusError as e:
            console.print(f"[red]Upload failed:[/red] HTTP {e.response.status_code}")
            raise typer.Exit(1) from e
        except Exception as e:
            console.print(f"[red]Upload error:[/red] {e}")
            raise typer.Exit(1) from e
