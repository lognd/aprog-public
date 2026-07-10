# Study Guide 7: Standard Library Types

This module introduces the two workhorse standard-library containers,
`std::array` and `std::vector`, focusing on where each stores its data and
what that implies for performance and safety, plus `std::string` mechanics
through a debugging exercise and a from-scratch CSV parser.

## Know before you start

- Stack vs. heap memory as two distinct storage regions [assumed: GAP -- a
  full treatment is row 10 (Memory Model), which comes later than this
  row; this module's `array-foray` activity introduces the stack/heap
  distinction informally itself]
- Basic C++ functions, loops, and `std::string` basics [assumed: row 6 --
  Control & Functions]

## Taught here

Concept: std::array vs std::vector storage
- Know that `std::array<T, N>` is a fixed-size array whose size N must be a
  compile-time value (a literal or compile-time constant), written directly
  in the type; it cannot grow or shrink.
- Know that `std::array` elements live on the stack, directly inside the
  variable, which is why the compiler must know N before the program runs
  (to lay out the stack frame).
- Know that `std::vector` elements live on the heap, so `sizeof(std::vector<T>)`
  is the same regardless of how many elements it holds -- the vector object
  itself is just a small handle pointing at heap memory.
- Be able to explain why a runtime variable cannot be used as `std::array`'s
  size template argument, even if its value never changes in practice.

Concept: std::vector capacity and reallocation
- Know that a `std::vector` tracks two separate numbers: size (how many
  elements it currently holds) and capacity (how many elements the current
  buffer has room for).
- Know that when size would exceed capacity, the vector reallocates:
  allocates a new bigger buffer, copies every existing element into it, and
  frees the old buffer.
- Be able to use `reserve(n)` once, before a loop of known final size, to
  pre-allocate capacity and avoid repeated reallocations during insertion.
- Know that every reallocation invalidates any pointer, reference, or
  iterator previously taken into the vector's old buffer, because that
  memory has been freed.

Concept: size vs. capacity bookkeeping
- Know that `size()` counts elements actually stored; `capacity()` counts
  how much room is reserved before the next `push_back` would need to
  reallocate a bigger buffer -- the two numbers are tracked separately and
  move independently.
- Know that `reserve(n)` is standard-guaranteed to leave `capacity() >= n`,
  making a pre-`reserve`d capacity a portable, exactly-predictable number
  across compilers.
- Know that `std::vector`'s growth factor when it DOES reallocate (1.5x,
  2x, or another factor) is implementation-defined by the standard, so raw
  `capacity()` values after unpinned repeated `push_back` are not portable
  and should never be predicted as an exact number.
- Know which operations change only `size()`: `push_back`, `pop_back`,
  `clear()`, and `resize()` to a size within the current capacity.
- Know which operations can change `capacity()`: `reserve()`, and any
  `push_back`/`resize()` that outgrows the current capacity (triggering a
  reallocation).
- Know that `clear()` and `pop_back()` never release already-allocated
  capacity -- `size()` drops but `capacity()` stays exactly where it was.
- Know that `resize(n)` to a smaller `n` drops trailing elements
  (`size()` only shrinks); `resize(n)` to a larger `n` value-initializes
  the new slots (0 for `int`), never copying an existing element into
  them.

Concept: std::string mechanics
- Be able to build a string incrementally by appending pieces (e.g. words
  separated by spaces) inside a loop.
- Know the "flush the last item" pattern: a loop that accumulates into a
  buffer and only pushes it to a results container when a threshold is
  crossed must also push the final leftover buffer after the loop ends, or
  the last item is silently dropped.
- Be able to distinguish an off-by-one comparison bug (`<` vs `<=`) from a
  missing-statement bug by tracing what the loop actually does at its
  boundary case.

Concept: parsing structured text
- Be able to parse CSV-formatted text by iterating character by character
  and tracking parser state (for example, "am I currently inside a quoted
  field?").
- Know the RFC 4180 CSV rules this course expects: a quoted field can
  contain commas and newlines; `""` inside a quoted field represents one
  literal `"`; empty fields and trailing commas are legal and must not be
  silently dropped; a short row (fewer fields than others) is not an error
  and must not be padded.
- Be able to build a nested `std::vector<std::vector<std::string>>` result
  where each inner vector's size can legitimately differ from the others.

## Study checklist

- [ ] Explain why `std::array<int, n>` fails to compile when `n` is a
      runtime variable, and how to fix it.
- [ ] Explain the difference between a vector's size and its capacity.
- [ ] State why calling `reserve` inside a loop, once per iteration, does
      not solve the reallocation problem, and what fixes it.
- [ ] Explain why a saved pointer into a vector can become invalid after a
      `push_back`.
- [ ] List which operations move size() only vs. which can move
      capacity() too.
- [ ] Predict size()/capacity() after a reserve/push_back/pop_back/clear/
      resize sequence.
- [ ] Describe the "flush the last item" bug pattern and how to fix it.
- [ ] Trace how a CSV parser should handle an escaped quote (`""`) inside a
      quoted field.

## Practiced in

`array-foray`, `vector-inspector-corrector`, `string-methods`, `csv-parser`,
`capacity-chronicles`
