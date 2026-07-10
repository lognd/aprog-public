"""Content hashing shared by generate-config, validate, and check-generated.

All source-hash computation funnels through `hash_paths` so there is exactly
one sorted-rglob-and-hash implementation instead of three near-identical
copies.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from aprog.paths import assignment_dir, template_dir


def hash_file(path: Path) -> str:
    """Hash a single file's contents (no path/name mixed in)."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def hash_paths(paths: list[Path], root: Path | None = None, extra: str = "") -> str:
    """Hash a set of paths deterministically: sorted, relative names (if `root`
    is given) plus file contents, plus an optional `extra` marker (e.g. a
    generator version) appended last so a version bump always invalidates
    the hash."""
    h = hashlib.sha256()
    for p in sorted(paths):
        name = str(p.relative_to(root)) if root else str(p)
        h.update(name.encode())
        if p.is_file():
            h.update(p.read_bytes())
    if extra:
        h.update(extra.encode())
    return f"sha256:{h.hexdigest()}"


def hash_assignment_public(public_root: Path, slug: str, generator_version: str) -> str:
    """Source hash for a public assignment: aprog.toml + assignment tree + the
    referenced template's template.toml, versioned by `generator_version` so
    that regenerating the output format invalidates every stored hash."""
    paths: list[Path] = []
    aprog_toml = public_root / "aprog.toml"
    if aprog_toml.exists():
        paths.append(aprog_toml)
    assignment_root = assignment_dir(public_root, slug)
    if assignment_root.exists():
        paths.extend(p for p in assignment_root.rglob("*") if p.is_file())
    template_section = _get_template_slug(public_root, slug)
    if template_section:
        tpl_toml = template_dir(public_root, template_section) / "template.toml"
        if tpl_toml.exists():
            paths.append(tpl_toml)
    return hash_paths(paths, root=public_root, extra=generator_version)


def _get_template_slug(public_root: Path, slug: str) -> str | None:
    """Read the `[template].slug` an assignment references, or None if unreadable."""
    from aprog.utils.repo import load_assignment_config

    try:
        return load_assignment_config(public_root, slug).template.slug
    except Exception:
        return None
