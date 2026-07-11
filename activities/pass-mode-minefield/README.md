# Activity: Pass-Mode Minefield

C++ gives you three different ways to hand a variable to a function: by
value, by reference, and by pointer. They look similar at the call site --
`f(x)` versus `f(x)` versus `f(&x)` -- but they produce completely different
relationships between the caller's variable and what the function sees.
Choosing the wrong one is one of the most common sources of silent bugs in
new C++ code: a function that "modifies" a variable but somehow the caller
never sees the change, or vice versa. This activity trains you to read a
function signature and know immediately what the callee can and cannot do.

## Background

**Pass by value** (`void f(int x)`) gives the function its own independent
copy. Whatever the function does to `x`, the caller's original variable is
completely unaffected -- the copy lives in its own stack slot and is
destroyed when the function returns.

```
caller:  n = 5
call:    double_it(n)   -- a COPY of n's value (5) is placed into x
inside:  x *= 2         -- x becomes 10, n is untouched
after:   n is still 5
```

**Pass by reference** (`void f(int& x)`) makes `x` an alias for the caller's
own variable -- not a copy, not a new object, just another name for the same
storage. Any modification to `x` inside the function is a modification to
the caller's variable, because they are the same memory.

```
caller:  n = 5
call:    double_it(n)   -- x becomes another name for n's storage
inside:  x *= 2         -- this writes directly into n's storage
after:   n is now 10
```

**Pass by pointer** (`void f(int* p)`) gives the function the *address* of
the caller's variable -- obtained at the call site with the address-of
operator `&` (`&n` means "the address where `n` lives") -- stored in its
own local pointer variable `p` (a variable whose value is an address rather
than an ordinary value). This is a hybrid: `p` itself is a copy (a copy of
an address), but dereferencing it (following the address to reach the
value stored there) with `*p` reaches back into the caller's original
storage.

```
caller:  n = 4
call:    triple(&n)     -- p is a new local variable holding n's address
inside:  *p *= 3         -- dereferencing p writes through to n's storage
after:   n is now 12
```

The distinction that trips people up most: **reassigning a pointer
parameter is not the same as modifying what it points to.** `p = &other;`
changes only the function's local copy of the address -- the caller's
pointer variable, if there was one, is unaffected, exactly like pass by
value for pointers. `*p = 99;` changes the pointee -- the actual object the
address refers to -- and the caller sees that change. A function that tries
to "swap two pointers" by swapping its own `int*` parameters demonstrates
this directly:

```cpp
void swap_ptrs(int* a, int* b) {
    int* tmp = a;
    a = b;
    b = tmp;
    // only the LOCAL variables a and b were swapped -- the caller's
    // pointers (whatever was passed as &x, &y) are untouched
}

void swap_vals(int* a, int* b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
    // this writes through both pointers into the caller's storage --
    // the caller's actual x and y are swapped
}
```

Arrays add one more wrinkle: a parameter written as `int arr[]` is, in
reality, just `int* arr` -- arrays *decay* (automatically convert) to a
pointer to their first element the moment they are passed to a function. There is no copying of array
contents; the function receives the address of the caller's array and can
modify its elements exactly as if it had been given a pointer explicitly.

One snippet in this activity combines the two reference-like tools you now
know -- a pointer, and a reference -- into a **reference to a pointer**:
`int*& rp = p;`. Read this type right-to-left: `rp` is a reference (`&`) to
an `int*` (a pointer to int). That makes `rp` an alias for the pointer
variable `p` itself, not for the int `p` points at. Assigning `rp = &b;`
therefore reassigns `p` (through its alias `rp`) to point at `b` -- exactly
as if you had written `p = &b;` directly. This matters because ordinary
pass-by-pointer (`int* p` as a parameter) only gives the callee a *copy* of
the address, so reassigning the parameter never affects the caller's
pointer (see the pointer-reassignment trap above); a reference to a
pointer is what you would need if you *did* want a function to be able to
repoint the caller's own pointer variable.

A common trap worth naming: passing a large object by value when you only
need to read it wastes an entire copy for no benefit (use `const T&`
instead), and passing by pointer or non-const reference when you only need
to read a value invites accidental modification. Choose the mode that
matches what the function actually needs to do: read-only access to a small
type -> pass by value; read-only access to a large type -> `const T&`;
the function must modify the caller's variable -> `T&` or `T*`.

## Concepts covered

- Pass by value: the callee gets an independent copy; the caller's variable
  never changes
- Pass by reference: the callee's parameter is an alias for the caller's
  storage; modifications are visible to the caller
- Pass by pointer: the callee gets a copy of an address; dereferencing
  reaches the caller's storage, but reassigning the pointer itself does not
- Reassigning a pointer parameter vs. modifying the pointee it refers to
- Array-to-pointer decay when arrays are passed as function parameters
- Reference to a pointer (`int*& rp`): an alias for the pointer variable
  itself, distinct from a plain pointer parameter

## How it works

You are shown six short C++ programs covering all three pass modes,
including a side-by-side pointer-swap vs. value-swap comparison and array
decay. Predict what each one prints before running it -- do not compile
them yourself, reason about what happens to each variable as it passes
through each function. The launcher compares your prediction against the
program's actual output. The activity unlocks when all six predictions are
correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All six predictions are correct and the program prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- ask "is this a copy or the same storage?"</summary>

For every parameter, ask: after the function returns, is the caller's
variable the same storage the function wrote to? Pass by value: no, always
a fresh copy. Pass by reference: yes, always the same storage. Pass by
pointer: the pointer variable itself is a copy, but `*p` reaches the same
storage as the address it holds.

</details>

<details>
<summary>Hint 2 -- swapping pointers does not swap what they point to</summary>

`a = b;` inside a function that receives `int* a, int* b` only changes
which address the *local* variable `a` holds. It does not touch the int
that the original `a` used to point at. To actually swap the values the
caller sees, you must dereference: `*a` and `*b`, not `a` and `b`.

</details>

<details>
<summary>Hint 3 -- arrays passed to functions are pointers</summary>

`void f(int arr[])` is identical to `void f(int* arr)` -- no array copying
happens. Modifying `arr[0]` inside the function modifies the caller's
array directly, because `arr` is the address of the caller's first element,
not a copy of the whole array.

</details>

## Going further

- Write a function that takes a large struct by value and the same function
  taking `const T&`. Compile both with `-O0` and compare the assembly. How
  many bytes are copied in each case?
- When does passing by pointer make more sense than passing by reference?
  Find a real example in a standard library function signature.
- Write a function that actually swaps two pointer variables in the
  caller -- what type does the parameter need to be? (Hint: you need a
  pointer to a pointer, or a reference to a pointer.)
- Look up move semantics (`T&&`). How does pass-by-move relate to the three
  modes covered here, and when would you use it?
