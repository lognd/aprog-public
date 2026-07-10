# Activity: Const Maze

C++ has four related keywords -- `const`, `constexpr`, `consteval`, and
`constinit` -- that all sound similar but do very different things. This
activity walks you through each one so you can distinguish them precisely.

## The four keywords at a glance

| Keyword | Applies to | Read-only? | When is the value set? |
|---------|-----------|------------|------------------------|
| `const` | variables, parameters, member functions | yes | compile time OR runtime |
| `constexpr` | variables and functions | yes (for variables) | must be evaluable at compile time |
| `consteval` | functions only | N/A | must be called at compile time |
| `constinit` | variables only | NO | must be initialized at compile time |

### `const`

Marks a variable or parameter as read-only after initialization. The
initializer can be a runtime value.

```cpp
int x = rand();
const int limit = x;   // read-only, but set at runtime
```

For pointers, position matters:

- `const int* p` -- pointer-to-const: you cannot write `*p`, but you can
  reassign `p` itself.
- `int* const p` -- const-pointer: you cannot reassign `p`, but you can
  write `*p`.
- `const int* const p` -- both locked.

Read pointer declarations right-to-left: "p is a const pointer to int" or
"p is a pointer to const int."

### `constexpr`

Requires that the value can be computed at compile time. For variables,
`constexpr` implies `const` -- the variable is always read-only.

```cpp
constexpr int SIZE = 64;    // compile-time constant, read-only
int arr[SIZE];              // legal: SIZE is known at compile time
```

A `constexpr` function may be called at compile time or runtime depending
on the arguments. If the arguments are compile-time constants, the call is
evaluated by the compiler.

### `consteval` (C++20)

An immediate function: every call must produce a compile-time constant. If
you pass a runtime value, the program is ill-formed.

```cpp
consteval int square(int n) { return n * n; }

constexpr int a = square(4);   // OK: 4 is a compile-time constant
int x = 5;
int b = square(x);             // ERROR: x is not a compile-time constant
```

Use `consteval` when you want to guarantee that a function is never called
at runtime.

### `constinit` (C++20)

Requires that a variable with static or thread storage duration is
initialized with a compile-time constant. Unlike `const` and `constexpr`,
it does NOT make the variable read-only -- you can assign to it later.

```cpp
constinit int counter = 0;   // guaranteed compile-time init
counter = 42;                // perfectly legal: counter is still mutable
```

`constinit` was introduced to prevent the static initialization order
fiasco: when two global variables in different translation units (the
separate `.cpp` files the compiler processes one at a time, each becoming
its own object file before linking) depend on each other, initialization
order is undefined. `constinit` ensures no
dynamic initialization is needed, eliminating the hazard.

## Concepts covered

- `const` position relative to `*`: pointer-to-const vs const-pointer vs both
- `const` member functions and what they prevent
- `const` references as the idiomatic way to pass large objects without copying
- `constexpr`: compile-time evaluation, implies read-only for variables
- `consteval`: immediate functions that must be called at compile time (C++20)
- `constinit`: compile-time initialization without read-only restriction (C++20)

## How it works

Eleven questions covering pointer const declarations, const member
functions, const references, constexpr, consteval, and constinit. Each
question has a hint. The activity unlocks a passphrase when all answers are
correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All eleven questions are correct and the program prints the passphrase.

## Going further

- Look up the "east const" convention (writing `int const*` instead of
  `const int*` so the qualifier always reads left-to-right after the type
  it applies to) and read the arguments for and against it.
- Why can a `const` reference bind to a temporary (`const int& r = 5;`) but
  a non-const reference cannot? (This will be super important for something
  called the "Big 5" later on!)
- Write a `consteval` function and confirm that passing a runtime variable
  produces a compile error.
- Add a `constinit` global to a program and verify you can modify it after
  `main` starts.
- Look up the static initialization order fiasco and explain why `constinit`
  solves it but `const` does not.
