# mypy: ignore-errors
from __future__ import annotations

from pathlib import Path

import pytest

from aprog.commands.generate_config_cmd import cmd_generate_config
from aprog.commands.validate_cmd import cmd_validate


def test_validate_passes_after_generate(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code == 0


def test_validate_fails_without_generated_files(public_root: Path) -> None:
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0


def test_validate_fails_unknown_language(public_root: Path) -> None:
    toml = public_root / "assignments" / "linked-list-insertion" / "assignment.toml"
    toml.write_text(
        toml.read_text().replace('language = "python"', 'language = "cobol"')
    )
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0


def test_validate_fails_missing_readme(public_root: Path) -> None:
    readme = public_root / "assignments" / "linked-list-insertion" / "README.md"
    readme.unlink()
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0


def test_validate_fails_missing_visible_tests(public_root: Path) -> None:
    import shutil

    vt = public_root / "assignments" / "linked-list-insertion" / "visible-tests"
    shutil.rmtree(vt)
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0


def test_validate_fails_on_boundary_violation(public_root: Path) -> None:
    (public_root / "assignments" / "linked-list-insertion" / "solution.py").touch()
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0


def test_validate_fails_slug_mismatch(public_root: Path) -> None:
    toml = public_root / "assignments" / "linked-list-insertion" / "assignment.toml"
    toml.write_text(
        toml.read_text().replace(
            'slug = "linked-list-insertion"', 'slug = "different-slug"'
        )
    )
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0


def test_validate_fails_stale_generated(public_root: Path) -> None:
    cmd_generate_config("linked-list-insertion", public_root=public_root)
    # Modify source after generating
    readme = public_root / "assignments" / "linked-list-insertion" / "README.md"
    readme.write_text("# Modified\n")
    code = cmd_validate("linked-list-insertion", public_root=public_root)
    assert code != 0
