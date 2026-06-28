#pragma once

bool mat_is_symmetric(const int* m, int n);
int  mat_col_sum(const int* m, int rows, int cols, int c);
int  mat_get(const int* m, int cols, int r, int c);
int  mat_row_sum(const int* m, int cols, int r);
void mat_add(const int* a, const int* b, int* dst, int rows, int cols);
void mat_fill(int* m, int rows, int cols, int val);
void mat_print(const int* m, int rows, int cols);
void mat_set(int* m, int cols, int r, int c, int val);
void mat_transpose(const int* src, int* dst, int rows, int cols);
