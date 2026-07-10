# Study Guide 16: Streams & Files

This module covers the C++ stream abstraction: `std::cin`/`std::cout`
mechanics and state flags, `<iomanip>` formatting manipulators,
`std::ifstream` file reading and its classic bugs, and `std::ios::binary`
for reading raw byte layouts. It ends with a log-parsing assignment that
combines file streams, string streams, and formatted output.

## Know before you start

- Byte-level reasoning about C strings and buffers [assumed: row 12 --
  C-Style Strings & Arrays]
- `sizeof` and how it reports byte counts of primitive types [assumed:
  row 5 -- Variables & Type]

## Taught here

Concept: the stream model and state flags
- Know that a stream is an object representing a flow of data in or out of
  a program, one character at a time, hiding whether the source is the
  keyboard, a file, or an in-memory string.
- Know that `operator<<` chains left to right, and that `operator>>` skips
  leading whitespace and stops at the next whitespace character.
- Know that `std::getline` reads an entire line including embedded spaces
  and does not skip leading whitespace, which is why mixing `>>` and
  `getline` on the same stream is a classic bug: `>>` leaves a trailing
  newline in the buffer that the next `getline` immediately consumes as an
  empty line.
- Know the stream state flags `fail()` and `good()`, and that once a
  stream's failbit is set, every subsequent `>>` on it becomes a no-op
  until `clear()` is called; `clear()` resets the error flags but does not
  rewind the stream's read position.
- Know that `while (stream >> val)` is the correct loop idiom because
  `operator>>` returns a reference to the stream, which converts to `bool`
  via its failure state -- this is different from (and safer than) `while
  (!stream.eof())`, which only becomes true one read too late.

Concept: output formatting with iomanip
- Know that `std::ostringstream` is an in-memory output buffer supporting
  the same `<<` syntax as `std::cout`; calling `.str()` extracts the
  built string.
- Know that most stream manipulators (`std::setfill`, `std::left`,
  `std::right`, `std::fixed`, `std::hex`, `std::showbase`, `std::boolalpha`)
  are "sticky": once applied, they persist until explicitly changed.
- Know that `std::setw` is the one-shot exception: it applies only to the
  very next inserted value and resets to 0 afterward.
- Know that `std::setprecision` controls the number of decimal digits in
  fixed-point mode, or significant digits in default floating-point mode.
- Know that `std::showbase` with `std::hex` adds a `0x` prefix to non-zero
  values, but zero is a special case and prints without the prefix
  regardless.

Concept: reading files with ifstream
- Know that `std::ifstream` reads a file through the same `>>` / `getline`
  stream interface used with `std::cin`.
- Know that `is_open()` must be checked after constructing an `ifstream`,
  because a missing or unreadable file does not throw by default -- it
  silently leaves the stream in a failed state.
- Be able to diagnose and fix the three classic `ifstream` bugs: using
  `eof()` as a loop condition (acts one read too late and double-processes
  the last value), skipping the `is_open()` check, and mixing `>>` with
  `getline` without clearing the leftover newline (fixable with
  `std::ws`, `ignore()`, or by using `getline` consistently).

Concept: binary streams
- Know that opening a file with `std::ios::binary` disables text-mode
  translation, so every byte read is exactly what is stored on disk.
- Be able to use the binary read pattern
  `f.read(reinterpret_cast<char*>(&val), sizeof(val))` to read raw bytes
  directly into a variable or struct.
- Know that `reinterpret_cast<char*>` tells the compiler to treat the bytes
  at an address as a raw byte array, with no data conversion.
- Be able to use `f.seekg(offset)` to move the read position to a computed
  byte offset, and to compute that offset from a header size plus `sizeof`
  of a fixed-size record type.
- Know that x86/x64 integers are stored little-endian (low byte first), so
  reading raw bytes directly into an integer type on the same architecture
  produces the correct value automatically.

Concept: combining streams for log parsing
- Be able to read a file line by line with `std::ifstream` +
  `std::getline`, then tokenize each line by wrapping it in an
  `std::istringstream` and extracting fields with `>>`.
- Be able to produce aligned column output using `std::setw`, `std::left`,
  and `std::right` together.
- Know that file-open failures should be reported to `std::cerr` with a
  non-zero exit code, keeping error output separate from the program's
  normal `std::cout` output.

## Study checklist

- [ ] Predict the output of a snippet mixing `>>` and `getline` on the same
      stream.
- [ ] Explain why `std::setw` needs to be reapplied before every field but
      `std::setfill` does not.
- [ ] Explain why `while (!stream.eof())` is the wrong loop condition.
- [ ] Compute a `seekg` offset from a header size and a record `sizeof`.
- [ ] Explain what `reinterpret_cast<char*>` does when passed to
      `f.read()`.

## Practiced in

`iostream-interceptor`, `sstream-formatter`, `text-stream-surgery`, `binary-stream-explorer`, `log-analyzer`
