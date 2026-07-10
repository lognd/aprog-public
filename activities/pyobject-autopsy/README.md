# Activity: PyObject Autopsy

Python is a C program. Every value you have ever created in Python -- an
`int`, a `str`, a `list`, an instance of a class you wrote -- is, underneath,
a plain C struct sitting on the heap, and every Python name is a pointer to
one of those structs. You already know structs (row 19), you already know
pointers (row 11), and you already know refcounting as automated shared
ownership (`who-frees-this`, row 27's smart pointers) -- this activity does
not teach you anything conceptually new. It just shows you where those exact
ideas were hiding the whole time you have been writing Python: inside
`PyObject`, `PyVarObject`, and the small handful of real (simplified)
CPython structs walked field by field below.

## Identity vs equality, at the struct level

`is` and `==` look like two spellings of "the same," but underneath they
are completely different operations. `is` reads the raw memory address of
each operand's `PyObject` struct -- exactly the number `id()` returns -- and
compares the two addresses directly. No Python code runs during that
comparison; nothing a class defines can change what `is` reports. `==`, on
the other hand, is dispatched (through `ob_type`, the same field this
activity opens with) to the operand's own `__eq__` method (the same dunder
method `dunder-decoder` introduces) -- an ordinary Python function that can
be written to return whatever its author wants, correctly or dishonestly.
That asymmetry -- one comparison the interpreter performs directly, one
routed through user-writable code -- is the mechanical reason `is` and `==`
can disagree, and the reason later questions in this activity ask you to
say, precisely, which one a class can lie about.

## Interned things and cached things

Not every object CPython reuses is reused for the same reason. Some
objects are genuinely guaranteed to be singletons -- there is exactly one
of them, ever, for the life of the process -- and some are merely cached as
an optimization, with no promise attached. Relying on the first is safe;
relying on the second is a bug waiting for a different CPython build,
version, or code path to break it.

| Category | Examples | Safe to rely on `is` for? |
|----------|----------|----------------------------|
| Guaranteed singletons | `None`, `True`, `False` | Yes -- exactly one struct each, for the whole process |
| Implementation-detail caches | string interning, the small-int cache (roughly -5 to 256) | No -- an optimization CPython is free to change; use `==` |

`x is None` is the one place `is` is the *preferred* idiom, precisely
because `None` is a guaranteed singleton and no class's `__eq__` can
intercept it. String interning and small-integer caching can make `is`
*look* like it works on strings or numbers -- but neither is a language
guarantee, both have documented exceptions, and `numeric-nuances` already
tells you why: never use `is` for numbers. This activity gives that rule
its C-level reason.

## Concepts covered

- `PyObject`: the two fields (`ob_refcnt`, `ob_type`) every single Python
  object carries, no matter its type
- reference counting as the exact same shared-ownership mechanism as
  `std::shared_ptr`, running automatically underneath every Python name
- the honest limit of refcounting alone (reference cycles) and the separate
  cyclic garbage collector that catches what refcounting cannot
- `PyVarObject`: the extra `ob_size` field that variable-sized types
  (`list`, `tuple`, `str`) carry and fixed-size types (`float`, `bool`) do not
- `PyListObject`'s `ob_item` array of `PyObject*` pointers -- the literal
  mechanism behind list aliasing and mutation-through-two-names
- why rebinding a name to a new value is cheap: a pointer swap plus refcount
  bookkeeping, never a conversion or a copy
- `id()` as a CPython implementation detail (a memory address), not a
  language guarantee
- why `sys.getrefcount()` should never be asserted against an exact number
- `allocated` vs. `ob_size` on a list: capacity vs. length, the same
  distinction `std::vector` draws between `capacity()` and `size()`
- `is` vs `==` at the struct level: `is` is a raw address comparison
  nothing can intercept; `==` dispatches to a class's own `__eq__`, which
  can be written to say anything
- string interning: why identical literal strings can share one struct
  (making `is` look like it works) while a runtime-built equal string
  usually does not, and why `==` is the only comparison you can trust for
  string contents
- `PyLongObject`'s variable-length `ob_digit` array -- the C-level reason
  Python's `int` never overflows, no matter how large
- the `None`/`True`/`False` singletons: exactly one struct each, for the
  whole process, which is what makes `x is None` an exact, unfakeable
  check and `x == None` a check a custom `__eq__` could lie about

## How it works

The launcher shows you fifteen questions, one at a time, each built around a
real (simplified) CPython struct definition or a short Python snippet. Read
the code, think through the C-level mechanics, and type your answer exactly
as shown in the prompt's "Type exactly one of:" list. A correct answer shows
an explanation and moves you on; a wrong answer shows an explanation of the
specific misconception behind that particular guess, then re-prompts. All
fifteen must be correct to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all fifteen questions and the launcher shows you
a passphrase.

## Hints

<details>
<summary>Hint 1 -- every question reduces to "what does this struct actually store?"</summary>

`PyObject` has exactly two fields. `PyVarObject` adds exactly one more.
`PyListObject` adds exactly two more on top of that. When a question feels
hard, go back to the specific struct definition printed with it and ask,
field by field, what each one is actually for -- the answer is almost always
sitting in the struct itself, not somewhere you have to guess.

</details>

<details>
<summary>Hint 2 -- you have already learned every mechanism here, just in C++</summary>

Refcounting is `std::shared_ptr`. A reference cycle is the same leak
`shared_ptr` has, with the same fix (a separate, deliberate mechanism, not
something plain counting does for free). A list of pointers instead of
objects is exactly why two `std::vector<Widget*>` variables could alias the
same underlying `Widget`s. `allocated` vs. `ob_size` is `capacity()` vs.
`size()`. If a question stumps you, ask "what was the C++ version of this
called?"

</details>

## Going further

- Read the real `PyObject`, `PyVarObject`, and `PyListObject` definitions in
  CPython's own source: search `Include/object.h` and
  `Include/cpython/listobject.h` on <https://github.com/python/cpython>. The
  structs in this activity are simplified and faithful, but the real ones
  have a few extra, build-configuration-dependent fields.
- Compare `sys.getsizeof(0)`, `sys.getsizeof(10**100)`, and
  `sys.getsizeof(10**1000)`. Since `int` is internally variable-sized
  (arbitrary precision), does the reported size grow, and does it grow the
  way you would predict from `PyVarObject`'s `ob_size` field?
- With `ctypes`, you can peek at an object's raw `ob_refcnt` directly
  instead of going through `sys.getrefcount()`'s extra temporary reference:
  `import ctypes; ctypes.c_long.from_address(id(obj)).value`. Try it, but do
  not build real code around it -- like everything else about a raw
  refcount value, it is an implementation detail, not something to depend
  on.
- This activity is the conceptual foundation for a CPython-internals
  project planned later in the course, where you will get to poke at (and
  eventually modify) a real interpreter build -- no specifics yet, since
  that project has not been built.
