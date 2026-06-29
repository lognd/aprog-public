"""Happy-path tests for Q&A activities with recorded correct answers.

Each activity in tests/fixtures/activity_answers.json with a non-empty answer
list gets a test that feeds those answers in order and verifies the passphrase
IS revealed.  Activities without recorded answers are skipped automatically.

To add coverage for a new activity:
    1. Run it manually: python3 activities/<slug>/launch.py
    2. Record the correct answers in tests/fixtures/activity_answers.json
    3. Re-run tests -- the new case is picked up automatically.
"""
from __future__ import annotations

import io
from contextlib import redirect_stdout
from unittest.mock import patch

import pytest

from tests.helpers.activity_harness import (
    PASSPHRASE_MARKERS,
    CorrectInput,
    answers_for,
    load_activity,
    qa_activity_slugs,
)


def _slugs_with_answers() -> list[str]:
    return [s for s in qa_activity_slugs() if answers_for(s)]


@pytest.mark.parametrize("slug", _slugs_with_answers() or ["_no_answers_recorded"])
def test_correct_answers_reveal_passphrase(slug: str) -> None:
    """Correct answers must produce passphrase output."""
    if slug == "_no_answers_recorded":
        pytest.skip("No activities have recorded answers yet -- add tests/fixtures/<slug>.json")

    answers = answers_for(slug)
    mod = load_activity(slug)
    buf = io.StringIO()

    with patch("builtins.input", side_effect=CorrectInput(answers)), redirect_stdout(buf):
        mod.main()

    output = buf.getvalue()
    assert any(m in output for m in PASSPHRASE_MARKERS), (
        f"activities/{slug}: correct answers did not produce passphrase output.\n"
        f"Stdout:\n{output}"
    )
