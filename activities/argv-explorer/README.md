# Activity: argv Explorer

Every C++ program that runs from a terminal receives its command-line
arguments through two parameters to `main`: `argc` and `argv`. Almost every
CLI tool you have ever used -- compilers, package managers, git -- relies on
this exact mechanism to know what you typed after the program name. This
activity builds a precise mental model of that mechanism: what `argc` counts,
what `argv` actually points to in memory, and the guarantees the standard
makes about both.

## Background

A C++ program can declare `main` two ways:

```cpp
int main() { ... }
int main(int argc, char* argv[]) { ... }
```

When you run `./prog foo bar` from the shell, the operating system splits
the command line on whitespace and hands your program an array of C strings.
`argc` ("argument count") tells you how many strings there are. `argv`
("argument vector") is the array itself, declared as `char* argv[]` -- an
array of pointers to `char`, where each pointer is the start of one
null-terminated C string.

The picture in memory looks like this:

```
argv:  [0]---> "./prog\0"
       [1]---> "foo\0"
       [2]---> "bar\0"
       [3]---> nullptr
argc = 3
```

Three things are easy to get wrong the first time:

**`argv[0]` is not the first "real" argument -- it is the program's own
invocation path.** The shell sets it before your program even starts
running, and its exact contents depend on how the program was invoked (it
might be `./prog`, `/usr/local/bin/prog`, or something else). Do not assume
`argv[0]` is meaningful for anything except diagnostics like error messages
("usage: prog <file>").

**`argv[argc]` is guaranteed to be `nullptr`.** The standard requires this
sentinel value -- a special marker that signals "the sequence ends here"
without being a real element itself, the same way null-terminated strings
guarantee a `'\0'` at the end. This is why some code loops over `argv` with
`while (*argv)` instead of tracking an index against `argc` -- both are
correct, but the sentinel is what makes the pointer-walking version safe.

**`argv[argc]` is a null pointer, not an empty string.** Every element from
`argv[0]` through `argv[argc-1]` is a valid, readable C string. Dereferencing
`argv[argc]` as if it pointed to a string is undefined behavior -- the C++
standard makes no promise about what happens (it might crash, print
garbage, or happen to look correct by luck) once your code does this. The
array
has `argc + 1` pointer slots even though only `argc` of them point at real
arguments.

Since each `argv[i]` is a `const char*`, not a number, converting a numeric
argument requires an explicit conversion. The classic C function is `atoi`
(from `<cstdlib>`), which is simple but gives no way to detect a malformed
input -- `atoi("banana")` silently returns `0`, the same value you would get
from `atoi("0")`. The more robust choice is `std::stoi` (from `<string>`) or
`strtol`, both of which can report failure. A typical conversion plus
validation pattern looks like:

```cpp
int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "usage: " << argv[0] << " <number>\n";
        return 1;
    }
    int n = std::stoi(argv[1]);  // throws std::invalid_argument on bad input
    ...
}
```

Note the check `argc < 2`: since `argv[0]` is always present, "at least one
real argument" means `argc >= 2`.

## Concepts covered

- The `argc` count and `argv` array layout in memory
- The null sentinel at `argv[argc]` guaranteed by the C standard
- Converting string arguments to integers with `atoi` / `strtol` / `std::stoi`
- Input validation patterns for command-line programs

## How it works

Seven questions walk through `argc`/`argv` layout, `argv[0]`, the sentinel,
the type of `argv`, argument conversion, and validating `argc` before
indexing. Each question gives you a short hint if you answer incorrectly.
The activity unlocks once every answer is exactly correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All seven questions are answered correctly and the program prints the
passphrase.

## Hints

<details>
<summary>Hint 1 -- counting argc</summary>

`argc` counts every string the shell hands you, and `argv[0]` -- the program
path -- is one of them. `./prog foo bar` has three strings total: the
program path, `foo`, and `bar`.

</details>

<details>
<summary>Hint 2 -- the type of argv</summary>

`argv` is declared `char* argv[]`, which is an array of `char*`. Each
element is a pointer to the first character of a null-terminated C string.
Do not confuse this with a single string -- it is an array of pointers to
strings.

</details>

<details>
<summary>Hint 3 -- what argv[argc] guarantees</summary>

The array always has one more slot than `argc`, and that final slot holds
`nullptr`. This is analogous to how a C string always has a `'\0'` after
its last real character -- it lets code walk the array without needing to
know its length in advance.

</details>

## Going further

- What happens if you access `argv[argc]`? The standard guarantees it is
  `nullptr` -- write a small program to verify that and look at the assembly.
- Write a simple option parser that handles `--key=value` style arguments
  without using any standard library parsing utilities.
- What does `strtol` return when the input is not a valid number? Read the
  man page and write a version of the converter that detects and reports
  errors, unlike `atoi`.
