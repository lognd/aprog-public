# mypy: ignore-errors
from __future__ import annotations

import shutil
from pathlib import Path

import pytest


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def public_root(tmp_path: Path) -> Path:
    """Minimal aprog-public repo with aprog.toml, one template, and one assignment."""
    root = tmp_path / "aprog-public"
    _write_aprog_toml(root)
    _write_template(root, "python-stdin-stdout", "python")
    _write_assignment(root, "linked-list-insertion", "python-stdin-stdout")
    return root


@pytest.fixture()
def public_root_no_generated(public_root: Path) -> Path:
    return public_root


@pytest.fixture()
def private_root(tmp_path: Path, public_root: Path) -> Path:
    root = tmp_path / "aprog-private"
    slug = "linked-list-insertion"
    (root / "solutions" / slug).mkdir(parents=True)
    (root / "solutions" / slug / "solution.py").write_text("def solve(): pass\n")
    (root / "hidden-tests" / slug / "tests").mkdir(parents=True)
    (root / "hidden-tests" / slug / "tests" / "test_hidden.py").write_text("# hidden\n")
    (root / "grader" / slug).mkdir(parents=True)
    (root / "grader" / slug / "pipeline.py").write_text(
        "from lograder.pipeline.pipeline import Pipeline\n"
        "from lograder.pipeline.input.local_directory import LocalDirectory\n\n"
        "def make_pipeline() -> Pipeline:\n"
        "    return Pipeline([LocalDirectory()])\n"
    )
    return root


def _write_aprog_toml(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "aprog.toml").write_text(
        "[classification.languages.python]\nname = \"Python\"\n"
        "[classification.languages.cpp]\nname = \"C++\"\n"
        "[classification.difficulties.easy]\nname = \"Easy\"\nrank = 1\n"
        "[classification.difficulties.medium]\nname = \"Medium\"\nrank = 2\n"
        "[classification.difficulties.hard]\nname = \"Hard\"\nrank = 3\n"
        "[classification.topics.data-structures]\nname = \"Data Structures\"\n"
        "[classification.topics.linked-lists]\nname = \"Linked Lists\"\n"
        "[classification.concepts.mutation]\nname = \"Mutation\"\n"
        "[labels.unit-tests]\nname = \"Unit Tests\"\ndescription = \"\"\n"
        "[organization]\n"
        "require_encryption = false\n"
        "require_hidden_tests = true\n"
        'default_grader_visibility = "after_due_date"\n'
    )


def _write_template(root: Path, slug: str, language: str) -> None:
    tpl = root / "templates" / slug
    tpl.mkdir(parents=True)
    (tpl / "template.toml").write_text(
        f'[template]\nslug = "{slug}"\nname = "{slug}"\nversion = "0.1"\ndescription = ""\n'
        f'[classification]\nlanguage = "{language}"\ndefault_difficulty = "medium"\n'
        f'recommended_topics = []\n'
        f'[outputs.public]\nassignment_toml = true\nreadme = true\nvisible_tests = true\n'
        f'expected = true\nassets = true\n'
        f'[outputs.private]\nsolution = true\nhidden_tests = true\ngrader = true\n'
    )


def _write_assignment(root: Path, slug: str, template_slug: str) -> None:
    a = root / "assignments" / slug
    a.mkdir(parents=True)
    (a / "assignment.toml").write_text(
        f'[assignment]\nslug = "{slug}"\nname = "Linked List Insertion"\n'
        f'author = "handle"\ndescription = "Insert into a linked list."\n'
        f'status = "draft"\n\n'
        f'[classification]\nlanguage = "python"\ndifficulty = "medium"\n'
        f'topics = ["data-structures", "linked-lists"]\n\n'
        f'[template]\nslug = "{template_slug}"\n\n'
        f'[grader]\nvisibility = "after_due_date"\nstdout_visibility = "after_due_date"\n'
    )
    (a / "README.md").write_text("# Linked List Insertion\n")
    (a / "visible-tests").mkdir()
    (a / "visible-tests" / "test_visible.py").write_text("# visible tests\n")
    (a / "expected").mkdir()
    (a / "assets").mkdir()
