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

### Per-function examples

- `group_by_section(roster)`
  - `group_by_section([{"name": "Zoe", "section": "A", "grade": 50}]) == {"A": ["Zoe"]}` -- a single record still becomes a one-name list, not a bare string.
  - `group_by_section([{"name": "Alice", "section": "A", "grade": 90}, {"name": "Alice", "section": "A", "grade": 95}]) == {"A": ["Alice", "Alice"]}` -- this function does NOT deduplicate; `dedupe_names` is the function for that job.
  - `group_by_section([]) == {}` -- empty roster in, empty dict out.
- `dedupe_names(roster)`
  - `dedupe_names([{"name": "Bob", "section": "A", "grade": 1}, {"name": "Bob", "section": "B", "grade": 2}]) == ["Bob"]` -- same name, two different sections, still counts as one student and is kept once.
  - `dedupe_names([{"name": "Alice", "section": "A", "grade": 90}, {"name": "Bob", "section": "A", "grade": 80}]) == ["Alice", "Bob"]` -- no duplicates present, so every name passes through unchanged.
  - `dedupe_names([]) == []` -- empty roster in, empty list out.
- `section_averages(roster)`
  - `section_averages([{"name": "A", "section": "X", "grade": 1}, {"name": "B", "section": "X", "grade": 1}, {"name": "C", "section": "X", "grade": 2}]) == {"X": 1.33}` -- `(1 + 1 + 2) / 3 = 1.3333...`, rounded to 2 places, not truncated.
  - `section_averages([{"name": "Alice", "section": "A", "grade": 90}]) == {"A": 90.0}` -- a single record is its own average, and the result is still a `float` (`90.0`, not the `int` `90`).
  - `section_averages([]) == {}` -- empty roster in, empty dict out; there is no section to divide zero grades by, so nothing is computed.
- `top_student_per_section(roster)`
  - `top_student_per_section([{"name": "Zack", "section": "A", "grade": 90}, {"name": "Amy", "section": "A", "grade": 90}]) == {"A": "Amy"}` -- exact tie on grade; alphabetically-first name wins regardless of which record came first in the roster.
  - `top_student_per_section([{"name": "Alice", "section": "A", "grade": 90}, {"name": "Alice", "section": "A", "grade": 60}]) == {"A": "Alice"}` -- the SAME student appears twice with different grades for the same section; the higher grade (`90`) is the one that counts.
  - `top_student_per_section([]) == {}` -- empty roster in, empty dict out.
- `enrollment_sets(roster_a, roster_b)`
  - `enrollment_sets([{"name": "Bob", "section": "A", "grade": 1}], [{"name": "Bob", "section": "A", "grade": 1}]) == (set(), {"Bob"}, set())` -- identical single-student rosters: nobody is "only in A" or "only in B", `Bob` is in both.
  - `enrollment_sets([], [{"name": "Eve", "section": "C", "grade": 100}]) == (set(), set(), {"Eve"})` -- an empty first roster means the "only in A" and "in both" sets are empty; everyone in `roster_b` falls into "only in B".
  - `enrollment_sets([], []) == (set(), set(), set())` -- both rosters empty, all three sets empty.
- `index_by_key(roster)`
  - `index_by_key([{"name": "Bob", "section": "A", "grade": 1}, {"name": "Bob", "section": "A", "grade": 9}]) == {("Bob", "A"): 9}` -- the SAME `(name, section)` pair appears twice with different grades; the map ends up holding only the LAST one (`9`), the earlier `1` is fully overwritten, not averaged or summed.
  - `index_by_key([{"name": "Alice", "section": "A", "grade": 90}, {"name": "Alice", "section": "B", "grade": 70}]) == {("Alice", "A"): 90, ("Alice", "B"): 70}` -- same name, different sections, so these are two DIFFERENT keys, not a collision.
  - `index_by_key([]) == {}` -- empty roster in, empty dict out.

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

---

## Examples at a glance: every function on one roster

To make all six functions concrete at once, here is **one** roster,
deliberately built with every tricky case this assignment tests: a name
(`Alice`) enrolled in two different sections, a duplicate `(name,
section)` pair (a corrected grade for `Alice` in section `A`), and a
grade tie in section `B` (`Carol` and `Dave` both scoring 88). Read this
table first -- it is the whole assignment in miniature.

```python
roster = [
    {"name": "Alice", "section": "A", "grade": 90},
    {"name": "Bob",   "section": "A", "grade": 80},
    {"name": "Alice", "section": "A", "grade": 95},  # correction: Alice's A grade
    {"name": "Carol", "section": "B", "grade": 88},
    {"name": "Dave",  "section": "B", "grade": 88},  # tie with Carol
    {"name": "Alice", "section": "B", "grade": 70},  # Alice also enrolled in B
]
```

| Call | Returns | Why |
|------|---------|-----|
| `group_by_section(roster)` | `{'A': ['Alice', 'Bob', 'Alice'], 'B': ['Carol', 'Dave', 'Alice']}` | every record's name is appended in roster order, including the repeat of `Alice` in each section -- this function does not deduplicate |
| `dedupe_names(roster)` | `['Alice', 'Bob', 'Carol', 'Dave']` | `Alice` appears three times across the roster (twice in `A`, once in `B`) but is kept only once, at her FIRST appearance |
| `section_averages(roster)` | `{'A': 88.33, 'B': 82.0}` | section `A`: `(90 + 80 + 95) / 3 = 88.333...` rounds to `88.33`; section `B`: `(88 + 88 + 70) / 3 = 82.0` |
| `top_student_per_section(roster)` | `{'A': 'Alice', 'B': 'Carol'}` | in `A`, `Alice`'s corrected `95` beats `Bob`'s `80`; in `B`, `Carol` and `Dave` TIE at `88`, so the alphabetically-first name (`Carol` < `Dave`) wins |
| `index_by_key(roster)` | `{('Alice', 'A'): 95, ('Bob', 'A'): 80, ('Carol', 'B'): 88, ('Dave', 'B'): 88, ('Alice', 'B'): 70}` | `('Alice', 'A')` appears twice in the input (`90` then `95`) -- the LAST one wins, so the map holds `95`, not `90` |
| `enrollment_sets(roster, roster_b)` where `roster_b = [{"name": "Bob", "section": "A", "grade": 80}, {"name": "Eve", "section": "C", "grade": 100}]` | `({'Alice', 'Carol', 'Dave'}, {'Bob'}, {'Eve'})` | by NAME only: `Alice`/`Carol`/`Dave` are only in the first roster, `Bob` is in both, `Eve` is only in the second |
| `group_by_section([])` | `{}` | empty input, empty output -- same pattern for every function below |
| `dedupe_names([])` | `[]` | empty input, empty output |
| `section_averages([])` | `{}` | empty input, empty output |
| `top_student_per_section([])` | `{}` | empty input, empty output |
| `index_by_key([])` | `{}` | empty input, empty output |
| `enrollment_sets([], [])` | `(set(), set(), set())` | no names anywhere, so all three sets are empty |

## Worked example: watch `top_student_per_section` run, step by step

This is the function most likely to trip you up (it needs to track the
BEST grade seen so far per section, and break ties alphabetically), so
here is every step spelled out on a small roster:

```python
roster = [
    {"name": "Carol", "section": "B", "grade": 88},
    {"name": "Dave",  "section": "B", "grade": 88},
    {"name": "Alice", "section": "B", "grade": 70},
]
```

We walk the roster once, front to back, keeping two running maps:
`best_grade` (section -> highest grade seen so far) and `best_name`
(section -> the name that earned it). For each record: if its section
has not been seen before, it automatically becomes the best so far. If
the section HAS been seen, compare the new grade to the current best --
a strictly higher grade replaces both maps; an EQUAL grade replaces
`best_name` only if the new name is alphabetically earlier (this is what
makes ties deterministic instead of "whichever came first").

| Step | Record | Section seen before? | Compare | Action | `best_grade` after | `best_name` after |
|------|--------|----------------------|---------|--------|---------------------|-------------------|
| 1 | `Carol`, `B`, `88` | no | -- (first record for `B`) | set `B` -> `88`/`Carol` | `{'B': 88}` | `{'B': 'Carol'}` |
| 2 | `Dave`, `B`, `88` | yes | `88 == 88` (tie) -> compare names: `'Dave' < 'Carol'`? No | keep `Carol` (name is NOT earlier) | `{'B': 88}` | `{'B': 'Carol'}` |
| 3 | `Alice`, `B`, `70` | yes | `70 < 88` -> not higher | no change | `{'B': 88}` | `{'B': 'Carol'}` |
| end | -- | -- | -- | return `best_name` | -- | `{'B': 'Carol'}` |

The loop ends with `best_name = {'B': 'Carol'}`, so
`top_student_per_section(roster)` returns exactly **`{'B': 'Carol'}`**.
Notice step 2: `Dave` arrived with an EQUAL grade to the current best,
not a higher one -- if the tie-break compared "did the grade increase"
alone, `Dave` would incorrectly overwrite `Carol` just for showing up
second. The alphabetical check is what keeps the answer stable no matter
what order tied records happen to appear in.

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
- **Type-annotation bonus (10 pts):** every function must annotate all of
  its parameters and its return type. The starter's signatures are left
  UNANNOTATED on purpose -- add the hints yourself, matching the fully typed
  signatures in the Interface section above (for example
  `def group_by_section(roster: list[dict]) -> dict[str, list[str]]:`). The
  bonus is awarded only when every function is fully annotated. A separate,
  informational [ty](https://docs.astral.sh/ty/) check then flags any
  annotation that does not hold up -- `ty check roster.py` should report no
  errors once your implementation is type-correct.

## Grading

| Component                              | Points |
|------------------------------------------|--------|
| No `collections`/`statistics` shortcuts   | 0 (gate) |
| Visible correctness tests                 | 35     |
| Hidden correctness tests                  | 50     |
| Complete type annotations (bonus)         | 10     |

## Submission

Submit your implementation as `roster.py`. Do not rename the module, and
do not change any function's name or parameter list (you should, however,
add type hints -- that is the bonus).
