from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional

import typer
from jinja2 import Template
from rich.console import Console

from aprog.constants import GENERATOR_VERSION
from aprog.models.assignment import AssignmentConfig
from aprog.models.manifest import (
    AssignmentManifest,
    ManifestAssignment,
    ManifestClassification,
    ManifestPaths,
    ManifestTemplate,
    PrivateManifest,
)
from aprog.paths import (
    generated_assignment_dir,
    grader_dir,
    sibling_hidden_tests_dir,
    solution_dir,
)
from aprog.utils.hashing import hash_assignment_public, hash_paths
from aprog.utils.repo import (
    all_assignment_slugs,
    find_public_root,
    load_assignment_config,
)

console = Console()

# Jinja renders the templated values (reprs computed in Python so the quoting
# style matches exactly what the old str.format(...!r) call produced); the
# literal Python dict/set braces in the exception handler are wrapped in
# {% raw %} so Jinja does not try to parse them as expressions.
_RUN_AUTOGRADER_PY_TEMPLATE = Template(
    """\
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
            grader_name={{ assignment_name_repr }},
            authors=[StaffAuthor(name={{ assignment_author_repr }}, role="Instructor")],
            notes="Contact course staff within 3 days if you believe there is a grading error.",
        )
        import inspect as _inspect
        _sig = _inspect.signature(make_pipeline)
        {% raw %}_kwargs = {"submission_dir": Path("/autograder/submission")} if "submission_dir" in _sig.parameters else {}{% endraw %}
        with config(root_directory=Path("/autograder")):
            pipeline = make_pipeline(**_kwargs)
            score = pipeline(metadata=metadata)
            score.write_results_json(
                config=GradescopeConfig(
                    visibility={{ visibility_repr }},
                    stdout_visibility={{ stdout_visibility_repr }},
                )
            )
    except Exception:
        # Always write results.json so Gradescope receives a structured response
        # instead of a blank "no results" error.
        _RESULTS.parent.mkdir(parents=True, exist_ok=True)
        {% raw %}_RESULTS.write_text(
            json.dumps({
                "score": 0,
                "output": "Autograder error:\\n\\n" + traceback.format_exc(),
            }),
            encoding="utf-8",
        ){% endraw %}
        sys.exit(1)
"""
)

_RUN_AUTOGRADER_SH = """\
#!/usr/bin/env bash
# run_autograder is copied to /autograder/run_autograder during the Docker
# image build, while the rest of the zip is extracted to /autograder/source/.
# Reference run_autograder.py by its known absolute path.
exec python3 /autograder/source/run_autograder.py "$@"
"""


def _git_mark_executable(path: Path) -> None:
    """Force git to track the file as executable (works even with core.fileMode=false)."""
    try:
        subprocess.run(
            ["git", "update-index", "--chmod=+x", str(path)],
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # not a git repo or git unavailable -- chmod already set above


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

    gen_dir = generated_assignment_dir(root, slug)
    manifest_path = gen_dir / "assignment-manifest.json"
    autograder_py = gen_dir / "run_autograder.py"
    autograder_sh = gen_dir / "run_autograder"

    source_hash = hash_assignment_public(root, slug, GENERATOR_VERSION)

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
        _RUN_AUTOGRADER_PY_TEMPLATE.render(
            assignment_name_repr=repr(cfg.assignment.name),
            assignment_author_repr=repr(cfg.assignment.author or "Course Staff"),
            visibility_repr=repr(cfg.grader.visibility),
            stdout_visibility_repr=repr(cfg.grader.stdout_visibility),
        )
    )

    autograder_sh.write_text(_RUN_AUTOGRADER_SH)
    autograder_sh.chmod(0o755)
    _git_mark_executable(autograder_sh)

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
    gen_dir = generated_assignment_dir(private_repo, slug)
    gen_dir.mkdir(parents=True, exist_ok=True)

    sol_dir = solution_dir(private_repo, slug)
    ht_dir = sibling_hidden_tests_dir(private_repo, slug)
    gr_dir = grader_dir(private_repo, slug)

    has_solution = sol_dir.exists()
    has_hidden_tests = ht_dir.exists() or (gr_dir / "hidden-tests").exists()

    # Private source hash: extend the public hash with every private file's
    # name and contents.
    private_files = [
        p
        for d in (sol_dir, ht_dir, gr_dir)
        if d.exists()
        for p in d.rglob("*")
        if p.is_file()
    ]
    private_hash = hash_paths(private_files, root=private_repo, extra=public_hash)

    private_manifest = PrivateManifest(
        assignment_slug=slug,
        solution_path=str(sol_dir.relative_to(private_repo)),
        hidden_tests_path=str(ht_dir.relative_to(private_repo)),
        grader_path=str(gr_dir.relative_to(private_repo)),
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

    # Derive the verification config from the manifest model itself (rather
    # than hand-building a near-identical dict) so the model stays the single
    # source of truth for this shape.
    verification_config = private_manifest.model_dump()
    verification_config["verification_state"] = existing_state
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
