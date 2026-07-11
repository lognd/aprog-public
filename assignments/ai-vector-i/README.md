# VectorI: Dynamic Integer Array

You are going to "vibe code" a fix for a broken class. **Vibe coding** means
using an AI assistant (or a friend, or a Stack Overflow answer you do not
fully read) to produce code and accepting it because it seems to work,
without checking that you understand every line. That is exactly what you
are asked to do here: hand the broken file below to an AI assistant, get it
to a state where it compiles and passes the tests, and submit it.

The point of this assignment is not the fix itself. The point is what
happens after: once your submission passes, you will be asked to explain,
line by line, why each bug was a bug and why your fix works (see
**Reflection** below). If the only thing you can say is "the AI changed it
and now it passes," you have just experienced, first-hand, why shipping
code you do not understand is a bad habit to build this early in a
programming course. Later courses and jobs will not have a visible-tests
folder checking your work for you.

---

## Task

Below is the starter file, reproduced exactly as given to you (the full
version is in `assets/vector_i.hpp`). It is **intentionally broken**: it
has several bugs, marked with comments telling you how many errors are on
each line, but not what they are.

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

Give this file to an AI assistant (or fix it yourself, if you already see
the bugs) and get it to a state where `VectorI`:

1. Compiles without warnings under `-Wall -Wextra`.
2. Correctly copies elements in the copy constructor -- no shallow copies,
   correct size, and a matching allocator (whatever you allocate with, free
   with the same family: `malloc`/`free` or `new[]`/`delete[]`, never mixed).
3. Correctly moves ownership in the move constructor -- leaves the source
   in a valid, empty state (`data == nullptr`, `size == 0`, `capacity == 0`).
4. Correctly implements copy and move assignment operators -- both return
   `*this`, and neither leaks the object's previous buffer.
5. Correctly grows the backing array in `push_back` -- doubles capacity
   from a non-zero base (a capacity of 0 should become 1, not stay 0).
6. Returns a reference to the element just inserted by `push_back`, not a
   reference to the local parameter.
7. Has a destructor that frees the buffer, and public `int& operator[](size_t i)`
   and `size_t get_size() const` accessors -- none of these three exist yet
   in the starter file, and the visible test below will not catch their
   absence, but the class cannot be used or graded without them.

## Files

| File | Purpose |
|------|---------|
| `vector_i.hpp` | The broken starter class -- fix it and submit this file |

## Compilation and Testing

```bash
cd visible-tests
g++ -std=c++17 -Wall -Wextra -o test_vi test_vector_i.cpp -I../assets
./test_vi
```

A clean compile with no warnings and a printed `ok` is a good first
indicator your fixes are correct. It does not exercise `operator[]`,
`get_size()`, or the destructor -- check those by hand, or write a quick
extra `main` of your own locally (do not submit one).

## Constraints

- Submit only `vector_i.hpp`. Do not add a `main` function to it.
- Pick one allocator family and use it everywhere in the file. Do not free
  `malloc`-allocated memory with `delete`/`delete[]`, and do not free
  `new[]`-allocated memory with `free`.

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| `push_back` stores values correctly | 10 |
| `push_back` tracks size correctly | 5 |
| `push_back` returns a reference to the stored element | 10 |
| Copy constructor (deep copy) | 15 |
| Move constructor | 15 |
| Copy assignment operator | 15 |
| Move assignment operator | 15 |
| Growth strategy (`push_back` past initial capacity) | 15 |
| **Total** | **100** |

## Submission

Submit a single file named `vector_i.hpp`. Do not rename it.

---

## Reflection

This part is not scored by the autograder -- follow your instructor's
instructions for where to submit it. After your `vector_i.hpp` passes the
visible tests, write a short paragraph (5-10 sentences) answering:

- For each of the seven fixes above, can you explain in your own words why
  the original code was wrong and why your fix is correct? List any you
  cannot explain.
- Did you read and understand every line the AI assistant produced before
  you accepted it, or did you accept something because it "made the errors
  go away"?
- If you had submitted this without being asked to explain it afterward,
  would you have caught the allocator mismatch (constraint above) or the
  missing destructor (item 7) on your own?

## Going further

- Run your fixed class under AddressSanitizer
  (`g++ -std=c++17 -fsanitize=address -g ...`) with a small `main` that
  copies and destroys several `VectorI` objects. If you picked `malloc` in
  the copy constructor but `delete[]` in the destructor (or vice versa),
  ASan will report an "alloc-dealloc-mismatch" -- this is exactly the bug
  described in the constraints above, and it is easy to introduce by
  accident when different fixes come from different AI suggestions.
- Compare your fixed `vector_i.hpp` against `std::vector<int>`. What does
  the standard library version do differently around growth strategy,
  exception safety, or allocator flexibility?
