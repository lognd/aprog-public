"""
Grader: Caesar Cipher
=====================

Pipeline:
  LocalDirectory          -- reads student submission
  SourceCheck             -- validates caesar-cipher.c submitted
  InjectStudentIntoStaff  -- copies .c into grader dir for CMake
  CMakeManifestCheck      -- verifies grader CMakeLists.txt
  CMakeBuild              -- compiles student binary
  OutputCompareTest       -- visible correctness cases
  OutputCompareTest       -- hidden correctness cases
  ValgrindTest            -- memory safety (extra credit)

Student submits: caesar-cipher.c
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
        name="sample_shift3",
        args=["3"],
        stdin=b"Hello, World!\n",
        expected_stdout="Khoor, Zruog!\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_rot13",
        args=["13"],
        stdin=b"Hello\n",
        expected_stdout="Uryyb\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_shift0",
        args=["0"],
        stdin=b"abc\n",
        expected_stdout="abc\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_VISIBLE_POINTS: dict[str, float] = {
    "sample_shift3": 10.0,
    "sample_rot13": 10.0,
    "sample_shift0": 10.0,
}

# ---------------------------------------------------------------------------
# Hidden test cases
# ---------------------------------------------------------------------------

_HIDDEN_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="hidden_wrap",
        args=["3"],
        stdin=b"xyz\n",
        expected_stdout="abc\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_uppercase_wrap",
        args=["3"],
        stdin=b"XYZ\n",
        expected_stdout="ABC\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_nonalpha",
        args=["5"],
        stdin=b"Hello, 123!\n",
        expected_stdout="Mjqqt, 123!\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_rot13_roundtrip",
        args=["13"],
        stdin=b"Uryyb\n",
        expected_stdout="Hello\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_multiline",
        args=["1"],
        stdin=b"abc\nxyz\n",
        expected_stdout="bcd\nyza\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_HIDDEN_POINTS: dict[str, float] = {
    "hidden_wrap": 14.0,
    "hidden_uppercase_wrap": 14.0,
    "hidden_nonalpha": 14.0,
    "hidden_rot13_roundtrip": 14.0,
    "hidden_multiline": 14.0,
}

# ---------------------------------------------------------------------------
# Valgrind cases
# ---------------------------------------------------------------------------

_VALGRIND_CASES: list[ValgrindCase] = [
    ValgrindCase(name="vg_basic", args=["3"], stdin=b"Hello\n", check_leaks=True),
]


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(source := SourceCheck(
        language="c",
        files=["caesar-cipher.c"],
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
        student_files=["caesar-cipher.c"],
    ))

    pipeline.add(cmake_check := CMakeManifestCheck())
    cmake_check.scorer = AllOrNothingScorer(0.0, label="CMake Setup")
    cmake_check.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    pipeline.add(build := CMakeBuild())
    build.scorer = AllOrNothingScorer(0.0, label="Compilation")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="3")

    pipeline.add(visible := OutputCompareTest("caesar-cipher", _VISIBLE_CASES))
    visible.scorer = TestCaseScorer(
        _VISIBLE_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Visible Correctness",
    )
    visible.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="4")

    pipeline.add(hidden := OutputCompareTest("caesar-cipher", _HIDDEN_CASES))
    hidden.scorer = TestCaseScorer(
        _HIDDEN_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Hidden Correctness",
    )
    hidden.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="5"
    )

    pipeline.add(vg := ValgrindTest("caesar-cipher", _VALGRIND_CASES))
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
        grader_name="Caesar Cipher",
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
