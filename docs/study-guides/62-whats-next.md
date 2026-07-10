# Study Guide 62: What's Next

This closing lecture is a map, not new material: it points from
everything the course has covered toward the directions a student can
take next -- deeper C++, systems programming, other languages (using row
60's mapping as the launchpad), open-source contribution, interview
preparation, and building real projects. No artifact accompanies this
row; it is taught in lecture, and it deliberately introduces no
machinery of its own.

## Know before you start

- The full arc of this course's C++ material, from variables through
  smart pointers and modern C++ [assumed: rows 5-27, 42-44 -- C++
  fundamentals through modern C++]
- The full arc of this course's data structures and algorithms material
  [assumed: rows 28-39 -- Complexity Theory through Function Pointers,
  Functors, Lambdas]
- The full arc of this course's Python material [assumed: rows 45-59 --
  Intro to Python through APIs]
- The cross-language concept map built in language-safari [assumed: row
  60 -- Concepts from Other Languages]

## Taught here

Concept: deeper C++
- Know that this course's C++ (through row 44) covers C++11 through
  C++17 features; C++20 and C++23 add further language features worth
  knowing exist even without covering them in depth here, most notably
  coroutines (functions that can suspend mid-execution and later resume
  exactly where they left off, a language-level building block for
  asynchronous code, related in spirit to row 55's `asyncio` but built
  into the language itself rather than a library).
- Know that C++20 also adds concepts (compile-time constraints on what a
  template parameter must support, a more readable alternative to the
  error messages produced by unconstrained templates) and modules (an
  alternative to `#include`-based header compilation, intended to speed
  up large-project build times, tying directly back to row 61's
  build-at-scale concerns).
- Know that continued C++ depth realistically means reading real
  large-codebase C++ (row 61's skills applied for real) and working
  through a text that goes past this course's C++17 stopping point.

Concept: systems programming
- Know that this course's row 15 (Basic OS Theory) and row 3 (What Is a
  Computer) are deliberately a floor, not a ceiling: a full operating
  systems course goes on to cover process scheduling, virtual memory
  management in depth, and inter-process communication mechanisms this
  course only named.
- Know that networking (how two programs on different machines
  communicate: sockets, the layered protocol stack, HTTP as one protocol
  built on top of that stack) builds directly on row 59's API material
  (which covered using HTTP-based APIs from the client side, one layer
  up from the raw networking this points toward).
- Know that databases (organized, queryable, durable storage, as opposed
  to this course's flat files from row 16) are the natural next stop
  after row 58's web server material, once a server needs to remember
  data across restarts and across many simultaneous users.

Concept: other languages
- Know that row 60's language-safari activity is meant as a launchpad,
  not a finish line: the actual next step is choosing one unfamiliar
  language and writing real code in it, using the concept-mapping habit
  practiced there (recognizing an unfamiliar language's ownership model,
  error handling, concurrency model, and type system as variations on
  concepts already known) to accelerate picking it up.
- Know that Rust is a natural next language for a C++ student
  specifically because of row 60's ownership-model mapping: it offers
  the same manual-control performance profile as C++ with compile-time
  enforced memory safety instead of programmer discipline.

Concept: open source contribution
- Know that reading an unfamiliar codebase (row 4's terminal-archeology,
  scaled up per row 61) is the actual first skill needed to contribute to
  an existing open-source project, before writing a single line of new
  code.
- Know that a first open-source contribution is usually small and
  low-risk on purpose: fixing a documentation typo, closing a
  well-specified "good first issue," or adding a small test -- practicing
  the full pull-request-and-code-review workflow from row 61 on a real
  project, with real reviewers, before attempting a larger change.

Concept: interview preparation
- Know that this course's data-structures-and-algorithms rows (28
  Complexity Theory through 39 Function Pointers, Functors, Lambdas)
  directly cover the material technical coding interviews draw from:
  Big-O reasoning, the standard ADTs (List, Stack, Queue, Map, Set),
  searching, and sorting.
- Know that interview practice from here means applying that material
  under new constraints this course did not impose: a time limit, no
  reference material, and explaining reasoning out loud while solving --
  the underlying data structures and complexity analysis are unchanged
  from what rows 28-39 already taught.

Concept: building real projects
- Know that the most direct next step after this course is a
  self-directed project applying its material end to end: a real build
  system (row 8), real tests (row 17), a real README (row 9), version
  control discipline (row 61), and a real dependency or two (row 40) --
  the SFML material from row 41 is one concrete on-ramp, since a small
  graphical program touches nearly every earlier row at once (memory
  layout, OOP for game objects, standard containers, and an external
  library).

## Study checklist

- [ ] Name two C++20/23 features not covered in this course and, for
      each, one earlier row's material it builds on or resembles.
- [ ] Name three systems-programming topics this course only introduced
      the surface of, and which row planted that surface.
- [ ] Explain how row 60's language-safari mapping habit is meant to be
      reused on a real new language.
- [ ] Describe what makes a good first open-source contribution, and
      which earlier row's skill it depends on most.
- [ ] Name which rows of this course map directly onto technical
      interview preparation, and why.
- [ ] Pick one: a self-directed C++ project, a first open-source
      contribution, a new language, or interview practice -- and name
      the specific earlier rows of this course it would draw on.

## Practiced in

none -- lecture only
