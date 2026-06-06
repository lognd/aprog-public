# mypy: ignore-errors
from __future__ import annotations

from pathlib import Path

from aprog.commands.validate_cmd import _scan_public_violations


def _make_assignment(tmp_path: Path, files: list[str]) -> Path:
    root = tmp_path / "linked-list-insertion"
    for rel in files:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
    return root


def test_clean_assignment_has_no_violations(tmp_path: Path) -> None:
    root = _make_assignment(
        tmp_path,
        [
            "assignment.toml",
            "README.md",
            "visible-tests/test_visible.py",
            "assets/starter.py",
        ],
    )
    assert _scan_public_violations(root) == []


def test_solution_file_is_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["solution.py"])
    violations = _scan_public_violations(root)
    assert any("solution" in v for v in violations)


def test_pipeline_py_is_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["pipeline.py"])
    violations = _scan_public_violations(root)
    assert any("pipeline.py" in v for v in violations)


def test_grader_dir_is_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["grader/pipeline.py"])
    violations = _scan_public_violations(root)
    assert any("grader" in v for v in violations)


def test_hidden_tests_dir_is_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["hidden-tests/test_hidden.py"])
    violations = _scan_public_violations(root)
    assert any("hidden" in v for v in violations)


def test_solution_prefixed_file_is_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["solution.cpp"])
    violations = _scan_public_violations(root)
    assert any("solution" in v for v in violations)


def test_answer_prefixed_file_is_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["answer.py"])
    violations = _scan_public_violations(root)
    assert any("answer" in v for v in violations)


def test_starter_py_in_assets_is_not_a_violation(tmp_path: Path) -> None:
    root = _make_assignment(tmp_path, ["assets/starter.py"])
    violations = _scan_public_violations(root)
    assert violations == []
