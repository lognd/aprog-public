# Activity: Throw-or-Not Court

Knowing the `throw`/`try`/`catch` syntax is only half of using exceptions
well -- the other half is judgment: deciding *when* an exception is the
right tool, versus when a return value (a `bool`, a `std::optional`, or a
sentinel value, the styles this course used before exceptions existed as
an option) fits better. This activity has no code to read. Every question
is a scenario or a direct question about that judgment call, phrased so
you can reason it out from first principles rather than recall a rule.

## Concepts covered

- When a failure is routine and expected (handle it with a return value)
  versus genuinely exceptional (handle it with an exception)
- Why a constructor that cannot establish its class's invariants (the
  conditions that must hold for every valid object of that class) has no
  option but to throw
- Why a destructor should never throw, and what `std::terminate` does
- Exceptions on performance-critical hot paths, and the precondition +
  `assert()` alternative
- The `catch (...) { }` empty-catch-all anti-pattern
- `noexcept` as a promise the compiler is allowed to optimize around
- The basic exception-safety guarantee (invariants survive; the exact
  resulting value is not promised) versus the stronger guarantees you may
  encounter later

## How it works

You are given nine scenarios or direct questions, one at a time, each with
an answer format constrained to a short, exact phrase (so there is no
ambiguity about what counts as correct). Every explanation, right or wrong,
walks through the reasoning from scratch -- this activity does not assume
you have seen any of these terms before.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All nine answers are correct and the program prints the passphrase.

## Hints

- Ask yourself: is this failure something the *immediate* caller already
  expects and can react to right there, or is it a condition far away
  from anywhere that could sensibly recover?
- Constructors are a recurring special case throughout this activity: they
  have no return type at all, so they cannot report failure the way an
  ordinary function can.
- "Never" and "always" answers in this activity are backed by a concrete
  mechanism (like `std::terminate`), not just convention -- the
  explanations spell out exactly what breaks if you go the other way.

## Going further

- Revisit the RAII payoff snippet in this course's companion activity,
  Unwind Tracer, and connect it to this activity's destructor-and-throw
  question: why does RAII cleanup being reliable during unwinding depend
  on destructors never throwing?
- Look up the strong exception-safety guarantee and the "copy-and-swap"
  idiom that is commonly used to implement it.
