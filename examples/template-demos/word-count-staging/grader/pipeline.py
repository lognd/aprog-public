"""
Grader: Word Count
==================

Pipeline:
  LocalDirectory      -- reads student submission
  MakefileBuild       -- runs make in submission dir
  PrebuiltArtifacts   -- registers the produced binary
  OutputCompareTest   -- visible correctness cases
  OutputCompareTest   -- hidden correctness cases

Student submits: Makefile + source files; default target builds word-count
"""

from __future__ import annotations

from pathlib import Path

import lograder.output.layout.pipeline.build  # noqa: F401
import lograder.output.layout.test.output_compare  # noqa: F401

from lograder.pipeline.build.makefile import MakefileBuild
from lograder.pipeline.build.prebuilt import PrebuiltArtifacts
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.score import (
    AllOrNothingScorer,
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

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

_VISIBLE_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="sample_three_lines",
        args=[],
        stdin=b"hello world\nfoo bar baz\none\n",
        expected_stdout="Line 1: 2 words\nLine 2: 3 words\nLine 3: 1 word\nTotal: 6 words\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="sample_single_line",
        args=[],
        stdin=b"the quick brown fox\n",
        expected_stdout="Line 1: 4 words\nTotal: 4 words\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_HIDDEN_CASES: list[OutputCompareCase] = [
    OutputCompareCase(
        name="hidden_one_word",
        args=[],
        stdin=b"hello\n",
        expected_stdout="Line 1: 1 word\nTotal: 1 word\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_multiline",
        args=[],
        stdin=b"a b\nc d e\nf\n",
        expected_stdout="Line 1: 2 words\nLine 2: 3 words\nLine 3: 1 word\nTotal: 6 words\n",
        comparison=ComparisonMode.STRIP,
    ),
    OutputCompareCase(
        name="hidden_single_word_total",
        args=[],
        stdin=b"word\n",
        expected_stdout="Line 1: 1 word\nTotal: 1 word\n",
        comparison=ComparisonMode.STRIP,
    ),
]

_VISIBLE_POINTS: dict[str, float] = {
    "sample_three_lines": 5.0,
    "sample_single_line": 5.0,
}
_HIDDEN_POINTS: dict[str, float] = {
    "hidden_one_word": 25.0,
    "hidden_multiline": 30.0,
    "hidden_single_word_total": 25.0,
}


# ---------------------------------------------------------------------------
# Pipeline factory
# ---------------------------------------------------------------------------


def make_pipeline(submission_dir: Path = _SUBMISSION_DIR) -> Pipeline:
    pipeline = Pipeline()

    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(build := MakefileBuild())
    build.scorer = AllOrNothingScorer(10.0, label="Build")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    pipeline.add(PrebuiltArtifacts({"word-count": submission_dir / "word-count"}))

    pipeline.add(visible := OutputCompareTest("word-count", _VISIBLE_CASES))
    visible.scorer = TestCaseScorer(
        _VISIBLE_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Visible Correctness",
    )
    visible.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="2")

    pipeline.add(hidden := OutputCompareTest("word-count", _HIDDEN_CASES))
    hidden.scorer = TestCaseScorer(
        _HIDDEN_POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Hidden Correctness",
    )
    hidden.scorer.gradescope = GradescopeTestConfig(
        visibility="after_due_date", number="3"
    )

    return pipeline


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from lograder.pipeline.config import config

    metadata = GraderMetadata.from_gradescope(
        grader_name="Word Count",
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
