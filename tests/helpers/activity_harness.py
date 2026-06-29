"""Shared test harness for activity launch.py files.

Usage
-----
    from tests.helpers.activity_harness import (
        load_activity,
        qa_activity_slugs,
        FuzzInput,
        CorrectInput,
        PASSPHRASE_MARKERS,
    )

Adding a new activity
---------------------
1. Drop a launch.py with QUESTIONS or SNIPPETS into activities/<slug>/.
2. If you have the correct answers, add them to tests/fixtures/activity_answers.json.
3. Run `make test` -- fuzz tests pick up automatically; correct-path tests
   activate as soon as the answers list is non-empty.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import sys
import types
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_ACTIVITIES_DIR = _ROOT / "activities"
_FIXTURES_DIR = _ROOT / "tests" / "fixtures"

# Tokens that appear in output only when the passphrase is revealed.
PASSPHRASE_MARKERS: tuple[str, ...] = ("Passphrase:", "passphrase:", "PASSPHRASE:")

# Default wrong-answer budget before EOFError is raised.
DEFAULT_MAX_WRONG = 12

# Wrong tokens used by the fuzz input mock (various shapes to cover edge cases).
FUZZ_TOKENS: list[str] = [
    "fuzz-DEADBEEF-wrong",
    "99999999",
    "",
    "NaN",
    "0x0",
    "-1",
    "???",
]


# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

def load_activity(slug: str) -> types.ModuleType:
    """Load activities/<slug>/launch.py as a fresh module.

    Does not execute the __main__ guard. The activity directory is temporarily
    added to sys.path so any relative asset references resolve correctly.
    """
    path = _ACTIVITIES_DIR / slug / "launch.py"
    if not path.exists():
        raise FileNotFoundError(f"No launch.py for activity {slug!r}")
    spec = importlib.util.spec_from_file_location(f"_activity_{slug}", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    activity_dir = str(path.parent)
    sys.path.insert(0, activity_dir)
    try:
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    finally:
        try:
            sys.path.remove(activity_dir)
        except ValueError:
            pass
    return mod


# ---------------------------------------------------------------------------
# Activity discovery
# ---------------------------------------------------------------------------

def _has_qa_loop(slug: str) -> bool:
    """Return True if the activity has a QUESTIONS or SNIPPETS top-level name."""
    src = (_ACTIVITIES_DIR / slug / "launch.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    top_names = {
        node.targets[0].id
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    }
    return bool(top_names & {"QUESTIONS", "SNIPPETS"})


def qa_activity_slugs() -> list[str]:
    """Return sorted slugs for all Q&A activities (have QUESTIONS or SNIPPETS)."""
    if not _ACTIVITIES_DIR.exists():
        return []
    return sorted(
        d.name
        for d in _ACTIVITIES_DIR.iterdir()
        if d.is_dir()
        and (d / "launch.py").exists()
        and _has_qa_loop(d.name)
    )


# ---------------------------------------------------------------------------
# Answer fixture
# ---------------------------------------------------------------------------

def answers_for(slug: str) -> list[str]:
    """Return correct answers for slug, or empty list if not yet recorded.

    Reads tests/fixtures/<slug>.json -- a bare JSON array of answer strings.
    """
    path = _FIXTURES_DIR / f"{slug}.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


# ---------------------------------------------------------------------------
# Input mocks
# ---------------------------------------------------------------------------

class FuzzInput:
    """Callable mock for builtins.input that injects wrong answers then EOF.

    - "Press Enter" / "enter to begin" prompts -> ""
    - "Try again" prompts -> "n"
    - All other prompts -> cycles through FUZZ_TOKENS
    - After max_wrong total answer calls -> raises EOFError
    """

    def __init__(self, max_wrong: int = DEFAULT_MAX_WRONG) -> None:
        self._max_wrong = max_wrong
        self._wrong_count = 0

    def __call__(self, prompt: str = "") -> str:
        p = prompt.lower()
        if "press enter" in p or "enter to begin" in p:
            return ""
        if "try again" in p:
            return "n"
        self._wrong_count += 1
        if self._wrong_count > self._max_wrong:
            raise EOFError("fuzz budget exhausted")
        return FUZZ_TOKENS[self._wrong_count % len(FUZZ_TOKENS)]


class CorrectInput:
    """Callable mock that feeds correct answers in order then EOF.

    Designed for the positive happy-path test: the activity should decrypt
    and print the passphrase before the mock runs out.
    """

    def __init__(self, answers: list[str]) -> None:
        self._answers = iter(answers)

    def __call__(self, prompt: str = "") -> str:
        p = prompt.lower()
        if "press enter" in p or "enter to begin" in p:
            return ""
        if "try again" in p:
            return "n"
        return next(self._answers)  # StopIteration if answers exhausted
