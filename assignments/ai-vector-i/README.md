# VectorI: Dynamic Integer Array

Your AI intern was asked to implement a small dynamic array class for
integers -- something like a tiny `std::vector<int>` -- and turned in code
that looks plausible, compiles in nobody's head, and is wrong in almost
every function. This assignment gives you that code as-is. Your job is to
read it critically, find every bug, and turn it into a `VectorI` that
actually owns its memory correctly.

This is really an exercise in **the Rule of Five**: any class that manages
a resource (here, a heap-allocated `int*` buffer) needs five special member
functions working together, not just "whatever compiles."

## Background

### Ownership and the Rule of Three / Rule of Five

When a class allocates a resource in its constructor -- heap memory, a file
handle, a socket -- it becomes responsible for that resource's entire
lifetime. The compiler will happily generate default versions of the
special member functions for you, but those defaults only know how to copy
member variables one at a time. For a raw pointer member, that means
copying the *address*, not the data it points to.

The classic guidance is the **Rule of Three**: if a class defines any one
of a destructor, a copy constructor, or a copy assignment operator, it
almost certainly needs to define all three. If you free a resource in the
destructor, but let the compiler generate a copy constructor that copies
the pointer, you end up with two objects that both think they own the same
memory -- and both will try to free it.

C++11 extended this to the **Rule of Five** by adding move construction and
move assignment. Moving a resource means transferring ownership instead of
duplicating it: the new object takes the pointer, and the old object is
left in a valid but empty state (typically `nullptr` and zero size) so its
destructor is a no-op. A class that manages a resource should define all
five: destructor, copy constructor, copy assignment, move constructor, move
assignment.

### Deep copy vs. shallow copy

A **shallow copy** copies a pointer's value -- the address -- leaving both
the original and the copy pointing at the same underlying memory. This is
what happens if you copy a `int*` member with plain assignment and do
nothing else:

```cpp
// shallow -- both objects now share one buffer
this->data = other.data;
```

Once both objects hold the same address, whichever one is destroyed first
frees the memory out from under the other. The survivor is left holding a
**dangling pointer** -- any use of it, including its own destructor running
later, is undefined behavior. This exact bug is why the starter code's copy
constructor and copy assignment operator both need to be rewritten: a
correct copy constructor performs a **deep copy** -- it allocates its own,
separate buffer and copies the *elements* into it, so the two objects never
share memory:

```cpp
// deep -- a new buffer, elements copied in
this->data = new int[other.capacity];
for (size_t i = 0; i < other.size; ++i) {
    this->data[i] = other.data[i];
}
```

### Move semantics

Copying is correct but wasteful when the source object is about to be
destroyed anyway -- for example, returning a local `VectorI` by value, or
explicitly writing `std::move(v)`. Move construction and move assignment
exist for exactly that case: instead of allocating a new buffer and copying
every element, the new object simply takes the old object's pointer, and
the old object is reset to a state where its destructor does nothing
harmful:

```cpp
VectorI(VectorI&& other) noexcept {
    this->data     = other.data;
    this->size     = other.size;
    this->capacity = other.capacity;
    other.data     = nullptr;   // leave the source empty and safe to destroy
    other.size     = 0;
    other.capacity = 0;
}
```

Notice the parameter type is `VectorI&&`, an rvalue reference -- not
`const VectorI&&`. `const` would forbid modifying `other`, but modifying
`other` (stealing its pointer, then zeroing it out) is the entire point of
a move. A `const` rvalue reference parameter cannot express "please let me
gut this object" -- which is one of the bugs you will find in the starter
code.

### Allocation consistency: new/delete vs malloc/free

C++'s `new[]` and `delete[]` are not interchangeable with C's `malloc` and
`free`. `new int[n]` allocates space for `n` ints and, for non-trivial
types, would run constructors; `malloc(n)` allocates `n` *bytes* with no
knowledge of `int` at all. Mixing them -- allocating with one and freeing
with the other, or allocating the wrong number of bytes -- is undefined
behavior even when it happens to "work" on your machine. A class that
allocates its buffer with `new int[...]` must free it with `delete[]`, not
`free`, and vice versa.

## Task

Fix every bug in `vector_i.hpp` so that `VectorI`:

1. Compiles cleanly under `-Wall -Wextra` with no warnings.
2. Has a correct destructor that frees the buffer exactly once.
3. Correctly deep-copies elements in the copy constructor (own buffer,
   correct size, no shared pointers).
4. Correctly transfers ownership in the move constructor (source left in a
   valid, empty state; parameter is a non-const rvalue reference).
5. Correctly implements copy assignment (returns `*this`; no leaked
   buffer from the object's previous contents).
6. Correctly implements move assignment (returns `*this`; transfers
   ownership rather than copying).
7. Correctly grows the backing array in `push_back` (doubles capacity from
   a non-zero base, uses the same allocation function it frees with).
8. Returns a reference to the element just inserted by `push_back`, not a
   reference to the parameter.

The starter file below is what you are given. Read every line -- most of
them look reasonable until you check what they actually do to `this` or
`other`.

```cpp
class VectorI {
// Something is missing here.
    VectorI() = default;

    VectorI(const VectorI& other) {
        this->capacity = other.capacity;
        this->size = other.size;
        this->data = static_cast<int*>(malloc(other.size));  // 2 errors: semantic & logical
        for (char i = 0; i < this->size; ++i) {             // 1 error: logical
            this->data[i] = other.data[i];
        }
    }

    VectorI(const VectorI&& other) {                        // 2 errors
        this->data = other.data;
        this->size = other.size;
        this->capacity = other.capacity;
    }

    VectorI& operator=(const VectorI& other) {
        this->capacity = other.capacity;
        this->size = other.size;
        this->data = other.data;                            // 1 error
    }

    VectorI& operator=(VectorI&& other) {                  // 1 error
        this->capacity = other.capacity;
        this->size = other.size;
        this->data = other.data;
        other.capacity = 0;
        other.size = 0;
        other.data = nullptr;
    }

    int& push_back(int i) {
        if (size >= capacity) {
            // error in this scope
            this->capacity = capacity ? 1 : capacity * 2;
            delete[] this->data;
            this->data = new int[this->capacity];
        }
        this->data[size++] = i;
        return i;                                           // 1 error
    }

private:
    size_t capacity = 0;
    size_t size = 0;
    int* data = nullptr;
};
```

## Files

| File | Purpose |
|------|---------|
| `assets/vector_i.hpp` | Starter header (intentionally broken) -- fix and submit this file |
| `visible-tests/test_vector_i.cpp` | Visible smoke test -- exercises the constructors and checks for a clean compile |

## Compilation and Testing

```bash
g++ -std=c++17 -Wall -Wextra -o test_vi visible-tests/test_vector_i.cpp -Iassets
./test_vi
```

A clean compile with zero warnings is a strong first signal that your Rule
of Five fixes are on the right track. The smoke test only checks that the
program runs without crashing and prints `ok` -- it does not check the
actual contents of copied or moved vectors, so passing it is necessary but
not sufficient.

## Constraints

- Do not add a `main` function to `vector_i.hpp`.
- Do not change the class's public interface (constructor, copy/move
  operations, and `push_back` must keep their existing signatures).
- Do not replace `int*` with `std::vector<int>` or another container --
  the point of the exercise is managing the raw buffer yourself.

## Grading

| Component               | Points |
|--------------------------|--------|
| Compilation              | 0*     |
| `push_back` basic values | 10     |
| `push_back` size tracking | 5     |
| `push_back` return reference | 10 |
| Copy constructor         | 15     |
| Move constructor         | 15     |
| Copy assignment          | 15     |
| Move assignment          | 15     |
| Growth (capacity doubling) | 15   |
| **Total**                | **100** |

\* Compilation must succeed before any correctness cases are scored, but
does not itself carry points.

## Submission

Submit only `vector_i.hpp`. Do not rename it, and do not add a `main`
function.

## Going further

- Add a destructor and run your fixed class under
  `g++ -fsanitize=address` with a program that copies and moves several
  `VectorI` instances. Do you get a clean run, or does ASan report a
  double-free or use-after-free?
- Implement `operator==` for `VectorI` by comparing size and elements.
  Why would comparing `data` pointers directly be wrong?
- Read about the copy-and-swap idiom. How would it simplify writing a
  correct copy assignment operator that is also exception-safe?
