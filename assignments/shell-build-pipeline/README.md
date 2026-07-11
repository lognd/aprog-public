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

Fill in `build.sh`. The script must do **four** things:

**1. Run the four stages as separate `g++` invocations** -- preprocess
(`-E`), compile to assembly (`-S`), assemble (`-c`), then link.

- **Example (preprocess):** `g++ -E greet.cpp -o greet.i` expands a
  **5-line source into a 22,733-line** `.i` file.
- **Example (compile):** `g++ -S greet.i -o greet.s` produces **490 lines
  of assembly**, containing the mangled symbol
  `_Z5greetRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE`.
- **Tricky case (missing input):** `g++ -c greet.s -o greet.o` only works
  if `greet.s` exists. Run it on a missing file --
  `g++ -c doesnotexist.s -o x.o` -- and the assembler prints `Error: can't
  open doesnotexist.s for reading: No such file or directory` and **exits
  nonzero**. Your script must not treat that as success.

**2. Skip a stage when its output is already up to date** -- run a stage
only if its input is newer than its output (or the output does not exist
yet).

- **Example (first run):** no `.i`/`.s`/`.o` files exist yet, so every
  stage's `[ ! -f "${src}.i" ]` check is true and **every stage runs**.
- **Example (unchanged rerun):** run the script again with nothing changed
  -- every `-nt` (newer-than) check is now false, so **`g++` is never
  invoked** and `greet.o`'s timestamp is unchanged (`stat -c %Y greet.o` is
  identical before and after).
- **Tricky case (one file changed):** `touch greet.cpp` and rerun. Only
  `greet.i`, `greet.s`, `greet.o`, and the relinked `program` get newer
  timestamps; **`main.o` and `math_utils.o` are untouched**, because their
  own `.cpp` inputs did not change.

**3. Send compiler error output to `build.log`** using `2>` or `2>>`.

- **Example (clean build):** `build.log` contains just `22` (the pipe count
  from requirement 4), with **zero compiler errors** after it.
- **Error case (syntax error):** give `greet.cpp` a missing closing `}` and
  `build.log` gains real diagnostics -- `greet.cpp:4:35: error: expected
  '}' at end of input`, then `Assembler messages: Error: can't open greet.s
  for reading` and `/usr/bin/ld: cannot find greet.o: No such file or
  directory`. The later stages still ran but had nothing to consume, so
  each **failed loudly into `build.log`**, and `program` is correctly never
  produced.
- **Empty-input case:** preprocessing a completely empty `.cpp` still
  succeeds and produces a small **non-empty** `.i` (6 lines of `#` line
  markers, no error) -- an empty file is not a missing one.

**4. Use at least one pipe** -- for example, count how many lines the
preprocessor produces before saving the result.

- **Example (raw source count):** `cat main.cpp greet.cpp math_utils.cpp |
  wc -l` prints **`22`** (13 + 5 + 4 lines), which the reference script
  appends to `build.log` at the start of the run.
- **Example (expanded count):** `g++ -E main.cpp | wc -l` prints
  **`22733`+** -- far larger than the raw count, which is the whole point:
  it makes "preprocessing expands the file a lot" visible as one number.

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

## Examples at a glance

To make the four stages concrete, here is **one** small file, `greet.cpp` (5
lines, shown below), and exactly what each stage produces for it when you run
the reference build. Read this table first -- it is the whole pipeline in
miniature, and every number below was produced by actually running the
commands, not guessed.

```cpp
#include "greet.h"

std::string greet(const std::string& name) {
    return "Hello, " + name + "!";
}
```

| Command | Output file | Size / shape | Why |
|---------|-------------|--------------|-----|
| `g++ -E greet.cpp -o greet.i` | `greet.i` | 22,733 lines (versus 5 lines of source) | preprocessing pulls in the ENTIRE contents of every header `greet.cpp` transitively `#include`s (here, `<string>` drags in a huge chunk of the C++ standard library headers), so the expanded file balloons even though your own code barely changed |
| `g++ -S greet.i -o greet.s` | `greet.s` | 490 lines of text, containing the mangled symbol `_Z5greetRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE` | compiling boils the huge preprocessed file down to just the assembly instructions actually needed for the functions greet.cpp defines -- the mangled name is how C++ encodes `greet`'s parameter types into a unique linker symbol |
| `g++ -c greet.s -o greet.o` | `greet.o` | an ELF relocatable object file (binary, not human-readable) | assembling turns the text instructions into raw machine bytes, but the file is not runnable yet -- it still has unresolved references to things like `std::string`'s constructor that live in OTHER object files |
| `g++ main.o greet.o math_utils.o -o program` | `program` | an ELF executable | linking is what actually resolves those cross-file references and produces something the OS can run directly |
| `cat main.cpp greet.cpp math_utils.cpp \| wc -l` | (piped to `wc -l`, then appended to `build.log`) | `22` | this is the "at least one pipe" requirement -- `main.cpp` is 13 lines, `greet.cpp` is 5, `math_utils.cpp` is 4, and `13 + 5 + 4 = 22` |

## Worked example: `greet.cpp` through all four stages, step by step

This is the single most important thing to understand in the assignment, so
here is every step spelled out for one translation unit, `greet.cpp`. (A
translation unit is one `.cpp` file plus everything it `#include`s -- see the
Task section below.)

| Step | Command | Consumes | Produces | Reason |
|------|---------|----------|----------|--------|
| 1. Preprocess | `g++ -E greet.cpp -o greet.i` | `greet.cpp` (5 lines) and everything `greet.h` and `<string>` pull in | `greet.i` (22,733 lines of plain C++ text -- `#include` lines are gone, replaced by the literal contents of the included files) | the preprocessor's whole job is textual substitution: expand `#include`, expand macros, strip comments -- nothing here understands C++ semantics yet |
| 2. Compile | `g++ -S greet.i -o greet.s` | `greet.i` | `greet.s` (490 lines of human-readable assembly, containing the function `_Z5greetRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE`) | `cc1plus` parses the expanded C++, understands types and control flow, and emits the exact CPU instructions that implement `greet` -- this is where "C++ becomes assembly" happens |
| 3. Assemble | `g++ -c greet.s -o greet.o` | `greet.s` | `greet.o` (a 9,272-byte ELF relocatable object file -- confirmed with `file greet.o`) | the assembler translates human-readable instruction mnemonics into the raw machine-code bytes the CPU actually executes, but leaves placeholders ("relocations") for anything defined in another file, like `std::string`'s internals |
| 4. Link | `g++ main.o greet.o math_utils.o -o program` | `main.o`, `greet.o`, `math_utils.o` | `program` (a 22,816-byte executable) | the linker is the only stage that looks at ALL three object files together -- it resolves every placeholder left by step 3 (for example, `main.o`'s call into `greet.o`'s `greet` function) and produces one runnable binary |
| Run | `./program` | `program` | prints:<br>`Hello, world!`<br>`answer: 42`<br>`passphrase: STAGES_COMPLETE` | this exact three-line output, verified by actually running the built binary, is what every stage above was building toward |

Notice how the file only gets SMALLER after preprocessing: 22,733 lines of
expanded text shrink to 490 lines of assembly, because compiling throws away
everything that was only needed to understand types (declarations, template
definitions never instantiated, etc.) and keeps only the instructions this
one file's functions actually need.

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
