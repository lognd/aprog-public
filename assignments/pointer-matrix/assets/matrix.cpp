#include "matrix.hpp"
#include <cstdio>

// Return the element at row r, column c.
// Offset formula: r * cols + c
int mat_get(const int* m, int cols, int r, int c) {
    // TODO: return *(m + ???)
    return 0;
}

// Set the element at row r, column c to val.
void mat_set(int* m, int cols, int r, int c, int val) {
    // TODO: *(m + ???) = val;
}

// Set every element to val.
void mat_fill(int* m, int rows, int cols, int val) {
    // TODO: iterate over all rows * cols elements and assign val
}

// Element-wise addition: dst[r][c] = a[r][c] + b[r][c]
void mat_add(const int* a, const int* b, int* dst, int rows, int cols) {
    // TODO: iterate and add corresponding elements
}

// Transpose: dst element (c, r) = src element (r, c)
// Hint: dst has cols rows and rows columns -- use rows as dst's col count.
void mat_transpose(const int* src, int* dst, int rows, int cols) {
    // TODO: for each (r, c) in src, write to (c, r) in dst
}

// Sum of all elements in row r.
int mat_row_sum(const int* m, int cols, int r) {
    // TODO: sum cols elements starting at offset r * cols
    return 0;
}

// Sum of all elements in column c.
int mat_col_sum(const int* m, int rows, int cols, int c) {
    // TODO: sum rows elements, stepping by cols each time
    return 0;
}

// True if m[r][c] == m[c][r] for all r, c in [0, n).
bool mat_is_symmetric(const int* m, int n) {
    // TODO: compare each (r, c) pair with (c, r)
    return false;
}

// Print the matrix: one row per line, elements separated by spaces.
// No trailing space before the newline.
void mat_print(const int* m, int rows, int cols) {
    // TODO: print each row; use printf or std::cout
}
