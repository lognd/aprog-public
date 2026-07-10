# Study Guide 48: Python Data Structures

This module covers Python's slicing traps (copy vs. alias, slice
assignment resizing a list, the shared-reference `[[0]*n]*m` trap,
`sort()` vs. `sorted()`), maps `list`/`tuple`/`dict`/`set` onto the same
order/lookup/duplicates questions used for C++ containers, and has
students combine all four in `roster-wrangler`.

## Know before you start

- Mutability of list vs. str/tuple, and aliasing via shared object
  references [assumed: row 47 -- Python Data Types]
- `std::vector`/`std::pair`/`std::map`/`std::set` container-choice
  reasoning by order/lookup/duplicates [assumed: row 32 -- Standard
  Containers p1; row 33 -- Map & Set ADT]
- Hashability requirements for map/set keys [assumed: row 33 -- Map & Set
  ADT; row 47 -- Python Data Types]

## Taught here

Concept: slicing traps
- Know `a[:]` (or any slice expression) builds a genuine, brand-new copy
  of a list; plain `b = a` (no slice) makes `b` an alias of the same
  object, never a copy.
- Know negative indices count from the end, and a negative step (`[::-1]`)
  reverses.
- Know slice assignment (`a[1:3] = [9]`) replaces the selected range with
  however many elements the right-hand side has -- which can SHRINK or
  GROW the list, unlike single-index assignment which never changes
  length.
- Know `del` can be applied to a slice (`del a[::2]`) to remove multiple
  elements at once.
- Know `list.sort()` mutates in place and returns `None`; `sorted()`
  returns a new list and leaves the original untouched -- confusing the
  two (`a = a.sort()`) is the single most common "why is my variable
  None" bug for a C++ programmer new to Python.
- Know the `[[0] * n] * m` trap: multiplying a list of lists repeats
  REFERENCES to the same inner list, not independent copies, so mutating
  one "row" silently mutates every row.

Concept: choosing among list, tuple, dict, set
- Know `list`: mutable, ordered, allows duplicates -- the default choice
  for a growing or editable sequence.
- Know `tuple`: immutable, ordered, fixed-size -- a lightweight bundle for
  values that are done being built, without the ceremony of a class, and
  usable as a hashable compound key (unlike a `list`, which cannot be a
  dict key or set element).
- Know `dict`: maps keys to values with average O(1) lookup by key, and
  preserves INSERTION order when iterated (a third, distinct guarantee
  from either `std::map` or `std::unordered_map`).
- Know `set`: unique elements, no guaranteed order, average O(1)
  membership testing, with built-in `-`/`&` operators for set difference
  and intersection.
- Be able to answer three questions to pick a structure: does order
  matter, do you need to look something up BY a key (versus just check
  presence), and do duplicates carry meaning or should they collapse.
- Know a `tuple` can serve as a compound `dict` key for coordinate-style
  or multi-field lookups.

Concept: combining structures for real tasks
- Be able to build a `dict[str, list[str]]` grouping records by a field
  while preserving each group's roster order.
- Be able to deduplicate while preserving first-occurrence order using a
  seen-set alongside the output list.
- Be able to compute per-group aggregates (averages, argmax with
  alphabetical tie-break) into a `dict`.
- Be able to compute set difference/intersection between two collections
  of names using `set` operators directly.
- Be able to build a `dict` keyed by a `tuple` of fields, with documented
  last-write-wins behavior for duplicate keys.

## Study checklist

- [ ] Predict output distinguishing a[:] (copy) from b = a (alias).
- [ ] Explain why a[1:3] = [9, 9, 9] changes the list's length.
- [ ] Explain the [[0]*n]*m shared-reference trap and how to avoid it.
- [ ] Explain why a = a.sort() loses the list.
- [ ] Given a scenario, pick list/tuple/dict/set using the three-question
      method.
- [ ] Explain why a tuple, not a list, is used as a dict key.
- [ ] Implement a group-by and a last-write-wins dict from a list of
      records.

## Practiced in

`slice-sorcery`, `structure-selector`, `roster-wrangler`
