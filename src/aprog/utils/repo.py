from __future__ import annotations

import os
from pathlib import Path

from aprog.models.assignment import AssignmentConfig
from aprog.models.root_config import RootConfig
from aprog.models.template import TemplateConfig
from aprog.paths import assignment_dir, template_dir
from aprog.utils.toml import load_toml


def find_public_root(start: Path | None = None) -> Path:
    """Walk up from start looking for aprog.toml."""
    candidate = (start or Path.cwd()).resolve()
    for directory in [candidate, *candidate.parents]:
        if (directory / "aprog.toml").exists():
            return directory
    raise FileNotFoundError(
        "Could not find aprog.toml. Are you inside an aprog-public repository?"
    )


def load_root_config(public_root: Path) -> RootConfig:
    data = load_toml(public_root / "aprog.toml")
    return RootConfig.model_validate(data)


def load_assignment_config(public_root: Path, slug: str) -> AssignmentConfig:
    path = assignment_dir(public_root, slug) / "assignment.toml"
    if not path.exists():
        raise FileNotFoundError(
            f"Assignment not found: assignments/{slug}/assignment.toml"
        )
    data = load_toml(path)
    return AssignmentConfig.model_validate(data)


def load_template_config(public_root: Path, template_slug: str) -> TemplateConfig:
    path = template_dir(public_root, template_slug) / "template.toml"
    if not path.exists():
        raise FileNotFoundError(
            f"Template not found: templates/{template_slug}/template.toml"
        )
    data = load_toml(path)
    return TemplateConfig.model_validate(data)


def all_assignment_slugs(public_root: Path) -> list[str]:
    assignments_dir = public_root / "assignments"
    if not assignments_dir.exists():
        return []
    return sorted(
        d.name
        for d in assignments_dir.iterdir()
        if d.is_dir() and (d / "assignment.toml").exists()
    )


def resolve_staging_dir(staging_flag: Path | None) -> Path | None:
    if staging_flag:
        return staging_flag.resolve()
    env = os.environ.get("APROG_STAGING_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return None
