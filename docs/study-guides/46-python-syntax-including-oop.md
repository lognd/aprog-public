# Study Guide 46: Python Syntax (including OOP)

This module maps Python's OOP syntax onto C++ OOP concepts already known
(`__init__`/self as constructor/this, `__str__`/`__repr__` as
`operator<<`, always-dynamic dispatch with no `virtual` keyword), then
covers idiomatic Python style versus C++-habit code that merely works.
`cpp-to-python-phrasebook` ports the word-ledger design to Python, meeting
`dict`, `key=` sorting, and string methods along the way.

## Know before you start

- Constructors, `this`, and member-initializer lists [assumed: row 21 --
  OOP Implementation in C++]
- `operator<<`, `operator==`, and operator overloading generally [assumed:
  row 21 -- OOP Implementation in C++]
- `virtual` dispatch and vtables [assumed: row 22 -- Inheritance]
- `static` class members [assumed: row 21 -- OOP Implementation in C++]
- Names as labels, not typed slots, and no C++-style access enforcement
  contrast point [assumed: row 45 -- Intro to Python]
- `std::map`'s sorted iteration vs. `std::unordered_map`'s hash-table
  layout [assumed: row 33 -- Map & Set ADT]

## Taught here

Concept: Python OOP syntax mapped to C++ OOP
- Know `__init__` is the constructor; `self` is an explicit, hand-written
  first parameter standing in for C++'s implicit `this` -- Python never
  hides it.
- Know `__str__` (used by `print()`) and `__repr__` (used by `repr()` and
  by containers displaying their elements) together cover what C++
  handles with a single `operator<<` overload.
- Know Python's silent default for `==` with no `__eq__` override falls
  back to identity comparison (`is`), not a compile error the way a
  missing `operator==` would be in C++.
- Know inheritance calls the base constructor with `super().__init__(...)`,
  replacing C++'s member-initializer-list base-class call.
- Know Python has no `virtual` keyword because EVERY method call is
  dynamically dispatched, unconditionally -- `obj.method()` always looks
  at `obj`'s actual runtime class first and walks upward through its base
  classes, with no separate "static" lookup path.
- Know class attributes (shared across all instances, closest to a C++
  `static` member) versus instance attributes, and that assigning through
  an instance shadows rather than modifies a class attribute of the same
  name.
- Know duck typing: calling a method on an object works with no shared
  base class or declared interface at all, as long as the method exists.

Concept: idiomatic Python vs. C++-habit Python
- Know direct iteration (`for item in v`) is idiomatic; index-based
  iteration (`for i in range(len(v))`) is a C++ habit that should become
  `enumerate()` when both index and value are genuinely needed.
- Know `sum()` replaces a hand-written accumulator loop.
- Know `str.join()` replaces repeated `+=` string concatenation, and WHY
  it matters: Python strings are immutable, so every `+=` builds an
  entirely new string, making repeated concatenation quadratic.
- Know Python has no `private`/`protected`/`public` -- a leading
  underscore on a name is only a naming CONVENTION, never an enforced
  restriction the way C++ access specifiers are.
- Know `isinstance()` vs. duck typing is a genuinely nuanced choice, not a
  one-line rule.
- Know truthiness is preferred over explicit comparison: `if flag:` over
  `if flag == True:`, `if not names:` over `if len(names) == 0:`.

Concept: porting a design from C++ to Python
- Know `def` has no return-type annotation and no enforced parameter
  types (only optional, unenforced type hints) -- a function can even
  return different types on different calls with nothing checking this at
  runtime.
- Know Python `str` plays `std::string`'s conceptual role but is
  IMMUTABLE: slicing, `+`, and methods like `.lower()` always build a new
  string object, never mutate in place.
- Know Python `dict` plays the associative-container role `std::map`/
  `std::unordered_map` play, but its iteration order is neither of
  those -- it remembers INSERTION order, a third distinct guarantee.
- Be able to port a tokenize-count-rank pipeline (word_count,
  unique_words_sorted, word_frequencies, most_frequent with alphabetical
  tie-breaking, reverse_words via join, palindrome check ignoring
  case/punctuation) from a known C++ design into Python's dict/str
  vocabulary.

## Study checklist

- [ ] Map __init__/self/__str__/__eq__ to their C++ constructor/this/
      operator<< /operator== counterparts.
- [ ] Explain why Python has no virtual keyword.
- [ ] Explain why assigning through an instance shadows rather than
      mutates a class attribute.
- [ ] Rewrite a range(len(v)) loop idiomatically.
- [ ] Explain why str.join beats repeated += for many strings.
- [ ] Explain why a leading underscore is not real access control.
- [ ] Explain the three different iteration-order guarantees: std::map,
      std::unordered_map, and Python dict.

## Practiced in

`dunder-decoder`, `pythonic-or-not`, `cpp-to-python-phrasebook`
