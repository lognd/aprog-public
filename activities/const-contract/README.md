# Activity: Const Contracts

The C++ compiler treats `const` as a binding promise. When a function declares
`const char* text`, it tells every caller: "I will not modify what this pointer
points to." When that promise is broken -- or when the wrong kind of `const` is
placed in the wrong position -- the compiler refuses to compile the code and
tells you exactly why.

This activity gives you five programs that each violate a different const rule.
Your job is to read the compiler's error message, understand which promise was
broken, and fix it. The bugs are not subtle -- each one illustrates a distinct
const pattern that appears constantly in real C++ code.

## Concepts covered

- The difference between `const char*` (pointer to const data) and `char* const` (const pointer)
- How `const` on a parameter is a promise to the caller about what the function will not do
- Why const-ness must be preserved through a function's return type
- How a const fix in one function can require a follow-up fix in its callers
- Reading compiler errors caused by const violations and tracing them to their root cause

## How it works

A shell opens inside a directory containing five broken `.cpp` files. Each file
has a comment at the top naming the bug and describing the fix. You edit the
files, recompile, and verify the output one at a time. When all five programs
compile and produce the correct output, the launcher detects this and reveals
the passphrase.

The launcher also checks that you did not use `const_cast` (an operator that
forcibly strips `const` from a pointer or reference so you can write through it
anyway) anywhere. That would technically silence the compiler, but it defeats
the purpose -- the point is to fix the type, not to cast the promise away.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- read the error in label.cpp

```bash
g++ -std=c++17 label.cpp
```

The compiler will refuse. Read the error. The function takes `char*` but the
caller passes `const char*`. Fix the parameter type so the function makes the
right promise.

```bash
g++ -std=c++17 label.cpp && ./label
```

### Step 2 -- fix censor.cpp

```bash
g++ -std=c++17 censor.cpp
```

This function accepts `const char*` correctly -- but then tries to write through
it. Fix the body so it copies the string into a local buffer before modifying it.

```bash
g++ -std=c++17 censor.cpp && ./censor
```

### Step 3 -- fix scan.cpp

```bash
g++ -std=c++17 scan.cpp
```

The parameter is declared `char* const`. That makes the pointer itself const --
it cannot be incremented. But the body tries to advance it. The fix is to remove
the `const` that is in the wrong place.

```bash
g++ -std=c++17 scan.cpp && ./scan
```

### Step 4 -- fix locate.cpp

```bash
g++ -std=c++17 locate.cpp
```

The function receives `const char*` and returns a pointer into that same string.
The return type says `char*`, which would strip the const from the input. Fix the
return type so it preserves the promise.

```bash
g++ -std=c++17 locate.cpp && ./locate
```

### Step 5 -- fix report.cpp

```bash
g++ -std=c++17 report.cpp
```

Two bugs in one file. Fix `tag_of` first -- its parameter type is wrong. Once you
fix it, a second line in the same file will fail. Follow the error and fix that
one too.

```bash
g++ -std=c++17 report.cpp && ./report
```

### Step 6 -- exit

```bash
exit
```

The launcher compiles and runs all five programs to verify your fixes are correct.

## You will know you are done when...

The launcher prints a passphrase after verifying that all five programs compile,
produce the expected output, and contain no `const_cast`.

## Hints

<details>
<summary>Hint 1 -- censor.cpp: how to copy into a local buffer</summary>

`strlen` gives you the length. Declare a local array large enough to hold the
string plus the null terminator: `char buf[64]`. Use `strcpy(buf, s)` to copy
the contents in. Then modify `buf`, not `s`.

</details>

<details>
<summary>Hint 2 -- report.cpp: the second error appears after fixing the first</summary>

After you change `tag_of` to take `const char*`, the line `char* copy = name`
in `describe` will fail because `name` is `const char*` and `char*` cannot alias
it. Change `copy` to `const char*` -- or remove it entirely and call
`tag_of(name)` directly.

</details>

## Going further

- Try introducing `const_cast` in one of the files to silence the error. Does
  the program still run? What does this tell you about what `const_cast` actually
  does at runtime versus what it tells the compiler?
- Look up the C++ standard's definition of undefined behavior for modifying a
  string literal. Which of these five files, in its broken state, would invoke
  undefined behavior if the compiler somehow allowed it to run?
- Add a sixth function that demonstrates `const int&` as a parameter -- a case
  where const on a reference is the right choice. When does `const T&` make more
  sense than passing `T` by value?
