# Activity: Dunder Decoder

You already know classes: constructors, member functions, inheritance,
`virtual`, operator overloading. Python's OOP syntax looks different --
`__init__` instead of a constructor named after the class, an explicit
`self` where C++ has an implicit `this`, methods named with double
underscores ("dunders") like `__str__` and `__eq__` instead of overloaded
operators -- but underneath, most of it maps directly onto something you
already know. This activity is eight small class-based programs that make
that mapping concrete, plus one genuine difference with real consequences:
Python has no `virtual` keyword, because *every* method is dynamically
dispatched, always.

## Concepts covered

- `__init__` as the constructor; `self` as an explicit, hand-written
  parameter standing in for C++'s implicit `this`
- `__str__` (used by `print()`) and `__repr__` (used by `repr()`, and by
  containers displaying their elements) as the two halves of what C++
  covers with a single `operator<<` overload
- `__eq__` and Python's silent default: `==` with no `__eq__` override
  falls back to identity comparison, not a compile error the way C++'s
  missing `operator==` would be
- inheritance and `super().__init__(...)`, replacing C++'s
  member-initializer-list base-class call
- no `virtual` keyword -- every method call is dynamically dispatched,
  unconditionally
- class attributes (shared, closest to a C++ `static` member) vs. instance
  attributes, and how assigning through an instance shadows, rather than
  modifies, a class attribute
- duck typing: calling a method on an object with no shared base class or
  declared interface at all

## How it works

The launcher shows you eight short Python class-based programs, one at a
time. Read the code, predict exactly what it prints
(entering each line separately if the output is more than one line), and
type your prediction. A correct guess shows a short explanation and moves
you on; a wrong guess shows the actual output and, for many wrong answers,
an explanation of the specific misconception behind that particular guess.
Every snippet actually runs on your own Python interpreter -- nothing here
is scripted or faked.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all eight snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- run it yourself</summary>

As with any prediction activity, if you are unsure, copy the snippet into
a file and run it. The goal is to understand *why* the output is what it
is, not to guess correctly by luck.

</details>

<details>
<summary>Hint 2 -- ask "which class's method actually runs?"</summary>

Several snippets hinge on dynamic dispatch: when you call `obj.method()`,
Python always looks at `obj`'s *actual* runtime class first, and walks
upward through its base classes from there. There is no separate "static"
lookup path the way an un-`virtual`-marked C++ method has.

</details>

## Going further

- Add a `__lt__` method to a class (Python's hook for `<`) and try sorting
  a list of instances with `sorted()`. What happens if you sort without
  defining `__lt__` at all?
- Python's default `__eq__` (identity) also affects using an object as a
  dictionary key or set element, via a related dunder, `__hash__`. Look up
  what happens if you define `__eq__` without also defining `__hash__`.
- Write a `Cat` class with its own `speak()` method but *no* shared base
  class with `Dog` at all, then call both through the exact same function.
  Confirm for yourself that Python never asked whether `Cat` and `Dog` were
  related.
