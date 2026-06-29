#include "grid.hpp"

// Copy your implementation from Const Qualifier Toolkit, or rewrite it here.

char cell_at(const char* grid, int cols, int row, int col) {
    return grid[row * cols + col];
}

bool cell_is(const char* grid, int cols, int row, int col, const char& target) {
    return grid[row * cols + col] == target;
}

int count_cells(const char* grid, int rows, int cols, const char& target) {
    int n = 0;
    for (int i = 0; i < rows * cols; ++i)
        if (grid[i] == target) ++n;
    return n;
}

bool grids_equal(const char* a, const char* b, int rows, int cols) {
    for (int i = 0; i < rows * cols; ++i)
        if (a[i] != b[i]) return false;
    return true;
}

bool row_contains(const char* grid, int cols, int row, const char& target) {
    const char* r = grid + row * cols;
    for (int c = 0; c < cols; ++c)
        if (r[c] == target) return true;
    return false;
}

int find_in_row(const char* grid, int cols, int row, const char& target) {
    const char* r = grid + row * cols;
    for (int c = 0; c < cols; ++c)
        if (r[c] == target) return c;
    return -1;
}

const char* row_ptr(const char* grid, int cols, int row) {
    return grid + row * cols;
}

char* row_ptr_mut(char* grid, int cols, int row) {
    return grid + row * cols;
}

void set_cell(char* grid, int cols, int row, int col, char val) {
    grid[row * cols + col] = val;
}

void fill_grid(char* grid, int rows, int cols, const char& fill) {
    for (int i = 0; i < rows * cols; ++i)
        grid[i] = fill;
}

void fill_row(char* grid, int cols, int row, const char& fill) {
    char* r = grid + row * cols;
    for (int c = 0; c < cols; ++c)
        r[c] = fill;
}

void copy_row(const char* src, int src_cols, int row, char* dst) {
    const char* s = src + row * src_cols;
    for (int c = 0; c < src_cols; ++c)
        dst[c] = s[c];
}

void copy_grid(const char* src, char* dst, int rows, int cols) {
    for (int i = 0; i < rows * cols; ++i)
        dst[i] = src[i];
}
