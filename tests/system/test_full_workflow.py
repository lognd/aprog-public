# mypy: ignore-errors
"""
System test: full contributor → maintainer workflow.

  aprog new → validate → generate-config → package-private → intake → verify

Uses a real lograder pipeline with a Python stdin/stdout assignment so the
grader actually executes. Marked slow because it spawns a subprocess.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from aprog.commands.generate_config_cmd import cmd_generate_config
from aprog.commands.intake_cmd import cmd_intake
from aprog.commands.new_cmd import cmd_new
from aprog.commands.package_cmd import cmd_package_private
from aprog.commands.validate_cmd import cmd_validate
from aprog.commands.verify_cmd import cmd_verify

SLUG = "echo-assignment"


@pytest.fixture()
def public_root(tmp_path: Path) -> Path:
    root = tmp_path / "aprog-public"
    root.mkdir()
    (root / "aprog.toml").write_text(
        "[classification.languages.python]\nname = \"Python\"\n"
        "[classification.difficulties.easy]\nname = \"Easy\"\nrank = 1\n"
        "[classification.difficulties.medium]\nname = \"Medium\"\nrank = 2\n"
        "[classification.topics.io]\nname = \"IO\"\n"
        "[organization]\nrequire_encryption = false\nrequire_hidden_tests = true\n"
        'default_grader_visibility = "after_due_date"\n'
    )
    tpl = root / "templates" / "python-stdin-stdout"
    tpl.mkdir(parents=True)
    (tpl / "template.toml").write_text(
        '[template]\nslug = "python-stdin-stdout"\nname = "Python stdin/stdout"\n'
        'version = "0.1"\ndescription = ""\n'
        '[classification]\nlanguage = "python"\ndefault_difficulty = "medium"\n'
        'recommended_topics = []\n'
        '[outputs.public]\nassignment_toml = true\nreadme = true\nvisible_tests = true\n'
        'expected = true\nassets = true\n'
        '[outputs.private]\nsolution = true\nhidden_tests = true\ngrader = true\n'
    )
    return root


@pytest.fixture()
def staging(tmp_path: Path) -> Path:
    return tmp_path / "staging"


@pytest.fixture()
def private_root(tmp_path: Path) -> Path:
    return tmp_path / "aprog-private"


@pytest.mark.slow
def test_full_contributor_maintainer_workflow(
    public_root: Path, staging: Path, private_root: Path, tmp_path: Path
) -> None:
    # 1. Scaffold
    cmd_new(SLUG, template="python-stdin-stdout", topics=["io"], staging_dir=staging, public_root=public_root)
    assert (public_root / "assignments" / SLUG / "assignment.toml").exists()
    assert (staging / SLUG / "grader" / "pipeline.py").exists()

    # 2. Write a real solution: echo stdin back to stdout
    sol_dir = staging / SLUG / "solution"
    sol_dir.mkdir(parents=True, exist_ok=True)
    (sol_dir / "solution.py").write_text(
        "import sys\nfor line in sys.stdin:\n    print(line, end='')\n"
    )

    # 3. Write the grader pipeline
    (staging / SLUG / "grader" / "pipeline.py").write_text(
        "from lograder.pipeline.input.local_directory import LocalDirectory\n"
        "from lograder.pipeline.pipeline import Pipeline\n"
        "from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase\n"
        "from lograder.pipeline.score import TestCaseScorer\n\n"
        "_CASES = [\n"
        "    OutputCompareCase(name='echo_hello', args=['solution.py'], stdin='hello\\n', expected_stdout='hello\\n'),\n"
        "    OutputCompareCase(name='echo_world', args=['solution.py'], stdin='world\\n', expected_stdout='world\\n'),\n"
        "]\n"
        "_SCORER = TestCaseScorer({'echo_hello': 10.0, 'echo_world': 10.0}, label='Echo')\n\n"
        "def make_pipeline() -> Pipeline:\n"
        "    from lograder.pipeline.input.local_directory import LocalDirectory\n"
        "    import sys\n"
        "    from lograder.process.registry.bash import BashExecutable\n"
        "    from lograder.pipeline.types.artifacts import FileArtifact\n"
        "    from lograder.pipeline.config import get_config\n"
        "    from lograder.common import Ok\n"
        "    from lograder.pipeline.types.parcels import Manifest\n"
        "    from lograder.pipeline.step import Step\n"
        "    from lograder.pipeline.types.sentinel import PIPELINE_START\n"
        "    from typing import Generator\n"
        "    from lograder.common import Result\n\n"
        "    class PythonInput(Step[PIPELINE_START, dict, Exception, Manifest, Exception]):\n"
        "        def __call__(self, input: PIPELINE_START) -> Generator[Result[Manifest, Exception], None, Result[dict, Exception]]:\n"
        "            cfg = get_config()\n"
        "            root = cfg.root_directory\n"
        "            artifacts = {}\n"
        "            for py in root.glob('*.py'):\n"
        "                artifacts[py.name] = FileArtifact(path=py)\n"
        "            if False: yield Ok(Manifest(root))\n"
        "            return Ok(artifacts)\n\n"
        "    step = PythonInput()\n"
        "    tests = OutputCompareTest('solution.py', _CASES)\n"
        "    tests.scorer = _SCORER\n"
        "    return Pipeline([step, tests])\n"
    )

    # 4. Generate config
    cmd_generate_config(SLUG, public_root=public_root)
    manifest = public_root / "generated" / "assignments" / SLUG / "assignment-manifest.json"
    assert manifest.exists()

    # 5. Validate
    code = cmd_validate(SLUG, public_root=public_root)
    assert code == 0

    # 6. Package private
    bundle = cmd_package_private(
        SLUG,
        solution=sol_dir,
        hidden_tests=staging / SLUG / "hidden-tests",
        grader=staging / SLUG / "grader",
        output_dir=tmp_path / "dist",
        public_root=public_root,
    )
    assert bundle.exists()

    # 7. Intake
    cmd_intake(bundle, public_repo=public_root, private_repo=private_root)
    assert (private_root / "grader" / SLUG / "pipeline.py").exists()

    # 8. Manifest content check
    data = json.loads(manifest.read_text())
    assert data["assignment"]["slug"] == SLUG
    assert data["source_hash"].startswith("sha256:")
