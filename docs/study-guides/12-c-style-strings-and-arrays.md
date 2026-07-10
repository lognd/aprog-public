# Study Guide 12: C-Style Strings & Arrays

This module drills the null-terminated C-string model that pointer
arithmetic operates on: what `'\0'` means, why `sizeof` and `strlen`
answer different questions, the classic bug patterns C strings invite, and
how `std::string` fixes most of them. It ends with implementing a
word-level string library using nothing but `char*`.

## Know before you start

- Pointer arithmetic, `p++` traversal, and array-to-pointer decay
  [assumed: row 11 -- Pointers]
- `const` with pointers (`const char*` vs `char* const`) [assumed: row 11
  -- Pointers]

## Taught here

Concept: the null-terminated C string model
- Know that a C string is a `char` array with a convention layered on top:
  the first `'\0'` byte marks where the meaningful data ends.
- Know that `char s[] = "hello";` allocates 6 bytes, not 5 -- the compiler
  appends the `'\0'` terminator automatically.
- Know that `sizeof(s)` on a char array is a compile-time constant equal to
  the declared/inferred byte count (including the terminator slot), while
  `strlen(s)` is a runtime scan that counts bytes up to (but not including)
  the first `'\0'` -- the two answer different questions and can disagree.
- Know that everything downstream of printing or measuring a C string
  (`std::cout << buf`, `strlen`) only looks as far as the first `'\0'`;
  bytes after it still exist in memory but are invisible to string
  functions.
- Know that a buffer's declared size (how many bytes it can hold) and a C
  string's current length (how many bytes are meaningful right now) are
  independent numbers that can change separately as the buffer is reused.

Concept: the core cstring functions as loops
- Be able to trace `strlen(s)` as: walk forward counting bytes while `s[i]
  != '\0'`, returning the count (never including the terminator).
- Be able to trace `strcpy(dst, src)` as: copy every byte of `src` into
  `dst`, including the final `'\0'`, with no bounds checking -- the caller
  is responsible for ensuring `dst` is large enough.
- Be able to trace `strcat(dst, src)` as: first scan forward through `dst`
  to find its own terminator (like `strlen` would), then copy `src` byte
  by byte starting at that position, ending with a fresh `'\0'`.
- Be able to implement `strlen`, `strcpy`, `strcat`, `strcmp`, and reverse
  from first principles using pointer arithmetic, following the shared "walk
  until `'\0'`" loop skeleton.

Concept: classic C-string bugs
- Know that comparing two `char*` with `==` compares addresses, not
  content -- `strcmp` (or `std::string`'s `operator==`) is required to
  compare the actual characters.
- Know that a string literal (`const char* s = "dog";`) points at read-only
  memory, so writing through it (`s[0] = 'x';`) is undefined behavior,
  while `char s[] = "dog"; s[0] = 'x';` is fine because the array is the
  program's own writable storage.
- Know that a buffer overflow is writing past the end of a fixed-size
  `char` array, and that `strncpy` can silently omit the null terminator
  when the source string exactly fills (or exceeds) the destination
  buffer.
- Know that undefined behavior is a category of bug where the C++ standard
  places no limit on what happens -- crash, silent memory corruption, or
  code that appears to work until it does not.

Concept: std::string vs C strings
- Know that `std::string` stores its own length (`.size()`), unlike a C
  string which has no stored length and must be found by scanning for
  `'\0'`.
- Know that `std::string` provides `operator+` for concatenation and
  `operator==` for content comparison, replacing manual buffer management
  and `strcmp`.
- Know that `.c_str()` is the bridge back to C-style APIs: it returns a
  `const char*` view of a `std::string`'s contents.
- Know that in-place mutation is legal on a `char[]` array but undefined
  behavior on a string literal, mirroring the same distinction that applies
  to raw C strings.

Concept: word-level C-string operations
- Be able to define a "word" as a maximal non-empty run of non-space
  characters and reason about word boundaries while scanning a C string.
- Be able to perform in-place mutation (trim, capitalize, lowercase) on a
  caller-owned `char*` buffer without any heap allocation.
- Know that a function body defined directly inside a header must be marked
  `inline`, or including that header from more than one `.cpp` file causes
  a linker "multiple definition" error.

## Study checklist

- [ ] Given a `char` array with an early `'\0'`, predict what `strlen` and
      `std::cout <<` each report.
- [ ] Trace `strcat(dst, src)` by hand, including finding `dst`'s existing
      terminator first.
- [ ] Explain why `==` on two `char*` is a common bug and what to use
      instead.
- [ ] Explain why writing to a string literal is undefined behavior but
      writing to a `char[]` array is not.
- [ ] Explain why a header-defined function body needs `inline`.

## Practiced in

`cstring-predictor`, `char-by-char`, `cstring-whodunit`, `cstring-vs-stdstring`, `sentence-tools`
