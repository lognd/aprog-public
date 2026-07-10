# Activity: Unwind Tracer

`throw`, `try`, and `catch` are C++'s mechanism for reporting and handling
conditions a function cannot recover from locally. This activity is your
first hands-on look at exceptions in this course: seven short, fully
deterministic programs that show exactly what happens, step by step, when
an exception is thrown -- which lines run, which are skipped, and in what
order destructors fire while the stack unwinds (the process of leaving
scopes and destroying their local objects on the way to a matching
`catch`).

## Concepts covered

- `throw` immediately abandoning the rest of the current `try` block
- Catch-clause type matching, tried in source order, first match wins
- Stack unwinding: local objects are destroyed in the exact reverse of
  their construction order
- RAII (Resource Acquisition Is Initialization) cleanup running
  automatically during unwinding, even across multiple function frames
- Rethrowing the current exception unchanged with a bare `throw;`
- Catching by value slicing a derived exception down to its base class

## How it works

You are shown seven short C++ programs, one at a time. Before running
anything, predict each program's exact console output. Once you answer,
the activity compiles and runs the real program (with `g++ -std=c++17`) and
checks your prediction against the real result. Every snippet has been
verified deterministic at both `-O0` and `-O2`.

## Getting started

```bash
python3 launch.py
```

Requires a working `g++` or `clang++` on your `PATH` with C++17 support.

## You will know you are done when...

All seven predictions are correct and the program prints the passphrase.

## Hints

- Whenever a snippet has a class with a constructor and destructor that
  both `printf`, trace through construction order first, then figure out
  where the `throw` happens, then destroy objects in the exact reverse of
  that construction order.
- A `catch` clause never intercepts a thrown type unless that type *is* the
  clause's type, or is derived from it. A near-miss clause (e.g. catching
  `std::logic_error` when a `std::runtime_error` was thrown) provides no
  protection at all.
- `catch (const Type& e)` (by const reference) preserves the real,
  un-sliced object and its virtual overrides. `catch (Type e)` (by value)
  slices a derived exception down to exactly the base-class portion.

## Going further

- Add a fourth `Loud`-style RAII object to the stack-unwinding snippet with
  its own id, and re-derive the expected construct/destruct order by hand
  before running it.
- Look up why a destructor should (almost) never throw, and what
  `std::terminate` is. You will see this reasoning again in this course's
  companion activity on judgment calls, Throw-or-Not Court.
