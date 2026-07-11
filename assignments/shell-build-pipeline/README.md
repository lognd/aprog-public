# Shell Build Pipeline

You will write a shell script that does exactly what `make` does -- but without `make`.
By the time you finish, you will understand the problem Makefiles were invented to solve.

## Learning goals

- Understand the four compilation stages: preprocess, compile, assemble, link
- Use `g++ -E`, `g++ -S`, `g++ -c`, and `g++` (link) as separate invocations
- Write a shell script that implements incremental builds using file timestamp comparisons
- Use pipes (chaining one program's output into another's input with `|`),
  stderr redirection (sending a program's error-message stream to a file
  instead of the screen), and `wc` as real tools in a build script

## Background

`g++` can compile a C++ program in one shot:

```bash
g++ main.cpp greet.cpp math_utils.cpp -o program
```

But under the hood it runs four separate programs, one after another:

| Stage | Tool | Input | Output |
|-------|------|-------|--------|
| Preprocess | `cpp` | `.cpp` | `.i` (expanded source) |
| Compile | `cc1plus` | `.i` | `.s` (assembly -- human-readable text listing the exact CPU instructions the program will run) |
| Assemble | `as` | `.s` | `.o` (object code -- the same instructions translated into raw bytes the CPU can execute, but not yet a runnable program) |
| Link | `ld` | `.o` files | executable |

You can ask `g++` to stop after each stage:

```bash
g++ -E main.cpp -o main.i      # preprocess only
g++ -S main.i  -o main.s      # compile to assembly only
g++ -c main.s  -o main.o      # assemble only
g++    main.o greet.o math_utils.o -o program   # link
```

A naive script runs all stages every time. The smart version only re-runs a stage when
its input has changed -- exactly what `make` does with its dependency graph (a map of
which files depend on which other files, so a tool can tell exactly what needs
rebuilding when one file changes).

To check whether a file is newer than another, use:

```bash
[ newer_file -nt older_file ]
```

---

## Task

Fill in `build.sh`. The script must:

1. Run `g++ -E`, `g++ -S`, `g++ -c`, and `g++` (link) as separate invocations.
2. Only run each stage if the input file is newer than the output file (or the output does not exist yet).
3. Redirect compiler error output to `build.log` using `2>` or `2>>`.
4. Use at least one pipe -- for example, count how many lines the preprocessor produces
   before you save the result to disk.

The project has three translation units (a translation unit is one `.cpp`
file plus everything it `#include`s -- the compiler runs the four stages
above on each one separately, then the link step combines the results):

```
main.cpp       greet.cpp       math_utils.cpp
```

Each one must pass through all four stages independently. The link step combines all three
object files into a single `program` binary.

`main.cpp` uses functions defined in `greet.cpp` and `math_utils.cpp`.
When compiled and run correctly, `./program` produces:

```
Hello, world!
answer: 42
passphrase: STAGES_COMPLETE
```

### Exploring with pipes

Before your script is complete, try these one-liners to see what each stage does:

```bash
# How many lines does preprocessing add?
g++ -E main.cpp | wc -l

# Find the line markers that show where each file was included:
g++ -E main.cpp | grep '^# '

# Does the assembly use a call instruction for greet?
# (a "call" is the assembly-language instruction that jumps into another
# function and remembers where to return to)
g++ -S greet.i -o /dev/stdout 2>/dev/null | grep -c 'call'
```

These patterns -- pipe to `wc`, `grep`, redirect stderr -- belong in your `build.sh` too.

---

## Files

| File | Purpose |
|------|---------|
| `build.sh` | Your build script -- fill this in |
| `greet.h` / `greet.cpp` | Greeting function |
| `math_utils.h` / `math_utils.cpp` | Arithmetic functions |
| `main.cpp` | Entry point |

## Compilation and Testing

Copy all files into one directory and run:

```bash
bash build.sh
./program
```

Or use the provided test script:

```bash
bash visible-tests/test_local.sh
```

## Constraints

- The script must be named `build.sh`.
- Do not use `make`, `cmake`, or any build tool other than `g++` and plain
  shell commands -- the point of this assignment is to replicate what those
  tools do under the hood.
- Each of the four stages (preprocess, compile, assemble, link) must be a
  separate `g++` invocation with the matching flag (`-E`, `-S`, `-c`, or no
  flag for the link step). Do not collapse stages together.

---

## Grading

| Component | Points |
|-----------|--------|
| Build succeeds (required to proceed) | 0 |
| Program produces correct output | 30 |
| Incremental: changed file chain is rebuilt | 40 |
| Redirection used (`build.log` created) | 15 |
| Pipe used in script | 15 |
| **Total** | **100** |

## Submission

Submit a single file named `build.sh`. Do not rename it.

---

## Hints

<details>
<summary>Hint 1 -- structure of the script</summary>

Write three blocks -- one per source file -- each containing all four stage-check/run pairs.
Then add a final link block. The pattern for each stage looks like:

```bash
if [ ! -f main.i ] || [ main.cpp -nt main.i ]; then
    g++ -E main.cpp -o main.i 2>>build.log
fi
```

</details>

<details>
<summary>Hint 2 -- adding a pipe</summary>

The simplest pipe is counting total source lines at the top of the script:

```bash
cat main.cpp greet.cpp math_utils.cpp | wc -l >> build.log
```

This pipes three files through `wc -l` and appends the count to `build.log`.
Any pipe that produces useful output counts.

</details>

<details>
<summary>Hint 3 -- the link step</summary>

The link step depends on ALL three object files. You should re-link if any of the three
`.o` files is newer than `program`:

```bash
if [ ! -f program ] || [ main.o -nt program ] || \
   [ greet.o -nt program ] || [ math_utils.o -nt program ]; then
    g++ main.o greet.o math_utils.o -o program 2>>build.log
fi
```

</details>

<details>
<summary>Hint 4 -- testing incremental behavior</summary>

After a successful build, touch one source file and run the script again:

```bash
touch greet.cpp
bash build.sh
```

Only `greet.i`, `greet.s`, `greet.o`, and `program` should be updated.
`main.o` and `math_utils.o` must not change.
Check with `ls -lt` to see modification times.

</details>

## Going further

- Add a `clean` target to your script: delete all generated `.i`, `.s`, `.o`,
  and `program` files.
- Look up `make -n` (dry run). Implement a `--dry-run` flag in your shell
  script that prints what would be rebuilt without actually running the commands.
- Read about `ninja` and `cmake --build`. How do they solve the same incremental
  build problem as your script, and what do they add?
