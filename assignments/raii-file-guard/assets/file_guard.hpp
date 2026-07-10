// RAII File Guard -- starter header.
//
// FileGuard wraps a single POSIX file descriptor and ties its lifetime to
// the lifetime of the FileGuard object: the constructor opens the file, the
// destructor closes it. This is the RAII pattern (Resource Acquisition Is
// Initialization) applied to the simplest resource you already know how to
// manage by hand -- a file descriptor from open()/close().
//
// Invariants:
//
//   1. If is_open() is true, fd() returns a valid, open file descriptor that
//      this FileGuard -- and only this FileGuard -- owns.
//   2. If is_open() is false, fd() returns -1 and no syscall is made against
//      it.
//   3. close() is idempotent: calling it once explicitly closes the fd and
//      marks the guard closed; calling it again (or letting the destructor
//      run afterward) does nothing. The underlying fd number is never
//      closed twice.
//
// Copying is deleted on purpose. A FileGuard is the sole owner of one fd;
// if you could copy it, two FileGuard objects would believe they each own
// the same fd, and whichever one's destructor ran second would call
// close() on an fd already closed (or, worse, on an unrelated fd that the
// OS has since reused for a different file -- the "double-close hazard"
// described in the README). Pass FileGuard by reference wherever you would
// otherwise be tempted to copy it.
//
// Do not modify this file. Implement every declared method in
// file_guard.cpp.
#pragma once

#include <string>

// How to open the file. Mirrors the flag combinations you used directly
// with ::open() in the write-your-first-syscalls activity.
enum class Mode {
    Read,   // O_RDONLY
    Write,  // O_WRONLY | O_CREAT | O_TRUNC, mode 0644
    Append, // O_WRONLY | O_CREAT | O_APPEND, mode 0644
};

class FileGuard {
public:
    // Opens `path` with the flags implied by `mode`.
    //
    // On success, is_open() is true and fd() returns the open descriptor.
    // On failure (the ::open() call itself fails), is_open() is false,
    // fd() returns -1, and errno is left exactly as ::open() set it, so the
    // caller can inspect it immediately after construction. This
    // constructor never throws and never terminates the program on a
    // failed open -- a missing file is an expected, recoverable outcome,
    // not a programmer bug.
    FileGuard(const char* path, Mode mode);

    // Closes the owned fd if is_open() is true. This is the only code in
    // the program guaranteed to run on every path out of the enclosing
    // scope -- normal fall-through, an early return, a break out of a
    // loop -- which is the entire point of RAII. See the README.
    ~FileGuard();

    // Copying is forbidden: two FileGuard objects must never believe they
    // each own the same fd. Deleting these tells the compiler to reject
    // any attempt to copy-construct or copy-assign a FileGuard, instead of
    // silently compiling code that would double-close.
    FileGuard(const FileGuard&) = delete;
    FileGuard& operator=(const FileGuard&) = delete;

    // True iff this FileGuard currently owns an open fd.
    bool is_open() const;

    // The owned fd, or -1 if is_open() is false.
    int fd() const;

    // Explicitly closes the owned fd before the FileGuard goes out of
    // scope. Idempotent: if is_open() is already false (whether because
    // close() was already called, or the constructor's open() failed),
    // this does nothing -- in particular it must not call ::close() a
    // second time on the same fd number.
    void close();

    // Writes exactly `n` bytes from `data` to the owned fd, looping on
    // partial writes (a single ::write() call is not guaranteed to write
    // everything you asked for -- this is the same partial-write loop from
    // the syscalls activity). Returns `n` on success, or -1 if a ::write()
    // call fails before all bytes are written. Precondition: is_open().
    long write_all(const char* data, long n);

    // A single ::read() call into `buf`, capacity `cap`. Returns whatever
    // ::read() returns: the number of bytes read (0 at end-of-file, or
    // fewer than `cap` on a partial read), or -1 on error. Precondition:
    // is_open().
    long read_some(char* buf, long cap);

    // Reads until end-of-file, accumulating everything read into a
    // std::string. Precondition: is_open().
    std::string read_all();

private:
    int fd_;
};
