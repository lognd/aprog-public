# Study Guide 47: Python Data Types

This module drills which Python built-in types are mutable versus
immutable (and what that implies for aliasing and `+=`), plus numeric
nuances where Python's rules diverge from C++'s: floor vs. true division,
banker's rounding, sign of `%`, and why `is` must never be used to compare
numbers.

## Know before you start

- Names as labels bound to objects, and assignment sharing one object
  between two names [assumed: row 45 -- Intro to Python]
- `is` vs. `==` [assumed: row 45 -- Intro to Python]
- IEEE 754 floating point representation and why exact equality
  comparisons are unreliable [assumed: row 5 -- Variables & Type]
- C++ `int / int` truncation and `%`'s sign-follows-dividend rule as the
  contrast point [assumed: row 5 -- Variables & Type]
- `const` vs. mutable objects, and pass-by-value vs. pass-by-reference, as
  the C++ analogy for Python's mutability question [assumed: row 13 --
  Const; row 11 -- Pointers]

## Taught here

Concept: mutability
- Know `str` and `tuple` are immutable: every "modifying" operation
  (`.upper()`, slicing, `+=`) builds a brand-new object and rebinds a
  name to it, leaving the original object untouched.
- Know `list`, `dict`, and `set` are mutable: methods like `.append()`
  change the object in place, and every alias (every other name bound to
  the same object) sees the change through it.
- Know a tuple's immutability only protects its own slots -- a mutable
  object (like a list) stored inside an immutable tuple can still be
  mutated through that slot, even though the tuple itself cannot be
  reassigned a different element.
- Know `+=` behaves completely differently depending on type: in-place
  mutation for `list`, but rebind-to-a-new-object for `str`, `tuple`, and
  `int`.
- Know hashability: `dict` keys and `set` elements must be immutable
  (hashable), because a mutable key's hash could change after insertion
  and corrupt the container's internal bucket placement -- Python raises
  a `TypeError` when a mutable type like `list` is used as a key.
- Know `bool` is a genuine subtype of `int` in Python (`True == 1`,
  `False == 0`); `None` is Python's guaranteed singleton "no value"
  object.
- Be able to track objects, not names: after `b = a`, both names point at
  the SAME object; a mutation reaches through either name to that one
  object, while a rebinding moves only one name's arrow to a new object.

Concept: numeric nuances
- Know binary floating point (Python `float`, the same IEEE 754 format as
  C++ `double`) cannot represent most decimal fractions exactly, so
  `0.1 + 0.2 == 0.3` is `False` -- the same underlying reason as in C++.
- Know `round()` uses banker's rounding (round-half-to-even) for exact
  `.5` ties, not "always round up."
- Know `/` is true division (always returns a `float`, even for two ints)
  and `//` is floor division (rounds toward negative infinity); `//` only
  matches C++'s `int / int` truncation for non-negative operands --
  `-7 // 2` is `-4` (floor), not `-3` (truncation toward zero).
- Know `%`'s sign follows the DIVISOR in Python (the opposite of C++,
  where it follows the dividend), and that `(a // b) * b + (a % b) == a`
  always holds, letting `%`'s sign be derived algebraically instead of
  memorized.
- Know `int()` has two different jobs: parsing a `str` into an integer,
  and truncating a `float` toward zero into an integer.
- Know Python's `int` has no fixed width and never overflows.
- Know `is` must never be used to compare numbers for equality, even
  though it can appear to "work" for small values -- whether two
  separately-created equal integers are the same object is an
  unguaranteed CPython implementation detail (small integer caching),
  not a language rule.

## Study checklist

- [ ] Classify str, tuple, int, list, dict, set as mutable or immutable.
- [ ] Predict output for += on a list vs. a str with an alias present.
- [ ] Explain why a list inside a tuple can still be mutated.
- [ ] Explain why a mutable type cannot be a dict key.
- [ ] Compute -7 // 2 and -7 % 2 by hand using the (a//b)*b + a%b == a
      identity.
- [ ] Explain why 0.1 + 0.2 == 0.3 is False.
- [ ] Explain why is is unsafe for comparing numbers.

## Practiced in

`mutability-tribunal`, `numeric-nuances`
