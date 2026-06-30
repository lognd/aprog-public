# Activity: Enum Field Day

Every program eventually needs to represent a small, fixed set of choices: days
of the week, HTTP status codes, directions on a compass, states in a workflow.
The naive approach is to use magic numbers -- `if (status == 2)` or `if (dir ==
3)` -- but this makes code unreadable and error-prone. A typo like `== 22`
compiles silently and does the wrong thing. A smarter approach is to use named
string constants, but comparing strings is slow and still lets you write
`if (dir == "Norht")` without a compiler warning.

C and C++ solve this with enumerations. An `enum` gives names to a group of
related integer constants. The compiler assigns the integers for you, or you
can assign them explicitly. Either way, you write readable names in your code
and the compiler checks that you are using them correctly. C++11 went further
and introduced `enum class` (called a "scoped enum"), which adds an extra layer
of safety by preventing the named values from accidentally mixing with plain
integers or with values from other enums.

In this activity you will predict the output of ten short programs, each
illuminating one concrete rule about how enums work in C and C++. Some of the
outputs will surprise you -- that is the point. Read each snippet carefully
before typing your answer.

---

## Concepts covered

- Unscoped `enum`: default integer numbering (0, 1, 2...) and explicit values
- Implicit conversion of unscoped enum values to `int` (and why this can be dangerous)
- `enum class` (scoped enum): no implicit conversion, must use `static_cast<int>`
- `sizeof` applied to both `enum` and `enum class` -- and why the sizes are the same
- The C idiom `typedef enum { ... } Name;` and why C++ does not require it
- `switch` on `enum class` with exhaustive case labels and qualified names
- Using `static_cast<int>` to extract underlying values from `enum class`

---

## How it works

This is a snippet-prediction activity. The launcher compiles and runs ten short
C++ programs using the compiler on your machine. For each program, it shows you
the source code and asks you to type exactly what it prints to stdout.

You must type the output character-for-character. If the program prints `404`,
type `404` -- not `"404"`, not `four hundred four`. If a snippet has multiple
lines of output, the launcher will ask you to enter each line separately.

When you type the wrong answer, you get a targeted explanation of why that
answer is wrong and what rule you may have misapplied. When you type the
correct answer, you get a deeper explanation of the underlying principle. You
must answer every snippet correctly before the passphrase is revealed. There is
no penalty for wrong guesses -- keep trying until you get it.

The programs cover: the default numbering of enum enumerators, explicit value
assignments with gaps, the size of enum types in memory, implicit vs explicit
integer conversion, the C typedef pattern, and exhaustive switch statements.
Each program teaches one rule and implies a broader principle about how the
compiler treats named integer constants.

---

## Getting started

```bash
python3 launch.py
```

The launcher compiles all ten snippets before asking any questions. If your
machine does not have `g++` or `clang++` installed, the launcher will tell you
and exit. Make sure your compiler is set up (see the Environment Setup
activities) before running this one.

---

## You will know you are done when...

The launcher prints a passphrase after you correctly predict the output of all
ten snippets. Record the passphrase and submit it to your instructor.

---

## Hints

<details>
<summary>Hint 1 -- unscoped enum vs enum class and cout</summary>

An unscoped `enum` (declared as just `enum Color { ... }`) has one convenient
property: its values convert to `int` automatically. This means you can pass an
unscoped enum value directly to `std::cout` and it prints the underlying integer.

An `enum class` (declared as `enum class Color { ... }`) deliberately removes
that automatic conversion. If you try `std::cout << Direction::EAST`, the
compiler will refuse because it does not know whether you wanted to print an
integer, a string, or something else. You must write `static_cast<int>(
Direction::EAST)` to extract the integer first.

This distinction is the most important thing to understand before working
through the snippets.

</details>

<details>
<summary>Hint 2 -- typedef enum in C and C++</summary>

In C, writing `enum Color { RED, GREEN, BLUE };` creates a type called `enum
Color` -- you must write both the keyword and the name every time you use it:
`enum Color c = RED;`. This is verbose. The C workaround is:

```c
typedef enum { RED, GREEN, BLUE } Color;
```

This creates an anonymous enum and immediately aliases it to `Color`, so you
can write just `Color c = RED;`. In C++ this is unnecessary because `enum Color
{ ... };` already creates a type called `Color` (without the `enum` keyword).
However, the `typedef enum` syntax is still valid C++ and you will see it in
code that is shared between C and C++ translation units.

</details>

<details>
<summary>Hint 3 -- sizeof and the underlying type</summary>

Every enum has an "underlying type" -- the actual integer type that stores its
values. For a plain `enum` or `enum class` with no explicit underlying type
annotation, the compiler defaults to `int` (4 bytes on all common platforms).
This means `sizeof(MyEnum)` returns 4 regardless of how many enumerators you
have or what values they hold.

You can change the underlying type:

```cpp
enum class Byte : uint8_t { A = 1, B = 2 };  // sizeof == 1
enum class Big : uint64_t { X = 0 };          // sizeof == 8
```

In the snippets you will see both `enum` and `enum class` -- their `sizeof`
values are the same because both default to `int`.

</details>

---

## Going further

- Change an unscoped enum in one of the snippets to `enum class` and try to
  compile it. Read every compiler error carefully -- each one tells you exactly
  where implicit conversion was happening silently before.
- Add `: uint8_t` to an enum declaration and check `sizeof` again. What is the
  smallest underlying type that can hold the values 0, 200, 404, 500? Is it
  `uint8_t`?
- Write a function that takes a `Direction` (enum class) and returns a `const
  char*` description. Use a switch statement. What warning does the compiler
  emit if you omit one of the cases?
- Look up the C++ standard's rules for when an enum's underlying type is
  automatically promoted to something larger than int. Can an enum's underlying
  type ever be `unsigned int` without you explicitly writing it?
