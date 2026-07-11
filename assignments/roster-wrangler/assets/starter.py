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
# required (the reference solution uses none). The signatures below are
# left UNANNOTATED on purpose: the type-annotation bonus asks you to add
# the parameter and return-type hints yourself (see the exact types in the
# README's Interface section). See README.md for the full spec.


def group_by_section(roster):
    """Return a dict mapping each section to the names enrolled in it, in roster order."""
    raise NotImplementedError


def dedupe_names(roster):
    """Return the distinct names in roster, first-occurrence order preserved."""
    raise NotImplementedError


def section_averages(roster):
    """Return a dict mapping each section to its average grade, rounded to 2 decimal places."""
    raise NotImplementedError


def top_student_per_section(roster):
    """Return a dict mapping each section to its top-scoring student's name (ties: alphabetical)."""
    raise NotImplementedError


def enrollment_sets(roster_a, roster_b):
    """Return (only in roster_a, in both, only in roster_b), by name."""
    raise NotImplementedError


def index_by_key(roster):
    """Return a dict mapping (name, section) to grade. Duplicate pairs: last one wins."""
    raise NotImplementedError
