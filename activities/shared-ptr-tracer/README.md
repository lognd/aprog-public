# Activity: Shared Pointer Tracer

`std::shared_ptr` lets multiple parts of a program share ownership of the
same object. It does this by keeping a REFERENCE COUNT -- a running total,
stored in a small extra block of memory called the CONTROL BLOCK, of how
many `shared_ptr` instances currently point at the same object. Copying a
`shared_ptr` increments that count. Destroying one (or calling `.reset()`)
decrements it. The moment the count reaches zero, the object is destroyed
automatically -- no explicit `delete` anywhere.

This activity gives you seven small, instrumented C++ programs, each printing
`use_count()` (the current value of the reference count) and constructor and
destructor messages at key moments. Your job is to predict, exactly, what
each program prints -- line for line -- before you see the real output. This
forces you to trace through copying, moving, function calls, and
`weak_ptr::lock()` by hand, rather than just believing whatever a tutorial
tells you `shared_ptr` does.

---

## Background

### Copying vs. moving

Copying a `shared_ptr` (`auto b = a;`) makes `b` a second, independent owner
of the same object -- the reference count goes up by one. MOVING a
`shared_ptr` (`auto b = std::move(a);`) does something different: ownership
is *transferred* from `a` to `b`. No new owner is created, so the reference
count does not change, and afterward `a` is left empty (it becomes a null
`shared_ptr`). This is exactly why moving is cheaper than copying: no atomic
increment happens at all.

### The reference cycle

If two objects hold `shared_ptr`s to *each other*, each one's reference
count can never reach zero -- object A is kept alive by object B's pointer to
it, and object B is kept alive by object A's pointer to it, forever, even
after nothing else in the program can reach either one. This is called a
REFERENCE CYCLE, and it is a genuine, silent memory leak: neither
destructor ever runs, for the rest of the program's execution. Two of the
snippets in this activity show exactly this bug, side by side with its fix.

### `weak_ptr` and `.lock()`

A `weak_ptr` is a NON-OWNING reference to an object managed by `shared_ptr`.
Holding a `weak_ptr` never increments the reference count. To actually use
the object, you call `.lock()`, which returns a fresh `shared_ptr` if the
object is still alive, or an empty (null) `shared_ptr` if it has already been
destroyed. This is how a `weak_ptr` safely "checks in" on an object without
ever being the reason that object stays alive.

### Why `use_count()` is safe to predict exactly here

`use_count()`'s exact value is not always guaranteed by the C++ standard to
be perfectly precise in multi-threaded code, because two threads could be
copying or destroying `shared_ptr`s to the same object at the same instant.
Every snippet in this activity is single-threaded and calls `use_count()`
only at points where no other copy or destruction could possibly be racing
with it -- so its value is completely deterministic here, and predicting it
exactly is a fair, well-defined exercise.

---

## Concepts covered

- `std::shared_ptr` reference counting and `use_count()`
- Copying a `shared_ptr` (increments the count) vs. moving one (does not)
- Passing a `shared_ptr` by value bumps the count for the duration of the call
- `std::weak_ptr` and `.lock()` -- observing without owning
- The `shared_ptr` reference-cycle memory leak, and fixing it with `weak_ptr`
- Scope-exit destruction and its effect on the reference count

---

## How it works

Each of the seven snippets is shown to you in full, with a short platform
note. Predict its exact stdout output. Answers with more than one line are
entered one line at a time, in order. If your prediction is wrong, you are
shown the real output and a full explanation, and you must type the correct
output before moving on. Every snippet is compiled and actually run (with
`g++ -std=c++17`) so the "actual output" you are checked against is real,
not scripted.

---

## Getting started

```bash
python3 launch.py
```

A C++ compiler (`g++` or `clang++`) must be available on your machine.

---

## You will know you are done when...

The launcher prints the passphrase after you have correctly predicted the
output of all seven snippets.

---

## Hints

<details>
<summary>Hint 1 -- track the reference count as a running total, not a snapshot</summary>

At every `use_count()` call, ask: how many separate `shared_ptr` variables
currently exist that own this object? Count constructions (`make_shared`,
copies) as +1 each, and destructions (scope exit, `.reset()`) as -1 each,
in the exact order they happen in the code.

</details>

<details>
<summary>Hint 2 -- local variables are destroyed in reverse order, at the closing brace of their scope</summary>

When a `{ ... }` block ends, every local variable declared inside it is
destroyed, in the REVERSE order it was declared. This determines exactly
when a `use_count()` drop (or a full destructor call) happens.

</details>

<details>
<summary>Hint 3 -- in the cycle snippets, ask "who has an owner left?"</summary>

For the two Parent/Child snippets, work out each object's reference count
immediately after both cross-assignments, then figure out what happens to
that count as the local variables `p` and `c` go out of scope. Ask, for
each object: is there still a live `shared_ptr` (not `weak_ptr`) pointing
at it after the local variables are gone?

</details>

---

## Going further

- Add a third object to the cycle -- a `Grandchild` owned by `Child` -- and
  predict whether adding *more* shared ownership in the same direction
  (Child owning Grandchild, not a cycle) changes anything about the leak.
- Run the leaking cycle snippet under Valgrind or with
  `-fsanitize=address -fsanitize=leak` and confirm it reports a real leak.
  Then run the `weak_ptr` version the same way and confirm it does not.
- Replace one of this activity's `make_shared<Widget>` calls with
  `std::shared_ptr<Widget>(new Widget(...))` (the older, two-allocation
  style). The observable behavior is identical, but `make_shared` does one
  heap allocation instead of two. Look up why, and what that means for
  performance.
- Try writing a snippet where two threads copy the same `shared_ptr`
  concurrently. What does the C++ standard actually guarantee is safe here,
  and what is not safe (hint: concurrently *writing* to the shared_ptr
  variable itself, versus concurrently copying from it)?
