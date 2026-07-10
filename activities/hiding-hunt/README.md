# Activity: Hiding Hunt

When a derived class (a class that extends a base class, reusing and adding
to it) declares a function with the same name as one in its base class, two
very different things can happen depending on a few small details in how
each function is written. The base version can be **overridden** -- properly
replaced so that calling it through a base reference or pointer still runs
the derived version -- or it can be **hidden**: a completely separate,
unrelated function that just happens to share a name, leaving the base
version untouched and, in many situations, still the one that gets called.
This activity trains you to tell the two apart by predicting exact program
output.

---

## Concepts covered

- **Static type** (the type written in the code, known at compile time) vs.
  **dynamic type** (the actual, concrete type of the object at runtime)
- `virtual` functions and dynamic dispatch: calling through a base
  reference/pointer runs the derived override
- Overriding vs. hiding: what makes a derived function actually replace a
  base one, and what silently makes it a stranger with the same name
- Signature mismatches (a missing `const`, for example) that silently turn
  an intended override into a hide
- Virtual calls made from inside a base class constructor always use the
  base version, never a derived override
- `protected` access: available to derived classes, hidden from everyone else

## How it works

Each snippet is a complete, compilable C++ program using only stack objects
and references/pointers to them -- no heap allocation. The launcher compiles
and runs each snippet with `g++` and you must type the exact output it
produces. As with `ctor-dtor-tracer`, this is predict-the-compiler's-actual-
output, not multiple choice: there is one correct answer per snippet, and it
is whatever the program actually prints.

## Getting started

```bash
python3 launch.py
```

For each snippet, read the code and work out, step by step: what is the
static type of the reference or pointer used to make the call? What is the
dynamic type of the object it actually refers to? Is the function being
called `virtual`? Does the derived class's version have the exact same
signature (name, parameters, and `const`-qualification)? Type your predicted
output.

## You will know you are done when...

Once you correctly predict every snippet's output, the launcher prints a
passphrase.

## Hints

<details>
<summary>Hint 1 -- static type vs. dynamic type, concretely</summary>

Given `Derived d; Base& ref = d;`, the STATIC type of `ref` is `Base&` --
that is what is written in the code, and it is all the compiler knows for
sure when compiling `ref.someFunction()`. The DYNAMIC type is `Derived` --
what `ref` actually refers to at runtime. Non-virtual function calls are
resolved using the static type alone. Virtual function calls, when the
function is properly overridden, are resolved using the dynamic type.

</details>

<details>
<summary>Hint 2 -- what turns an "override" into a "hide"?</summary>

For a derived class's function to actually override a base class's virtual
function, its signature must match EXACTLY: same name, same parameter types,
and the same `const`-qualification (a member function's `const` marker is
part of its signature, not just a style choice). If any part differs -- most
commonly, forgetting `const` on the derived version when the base version
has it -- the derived function is an entirely separate function that merely
shares a name. It hides the base name when called directly on a derived
object, but it does not replace the base version in virtual dispatch.
Marking the intended override with the `override` keyword makes the compiler
reject this kind of mismatch outright -- always use it.

</details>

<details>
<summary>Hint 3 -- why does a virtual call inside a base constructor use the base version?</summary>

While a base class's constructor is running (even as part of building a
derived object), the derived part of the object has not been constructed
yet. If a virtual call made from inside that constructor jumped straight to
the derived override, that override might read or use derived-only member
fields that do not have valid values yet. To avoid this, C++ treats the
object as "just a Base" for the duration of Base's own constructor -- virtual
calls made there always resolve to the base version, regardless of what the
object's final, fully-constructed type will be.

</details>

## Going further

- Add a third class, `MoreDerived`, that further extends `Derived`, and
  predict what happens when you call the virtual function through a
  `Base&` pointing at a `MoreDerived` object.
- Deliberately remove the `override` keyword from one of the correctly
  overriding snippets and add a small signature mismatch (an extra
  parameter, a missing `const`). Recompile with `override` back in place
  and confirm the compiler now reports an error instead of silently
  compiling a hide.
- Look up why virtual functions are implemented, in most C++ compilers, with
  a per-class lookup table called a **vtable** (a table of function pointers
  the compiler builds once per class, used to find the correct override at
  runtime). Consider why a hidden (non-overriding) function never appears in
  that table under the base class's slot.
