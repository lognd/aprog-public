# Log Analyzer

Real systems produce log files.  Reading them reliably means knowing which
stream abstraction to reach for at each step: `std::ifstream` to open the
file, `std::istringstream` to tokenize each line, and `std::cout` with
`<iomanip>` manipulators to produce aligned output.  This assignment
combines all three into one tool.

You will write `log-analyzer`, a command-line program that reads a structured
log file, counts how many times each log level appears, tracks the most
recent message for each level, and prints a formatted summary table.

---

## Learning goals

- Open and read a text file line-by-line using `std::ifstream` and
  `std::getline`.
- Parse each line by wrapping it in an `std::istringstream` and extracting
  fields with `>>`.
- Handle the leftover-whitespace problem that arises when mixing `>>` and
  `std::getline` on the same stream.
- Produce column-aligned output using `std::setw`, `std::left`, and
  `std::right` from `<iomanip>`.
- Report errors through `std::cerr` and use a non-zero exit code when a
  file cannot be opened.

---

## Task

Implement `log-analyzer.cpp`.  The program reads a log file whose path is
given as a command-line argument, then prints a summary table to standard
output.

### Command-line interface

```
./log-analyzer <logfile>
```

If the file cannot be opened, print to `stderr`:

```
error: cannot open <logfile>
```

and exit with code 1.

### Log file format

Each line of the log file has the form:

```
TIMESTAMP LEVEL MESSAGE
```

- `TIMESTAMP` -- a single token with no whitespace (e.g.,
  `2024-01-15T10:00:00`).
- `LEVEL` -- a single token with no whitespace (e.g., `INFO`, `ERROR`,
  `WARNING`, `DEBUG`).
- `MESSAGE` -- the rest of the line after the level token.  May contain
  spaces.  Strip any leading whitespace from the message before storing it.

A line is **malformed** if it contains fewer than two whitespace-separated
tokens (no level field).  Malformed lines are skipped and counted.

### Output format

Print a header followed by one row per level, sorted alphabetically by level
name.  Use these column widths:

- Level column: `std::left << std::setw(8)` (left-aligned, minimum 8 chars).
- Count column: `std::right << std::setw(5)` (right-aligned, minimum 5 chars).
- Two spaces between each column and before the message.

```
LEVEL     COUNT  MOST RECENT
DEBUG         2  loop iteration
ERROR         3  connection refused
INFO          3  request handled
WARNING       2  retrying connection
```

"MOST RECENT" is the message from the **last** log line with that level.

If any malformed lines were skipped, print after the table:

```
N malformed line(s) skipped
```

where N is the count.

If the file is empty (or contains only malformed lines), print the header and
then the malformed count if nonzero.

### Parsing with istringstream

The recommended approach for each line:

```cpp
std::istringstream iss(line);
std::string ts, level, message;
if (!(iss >> ts >> level)) {
    // malformed
    continue;
}
std::getline(iss >> std::ws, message);  // skip leading whitespace first
```

The `>> std::ws` call is critical: after `>> level` the stream position sits
on the space before the message.  Without `>> std::ws`, `getline` captures
that leading space as part of the message.

---

## Files

| File | Purpose |
|------|---------|
| `log-analyzer.cpp` | Your implementation -- the only file you submit. |

---

## Compilation and Testing

```bash
g++ -std=c++17 -Wall -Wextra -o log-analyzer log-analyzer.cpp
bash visible-tests/run_tests.sh
```

The test script compiles nothing; run the compile command first.

---

## Constraints

- You must use `std::ifstream` to open the log file.
- You must use `std::istringstream` to parse each line.
- You must use `std::setw` from `<iomanip>` for column alignment.
- Do not use `std::filesystem`, `<regex>`, or any POSIX file APIs (`open`,
  `read`, `fopen`).
- The program must exit with code 0 on success and code 1 if the file cannot
  be opened.

---

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required) |
| Visible correctness | 20 |
| Hidden correctness | 70 |
| Memory safety (Valgrind, extra credit) | +10 |
| **Total** | **90** |

Valgrind is a tool that runs your compiled program and reports memory errors
(leaks, reads of uninitialized memory, etc.) that would otherwise go
unnoticed since the program can still appear to run correctly.

Hidden tests cover: multiple levels in alphabetical order, most-recent
tracking across many entries, malformed-line counting, empty files, large
entry counts, and messages containing spaces.

---

## Submission

Submit `log-analyzer.cpp`.  The grader compiles it with
`g++ -std=c++17 -Wall -o log-analyzer log-analyzer.cpp`.

---

## Going further

- Add a `--level` flag that filters output to a single level.
- Support reading from `stdin` when the argument is `-`.
- Count the number of distinct timestamps and report the time range
  (earliest and latest).
- Add a `--tail N` flag that shows only the last N messages per level.
