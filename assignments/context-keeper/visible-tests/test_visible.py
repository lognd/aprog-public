"""Visible tests for Context Keeper.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import os
import sys

sys.path.insert(0, os.environ["SUBMISSION_DIR"])

from context_keeper import Muffle, Workspace, cleanup_chain, divide_or, transaction  # noqa: E402


# ---------------------------------------------------------------------------
# Workspace
# ---------------------------------------------------------------------------


def test_workspace_journals_open_then_close():
    journal = []
    with Workspace(journal):
        pass
    assert journal == ["open", "close"]


def test_workspace_returns_self_from_enter():
    journal = []
    with Workspace(journal) as ws:
        assert isinstance(ws, Workspace)


def test_workspace_closes_even_on_exception():
    journal = []
    try:
        with Workspace(journal):
            raise ValueError("boom")
    except ValueError:
        pass
    assert journal == ["open", "close"]


def test_workspace_does_not_suppress():
    journal = []
    raised = False
    try:
        with Workspace(journal):
            raise ValueError("boom")
    except ValueError:
        raised = True
    assert raised


# ---------------------------------------------------------------------------
# Muffle
# ---------------------------------------------------------------------------


def test_muffle_suppresses_exact_match():
    with Muffle(ValueError):
        raise ValueError("boom")
    # no exception escapes -- reaching here is the assertion


def test_muffle_suppresses_subclass():
    class MyValueError(ValueError):
        pass

    with Muffle(ValueError):
        raise MyValueError("boom")


def test_muffle_records_caught_type_name():
    m = Muffle(ValueError)
    with m:
        raise ValueError("boom")
    assert m.caught == ["ValueError"]


def test_muffle_does_not_suppress_other_types():
    raised = False
    try:
        with Muffle(ValueError):
            raise TypeError("nope")
    except TypeError:
        raised = True
    assert raised


def test_muffle_caught_empty_when_nothing_raised():
    m = Muffle(ValueError)
    with m:
        pass
    assert m.caught == []


# ---------------------------------------------------------------------------
# transaction
# ---------------------------------------------------------------------------


def test_transaction_commits_on_clean_exit():
    ledger = [1, 2, 3]
    with transaction(ledger) as working:
        working.append(4)
    assert ledger == [1, 2, 3, 4]


def test_transaction_discards_on_exception():
    ledger = [1, 2, 3]
    try:
        with transaction(ledger) as working:
            working.append(4)
            raise ValueError("boom")
    except ValueError:
        pass
    assert ledger == [1, 2, 3]


def test_transaction_yields_a_copy_not_the_original():
    ledger = [1, 2, 3]
    with transaction(ledger) as working:
        assert working is not ledger


# ---------------------------------------------------------------------------
# divide_or
# ---------------------------------------------------------------------------


def test_divide_or_normal_division():
    assert divide_or(10.0, 2.0, -1.0) == 5.0


def test_divide_or_fallback_on_zero_division():
    assert divide_or(10.0, 0.0, -1.0) == -1.0


# ---------------------------------------------------------------------------
# cleanup_chain
# ---------------------------------------------------------------------------


def test_cleanup_chain_runs_all_steps_no_errors():
    ran = []
    steps = [lambda: ran.append(1), lambda: ran.append(2), lambda: ran.append(3)]
    result = cleanup_chain(steps)
    assert ran == [1, 2, 3]
    assert result == []


def test_cleanup_chain_continues_past_a_failure():
    ran = []

    def bad():
        raise ValueError("boom")

    steps = [lambda: ran.append(1), bad, lambda: ran.append(3)]
    result = cleanup_chain(steps)
    assert ran == [1, 3]
    assert result == ["ValueError"]


def test_cleanup_chain_empty_steps():
    assert cleanup_chain([]) == []


def test_cleanup_chain_returns_a_list():
    assert isinstance(cleanup_chain([]), list)


def test_workspace_journal_is_the_same_list_object_passed_in():
    journal = []
    ws = Workspace(journal)
    with ws:
        pass
    assert ws.journal is journal


def test_muffle_enter_returns_self():
    m = Muffle(ValueError)
    with m as entered:
        assert entered is m
