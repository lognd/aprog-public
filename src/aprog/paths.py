"""Single home for the aprog-public/aprog-private repo layout.

Every command that needs to know where an assignment's public or private
files live should call one of these helpers instead of hardcoding the path
string -- that way the layout only has to be documented, and changed, in one
place.

Public layout (rooted at the aprog-public repo):
    assignments/<slug>/
    generated/assignments/<slug>/
    templates/<template_slug>/
    dist/

Private layout (rooted at the aprog-private repo):
    grader/<slug>/
    grader/<slug>/pipeline.py
    grader/<slug>/hidden-tests/          (preferred hidden-tests location)
    hidden-tests/<slug>/                 (sibling location, also supported)
    solutions/assignments/<slug>/        (canonical solution storage)
    solutions/<slug>/                    (legacy fallback)
    generated/assignments/<slug>/
"""

from __future__ import annotations

from pathlib import Path

# -- public repo paths ---------------------------------------------------------


def assignment_dir(public_root: Path, slug: str) -> Path:
    """Public assignment source directory."""
    return public_root / "assignments" / slug


def generated_assignment_dir(root: Path, slug: str) -> Path:
    """Generated-artifacts directory, valid under either the public or private root."""
    return root / "generated" / "assignments" / slug


def template_dir(public_root: Path, template_slug: str) -> Path:
    """Template source directory."""
    return public_root / "templates" / template_slug


def dist_dir(public_root: Path) -> Path:
    """Directory packaged bundles (zips/tarballs) are written to."""
    return public_root / "dist"


# -- private repo paths ---------------------------------------------------------


def grader_dir(private_root: Path, slug: str) -> Path:
    """Private grader directory for an assignment."""
    return private_root / "grader" / slug


def grader_pipeline_file(private_root: Path, slug: str) -> Path:
    """Path to the grader's `pipeline.py` entry point."""
    return grader_dir(private_root, slug) / "pipeline.py"


def grader_hidden_tests_dir(private_root: Path, slug: str) -> Path:
    """Preferred hidden-tests location: embedded inside the grader directory."""
    return grader_dir(private_root, slug) / "hidden-tests"


def sibling_hidden_tests_dir(private_root: Path, slug: str) -> Path:
    """Sibling hidden-tests location, packaged alongside (not inside) the grader dir."""
    return private_root / "hidden-tests" / slug


def solution_dir(private_root: Path, slug: str) -> Path:
    """Canonical solution directory; falls back to the legacy flat layout.

    Canonical storage is `solutions/assignments/<slug>`. Older private repos
    may still use the flat `solutions/<slug>` layout, so that path is used if
    the canonical one does not exist.
    """
    canonical = private_root / "solutions" / "assignments" / slug
    if canonical.exists():
        return canonical
    return private_root / "solutions" / slug
