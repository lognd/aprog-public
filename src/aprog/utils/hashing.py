from __future__ import annotations

import hashlib
from pathlib import Path


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def hash_paths(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(str(p).encode())
        if p.is_file():
            h.update(p.read_bytes())
    return f"sha256:{h.hexdigest()}"


def hash_assignment_public(
    public_root: Path, slug: str, generator_version: str = "0.1"
) -> str:
    paths: list[Path] = []
    aprog_toml = public_root / "aprog.toml"
    if aprog_toml.exists():
        paths.append(aprog_toml)
    assignment_root = public_root / "assignments" / slug
    if assignment_root.exists():
        paths.extend(p for p in assignment_root.rglob("*") if p.is_file())
    template_section = _get_template_slug(public_root, slug)
    if template_section:
        tpl_root = public_root / "templates" / template_section
        tpl_toml = tpl_root / "template.toml"
        if tpl_toml.exists():
            paths.append(tpl_toml)
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(str(p).encode())
        if p.is_file():
            h.update(p.read_bytes())
    h.update(generator_version.encode())
    return f"sha256:{h.hexdigest()}"


def _get_template_slug(public_root: Path, slug: str) -> str | None:
    from aprog.utils.toml import load_toml

    assignment_toml = public_root / "assignments" / slug / "assignment.toml"
    if not assignment_toml.exists():
        return None
    try:
        data = load_toml(assignment_toml)
        tpl = data.get("template")
        if isinstance(tpl, dict):
            val = tpl.get("slug")
            if isinstance(val, str):
                return val
        return None
    except Exception:
        return None
