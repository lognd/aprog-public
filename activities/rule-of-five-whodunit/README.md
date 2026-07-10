# Activity: Rule of Five Whodunit

A C++ class that manages a raw resource -- HEAP memory obtained with `new`,
a file handle from `fopen`, a socket, anything that must eventually be
released by hand -- has to get FIVE special member functions right, or bad
things happen: the destructor, the copy constructor, the copy-assignment
operator, the move constructor, and the move-assignment operator. Together
these are called the **Rule of Five** (the older **Rule of Three** covers
just the first three, from before C++11 added move semantics).

Each question in this activity shows you a class with one or more of those
five missing, wrong, or subtly broken. Your job is to play detective: read
the code, trace through what actually happens when it runs, and name the
bug.

## Concepts covered

- The Rule of Three / Rule of Five: if a class needs a user-defined
  destructor, copy constructor, or copy-assignment operator, it very
  likely needs all of them (plus, since C++11, the two move members)
- Shallow copy (copying a pointer's VALUE) vs. deep copy (allocating new
  memory and copying the pointed-to data)
- Double delete / double free: calling `delete` or `delete[]` twice on the
  same address
- Memory leaks: allocated memory that nothing ever frees
- Dangling pointers: pointers left pointing at memory that has already
  been freed
- The self-assignment bug and why `if (this == &other)` guards exist
- Why a move constructor must leave the source object in a state its
  destructor can safely handle (usually by nulling out a pointer member)

## How it works

Each question shows a short, complete class definition and a `demo()`
function that uses it. Nothing is compiled or run here -- you are reading
the code by hand, the same way you would when reviewing a classmate's (or
your own) code for a subtle bug. For each question, decide which of five
outcomes best describes what actually happens:

- `double delete` -- the same memory address is freed more than once
- `memory leak` -- memory is allocated and never freed
- `dangling pointer after copy` -- a pointer is left referring to memory
  that has already been freed
- `self-assignment bug` -- the code breaks specifically when an object is
  assigned to itself (`a = a;`)
- `nothing wrong` -- the class is actually correct

Wrong answers come with a detailed explanation of why that outcome does
NOT match the code, and the correct answer's explanation walks through
the Rule of Three/Five reasoning in full.

## Getting started

```bash
python3 launch.py
```

Read each class carefully. Pay special attention to which of the five
special members are present, which are missing (and therefore
compiler-generated), and what the compiler-generated DEFAULT version of
each one actually does with a raw pointer member (it just copies the
pointer VALUE -- a shallow copy -- never the memory it points to).

## You will know you are done when...

All seven questions have been answered correctly and the launcher prints
the passphrase.

## Hints

<details>
<summary>Hint 1 -- what does the compiler generate by default?</summary>

If a class does not declare a copy constructor, the compiler generates one
that copies every member FIELD BY FIELD. For a raw pointer, "copying the
field" means copying the pointer's numeric address -- both objects end up
pointing at the exact same memory. This is a SHALLOW COPY. It is almost
never what you want for a class that owns a resource.

</details>

<details>
<summary>Hint 2 -- constructor calls vs. assignment operator calls</summary>

`Type b = a;` where `b` is a BRAND NEW variable calls the COPY
CONSTRUCTOR. `b = a;` where `b` was ALREADY declared on an earlier line
calls the COPY-ASSIGNMENT OPERATOR instead. These are two different
functions with two different jobs -- a constructor builds a new object; an
assignment operator must first deal with whatever the target object
already owned.

</details>

<details>
<summary>Hint 3 -- self-assignment</summary>

`a = a;` looks pointless, but it can happen indirectly (e.g. through a
reference or a container operation) and a naive `operator=` that frees its
own data before finishing reading from `other` will corrupt itself when
`other` turns out to BE `*this`. The fix is a guard at the very top:
`if (this == &other) return *this;`.

</details>

## Going further

- Take the `LinkedList` example from this activity and write a CORRECT
  deep-copy copy constructor for it. How many new `Node` allocations does
  copying a list of length N require?
- Rewrite the `Buffer` class using `std::vector<int>` internally instead
  of a raw `new[]` array. How many of the five special members do you
  still need to write by hand?
- Research `std::unique_ptr` and `std::shared_ptr`. For each bug in this
  activity, would replacing the raw pointer with a smart pointer have
  prevented it entirely, or would you still need to think about the same
  issue?
- Compile one of the buggy classes for real, run it under
  AddressSanitizer (`g++ -fsanitize=address -g`), and read the report.
  Does it point at the exact line you identified as the bug?
