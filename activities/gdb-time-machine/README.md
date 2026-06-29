# Activity: GDB Time Machine

Every crash leaves evidence.  When a program segfaults, gdb lets you freeze
time at the moment of impact and inspect the exact state that caused it.  In
this activity you will debug two programs that demonstrate two of the most
common bugs in C and C++: a null pointer dereference and a missing null
terminator.  Neither bug is obvious from reading the code; you have to step
through execution and examine memory to understand what went wrong.

## Concepts covered

- Using `run`, `bt`, `frame`, `print`, and `x/Ncb` in gdb
- Identifying the crash site from a backtrace
- Reading a null pointer value in gdb (`0x0`)
- How `strncpy` behaves when the source exactly fills the destination buffer
- Why a missing null terminator causes out-of-bounds reads

## How it works

The launcher drops you into a shell with two buggy C++ source files and a
Makefile.  You build the programs with `make`, then use gdb to investigate
each one.  After you exit the shell, the launcher asks four questions about
what you observed.  Answer them all correctly to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

### Step 1 -- build both programs

```
make
```

### Step 2 -- debug null_crash

```
gdb ./null_crash
(gdb) run
(gdb) bt
(gdb) frame 0
(gdb) print cfg
(gdb) quit
```

Note: the function name in frame 0 and the value printed for `cfg`.

### Step 3 -- run entry_bug and observe its output

```
./entry_bug
```

The name printed between the brackets may surprise you.

### Step 4 -- debug entry_bug with gdb

```
gdb ./entry_bug
(gdb) break set_name
(gdb) run
(gdb) next
(gdb) x/5cb e->name
(gdb) quit
```

Look at byte index 4 (the fifth byte shown by `x/5cb`).

### Step 5 -- exit and answer the questions

```
exit
```

## You will know you are done when the launcher prints a passphrase.

## Hints

<details>
<summary>Hint 1 -- reading a backtrace</summary>

`bt` prints a stack trace from innermost (frame 0) to outermost.  Frame 0 is
where execution stopped.  The function name in parentheses next to `in` is the
answer.

</details>

<details>
<summary>Hint 2 -- what x/5cb means</summary>

`x` = examine memory.  `5` = show 5 units.  `c` = format as characters.
`b` = one byte per unit.  So `x/5cb e->name` shows 5 consecutive bytes
starting at `e->name`, each formatted as a character and its decimal value.

</details>

<details>
<summary>Hint 3 -- strncpy and null terminators</summary>

`strncpy(dst, src, n)` copies at most n bytes from src to dst.  If
`strlen(src) == n`, it fills the entire destination with characters and writes
no null terminator.  The null that `printf("%s")` depends on must come from
somewhere -- in entry_bug, it leaks in from the next field in the struct.

</details>

## Going further

- Read `man strncpy` and note the warning about null termination.
- Add a `char sentinel` between `name` and `id` in the Entry struct and
  re-run entry_bug.  Does the output change?  Why?
- Fix both bugs.  For null_crash: initialize `cfg` to a real Config.  For
  entry_bug: change the strncpy call so a null is always written.
- Learn about `AddressSanitizer`: compile with `-fsanitize=address` and run
  entry_bug.  Does it flag the out-of-bounds read?
