# Activity: Text Stream Surgery

Three small C++ programs.  Each one has a single file-stream bug.
`std::ifstream` is the class C++ uses to read a file through the same
stream interface (`>>`, `std::getline`) you already use with `std::cin`.
The bugs are the classic mistakes that appear in nearly every programmer's
first week with `std::ifstream`: using `eof()` (a flag that only turns true
AFTER a read has already failed at the end of the file -- checking it as a
loop condition means acting one read too late) as a loop condition,
forgetting to check `is_open()` (a function that reports whether the file
was actually opened, since a missing file does not throw an error by
default), and mixing `operator>>` with `std::getline` without clearing the
leftover newline.

The programs compile.  They even produce output.  The output is just wrong.
Your job is to read each program, diagnose the mistake, fix it, and confirm
that the fixed program produces the expected output.

## Concepts covered

- `while (stream >> val)` as the correct loop idiom (an idiom is a standard,
  recognized pattern for writing something -- not a language feature, just
  the way experienced programmers write it) vs. `while (!stream.eof())`
- `is_open()` to detect a failed file open before reading
- Why `operator>>` leaves the newline in the buffer and how it breaks `std::getline`
- `std::ifstream` open, read, and close lifecycle
- Connecting file-stream bugs to the stream-state behavior from iostream

## How it works

The launcher drops you into a shell with three source files (`eof_loop.cpp`,
`no_check.cpp`, `mixed_io.cpp`) and two data files (`numbers.txt`,
`profile.txt`).  The banner inside the shell shows the expected and actual
output for each program.  Fix all three programs so their output matches the
expected output, then type `exit`.  The launcher compiles and runs them
automatically to check your work.

## Getting started

```bash
python3 launch.py
```

A shell opens with the broken programs.  Edit the `.cpp` files in place with
any text editor available in the shell (`nano eof_loop.cpp`, `vim
eof_loop.cpp`, or `code .` if you have VS Code set up) -- there is no
separate "submit" step; the launcher checks whatever is on disk when you
`exit`.

### Step 1 -- understand what each program should do

Read all three source files before touching any of them.  The comments and
the banner inside the shell describe what each program is supposed to print.

### Step 2 -- fix eof_loop.cpp

Run the broken version, observe that the sum is wrong, then find the loop
condition that causes the last number to be counted twice.  Fix it so the loop
stops exactly when extraction fails.

```bash
g++ -std=c++17 -o eof_loop eof_loop.cpp && ./eof_loop
```

### Step 3 -- fix no_check.cpp

The file `missing.txt` does not exist in this directory.  The broken program
silently reads nothing.  Add the check that makes the missing-file case
produce a clear error message instead.

```bash
g++ -std=c++17 -o no_check no_check.cpp && ./no_check
```

### Step 4 -- fix mixed_io.cpp

The bio field is always empty even though `profile.txt` has two lines.  Trace
what happens in the stream buffer (the region of memory where characters
wait to be read out of the stream) between the `>>` call and the `getline`
call.

```bash
g++ -std=c++17 -o mixed_io mixed_io.cpp && ./mixed_io
```

### Step 5 -- exit and let the launcher check

```bash
exit
```

The launcher recompiles and runs all three programs and checks the output.

## You will know you are done when...

The launcher prints three PASS lines and reveals the passphrase.

## Hints

<details>
<summary>Hint 1 -- the eof loop bug</summary>

`f.eof()` becomes true AFTER a read that hits the end of file.  When the
loop reads the last integer successfully, `f.eof()` is still false.  The loop
runs one more time, `f >> n` fails (and `n` keeps its previous value), and
that value is added to the sum again.

The fix: use `while (f >> n)` so the loop condition IS the extraction.

</details>

<details>
<summary>Hint 2 -- checking is_open()</summary>

After constructing `std::ifstream f("missing.txt")`, check `f.is_open()`.
If it returns false, the file could not be opened.  Print the error message
to stdout and return 1.

</details>

<details>
<summary>Hint 3 -- the leftover newline</summary>

`f >> name` reads "Alice" and stops.  The `'\n'` after "Alice" stays in the
stream buffer.  The very next `std::getline(f, bio)` reads up to that `'\n'`
and returns an empty string.

Fix: replace `f >> name` with `std::getline(f, name)`.

</details>

## Going further

- What happens to `mixed_io.cpp` if you keep `f >> name` but add
  `f.ignore()` immediately after?  Try it and verify it produces the correct
  output.
- `while (f >> n)` works because `operator>>` returns a reference to the
  stream, and a stream converts to `bool` via `operator bool()`.  Look up
  what conditions make `operator bool()` return false.
- Try deliberately passing the wrong filename to `std::ifstream` in
  `eof_loop.cpp` (without adding an `is_open()` check).  What does the
  program print for the sum?  Why?
- Add a `while (f >> n)` loop to `no_check.cpp` that runs after the
  `is_open()` check succeeds.  What should it print for a file that actually
  exists?
