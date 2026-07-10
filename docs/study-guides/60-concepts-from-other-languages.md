# Study Guide 60: Concepts from Other Languages

This is the course's capstone recognition tour. language-safari
describes a feature from a different language on each question --
Rust, Java, JavaScript, Go, Haskell, C#, TypeScript -- and asks which
concept from earlier in this course it maps to. No new syntax is
taught here; the activity exists to practice the actual transferable
skill of picking up any new language: recognizing that its unfamiliar
syntax is very often an old idea from a different angle, and honestly
naming the places a mapping is close but not a perfect match.

## Know before you start

- RAII and the Big 5 (copy/move constructors and assignment,
  destructor), and how a resource's lifetime is tied to a scope
  [assumed: row 25 -- Dynamic Memory (Big 5, move semantics)]
- `std::unique_ptr` and `std::shared_ptr` as C++'s deterministic,
  scope-tied alternative to a garbage collector [assumed: row 27 --
  Smart Pointers]
- `std::optional<T>` as a type-safe "value or nothing" alternative to
  a nullable raw pointer [assumed: row 43 -- Modern C++ (C++11-C++17
  features)]
- The error-contract spectrum -- throwing an exception versus
  returning an explicit sentinel/value on failure -- and the honest
  tradeoffs between them [assumed: row 44 -- Exception Handling]
- `asyncio`'s single-threaded, cooperative event-loop model, and why
  it helps I/O-bound work but not CPU-bound work [assumed: row 55 --
  Python Async, Threads, Multiprocessing]
- Threading versus multiprocessing tradeoffs, the GIL, and
  shared-mutable-state race conditions [assumed: row 55 -- Python
  Async, Threads, Multiprocessing]
- Const-correctness and referential transparency as a discipline for
  functions that should not mutate outside state [assumed: row 18 --
  Programming Paradigms]
- Python's `@property` decorator (plus `@x.setter`) for attribute-
  looking syntax backed by real code [assumed: row 50 -- Python
  Classes (instance, class, static)]
- Abstract Base Classes as an explicit, checked method contract
  [assumed: row 22 -- Inheritance (ABC, drawbacks, composition)]
- Duck typing as Python's implicit, unchecked "has the right methods"
  convention, contrasted with interface-based dispatch [assumed: row
  23 -- Polymorphism (Interfaces, Templating)]
- Python type annotations and running a static checker like `ty` over
  them separately from execution [assumed: row 53 -- Python Generics &
  Typing]

## Taught here

Concept: ownership and cleanup across languages
- Know Rust's ownership/borrowing system is a compiler-enforced
  descendant of the same idea behind C++'s Big 5 and RAII: a
  resource's lifetime is tied to a scope and cleaned up automatically
  when that scope ends.
- Know the real difference from Python's garbage collector: Rust's
  ownership rules are checked entirely at compile time with no runtime
  scanning, and cleanup is deterministic (happens the instant a scope
  ends) rather than at some later, unpredictable collection pass.
- Know C++ achieves automatic cleanup without a garbage collector
  through RAII and smart pointers (`std::unique_ptr`,
  `std::shared_ptr`), which call `delete` in their own destructor at a
  precise, predictable point, in exchange for requiring the programmer
  to actually use them (a raw `new` with no wrapper is still
  unmanaged).

Concept: errors as values versus exceptions across languages
- Know Rust's `Option<T>` maps to `std::optional<T>`: both represent
  "a value, or explicitly nothing" as part of the type itself, with a
  required check before the contained value can be used.
- Know Rust's `Result<T, E>` maps to the course's error-contract
  spectrum: returning an explicit success-or-failure value instead of
  throwing, forcing every caller to see at the call site that failure
  is possible, the same tradeoff this course discussed comparing
  return values against C++ exceptions.

Concept: concurrency models across languages
- Know JavaScript's single-threaded event loop and Python's `asyncio`
  are structurally the same idea: one thread, one event loop, tasks
  yield control at a wait point (an `await`, or an async operation's
  boundary) so other tasks can run during I/O waits, and both freeze
  entirely if heavy synchronous computation blocks that one thread.
- Know Go's goroutines relate to the same threading/multiprocessing
  workload-shape tradeoff this course covered (I/O-bound versus
  CPU-bound, and whether concurrency actually helps), just with a
  cheaper unit of concurrent execution.
- Know Go's channels are a structured way to pass data between
  concurrent units instead of directly sharing one mutable variable,
  sidestepping the exact class of race condition a shared counter
  produces without threads without a channel-like structure.

Concept: purity and mutation discipline across languages
- Know Haskell's pure functions (output depends only on input, no
  side effects) are a language-enforced, pervasive version of the same
  discipline practiced as const-correctness and referential
  transparency: a function whose behavior does not depend on, or
  mutate, anything outside its declared inputs.

Concept: attribute-syntax-backed-by-code across languages
- Know C# properties map directly to Python's `@property` (with a
  matching `@x.setter`): both let calling code use plain,
  field-looking syntax while a real method runs underneath, with no
  call-site change needed if validation or computed logic is added
  later.

Concept: method contracts across languages
- Know Java's `implements SomeInterface` is an explicit,
  compile-time-checked contract that a class provides every required
  method.
- Know Python's two related but different analogs: duck typing (no
  declared relationship at all -- an object is usable anywhere its
  needed methods exist, nothing checked until first use) and ABCs (a
  class explicitly inherits from an ABC, and Python enforces that
  every abstract method is implemented before the class can be
  instantiated), with ABCs the closer analog to Java's interfaces.

Concept: gradual static typing across languages
- Know TypeScript's gradual typing (types added incrementally, file
  by file, with untyped code still running) maps to Python's type
  annotations combined with a separately-run static checker like
  `ty`: in both cases the type checking is optional, incremental, and
  a separate step layered on top of a runtime that never required
  types to begin with.

Concept: the general lesson
- Know the point of the whole module: languages differ mainly in
  syntax and surface feature design, but the underlying concepts --
  resource ownership, error handling as values versus exceptions,
  concurrency models fit to workload shape, static versus dynamic
  typing, method contracts -- recur, because they are solutions to the
  same small set of problems every language eventually has to solve.
  Learning a new language is largely recognizing which already-known
  concept its unfamiliar syntax expresses.

## Study checklist

- [ ] Explain why Rust's ownership model is a compile-time-enforced
      version of C++'s RAII/Big 5, and name the concrete difference
      from Python's garbage collector.
- [ ] Map Rust's `Option<T>` and `Result<T, E>` to their C++/course
      equivalents, and state what each one replaces.
- [ ] Explain what C++ uses instead of a garbage collector, and the
      real tradeoff (deterministic cleanup vs. no required
      programmer discipline).
- [ ] Explain why JavaScript's event loop and Python's `asyncio` are
      the same structural idea, and why both stall on heavy
      synchronous work.
- [ ] Explain what problem Go's channels solve, and tie it back to a
      specific race-condition scenario from earlier in the course.
- [ ] Explain how Haskell's pure functions relate to
      const-correctness and referential transparency.
- [ ] Map C# properties to Python's `@property`/`@x.setter`.
- [ ] Contrast Java interfaces with Python's duck typing and ABCs, and
      say which one is the closer analog and why.
- [ ] Map TypeScript's gradual typing to Python annotations plus a
      checker like `ty`.
- [ ] State, in your own words, the one lesson every question in this
      module is making.

## Practiced in

`language-safari`
