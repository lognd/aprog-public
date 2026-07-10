# Activity: Dispatch Detective

Every function call in C++ has to be resolved to an actual piece of code
somewhere. Sometimes the compiler can figure out exactly which code that is
just by reading your source file -- before the program ever runs. Other
times, the right code can only be picked once the program is actually
running, by looking at the real object involved. This activity is about
telling those two situations apart, precisely, and about a few gotchas
where the difference produces genuinely surprising output.

## Concepts covered

- Static dispatch (decided at compile time) vs. dynamic dispatch (decided
  at run time)
- The vtable: the hidden per-class table of function pointers that makes
  dynamic dispatch work
- Static type (the declared type in your source code) vs. dynamic type
  (the actual, concrete object at runtime)
- Default arguments on virtual functions being bound statically -- a
  classic gotcha
- Object slicing: what happens when a derived object is copied into a
  base-typed variable by value
- Overload resolution as a separate, always-compile-time mechanism

## How it works

You are shown seven small, complete C++ programs, one at a time. Each one
compiles and runs. Your job is to predict EXACTLY what it prints -- not
roughly, not "something like it" -- character for character. Once you
type a prediction, the activity actually compiles and runs the program (it
never just tells you the "correct" answer from a script) and compares your
prediction against the real output.

If you are wrong, you are shown the real output and asked to type it
exactly before moving on, so you always leave with the correct answer
fixed in your mind, along with a full explanation of why the program
behaves the way it does.

A term you will see repeatedly is DYNAMIC TYPE versus STATIC TYPE. The
STATIC TYPE of a variable is whatever type is written in its declaration
in the source code (for example, `Base&` in `Base& ref = derivedObject;`)
-- it is fixed and known to the compiler without running anything. The
DYNAMIC TYPE is the actual, concrete type of the object that variable
refers to at runtime (in that example, it might really be a `Derived`).
Most of this activity is about which of the two -- static type or dynamic
type -- actually decides what a given piece of code does.

## Getting started

```bash
python3 launch.py
```

Requires `g++` (or `clang++`) with C++17 support on your PATH.

## You will know you are done when...

You have correctly predicted the exact output of all seven snippets, and
the activity prints your passphrase.

## Hints

- Draw two boxes for every variable involved: one for its static type
  (what the source code declares) and one for its dynamic type (what
  object it actually refers to). Dispatch questions almost always reduce
  to "which of these two boxes actually decides the answer here?"
- `virtual` on a function is what makes dynamic dispatch possible for
  calls made through a reference or a pointer to that type. No `virtual`
  keyword means no vtable involvement at all, and the call is resolved
  purely by static type.
- Passing or storing an object BY VALUE where a base type is expected
  always copies just the base part -- this is object slicing, and it
  happens regardless of whether any function involved is virtual.
