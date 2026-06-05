# mypy: ignore-errors
from __future__ import annotations

from pathlib import Path

import pytest
import typer

from aprog.commands.intake_cmd import cmd_intake
from aprog.commands.package_cmd import cmd_package_private


def _make_bundle(public_root: Path, private_root: Path, tmp_path: Path) -> Path:
    sol = private_root / "solutions" / "linked-list-insertion"
    ht = private_root / "hidden-tests" / "linked-list-insertion"
    gr = private_root / "grader" / "linked-list-insertion"
    return cmd_package_private(
        "linked-list-insertion",
        solution=sol,
        hidden_tests=ht,
        grader=gr,
        output_dir=tmp_path / "dist",
        public_root=public_root,
    )


def test_intake_copies_solution(
    public_root: Path, private_root: Path, tmp_path: Path
) -> None:
    bundle = _make_bundle(public_root, private_root, tmp_path)
    dest_private = tmp_path / "private"
    cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)
    assert (dest_private / "solutions" / "linked-list-insertion").exists()


def test_intake_copies_grader(
    public_root: Path, private_root: Path, tmp_path: Path
) -> None:
    bundle = _make_bundle(public_root, private_root, tmp_path)
    dest_private = tmp_path / "private"
    cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)
    assert (dest_private / "grader" / "linked-list-insertion" / "pipeline.py").exists()


def test_intake_copies_hidden_tests(
    public_root: Path, private_root: Path, tmp_path: Path
) -> None:
    bundle = _make_bundle(public_root, private_root, tmp_path)
    dest_private = tmp_path / "private"
    cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)
    assert (dest_private / "hidden-tests" / "linked-list-insertion").exists()


def test_intake_refuses_overwrite_without_force(
    public_root: Path, private_root: Path, tmp_path: Path
) -> None:
    bundle = _make_bundle(public_root, private_root, tmp_path)
    dest_private = tmp_path / "private"
    cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)
    with pytest.raises(typer.Exit):
        cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)


def test_intake_force_overwrites(
    public_root: Path, private_root: Path, tmp_path: Path
) -> None:
    bundle = _make_bundle(public_root, private_root, tmp_path)
    dest_private = tmp_path / "private"
    cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)
    cmd_intake(bundle, public_repo=public_root, private_repo=dest_private, force=True)
    assert (dest_private / "grader" / "linked-list-insertion" / "pipeline.py").exists()


def test_intake_rejects_missing_bundle(public_root: Path, tmp_path: Path) -> None:
    with pytest.raises(typer.Exit):
        cmd_intake(
            tmp_path / "nonexistent.tar.gz",
            public_repo=public_root,
            private_repo=tmp_path / "priv",
        )


def test_intake_rejects_unknown_assignment(
    public_root: Path, private_root: Path, tmp_path: Path
) -> None:
    bundle = _make_bundle(public_root, private_root, tmp_path)
    # Remove the assignment from the public repo to simulate unknown slug
    import shutil

    shutil.rmtree(public_root / "assignments" / "linked-list-insertion")
    dest_private = tmp_path / "private"
    with pytest.raises(typer.Exit):
        cmd_intake(bundle, public_repo=public_root, private_repo=dest_private)
