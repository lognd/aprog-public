# roster-wrangler -- starter file.
#
# A roster is a list[dict] of student records; each record has three keys:
# "name" (str), "section" (str), and "grade" (int). Every function below is
# a pure function over one or two rosters -- no printing, no mutating the
# roster you were given, no reading from a file.
#
# Do not rename this file. Do not import anything except (optionally)
# typing -- every function is implementable with plain dict/list/set/tuple
# operations from the language itself, no standard-library modules
# required (the reference solution uses none). Type hints are REQUIRED on
# every function signature (already filled in below -- keep them). See
# README.md for the exact spec of each function.


def group_by_section(roster: list[dict]) -> dict[str, list[str]]:
    """Return a dict mapping each section to the names enrolled in it, in roster order."""
    raise NotImplementedError


def dedupe_names(roster: list[dict]) -> list[str]:
    """Return the distinct names in roster, first-occurrence order preserved."""
    raise NotImplementedError


def section_averages(roster: list[dict]) -> dict[str, float]:
    """Return a dict mapping each section to its average grade, rounded to 2 decimal places."""
    raise NotImplementedError


def top_student_per_section(roster: list[dict]) -> dict[str, str]:
    """Return a dict mapping each section to its top-scoring student's name (ties: alphabetical)."""
    raise NotImplementedError


def enrollment_sets(
    roster_a: list[dict], roster_b: list[dict]
) -> tuple[set[str], set[str], set[str]]:
    """Return (only in roster_a, in both, only in roster_b), by name."""
    raise NotImplementedError


def index_by_key(roster: list[dict]) -> dict[tuple[str, str], int]:
    """Return a dict mapping (name, section) to grade. Duplicate pairs: last one wins."""
    raise NotImplementedError
