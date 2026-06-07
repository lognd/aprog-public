# mypy: ignore-errors
"""
Integration tests for all examples in examples/.

Fast tests (test_make_pipeline_constructs):
  Import each pipeline module and call make_pipeline() to verify it constructs
  without error. No filesystem setup; no compilation.

Slow tests (test_pipeline_passes_with_solution):
  Run each pipeline against the included reference solution and assert that all
  required test cases pass. Requires a compiler / Python / make depending on the
  example. Skip examples where prerequisite tooling is unavailable.
"""

from __future__ import annotations

import importlib.util
import shutil
import sys
import types
from pathlib import Path

import pytest
from lograder.pipeline.config import config
from lograder.pipeline.pipeline import Pipeline

_PUBLIC_ROOT = Path(__file__).resolve().parents[2]
_DEMOS_DIR = _PUBLIC_ROOT / "examples" / "template-demos"
_ASSIGNMENTS_DIR = _PUBLIC_ROOT / "examples" / "assignments"

# ---------------------------------------------------------------------------
# Module loading helpers
# ---------------------------------------------------------------------------


def _load_module(pipeline_py: Path, name: str) -> types.ModuleType:
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, pipeline_py)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _module_name(slug: str) -> str:
    return f"_test_example_{slug.replace('-', '_')}"


# ---------------------------------------------------------------------------
# Example registry
# ---------------------------------------------------------------------------

_DEMO_SLUGS: list[str] = sorted(
    d.name.removesuffix("-staging")
    for d in _DEMOS_DIR.iterdir()
    if d.is_dir() and d.name.endswith("-staging")
)

_ALL_SLUGS: list[str] = _DEMO_SLUGS + ["cpp-linked-list"]


def _pipeline_py(slug: str) -> Path:
    if slug == "cpp-linked-list":
        return _ASSIGNMENTS_DIR / "cpp-linked-list" / "grader" / "pipeline.py"
    return _DEMOS_DIR / f"{slug}-staging" / "grader" / "pipeline.py"


# ---------------------------------------------------------------------------
# Fast tests: import + construct only
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("slug", _ALL_SLUGS)
def test_make_pipeline_constructs(slug: str, tmp_path: Path) -> None:
    mod = _load_module(_pipeline_py(slug), _module_name(slug))
    pipeline = mod.make_pipeline(tmp_path / "submission")
    assert isinstance(pipeline, Pipeline)


# ---------------------------------------------------------------------------
# Slow test helpers
# ---------------------------------------------------------------------------


def _copy_tree(src: Path, dst: Path) -> None:
    """Copy an entire directory tree to dst (dst is created if needed)."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _run_pipeline(
    slug: str,
    module_name: str,
    pipeline_py: Path,
    submission_dir: Path,
    root_dir: Path,
    grader_dir_override: Path | None = None,
) -> None:
    """Load module, optionally patch _GRADER_DIR, run pipeline, assert passing."""
    mod = _load_module(pipeline_py, module_name)
    if grader_dir_override is not None:
        mod._GRADER_DIR = grader_dir_override
    pipeline = mod.make_pipeline(submission_dir)
    with config(root_directory=root_dir, executable_timeout=300.0):
        score = pipeline()
    total = score.total()
    assert total.earned >= total.possible, (
        f"{slug}: earned {total.earned} < possible {total.possible}"
    )


# ---------------------------------------------------------------------------
# Slow tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
def test_pipeline_add_two_numbers(tmp_path: Path) -> None:
    slug = "add-two-numbers"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(
        _DEMOS_DIR / f"{slug}-staging" / "solution" / "solution.py",
        submission / f"{slug}.py",
    )
    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=_pipeline_py(slug),
        submission_dir=submission,
        root_dir=tmp_path,
    )


@pytest.mark.slow
def test_pipeline_binary_search(tmp_path: Path) -> None:
    slug = "binary-search"
    staging = _DEMOS_DIR / f"{slug}-staging"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "solution.py", submission / f"{slug}.py")
    grader_tmp = tmp_path / "grader"
    shutil.copy2(staging / "grader" / "pipeline.py", tmp_path)
    _copy_tree(staging / "hidden-tests", grader_tmp / "hidden-tests")
    (grader_tmp).mkdir(exist_ok=True)
    shutil.copy2(staging / "grader" / "pipeline.py", grader_tmp / "pipeline.py")

    mod = _load_module(grader_tmp / "pipeline.py", _module_name(slug))
    mod._GRADER_DIR = grader_tmp
    mod._HIDDEN_TESTS = grader_tmp / "hidden-tests"
    pipeline = mod.make_pipeline(submission)
    with config(root_directory=tmp_path, executable_timeout=60.0):
        score = pipeline()
    total = score.total()
    assert total.earned >= total.possible


@pytest.mark.slow
def test_pipeline_stack_adt(tmp_path: Path) -> None:
    slug = "stack-adt"
    staging = _DEMOS_DIR / f"{slug}-staging"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "solution.py", submission / f"{slug}.py")

    grader_tmp = tmp_path / "grader"
    grader_tmp.mkdir()
    shutil.copy2(staging / "grader" / "pipeline.py", grader_tmp / "pipeline.py")
    _copy_tree(staging / "hidden-tests", grader_tmp / "hidden-tests")

    mod = _load_module(grader_tmp / "pipeline.py", _module_name(slug))
    mod._GRADER_DIR = grader_tmp
    pipeline = mod.make_pipeline(submission)
    with config(root_directory=tmp_path, executable_timeout=60.0):
        score = pipeline()
    total = score.total()
    assert total.earned >= total.possible


@pytest.mark.slow
def test_pipeline_caesar_cipher(tmp_path: Path) -> None:
    slug = "caesar-cipher"
    staging = _DEMOS_DIR / f"{slug}-staging"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "solution.c", submission / f"{slug}.c")

    grader_tmp = tmp_path / "grader"
    _copy_tree(staging / "grader", grader_tmp)

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=grader_tmp / "pipeline.py",
        submission_dir=submission,
        root_dir=tmp_path,
        grader_dir_override=grader_tmp,
    )


@pytest.mark.slow
def test_pipeline_cpp_bst(tmp_path: Path) -> None:
    slug = "cpp-bst"
    staging = _DEMOS_DIR / f"{slug}-staging"
    public = _DEMOS_DIR / f"{slug}-public"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "solution.hpp", submission / f"{slug}.hpp")

    grader_tmp = tmp_path / "grader"
    _copy_tree(staging / "grader", grader_tmp)
    _copy_tree(public / "visible-tests", grader_tmp / "visible-tests")
    _copy_tree(staging / "hidden-tests", grader_tmp / "hidden-tests")

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=grader_tmp / "pipeline.py",
        submission_dir=submission,
        root_dir=tmp_path,
        grader_dir_override=grader_tmp,
    )


@pytest.mark.slow
def test_pipeline_graph_search(tmp_path: Path) -> None:
    slug = "graph-search"
    staging = _DEMOS_DIR / f"{slug}-staging"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "CMakeLists.txt", submission / "CMakeLists.txt")
    shutil.copy2(staging / "solution" / "main.cpp", submission / "main.cpp")

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=_pipeline_py(slug),
        submission_dir=submission,
        root_dir=tmp_path,
    )


@pytest.mark.slow
def test_pipeline_matrix_class(tmp_path: Path) -> None:
    slug = "matrix-class"
    staging = _DEMOS_DIR / f"{slug}-staging"
    public = _DEMOS_DIR / f"{slug}-public"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "solution.hpp", submission / f"{slug}.hpp")
    shutil.copy2(staging / "solution" / "solution.cpp", submission / f"{slug}.cpp")

    grader_tmp = tmp_path / "grader"
    _copy_tree(staging / "grader", grader_tmp)
    _copy_tree(staging / "hidden-tests", grader_tmp / "hidden-tests")
    _copy_tree(public / "visible-tests", grader_tmp / "visible-tests")

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=grader_tmp / "pipeline.py",
        submission_dir=submission,
        root_dir=tmp_path,
        grader_dir_override=grader_tmp,
    )


@pytest.mark.slow
def test_pipeline_reverse_string(tmp_path: Path) -> None:
    slug = "reverse-string"
    staging = _DEMOS_DIR / f"{slug}-staging"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "solution.cpp", submission / f"{slug}.cpp")

    grader_tmp = tmp_path / "grader"
    _copy_tree(staging / "grader", grader_tmp)

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=grader_tmp / "pipeline.py",
        submission_dir=submission,
        root_dir=tmp_path,
        grader_dir_override=grader_tmp,
    )


@pytest.mark.slow
def test_pipeline_word_count(tmp_path: Path) -> None:
    slug = "word-count"
    staging = _DEMOS_DIR / f"{slug}-staging"
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(staging / "solution" / "Makefile", submission / "Makefile")
    shutil.copy2(staging / "solution" / "solution.cpp", submission / "solution.cpp")

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=_pipeline_py(slug),
        submission_dir=submission,
        root_dir=tmp_path,
    )


@pytest.mark.slow
def test_pipeline_cpp_linked_list(tmp_path: Path) -> None:
    slug = "cpp-linked-list"
    src = _ASSIGNMENTS_DIR / slug
    submission = tmp_path / "submission"
    submission.mkdir()
    shutil.copy2(src / "solution" / "linked_list.hpp", submission / "linked_list.hpp")

    grader_tmp = tmp_path / "grader"
    _copy_tree(src / "grader", grader_tmp)
    _copy_tree(src / "visible-tests", tmp_path / "visible-tests")
    _copy_tree(src / "hidden-tests", tmp_path / "hidden-tests")

    _run_pipeline(
        slug=slug,
        module_name=_module_name(slug),
        pipeline_py=grader_tmp / "pipeline.py",
        submission_dir=submission,
        root_dir=tmp_path,
        grader_dir_override=grader_tmp,
    )
