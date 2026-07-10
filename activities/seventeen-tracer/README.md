# Activity: Seventeen Tracer

C++17 added several small language and library features aimed squarely at
making everyday code shorter and safer, without changing what you already
know about containers, iterators, or `auto`. This activity compiles and
runs six short, fully deterministic programs that exercise those features
directly, so you can *see* what they do instead of just reading about them.
Exception handling is not used anywhere in this activity -- it is
introduced later in this course, in its own activities.

## Concepts covered

- Structured bindings: unpacking a `std::pair` (or a map element) into
  individually named variables in one declaration
- `if` with an initializer statement (`if (init; condition)`) and its
  tight scoping
- `std::optional<T>` as a type-safe "maybe" value, checked with
  `has_value()`/`value_or()`
- Variable shadowing inside a tightly scoped `if`-initializer
- `std::string_view` as a non-owning view over existing character data

## How it works

You are shown six short C++17 programs, one at a time. Before running
anything, predict each program's exact console output. Once you answer,
the activity compiles and runs the real program (with `g++ -std=c++17`) and
checks your prediction against the real result. Every snippet has been
verified deterministic at both `-O0` and `-O2`, so your prediction should
not depend on which optimization level a real compiler happens to use.

## Getting started

```bash
python3 launch.py
```

Requires a working `g++` or `clang++` on your `PATH` with C++17 support.

## You will know you are done when...

All six predictions are correct and the program prints the passphrase.

## Hints

- Structured bindings follow the exact same copy-vs-reference rule plain
  `auto` does: no `&` written means an independent copy, `&` means a real
  reference into the original object.
- A variable declared inside an `if`-initializer (`if (auto it = ...; ...)`)
  does not exist outside that `if`/`else` -- it is not visible to any code
  after the whole `if` statement ends.
- `std::optional<T>::value_or(fallback)` never throws and never reads
  garbage -- it either returns the real held value, or exactly the
  fallback argument you passed it.

## Going further

- Try `std::optional<int>::value()` (not `value_or`) on an empty
  `std::optional` outside this activity, in your own scratch file. What
  happens? (This activity deliberately avoids that case -- exceptions are
  covered later in this course.)
- Look up C++17 fold expressions and inline nested namespaces. Why might
  they be harder to demonstrate with a "predict the printed output"
  activity like this one?
