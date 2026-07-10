# Activity: Capture Court

A round of verdicts on lambda **capture** semantics: the single most
important -- and most frequently gotten-wrong -- part of writing
lambdas in C++. This activity has no programs to compile; every
question is a decision or a definition, built from a short code
fragment. It covers what a **closure** actually is, the difference
between capturing a variable **by value** (a frozen private copy) and
**by reference** (a live link back to the original), what `[=]` and
`[&]` capture by default, when a lambda needs no capture list at all,
what an **init-capture** computes, and the single most dangerous
capture mistake in C++: a reference capture that outlives the variable
it refers to.

## Background

A **closure** is the concrete object a lambda expression builds at the
exact point in the code where it is written. It bundles the compiled
lambda body together with its captured variables into one callable
object. A **capture list** -- the `[...]` at the start of a lambda --
controls which variables from the surrounding scope that closure gets
access to, and how:

- `[x]` captures `x` **by value**: a private copy, frozen at creation
  time, unaffected by anything that happens to the real `x`
  afterward.
- `[&x]` captures `x` **by reference**: a live link to the original
  `x`, always reflecting its current value, including changes made
  after the lambda was created.
- `[=]` and `[&]` are **default-capture** markers: instead of naming
  each variable individually, they automatically capture every
  variable the lambda body actually uses -- `[=]` by value, `[&]` by
  reference.
- A capture list is only for reaching OUT to variables that already
  exist in the enclosing scope. A lambda's own **parameters** (the
  `(...)` list) are not captures at all -- they are supplied fresh on
  every call, exactly like a plain function's parameters.
- `[y = x + 1]` is an **init-capture**: it creates a brand-new
  captured variable, initialized once, to whatever expression you
  write, computed at the moment the lambda is created.

This is exactly the same "reference to something that has gone out of
scope" danger you already know from dangling pointers: capturing a
local variable by reference in a lambda that is called AFTER that
local's scope has ended is undefined behavior, for the same underlying
reason a dangling pointer is.

## Concepts covered

- What a closure is, precisely, and when a new one gets created
- Capture by value vs. capture by reference, and why they diverge
- The default-capture markers `[=]` and `[&]`
- Capture list vs. parameter list -- they are not the same thing
- Init-capture (`[y = x + 1]`)
- The dangling reference-capture trap, tied to what you already know
  about dangling pointers

## How it works

Each question presents a short code fragment and a hint. Type your
answer exactly as the prompt specifies (a number, or one of a small
set of exact phrases). Getting a question wrong shows a detailed
explanation of the capture rule you missed; answer every question
correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every question correctly and the launcher prints
the passphrase.

## Going further

- Take the dangling-capture example from this activity and actually
  compile and run it (with `-fsanitize=address`, if available) --
  does it crash immediately, print garbage, or (worst of all) appear
  to work by pure luck?
- Write a lambda that uses an init-capture to rename a long expression
  to a short, readable local name, and compare it to writing a
  separate named variable just before the lambda instead.
- Once you have worked through this activity, move on to
  sort-with-anything, where you will pass lambdas, functors, and free
  functions as comparators to your own generic sorting code.
