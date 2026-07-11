# Activity: Array Foray

`std::array` is a fixed-size array. Unlike `std::vector`, it cannot grow or
shrink -- its size is set once and never changes. That size must appear in
the type itself, written between the angle brackets:

```cpp
std::array<int, 3>   // an array of exactly 3 ints -- always
```

This activity shows you what that constraint means in practice and why it
exists.

## Background

Every program has two main regions of memory for storing data.

**The stack** is where local variables live. When you write `int x = 5;`
inside a function, `x` lands on the stack. The compiler figures out exactly
how much space the function needs for all of its local variables and writes
that number into the program *before it ever runs* -- at compile time.
Because of this, stack variables are sometimes called "**statically
allocated**": their layout is fixed.*

**The heap** is a separate region used for memory whose size is only known
*at runtime* and is "**dynamically allocated**" -- for example, an array
whose length comes from user input. We will cover the heap in detail later.
For now the key point is that it is *elsewhere*: heap memory has a
completely different address range than stack memory. `std::vector` stores
its elements on the heap, which is why its size can change as you call
`push_back`. `std::array` stores its elements directly inside the variable,
on the stack, which is why its size cannot change after the type is written.

<details>
<summary>* Footnote</summary>
There is a small caveat. If you have programmed in C before, this might be
interesting. If this footnote does not make sense, please don't let it
distract you from the main point and ignore it. However, <i>technically
speaking</i>, nothing <i>stops</i> variable length stack allocations. In
fact, you can <code>alloca</code> (which doesn't require a
<code>free</code>) rather than <code>malloc</code> (which does). This
technique is used for the <b>universally hated</b> "variable-length array".
Variable length stack allocations are <b>super dangerous</b> because (1)
they are impossible to statically analyze with coding tools, and (2) your
maximum stack size is generally small, so static allocation is <i>always</i>
preferred to avoid stack-smashing. If you want to learn more, we encourage
you to talk to course staff.
</details>

## Concepts covered

- `std::array<T, N>` and why its size must be a compile-time value
- Stack vs. heap memory and where each container stores its elements
- `sizeof` and what it reveals about a type's layout
- Compile-time constants vs. runtime variables

## How it works

A shell opens inside a fresh copy of the project. You will run an
exploration program to observe how `std::array` and `std::vector` differ in
memory, then fix a compile error that illustrates why `std::array` requires
a compile-time size.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- run the exploration program

```bash
make explore && ./explore
```

Read every line of the output before continuing. It covers two things:

**sizeof** -- `sizeof(T)` tells you how many bytes a value of type `T`
occupies. Notice that `sizeof(std::array<int, 3>)` and
`sizeof(std::array<int, 10>)` are not the same -- the size is baked into
the type, so different sizes are literally different types with different
byte counts.

`sizeof(std::vector<int>)` is the same number no matter how many elements
the vector holds, because the vector's elements live on the heap and are
not counted in the vector object itself.

**Addresses** -- the output prints three addresses: one for a local `int`,
one for `arr[0]`, and one for `vec[0]`. Notice which two are close together
and which one is far away. Local variables and `std::array` elements all
live on the stack -- same region, similar addresses. `std::vector` elements
live on the heap -- a completely different region, far away.

### Step 2 -- try to compile main.cpp

```bash
make
```

It will fail. Read the error message carefully. The compiler is rejecting
`main.cpp` because of how `std::array`'s size is written.

Here is why: to lay out the stack frame the compiler must know the exact
size of every local variable before the program runs. For
`std::array<int, N>` that means `N` must be a compile-time value -- a
literal or a compile-time constant, not an ordinary variable whose value
is only known at runtime.

### Step 3 -- fix main.cpp and compile again

Open `main.cpp`, find the line that fails to compile, and change it so the
array size is a compile-time value.

```bash
make run
```

### Step 4 -- exit

```
exit
```

The launcher will check your fix automatically and reveal the passphrase.

## You will know you are done when...

`make run` compiles and runs without errors and the launcher prints the
passphrase.

## Hints

<details>
<summary>Hint 1 -- which line to change</summary>

Look for the line that declares the `std::array`. The size is currently
written using an ordinary `int` variable, which is a runtime value. Replace
the variable with the number directly.

</details>

<details>
<summary>Hint 2 -- why a literal works but a variable does not</summary>

The literal `3` is written directly in the source code, so the compiler sees
it immediately and can use it to size the stack frame. A variable like
`int n = 3` could in principle be changed before that line runs, so the
compiler treats it as a runtime value even when you can tell it never
changes.

</details>
