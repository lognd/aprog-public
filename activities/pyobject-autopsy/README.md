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

## How it works

The launcher shows you ten questions, one at a time, each built around a
real (simplified) CPython struct definition or a short Python snippet. Read
the code, think through the C-level mechanics, and type your answer exactly
as shown in the prompt's "Type exactly one of:" list. A correct answer shows
an explanation and moves you on; a wrong answer shows an explanation of the
specific misconception behind that particular guess, then re-prompts. All
ten must be correct to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all ten questions and the launcher shows you a
passphrase.

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
