# mypy: ignore-errors
from __future__ import annotations

import json
from pathlib import Path

import pytest

from aprog.commands.generate_config_cmd import cmd_generate_config
from aprog.utils.hashing import hash_assignment_public


def test_generate_config_creates_manifest(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    manifest = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "assignment-manifest.json"
    )
    assert manifest.exists()


def test_generate_config_creates_run_autograder_py(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    py = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "run_autograder.py"
    )
    assert py.exists()
    content = py.read_text()
    assert "make_pipeline" in content
    assert "write_results_json" in content


def test_generate_config_creates_run_autograder_sh(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    sh = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "run_autograder"
    )
    assert sh.exists()
    assert sh.stat().st_mode & 0o111  # executable bit


def test_manifest_contains_source_hash(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    manifest_path = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "assignment-manifest.json"
    )
    data = json.loads(manifest_path.read_text())
    assert data["source_hash"].startswith("sha256:")


def test_manifest_hash_matches_computed(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    manifest_path = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "assignment-manifest.json"
    )
    data = json.loads(manifest_path.read_text())
    expected = hash_assignment_public(public_root, "linked-list-insertion")
    assert data["source_hash"] == expected


def test_generate_config_skips_when_current(public_root: Path, capsys) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    out = capsys.readouterr().out
    assert "current" in out


def test_generate_config_force_regenerates(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    manifest_path = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "assignment-manifest.json"
    )
    mtime1 = manifest_path.stat().st_mtime
    import time

    time.sleep(0.01)
    cmd_generate_config("linked-list-insertion", force=True, public_root=public_root)
    mtime2 = manifest_path.stat().st_mtime
    assert mtime2 >= mtime1


def test_manifest_slug_matches(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    manifest_path = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "assignment-manifest.json"
    )
    data = json.loads(manifest_path.read_text())
    assert data["assignment"]["slug"] == "linked-list-insertion"


def test_run_autograder_py_uses_grader_visibility(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    py = (
        public_root
        / "generated"
        / "assignments"
        / "linked-list-insertion"
        / "run_autograder.py"
    )
    content = py.read_text()
    assert "after_due_date" in content
