"""Fuzz tests for Q&A activities.

For each activity with a QUESTIONS or SNIPPETS global, inject wrong answers
via a patched builtins.input and assert no passphrase is ever revealed.
Shell-drop activities have no answer-checking loop and are skipped.

See tests/helpers/activity_harness.py for the shared harness.
See tests/fixtures/activity_answers.json to record correct answers.
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout
from unittest.mock import patch

import pytest

from tests.helpers.activity_harness import (
    DEFAULT_MAX_WRONG,
    PASSPHRASE_MARKERS,
    FuzzInput,
    load_activity,
    qa_activity_slugs,
)

_SLUGS = qa_activity_slugs()


def _assert_no_passphrase(output: str, slug: str, scenario: str) -> None:
    for marker in PASSPHRASE_MARKERS:
        assert marker not in output, (
            f"activities/{slug} [{scenario}]: passphrase marker {marker!r} "
            f"appeared with wrong answers -- possible crypto bypass"
        )


def _run_with_input(slug: str, input_mock: object) -> str:
    """Run activity main() under patched input; return captured stdout."""
    mod = load_activity(slug)
    buf = io.StringIO()
    with (
        patch("builtins.input", side_effect=input_mock),
        redirect_stdout(buf),
        pytest.raises((EOFError, SystemExit, StopIteration)),
    ):
        mod.main()
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Fuzz scenario 1: random-token wrong answers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("slug", _SLUGS)
def test_fuzz_wrong_token(slug: str) -> None:
    """Random fuzz tokens must never unlock a passphrase."""
    output = _run_with_input(slug, FuzzInput())
    _assert_no_passphrase(output, slug, "fuzz-token")


# ---------------------------------------------------------------------------
# Fuzz scenario 2: all-empty answers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("slug", _SLUGS)
def test_fuzz_empty_answers(slug: str) -> None:
    """Empty string answers must never unlock a passphrase."""
    call_count = 0

    def _empty(prompt: str = "") -> str:
        nonlocal call_count
        p = prompt.lower()
        if "try again" in p:
            return "n"
        call_count += 1
        if call_count > DEFAULT_MAX_WRONG:
            raise EOFError("fuzz budget exhausted")
        return ""

    output = _run_with_input(slug, _empty)
    _assert_no_passphrase(output, slug, "empty-answers")


# ---------------------------------------------------------------------------
# Fuzz scenario 3: numeric noise (catches activities that expect numeric answers)
# ---------------------------------------------------------------------------

_NUMERIC_NOISE = ["0", "1", "-1", "42", "999", "3.14", "0x0", "NaN"]


@pytest.mark.parametrize("slug", _SLUGS)
def test_fuzz_numeric_noise(slug: str) -> None:
    """Numeric-looking wrong values must never unlock a passphrase."""
    call_count = 0

    def _numeric(prompt: str = "") -> str:
        nonlocal call_count
        p = prompt.lower()
        if "press enter" in p or "enter to begin" in p:
            return ""
        if "try again" in p:
            return "n"
        call_count += 1
        if call_count > DEFAULT_MAX_WRONG:
            raise EOFError("fuzz budget exhausted")
        return _NUMERIC_NOISE[call_count % len(_NUMERIC_NOISE)]

    output = _run_with_input(slug, _numeric)
    _assert_no_passphrase(output, slug, "numeric-noise")
