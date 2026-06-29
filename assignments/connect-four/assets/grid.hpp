#pragma once

// 2D character grid utility -- flat row-major storage.
// Element at (row, col) is grid[row * cols + col].
// This is the same library from Const Qualifier Toolkit.

char        cell_at(const char* grid, int cols, int row, int col);
bool        cell_is(const char* grid, int cols, int row, int col, const char& target);
int         count_cells(const char* grid, int rows, int cols, const char& target);
bool        grids_equal(const char* a, const char* b, int rows, int cols);
bool        row_contains(const char* grid, int cols, int row, const char& target);
int         find_in_row(const char* grid, int cols, int row, const char& target);
const char* row_ptr(const char* grid, int cols, int row);
char*       row_ptr_mut(char* grid, int cols, int row);
void        set_cell(char* grid, int cols, int row, int col, char val);
void        fill_grid(char* grid, int rows, int cols, const char& fill);
void        fill_row(char* grid, int cols, int row, const char& fill);
void        copy_row(const char* src, int src_cols, int row, char* dst);
void        copy_grid(const char* src, char* dst, int rows, int cols);
