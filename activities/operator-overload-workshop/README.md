# Activity: Operator Overload Workshop

Back in the C-string vs std::string activity, you saw something that
probably looked like a small inconsistency: comparing two `std::string`
objects with `==` compared their CONTENTS (are the characters the same?),
while comparing two `const char*` pointers with `==` compared their
ADDRESSES (do they point at the same memory?). The explanation mentioned
in passing that this was because `std::string` overloaded `operator==` --
but that idea, operator overloading, was never actually taught. This
activity teaches it, and the first snippet recreates that exact mystery
with a tiny class you can read top to bottom.

Operator overloading is C++'s way of letting your own classes plug into
the same symbols you already use every day: `+`, `==`, `<<`, `[]`, and
more. Every one of those symbols, when applied to a class type, is
secretly a function call to a function you (or the standard library
author) wrote. `a + b` for two `int`s is built into the language, but
`a + b` for two `std::string`s is a function named `operator+` that
somebody defined. Once you can read and write these functions, a lot of
"magic" behavior you have been using all course -- `std::string`'s `+`,
`std::cout`'s `<<`, and soon the `++`/`*` you will see on iterators --
stops being magic.

## Concepts covered

- Operators as ordinary functions with special names (`a + b` is
  `operator+(a, b)`, or `a.operator+(b)` for a member)
- The member-vs-free decision: a member function when your type is the
  left operand, a free function when it is not (e.g. `operator<<` with
  `std::cout` on the left)
- `operator==`, `operator!=`, and `operator<` for content-based
  comparison and ordering
- `operator+` returning a new object instead of mutating an operand
- `operator[]` with a non-const overload (returns a reference, so it can
  be written through) and a const overload (returns by value, read-only)
- Pre-increment vs. post-increment (`operator++()` vs `operator++(int)`)
  and why post-increment needs an extra copy
- `explicit operator bool` for safe use in `if`/`while` conditions

## How it works

Read each short C++ program and predict exactly what it prints to
standard output. Correct predictions unlock an explanation of the
operator-overloading rule the snippet demonstrates. All nine correct
answers together unlock the passphrase.

No compilation needed on your end -- just read the code and reason
through it.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All nine answers are correct and the program prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- operators are just functions</summary>

Whenever you see `a + b`, `a == b`, `a < b`, or `a[i]` on a value of a
class type, mentally rewrite it as a function call:
`a.operator+(b)`, `a.operator==(b)`, `a.operator<(b)`, `a.operator[](i)`.
Then go read that function's body like you would read any other member
function -- the operator syntax is just a shorthand the compiler
provides for calling it.

</details>

<details>
<summary>Hint 2 -- reference vs. value return matters</summary>

If an operator returns a reference (`T&`), the caller can write through
what it returns (`t[1] = 99;`). If it returns by value (`T`), the caller
gets a fresh copy and cannot modify the original through it. This single
distinction explains both `operator[]`'s two overloads and the
difference between pre-increment (returns `*this` by reference) and
post-increment (returns a saved copy by value).

</details>

<details>
<summary>Hint 3 -- who is on the left?</summary>

For a binary operator like `a @ b` (`@` standing in for `+`, `==`,
`<<`, whatever), ask: is `a`'s type one you wrote? If yes, a member
function works, because the compiler passes `a` as the implicit `this`
and `b` as the parameter. If `a`'s type is NOT yours (like
`std::ostream` for `std::cout << p`), the operator must be a free
function taking both sides as explicit parameters -- you cannot add
member functions to a class you do not own.

</details>

## Going further

- Implement `operator+=` for a small class first, then write
  `operator+` in terms of it (`T operator+(const T& o) const { T r =
  *this; r += o; return r; }`). Many real codebases prefer this order
  because it avoids duplicating the arithmetic logic.
- Look up `std::string`'s full operator catalog (`operator+`,
  `operator==`, `operator[]`, `operator+=`, and more) in a reference and
  compare each one's signature to the patterns from this activity.
- Consider a class where `operator+` is defined to actually SUBTRACT.
  It compiles fine -- the compiler enforces nothing about what an
  operator "should" do. Nothing stops you from writing this, which is
  exactly why it is a bug: it violates the reader's expectation that `+`
  behaves like addition. This "least surprise" rule is the real
  constraint on operator overloading, and the compiler cannot check it
  for you.
- C++20 adds the spaceship operator `operator<=>`, which can generate
  `<`, `<=`, `>`, `>=`, `==`, and `!=` all from a single function. Look
  up its default (`= default`) form as a preview of where this is
  heading.
