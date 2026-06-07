"""
Grader: Matrix Class
====================

Pipeline:
  SourceCheck               -- validates .hpp and .cpp submitted
  InjectStudentIntoStaff    -- copies both files into grader dir for CMake
  CMakeManifestCheck        -- sanity check for grader CMakeLists.txt
  CMakeBuild                -- builds matrix-class_tests and matrix-class_hidden_tests
  Catch2Test (visible)      -- runs visible test suite
  Catch2Test (hidden)       -- runs hidden test suite; visibility: after_due_date

Student submits: matrix-class.hpp and matrix-class.cpp
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.check.source  # noqa: F401
import lograder.output.layout.pipeline.build  # noqa: F401
import lograder.output.layout.pipeline.mixin  # noqa: F401
import lograder.output.layout.project.simple_project  # noqa: F401
import lograder.output.layout.test.catch2  # noqa: F401

from lograder.pipeline.build.cmake import CMakeBuild
from lograder.pipeline.check.project.simple_project import CMakeManifestCheck
from lograder.pipeline.check.source.source_check import SourceCheck
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.mixin.mixin import InjectStudentIntoStaff
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.score import (
    AllOrNothingScorer,
    CleanRunScorer,
    GimmeConfig,
    GradescopeConfig,
    GradescopeTestConfig,
    TestCaseScorer,
)
from lograder.pipeline.test.catch2 import Catch2Test

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_GRADER_DIR = Path(__file__).parent
_SUBMISSION_DIR = Path("/autograder/submission")

# ---------------------------------------------------------------------------
# Scoring
# Format: "<binary_name>/<TEST_CASE string>"
# ---------------------------------------------------------------------------

_VISIBLE_CATCH2_POINTS: dict[str, float] = {
    "matrix-class_tests/constructor -- zero initialized": 12.0,
    "matrix-class_tests/at -- read and write": 12.0,
    "matrix-class_tests/operator+ -- element-wise add": 12.0,
    "matrix-class_tests/transpose -- 2x3 becomes 3x2": 12.0,
    "matrix-class_tests/operator* -- 2x2 identity": 12.0,
}

_HIDDEN_CATCH2_POINTS: dict[str, float] = {
    "matrix-class_hidden_tests/hidden -- copy constructor deep copy": 10.0,
    "matrix-class_hidden_tests/hidden -- copy assignment deep copy": 10.0,
    "matrix-class_hidden_tests/hidden -- matrix multiply 2x3 * 3x2": 10.0,
    "matrix-class_hidden_tests/hidden -- print output": 10.0,
}


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(source := SourceCheck(
        language="cpp",
        files=["matrix-class.hpp", "matrix-class.cpp"],
        constraints=[],
        label="Source Files Submitted",
    ))
    source.scorer = CleanRunScorer(
        0.0,
        max_errors=0,
        require_ok_return=True,
        label="Source Files Submitted",
    )
    source.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    pipeline.add(InjectStudentIntoStaff(
        _GRADER_DIR,
        student_files=["matrix-class.hpp", "matrix-class.cpp"],
    ))

    pipeline.add(cmake_check := CMakeManifestCheck())
    cmake_check.scorer = AllOrNothingScorer(0.0, label="CMake Setup")
    cmake_check.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    pipeline.add(build := CMakeBuild())
    build.scorer = AllOrNothingScorer(0.0, label="Compilation")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="3")

    pipeline.add(catch2_vis := Catch2Test("matrix-class_tests"))
    catch2_vis.scorer = TestCaseScorer(
        _VISIBLE_CATCH2_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Visible Correctness (Catch2)",
    )
    catch2_vis.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="4")

    pipeline.add(catch2_hid := Catch2Test("matrix-class_hidden_tests"))
    catch2_hid.scorer = TestCaseScorer(
        _HIDDEN_CATCH2_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Hidden Correctness (Catch2)",
    )
    catch2_hid.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="5"
    )

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Matrix Class",
        authors=[StaffAuthor(name="Course Staff", role="Instructor")],
        notes="Contact course staff within 3 days if you believe there is a grading error.",
    )

    with config(root_directory=Path("/autograder"), executable_timeout=60.0):
        score = make_pipeline()(metadata=metadata)

    score.write_results_json(
        config=GradescopeConfig(
            visibility="visible",
            stdout_visibility="after_due_date",
        ),
    )
