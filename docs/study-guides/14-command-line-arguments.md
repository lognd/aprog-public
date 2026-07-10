# Study Guide 14: Command Line Arguments

This module covers exactly how a C++ program receives its command-line
arguments through `argc`/`argv`, how to explore an unfamiliar compiled
binary's CLI interface as a black box, and applies flat-grid manipulation
skills to build a playable Connect Four board.

## Know before you start

- Pointer arrays and array-of-pointers layout (`char*` decay, pointer
  arithmetic) [assumed: row 11 -- Pointers]
- Null-terminated C strings and `'\0'` as a sentinel [assumed: row 12 --
  C-Style Strings & Arrays]
- Reading and writing a flat row-major 2D grid through `const char*`/`char*`
  accessor functions [assumed: row 13 -- Const]

## Taught here

Concept: argc and argv
- Know that every C++ program run from a terminal can declare `int
  main(int argc, char* argv[])` to receive its command-line arguments: the
  operating system splits the command line on whitespace and hands the
  program an array of C strings.
- Know that `argc` ("argument count") is the number of strings, and `argv`
  ("argument vector") is declared `char* argv[]` -- an array of pointers to
  `char`, each pointing at the start of one null-terminated C string.
- Know that `argv[0]` is the program's own invocation path, not the first
  "real" argument, and its exact contents depend on how the program was
  invoked -- it is meaningful only for diagnostics, not logic.
- Know that `argv[argc]` is guaranteed by the standard to be `nullptr`, the
  same way a C string guarantees a trailing `'\0'`; this sentinel lets code
  walk the array with `while (*argv)` instead of tracking an index against
  `argc`.
- Know that "at least one real argument" corresponds to `argc >= 2`, since
  `argv[0]` is always present and counted.
- Be able to convert a string argument to a number with `std::stoi` (throws
  on invalid input, unlike `atoi`, which silently returns 0 for malformed
  input such as `atoi("banana")`).

Concept: reverse-engineering a CLI's interface
- Be able to explore a compiled binary with no source code (a "black box")
  by running it with no arguments, `-h`/`--help`, and other guessed flags,
  and reading its output carefully.
- Know the `usage:` convention: a one-line summary of correct invocation,
  printed when a program is run incorrectly or asked for help.
- Be able to distinguish flags (optional named switches, usually starting
  with `-` or `--`) from positional arguments (values identified by their
  order, not a name).

Concept: flat grid as a game board
- Be able to reuse a flat row-major `char*` grid (with accessor functions
  like `cell_at`, `set_cell`, `row_ptr`) as the backing storage for a real
  game board, not just a toy exercise.
- Be able to implement four-direction run detection (horizontal, vertical,
  diagonal, anti-diagonal) to check for a winning line on a grid.
- Be able to implement a simple layered decision procedure -- win move,
  else block move, else heuristic fallback -- as a deterministic algorithm
  with no randomness.
- Know the distinction between a mutating grid function (`char*` parameter,
  writes through it) and a read-only grid function (`const char*`
  parameter, never writes), and apply it correctly to functions like
  `check_win` (read-only) vs. `drop_piece` (mutating).

## Study checklist

- [ ] Draw the memory layout of `argv` for `./prog foo bar`, including the
      `argc` value and the trailing `nullptr`.
- [ ] Explain why `atoi("banana")` is dangerous and what to use instead.
- [ ] Given an unfamiliar compiled CLI tool, list the exploration steps you
      would take to learn its interface.
- [ ] Explain why `check_win` should take `const char*` while `drop_piece`
      takes `char*`.
- [ ] Describe the win/block/heuristic priority order for a simple
      deterministic game AI.

## Practiced in

`argv-explorer`, `cli-contract`, `connect-four`
