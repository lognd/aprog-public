#pragma once
#include <cstdlib>
#include <cstddef>

class VectorI {
// Something is missing here.
    VectorI() = default;

    VectorI(const VectorI& other) {
        this->capacity = other.capacity;
        this->size = other.size;
        this->data = static_cast<int*>(malloc(other.size));  // 2 errors on this line: semantic & logical
        for (char i = 0; i < this->size; ++i) {             // 1 error on this line: logical
            this->data[i] = other.data[i];
        }
    }

    VectorI(const VectorI&& other) {                        // 2 errors on this line
        this->data = other.data;
        this->size = other.size;
        this->capacity = other.capacity;
    }

    VectorI& operator=(const VectorI& other) {
        this->capacity = other.capacity;
        this->size = other.size;
        this->data = other.data;                            // 1 error on this line
    }

    VectorI& operator=(VectorI&& other) {                  // 1 error on this line
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
        return i;                                           // error on this line
    }

private:
    size_t capacity = 0;
    size_t size = 0;
    int* data = nullptr;
};
