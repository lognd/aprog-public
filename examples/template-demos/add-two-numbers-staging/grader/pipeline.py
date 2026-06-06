"""
Grader: Add Two Numbers
=======================

Pipeline:
  LocalDirectory      -- reads student submission
  PrebuiltArtifacts   -- registers add-two-numbers.py as the graded artifact
  OutputCompareTest   -- compares stdout for each case

Student submits: add-two-numbers.py
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.pipeline.build  # noqa: F401
import lograder.output.layout.test.output_compare  # noqa: F401

from lograder.pipeline.build.prebuilt import PrebuiltArtifacts
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.score import (
    GimmeConfig,
    GradescopeConfig,
    GradescopeTestConfig,
    TestCaseScorer,
)
from lograder.pipeline.test.output_compare import ComparisonMode, OutputCompareCase, OutputCompareTest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_SUBMISSION_DIR = Path("/autograder/submission")
_ARTIFACT_NAME = "add-two-numbers.py"

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

_CASES: list[OutputCompareCase] = [
    # Visible cases
    OutputCompareCase(
        name="sample_1",
        args=[],
        stdin=b"3\n7\n",
        expected_stdout="10\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_2",
        args=[],
        stdin=b"-5\n3\n",
        expected_stdout="-2\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_zeros",
        args=[],
        stdin=b"0\n0\n",
        expected_stdout="0\n",
        comparison=ComparisonMode.STRIP,
    ),
    # Hidden cases
    OutputCompareCase(
        name="hidden_large",
        args=[],
        stdin=b"1000000000\n-1000000000\n",
        expected_stdout="0\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_negative",
        args=[],
        stdin=b"-100\n-200\n",
        expected_stdout="-300\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_both_positive",
        args=[],
        stdin=b"42\n58\n",
        expected_stdout="100\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_VISIBLE_POINTS: dict[str, float] = {
    "sample_1": 10.0,
    "sample_2": 10.0,
    "sample_zeros": 10.0,
}

_HIDDEN_POINTS: dict[str, float] = {
    "hidden_large": 25.0,
    "hidden_negative": 20.0,
    "hidden_both_positive": 25.0,
}

_ALL_POINTS = {**_VISIBLE_POINTS, **_HIDDEN_POINTS}


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(PrebuiltArtifacts({_ARTIFACT_NAME: _ARTIFACT_NAME}))

    pipeline.add(tests := OutputCompareTest(_ARTIFACT_NAME, _CASES))
    tests.scorer = TestCaseScorer(
        _ALL_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Add Two Numbers Correctness",
    )
    tests.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Add Two Numbers",
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
