# Matrix Class

Implement a 2D matrix class that supports addition, multiplication, and
transposition.

## Problem Statement

The header `matrix-class.hpp` declares the `Matrix` class. Implement all
methods in `matrix-class.cpp`. Matrices contain `double` values and are
stored in row-major order.

## Interface

```cpp
class Matrix {
public:
    Matrix(int rows, int cols);          // create rows x cols zero matrix
    Matrix(const Matrix &other);         // deep copy
    Matrix &operator=(const Matrix &);   // copy assignment
    ~Matrix();

    int rows() const;
    int cols() const;
    double &at(int r, int c);            // element access (0-indexed)
    const double &at(int r, int c) const;

    Matrix operator+(const Matrix &rhs) const;  // element-wise add
    Matrix operator*(const Matrix &rhs) const;  // matrix multiply
    Matrix transpose() const;

    void print(std::ostream &out) const; // space-separated rows, one per line
};
```

## Requirements

- Use a heap-allocated array for storage (no `std::vector`)
- All operations must work on matrices of compatible dimensions
- `print` separates values with spaces and ends each row with a newline

## Grading

| Component              | Points |
|------------------------|--------|
| Compilation            | 0 (required) |
| Visible tests (Catch2) | 60     |
| Hidden tests (Catch2)  | 40     |

## Submission

Submit `matrix-class.hpp` and `matrix-class.cpp`. Do not change the
class name or method signatures in the header.
