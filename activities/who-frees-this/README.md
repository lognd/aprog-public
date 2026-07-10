# Activity: Who Frees This?

Every resource your program acquires -- heap memory from `new` or `malloc`,
a file handle, a socket -- has to be released exactly once, by exactly one
piece of code that is responsible for it. That responsibility is called
OWNERSHIP, and it has nothing to do with holding a pointer, or with having
written the line of code that created the resource. This activity is not
about `unique_ptr` or `shared_ptr` yet (those arrive in the very next
module) -- it drills the CONCEPT underneath them, in the raw-pointer C world
where nothing but a comment and your own discipline enforces it, so that
when the smart-pointer types show up they read as "the compiler finally
checking a rule you already understand," not as new vocabulary from
nowhere.

---

## Background

### An analogy: lending a book

Think of ownership like a library book. If you GIVE someone a book (you
hand it over and no longer expect it back), that is a TRANSFER -- the
responsibility for eventually returning it moves entirely to them, and you
must not go looking for it on your shelf anymore. If you LEND someone a
book (they read it and hand it back), that is a BORROW -- they never
owned it, they just used it for a while, and you are still the one who
has to return it to the library eventually. If you PHOTOCOPY a page, that
is a COPY -- now there are two independent objects, and each needs its own
"return it eventually" plan. And the rule underneath all three: every book
must go back to the shelf EXACTLY ONCE. Not zero times (a lost book -- a
LEAK). Not twice (two people both think they returned it, and the library
desk gets a book slammed on the counter that was already checked back in --
a DOUBLE-FREE). And nobody should read a book that has already gone back to
the shelf and been reshelved somewhere the reader can no longer find it --
using a book after it is gone is a DANGLING USE.

### Why C wrote ownership in comments -- and what it cost

C's type system has no way to say "this function takes ownership of the
pointer you pass it" versus "this function only borrows it." Both are
spelled exactly `void f(Widget*)`. The only place that information can live
is in a comment or a header file's documentation, and the compiler cannot
read either one. `strdup`'s man page says its return value "must be freed
by the caller" -- in plain words, right there in the documentation, because
there is nowhere else to put it. `getenv`'s man page says the opposite: its
return value "must not be freed" -- it points into memory the C library
itself owns and reuses. Two functions, two completely different ownership
rules, and the only thing distinguishing them is prose a programmer has to
read and trust. If you skip the man page, or misremember it, or a teammate
six months from now never reads it at all, the program still compiles.
It just corrupts memory, or leaks it, or crashes -- sometime later, maybe
nowhere near the line that caused it.

### The lifetime contract

Every ownership relationship comes with an implicit CONTRACT: the owner's
lifetime must contain the borrower's use. Picture it as two brackets on a
timeline -- the owner's lifetime is the outer bracket, and every borrow has
to happen entirely inside it:

```
owner:     [==========================================]
borrow 1:      [====]                 <- fine, fully inside
borrow 2:                        [========]            <- fine
borrow 3:                                      [====]  <- BROKEN, starts after
                                                            the owner's bracket closes
```

Every one of the bugs in this activity -- returning a pointer to a local
variable, using a pointer after its owner already freed it, reading through
a pointer whose target function already returned -- is the same diagram
with the borrower's bracket poking out past the right edge of the owner's.

### Shared ownership, honestly

Sometimes two owners are genuinely, legitimately both responsible for the
same object at once -- neither one can be identified in advance as "the one
who will free it," because both need it to stay alive for as long as they
are using it. This is SHARED ownership, and it is real, but it is rarer
than it feels: most of the time a single, clear owner (or a plain borrow)
is the right shape, and reaching for shared ownership by default has a real
cost (a later module covers `shared_ptr`'s reference-counting overhead in
detail). Shared ownership's own dedicated failure mode is the CYCLE: if
object A shares ownership of object B, and B shares ownership right back of
A, neither one's "last owner let go" condition is ever satisfied, and
neither is ever released -- a silent, permanent leak, even after the rest
of the program has completely forgotten both objects exist.

### The fix ladder

This whole module sits at one rung of a ladder that climbs across the rest
of the course:

1. **Comments** (this activity, and every C API you will meet) -- the
   weakest enforcement there is. The compiler cannot see it, and nothing
   stops a caller from ignoring it.
2. **Conventions and RAII** (`raii-file-guard`, back in the OOP module) --
   binding a resource's release to an object's destructor, so the release
   code is written once and runs automatically on every exit path. Far more
   reliable, but still a discipline the class author has to get right.
3. **Types that enforce ownership** (`unique_ptr`, `shared_ptr` -- the very
   next module) -- the type system finally gets a way to represent
   ownership, and violating it becomes a compile error instead of a bug
   report.
4. **A language that refuses to compile the violation** (Rust, covered in
   the concepts-from-other-languages module near the end of this course) --
   ownership and borrowing enforced for every type in the language, by
   construction, not just the ones a library author remembered to design
   carefully.

Each rung removes a little more of the responsibility from "a human
remembers correctly." This activity lives entirely on rung one, on
purpose, so the jump to rung three actually feels like a jump.

---

## Concepts covered

- Ownership as the responsibility to release a resource exactly once (not
  "having a pointer," not "having created it," not "being the only reader")
- The three ownership failure modes: leak (zero releases), double-free (two
  claimed owners), dangling use (a borrower outlives the owner)
- Transfer vs. borrow, and why nothing in C's type system distinguishes
  them -- only a comment does
- Reading real C API ownership contracts: `strdup`, `getenv`, `fopen`/
  `fclose`, and a pointer into a caller-owned buffer
- The lifetime contract: an owner's lifetime must contain every borrower's
  use of it
- Legitimate shared ownership, and its own failure mode, the reference
  cycle
- The fix ladder from comments to a language that refuses to compile the
  violation

---

## How it works

You will be shown eleven questions, each with a short C or C++ snippet
where relevant. Some ask you to classify a bug (leak, double-free, or
dangling use) from a code sketch; others ask you to read a real API's
documented ownership contract and say who owns what; the last two work
through shared ownership and the fix ladder as concepts. Type your answer
exactly as shown in the prompt. If you answer incorrectly, the activity
explains specifically why that answer is wrong for that question before
letting you try again. Once you answer correctly, you get a full
explanation before moving to the next question. All eleven must be
answered correctly to unlock the passphrase.

---

## Getting started

```bash
python3 launch.py
```

---

## You will know you are done when...

The launcher prints the passphrase after all eleven questions have been
answered correctly.

---

## Hints

<details>
<summary>Hint 1 -- count the free() calls, not the lines</summary>

For any code-sketch question, count how many times the resource is
actually released (`free`, `delete`, `close`, the pointer going out of a
function whose caller never captures it) versus how many independent
pieces of code believe they are responsible for releasing it. Zero
releases is a leak. Two claimed releases is a double-free. A release
followed by a later use is a dangling use.

</details>

<details>
<summary>Hint 2 -- the type signature never tells you transfer vs. borrow</summary>

`void f(Widget*)` looks identical whether `f` takes ownership or just
peeks at the argument. The only place that answer lives, in raw C/C++, is
a comment or a piece of documentation -- there is nothing to inspect on
the function's actual type.

</details>

<details>
<summary>Hint 3 -- shared ownership releases on the LAST owner, not the first</summary>

If you are unsure whether a shared-ownership question is about the normal
case or the cycle failure mode, ask: does every owner's "let go" condition
ever actually get satisfied? If two owners are each waiting on the other to
let go first, and neither ever does, that is the cycle.

</details>

---

## Going further

- Read the actual man page for `strdup` (`man 3 strdup` on Linux) and find
  the exact sentence that tells you who owns the returned pointer. Do the
  same for `getenv`. Notice that both answers live entirely in prose.
- Search any C library you have installed (or a large open-source C
  project) for a comment containing the phrase "caller must free" or
  "caller owns." Find the function it documents and see whether every
  call site you can find actually obeys it.
- Write the A-owns-B, B-owns-A reference cycle from this activity's shared
  ownership question using nothing but raw pointers and manual `delete`
  calls in each destructor, deliberately introduce the cycle (never call
  the extra `delete` that would break it), and run the program under
  Valgrind (see `valgrind-leak-lab`). Confirm it reports the leak, and
  notice that Valgrind can see the leaked memory but has no way to tell
  you it was caused by a cycle specifically -- that diagnosis is still on
  you.
