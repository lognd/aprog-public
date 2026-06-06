"""
Grader: Binary Search
=====================

Pipeline:
  LocalDirectory    -- reads student submission
  PytestTest        -- runs hidden pytest suite against the student's module

The hidden test suite lives in hidden-tests/ and loads the student's module
from /autograder/submission/binary-search.py via importlib.

Student submits: binary-search.py
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.pipeline.build  # noqa: F401

from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.score import (
    GimmeConfig,
    GradescopeConfig,
    GradescopeTestConfig,
    TestCaseScorer,
)
from lograder.pipeline.test.pytest import PytestTest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_GRADER_DIR = Path(__file__).parent
_SUBMISSION_DIR = Path("/autograder/submission")
_HIDDEN_TESTS = _GRADER_DIR / "hidden-tests"

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

_POINTS: dict[str, float] = {
    "test_hidden::test_single_element_found": 10.0,
    "test_hidden::test_single_element_not_found": 10.0,
    "test_hidden::test_large_array": 20.0,
    "test_hidden::test_negative_values": 20.0,
    "test_hidden::test_two_elements_found_first": 20.0,
    "test_hidden::test_two_elements_found_second": 20.0,
}


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    import os
    os.environ["SUBMISSION_DIR"] = str(submission_dir)

    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(pytest_step := PytestTest(paths=[_HIDDEN_TESTS]))
    pytest_step.scorer = TestCaseScorer(
        _POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Binary Search Correctness",
    )
    pytest_step.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="1"
    )

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Binary Search",
        authors=[StaffAuthor(name="Course Staff", role="Instructor")],
        notes="Contact course staff within 3 days if you believe there is a grading error.",
    )

    with config(root_directory=_SUBMISSION_DIR, executable_timeout=30.0):
        score = make_pipeline()(metadata=metadata)

    score.write_results_json(
        config=GradescopeConfig(
            visibility="after_due_date",
            stdout_visibility="after_due_date",
        ),
    )
