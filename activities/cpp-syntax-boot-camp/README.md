# Activity: C++ Syntax Boot Camp

You just installed a C++ compiler and learned how to run it from the
command line. Before that compiler is useful for anything else, you need to
be able to read the tiny building blocks of a C++ program: what a program
actually is, what a statement is, how a variable stores a value, how a loop
repeats something, and how a function packages up reusable code. This
activity is the very first C++ you will read in this course. It assumes
nothing.

A **program** is a list of instructions, written in a file, that the
computer carries out one after another. A **statement** is one complete
instruction -- one step in that list -- and in C++ every statement ends
with a semicolon (`;`), the same way a sentence ends with a period. A
**variable** is a named, labeled storage location that holds one value at a
time (a box with a name on it); a **function** is a named, reusable block
of statements that can take input and hand back a result.

In this activity you will read twelve tiny, complete C++ programs, one at a
time. For each one, you predict exactly what it will print, before you run
it. This "predict, then verify" loop -- guessing first, then checking your
guess against reality -- is the single most useful habit you can build
while learning to program: it forces you to actually understand the code
instead of skimming past it.

---

## Concepts covered

- What a statement, variable, and function are, from zero
- Declaring and printing a variable with `std::cout`
- Assignment (`=`) changing a variable's stored value
- Integer arithmetic, including honest integer division (`7 / 2` is `3`,
  not `3.5`)
- `if`/`else` branching
- `for` loops and the three-part header (initializer; condition; update)
- `while` loops
- Functions that take parameters and `return` a value
- `std::string` declaration and concatenation with `+`
- `bool` and its default printed form (`1`/`0`, not `true`/`false`)
- Comments (`//`) and why commented-out code never runs

---

## How it works

This is a snippet-prediction activity. The launcher compiles and runs
twelve short C++ programs using the compiler on your machine (`g++` or
`clang++` -- whichever it finds first). For each program, it shows you the
full source code and asks you to type exactly what the program prints to
the screen.

Type the output character-for-character. If a program prints `16`, type
`16` -- not `sixteen`, not `"16"`. If a program's output has more than one
line, the launcher tells you how many lines to expect and asks for each
line separately.

If you type the wrong answer, you get an explanation of exactly why that
answer is wrong and what you may have misread. If you type the right
answer, you get a deeper explanation of the rule the snippet was
demonstrating. You must get every snippet correct before the passphrase is
revealed -- there is no penalty for guessing wrong, so use the feedback and
try again.

You are strongly encouraged to also compile and run every snippet yourself
before -- or after -- predicting it. Copy the code shown into a file, and
from your terminal:

```bash
g++ file.cpp -o prog
./prog
```

`g++ file.cpp -o prog` compiles `file.cpp` (translates your C++ source into
a program the computer can actually run) and names the resulting program
`prog` (the `-o` flag means "output file name"). `./prog` then runs it --
the `./` tells your shell "run the program named `prog` sitting right here
in the current directory," since your shell will not run a program by name
alone unless it lives on your configured search path. Predicting the
output in your head and then watching the real compiler confirm (or
correct) you is exactly how this skill is built.

---

## Getting started

```bash
python3 launch.py
```

For each of the twelve snippets: read the code, decide what you think it
prints, and type your prediction. Feel free to also copy the snippet into
its own `.cpp` file and compile/run it yourself alongside the launcher --
seeing the same answer come from two different places (your prediction and
the real compiler) is how the ideas stick.

---

## You will know you are done when...

You have correctly predicted the output of all twelve snippets and the
launcher reveals the passphrase.

---

## Hints

<details>
<summary>Hint 1 -- reading a for loop header</summary>

A `for` loop's parentheses hold three parts, separated by semicolons:

```cpp
for (int i = 0; i < 3; i++) { ... }
```

- `int i = 0` -- runs once, before the loop starts. It creates the loop
  variable.
- `i < 3` -- checked before every pass through the loop body. As long as
  it is true, the loop keeps going.
- `i++` -- runs after every pass through the body. It means "add 1 to
  `i`," shorthand for `i = i + 1`.

So the loop body runs once for `i = 0`, once for `i = 1`, once for
`i = 2` -- then `i` becomes `3`, the condition `3 < 3` is false, and the
loop stops before running again.

</details>

<details>
<summary>Hint 2 -- integer division does not round</summary>

When both sides of `/` are `int`, C++ throws away the fractional part
entirely -- it does not round to the nearest whole number. `7 / 2` is
`3`, not `4` and not `3.5`. If you want a fractional result, at least one
side of the division needs to be a floating-point type like `double`.

</details>

<details>
<summary>Hint 3 -- bool prints as 1 or 0, not true/false</summary>

By default, `std::cout << someBoolValue` prints the digit `1` for `true`
or `0` for `false` -- not the words. C++ has a way to make it print the
words instead (`std::boolalpha`), but none of these snippets use it.

</details>

---

## Going further

- Take snippet 6 (the `for` loop) and change the condition from `i < 3` to
  `i <= 3`. Predict the new output, then compile and check yourself.
- Rewrite snippet 7 (the `while` loop) as a `for` loop that produces the
  exact same output. What has to move into the header?
- Change snippet 4's variables from `int` to `double` and see how the
  output changes. Why does `7.0 / 2.0` behave differently from `7 / 2`?
- Write your own tiny program, from scratch, that declares two `int`
  variables, adds them, and prints the result with `std::cout`. Compile it
  yourself with `g++ file.cpp -o prog && ./prog`.
