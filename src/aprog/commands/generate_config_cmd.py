from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from aprog.models.assignment import AssignmentConfig
from aprog.models.manifest import (
    AssignmentManifest,
    ManifestAssignment,
    ManifestClassification,
    ManifestPaths,
    ManifestTemplate,
    PrivateManifest,
)
from aprog.utils.hashing import hash_assignment_public
from aprog.utils.repo import (
    all_assignment_slugs,
    find_public_root,
    load_assignment_config,
)

console = Console()

_RUN_AUTOGRADER_PY_TEMPLATE = """\
import json
import sys
import traceback
from pathlib import Path

# /autograder/source/ is the extracted zip root; grader/pipeline.py lives there.
_SOURCE = Path("/autograder/source")
sys.path.insert(0, str(_SOURCE))

from lograder.pipeline.config import config
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.score import GradescopeConfig

from grader.pipeline import make_pipeline

_RESULTS = Path("/autograder/results/results.json")

if __name__ == "__main__":
    try:
        metadata = GraderMetadata.from_gradescope(
            grader_name={assignment_name!r},
            authors=[StaffAuthor(name={assignment_author!r}, role="Instructor")],
            notes="Contact course staff within 3 days if you believe there is a grading error.",
        )
        import inspect as _inspect
        _sig = _inspect.signature(make_pipeline)
        _kwargs = {{"submission_dir": Path("/autograder/submission")}} if "submission_dir" in _sig.parameters else {{}}
        with config(root_directory=Path("/autograder")):
            pipeline = make_pipeline(**_kwargs)
            score = pipeline(metadata=metadata)
            score.write_results_json(
                config=GradescopeConfig(
                    visibility={visibility!r},
                    stdout_visibility={stdout_visibility!r},
                )
            )
    except Exception:
        # Always write results.json so Gradescope receives a structured response
        # instead of a blank "no results" error.
        _RESULTS.parent.mkdir(parents=True, exist_ok=True)
        _RESULTS.write_text(
            json.dumps({{
                "score": 0,
                "output": "Autograder error:\\n\\n" + traceback.format_exc(),
            }}),
            encoding="utf-8",
        )
        sys.exit(1)
"""

_RUN_AUTOGRADER_SH = """\
#!/usr/bin/env bash
# run_autograder is copied to /autograder/run_autograder during the Docker
# image build, while the rest of the zip is extracted to /autograder/source/.
# Reference run_autograder.py by its known absolute path.
exec python3 /autograder/source/run_autograder.py "$@"
"""

_GENERATOR_VERSION = "0.1"


def cmd_generate_config(
    slug: str,
    private_repo: Optional[Path] = None,
    force: bool = False,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()

    try:
        cfg = load_assignment_config(root, slug)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    gen_dir = root / "generated" / "assignments" / slug
    manifest_path = gen_dir / "assignment-manifest.json"
    autograder_py = gen_dir / "run_autograder.py"
    autograder_sh = gen_dir / "run_autograder"

    source_hash = hash_assignment_public(
        root, slug, generator_version=_GENERATOR_VERSION
    )

    # Check if regeneration is needed
    if manifest_path.exists() and not force:
        try:
            existing = json.loads(manifest_path.read_text())
            if existing.get("source_hash") == source_hash:
                console.print(
                    f"[dim]Generated files for '{slug}' are current. Use --force to regenerate.[/dim]"
                )
                return
        except Exception:
            pass

    gen_dir.mkdir(parents=True, exist_ok=True)

    a = cfg.assignment
    c = cfg.classification
    t = cfg.template

    manifest = AssignmentManifest(
        assignment=ManifestAssignment(
            slug=a.slug,
            name=a.name,
            author=a.author,
            description=a.description,
        ),
        classification=ManifestClassification(
            language=c.language,
            difficulty=c.difficulty,
            topics=c.topics,
            course=c.course,
        ),
        template=ManifestTemplate(slug=t.slug, version=t.version),
        paths=ManifestPaths(
            assignment_root=f"assignments/{slug}",
            readme=f"assignments/{slug}/README.md",
            visible_tests=f"assignments/{slug}/visible-tests",
        ),
        state=a.status,
        source_hash=source_hash,
    )

    manifest_path.write_text(json.dumps(manifest.model_dump(), indent=2) + "\n")

    autograder_py.write_text(
        _RUN_AUTOGRADER_PY_TEMPLATE.format(
            assignment_name=cfg.assignment.name,
            assignment_author=cfg.assignment.author or "Course Staff",
            visibility=cfg.grader.visibility,
            stdout_visibility=cfg.grader.stdout_visibility,
        )
    )

    autograder_sh.write_text(_RUN_AUTOGRADER_SH)
    autograder_sh.chmod(0o755)

    console.print(f"[green][OK][/green] Generated configs for '{slug}':")
    console.print(f"  {manifest_path.relative_to(root)}")
    console.print(f"  {autograder_py.relative_to(root)}")
    console.print(f"  {autograder_sh.relative_to(root)}")

    if private_repo:
        _generate_private(root, private_repo, slug, cfg, source_hash)


def _generate_private(
    public_root: Path,
    private_repo: Path,
    slug: str,
    cfg: "AssignmentConfig",
    public_hash: str,
) -> None:
    import hashlib

    gen_dir = private_repo / "generated" / "assignments" / slug
    gen_dir.mkdir(parents=True, exist_ok=True)

    sol_dir = private_repo / "solutions" / slug
    ht_dir = private_repo / "hidden-tests" / slug
    gr_dir = private_repo / "grader" / slug

    has_solution = sol_dir.exists()
    has_hidden_tests = ht_dir.exists()

    # Private source hash: extend public hash with private files
    h = hashlib.sha256()
    h.update(public_hash.encode())
    for d in [sol_dir, ht_dir, gr_dir]:
        if d.exists():
            for p in sorted(d.rglob("*")):
                if p.is_file():
                    h.update(str(p.relative_to(private_repo)).encode())
                    h.update(p.read_bytes())
    private_hash = f"sha256:{h.hexdigest()}"

    private_manifest = PrivateManifest(
        assignment_slug=slug,
        solution_path=f"solutions/{slug}",
        hidden_tests_path=f"hidden-tests/{slug}",
        grader_path=f"grader/{slug}",
        has_solution=has_solution,
        has_hidden_tests=has_hidden_tests,
        private_source_hash=private_hash,
        verification_state="unverified",
    )

    (gen_dir / "private-assignment-manifest.json").write_text(
        json.dumps(private_manifest.model_dump(), indent=2) + "\n"
    )

    vc_path = gen_dir / "verification-config.json"
    existing_state = "unverified"
    if vc_path.exists():
        try:
            existing = json.loads(vc_path.read_text())
            if existing.get("private_source_hash") == private_hash:
                existing_state = existing.get("verification_state", "unverified")
        except Exception:
            pass

    verification_config = {
        "schema_version": "0.1",
        "assignment_slug": slug,
        "solution_path": f"solutions/{slug}",
        "hidden_tests_path": f"hidden-tests/{slug}",
        "grader_path": f"grader/{slug}",
        "has_solution": has_solution,
        "has_hidden_tests": has_hidden_tests,
        "private_source_hash": private_hash,
        "verification_state": existing_state,
    }
    vc_path.write_text(json.dumps(verification_config, indent=2) + "\n")

    console.print(
        f"  {(gen_dir / 'private-assignment-manifest.json').relative_to(private_repo)} (private)"
    )
    console.print(f"  {vc_path.relative_to(private_repo)} (private)")


def cmd_generate_config_all(
    private_repo: Optional[Path] = None,
    force: bool = False,
    public_root: Optional[Path] = None,
) -> None:
    root = public_root or find_public_root()
    for slug in all_assignment_slugs(root):
        cmd_generate_config(
            slug, private_repo=private_repo, force=force, public_root=root
        )
