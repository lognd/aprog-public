from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, TypedDict

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from aprog.constants import GENERATOR_VERSION
from aprog.paths import (
    generated_assignment_dir,
    grader_dir,
    sibling_hidden_tests_dir,
    solution_dir,
)
from aprog.utils.hashing import hash_assignment_public
from aprog.utils.repo import (
    all_assignment_slugs,
    find_public_root,
    load_assignment_config,
)

console = Console()


class _Row(TypedDict):
    slug: str
    language: str
    difficulty: str
    topics: list[str]
    status: str


def cmd_list(
    language: Optional[str] = None,
    difficulty: Optional[str] = None,
    topics: Optional[list[str]] = None,
    status: Optional[str] = None,
    as_json: bool = False,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    slugs = all_assignment_slugs(root)

    results: list[_Row] = []
    for slug in slugs:
        try:
            cfg = load_assignment_config(root, slug)
        except (FileNotFoundError, ValidationError):
            continue
        a = cfg.assignment
        c = cfg.classification

        if language and c.language != language:
            continue
        if difficulty and c.difficulty != difficulty:
            continue
        if topics and not all(t in c.topics for t in topics):
            continue
        if status and a.status != status:
            continue
        if not status and a.status == "draft":
            continue

        results.append(
            {
                "slug": a.slug,
                "language": c.language,
                "difficulty": c.difficulty,
                "topics": c.topics,
                "status": a.status,
            }
        )

    if as_json:
        console.print_json(json.dumps(results))
        return

    if not results:
        console.print("[dim]No assignments found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Slug")
    table.add_column("Language")
    table.add_column("Difficulty")
    table.add_column("Topics")
    table.add_column("Status")
    for r in results:
        table.add_row(
            r["slug"],
            r["language"],
            r["difficulty"],
            ", ".join(r["topics"]),
            r["status"],
        )
    console.print(table)


def cmd_info(
    slug: str,
    private_repo: Optional[Path] = None,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    try:
        cfg = load_assignment_config(root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(2) from e

    a = cfg.assignment
    c = cfg.classification
    t = cfg.template

    manifest_path = generated_assignment_dir(root, slug) / "assignment-manifest.json"

    hash_status = "missing"
    if manifest_path.exists():
        try:
            manifest_data = json.loads(manifest_path.read_text())
            current = hash_assignment_public(root, slug, GENERATOR_VERSION)
            stored = manifest_data.get("source_hash", "")
            hash_status = "current" if current == stored else "stale"
        except Exception:
            hash_status = "error"

    console.print(f"[bold]Slug:[/bold]         {a.slug}")
    console.print(f"[bold]Name:[/bold]         {a.name}")
    console.print(f"[bold]Author:[/bold]       {a.author}")
    console.print(f"[bold]Description:[/bold]  {a.description}")
    console.print(f"[bold]Status:[/bold]       {a.status}")
    console.print()
    console.print("[bold]Classification:[/bold]")
    console.print(f"  Language:   {c.language}")
    console.print(f"  Difficulty: {c.difficulty}")
    console.print(f"  Topics:     {', '.join(c.topics)}")
    if c.concepts:
        console.print(f"  Concepts:   {', '.join(c.concepts)}")
    console.print()
    console.print(
        f"[bold]Template:[/bold]     {t.slug}"
        + (f" (v{t.version})" if t.version else "")
    )
    console.print()
    console.print("[bold]Paths:[/bold]")
    console.print(f"  Root:          assignments/{slug}/")
    console.print(f"  README:        assignments/{slug}/README.md")
    console.print(f"  Visible tests: assignments/{slug}/visible-tests/")
    console.print()
    console.print("[bold]Generated:[/bold]")
    console.print(
        f"  Manifest:     generated/assignments/{slug}/assignment-manifest.json"
    )
    console.print(f"  Autograder:   generated/assignments/{slug}/run_autograder.py")
    console.print(f"  Hash status:  {hash_status}")

    if private_repo:
        console.print()
        console.print("[bold]Private:[/bold]")
        sol = solution_dir(private_repo, slug)
        ht = sibling_hidden_tests_dir(private_repo, slug)
        gr = grader_dir(private_repo, slug)
        vc = generated_assignment_dir(private_repo, slug) / "verification-config.json"
        console.print(
            f"  Solution:     {sol.relative_to(private_repo)}/      {'present' if sol.exists() else 'missing'}"
        )
        console.print(
            f"  Hidden tests: hidden-tests/{slug}/   {'present' if ht.exists() else 'missing'}"
        )
        console.print(
            f"  Grader:       grader/{slug}/          {'present' if gr.exists() else 'missing'}"
        )
        verified = "unknown"
        if vc.exists():
            try:
                d = json.loads(vc.read_text())
                verified = "yes" if d.get("verification_state") == "verified" else "no"
            except Exception:
                verified = "error"
        console.print(f"  Verified:     {verified}")
