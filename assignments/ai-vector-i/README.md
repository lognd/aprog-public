# VectorI: Dynamic Integer Array

For this lab you will use AI or a friend's code to produce a working implementation
of a dynamic integer array -- and then fix it.

You are given the following **intentionally broken** starter code. It has **several bugs**.
Your job is to find and fix every one of them so that `VectorI` compiles and behaves correctly.

## Learning goals

- Learn how to vibe code.
- Understand why relying on code-generation tools in a course designed to teach you how to program is a bad idea.
- Understand that you will be shooting yourself in the foot in later courses and work if you rely on code-generation tools.

## Starter file

**`vector_i.hpp`** (see `assets/`)

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

## Your task

Fix every bug in `vector_i.hpp` so that `VectorI`:

1. Compiles without warnings under `-Wall -Wextra`.
2. Correctly copies elements in the copy constructor (no shallow copies, correct size).
3. Correctly moves ownership in the move constructor (leaves source in a valid empty state).
4. Correctly implements copy and move assignment operators (returns `*this`, no resource leaks).
5. Correctly grows the backing array in `push_back` (doubles capacity from a non-zero base).
6. Returns a reference to the element just inserted by `push_back`.

## Submission

Submit only `vector_i.hpp`. Do not add a `main` function.
