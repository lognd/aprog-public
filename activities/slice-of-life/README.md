# Activity: Slice of Life

**Slicing** is what happens when an object of a derived type gets copied
into something declared as its base type: only the base-class part of the
object survives the copy, and everything the derived class added -- extra
fields, and any overridden behavior -- is silently cut off ("sliced away").
The resulting object is not a derived object in disguise; it is a genuine,
complete base object, nothing more. This activity walks through exactly
when slicing happens, when it does not, and how to avoid it, by predicting
the exact output of small compilable programs.

---

## Concepts covered

- **Slicing**: copying a derived object into a base-typed variable, parameter,
  or container element, discarding the derived-only parts
- Pass-by-value (which copies, and therefore slices) vs. pass-by-reference
  (which does not copy, and therefore does not slice)
- `std::vector<Base>` (stores actual objects, slices every insertion) vs.
  `std::vector<Base*>` of non-owning pointers to stack objects (stores
  addresses, never slices)
- Which constructor runs during a slicing copy (the base class's own copy
  constructor, never a derived one)
- Slicing discards derived-only data fields, not just derived-only behavior

## How it works

Each snippet is a complete, compilable C++ program built around a small
`Base`/`Derived` pair with a virtual function. None of these snippets use
heap allocation (`new`/`delete`) -- only stack objects and, where a container
of pointers is used, non-owning raw pointers to those stack objects (pointers
that point at an object but do not own or manage its lifetime). The launcher
compiles and runs each snippet with `g++`, and you type the exact output.

## Getting started

```bash
python3 launch.py
```

For each snippet, identify every place a `Derived` object is copied into
something typed as `Base` -- an assignment, a by-value function parameter, or
an insertion into a `std::vector<Base>`. Anywhere that happens, the result
behaves as a plain `Base`, not a `Derived`, no matter what the original
object was. Type your predicted output for each snippet.

## You will know you are done when...

Once you correctly predict every snippet's output, the launcher prints a
passphrase.

## Hints

<details>
<summary>Hint 1 -- when exactly does a copy happen?</summary>

Slicing requires an actual COPY of an object into a base-typed slot. Look
for: `Base b = someDerived;` (copy-initialization), a function parameter
declared as `Base` (not `Base&` or `Base*`) receiving a `Derived` argument,
or `push_back`/`emplace_back` into a `std::vector<Base>`. If instead you see
a reference (`Base&`) or a pointer (`Base*`) being used, no copy is being
made, and nothing is sliced -- the reference or pointer still refers to the
original, complete `Derived` object.

</details>

<details>
<summary>Hint 2 -- vector<Base> vs. vector<Base*></summary>

A `std::vector<Base>` allocates storage sized for `Base` objects -- each slot
is exactly `sizeof(Base)` bytes, with no room for anything a derived class
might add. Inserting a `Derived` object copies (and therefore slices) it down
to fit. A `std::vector<Base*>` instead stores pointers -- each slot is just
the size of an address, regardless of what it points to -- so inserting
`&someDerivedObject` stores the address of the real, complete object with no
copying and no slicing at all.

</details>

<details>
<summary>Hint 3 -- which copy constructor runs?</summary>

When a `Derived` object is copied into a variable declared as `Base` (for
example `Base b(someDerived);`), the compiler is constructing a `Base`
object, so it uses `Base`'s own copy constructor -- there is no such thing as
`Derived`'s copy constructor being invoked to build a `Base`. This copy
constructor only knows how to copy the fields `Base` itself declares; any
extra fields `Derived` added are simply not copied, because `Base`'s copy
constructor has no knowledge that they exist.

</details>

## Going further

- Take one of the slicing snippets and fix it two different ways: first by
  changing a by-value parameter to a reference, and second by changing a
  `std::vector<Base>` to a `std::vector<Base*>`. Confirm both fixes produce
  the derived behavior.
- Add a second derived class, `MoreDerived`, and predict what happens if you
  slice it into a `Base` -- does it matter how many levels of inheritance are
  involved, or does slicing always cut straight down to the exact static
  type of the destination?
- Research why some codebases disable slicing outright by deleting the base
  class's copy constructor and copy-assignment operator, or by making the
  base class's destructor `protected` -- both are real techniques used when a
  class hierarchy is meant to be used only through references or pointers,
  never copied by value.
