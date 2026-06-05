"""
Grader: C++ Singly Linked List
================================

Showcases the full lograder pipeline:

  SourceCheck               --  validates linked_list.hpp submitted; forbids STL containers
  InjectStudentIntoStaff   --  copies header into grader dir so CMake can find it
  CMakeManifestCheck        --  verifies CMakeLists.txt is present (required by CMakeBuild)
  CMakeBuild                --  builds four targets:
                               linked_list_tests        (visible Catch2)
                               linked_list_hidden_tests (hidden Catch2)
                               linked_list              (CLI driver  --  student impl)
                               reference                (CLI driver  --  staff impl)
  Catch2Test (visible)      --  structured XML parse of visible test cases
  Catch2Test (hidden)       --  same for hidden cases; visibility: after_due_date
  ValgrindTest              --  memory leak / error detection
  OutputCompareTest         --  manual cases with hardcoded expected stdout
  DifferentialTest          --  extra-credit cases; reference_artifact="reference"
                             (no pre-compiled binary required)

Private layout (aprog staging):
  grader/
    CMakeLists.txt            (builds all four targets)
    main.cpp                  (CLI driver, compiled twice: student + reference)
    pipeline.py               (this file)
  hidden-tests/
    linked_list.hpp           (staff reference implementation)
    test_hidden.cpp           (hidden Catch2 source)

setup.sh installs: cmake, valgrind  ([grader.dependencies] system in assignment.toml)
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
from lograder.pipeline.check.project.simple_project import (
    CMakeManifest,
    CMakeManifestCheck,
)
from lograder.pipeline.check.source.source_check import (
    IncludeConstraint,
    QualifiedNameConstraint,
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
# Catch2  --  visible test cases
# ---------------------------------------------------------------------------

_VISIBLE_CATCH2_POINTS: dict[str, float] = {
    "linked_list_tests/empty list has size 0":                                        5.0,
    "linked_list_tests/push_back increases size":                                     5.0,
    "linked_list_tests/front and back after push_back":                               5.0,
    "linked_list_tests/push_front prepends correctly":                                5.0,
    "linked_list_tests/pop_front on single element leaves empty list":                5.0,
    "linked_list_tests/pop_front on multiple elements":                               5.0,
    "linked_list_tests/pop_front on empty list is a no-op":                           5.0,
    "linked_list_tests/pop_back on single element leaves empty list":                 5.0,
    "linked_list_tests/pop_back removes the tail":                                    5.0,
    "linked_list_tests/pop_back on empty list is a no-op":                            5.0,
    "linked_list_tests/print produces space-separated output with trailing newline":  5.0,
    "linked_list_tests/copy constructor creates an independent deep copy":            5.0,
}  # 12 x 5 = 60 pts

# ---------------------------------------------------------------------------
# Catch2  --  hidden test cases (linked_list_hidden_tests binary)
# ---------------------------------------------------------------------------

_HIDDEN_CATCH2_POINTS: dict[str, float] = {
    "linked_list_hidden_tests/size tracks push_back and pop_front correctly":    5.0,
    "linked_list_hidden_tests/size tracks push_front and pop_back correctly":    5.0,
    "linked_list_hidden_tests/pop_front restores expected front value":          5.0,
    "linked_list_hidden_tests/pop_back restores expected back value":            5.0,
    "linked_list_hidden_tests/copy constructor produces same contents":          5.0,
    "linked_list_hidden_tests/mutating copy does not affect original":           5.0,
    "linked_list_hidden_tests/mutating original does not affect copy":           5.0,
    "linked_list_hidden_tests/print on two-element list is space-separated with newline": 5.0,
    "linked_list_hidden_tests/print on single-element list has no leading/trailing space": 5.0,
}  # 9 x 5 = 45 pts

# ---------------------------------------------------------------------------
# Valgrind  --  memory safety cases
# ---------------------------------------------------------------------------

_VALGRIND_CASES: list[ValgrindCase] = [
    ValgrindCase(
        name="valgrind_push_pop",
        args=["push_back", "1", "push_back", "2", "pop_front", "pop_front"],
        stdin=b"",
        check_leaks=True,
    ),
    ValgrindCase(
        name="valgrind_copy",
        args=["push_back", "1", "push_back", "2", "copy_push", "99"],
        stdin=b"",
        check_leaks=True,
    ),
    ValgrindCase(
        name="valgrind_large",
        args=sum([["push_back", str(i)] for i in range(50)], []) + ["pop_back"] * 25,
        stdin=b"",
        check_leaks=True,
    ),
    ValgrindCase(
        name="valgrind_empty_ops",
        args=["pop_front", "pop_back"],
        stdin=b"",
        check_leaks=True,
    ),
]

_VALGRIND_POINTS: dict[str, float] = {
    "valgrind_push_pop":  5.0,
    "valgrind_copy":      5.0,
    "valgrind_large":     5.0,
    "valgrind_empty_ops": 5.0,
}  # 4 x 5 = 20 pts

# ---------------------------------------------------------------------------
# OutputCompareTest  --  manual cases with hardcoded expected stdout
# ---------------------------------------------------------------------------

_MANUAL_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="manual_five_print",
        args=["push_back", "10", "push_back", "20", "push_back", "30",
              "push_back", "40", "push_back", "50", "print"],
        stdin=b"",
        expected_stdout="10 20 30 40 50\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_interleave_print",
        args=["push_back", "1", "push_front", "0",
              "push_back", "2", "push_front", "-1", "print"],
        stdin=b"",
        expected_stdout="-1 0 1 2\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_pop_to_empty_repush",
        args=["push_back", "1", "push_back", "2",
              "pop_front", "pop_front",
              "push_back", "42", "size", "front", "back"],
        stdin=b"",
        expected_stdout="size=1\nfront=42\nback=42\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_alternating_pop_remainder",
        args=["push_back", "1", "push_back", "2",
              "push_back", "3", "push_back", "4",
              "pop_front", "pop_back", "size", "front", "back"],
        stdin=b"",
        expected_stdout="size=2\nfront=2\nback=3\n",
        comparison=ComparisonMode.EXACT,
    ),
    OutputCompareCase(
        name="manual_push_front_order",
        args=["push_front", "3", "push_front", "2", "push_front", "1", "print"],
        stdin=b"",
        expected_stdout="1 2 3\n",
        comparison=ComparisonMode.EXACT,
    ),
]

_MANUAL_POINTS: dict[str, float] = {
    "manual_five_print":                5.0,
    "manual_interleave_print":          5.0,
    "manual_pop_to_empty_repush":       5.0,
    "manual_alternating_pop_remainder": 5.0,
    "manual_push_front_order":          5.0,
}  # 5 x 5 = 25 pts

# ---------------------------------------------------------------------------
# DifferentialTest  --  extra-credit cases
#
# reference_artifact="reference" resolves the reference binary from the
# CMakeBuild artifacts dict at grading time.  The "reference" target in
# grader/CMakeLists.txt compiles grader/main.cpp against hidden-tests/linked_list.hpp
# (the staff solution), so no pre-compiled binary needs to be committed.
# ---------------------------------------------------------------------------

_DIFF_CASES: list[OracleInput] = [
    OracleInput(
        name="diff_large_sequence",
        args=sum([["push_back", str(i)] for i in range(1, 21)], []) + ["size", "print"],
        stdin=b"",
    ),
    OracleInput(
        name="diff_stress_mixed",
        args=["push_back", "1", "push_back", "2", "push_front", "0",
              "pop_front", "push_back", "3", "pop_back",
              "size", "print"],
        stdin=b"",
    ),
    OracleInput(
        name="diff_copy_bonus",
        args=["push_back", "10", "push_back", "20", "push_back", "30",
              "copy_push", "99"],
        stdin=b"",
    ),
]

_DIFF_BASE_POINTS: dict[str, float] = {
    "diff_large_sequence": 0.0,
    "diff_stress_mixed":   0.0,
    "diff_copy_bonus":     0.0,
}

# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    # -- 1. Read student submission -------------------------------------------
    pipeline.add(LocalDirectory(root=submission_dir))

    # -- 2. Source check ------------------------------------------------------
    # BREAKS EARLY if linked_list.hpp is missing; non-fatal Err per STL violation.
    pipeline.add(source := SourceCheck(
        language="cpp",
        files=["linked_list.hpp"],
        constraints=[
            IncludeConstraint(
                headers=["<vector>", "<list>", "<deque>",
                         "<forward_list>", "<stack>", "<queue>"],
                max_count=0,
                label="No STL container headers",
            ),
            QualifiedNameConstraint(
                qualified_names=["std::vector", "std::list",
                                 "std::deque", "std::forward_list"],
                max_count=0,
                label="No STL container qualified names",
            ),
        ],
        label="Header Submitted / No STL Containers",
    ))
    source.scorer = CleanRunScorer(
        0.0,
        max_errors=0,
        require_ok_return=True,
        extra_credit=5.0,
        label="No STL Containers",
    )
    source.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    # -- 3. Inject student header into grader dir -----------------------------
    pipeline.add(InjectStudentIntoStaff(
        _GRADER_DIR,
        student_files=["linked_list.hpp"],
    ))

    # -- 4. CMake manifest check ----------------------------------------------
    pipeline.add(cmake_check := CMakeManifestCheck())
    cmake_check.scorer = AllOrNothingScorer(0.0, label="CMake Setup")
    cmake_check.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    # -- 5. CMake build -------------------------------------------------------
    # Produces four artifacts: linked_list_tests, linked_list_hidden_tests,
    # linked_list (student impl), reference (staff impl from hidden-tests/).
    pipeline.add(build := CMakeBuild())
    build.scorer = AllOrNothingScorer(0.0, label="Compilation")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="3")

    # -- 6. Visible Catch2 tests ----------------------------------------------
    pipeline.add(catch2_vis := Catch2Test("linked_list_tests"))
    catch2_vis.scorer = TestCaseScorer(
        _VISIBLE_CATCH2_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Visible Correctness (Catch2)",
    )
    catch2_vis.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="4")

    # -- 7. Hidden Catch2 tests -----------------------------------------------
    pipeline.add(catch2_hid := Catch2Test("linked_list_hidden_tests"))
    catch2_hid.scorer = TestCaseScorer(
        _HIDDEN_CATCH2_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Hidden Correctness (Catch2)",
    )
    catch2_hid.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="5"
    )

    # -- 8. Valgrind memory check ---------------------------------------------
    pipeline.add(vg := ValgrindTest("linked_list", _VALGRIND_CASES))
    vg.scorer = TestCaseScorer(_VALGRIND_POINTS, label="Memory Safety (Valgrind)")
    vg.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="6")

    # -- 9. Manual OutputCompare cases ----------------------------------------
    pipeline.add(manual := OutputCompareTest("linked_list", _MANUAL_CASES))
    manual.scorer = TestCaseScorer(_MANUAL_POINTS, label="Hidden Manual Cases")
    manual.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="7"
    )

    # -- 10. DifferentialTest  --  extra credit ----------------------------------
    # reference_artifact="reference" resolves the staff binary from CMakeBuild.
    # No pre-compiled binary needed  --  it's built fresh at grading time.
    pipeline.add(diff := DifferentialTest(
        "linked_list",
        reference_artifact="reference",
        test_cases=_DIFF_CASES,
    ))
    diff.scorer = TestCaseScorer(
        _DIFF_BASE_POINTS,
        extra_credit_cases={
            "diff_large_sequence": 5.0,
            "diff_stress_mixed":   5.0,
            "diff_copy_bonus":     5.0,
        },
        label="Differential Extra Credit",
    )
    diff.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="8"
    )

    return pipeline


# ---------------------------------------------------------------------------
# Entry point  --  called by run_autograder.py on Gradescope
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="C++ Linked List",
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
