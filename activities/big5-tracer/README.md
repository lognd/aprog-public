# Activity: Big 5 Tracer

Every C++ class has up to five special member functions that the compiler
can call on your behalf: the constructor, the copy constructor, the move
constructor, the copy-assignment operator, and the move-assignment
operator, plus the destructor. Together the first five are commonly called
the **Big Five**. Most of the time you never see them run -- they fire
silently whenever an object is constructed, copied, moved, or destroyed.
This activity makes them loud.

You are given nine short C++ snippets, each using an instrumented class
that prints a line from inside every special member function it runs. Your
job is to predict the EXACT sequence of output before you see it, then
compile and check your answer.

## Concepts covered

- The Big Five special member functions: constructor, copy constructor,
  move constructor, copy-assignment operator, move-assignment operator,
  and the destructor
- The difference between constructing a new object (a constructor runs)
  and overwriting an existing one (an assignment operator runs)
- `std::move` as a cast, not an action -- and how it changes which
  overload is selected
- Guaranteed copy elision in C++17 for a direct `return SomeType(...);`
- Why passing by `const&` avoids a copy entirely, while passing by value
  does not
- Member initializer lists vs. assignment in the constructor body

## How it works

Every snippet is built around a `Tracer` class. `Tracer` owns nothing real
(no HEAP memory, meaning dynamically-allocated memory obtained with `new`
that must later be released with `delete`) -- it exists purely to print
which special member function ran, in order, with the `id` value involved:

```cpp
struct Tracer {
    int id;
    Tracer(int i) : id(i) { printf("ctor %d\n", id); }
    Tracer(const Tracer& o) : id(o.id) { printf("copy-ctor %d\n", id); }
    Tracer(Tracer&& o) noexcept : id(o.id) { printf("move-ctor %d\n", id); o.id = -1; }
    Tracer& operator=(const Tracer& o) { id = o.id; printf("copy-assign %d\n", id); return *this; }
    Tracer& operator=(Tracer&& o) noexcept { id = o.id; printf("move-assign %d\n", id); o.id = -1; return *this; }
    ~Tracer() { printf("dtor %d\n", id); }
};
```

The launcher compiles each snippet with `g++ -std=c++17`, runs it, and
compares your prediction against the real output character-for-character.
Snippets whose output spans multiple lines ask you to enter one line at a
time. Every prediction has to be exact, including the ORDER of lines --
destructors, in particular, always run in the REVERSE order of
construction for objects in the same scope.

## Getting started

```bash
python3 launch.py
```

You will be shown each snippet's source code, then asked to predict its
output. Read the code carefully before answering -- in particular, notice
whether an object is passed BY VALUE (a copy) or BY REFERENCE (no copy),
and whether `std::move` appears anywhere.

## You will know you are done when...

All nine snippets have been predicted correctly and the launcher prints
the passphrase.

## Hints

<details>
<summary>Hint 1 -- constructor vs. assignment operator</summary>

A CONSTRUCTOR runs when a NEW object is being brought into existence for
the first time (`Tracer b(a);` or `Tracer b = a;` with `b` freshly
declared). An ASSIGNMENT OPERATOR runs when an object that ALREADY EXISTS
is being overwritten (`b = a;` where `b` was declared on an earlier line).
Look at whether the left-hand object is brand new or already declared.

</details>

<details>
<summary>Hint 2 -- std::move does not move anything by itself</summary>

`std::move(x)` is just a cast: it tells the compiler "you may treat `x` as
disposable," which makes overload resolution prefer the move constructor
or move-assignment operator over the copy versions. The actual "stealing"
of the value happens inside whichever move function runs, not inside
`std::move` itself.

</details>

<details>
<summary>Hint 3 -- guaranteed copy elision</summary>

Since C++17, a function that directly returns a temporary written right
there in the `return` statement (a PRVALUE, e.g. `return Tracer(5);`) is
GUARANTEED by the standard to construct that value directly in the
caller's storage -- no move constructor call happens at all, even though
it might look like one should. This is different from returning a named
local variable, where the compiler is only ALLOWED, not required, to skip
the move.

</details>

## Going further

- Add a `std::vector<Tracer>` and call `push_back` several times without
  reserving capacity first. Watch what happens when the vector reallocates
  -- do you see move-ctor or copy-ctor calls, and why does that depend on
  whether the move constructor is marked `noexcept`?
- Delete the move constructor and move-assignment operator from `Tracer`
  (`Tracer(Tracer&&) = delete;`) and rerun snippet 4. What happens to
  `std::move(a)` now -- does the code still compile, and if so, which
  constructor actually runs?
- Write a class that owns a real heap resource (a `new[]`-allocated
  array) instead of just an `int`, following the same print-from-every-
  special-member pattern, and confirm your understanding of when each
  member runs before moving on to the Rule of Five Whodunit activity.
