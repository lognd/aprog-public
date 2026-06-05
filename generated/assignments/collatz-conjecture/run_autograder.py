import json
import sys
import traceback
from pathlib import Path

# /autograder/source/ is the extracted zip root; grader/pipeline.py lives there.
_SOURCE = Path("/autograder/source")
sys.path.insert(0, str(_SOURCE))

from lograder.pipeline.config import config
from lograder.pipeline.score import GradescopeConfig

from grader.pipeline import make_pipeline

_RESULTS = Path("/autograder/results/results.json")

if __name__ == "__main__":
    try:
        with config(root_directory=Path("/autograder/submission")):
            pipeline = make_pipeline()
            score = pipeline()
            score.write_results_json(
                config=GradescopeConfig(
                    visibility='visible',
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
