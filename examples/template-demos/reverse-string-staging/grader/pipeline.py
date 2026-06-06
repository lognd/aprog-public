"""
Grader: Reverse String
======================

Pipeline:
  LocalDirectory          -- reads student submission
  SourceCheck             -- validates reverse-string.cpp submitted
  InjectStudentIntoStaff  -- copies .cpp into grader dir for CMake
  CMakeManifestCheck      -- verifies grader CMakeLists.txt
  CMakeBuild              -- compiles student binary
  OutputCompareTest       -- visible I/O correctness cases
  OutputCompareTest       -- hidden I/O correctness cases
  ValgrindTest            -- memory safety (extra credit)

Student submits: reverse-string.cpp
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.check.source  # noqa: F401
import lograder.output.layout.pipeline.build  # noqa: F401
import lograder.output.layout.pipeline.mixin  # noqa: F401
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
from lograder.pipeline.test.output_compare import ComparisonMode, OutputCompareCase, OutputCompareTest
from lograder.pipeline.test.valgrind import ValgrindCase, ValgrindTest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_GRADER_DIR = Path(__file__).parent
_SUBMISSION_DIR = Path("/autograder/submission")

# ---------------------------------------------------------------------------
# Visible test cases
# ---------------------------------------------------------------------------

_VISIBLE_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="sample_hello",
        args=[],
        stdin=b"hello\n",
        expected_stdout="olleh\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_palindrome",
        args=[],
        stdin=b"racecar\n",
        expected_stdout="racecar\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_VISIBLE_POINTS: dict[str, float] = {
    "sample_hello": 10.0,
    "sample_palindrome": 10.0,
}

# ---------------------------------------------------------------------------
# Hidden test cases
# ---------------------------------------------------------------------------

_HIDDEN_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="hidden_abcde",
        args=[],
        stdin=b"abcde\n",
        expected_stdout="edcba\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_single",
        args=[],
        stdin=b"z\n",
        expected_stdout="z\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_spaces",
        args=[],
        stdin=b"hello world\n",
        expected_stdout="dlrow olleh\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_numbers",
        args=[],
        stdin=b"12345\n",
        expected_stdout="54321\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_HIDDEN_POINTS: dict[str, float] = {
    "hidden_abcde": 20.0,
    "hidden_single": 20.0,
    "hidden_spaces": 20.0,
    "hidden_numbers": 20.0,
}

# ---------------------------------------------------------------------------
# Valgrind cases
# ---------------------------------------------------------------------------

_VALGRIND_CASES: list[ValgrindCase] = [
    ValgrindCase(name="vg_hello", args=[], stdin=b"hello\n", check_leaks=True),
]


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(source := SourceCheck(
        language="cpp",
        files=["reverse-string.cpp"],
        constraints=[],
        label="Source File Submitted",
    ))
    source.scorer = CleanRunScorer(
        0.0,
        max_errors=0,
        require_ok_return=True,
        label="Source File Submitted",
    )
    source.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    pipeline.add(InjectStudentIntoStaff(
        _GRADER_DIR,
        student_files=["reverse-string.cpp"],
    ))

    pipeline.add(cmake_check := CMakeManifestCheck())
    cmake_check.scorer = AllOrNothingScorer(0.0, label="CMake Setup")
    cmake_check.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    pipeline.add(build := CMakeBuild())
    build.scorer = AllOrNothingScorer(0.0, label="Compilation")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="3")

    pipeline.add(visible := OutputCompareTest("reverse-string", _VISIBLE_CASES))
    visible.scorer = TestCaseScorer(
        _VISIBLE_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Visible Correctness",
    )
    visible.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="4")

    pipeline.add(hidden := OutputCompareTest("reverse-string", _HIDDEN_CASES))
    hidden.scorer = TestCaseScorer(
        _HIDDEN_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Hidden Correctness",
    )
    hidden.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="5"
    )

    pipeline.add(vg := ValgrindTest("reverse-string", _VALGRIND_CASES))
    vg.scorer = AllOrNothingScorer(0.0, extra_credit=5.0, label="Memory Safety")
    vg.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="6"
    )

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Reverse String",
        authors=[StaffAuthor(name="Course Staff", role="Instructor")],
        notes="Contact course staff within 3 days if you believe there is a grading error.",
    )

    with config(root_directory=Path("/autograder"), executable_timeout=60.0):
        score = make_pipeline()(metadata=metadata)

    score.write_results_json(
        config=GradescopeConfig(
            visibility="after_due_date",
            stdout_visibility="after_due_date",
        ),
    )
