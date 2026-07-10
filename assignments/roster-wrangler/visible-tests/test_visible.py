"""
Visible tests for Roster Wrangler.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from roster import (  # noqa: E402
    dedupe_names,
    enrollment_sets,
    group_by_section,
    index_by_key,
    section_averages,
    top_student_per_section,
)

_ROSTER = [
    {"name": "Alice", "section": "A", "grade": 90},
    {"name": "Bob", "section": "A", "grade": 80},
    {"name": "Alice", "section": "B", "grade": 70},
    {"name": "Carol", "section": "B", "grade": 95},
]


def test_group_by_section_basic():
    assert group_by_section(_ROSTER) == {
        "A": ["Alice", "Bob"],
        "B": ["Alice", "Carol"],
    }


def test_group_by_section_preserves_roster_order():
    roster = [
        {"name": "Zoe", "section": "A", "grade": 50},
        {"name": "Amy", "section": "A", "grade": 60},
    ]
    assert group_by_section(roster) == {"A": ["Zoe", "Amy"]}


def test_dedupe_names_basic():
    roster = [
        {"name": "Alice", "section": "A", "grade": 90},
        {"name": "Bob", "section": "A", "grade": 80},
        {"name": "Alice", "section": "B", "grade": 70},
    ]
    assert dedupe_names(roster) == ["Alice", "Bob"]


def test_dedupe_names_no_duplicates():
    roster = [
        {"name": "Alice", "section": "A", "grade": 90},
        {"name": "Bob", "section": "A", "grade": 80},
    ]
    assert dedupe_names(roster) == ["Alice", "Bob"]


def test_section_averages_basic():
    assert section_averages(_ROSTER) == {"A": 85.0, "B": 82.5}


def test_section_averages_rounds_to_two_places():
    roster = [
        {"name": "A", "section": "X", "grade": 1},
        {"name": "B", "section": "X", "grade": 1},
        {"name": "C", "section": "X", "grade": 2},
    ]
    assert section_averages(roster) == {"X": 1.33}


def test_top_student_per_section_basic():
    assert top_student_per_section(_ROSTER) == {"A": "Alice", "B": "Carol"}


def test_top_student_per_section_ties_alphabetical():
    roster = [
        {"name": "Zack", "section": "A", "grade": 90},
        {"name": "Amy", "section": "A", "grade": 90},
    ]
    assert top_student_per_section(roster) == {"A": "Amy"}


def test_enrollment_sets_basic():
    roster_a = [
        {"name": "Alice", "section": "A", "grade": 90},
        {"name": "Bob", "section": "A", "grade": 80},
    ]
    roster_b = [
        {"name": "Bob", "section": "A", "grade": 80},
        {"name": "Carol", "section": "B", "grade": 95},
    ]
    assert enrollment_sets(roster_a, roster_b) == (
        {"Alice"},
        {"Bob"},
        {"Carol"},
    )


def test_index_by_key_basic():
    assert index_by_key(_ROSTER) == {
        ("Alice", "A"): 90,
        ("Bob", "A"): 80,
        ("Alice", "B"): 70,
        ("Carol", "B"): 95,
    }
