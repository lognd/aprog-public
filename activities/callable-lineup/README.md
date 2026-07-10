# Activity: Callable Lineup

A **callable** is anything that can be invoked with `()`, the way a
function can. C++ has three different species of callable, and this
activity walks through all three side by side: a **function pointer**
(a variable holding the address of a function, called through it), a
**functor** (a struct or class with an `operator()` member, so an
object of that type can be "called" like a function), and a **lambda**
(an inline, unnamed callable you write right where you need it,
optionally with a **capture list** that pulls variables in from the
surrounding scope). Every snippet is a short, deterministic C++
program -- predict its exact output, then the launcher compiles and
runs it with `g++` to check your answer.

## Background

Up through sorting, every comparison you have written has been
hardcoded directly into the algorithm (`if (v[i] > v[j])`). This
activity is the payoff moment: once behavior can be passed around as a
value -- a function pointer, a functor object, or a lambda -- an
algorithm like `std::sort` can be written ONCE and reused with any
comparison rule the caller supplies, instead of being rewritten for
every new rule.

The gnarliest syntax here is the function pointer declaration itself:
`bool (*pred)(int)` declares `pred` as a variable that can hold the
address of any function taking an `int` and returning a `bool`. Read
it from the inside out: `pred` is a pointer to a function `(int) ->
bool`. The parentheses around `*pred` are required -- without them,
`bool *pred(int)` declares something completely different (a function
returning `bool*`).

A **closure** is the actual object a lambda expression builds at the
point it is written: it bundles the lambda's compiled body together
with whatever it captured. Capturing a variable **by value** (`[x]`)
takes a frozen private copy at the moment the lambda is created,
completely disconnected from the original afterward. Capturing **by
reference** (`[&x]`) instead stores a live link back to the original
variable, so the lambda always sees its current value -- including
changes made after the lambda was created. `mutable` lifts the default
restriction that a value-capturing lambda's own copies are read-only,
letting the lambda's internal state change across repeated calls.

## Concepts covered

- Function pointer declaration and call syntax: `bool (*pred)(int)`
- Passing a function pointer as a parameter (the comparator pattern)
- Functors: a struct with `operator()`, carrying state across calls
- Lambdas assigned to `auto` and called
- Capture by value `[x]` vs. capture by reference `[&x]`, and why they
  diverge once the captured variable changes after the lambda is made
- `mutable` lambdas, whose internal value-captured copies can change
  across calls
- Passing a lambda directly to `std::sort` as a comparator

## How it works

Each snippet shows a short C++ program. Predict its exact output, then
the launcher compiles and runs it with `g++` to check your answer.
Getting a snippet wrong shows a detailed explanation of the callable
mechanics you missed; predict every snippet correctly to reveal the
passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of every snippet and the
launcher prints the passphrase.

## Going further

- Rewrite the function-pointer snippets (`isPositive`, `countMatching`)
  using a lambda passed directly as the third argument instead of a
  named function -- does the calling code get simpler?
- Write your own functor with two `operator()` overloads (e.g. one
  taking an `int`, one taking a `double`) and see which one gets
  called for different argument types.
- Try capturing the SAME variable both by value and by reference in
  two different lambdas in the same scope, then change the variable
  and call both lambdas again later -- confirm the divergence for
  yourself before moving on to capture-court.
