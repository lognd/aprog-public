# Study Guide 45: Intro to Python

This module is the first Python exposure of the course, aimed at
un-learning specific C++ assumptions Python quietly breaks: division
semantics, unbounded integers, names-as-labels instead of typed storage,
identity vs. equality, and Python's total lack of `{}`-based block scope.

## Know before you start

- C++ `int` overflow and fixed-width integer types [assumed: row 5 --
  Variables & Type]
- C++ `{}` block scope and variable shadowing [assumed: row 6 -- Control &
  Functions]
- Pointers vs. value copies, and what "two names for the same object"
  means [assumed: row 11 -- Pointers]
- `std::vector` slicing/copy-on-assignment behavior as the contrast point
  for Python list slicing [assumed: row 7 -- Standard Library Types]

## Taught here

Concept: bare Python syntax, contrasted with the equivalent C++ construct
- Know `print()` is Python's equivalent of `std::cout`, and that a Python
  name (`x = 5`) has no fixed type the way a C++ variable declaration
  does -- the same name can be rebound to a value of any type later.
- Be able to read `def`/`return` for a function definition, `if`/`elif`/
  `else`, `for x in range(n)`, `for x in a_list`, and `while`, and know
  that Python marks each block with a trailing colon `:` plus indentation
  instead of C++'s `{ }`.
- Be able to read an f-string (`f"{name} is {age}"`) as Python's built-in
  way of building text with values inside it, `len()` as the equivalent of
  a length/size query, and a list literal with `.append()` as the
  closest analog to a growable `std::vector`.
- Know a dictionary literal (`{"key": value}`) and key-based lookup with
  `[ ]` has no single-token C++ equivalent, though `std::map` plays a
  similar role.

Concept: numbers behave differently
- Know Python splits what C++'s `int / int` does into two separate
  operators: `/` is true division (always returns a float, even for two
  ints), `//` is floor division (the C++-like truncating-toward-negative-
  infinity operator, not the same as C++'s truncate-toward-zero `int/int`
  for negative operands).
- Know Python's `int` has no fixed width and never overflows -- arbitrary
  precision is baked into the language itself, unlike C++'s fixed-width
  `int`.

Concept: names are labels, not typed storage
- Know a Python name is a label bound to an object, not a typed storage
  slot -- the same name can be rebound to an object of any type at any
  time.
- Know plain assignment (`b = a`) makes `b` a second label for the SAME
  object `a` already refers to, closer to copying a C++ pointer than to
  copying a `std::vector`'s contents.
- Know `is` (identity: are these two names the SAME object) and `==`
  (value equality: do these two objects compare equal) ask two entirely
  different questions, and are not interchangeable.
- Know list slicing (`a[1:3]`) always produces a brand-new, independent
  list (a copy), unlike a pointer-offset view or `std::span`.
- Know negative indexing (`a[-1]` for the last element) has no
  `std::vector::operator[]` equivalent at all.
- Know Python evaluates the ENTIRE right-hand side of an assignment
  before performing any of the individual bindings, which is exactly what
  makes `a, b = b, a` swap safely without a temporary variable.

Concept: indentation as syntax, and no block scope
- Know Python has no `{}` -- indentation itself is the syntax marking
  where a block begins and ends, and every block-opening line (`if`,
  `for`, `while`, `def`, `class`, ...) requires a trailing colon `:`.
- Know Python's `if`/`for`/`while`/`with` blocks create NO new variable
  scope -- a variable assigned inside one of them is a normal variable in
  the enclosing scope, visible both before (if already assigned) and
  after the block ends; only `def`, `class` bodies, `lambda`, and
  comprehensions create a new scope.
- Know every Python function returns a value even with no explicit
  `return` statement -- it implicitly returns `None`.
- Know truthiness: values that count as `False` in a condition without
  being the literal boolean `False`, including empty containers (`[]`,
  `""`, `{}`), `0`, and `None`.
- Know the `is None` convention (not `== None`) for checking "no value
  here," preferred because `is` cannot be fooled by a custom `__eq__`
  that redefines what counts as equal to `None`.

## Study checklist

- [ ] Predict the output of a snippet mixing / and // on ints and floats.
- [ ] Explain why 2**100 does not overflow in Python.
- [ ] Explain the difference between rebinding a name and mutating an
      object, using b = a as the example.
- [ ] Distinguish is from == with a concrete pair of objects.
- [ ] Explain why a[1:3] copies while a C++ span-like view would not.
- [ ] State which Python block constructs create a new scope and which do
      not.
- [ ] List which values are falsy without being literally False.

## Practiced in

`python-syntax-boot-camp`, `python-culture-shock`, `indentation-court`
