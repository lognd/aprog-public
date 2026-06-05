# mypy: ignore-errors
from __future__ import annotations

import json
import tarfile
from pathlib import Path

import pytest

from aprog.commands.package_cmd import cmd_package_private, cmd_package_public


def test_package_public_creates_tarball(public_root: Path, tmp_path: Path) -> None:
    out = cmd_package_public("linked-list-insertion", output_dir=tmp_path, public_root=public_root)
    assert out.exists()
    assert out.name == "linked-list-insertion-public.tar.gz"


def test_package_public_contains_readme(public_root: Path, tmp_path: Path) -> None:
    out = cmd_package_public("linked-list-insertion", output_dir=tmp_path, public_root=public_root)
    with tarfile.open(out, "r:gz") as tar:
        names = tar.getnames()
    assert any("README.md" in n for n in names)


def test_package_public_contains_assignment_toml(public_root: Path, tmp_path: Path) -> None:
    out = cmd_package_public("linked-list-insertion", output_dir=tmp_path, public_root=public_root)
    with tarfile.open(out, "r:gz") as tar:
        names = tar.getnames()
    assert any("assignment.toml" in n for n in names)


def test_package_private_creates_tarball(public_root: Path, private_root: Path, tmp_path: Path) -> None:
    sol = private_root / "solutions" / "linked-list-insertion"
    ht = private_root / "hidden-tests" / "linked-list-insertion"
    gr = private_root / "grader" / "linked-list-insertion"
    out = cmd_package_private(
        "linked-list-insertion",
        solution=sol, hidden_tests=ht, grader=gr,
        output_dir=tmp_path, public_root=public_root,
    )
    assert out.exists()
    assert out.name == "linked-list-insertion-private.tar.gz"


def test_package_private_contains_pipeline(public_root: Path, private_root: Path, tmp_path: Path) -> None:
    sol = private_root / "solutions" / "linked-list-insertion"
    ht = private_root / "hidden-tests" / "linked-list-insertion"
    gr = private_root / "grader" / "linked-list-insertion"
    out = cmd_package_private(
        "linked-list-insertion",
        solution=sol, hidden_tests=ht, grader=gr,
        output_dir=tmp_path, public_root=public_root,
    )
    with tarfile.open(out, "r:gz") as tar:
        names = tar.getnames()
    assert any("pipeline.py" in n for n in names)


def test_package_private_contains_manifest(public_root: Path, private_root: Path, tmp_path: Path) -> None:
    sol = private_root / "solutions" / "linked-list-insertion"
    ht = private_root / "hidden-tests" / "linked-list-insertion"
    gr = private_root / "grader" / "linked-list-insertion"
    out = cmd_package_private(
        "linked-list-insertion",
        solution=sol, hidden_tests=ht, grader=gr,
        output_dir=tmp_path, public_root=public_root,
    )
    with tarfile.open(out, "r:gz") as tar:
        f = tar.extractfile("linked-list-insertion/package-manifest.json")
        data = json.loads(f.read())
    assert data["assignment_slug"] == "linked-list-insertion"
    assert data["contains_grader"] is True


def test_package_private_fails_without_pipeline(public_root: Path, tmp_path: Path) -> None:
    sol = tmp_path / "solution"
    sol.mkdir()
    gr = tmp_path / "grader"
    gr.mkdir()
    with pytest.raises(typer.Exit):
        cmd_package_private(
            "linked-list-insertion",
            solution=sol, grader=gr,
            output_dir=tmp_path, public_root=public_root,
        )


import typer  # noqa: E402
