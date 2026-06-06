# Scope Safari

Every name in C++ has a *scope* -- the region of the program where it exists.
Scope is governed by curly braces `{ }`.  A variable lives from the line where
it is declared to the closing `}` of the block that contains it.  This rule has
some consequences that are easy to miss the first time you see them.

This activity walks you through five of those consequences, then asks you to
fix a program that breaks three of them at once.

## Getting started

    python3 launch.py

A shell opens inside a fresh copy of the project.

## Walk-through

### Step 1 -- run the exploration program

    make explore && ./explore

Read every section before moving on.  The exploration program demonstrates:

1. **Blank scope** -- a bare `{ }` block creates a new scope; any variable
   declared inside it is destroyed when the block ends.
2. **For-loop variable scope** -- the variable in `for (int i = ...)` belongs
   to the loop body and does not exist after the closing `}`.
3. **Shadowing** -- declaring a variable with the same name as an outer one
   creates a *separate* variable that hides the outer one inside that scope.
   The outer variable is unchanged.
4. **Switch-case scope** -- all `case` labels in a `switch` share one scope.
   Declaring a variable with an initializer in one case makes it technically
   visible in every other case, even ones that jump over the declaration.
   Compilers reject this.
5. **do-while** -- the body of a `do { } while (cond)` always runs at least
   once because the condition is checked *after* the body, not before.

### Step 2 -- try to compile main.cpp

    make

It will not compile.  `main.cpp` has three scope bugs.  Read the error
messages carefully -- the compiler will point you to each one.

### Step 3 -- fix all three bugs

Open `main.cpp` in an editor and fix each bug:

- **Bug 1** produces a compiler warning about shadowing and causes the wrong
  answer.
- **Bug 2** produces a "not declared in this scope" error.
- **Bug 3** produces a "jump to case label crosses initialization" error.

After each fix, try `make` again.  Once it compiles:

    make run

### Step 4 -- exit

    exit

The launcher will check your output automatically and reveal the passphrase.

## You'll know you're done when...

`make run` prints three lines and all three values are correct.

## Hints

<details>
<summary>Bug 1 hint -- shadowing</summary>

Look for a variable declared with `int` inside a loop body when a variable
with the same name already exists in the outer scope.  The inner declaration
creates a new variable that is discarded at the end of each iteration; the
outer one is never modified.  Remove the `int` keyword from the inner
declaration (or restructure the code so only one variable exists).

</details>

<details>
<summary>Bug 2 hint -- out-of-scope variable</summary>

The loop variable `i` is declared inside the `for (...)` header, so it only
exists inside the loop.  If you need the final value of `i` after the loop
ends, declare `int i = 0;` *before* the `for` and remove `int` from the
header.

</details>

<details>
<summary>Bug 3 hint -- switch-case scope</summary>

When execution enters a `switch` at `case 7:` or `default:`, it jumps over
the `int bonus = 10;` line in `case 8:`.  The compiler forbids this because
`bonus` would be in scope but never initialized.  One clean fix: declare
`int bonus = 0;` before the `switch`, then assign inside each case without
the `int` keyword.

</details>
