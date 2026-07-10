# Activity: Language Safari

This is the capstone recognition tour for the whole course. Every
question here describes a feature from a DIFFERENT programming
language -- Rust, Java, JavaScript, Go, Haskell, C#, TypeScript -- and
asks you to name which concept from THIS course it maps to. You are
not learning any of these languages. You are practicing the single
most useful skill for picking up a new language quickly: recognizing
that its unfamiliar syntax is very often expressing an idea you
already understand, under a different name. Languages differ in
syntax; the concepts transfer.

## Concepts covered

- RAII / the Big 5 / move semantics, seen through Rust's ownership
  and borrowing
- std::optional and the error-contract spectrum, seen through Rust's
  Option and Result types
- Smart pointers and RAII as C++'s alternative to garbage collection
- asyncio's event-loop model, seen through JavaScript's event loop
- Threading/multiprocessing tradeoffs and shared-state hazards, seen
  through Go's goroutines and channels
- Const-correctness and referential transparency, seen through
  Haskell's pure functions
- Python properties, seen through C# properties
- ABCs and duck typing, seen through Java interfaces
- Type annotations and static type checkers like ty, seen through
  TypeScript's gradual typing

## How it works

The launcher shows you ten scenarios, one at a time -- each describes
a feature of some other language and asks which course concept it
maps to. No code, no syntax to write. A correct answer shows an
explanation of the mapping, including anywhere the analogy is not a
perfect one-to-one match -- read those honestly; a mapping that is
"close but not identical" is still useful, and pretending it is
perfect would be a worse lesson than admitting the difference. A wrong
answer explains the specific misconception behind that guess.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all ten questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask what problem the other language's feature actually solves</summary>

Do not match on surface similarity (special syntax, keyword
similarity). Ask: what real problem does this feature exist to solve,
and which activity or lesson in this course solved that same problem?

</details>

<details>
<summary>Hint 2 -- most mappings pair with a specific earlier activity</summary>

Several questions map straight back to a named activity you already
completed (paradigm-refactor-detector, concurrency-court). If a
scenario feels unfamiliar, think about which earlier activity covered
the closest idea.

</details>

<details>
<summary>Hint 3 -- some course concepts show up more than once</summary>

RAII and the Big 5 come up twice, from two different angles (Rust's
ownership, and C++'s own alternative to Java's garbage collection).
That is not a mistake -- some ideas are central enough to recur.

</details>

## Going further

- Pick one language from this activity you have never written a line
  of, and find a short "getting started" tutorial for it. How much of
  it can you already follow, just from concepts this course taught?
- Rust's borrow checker rejects some programs at compile time that a
  human would consider obviously safe. Look up one commonly-cited
  example and explain why the checker's rule, though overly strict
  there, is still preventing a genuine class of bug in general.
- Pick a concept this course taught that did NOT appear in this
  activity (for example, templates, or virtual dispatch) and find
  which other language you know of implements the closest equivalent.
