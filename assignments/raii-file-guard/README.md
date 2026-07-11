# RAII File Guard

Every file descriptor you open with `::open()` occupies a slot in your
process's file descriptor table, and that table is finite. If you forget to
call `::close()`, the slot stays occupied until the process exits -- there is
no garbage collector coming to reclaim it for you. `FileGuard` is a class (a
programmer-defined type that bundles data with the functions that operate on
it) whose object -- an instance of that class, i.e. one concrete variable
built from it -- owns a file descriptor. Every class has a **constructor**
(a special function that runs automatically when an object is created,
usually named after the class) and can have a **destructor** (a special
function, named `~ClassName`, that runs automatically when the object's
lifetime ends). `FileGuard` exists so that "forgetting to close" becomes
structurally impossible: the file descriptor's lifetime is tied to the
lifetime of a `FileGuard` object, and the object's destructor -- not a line
of code you have to remember to write at every exit point -- does the
closing.

## Learning goals

- Understand RAII (Resource Acquisition Is Initialization): binding a
  resource's lifetime to an object's lifetime instead of to hand-written
  cleanup code
- Recognize why a destructor is the only code guaranteed to run on every
  exit path out of a scope, including early returns and thrown-away branches
- Reason about a finite, process-wide resource (the file descriptor table)
  and what happens when it leaks
- Understand the double-close hazard and why deleting the copy constructor
  and copy assignment operator is the correct fix, not an incidental detail
- Practice the partial-write loop from POSIX I/O (POSIX is the standard that
  defines the open/read/write/close system calls shared across Unix-like
  operating systems) in a class method instead of free-standing code

## Background

### Resource lifetime tied to object lifetime

A `FileGuard` constructor calls `::open()`. Its destructor calls
`::close()`. Nothing else in the class touches the fd's existence. This
means that anywhere a `FileGuard` variable goes out of scope -- the end of a
function, an early `return`, a `break` out of a loop, or an exception
unwinding the stack (an exception is a signal thrown to report an error;
"unwinding the stack" means the program leaves each function it is currently
inside, one after another, running each one's destructors as it goes -- not
something you will trigger in this assignment, since you are not using
exceptions yet, but worth knowing) -- the destructor runs and the
fd gets closed. You do not write a `close()` call at each of those exit
points. You write it once, in the destructor, and the compiler guarantees it
runs everywhere it needs to.

Compare this to the alternative: a raw fd stored in an `int`, with a
`::close()` call the programmer is responsible for placing before every
`return`. Consider a function that opens a file, does some work, and returns
early if a condition fails:

```cpp
int process(const char* path) {
    int fd = open(path, O_RDONLY);
    if (some_condition) {
        return -1; // BUG: fd is never closed on this path
    }
    // ... use fd ...
    close(fd);
    return 0;
}
```

The bug is easy to write and easy to miss in review, because the function
still compiles, still runs, and still works most of the time -- it only
leaks a file descriptor, which does not crash anything immediately. It just
quietly consumes one slot in the process's fd table every time this path is
taken. With `FileGuard`, that early return is not a bug at all:

```cpp
int process(const char* path) {
    FileGuard g(path, Mode::Read);
    if (some_condition) {
        return -1; // g's destructor runs here. The fd is closed. No leak.
    }
    // ... use g ...
    return 0; // g's destructor runs here too.
}
```

### Why the fd table matters

Every process has a finite table mapping small integers (file descriptors)
to open files, pipes, and sockets. The exact limit is configurable (see
`ulimit -n` on your shell, or `getrlimit`/`setrlimit` in code) but it is
never infinite. If a program opens files in a loop and never closes them --
even if each individual file's contents are tiny and irrelevant -- it will
eventually exhaust the table, and every subsequent `open()` call in the
entire process will fail, no matter what file it's for. This is not a
theoretical concern: it is one of the most common resource-leak bugs in
long-running server code, and it is exactly what the hidden tests for this
assignment are designed to catch.

The leaked fds are only ever reclaimed when the process exits and the
kernel tears down its whole fd table at once. Nothing inside the process
can get them back once they are lost.

### The double-close hazard

`FileGuard`'s copy constructor and copy assignment operator are deleted in
the header:

```cpp
FileGuard(const FileGuard&) = delete;
FileGuard& operator=(const FileGuard&) = delete;
```

Here is why. Suppose copying were allowed, and you wrote:

```cpp
FileGuard a("log.txt", Mode::Write);
FileGuard b = a; // if this compiled, b.fd_ == a.fd_
```

Now two `FileGuard` objects both believe they own the same fd. When `b`
goes out of scope first, its destructor closes the fd. When `a` goes out of
scope afterward, its destructor closes the same fd number *again*. By that
point, the operating system may have already handed that exact fd number to
a completely unrelated file opened by other code elsewhere in the program --
and `a`'s destructor closes someone else's file out from under them. This is
the double-close hazard: the bug is not "closing something already closed"
(which is often harmless), it is "closing whatever the OS has since decided
to put in that slot."

`= delete` turns this from a runtime bug into a compile error. If you try to
copy a `FileGuard`, the compiler rejects the program before it ever runs.
This is why `FileGuard` is always passed by reference (`const FileGuard&` or
`FileGuard&`) in function signatures -- passing by value would require a
copy, which is exactly what is forbidden.

`close()` itself must also be idempotent (calling it many times has the same
effect as calling it once, with no extra side effects on the second or later
call) for a related reason: even without
copying, a caller might call `close()` explicitly and then let the
`FileGuard` go out of scope normally. The destructor must recognize that the
fd was already closed and do nothing, rather than closing whatever fd
number the OS has since reused.

### RAII beyond files

This pattern -- acquire a resource in a constructor, release it in a
destructor -- is not specific to file descriptors. The same shape manages
heap memory (you will meet this formally in the Dynamic Memory topic), lock
objects that must be released even if the code between lock and unlock
returns early, and network sockets, which are just another kind of file
descriptor on POSIX systems. In fact, `std::fstream` -- which you have
already used -- is itself an RAII wrapper over a file: its destructor closes
the underlying file for you, which is exactly the guarantee `FileGuard`
reimplements by hand here, one layer closer to the operating system.

## Examples at a glance

To make the whole class concrete, here is **one** scenario -- writing the
two-byte string `"hi"` to a file named `notes.txt`, then reopening it -- and
what every relevant method does for it. Read this table first; it is the
whole assignment in miniature.

| Call (in order) | Result | Why |
|------|--------|-----|
| `FileGuard g("notes.txt", Mode::Write)` | `g.is_open() == true`, `g.fd() >= 0` (e.g. `3`) | `Mode::Write` creates the file if it does not exist and truncates it if it does |
| `g.write_all("hi", 2)` | returns `2` | both bytes were written in a single underlying `::write()` call, so the partial-write loop exits immediately with `written == n` |
| *(end of scope)* | destructor runs, fd is closed | `g` goes out of scope, so `~FileGuard()` calls `close()` automatically -- no explicit `close()` call was needed |
| `FileGuard g2("notes.txt", Mode::Read)` | `g2.is_open() == true` | the file now exists (created above), and `Mode::Read` maps to `O_RDONLY`, which succeeds against an existing file |
| `g2.read_all()` | returns `"hi"` (size `2`) | `read_all` loops on `read_some` until it sees `0` (end-of-file) and accumulates every byte read in between |
| `FileGuard g3("missing.txt", Mode::Read)` | `g3.is_open() == false`, `g3.fd() == -1` | the file does not exist, so `::open()` fails; this is an expected outcome the caller checks with `is_open()`, not an error `FileGuard` reports itself |
| `g.close()` then `g.close()` again | `is_open() == false` and `fd() == -1` both times | the first `close()` actually closes the fd; the second is a no-op because `is_open()` is already false -- this is what makes `close()` safe to call any number of times |

## Worked example: constructing, using, and destroying a `FileGuard`

This is the single most important thing to understand in the assignment, so
here is every step spelled out. We create a file named `notes.txt`, write
`"hi"` into it through a `FileGuard`, let that guard go out of scope, then
reopen the same file for reading through a second `FileGuard`.

| Step | Code | What happens to the file descriptor | Reason |
|------|------|--------------------------------------|--------|
| 1 | `FileGuard g("notes.txt", Mode::Write);` | The constructor calls `::open("notes.txt", O_WRONLY \| O_CREAT \| O_TRUNC, 0644)`. Say the OS hands back fd `3`. `g` stores `fd_ = 3`. | `Mode::Write` both creates the file if absent and truncates it to empty if present, so we always start from a clean file |
| 2 | `g.write_all("hi", 2)` | One `::write(3, "hi", 2)` call succeeds and reports `2` bytes written. The loop's running total (`written`) reaches `n` (`2`), so the loop exits and `write_all` returns `2`. | The partial-write loop only keeps looping while `written < n`; a single successful call that writes everything ends the loop on its first iteration |
| 3 | `g` reaches the closing `}` of its scope | `g`'s destructor `~FileGuard()` runs automatically. It calls `close()`, which sees `fd_ != -1`, calls `::close(3)`, and sets `fd_ = -1`. | This is RAII's entire guarantee: the programmer never wrote a `close()` call, yet the fd is still closed the instant the object's lifetime ends |
| 4 | `FileGuard g2("notes.txt", Mode::Read);` | The constructor calls `::open("notes.txt", O_RDONLY)`. The file exists (created in step 1) and now contains `"hi"`, so the OS returns a fresh fd, say `3` again (the same number is free to reuse now that step 3 closed it). `g2.is_open() == true`. | `Mode::Read` never creates a file; it only succeeds because the file was actually created and populated in the earlier steps |
| 5 | `g2.read_all()` | `read_all` calls `read_some` in a loop: first call reads `2` bytes (`"hi"`) into its internal buffer and appends them to the result string; the next call reads `0` bytes, which signals end-of-file, so the loop stops. | `read_all` must keep looping until it sees the `0`-byte end-of-file signal, not stop after the first `read_some` call, in case the file is larger than one buffer |
| end | -- | `read_all()` returns the string `"hi"`. `g2` then goes out of scope and its destructor closes fd `3` a second time (a different, later open of the same number -- not a double-close of the same open file). | The exact expected observable outcome: the two bytes written in step 2 come back unchanged in step 5, and every fd this program opened has been closed by the time the program ends |

Note step 3 is the crux of the whole assignment: nothing in `main()`
(or wherever `g` lives) ever calls `g.close()` or `::close(3)` directly.
The destructor is the only code that does, and the compiler guarantees it
runs the moment `g`'s scope ends -- on a normal fall-through exit exactly
as shown here, but equally on an early `return` or a `break` out of a loop.

## Task

Implement every method declared in `file_guard.hpp` inside `file_guard.cpp`.

```cpp
enum class Mode { Read, Write, Append };

class FileGuard {
public:
    FileGuard(const char* path, Mode mode);
    ~FileGuard();

    FileGuard(const FileGuard&) = delete;
    FileGuard& operator=(const FileGuard&) = delete;

    bool is_open() const;
    int fd() const;

    void close();

    long write_all(const char* data, long n);
    long read_some(char* buf, long cap);
    std::string read_all();
};
```

`Mode` maps to `::open()` flags as follows:

| Mode | Flags | Creation mode |
|------|-------|---------------|
| `Read` | `O_RDONLY` | -- |
| `Write` | `O_WRONLY \| O_CREAT \| O_TRUNC` | `0644` |
| `Append` | `O_WRONLY \| O_CREAT \| O_APPEND` | `0644` |

**The constructor calls `::open()` with the flags above.** If `::open()`
succeeds, the returned fd is stored and `is_open()` becomes true. If it
fails (returns -1), store -1 and leave `errno` exactly as `::open()` set
it -- do not print anything, do not throw, do not terminate. A missing
file on `Mode::Read` is an expected outcome the caller checks with
`is_open()`, not an error condition you handle inside `FileGuard`.

- **Example (create-and-write):** `FileGuard("notes.txt", Mode::Write)` on
  a nonexistent `notes.txt` creates it and leaves `is_open() == true`,
  **`fd() >= 0`** (some non-negative descriptor number, e.g. `3`).
- **Example (truncate on write):** `FileGuard("notes.txt", Mode::Write)`
  on a `notes.txt` that already contains `"old contents"` truncates it to
  empty -- reading it back afterward yields **`""`**, not `"old contents"`.
- **Tricky case (missing file on read):** `FileGuard("missing.txt",
  Mode::Read)` where `missing.txt` does not exist leaves
  **`is_open() == false` and `fd() == -1`** -- no crash, no thrown
  exception, `errno` simply reflects whatever `::open()` set (typically
  `ENOENT`).

**The destructor calls `close()` if and only if `is_open()` is true.**

- **Example (normal scope exit):** a `FileGuard g("notes.txt",
  Mode::Write)` that falls out of scope normally has its fd
  **closed automatically** -- no code in the caller calls `close()` at
  all, yet the file is fully written and closed on disk.
- **Edge case (already-failed open):** a `FileGuard` whose constructor's
  `::open()` failed (`is_open() == false`) runs its destructor with
  **no effect at all** -- there is no fd to close, so `close()` is never
  actually invoked against the OS.

**`close()` itself must be safe to call zero, one, or many times.** The
first call (whether explicit or from the destructor) closes the fd and
sets the internal state so that `is_open()` becomes false and `fd()`
becomes -1; every call after that is a no-op.

- **Example (single close):** after `g.close()` on an open guard,
  **`g.is_open() == false` and `g.fd() == -1`**.
- **Tricky case (double close):** calling `g.close()` a second time right
  after the first changes nothing further -- `is_open()` is still `false`
  and `fd()` is still `-1`, and **no second `::close()` syscall** is made
  on the (possibly already-reused) fd number.
- **Edge case (close on failed open):** calling `g.close()` on a guard
  whose constructor's `::open()` already failed (`is_open()` was already
  `false`) is a **no-op from the start** -- `fd()` was already `-1` and
  stays `-1`.

**`write_all` must not assume a single `::write()` call writes
everything** -- loop, accumulating bytes written, until either all `n`
bytes are written (return `n`) or a `::write()` call fails (return -1).
This is the same partial-write loop from the write-your-first-syscalls
activity, now living inside a method.

- **Example (single call suffices):** `g.write_all("hi", 2)` returns
  **`2`** on a guard opened with `Mode::Write`.
- **Empty-input case:** `g.write_all("", 0)` returns **`0`** -- writing
  zero bytes trivially succeeds without ever calling `::write()`.
- **Error case (partial write then failure):** if the underlying
  `::write()` call fails partway through (say, the disk fills up after
  some bytes were already written), `write_all` returns **`-1`** rather
  than the partial count -- the caller cannot tell from the return value
  alone how many bytes actually made it, only that the requested write as
  a whole did not complete.

**`read_some` is a thin wrapper:** call `::read()` once with the given
buffer and capacity, and return exactly what it returns (bytes read, 0 at
EOF -- end of file, meaning there is nothing left to read -- or -1 on
error). Do not loop here -- that is the caller's job, and `read_all`
below is where the looping version lives.

- **Example (partial read):** on a file containing `"0123456789"`,
  `g.read_some(buf, 4)` returns **`4`** and fills `buf` with `"0123"` --
  exactly one `::read()` call's worth, even though the file has 10 bytes
  total.
- **Example (continues from read position):** calling `g.read_some(buf,
  64)` again immediately after, on the same still-open guard, continues
  from where the fd's read position left off (**`"456789"`**), not from
  the beginning of the file.
- **Edge case (EOF):** calling `g.read_some(buf, 64)` once the fd has
  already reached the end of the file returns **`0`** -- the end-of-file
  signal, distinct from `-1` (error).

**`read_all` reads in a loop** (using a buffer of your choosing, in terms
of `read_some` or `::read` directly) until end-of-file, accumulating
everything read into a `std::string`, which it returns.

- **Example (basic round trip):** `g.read_all()` returns **`"hi"`** on a
  file that was written with `write_all("hi", 2)`.
- **Empty-input case:** `g.read_all()` returns **`""`** on a freshly
  created, still-empty file -- the first underlying read immediately
  reports end-of-file, so the loop never appends anything and returns an
  empty string, not an error.
- **Tricky case (already consumed):** calling `g.read_all()` a second
  time on the same guard, right after a first call already consumed the
  whole file, returns **`""`** again -- the fd's read position is already
  at the end, so there is nothing left to read.

## Files

| File | Purpose |
|------|---------|
| `file_guard.hpp` | Declarations and invariant contract (the rules this class always guarantees, such as "an fd is closed exactly once") -- do not modify |
| `file_guard.cpp` | Write your implementation here |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

Build and run the visible tests locally:

```bash
g++ -std=c++17 -Wall -Wextra -Werror \
    -I. file_guard.cpp visible-tests/test_catch.cpp \
    -o file_guard_tests
./file_guard_tests
```

You will need Catch2 installed, or you can fetch it via CMake. The grader
uses CMake internally; see `visible-tests/CMakeLists.txt` for details.

## Constraints

- Do not modify `file_guard.hpp`.
- Use POSIX file descriptors (`::open`, `::read`, `::write`, `::close`) --
  do not use `fopen`, `std::fstream`, `std::ifstream`, or `std::ofstream`.
- Do not throw exceptions.
- Do not use `new`, `delete`, or dynamic memory of any kind.
- Every open fd owned by a `FileGuard` must be closed exactly once, no
  matter how many times `close()` is called or whether the destructor also
  runs afterward.

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `fopen`/`fstream`/`throw`/`new`/`delete` (source check) | 10 |
| Visible tests (Catch2) | 20 |
| Hidden tests (Catch2) | 70 |
| **Total** | **100** |

The compilation check is a gate: if your code does not compile, no further
tests run.

## Submission

Submit a single file named `file_guard.cpp`. Do not rename it.

---

## Going further

- Suppose you wanted to write a function `FileGuard open_log()` that opens
  a file and returns the `FileGuard` to the caller by value. Try declaring
  that signature and see what the compiler says. Which deleted member is
  the problem, and why does returning by value require it? The Dynamic
  Memory (Big 5, move semantics) topic introduces move constructors and
  move assignment, which are exactly the feature that lets ownership of a
  resource like a file descriptor transfer between objects without ever
  copying it -- keep this question in mind when you get there.
- Compare `FileGuard` to `std::fstream`. Both are RAII wrappers around a
  file, but `std::fstream` is copy-disabled for the same reason `FileGuard`
  is, and it does support move semantics already (`std::fstream` is
  moveable in the standard library, even though you have not built that
  capability into `FileGuard` yet). Open the same file both ways and step
  through what each destructor does with a debugger.
- Look up `dup()`. It creates a second file descriptor that refers to the
  same underlying open file description as an existing one -- but unlike
  copying a `FileGuard`, the two fd numbers are genuinely independent from
  the OS's point of view (each has to be closed separately, and neither
  closing one closes the other). What would it take to add a `duplicate()`
  method to `FileGuard` that returns a new, independently-owned fd instead
  of aliasing the existing one (aliasing means two names referring to the
  same underlying thing, so an action through one name affects the other)?
  Why does this sidestep the double-close hazard that copying does not?
