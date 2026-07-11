# Activity: Modernization Bureau

Every piece of C++ code shown in this activity works. That is the problem:
it works using a pre-C++11 idiom that a modern C++ compiler can do better --
more safely, more clearly, or both. You already know the fundamentals this
course covered before now (containers, iterators, lambdas, templates, the
Big Five and move semantics, smart pointers, `auto`). This activity is about
the small, targeted C++11/C++14 features that replace older, riskier
patterns with the same result but fewer ways to get it wrong. None of the
code here uses exceptions -- exception handling is introduced later in this
course, in its own activities.

## Concepts covered

- `nullptr` vs. `NULL`/`0` and why a real null-pointer type matters
- Range-based `for` loops replacing manual iterator loops
- `enum class` (scoped enums) vs. old-style unscoped `enum`
- `auto` replacing long, spelled-out iterator and container types
- Structured bindings (C++17) unpacking a `std::pair` instead of `.first`/`.second`
- `std::array` replacing raw C-style fixed-size arrays
- `using` alias-declarations replacing `typedef`
- Uniform (brace) initialization and the "most vexing parse"
- Delegating constructors
- `= default` and `= delete` for special member functions

## How it works

You are shown ten short snippets, each written in an older, pre-C++11-ish
style. For each one, you must name the exact modern C++ feature that
replaces it. Every explanation shows the fully modernized rewrite and
explains, from first principles, why the replacement is safer or clearer --
you do not need to have memorized the feature going in.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All ten answers are correct and the program prints the passphrase.

## Hints

- Read each snippet's comment carefully -- several point directly at the
  bug or footgun the old-style code has.
- If a question's code declares a variable with a long, nested type just to
  hold the result of one expression, the answer is very likely `auto`.
- If two answers seem close (e.g. `enum class` vs. `enum struct`, or
  `nullptr` vs. `0`), the explanation for the wrong answer spells out
  exactly why the distinction matters.
- Answer with the short technical term itself (a keyword, or the
  feature's usual name, like `auto` or `enum class`) -- not a full
  sentence describing it. If your first guess is a reasonable synonym
  and it is rejected, try the more standard/official name for the
  feature.

## Going further

- Take one of the "before" snippets and actually compile both the old and
  modernized versions with `g++ -std=c++17 -Wall -Wextra`. Do you get any
  extra warnings on the old version that the modernized version avoids?
- Look up `std::string_view` (C++17): why was it *not* included as an
  answer choice in this activity, and what tradeoff does it introduce that
  the other features here do not?
