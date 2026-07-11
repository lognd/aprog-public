# Unique Pointer From Scratch

You already know that every `new` needs a matching `delete`, and that the
Big 5 exist so an object can manage a resource correctly through copies,
moves, and destruction. `std::unique_ptr<T>` packages that pattern up once
and for all: it is a small class that owns exactly one heap object and
guarantees the matching `delete` happens, no matter how the owning object's
lifetime ends. This assignment asks you to build that class yourself, then
use the real `std::unique_ptr` to see the same idea from the caller's side.

---

## Learning goals

- Explain RAII (Resource Acquisition Is Initialization): binding a
  resource's lifetime to an object's lifetime so the destructor is the one
  and only place that has to remember to free it
- Explain why a "unique owner" type must forbid copying, and implement that
  by deleting the copy constructor and copy assignment operator
- Implement move construction and move assignment that transfer ownership
  and leave the source owning nothing
- Distinguish `get()` (inspect, keep ownership), `release()` (give up
  ownership, caller now owns the raw pointer), and `reset()` (destroy what
  you own now, then take ownership of something else)
- Recognize and prevent a double-delete: the disaster that happens when two
  objects both believe they own the same pointer
- Use `std::unique_ptr` and `std::make_unique` as a caller: write a
  **factory function** (a function whose only job is to construct and
  return an object, so callers never write `new` themselves) that returns
  one, a function that takes a container of them by reference to inspect
  it without taking ownership of anything inside, and a function that
  moves one out of that container and returns it by value (which forces
  the caller to `std::move` it out of the slot it currently lives in)

## Background

### RAII, one more time, but from the ownership side

You have already used RAII implicitly: a `std::vector` allocates its buffer
in its constructor and frees it in its destructor, so you never call
`delete[]` yourself. `MyUniquePtr<T>`, the class you are about to build, is
RAII applied to a single object instead of a buffer: construct it with a
pointer from `new`, and its destructor calls `delete` on that pointer when
the `MyUniquePtr` itself goes out of scope -- whether that's from falling
off the end of a function, an early `return`, or the object living inside a
container that gets destroyed. You write the `delete` exactly once, in the
destructor, and then never again -- every code path that ends the
`MyUniquePtr`'s lifetime runs through it automatically.

### Why copying a unique owner has to be illegal

Consider what a copy constructor for `MyUniquePtr` would have to do if it
just copied the raw pointer field, the way the compiler-generated copy
constructor does for every other member:

```cpp
MyUniquePtr<int> a(new int(5));
MyUniquePtr<int> b = a;   // if this compiled...
```

Now `a` and `b` both store the same address. Both of their destructors will
eventually run, and both will call `delete` on that same address. The
second `delete` is a **double-delete** -- an instance of **undefined
behavior**, meaning the C++ standard places no requirement on what happens
next. In practice it corrupts the heap allocator's internal bookkeeping and
can crash the program at some unrelated later point, far from the line that
actually caused it. There is no correct body you could write for a copy constructor
here: either both copies think they own the pointer (double-delete waiting
to happen), or the "copy" would have to steal ownership from the original
(which is not a copy at all -- that is a move).

The fix is not to write a clever copy constructor. It is to delete it:

```cpp
MyUniquePtr(const MyUniquePtr&) = delete;
MyUniquePtr& operator=(const MyUniquePtr&) = delete;
```

This turns an accidental copy into a compile error instead of a runtime
heap-corruption bug. If you need two references to the same object with
shared, reference-counted ownership, that is what `std::shared_ptr`
is for -- a different type with a different contract, out of scope here.

### Move instead: transfer, don't duplicate

Ownership can still move from one `MyUniquePtr` to another -- moving is not
copying. A move constructor steals the source's pointer and **must** leave
the source owning nothing (its internal pointer set to `nullptr`):

```cpp
MyUniquePtr(MyUniquePtr&& other) noexcept {   // noexcept: promises this function never throws
                                              // an exception, which lets containers like
                                              // std::vector move objects instead of copying them
    ptr_ = other.ptr_;
    other.ptr_ = nullptr;   // critical: without this line, ~other() double-deletes
}
```

If you forget to null out `other`'s pointer, both the new object and the
(soon-to-be-destroyed) source object own the same address, and you are back
to a double-delete -- just one call deep instead of at the copy-constructor
call site. One of the "wrong" reference solutions this assignment is graded
against makes exactly this mistake, so the grader's leak/crash checks are
there for a reason, not decoration.

Move *assignment* has one more responsibility that move construction
doesn't: `*this` might already own something before the assignment runs.
That old object must be deleted before (or instead of) being silently
overwritten and leaked. And self-move-assignment --
`p = std::move(p);` -- must not delete the object out from under itself
just because `other` and `*this` happen to be the same object. Guard
against it explicitly.

### get(), release(), and reset() -- three different things

These three functions are the part students most often mix up:

| Function | What it does | Who owns the pointer afterward |
|---|---|---|
| `get()` | Returns the raw pointer to look at it | `MyUniquePtr` still owns it -- do not `delete` what `get()` returns |
| `release()` | Returns the raw pointer *and* forgets it | The caller now owns it -- you must `delete` it yourself eventually |
| `reset(p)` | Deletes what you currently own, then starts owning `p` | `MyUniquePtr` owns the new `p` (or nothing, if `p` is omitted) |

`reset()` has a subtle self-reset trap: `p.reset(p.get())` deletes the
pointer `p` currently owns and then tries to store it again -- if your
`reset()` deletes unconditionally and only afterward assigns the parameter,
it deletes the very pointer it was about to re-store, leaving `p` holding a
dangling address. The fix is to compare the incoming pointer against the
one you already own before deleting anything.

## Examples at a glance

To make every operation concrete, here is **one** running scenario: a
`MyUniquePtr<int>` named `p`, tracked through every operation it supports.
"Underlying object" means the heap `int` that `new` allocated -- as long as
some `MyUniquePtr` owns it, it is alive; once nothing owns it, `delete` has
run and it is gone.

| Call | Result | `p.get()` afterward | Underlying object | Why |
|------|--------|----------------------|--------------------|-----|
| `MyUniquePtr<int> p(new int(5));` | constructs `p` | address of the `int` (call it `A`) | alive, holds `5` | `p` now owns the object `new` just allocated |
| `p.get()` | returns `A` | `A` (unchanged) | alive, holds `5` | `get()` only looks -- it does not transfer or affect ownership |
| `*p` | `5` | `A` (unchanged) | alive, holds `5` | `operator*` dereferences the owned object; `p` still owns it afterward |
| `p->` (on a struct member) | reads/writes that member | `A` (unchanged) | alive | `operator->` behaves like `get()` followed by `->` on the raw pointer |
| `static_cast<bool>(p)` | `true` | `A` (unchanged) | alive | `operator bool` is `true` exactly when the owned pointer is non-null |
| `int* raw = p.release();` | `raw == A` | `nullptr` | still alive, but **nobody owns it now** | `release()` hands ownership to the caller; `p` forgets the pointer entirely without deleting it -- `raw` must be `delete`d by hand or it leaks |
| `p.reset(new int(9));` (starting from `p` owning `A`) | -- | address of the new `int` (call it `B`) | `A` is deleted, `B` is alive holding `9` | `reset(x)` deletes whatever `p` currently owns first, then takes ownership of `x` |
| `p.reset();` (no argument, `p` owns `B`) | -- | `nullptr` | `B` is deleted | omitting the argument is the same as `reset(nullptr)` -- delete the old object, own nothing |
| `p.reset();` again (already empty) | -- | `nullptr` | nothing to delete | resetting an already-empty `MyUniquePtr` is a no-op, not a crash -- there is no double-delete because `reset` compares against the pointer it already owns |
| `MyUniquePtr<int> q(std::move(p));` (`p` owns `A` beforehand) | `q` now owns `A` | `p.get() == nullptr` | `A` still alive, owned by `q` now | move construction steals the pointer and nulls the source -- `p` is left in the valid-but-empty state, safe to destroy or reset |
| `q = std::move(p);` where `q` owns `B` and `p` owns `A` | `q` now owns `A` | `p.get() == nullptr` | `B` is deleted, `A` is alive, owned by `q` | move assignment deletes whatever `q` used to own **before** stealing `p`'s pointer, so nothing leaks |
| `p = std::move(p);` (self-move-assignment) | `p` still owns whatever it owned before | unchanged | unchanged, still alive | a correct move assignment checks `this == &other` and returns immediately; without that check, `p` would delete its own object out from under itself before "stealing" it back |
| `p.swap(other);` | `p` and `other` trade owned pointers | `p.get()` becomes what `other.get()` was, and vice versa | both objects still alive, ownership swapped | `swap` exchanges the two raw pointers directly -- no allocation, no deletion, nothing is destroyed |

## Worked example: a `MyUniquePtr<int>` through construct, move, reset, release

This traces one sequence of calls end to end, the way you would step through
it in a debugger. Read "owner" as "which variable's destructor will
eventually call `delete` on this object" -- there must be exactly one owner
(or zero) at every step, never two.

```cpp
MyUniquePtr<int> a(new int(10));      // step 1
MyUniquePtr<int> b(std::move(a));     // step 2
b.reset(new int(20));                 // step 3
int* raw = b.release();               // step 4
MyUniquePtr<int> c(raw);               // step 5
```

| Step | Code | `a.get()` | `b.get()` | Heap objects alive | Owner | Why |
|------|------|-----------|-----------|---------------------|-------|-----|
| 1 | `MyUniquePtr<int> a(new int(10));` | `ptr A` (holds `10`) | -- | `ptr A` | `a` | the constructor takes ownership of the pointer `new` just returned |
| 2 | `MyUniquePtr<int> b(std::move(a));` | `nullptr` | `ptr A` | `ptr A` | `b` | move construction steals `a`'s pointer and nulls `a` out -- `a` is now a valid, empty `MyUniquePtr`; nothing double-owns `ptr A` |
| 3 | `b.reset(new int(20));` | `nullptr` | `ptr B` (holds `20`) | `ptr B` (`ptr A` just got `delete`d) | `b` | `reset` deletes what `b` currently owns (`ptr A`) before taking ownership of the new pointer (`ptr B`) -- this is the only line in the whole trace where a `delete` actually runs |
| 4 | `int* raw = b.release();` | `nullptr` | `nullptr` | `ptr B` (still alive, but unowned) | *nobody* (raw pointer `raw` in a plain `int*` variable) | `release()` hands `ptr B` to the caller as a plain pointer and forgets it -- `b` is now empty, and `ptr B` is temporarily not managed by any `MyUniquePtr` at all; if the program ended here without calling `delete raw` or wrapping it, `ptr B` would leak |
| 5 | `MyUniquePtr<int> c(raw);` | `nullptr` | `nullptr` | `ptr B` | `c` | the constructor re-establishes RAII ownership over the raw pointer `release()` had cut loose -- `c`'s destructor will now `delete ptr B` automatically when `c` goes out of scope |

At the end of this trace, `a` and `b` are both empty (safe to destroy or
`reset` again with no effect), and `c` owns `ptr B` -- when `c`'s destructor
runs, it deletes `ptr B` exactly once. Every heap object was deleted exactly
once (step 3's `delete` of `ptr A`, and `c`'s eventual destructor deleting
`ptr B`), and every step had exactly one owner or zero -- never two owners
of the same object at once.

### Leak-checking

Because this whole assignment is about getting deletion right, the grader
runs your test binary under both **Valgrind** (a program that runs your
compiled binary inside a simulator and reports every leaked allocation,
double-free, and invalid memory access it observes) and **AddressSanitizer
(ASan)** in addition to the normal Catch2 checks. A test can report "all
assertions passed" and still leak memory or narrowly avoid a crash --
Valgrind and ASan catch what the assertions alone cannot: leaked
allocations, double-frees, and use of memory after it was freed. Build and
run your own tests under ASan locally before submitting (see
**Compilation and Testing** below) -- it is much faster to read an ASan
report on your machine than to find out about a leak from the grader.

## Task

### Part 1 -- `MyUniquePtr<T>` (`my_unique_ptr.hpp`)

Implement every member declared in `my_unique_ptr.hpp`:

- `explicit MyUniquePtr(T* p = nullptr)` -- takes ownership of `p`.
  *Examples:* `MyUniquePtr<int> a(new int(5));` -- `a` now owns that `int`.
  `MyUniquePtr<int> empty;` -- default argument `nullptr` means `empty` owns
  nothing (`empty.get() == nullptr`, `static_cast<bool>(empty) == false`).
- `~MyUniquePtr()` -- deletes the owned pointer, if any.
  *Examples:* if `p` owns an `int`, its destructor calls `delete` on it
  exactly once, whenever `p` goes out of scope. If `p` is empty (owns
  `nullptr`), the destructor must **not** call `delete` on anything --
  `delete nullptr` is technically legal C++ (a no-op), but the point is
  there is nothing to free after `release()` was called, so a correct
  destructor here does no work at all.
- Copy constructor and copy assignment operator: `= delete`. (Already done
  for you -- do not remove these lines.)
- Move constructor and move assignment operator: transfer ownership, leave
  the source owning nothing, and (for assignment) release whatever `*this`
  owned first. Move assignment must be self-move-safe.
  *Examples:* `MyUniquePtr<int> b(std::move(a));` -- `b` now owns what `a`
  owned; `a.get() == nullptr` afterward, even if `a` owned nothing to begin
  with (moving from an already-empty `MyUniquePtr` just produces another
  empty one -- no crash, no special case needed). `b = std::move(a);` where
  `b` already owned something -- `b`'s old object must be deleted before
  `b` takes `a`'s pointer, or it leaks. `p = std::move(p);` (self-move
  assignment, same variable on both sides) must leave `p` owning exactly
  what it owned before -- without an explicit `this == &other` check, `p`
  would `delete` its own object and then try to "steal" the now-dangling
  pointer from itself.
- `T* get() const` -- returns the owned pointer without giving up ownership.
  *Examples:* `p.get()` right after `MyUniquePtr<int> p(new int(5))` returns
  that address, and calling `get()` again immediately after returns the
  identical address -- `get()` never changes what `p` owns, no matter how
  many times you call it.
- `T* release()` -- returns the owned pointer and gives up ownership
  (`get()` becomes `nullptr` afterward).
  *Examples:* `int* raw = p.release();` -- `raw` now equals what `p.get()`
  used to return, `p.get()` is now `nullptr`, and the object itself is
  still alive in memory (nothing was deleted) but now unmanaged -- the
  caller must `delete raw` eventually or it leaks. Calling `release()` on
  an already-empty `MyUniquePtr` is legal and returns `nullptr` -- there is
  nothing to hand off, so there is nothing to do beyond that.
- `void reset(T* p = nullptr)` -- deletes the current pointer, then owns
  `p`. Must be safe when called as `reset(get())`.
  *Examples:* `p.reset();` on a `p` that already owns nothing is a no-op --
  no `delete` runs, `p.get()` stays `nullptr`. `p.reset(p.get());` (the
  self-reset trap) must leave `p` owning the exact same pointer it started
  with and must **not** delete it -- your `reset` has to compare the
  incoming pointer against the one already owned before deleting anything,
  or this deletes the object out from under itself. Calling `reset()` twice
  in a row (`p.reset(); p.reset();`) is safe both times -- the second call
  is just another no-op on an already-empty `p`.
- `void swap(MyUniquePtr& other)` -- exchanges ownership between `*this` and
  `other` (this assignment uses a **member** `swap`; do not add a
  non-member overload).
  *Examples:* if `a` owns object `X` and `b` owns object `Y`, after
  `a.swap(b)`, `a.get()` returns `Y`'s address and `b.get()` returns `X`'s
  address -- no allocation or deletion happens, only the two internal
  pointers trade places. `a.swap(a)` (swapping a `MyUniquePtr` with itself)
  must leave `a` unchanged -- swapping a variable's own two fields with
  themselves is always safe, but confirm your implementation does not
  accidentally null it out.
- `T& operator*() const`, `T* operator->() const` -- dereference/access the
  owned object. Undefined behavior if `get() == nullptr`, same as
  `std::unique_ptr`.
  *Examples:* if `p` owns a `Point{3, 4}`, `(*p).x == 3` and `p->y == 4`;
  writing through it (`p->x = 10;`) mutates the owned object in place, and
  `p` still owns the same object afterward -- dereferencing never transfers
  or affects ownership. Calling `*p` or `p->` when `p.get() == nullptr` is
  undefined behavior (do not guard against it inside these operators --
  the contract, like `std::unique_ptr`'s, is that the caller must not do
  this).
- `explicit operator bool() const` -- `true` if a non-null pointer is owned.
  *Examples:* `static_cast<bool>(p)` is `true` right after
  `MyUniquePtr<int> p(new int(5))`, becomes `false` right after
  `p.release()` or `p.reset()` with no arguments, and is `false` for a
  default-constructed `MyUniquePtr<int> p;` from the start. The `explicit`
  keyword means `if (p)` still compiles (contexts that require a `bool`
  convert implicitly) but `int x = p;` does not -- this prevents accidental
  pointer-to-int conversions elsewhere in code that uses `MyUniquePtr`.

### Part 2 -- using `std::unique_ptr` (`std_smart_pointers.hpp`)

`Shape`, `Circle`, and `Square` are provided, complete. Implement three
functions using `std::unique_ptr` and `std::make_unique`:

- `std::unique_ptr<Shape> make_shape(const std::string& kind, double size)`
  -- a factory. `"circle"` builds a `Circle` with that radius, `"square"`
  builds a `Square` with that side length, anything else returns an empty
  `std::unique_ptr<Shape>`. Use `std::make_unique`, not `new`.
- `double total_area(const std::vector<std::unique_ptr<Shape>>& shapes)` --
  takes the vector **by reference**, only inspects it (sums `area()` over
  every non-null entry), and does not take ownership of anything in it.
- `std::unique_ptr<Shape> claim_biggest(std::vector<std::unique_ptr<Shape>>& shapes)`
  -- finds the largest-area shape, **moves** it out of the vector (its slot
  becomes an empty `unique_ptr`, the element itself is not erased), and
  returns it **by value**. A `std::unique_ptr` cannot be copied out of a
  vector -- only moved -- so writing this function correctly requires
  `std::move`.

## Files

| File | Purpose |
|------|---------|
| `my_unique_ptr.hpp` | Part 1 -- implement `MyUniquePtr<T>` here |
| `std_smart_pointers.hpp` | Part 2 -- implement the three functions here; `Shape`/`Circle`/`Square` are complete |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./unique-ptr-from-scratch_tests
```

To check your own work for leaks and double-frees before submitting, add
`-fsanitize=address` and re-run:

```bash
g++ -std=c++17 -Wall -Wextra -g -fsanitize=address \
    -I<path-to-your-submission> \
    <path-to-catch2-single-include-or-lib-setup> \
    visible-tests/test_catch.cpp -o tests_asan
./tests_asan
```

(If you already have the CMake build set up, adding
`target_compile_options(... PRIVATE -fsanitize=address)` and
`target_link_options(... PRIVATE -fsanitize=address)` to a second target is
the easier route.)

## Constraints

- Do not modify the class or function signatures in `my_unique_ptr.hpp` or
  `std_smart_pointers.hpp`.
- Do not use `std::unique_ptr`, `std::shared_ptr`, or any other smart
  pointer type inside `my_unique_ptr.hpp` -- build the ownership logic
  yourself with a raw pointer.
- Do not add a custom deleter template parameter to `MyUniquePtr`.
  `MyUniquePtr<T>` always deletes with a plain `delete` (single-object
  ownership, not array ownership, and no custom cleanup).
- Do not use exceptions (`throw`/`try`/`catch`) anywhere in either file.
- In `std_smart_pointers.hpp`, use `std::make_unique`, not `new`, to build
  shapes.

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `std::unique_ptr`/`std::shared_ptr` in `my_unique_ptr.hpp` (source check) | 10 |
| Visible tests (Catch2) | 30 |
| Hidden tests (Catch2) | 40 |
| Memory safety (Valgrind) | 10 |
| Memory safety (AddressSanitizer) | 10 |
| **Total** | **100** |

## Submission

Submit both `my_unique_ptr.hpp` and `std_smart_pointers.hpp`. Do not rename
either file.

---

## Going further

- `std::unique_ptr` supports a **custom deleter** as a second template
  parameter (`std::unique_ptr<T, Deleter>`), so it can own things that
  aren't freed with plain `delete` -- a `FILE*` closed with `fclose`, for
  example. That requires storing and invoking a callable, which needs
  either a function pointer or a lambda -- both are topics for later in the
  course. Once you've seen those, come back and add an optional deleter
  template parameter to `MyUniquePtr`.
- Add a `MyUniquePtr<T[]>` partial specialization (a separate version of the
  template that the compiler picks instead of the general one whenever `T`
  is an array type) that calls `delete[]` instead of `delete`, the way
  `std::unique_ptr` does for array types.
- Implement a non-member `swap(MyUniquePtr<T>&, MyUniquePtr<T>&)` free
  function that calls the member `swap` -- this is the pattern the standard
  library itself uses (`std::swap` has an overload that calls a type's
  member `swap` when one exists).
- Read about `std::shared_ptr` and its control block. What has to change
  about the ownership model for copying to become safe?
