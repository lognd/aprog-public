# Study Guide 54: Python Generators

This module proves generator pause/resume behavior directly by
interleaving `print()` output across `next()` calls, then has students
build a real five-stage lazy log-processing pipeline whose grading
watches HOW MUCH of the input was actually touched, not just what values
come out.

## Know before you start

- Iterator/`begin()`/`end()`/fence-post mental model as the C++ analogue
  for "pulling the next value" [assumed: row 35 -- Iterators]
- `Iterable`/`Iterator` type-hint annotations [assumed: row 53 -- Python
  Generics & Typing]
- Comprehension laziness for generator expressions specifically [assumed:
  row 52 -- Python Types & Comprehensions]

## Taught here

Concept: pause and resume
- Know a Python generator function is any function with `yield` anywhere
  in its body; calling it returns a paused generator object without
  running a single line of the body -- the body only starts running on
  the first `next()` call (or the first iteration of a `for` loop over
  it).
- Know `yield` suspends execution mid-function, and the next `next()`
  call resumes exactly where it left off, remembering local variable
  state automatically -- no hand-written state-machine bookkeeping
  required, unlike C++ (which has no real equivalent until C++20
  `co_yield` coroutines, an advanced, rarely-touched corner of the
  language).
- Know `StopIteration` is the signal a generator has nothing left to
  produce, and that a `for` loop over a generator catches it
  automatically to end the loop.
- Know exhaustion is permanent for that one object: once a generator has
  been fully consumed, it stays empty forever; getting a fresh sequence
  means calling the generator function again to build a brand-new
  generator object.

Concept: laziness
- Know laziness means "on demand": a generator expression's side effects
  (like a `print` inside the thing being generated) happen exactly when a
  value is pulled out of it, one at a time -- never earlier, never all at
  once up front.
- Know generators can be chained (piped) one into another, and an
  infinite generator can be consumed safely with a bounded loop or a
  `take`-style helper.
- Be able to distinguish "produces the right values" from "produces them
  LAZILY" -- a function that secretly builds a full list before yielding
  anything can pass a naive correctness check on output values while
  still failing a laziness requirement that watches how much of the
  input was actually touched.

Concept: building a lazy pipeline
- Be able to write a chain of generator functions, each consuming exactly
  as much of its input as its own caller demands, never reading ahead
  speculatively.
- Be able to implement `take(iterable, n)` so it never pulls an `n+1`th
  item from its source just to check whether one exists -- the core
  laziness proof hook.
- Be able to implement a filtering stage (`only_level`) and a
  running-aggregate stage (`running_count`) that both preserve order and
  pull one item at a time.
- Be able to implement `chunked` yielding successive fixed-size lists,
  including a shorter final chunk when the input length is not an exact
  multiple of the chunk size.
- Be able to skip malformed input silently within a generator (e.g. a log
  line missing its delimiter) without breaking the pipeline's laziness.

## Study checklist

- [ ] Explain why calling a generator function runs zero lines of its
      body.
- [ ] Predict interleaved print output across multiple next() calls on a
      generator.
- [ ] Explain why a generator object cannot be reused after exhaustion.
- [ ] Explain the difference between "correct output" and "lazy" for a
      pipeline stage.
- [ ] Implement take(iterable, n) so it never over-pulls from its source.
- [ ] Implement chunked() with a correctly-yielded short final chunk.

## Practiced in

`yield-yard`, `lazy-pipeline`
