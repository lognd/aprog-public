# Activity: Ownership Court

Every object your program creates on the HEAP (memory explicitly allocated
with `new`, as opposed to the STACK, where local variables normally live and
are cleaned up automatically) needs exactly one thing to decide when it gets
destroyed. That responsibility is called OWNERSHIP: whoever "owns" an object
is the one responsible for eventually freeing it. Smart pointers are C++
types that automate this decision -- but a smart pointer is only helpful if
you pick the *right kind* for the ownership relationship you actually have.

This activity gives you ten concrete scenarios, in plain English, with no
code. For each one, you play judge: decide which of four verdicts fits --
`unique_ptr`, `shared_ptr`, `weak_ptr`, or a plain raw pointer/reference --
and the explanations teach you the underlying decision rules from scratch,
including the classic traps that catch almost everyone the first time.

---

## Background

### The four verdicts

- **`unique_ptr`** -- a smart pointer with exactly ONE owner at a time. It
  cannot be copied (copying it is a compile error), only MOVED, which
  transfers ownership to a new variable and leaves the old one empty. When
  a `unique_ptr` is destroyed, it automatically deletes the object it owns.
  Use this whenever exactly one thing is responsible for an object's
  lifetime.
- **`shared_ptr`** -- a smart pointer that allows MULTIPLE simultaneous
  owners. Internally it keeps a REFERENCE COUNT (a number, stored in a small
  extra block of memory called the CONTROL BLOCK, tracking how many
  `shared_ptr`s currently point at the same object). Copying a `shared_ptr`
  increments the count; destroying one decrements it; the object is only
  destroyed once the count reaches zero. Use this when ownership is
  genuinely shared among several independent parts of the program, and no
  single one of them can be identified in advance as "the last one standing."
- **`weak_ptr`** -- a NON-OWNING observer of an object managed by
  `shared_ptr`. Holding a `weak_ptr` never increments the reference count and
  never keeps the object alive. To actually use the object, you call
  `.lock()`, which returns a live `shared_ptr` if the object still exists, or
  an empty one if it has already been destroyed. Use this when code needs to
  check on an object without being a reason it stays alive.
- **Raw pointer or reference** -- no smart pointer at all. Use this when a
  function or piece of code just needs to *look at* or *use* an object for a
  short time, without ever being responsible for creating or destroying it.
  Not every pointer needs to manage a lifetime.

### The classic trap: reference cycles

If object A owns object B with a `shared_ptr`, and object B *also* owns
object A back with a `shared_ptr`, you get a CYCLE: each object's reference
count can never reach zero, because the other object is still holding a
reference to it. Neither destructor ever runs, even after both objects are
otherwise unreachable from the rest of the program -- this is a genuine,
silent MEMORY LEAK (memory that is never freed, because nothing frees it).
The standard fix is to make one direction of the relationship a `weak_ptr`
instead of a `shared_ptr` -- typically the "back-reference" direction (like a
child pointing back to its parent), since ownership usually has one natural
direction already.

### The other classic trap: "`shared_ptr` everywhere"

Because `shared_ptr` is easy to reach for and "just works" in almost any
situation, it is tempting to use it as the default answer for every pointer
in a program. This has a real, measurable cost: every copy of a `shared_ptr`
does an ATOMIC increment or decrement of the reference count (an operation
that is safe to run from multiple threads at once but is slower than a plain
integer increment), and every `shared_ptr` requires that heap-allocated
control block. Using `shared_ptr` when a plain `unique_ptr`, or no smart
pointer at all, would do is a common overuse mistake this activity trains you
to recognize.

---

## Concepts covered

- Ownership as a design question: who is responsible for an object's lifetime
- `unique_ptr` -- single ownership, move-only, zero-cost cleanup
- `shared_ptr` -- multiple ownership via reference counting
- `weak_ptr` -- non-owning observation of a `shared_ptr`-managed object
- Recognizing when no smart pointer is needed at all (raw pointers/references
  for pure "borrow, don't own" use)
- The `shared_ptr` reference-cycle leak, and using `weak_ptr` to break it
- Avoiding "`shared_ptr` everywhere" overuse

---

## How it works

You will be shown ten scenarios, one at a time, each describing a concrete
situation: a tree's children, an observer list, a cache, a function
parameter, and so on. For each one, type exactly one of the five listed
verdicts (spelled exactly as shown, e.g. `unique_ptr` or `raw pointer or
reference`). If you answer incorrectly, the activity explains specifically
why that verdict is wrong for that scenario before letting you try again.
Once you answer correctly, you get a full explanation of the reasoning
before moving to the next question. All ten must be answered correctly to
unlock the passphrase.

---

## Getting started

```bash
python3 launch.py
```

---

## You will know you are done when...

The launcher prints the passphrase after all ten scenarios have been
answered correctly.

---

## Hints

<details>
<summary>Hint 1 -- start by asking "how many owners, and do they overlap in time?"</summary>

For every scenario, ask: does exactly one thing own this object for its
entire lifetime (`unique_ptr`)? Do multiple independent things need to keep
it alive at the same time, with no clear "last owner" (`shared_ptr`)? Does
something need to check on an object without keeping it alive
(`weak_ptr`)? Or does something just need to look at an object it does not
own at all (raw pointer or reference)?

</details>

<details>
<summary>Hint 2 -- watch for cross-references between two owning pointers</summary>

Any time a scenario describes two objects that both need pointers to each
other, ask whether both directions are really meant to be *owning*. If they
are, you likely have a cycle -- and the fix is almost always to make one
direction (usually the "look back at my container" direction) a `weak_ptr`.

</details>

<details>
<summary>Hint 3 -- a function that only reads or uses something briefly rarely needs a smart pointer at all</summary>

If a scenario describes a function that is handed an object, does something
with it, and returns -- without storing it anywhere or affecting how long it
lives -- that is almost always a raw pointer or reference case, even if the
object itself happens to be managed by a smart pointer somewhere else in the
program.

</details>

---

## Going further

- Take the tree scenario from this activity and actually write it in C++:
  a `Node` struct with `std::vector<std::unique_ptr<Node>> children`. Try to
  copy a `Node` -- what compile error do you get, and why does that error
  make sense given what you just learned about `unique_ptr`?
- Write the Parent/Child reference-cycle example from `shared-ptr-tracer`
  (the sibling activity to this one) and run it under a leak-checking tool
  like Valgrind or AddressSanitizer's leak detector. Confirm it reports a
  leak. Then change one direction to `weak_ptr` and confirm the leak is gone.
- Look up `std::enable_shared_from_this`. Why does an object sometimes need
  to hand out a `shared_ptr` to itself, and why can it not just write
  `std::shared_ptr<T>(this)` safely?
