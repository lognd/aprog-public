# mypy: ignore-errors
from __future__ import annotations

from pathlib import Path

import pytest
import typer

from aprog.commands.new_cmd import cmd_new


def test_new_creates_assignment_toml(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    assert (public_root / "assignments" / "my-assignment" / "assignment.toml").exists()


def test_new_creates_readme(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    assert (public_root / "assignments" / "my-assignment" / "README.md").exists()


def test_new_creates_visible_tests(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    assert (public_root / "assignments" / "my-assignment" / "visible-tests").is_dir()


def test_new_creates_private_staging(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    assert (staging / "my-assignment" / "grader" / "pipeline.py").exists()


def test_new_pipeline_scaffold_has_make_pipeline(
    public_root: Path, tmp_path: Path
) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    content = (staging / "my-assignment" / "grader" / "pipeline.py").read_text()
    assert "make_pipeline" in content


def test_new_rejects_invalid_slug(public_root: Path, tmp_path: Path) -> None:
    with pytest.raises(typer.Exit):
        cmd_new(
            "MyAssignment",
            template="python-stdin-stdout",
            staging_dir=tmp_path / "s",
            public_root=public_root,
        )


def test_new_refuses_overwrite_without_force(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    with pytest.raises(typer.Exit):
        cmd_new(
            "my-assignment",
            template="python-stdin-stdout",
            staging_dir=staging,
            public_root=public_root,
        )


def test_new_force_overwrites(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        force=True,
        public_root=public_root,
    )
    assert (public_root / "assignments" / "my-assignment" / "assignment.toml").exists()


def test_new_assignment_toml_contains_slug(public_root: Path, tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    cmd_new(
        "my-assignment",
        template="python-stdin-stdout",
        staging_dir=staging,
        public_root=public_root,
    )
    content = (
        public_root / "assignments" / "my-assignment" / "assignment.toml"
    ).read_text()
    assert 'slug = "my-assignment"' in content
