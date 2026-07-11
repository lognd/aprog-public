# Log Analyzer

Real systems produce log files.  Reading them reliably means knowing which
stream abstraction to reach for at each step: `std::ifstream` to open the
file, `std::istringstream` to tokenize each line (split it into separate
words/fields), and `std::cout` with
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

## Examples at a glance

Before diving into the spec, here is one small log file and exactly what the
finished program does with it. This is the whole assignment in miniature --
read this table first.

Input file (7 lines):

```
2024-03-01T09:00:00 INFO server started
2024-03-01T09:00:01 WARNING disk usage high
2024-03-01T09:00:02 INFO heartbeat ok
OOPS
2024-03-01T09:00:05 ERROR connection refused
2024-03-01T09:00:06 WARNING retrying connection
2024-03-01T09:00:07 ERROR connection refused again
```

| Line | What happens | Why |
|------|--------------|-----|
| `... INFO server started` | Counted under `INFO`; becomes `INFO`'s "most recent" (for now) | Well-formed: has a timestamp token and a level token, and a message follows |
| `... WARNING disk usage high` | Counted under `WARNING`; becomes `WARNING`'s "most recent" (for now) | Same as above, different level |
| `... INFO heartbeat ok` | `INFO`'s count becomes 2; `INFO`'s "most recent" is now overwritten to `"heartbeat ok"` | The **second** `INFO` line replaces the first as the most recent -- "most recent" always means the *last* line seen with that level, not the first |
| `OOPS` | Skipped, and the malformed counter goes up by 1 | This line has only **one** whitespace-separated token (`OOPS`). Reading it as `TIMESTAMP LEVEL` succeeds for the timestamp (`OOPS` itself) but fails for the level, since there is nothing left to read -- exactly the "fewer than two tokens" malformed rule |
| `... ERROR connection refused` | Counted under `ERROR`; becomes `ERROR`'s "most recent" (for now) | Well-formed |
| `... WARNING retrying connection` | `WARNING`'s count becomes 2; `WARNING`'s "most recent" is now `"retrying connection"` | Same overwrite behavior as the second `INFO` line |
| `... ERROR connection refused again` | `ERROR`'s count becomes 2; `ERROR`'s "most recent" is now `"connection refused again"` | Same overwrite behavior again |

Final program output for this exact file:

```
LEVEL     COUNT  MOST RECENT
ERROR         2  connection refused again
INFO          2  heartbeat ok
WARNING       2  retrying connection
1 malformed line(s) skipped
```

Notice three things that are easy to miss on a first read:

- The rows are printed **alphabetically by level name** (`ERROR`, `INFO`,
  `WARNING`), not in the order the levels first appeared in the file (the
  file saw `INFO` first, but `ERROR` prints first).
- All three levels happen to tie at a count of 2 here -- ties are not a
  special case; each level's count is simply printed on its own row.
- The malformed-line summary (`1 malformed line(s) skipped`) only appears
  **after** the table, and only because the count is nonzero.

## Worked example: watch the program process this file line by line

This is the single most important thing to understand in the assignment, so
here is every line traced by hand. The program keeps two running pieces of
state while it reads: a **count** per level (how many lines had that level
so far) and a **most recent message** per level (overwritten every time a
new line with that level is seen), plus a running **malformed** counter.
We process the same 7-line file from above.

| Step | Line read | Tokens `>> ts >> level` | Result | Running state after this line |
|------|-----------|--------------------------|--------|-------------------------------|
| 1 | `... INFO server started` | `ts="..."`, `level="INFO"` -- both succeed | Message is everything after the level, with leading whitespace stripped: `"server started"` | `INFO`: count=1, most recent="server started" |
| 2 | `... WARNING disk usage high` | both succeed | message = `"disk usage high"` | `WARNING`: count=1, most recent="disk usage high" |
| 3 | `... INFO heartbeat ok` | both succeed | message = `"heartbeat ok"` | `INFO`: count=2, most recent="heartbeat ok" (overwrites step 1's message) |
| 4 | `OOPS` | `ts="OOPS"` succeeds, but there is no second token, so `level` fails to read | Malformed -- line is skipped entirely, nothing is counted or stored | malformed=1 |
| 5 | `... ERROR connection refused` | both succeed | message = `"connection refused"` | `ERROR`: count=1, most recent="connection refused" |
| 6 | `... WARNING retrying connection` | both succeed | message = `"retrying connection"` | `WARNING`: count=2, most recent="retrying connection" (overwrites step 2's message) |
| 7 | `... ERROR connection refused again` | both succeed | message = `"connection refused again"` | `ERROR`: count=2, most recent="connection refused again" (overwrites step 5's message) |

After all 7 lines, the state is:

- `ERROR`: count 2, most recent "connection refused again"
- `INFO`: count 2, most recent "heartbeat ok"
- `WARNING`: count 2, most recent "retrying connection"
- malformed: 1

Printing sorts the levels alphabetically (`ERROR`, `INFO`, `WARNING`) and
prints the malformed summary last, producing exactly:

```
LEVEL     COUNT  MOST RECENT
ERROR         2  connection refused again
INFO          2  heartbeat ok
WARNING       2  retrying connection
1 malformed line(s) skipped
```

If you strip the `OOPS` line out entirely and re-run this trace, everything
is identical except malformed stays at 0, and the final
`N malformed line(s) skipped` line does not print at all -- it is only
printed when the count is greater than zero.

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

- **Example (valid file):** `./log-analyzer visible-tests/logs/single.log`
  on an existing, readable file -- prints the summary table and **exits
  `0`**.
- **Error case (missing file):** `./log-analyzer does_not_exist.log` on a
  path that does not exist -- prints `error: cannot open does_not_exist.log`
  to `stderr` and **exits `1`**.
- **Edge case (no argument):** `./log-analyzer` with no argument at all --
  your program should also reject this (there is no `logfile` to read);
  the reference solution prints a usage message to `stderr` and **exits
  `1`**.

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

- **Example (well-formed):** `"2024-01-15T10:00:00 INFO request handled"`
  -- 3+ tokens, well-formed; `TIMESTAMP="2024-01-15T10:00:00"`,
  `LEVEL="INFO"`, **`MESSAGE="request handled"`**.
- **Tricky case (one token):** `"OOPS"` -- only **one** token. Reading
  `TIMESTAMP` succeeds (it consumes `"OOPS"`), but there is nothing left
  for `LEVEL` to read, so this line is **malformed** and is skipped (not
  counted toward any level).
- **Edge case (empty line):** `""` (a completely empty line, e.g. a blank
  line in the file) -- zero tokens. Both `TIMESTAMP` and `LEVEL` fail to
  read. **Malformed.**
- **Tricky case (empty message):** `"2024-01-15T10:00:00 DEBUG"` --
  exactly two tokens and nothing after the level. This is **not**
  malformed (it has a timestamp and a level); the message is simply the
  empty string `""`. Your output row for this line would show `DEBUG`
  with an **empty "most recent" column**.

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

- **Empty-input case:** an empty file (0 lines at all) -- prints only the
  header line `LEVEL     COUNT  MOST RECENT` and **nothing else** (no
  malformed line, since the malformed count is 0).
- **Edge case (all malformed):** a file containing only `"OOPS"` and
  `"ONEWORD"` (two malformed lines, no well-formed lines) -- prints the
  header, no level rows (there is nothing to sort or count), then
  **`2 malformed line(s) skipped`**.
- **Tricky case (three-way tie):** a file where `INFO` appears twice,
  `ERROR` appears twice, and `WARNING` appears twice (a three-way tie at
  count 2) -- all three still print, one row each, sorted alphabetically
  as **`ERROR`, `INFO`, `WARNING`**; a tie in count does not merge or
  reorder rows, it is simply not a special case at all.
- **Example (message with spaces):** a message containing internal
  spaces, e.g. `"connection refused again"` -- printed **verbatim** in the
  "MOST RECENT" column, spaces and all; only *leading* whitespace before
  the message is stripped, never spaces inside it.

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
- Do not use `std::filesystem`, `<regex>`, or any POSIX file APIs -- POSIX
  (Portable Operating System Interface) is the standard that defines the
  low-level, operating-system-provided file functions `open`, `read`, and
  `fopen`; this assignment sticks to the C++ stream classes instead.
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
