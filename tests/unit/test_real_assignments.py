# mypy: ignore-errors
"""
Validates that every committed assignment in assignments/ parses cleanly
and passes structural checks. Catches regressions when assignment.toml or
aprog.toml are edited without running `aprog validate`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_PUBLIC_ROOT = Path(__file__).resolve().parents[2]
_ASSIGNMENTS_DIR = _PUBLIC_ROOT / "assignments"


def _all_slugs() -> list[str]:
    if not _ASSIGNMENTS_DIR.exists():
        return []
    return sorted(
        d.name
        for d in _ASSIGNMENTS_DIR.iterdir()
        if d.is_dir() and (d / "assignment.toml").exists()
    )


@pytest.mark.parametrize("slug", _all_slugs())
def test_assignment_config_parses(slug: str) -> None:
    from aprog.utils.repo import load_assignment_config

    cfg = load_assignment_config(_PUBLIC_ROOT, slug)
    assert cfg.assignment.slug == slug


@pytest.mark.parametrize("slug", _all_slugs())
def test_assignment_validates_against_root_config(slug: str) -> None:
    from aprog.commands.validate_cmd import cmd_validate

    code = cmd_validate(slug, public_root=_PUBLIC_ROOT)
    assert code in (0, 4), f"{slug}: validation failed (code {code})"


@pytest.mark.parametrize("slug", _all_slugs())
def test_no_private_content_in_public(slug: str) -> None:
    from aprog.commands.validate_cmd import _scan_public_violations

    violations = _scan_public_violations(_ASSIGNMENTS_DIR / slug)
    assert violations == [], f"{slug}: public/private boundary violations: {violations}"
