import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lograder.pipeline.config import config
from lograder.pipeline.score import GradescopeConfig

from grader.pipeline import make_pipeline

if __name__ == "__main__":
    with config(root_directory=Path("/autograder/submission")):
        pipeline = make_pipeline()
        score = pipeline()
        score.write_results_json(
            config=GradescopeConfig(
                visibility='after_due_date',
                stdout_visibility='after_due_date',
            )
        )
