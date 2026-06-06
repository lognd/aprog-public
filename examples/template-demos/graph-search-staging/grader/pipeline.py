"""
Grader: Graph Search
====================

Pipeline:
  LocalDirectory      -- reads student submission
  SourceCheck         -- validates required files submitted
  CMakeManifestCheck  -- verifies CMakeLists.txt exists in submission
  CMakeBuild          -- builds student's CMake project
  OutputCompareTest   -- visible correctness cases
  OutputCompareTest   -- hidden correctness cases
  ValgrindTest        -- memory safety

Student submits: CMakeLists.txt + source files, must produce target "graph-search"
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.check.source  # noqa: F401
import lograder.output.layout.pipeline.build  # noqa: F401
import lograder.output.layout.project.simple_project  # noqa: F401
import lograder.output.layout.test.output_compare  # noqa: F401
import lograder.output.layout.test.valgrind  # noqa: F401

from lograder.pipeline.build.cmake import CMakeBuild
from lograder.pipeline.check.project.simple_project import (
    CMakeManifest,
    CMakeManifestCheck,
)
from lograder.pipeline.check.source.source_check import SourceCheck
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.score import (
    AllOrNothingScorer,
    CleanRunScorer,
    GimmeConfig,
    GradescopeConfig,
    GradescopeTestConfig,
    TestCaseScorer,
)
from lograder.pipeline.test.output_compare import ComparisonMode, OutputCompareCase, OutputCompareTest
from lograder.pipeline.test.valgrind import ValgrindCase, ValgrindTest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_SUBMISSION_DIR = Path("/autograder/submission")

_GRAPH1 = b"5 5\n0 1\n0 2\n1 3\n2 3\n3 4\n0\n"
_GRAPH2 = b"4 2\n0 1\n2 3\n0\n"
_GRAPH3 = b"1 0\n0\n"
_GRAPH4 = b"6 6\n0 1\n0 2\n1 4\n2 3\n3 5\n4 5\n0\n"
_GRAPH5 = b"3 2\n0 1\n1 2\n2\n"

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

_VISIBLE_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="sample_connected",
        args=[],
        stdin=_GRAPH1,
        expected_stdout="0 1 2 3 4\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_disconnected",
        args=[],
        stdin=_GRAPH2,
        expected_stdout="0 1\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_HIDDEN_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="hidden_single_node",
        args=[],
        stdin=_GRAPH3,
        expected_stdout="0\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_layered",
        args=[],
        stdin=_GRAPH4,
        expected_stdout="0 1 2 4 3 5\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_path_from_end",
        args=[],
        stdin=_GRAPH5,
        expected_stdout="2 1 0\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_VALGRIND_CASES: list[ValgrindCase] = [
    ValgrindCase(name="vg_basic", args=[], stdin=_GRAPH1, check_leaks=True),
]

_VISIBLE_POINTS: dict[str, float] = {
    "sample_connected": 10.0,
    "sample_disconnected": 10.0,
}
_HIDDEN_POINTS: dict[str, float] = {
    "hidden_single_node": 20.0,
    "hidden_layered": 20.0,
    "hidden_path_from_end": 20.0,
}
_VALGRIND_POINTS: dict[str, float] = {"vg_basic": 20.0}


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(source := SourceCheck(
        language="cpp",
        files=["CMakeLists.txt", "main.cpp"],
        constraints=[],
        label="Required Files Submitted",
    ))
    source.scorer = CleanRunScorer(
        0.0,
        max_errors=0,
        require_ok_return=True,
        label="Required Files Submitted",
    )
    source.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    pipeline.add(cmake_check := CMakeManifestCheck())
    cmake_check.scorer = AllOrNothingScorer(0.0, label="CMake Setup")
    cmake_check.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    pipeline.add(build := CMakeBuild())
    build.scorer = AllOrNothingScorer(0.0, label="Compilation")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="3")

    pipeline.add(visible := OutputCompareTest("graph-search", _VISIBLE_CASES))
    visible.scorer = TestCaseScorer(
        _VISIBLE_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Visible Correctness",
    )
    visible.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="4")

    pipeline.add(hidden := OutputCompareTest("graph-search", _HIDDEN_CASES))
    hidden.scorer = TestCaseScorer(
        _HIDDEN_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Hidden Correctness",
    )
    hidden.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="5"
    )

    pipeline.add(vg := ValgrindTest("graph-search", _VALGRIND_CASES))
    vg.scorer = TestCaseScorer(_VALGRIND_POINTS, label="Memory Safety (Valgrind)")
    vg.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="6")

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Graph Search",
        authors=[StaffAuthor(name="Course Staff", role="Instructor")],
        notes="Contact course staff within 3 days if you believe there is a grading error.",
    )

    with config(root_directory=_SUBMISSION_DIR, executable_timeout=60.0):
        score = make_pipeline()(metadata=metadata)

    score.write_results_json(
        config=GradescopeConfig(
            visibility="after_due_date",
            stdout_visibility="after_due_date",
        ),
    )
