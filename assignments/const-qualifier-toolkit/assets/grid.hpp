#pragma once

// 2D character grid utility -- flat row-major storage.
// Element at (row, col) is grid[row * cols + col].
//
// const char* parameters promise the function will not modify the grid.
// char*       parameters mean the function may write to it.
// const char& parameters pass a single character read-only by reference.
//
// Do not modify this file.

// -- Read-only operations ----------------------------------------------------

// Return the character at (row, col).
char        cell_at(const char* grid, int cols, int row, int col);

// Return true if the character at (row, col) equals target.
bool        cell_is(const char* grid, int cols, int row, int col, const char& target);

// Count how many cells in the grid equal target.
int         count_cells(const char* grid, int rows, int cols, const char& target);

// Return true if grids a and b have identical content (same dimensions assumed).
bool        grids_equal(const char* a, const char* b, int rows, int cols);

// Return true if any cell in the given row equals target.
bool        row_contains(const char* grid, int cols, int row, const char& target);

// Return the column index of the first occurrence of target in the given row,
// or -1 if not found.
int         find_in_row(const char* grid, int cols, int row, const char& target);

// -- Pointer-into-grid -------------------------------------------------------
// These return a pointer directly into the grid (not a copy).
// The const-ness of the return must match the const-ness of the input.

const char* row_ptr(const char* grid, int cols, int row);
char*       row_ptr_mut(char* grid, int cols, int row);

// -- Write operations --------------------------------------------------------

// Set the character at (row, col) to val.
void set_cell(char* grid, int cols, int row, int col, char val);

// Fill every cell in the grid with fill.
void fill_grid(char* grid, int rows, int cols, const char& fill);

// Fill every cell in the given row with fill.
void fill_row(char* grid, int cols, int row, const char& fill);

// -- Mixed: const source, mutable destination --------------------------------

// Copy one row from src into dst (dst has the same number of columns).
void copy_row(const char* src, int src_cols, int row, char* dst);

// Copy the entire src grid into dst (same dimensions).
void copy_grid(const char* src, char* dst, int rows, int cols);
