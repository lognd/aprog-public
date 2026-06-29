#include "grid.hpp"

// Implement each function below.  Do not modify grid.hpp.
// Do not use const_cast.  Do not use std::string or std::vector.

char cell_at(const char* grid, int cols, int row, int col) {
    // TODO
    return '\0';
}

bool cell_is(const char* grid, int cols, int row, int col, const char& target) {
    // TODO
    return false;
}

int count_cells(const char* grid, int rows, int cols, const char& target) {
    // TODO
    return 0;
}

bool grids_equal(const char* a, const char* b, int rows, int cols) {
    // TODO
    return false;
}

bool row_contains(const char* grid, int cols, int row, const char& target) {
    // TODO
    return false;
}

int find_in_row(const char* grid, int cols, int row, const char& target) {
    // TODO
    return -1;
}

const char* row_ptr(const char* grid, int cols, int row) {
    // TODO: return a pointer directly into grid -- not a copy.
    return nullptr;
}

char* row_ptr_mut(char* grid, int cols, int row) {
    // TODO: same arithmetic as row_ptr; only the types differ.
    return nullptr;
}

void set_cell(char* grid, int cols, int row, int col, char val) {
    // TODO
}

void fill_grid(char* grid, int rows, int cols, const char& fill) {
    // TODO
}

void fill_row(char* grid, int cols, int row, const char& fill) {
    // TODO
}

void copy_row(const char* src, int src_cols, int row, char* dst) {
    // TODO
}

void copy_grid(const char* src, char* dst, int rows, int cols) {
    // TODO
}
