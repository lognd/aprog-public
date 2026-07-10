# Activity: Const Refactoring Sprint

Adding `const` to a working codebase feels like it should be easy -- just
sprinkle it around until the compiler is happy. In practice, it reveals something
more interesting: const is contagious. Adding it to one function parameter often
forces you to add it to a local variable in the caller, which forces you to add
it to that caller's parameter, which propagates upward through the whole call
chain. This is not a quirk; it is the point. `const` is a contract, and contracts
have to be consistent end to end.

This activity starts you with a working, const-free 2D character grid library.
The code compiles and runs correctly -- but the function signatures make no
promises. A script called `./lint.sh` -- a linter, a program that scans source code for
style or correctness issues without compiling it -- flags every location where
`const` could legally be added. Your job is to add qualifiers one site at a time, recompile
after each, and follow the propagation wherever it leads.

This is also a preview of the grid library you will implement from scratch in the
upcoming Const Qualifier Toolkit assignment. After this sprint, the signatures in
`grid.hpp` will be familiar -- you will have earned them.

## Concepts covered

- Propagating `const` from a callee up through its callers
- `const char*` (pointer to const data) vs. `char*` (mutable data)
- `const char&` as a read-only reference parameter
- `const char*` as a return type when the input is also `const char*`
- Reading a linter report and acting on it methodically

## How it works

A shell opens inside a directory containing `grid.hpp`, `grid.cpp`, and
`grid_demo.cpp`. The header already shows the fully const-correct function
signatures. Your task is to edit `grid.cpp` so that its implementations match
those signatures.

Run `./lint.sh` at any time to see how many `const` keywords are still missing
from `grid.cpp`. Run `make` after each edit to confirm the code still compiles.
When the linter is satisfied and `make` succeeds, type `exit`. The launcher then
rebuilds, runs the demo program, and verifies the output before revealing the
passphrase.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- read the target signatures

```bash
cat grid.hpp
```

These are the signatures your `grid.cpp` must match. Every `const` in the header
is a promise the implementation must keep.

### Step 2 -- run the linter

```bash
./lint.sh
```

The linter counts `const` keywords in `grid.cpp` and reports how many are still
missing. It also catches `const_cast`, which is not allowed.

### Step 3 -- edit grid.cpp

Open `grid.cpp` in your editor and add `const` to one function at a time. Start
with a read-only function like `cell_at` -- its input never needs to change, so
the parameter should be `const char*`.

### Step 4 -- recompile

```bash
make
```

If the compiler complains, read the error. A mismatch between a declaration in
`grid.hpp` and the definition in `grid.cpp` will produce a linker error, not a
type error -- if the function compiles but is not found, check that the signature
matches exactly.

### Step 5 -- repeat until the linter is clean

```bash
./lint.sh
```

Keep editing, compiling, and running the linter until it reports zero findings.

### Step 6 -- exit

```bash
exit
```

The launcher verifies your work and reveals the passphrase if everything checks
out.

## You will know you are done when...

The launcher prints a passphrase after confirming that `grid.cpp` contains at
least 12 `const` keywords, compiles cleanly, and produces the correct output
from the demo program.

## Hints

<details>
<summary>Hint 1 -- the return type of row_ptr matters</summary>

`row_ptr` returns a pointer into the grid. If the grid is `const char*`, the
return type must also be `const char*` -- returning `char*` would let the caller
modify data it was not supposed to touch. `row_ptr_mut` takes a plain `char*`
and returns `char*` for the case where the caller does need to write.

</details>

<details>
<summary>Hint 2 -- const char& for the fill and target parameters</summary>

Several functions take a single character as a "fill value" or "target to search
for." In `grid.hpp` these are declared as `const char& fill` and
`const char& target`. Change the corresponding parameters in `grid.cpp` to match.
The `const` here means the function promises not to modify the character it was
handed; the `&` means it is passed by reference rather than by value.

</details>

<details>
<summary>Hint 3 -- grids_equal and copy_grid take two pointers</summary>

`grids_equal` reads from both grids and modifies neither, so both parameters
should be `const char*`. `copy_grid` reads from `src` and writes to `dst`, so
`src` is `const char*` and `dst` is plain `char*`. These two functions together
make the contrast visible in a single file.

</details>

## Going further

- Count how many lines you changed in `grid.cpp`. How does that compare to the
  number of functions? Some functions required more than one change per line.
- Look at `grid.hpp` after finishing. Could you write it from scratch now without
  looking? Try it on a blank file.
- The Const Qualifier Toolkit assignment uses these exact same signatures. When
  you get to that assignment, notice which functions feel familiar and which ones
  require more thought. The ones that feel unfamiliar are worth reviewing here.
