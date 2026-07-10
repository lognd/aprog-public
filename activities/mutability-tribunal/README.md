# Activity: Mutability Tribunal

You already know the difference between a `const` object and a mutable one
in C++, and the difference between passing by value and passing by
reference. Python asks a related but differently-shaped question about
every object: is this TYPE mutable at all, or is every operation on it
secretly building a brand-new object and rebinding a name to it? This
activity puts nine short programs on trial, one type at a time, so you can
build the instinct for which of Python's built-in types can be changed in
place and which only look like they can.

## Concepts covered

- `str` and `tuple` are immutable: every "modifying" operation (`.upper()`,
  slicing, `+=`) builds a new object and rebinds a name, leaving the
  original untouched
- `list`, `dict`, and `set` are mutable: methods like `.append()` change
  the object in place, and every alias (every other name bound to the same
  object) sees the change
- a tuple's immutability only protects its own slots -- a mutable object
  (like a list) stored inside an immutable tuple can still be mutated
- `+=` behaves completely differently depending on the type: in-place
  mutation for `list`, rebind-to-a-new-object for `str`, `tuple`, and `int`
- hashability: why `dict` keys and `set` elements must be immutable, and
  what error a mutable key produces
- `bool` as a genuine subtype of `int`, and `None` as Python's guaranteed
  singleton value

## How it works

The launcher shows you nine short Python programs, one at a time. Read the
code, predict exactly what it prints, and type your prediction (entering
each line separately if the output has more than one line). A correct
guess shows a short explanation and moves you on; a wrong guess shows the
actual output and, for many wrong answers, an explanation of the specific
misconception behind that particular guess. Every snippet actually runs on
your own Python interpreter -- nothing here is scripted or faked.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all nine snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask "does this type have ANY mutating method?"</summary>

For every snippet, before predicting the output, ask yourself: does the
type of the object involved (`str`, `tuple`, `int`, `list`, `dict`, `set`)
have any method that changes the object's contents in place, or does
every operation on it necessarily build something new? `str`, `tuple`,
and `int` are all immutable -- no method or operator on them ever mutates
the object itself, no matter how much the syntax might look like it does.

</details>

<details>
<summary>Hint 2 -- track objects, not names</summary>

When two names (`a` and `b`) are involved, draw two boxes labeled `a` and
`b`, and one circle for the actual object. After `b = a`, both boxes point
at the SAME circle -- there is only one object. A mutation reaches through
either box to the same circle. A rebinding (`a = a + 1`, or any `=` after
the first one) draws a brand-new circle and moves only one box's arrow to
point at it; the other box's arrow does not move.

</details>

<details>
<summary>Hint 3 -- run it yourself</summary>

If you are unsure, nothing stops you from opening a second terminal,
pasting the snippet into a Python file, and running it before you answer.
Predicting correctly matters more than predicting from memory.

</details>

## Going further

- Write a function that takes a list and appends to it, and a separate
  function that takes an int and "increments" it by rebinding its local
  parameter. Call both from a caller that prints the argument afterward.
  Which one visibly changed, and why?
- `frozenset` is an immutable version of `set`. Look up what problem it
  solves -- specifically, what can a `frozenset` do that a plain `set`
  cannot (hint: think about what mutability-tribunal's snippet 6 says
  about hashability).
- Try `id(a)` before and after a mutation versus before and after a
  rebinding, for both a list and a str. `id()` returns a unique number for
  each object -- does it change?
