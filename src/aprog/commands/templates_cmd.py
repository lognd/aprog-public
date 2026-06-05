from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from aprog.utils.repo import find_public_root, load_template_config

console = Console()


def _all_template_slugs(public_root: Path) -> list[str]:
    tpl_dir = public_root / "templates"
    if not tpl_dir.exists():
        return []
    return sorted(
        d.name
        for d in tpl_dir.iterdir()
        if d.is_dir() and (d / "template.toml").exists()
    )


def cmd_templates_list(
    language: Optional[str] = None,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    slugs = _all_template_slugs(root)

    table = Table(show_header=True, header_style="bold")
    table.add_column("Slug")
    table.add_column("Language")
    table.add_column("Description")

    found = False
    for slug in slugs:
        try:
            cfg = load_template_config(root, slug)
        except (FileNotFoundError, ValidationError):
            continue
        if language and cfg.classification.language != language:
            continue
        table.add_row(
            cfg.template.slug, cfg.classification.language, cfg.template.description
        )
        found = True

    if not found:
        console.print("[dim]No templates found.[/dim]")
        return
    console.print(table)


def cmd_templates_info(slug: str, public_root: Optional[Path] = None) -> None:
    root = public_root or find_public_root()
    try:
        cfg = load_template_config(root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(2)

    t = cfg.template
    c = cfg.classification
    pub = cfg.outputs.public
    priv = cfg.outputs.private

    console.print(f"[bold]Slug:[/bold]        {t.slug}")
    console.print(f"[bold]Name:[/bold]        {t.name}")
    console.print(f"[bold]Version:[/bold]     {t.version}")
    console.print(f"[bold]Language:[/bold]    {c.language}")
    console.print(f"[bold]Description:[/bold] {t.description}")
    console.print()

    pub_outputs = []
    if pub.assignment_toml:
        pub_outputs.append("assignment.toml")
    if pub.readme:
        pub_outputs.append("README.md")
    if pub.visible_tests:
        pub_outputs.append("visible-tests/")
    if pub.expected:
        pub_outputs.append("expected/")
    if pub.assets:
        pub_outputs.append("assets/")
    console.print(f"[bold]Public outputs:[/bold]")
    console.print(f"  {', '.join(pub_outputs)}")

    priv_outputs = []
    if priv.solution:
        priv_outputs.append("solution/")
    if priv.hidden_tests:
        priv_outputs.append("hidden-tests/")
    if priv.grader:
        priv_outputs.append("grader/pipeline.py")
    console.print(f"[bold]Private outputs:[/bold]")
    console.print(f"  {', '.join(priv_outputs)}")
