# Activity: Structure Selector

You already reason about `std::vector`, `std::pair`/`std::tuple`,
`std::map`/`std::unordered_map`, and `std::set`/`std::unordered_set` in
C++: which one fits a given job depends on whether you need order,
whether you need to look things up by key, and whether duplicates matter.
Python's `list`, `tuple`, `dict`, and `set` map onto exactly those same
four questions, with lighter syntax. This activity is nine real-world
scenarios -- no code at all -- where you have to pick the right structure
and explain why the other three would not fit as well.

## Concepts covered

- `list`: mutable, ordered, allows duplicates -- the default choice for a
  growing or editable sequence
- `tuple`: immutable, ordered, fixed-size -- a lightweight bundle for
  values that are done being built, without the ceremony of a class
- `dict`: maps keys to values with average O(1) lookup by key, and
  preserves insertion order when iterated
- `set`: unique elements, no guaranteed order, average O(1) membership
  testing -- and the built-in `-`, `&` operators for comparing two sets
- hashability: which types can be a `dict` key or `set` element, and why
  a `list` cannot
- a `tuple` used as a compound `dict` key, for a coordinate-style lookup
- when a `dict` genuinely outperforms two parallel lists kept in sync by
  hand

## How it works

The launcher shows you nine scenarios, one at a time, each describing
something you need to store and how you need to use it. Read the
scenario and type which structure you would use (and, for a couple of
questions, a short reason why). A correct answer shows a short explanation
and moves you on; a wrong answer shows an explanation of the specific
misconception behind that guess.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all nine scenarios and the launcher shows you
a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask three questions about the data</summary>

Does order matter? Do you need to look something up BY a key, rather than
just check for its presence? Do duplicates carry meaning, or should they
collapse? Every scenario in this activity is answerable from those three
questions alone.

</details>

<details>
<summary>Hint 2 -- "look up by X" almost always means dict</summary>

If the scenario's core operation is "given A, find B" (rather than "is A
present at all" or "give me everything in order"), you are almost always
looking for a `dict`, with A as the key and B as the value.

</details>

<details>
<summary>Hint 3 -- a tuple can be a dict key; a list cannot</summary>

When a scenario needs a compound key (more than one value together
identifying an entry, like a coordinate pair), reach for a `tuple` as the
key -- never a `list`, which is not hashable.

</details>

## Going further

- Look up `collections.Counter` (part of the standard library). Which
  scenario in this activity would it fit especially well, and why is it
  really just a specialized `dict` under the hood?
- For the sparse-grid scenario, what happens to a `dict`-keyed-by-tuple
  approach if you need to find "everything in row 3," not just a single
  `(row, col)` lookup? Is a plain `dict` still the best fit, or would you
  need to restructure it?
- Pick one scenario from this activity and estimate, roughly, how the
  runtime cost of the WRONG structure would grow as the data got 10x
  larger. Compare that to the structure you actually chose.
