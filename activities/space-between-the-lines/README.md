# Activity: Space Between the Lines

Every line of code between the moment an object is constructed and the
moment it is actually ready to use is a place someone can insert code that
compiles fine and is broken. That gap is "the space between the lines," and
this activity's thesis is simple: junior-dev bugs live in that space,
because nothing except a comment or a hope stops a teammate from writing
code there. Senior API design does not rely on comments or hope -- it
reshapes the TYPE so that touching a partially formed object is not merely
discouraged, it is impossible to write in the first place. This activity is
inspired by Logan Smith's "Rust API design" video series on YouTube, which
makes this same argument for a language that enforces it at compile time;
this activity makes the same argument for C++, where it is a discipline you
choose rather than a rule the compiler hands you for free.

## Background

Picture a `Connection` class with an `init()` method and a `send()` method.
Somewhere in a real codebase, three lines like these exist:

```cpp
Connection c;
c.init(host, port);
c.send(data);
```

`Connection c;` alone does not connect anything -- it just default-constructs
an object that is not yet ready. The gap between that line and the
`c.init(host, port);` line right after it is exactly the space between the
lines: for however briefly, `c` exists in a state that is neither "doesn't
exist" nor "ready to use." A teammate six months from now, skimming this
file while fixing something unrelated, might insert one more line right
there -- a debug print that happens to call `c.send()` early, a copy of `c`
made "just to log it" before `init()` ran, a reordering during a merge
conflict that nobody double-checked. Every one of those insertions compiles.
None of them are caught by the type system. Some of them crash immediately;
some of them corrupt data silently and show up as a bug report three weeks
later that nobody can reproduce.

This is not a story about a careless engineer. Every single decision that
got `Connection` here -- add an `init()` step, keep the default constructor
around so existing code still compiles, add one more flag, add one more
setter -- was locally reasonable. That is exactly how rot happens: not one
bad choice, but a sequence of small, plausible ones that never quite closed
the gap. The fix is not "write better comments" or "remember to check." The
fix is to change the shape of the type so the bad state has nowhere left to
live.

## Concepts covered

- The "space between the lines": every gap between construction and
  readiness is a place misuse can be inserted, and it compiles
- The fix ladder: comment (ignored) -> assert (catches it too late, and
  only in debug builds) -> type design (makes the bad state uncompilable)
- Fully-forming constructors: doing all of an object's real setup work in
  one constructor, paired with RAII (Resource Acquisition Is
  Initialization -- the idiom this course covers in `raii-file-guard`,
  where a resource's lifetime is tied to an object's constructor and
  destructor) so the object is never seen half-made
- The zombie-object anti-pattern (a constructor that never fails, but
  leaves an `is_valid_` flag every caller must remember to check) versus a
  private constructor plus a static `create()` factory that makes the
  validating path the *only* path
- `const` data members as a way to prevent mutation after construction, not
  just failure to construct correctly
- Making invalid states unrepresentable: a struct with a flag plus two
  members that can both be populated at once (nonsense) versus a sum type
  (the tagged-union idea from `union-dissector`) that can only ever hold
  one alternative at a time
- Why calling a virtual function from a constructor is the exact same
  disease (a partially formed object) wearing a different mechanism

## How it works

You are shown ten short C++ scenarios, each building on the `Connection`
villain from the opening story or a closely related example. Each question
gives you an enumerated list of possible answers; type the one that matches
exactly as written. A wrong answer explains specifically why that option
misreads the scenario. A correct answer unlocks the fuller explanation,
which usually connects the scenario back to the same underlying idea: never
let an object that is not fully formed become reachable by ordinary code.

## Getting started

```bash
python3 launch.py
```

No compiler is needed for this activity -- it is a plain question-and-answer
activity with C++ snippets shown as text, not compiled or run.

## You will know you are done when...

You have correctly answered all ten questions and the activity prints your
passphrase.

## Hints

<details>
<summary>Hint 1 -- what changed, and when</summary>

For every scenario, ask: at what exact moment does this object become
"ready," and is there any legal C++ that lets you hold, copy, or call a
method on it before that moment? If the answer is yes, that gap is the bug,
no matter how small it looks.

</details>

<details>
<summary>Hint 2 -- detection is not prevention</summary>

A comment, an `assert`, or an `is_valid()` flag all *detect* misuse, at
best, after the broken code has already been written and sometimes after it
has already run. This activity is specifically looking for designs that
make the misuse fail to *compile* -- that is a stronger guarantee than
catching it at runtime.

</details>

<details>
<summary>Hint 3 -- fallible construction, before std::optional and exceptions</summary>

This course covers `std::optional` in the Modern C++ module and exceptions
in the Exception Handling module, both later than this one. Where a
question asks about handling a constructor that might fail, reason about
what each option guarantees using only what you know right now: does an
invalid object still exist and stay reachable, or does construction never
finish at all?

</details>

## Going further

- Refactor the `Connection` villain end to end, on paper or in a real file:
  start from `Connection c; c.init(host, port); c.send(data);` and rewrite
  it as a class with a private constructor, a static `create()` factory,
  and `const` members for anything that should never change after setup.
- Find a real two-phase-init API in a codebase you have used (a game engine
  `Entity` class, a GUI widget that needs `create()` after its constructor,
  a network library `Socket` that needs `bind()` and `listen()` calls after
  construction). Is the split deliberate (documented, for a real structural
  reason) or accidental? How would you tell the difference just from
  reading the header?
- Watch Logan Smith's "Rust API design" series on YouTube (the direct
  inspiration for this activity) and pick one idea from it -- ownership,
  the typestate pattern, or making illegal states unrepresentable -- and
  write down, in your own words, what the closest C++ equivalent tool is
  for expressing the same guarantee.
