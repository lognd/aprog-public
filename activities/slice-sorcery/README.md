# Activity: Slice Sorcery

Slicing a `std::vector` in C++ means writing out an iterator range by
hand; Python bakes the same idea directly into the language with
`a[start:stop:step]` syntax. That convenience hides a few traps: a slice
sometimes copies and sometimes does not, assigning to a slice can change a
list's length outright, and two of Python's most commonly reached-for list
operations have a habit of quietly returning the wrong thing if you are
not paying attention. Eight short programs walk through exactly what
slicing does and does not do.

## Concepts covered

- `a[:]` builds a genuine copy of a list; plain `b = a` (no slice) makes
  `b` an alias of the same object, not a copy
- negative indices (counting from the end) and a negative step (`[::-1]`
  reverses)
- slice assignment (`a[1:3] = [9]`) replaces the selected range with
  however many elements the right-hand side has -- which can shrink or
  grow the list
- `del` applied to a slice (`del a[::2]`)
- `list.sort()` mutates in place and returns `None`; `sorted()` returns a
  new list and leaves the original untouched -- the single most common
  "why is my variable `None`" bug for a C++ programmer new to Python
- the `[[0] * n] * m` trap: multiplying a list of lists repeats
  REFERENCES, not independent copies, so every "row" secretly shares one
  underlying list

## How it works

The launcher shows you eight short Python programs, one at a time. Read
the code, predict exactly what it prints (entering each line separately
if the output has more than one line), and type your prediction. A
correct guess shows a short explanation and moves you on; a wrong guess
shows the actual output and, for many wrong answers, an explanation of the
specific misconception behind that particular guess. Every snippet
actually runs on your own Python interpreter -- nothing here is scripted
or faked.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all eight snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- slicing always builds something new</summary>

Every slice expression (`a[1:3]`, `a[:]`, `a[::-1]`, ...) builds and
returns a brand-new list -- it never returns the original list object,
even when the slice happens to select every element. Plain indexing
(`a[1]`) and plain assignment (`b = a`) are the ones that never copy.

</details>

<details>
<summary>Hint 2 -- slice assignment replaces a RANGE, not a value</summary>

`a[i] = x` replaces one element and never changes the list's length.
`a[i:j] = some_iterable` replaces the entire selected range with however
many elements `some_iterable` actually has -- which might be more, fewer,
or the same number as the range it replaced.

</details>

<details>
<summary>Hint 3 -- for the sort() vs. sorted() snippets, look at what is assigned</summary>

Ask specifically: is the variable being printed the list that got sorted
in place, or the variable that captured a method's RETURN VALUE? Those
are not always the same thing.

</details>

## Going further

- Predict, then check, what `a[10:20]` gives on a 5-element list (an
  out-of-bounds slice). Does it raise an error the way `a[10]` would?
- Write a loop-based fix for the `[[0] * 3] * 2` trap that builds each row
  independently, and confirm mutating one row no longer affects the
  others.
- Look up `list.copy()` and `copy.deepcopy()`. What does `a[:]` NOT
  protect you from, if the list contains other mutable objects (like the
  list-inside-a-tuple from mutability-tribunal)?
