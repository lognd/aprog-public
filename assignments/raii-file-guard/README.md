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

The constructor calls `::open()` with the flags above. If `::open()`
succeeds, the returned fd is stored and `is_open()` becomes true. If it
fails (returns -1), store -1 and leave `errno` exactly as `::open()` set
it -- do not print anything, do not throw, do not terminate. A missing
file on `Mode::Read` is an expected outcome the caller checks with
`is_open()`, not an error condition you handle inside `FileGuard`.

The destructor calls `close()` if and only if `is_open()` is true.

`close()` itself must be safe to call zero, one, or many times: the first
call (whether explicit or from the destructor) closes the fd and sets the
internal state so that `is_open()` becomes false and `fd()` becomes -1;
every call after that is a no-op.

`write_all` must not assume a single `::write()` call writes everything --
loop, accumulating bytes written, until either all `n` bytes are written
(return `n`) or a `::write()` call fails (return -1). This is the same
partial-write loop from the write-your-first-syscalls activity, now living
inside a method.

`read_some` is a thin wrapper: call `::read()` once with the given buffer
and capacity, and return exactly what it returns (bytes read, 0 at EOF -- end of file,
meaning there is nothing left to read -- or -1 on error). Do not loop here -- that is the caller's job, and `read_all`
below is where the looping version lives.

`read_all` reads in a loop (using a buffer of your choosing, in terms of
`read_some` or `::read` directly) until end-of-file, accumulating everything
read into a `std::string`, which it returns.

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
