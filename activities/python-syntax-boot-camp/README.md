# Activity: Python Syntax Boot Camp

You already know C++. Now you are meeting Python for the first time, and
the fastest way to get comfortable is to see the same handful of ideas --
printing, variables, functions, loops, conditions -- written in both
languages side by side. Nothing here is a "gotcha" or a trick; this
activity is pure syntax, the honest happy path. The surprising ways Python
quietly behaves differently from C++ (mutation, overflow, `is` vs `==`)
are saved for a later activity -- here you are just learning to read the
shape of Python code.

In this activity you will read twelve tiny, complete Python programs, one
at a time. For each one, you predict exactly what it prints, before you
run it. This "predict, then verify" loop is the same skill you built
reading C++ snippets earlier in this course -- it works exactly as well
on a new language.

---

## C++ -> Python, side by side

| Concept | C++ | Python |
|---------|-----|--------|
| Print text | `std::cout << "hi" << "\n";` | `print("hi")` |
| Declare a variable | `int x = 5;` (type fixed forever) | `x = 5` (no type declared; `x` can be rebound to any type later) |
| Define a function | `int square(int x) { return x * x; }` | `def square(x):`<br>`    return x * x` |
| If/else | `if (x > 5) { ... } else { ... }` | `if x > 5:`<br>`    ...`<br>`else:`<br>`    ...` |
| Block delimiter | curly braces `{ }` | a colon `:` plus indentation -- no braces at all |
| Counted loop | `for (int i = 0; i < 3; i++) { ... }` | `for i in range(3):`<br>`    ...` |
| Loop over a collection | `for (const auto& f : fruits) { ... }` | `for fruit in fruits:`<br>`    ...` |
| Condition-controlled loop | `while (n > 0) { ... }` | `while n > 0:`<br>`    ...` |
| Build a string with values inside | `name + " is " + std::to_string(age)` | `f"{name} is {age}"` (an f-string) |
| Length of a string | `word.size()` / `strlen(word)` | `len(word)` |
| Comment | `// this is ignored` | `# this is ignored` |

Two patterns worth calling out explicitly, since they have no direct C++
equivalent:

- **No block scope from indentation alone.** Python marks a block with a
  colon and indentation, but that indentation is purely about grouping
  which statements belong to the `if`/`for`/`while`/`def` -- it plays the
  same structural role as C++'s `{ }`.
- **A dictionary literal**, `{"name": "Ada", "age": 28}`, is a collection
  of key-value pairs with no exact single-token C++ equivalent -- the
  closest cousin is `std::map<std::string, ...>`, but Python's dictionary
  needs no type written out and no `#include`.

---

## Concepts covered

- `print()` as Python's equivalent of `std::cout`
- Variables with no type declaration -- a name can be rebound to any type
- `def` and `return` for defining a function
- `if`/`elif`/`else` -- no parentheses, no braces, colon-plus-indentation
- `for i in range(3)`, Python's counted loop
- `for x in a_list`, iterating directly over a collection's elements
- `while` loops
- f-strings (`f"{name} is {age}"`) for building text with values inside it
- `len()` for the length of a string
- List literals, `.append()`, and printing a list
- Dictionary literals and key-based lookup with `[ ]`
- `#` comments

---

## How it works

This is a snippet-prediction activity, just like the C++ ones you have
already done -- except instead of compiling with `g++`, the launcher runs
each snippet directly with the Python interpreter on your machine
(`sys.executable`, whichever `python3` you are running the launcher with).

For each of the twelve short Python programs, the launcher shows you the
full source code and asks you to type exactly what it prints. Type the
output character-for-character, including punctuation Python adds itself
(brackets around a printed list, for example). If a program's output has
more than one line, the launcher tells you how many lines to expect and
asks for each one separately.

Wrong answers get a targeted explanation of what you may have misread;
correct answers get a deeper explanation of the rule being demonstrated.
You must get all twelve correct before the passphrase is revealed.

---

## Getting started

```bash
python3 launch.py
```

For each snippet, read the code, decide what you think it prints, and
type your prediction. If you want to double-check yourself outside the
launcher, copy any snippet into its own `.py` file and run it directly:

```bash
python3 file.py
```

---

## You will know you are done when...

You have correctly predicted the output of all twelve snippets and the
launcher reveals the passphrase.

---

## Hints

<details>
<summary>Hint 1 -- indentation is not optional</summary>

In C++, `{ }` marks a block, and indentation is just a style convention
for humans -- the compiler does not care how you indent. In Python,
indentation IS the syntax: it is the only thing that marks where a block
(the body of an `if`, `for`, `while`, or `def`) begins and ends. Lines
indented at the same level under a `:` line are all part of that block.

</details>

<details>
<summary>Hint 2 -- range(3) means 0, 1, 2</summary>

`range(3)` produces three values, starting at 0: `0`, `1`, `2`. The
number you pass to `range()` tells it how many values to produce (and is
one past the last value produced), not the last value included -- the
same "starts at 0" convention C++'s `for (int i = 0; i < 3; i++)` uses.

</details>

<details>
<summary>Hint 3 -- printing a whole list shows the brackets</summary>

When you `print()` an entire Python list, Python shows you exactly how it
represents that list internally: square brackets, elements separated by
commas, like `[1, 2, 3, 4]`. This is different from printing individual
elements one at a time inside a loop, which shows just the bare values.

</details>

---

## Going further

- Take snippet 5 (`for i in range(3)`) and change it to `range(1, 4)`.
  Predict the new output, then run it. What do the two arguments to
  `range()` mean?
- Rewrite snippet 7 (the `while` loop) as a `for i in range(...)` loop that
  produces the exact same output.
- Add a third key-value pair to snippet 11's dictionary and print a
  different key's value. What happens if you look up a key that is not
  there?
- Write your own tiny Python program, from scratch, that declares two
  variables, adds them, and prints the result with an f-string. Run it
  yourself with `python3 file.py`.
