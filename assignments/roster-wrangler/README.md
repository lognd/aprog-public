# Roster Wrangler

You now know Python's four core built-in structures individually --
`list`, `tuple`, `dict`, `set` -- and you have practiced choosing among
them in structure-selector. This assignment asks you to actually USE them
together: six small, pure functions over a roster of student records,
each one built from whichever combination of `list`, `dict`, `set`, and
`tuple` best fits the job. Nothing here needs anything more advanced than
what you already have -- loops, `if`, indexing, and the seen-set /
seen-dict pattern for tracking "have I processed this before."

## Problem statement

A **roster** is a `list[dict]`: each record is a `dict` with exactly three
keys, `"name"` (`str`), `"section"` (`str`), and `"grade"` (`int`), for
example:

```python
{"name": "Alice", "section": "A", "grade": 90}
```

Implement six pure functions in a file named `roster.py`, each described
below. None of them print anything, read a file, or mutate the roster
list (or any record inside it) that was passed in.

## Interface

```python
def group_by_section(roster: list[dict]) -> dict[str, list[str]]:
    """Map each section to the names enrolled in it, in roster order."""

def dedupe_names(roster: list[dict]) -> list[str]:
    """Distinct names in roster, first-occurrence order preserved."""

def section_averages(roster: list[dict]) -> dict[str, float]:
    """Map each section to its average grade, rounded to 2 decimal places."""

def top_student_per_section(roster: list[dict]) -> dict[str, str]:
    """Map each section to its top-scoring student's name (ties: alphabetical)."""

def enrollment_sets(
    roster_a: list[dict], roster_b: list[dict]
) -> tuple[set[str], set[str], set[str]]:
    """(only in roster_a, in both, only in roster_b), by name."""

def index_by_key(roster: list[dict]) -> dict[tuple[str, str], int]:
    """Map (name, section) to grade. Duplicate pairs: last one wins."""
```

### Examples

```python
>>> roster = [
...     {"name": "Alice", "section": "A", "grade": 90},
...     {"name": "Bob", "section": "A", "grade": 80},
...     {"name": "Alice", "section": "B", "grade": 70},
...     {"name": "Carol", "section": "B", "grade": 95},
... ]
>>> group_by_section(roster)
{'A': ['Alice', 'Bob'], 'B': ['Alice', 'Carol']}
>>> dedupe_names(roster)
['Alice', 'Bob', 'Carol']
>>> section_averages(roster)
{'A': 85.0, 'B': 82.5}
>>> top_student_per_section(roster)
{'A': 'Alice', 'B': 'Carol'}
>>> index_by_key(roster)
{('Alice', 'A'): 90, ('Bob', 'A'): 80, ('Alice', 'B'): 70, ('Carol', 'B'): 95}
```

`enrollment_sets` compares two separate rosters by name:

```python
>>> roster_a = [{"name": "Alice", "section": "A", "grade": 90},
...              {"name": "Bob", "section": "A", "grade": 80}]
>>> roster_b = [{"name": "Bob", "section": "A", "grade": 80},
...              {"name": "Carol", "section": "B", "grade": 95}]
>>> enrollment_sets(roster_a, roster_b)
({'Alice'}, {'Bob'}, {'Carol'})
```

Every function must handle an empty roster (`[]`) without raising, and
`group_by_section`, `dedupe_names`, `section_averages`,
`top_student_per_section`, and `index_by_key` all return an empty
container (`{}` or `[]`) for an empty input.

### On duplicate records

Two kinds of duplication show up in this assignment, and they are handled
differently on purpose:

- `dedupe_names` is about the roster containing the **same student's name
  more than once** (perhaps enrolled in two sections) -- keep only the
  first occurrence, in the order it appeared.
- `index_by_key`'s duplicate handling is about the same **(name,
  section)** pair appearing more than once in the input (a data-entry
  correction, for example) -- the LAST record with that exact pair wins,
  overwriting any earlier grade for that same key. `top_student_per_section`
  similarly should reflect each student's best recorded grade in a
  section, not simply whichever record was processed last.

## Every Python concept here, defined via its C++ counterpart

<details>
<summary>the seen-set pattern -- Python's dedupe idiom, with no std::set include needed</summary>

The pattern in `dedupe_names` -- keep a `set` of names already seen, check
membership before appending to a result `list` -- is the direct Python
analogue of a C++ loop using a `std::unordered_set<std::string>` to track
which values have already been emitted. The mechanics are identical; the
only difference is that Python's `set` needs no template argument and no
`#include`.

</details>

<details>
<summary>dict.get(key, default) -- avoiding a KeyError without an extra if</summary>

`totals.get(section, 0)` returns `totals[section]` if the key is already
present, or the given default (`0`) if it is not -- one expression instead
of writing `if section in totals: ... else: ...` by hand. This is
Python's answer to the C++ pattern of checking `map.find(key) !=
map.end()` before reading a possibly-absent key; `dict.get` folds the
check and the fallback into a single call.

</details>

<details>
<summary>a tuple as a dict key -- the compound-key pattern from structure-selector</summary>

`index_by_key` needs to look something up by TWO values together (a name
AND a section), which is exactly the coordinate-pair pattern from
structure-selector: build the key as a `tuple`, `(name, section)`, and use
it as an ordinary `dict` key. `tuple` is hashable (as long as everything
inside it is), so this works with no special machinery -- the same role a
hand-written `struct` with a hash specialization would play as a C++
`std::unordered_map` key.

</details>

<details>
<summary>set operators -- - and & for comparing two collections</summary>

`enrollment_sets` is a direct application of `set`'s built-in comparison
operators: `a - b` (elements in `a` but not `b`), `a & b` (elements in
both). Building each roster's names into a `set` first, then combining
them with these operators, computes all three groups this function needs
to return without a hand-written nested loop comparing every name in one
roster against every name in the other.

</details>

## Constraints

- `roster.py` must contain **no `import` statements of `collections` or
  `statistics`** -- the point of this assignment is to build the
  grouping, deduplication, and averaging logic yourself with plain
  `dict`/`list`/`set` operations, rather than reach for
  `collections.Counter`/`collections.defaultdict` or `statistics.mean` to
  skip past it.
- All six functions must be **pure**: no `print`, no reading from a file,
  no mutating the `roster` (or any record inside it) that was passed in.
- **Type hints are required** on every function's parameters and return
  type. The starter file already has them filled in -- keep them exactly
  as given; do not widen or remove them.
- A clean run of [ty](https://docs.astral.sh/ty/) (a fast, modern Python
  type checker, run over `roster.py`) earns a bonus. `ty check roster.py`
  should report no errors once your implementation is type-correct.

## Grading

| Component                              | Points |
|------------------------------------------|--------|
| No `collections`/`statistics` shortcuts   | 0 (gate) |
| Visible correctness tests                 | 35     |
| Hidden correctness tests                  | 50     |
| Clean `ty` type-check (bonus)              | 10     |

## Submission

Submit your implementation as `roster.py`. Do not rename the module, and
do not change any function's name, parameter list, or type hints.
