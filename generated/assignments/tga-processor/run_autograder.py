import json
import sys
import traceback
from pathlib import Path

# /autograder/source/ is the extracted zip root; grader/pipeline.py lives there.
_SOURCE = Path("/autograder/source")
sys.path.insert(0, str(_SOURCE))

from lograder.pipeline.config import config
from lograder.pipeline.metadata import GraderMetadata, StaffAuthor
from lograder.pipeline.score import GradescopeConfig

from grader.pipeline import make_pipeline

_RESULTS = Path("/autograder/results/results.json")

if __name__ == "__main__":
    try:
        metadata = GraderMetadata.from_gradescope(
            grader_name='TGA Image Processor',
            authors=[StaffAuthor(name='lognd', role="Instructor")],
            notes="Contact course staff within 3 days if you believe there is a grading error.",
        )
        import inspect as _inspect
        _sig = _inspect.signature(make_pipeline)
        _kwargs = {"submission_dir": Path("/autograder/submission")} if "submission_dir" in _sig.parameters else {}
        with config(root_directory=Path("/autograder")):
            pipeline = make_pipeline(**_kwargs)
            score = pipeline(metadata=metadata)
            score.write_results_json(
                config=GradescopeConfig(
                    visibility='after_due_date',
                    stdout_visibility='after_due_date',
                )
            )
    except Exception:
        # Always write results.json so Gradescope receives a structured response
        # instead of a blank "no results" error.
        _RESULTS.parent.mkdir(parents=True, exist_ok=True)
        _RESULTS.write_text(
            json.dumps({
                "score": 0,
                "output": "Autograder error:\n\n" + traceback.format_exc(),
            }),
            encoding="utf-8",
        )
        sys.exit(1)