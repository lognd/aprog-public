"""
Grader: Binary Search Tree
==========================

Pipeline:
  SourceCheck               -- validates cpp-bst.hpp submitted; checks constraints
  InjectStudentIntoStaff    -- copies header into grader dir so CMake can find it
  CMakeManifestCheck        -- verifies grader CMakeLists.txt is present
  CMakeBuild                -- builds four targets:
                               cpp-bst_tests        (visible Catch2)
                               cpp-bst_hidden_tests (hidden Catch2)
                               cpp-bst              (CLI driver -- student impl)
                               reference            (CLI driver -- staff impl)
  Catch2Test (visible)      -- structured parse of visible test cases
  Catch2Test (hidden)       -- same for hidden cases; visibility: after_due_date
  ValgrindTest              -- memory leak / error detection
  OutputCompareTest         -- manual I/O cases
  DifferentialTest          -- extra-credit cases compared against reference binary

Private layout:
  grader/
    CMakeLists.txt            (builds all four targets)
    main.cpp                  (CLI driver, compiled twice)
    pipeline.py               (this file)
  hidden-tests/
    solution.hpp              (staff reference implementation)
    test_hidden.cpp           (hidden Catch2 source)
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.check.source  # noqa: F401
import lograder.output.layout.pipeline.build  # noqa: F401
import lograder.output.layout.pipeline.mixin  # noqa: F401
import lograder.output.layout.project.simple_project  # noqa: F401
import lograder.output.layout.test.catch2  # noqa: F401
import lograder.output.layout.test.differential  # noqa: F401
import lograder.output.layout.test.output_compare  # noqa: F401
import lograder.output.layout.test.valgrind  # noqa: F401

from lograder.pipeline.build.cmake import CMakeBuild
from lograder.pipeline.check.project.simple_project import CMakeManifestCheck
from lograder.pipeline.check.source.source_check import (
    IncludeConstraint,
    SourceCheck,
)
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
from lograder.pipeline.test.differential import DifferentialTest
from lograder.pipeline.test.oracle import OracleInput
from lograder.pipeline.test.output_compare import ComparisonMode, OutputCompareCase, OutputCompareTest
from lograder.pipeline.test.valgrind import ValgrindCase, ValgrindTest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_GRADER_DIR = Path(__file__).parent
_SUBMISSION_DIR = Path("/autograder/submission")

# ---------------------------------------------------------------------------
# Catch2 scoring
# Key format: "<binary_name>/<TEST_CASE string>"
# ---------------------------------------------------------------------------

_VISIBLE_CATCH2_POINTS: dict[str, float] = {
    "cpp-bst_tests/insert and search -- basic": 15.0,
    "cpp-bst_tests/inorder -- sorted output": 15.0,
    "cpp-bst_tests/insert -- duplicates ignored": 15.0,
    "cpp-bst_tests/empty tree -- search returns false": 15.0,
}

_HIDDEN_CATCH2_POINTS: dict[str, float] = {
    "cpp-bst_hidden_tests/hidden -- single element inorder": 10.0,
    "cpp-bst_hidden_tests/hidden -- insert descending": 15.0,
    "cpp-bst_hidden_tests/hidden -- search after many inserts": 10.0,
    "cpp-bst_hidden_tests/hidden -- inorder large": 10.0,
}

# ---------------------------------------------------------------------------
# Valgrind cases
# ---------------------------------------------------------------------------

_VALGRIND_CASES: list[ValgrindCase] = [
    ValgrindCase(
        name="vg_insert_search",
        args=["insert", "5", "insert", "3", "insert", "7", "inorder"],
        stdin=b"",
        check_leaks=True,
    ),
]

_VALGRIND_POINTS: dict[str, float] = {"vg_insert_search": 20.0}

# ---------------------------------------------------------------------------
# Manual I/O cases
# ---------------------------------------------------------------------------

_MANUAL_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="manual_search_found",
        args=["insert", "10", "insert", "5", "search", "5"],
        stdin=b"",
        expected_stdout="found\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_search_not_found",
        args=["insert", "10", "search", "99"],
        stdin=b"",
        expected_stdout="not found\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_inorder_3",
        args=["insert", "3", "insert", "1", "insert", "2", "inorder"],
        stdin=b"",
        expected_stdout="1 2 3\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_duplicate",
        args=["insert", "7", "insert", "7", "inorder"],
        stdin=b"",
        expected_stdout="7\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_empty_inorder",
        args=["inorder"],
        stdin=b"",
        expected_stdout="\n",
        comparison=ComparisonMode.EXACT,
    ),
]

_MANUAL_POINTS: dict[str, float] = {
    "manual_search_found": 5.0,
    "manual_search_not_found": 5.0,
    "manual_inorder_3": 5.0,
    "manual_duplicate": 5.0,
    "manual_empty_inorder": 5.0,
}

# ---------------------------------------------------------------------------
# Differential extra-credit cases
# ---------------------------------------------------------------------------

_DIFF_CASES: list[OracleInput] = [
    OracleInput(
        name="diff_large_tree",
        args=["insert", "50", "insert", "25", "insert", "75",
              "insert", "12", "insert", "37", "insert", "62", "insert", "87",
              "inorder"],
        stdin=b"",
    ),
    OracleInput(
        name="diff_search_boundary",
        args=["insert", "5", "insert", "10", "insert", "15",
              "search", "5", "search", "10", "search", "15"],
        stdin=b"",
    ),
]

_DIFF_BASE_POINTS: dict[str, float] = {
    "diff_large_tree": 0.0,
    "diff_search_boundary": 0.0,
}

_DIFF_EXTRA_CREDIT: dict[str, float] = {
    "diff_large_tree": 8.0,
    "diff_search_boundary": 7.0,
}


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(source := SourceCheck(
        language="cpp",
        files=["cpp-bst.hpp"],
        constraints=[
            IncludeConstraint(
                headers=["<set>", "<map>", "<unordered_set>", "<unordered_map>"],
                max_count=0,
                label="No STL container headers",
            ),
        ],
        label="Header Submitted",
    ))
    source.scorer = CleanRunScorer(
        0.0,
        max_errors=0,
        require_ok_return=True,
        extra_credit=5.0,
        label="Code Constraints",
    )
    source.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    pipeline.add(InjectStudentIntoStaff(
        _GRADER_DIR,
        student_files=["cpp-bst.hpp"],
    ))

    pipeline.add(cmake_check := CMakeManifestCheck())
    cmake_check.scorer = AllOrNothingScorer(0.0, label="CMake Setup")
    cmake_check.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    pipeline.add(build := CMakeBuild())
    build.scorer = AllOrNothingScorer(0.0, label="Compilation")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="3")

    pipeline.add(catch2_vis := Catch2Test("cpp-bst_tests"))
    catch2_vis.scorer = TestCaseScorer(
        _VISIBLE_CATCH2_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Visible Correctness (Catch2)",
    )
    catch2_vis.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="4")

    pipeline.add(catch2_hid := Catch2Test("cpp-bst_hidden_tests"))
    catch2_hid.scorer = TestCaseScorer(
        _HIDDEN_CATCH2_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Hidden Correctness (Catch2)",
    )
    catch2_hid.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="5"
    )

    pipeline.add(vg := ValgrindTest("cpp-bst", _VALGRIND_CASES))
    vg.scorer = TestCaseScorer(_VALGRIND_POINTS, label="Memory Safety (Valgrind)")
    vg.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="6")

    pipeline.add(manual := OutputCompareTest("cpp-bst", _MANUAL_CASES))
    manual.scorer = TestCaseScorer(_MANUAL_POINTS, label="Hidden Manual Cases")
    manual.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="7"
    )

    pipeline.add(diff := DifferentialTest(
        "cpp-bst",
        reference_artifact="reference",
        test_cases=_DIFF_CASES,
    ))
    diff.scorer = TestCaseScorer(
        _DIFF_BASE_POINTS,
        extra_credit_cases=_DIFF_EXTRA_CREDIT,
        label="Extra Credit (Differential)",
    )
    diff.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="8"
    )

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Binary Search Tree",
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
