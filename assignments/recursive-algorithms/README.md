# Recursive Algorithms

## Overview

Recursion lets a function solve a problem by reducing it to a smaller version of
itself. Each call pushes a new frame onto the call stack; when the base case is
reached the frames unwind in reverse order. In this assignment you implement five
classic recursive algorithms and explore how each one decomposes its problem.

## Task

Implement all five functions in a file named `recursive_algorithms.cpp`. The
declarations are in `recursive_algorithms.hpp` inside the `recur` namespace.

### `binary_search`

```cpp
int binary_search(const std::vector<int>& arr, int target, int lo, int hi);
```

Search the sorted range `arr[lo..hi]` (inclusive) for `target`. Return its index
or -1 if not found. The `lo`/`hi` parameters define the recursive sub-range.

### `merge_sort`

```cpp
void merge_sort(std::vector<int>& arr, int lo, int hi);
```

Sort `arr[lo..hi]` in ascending order using merge sort. Divide the range at the
midpoint, sort each half recursively, then merge the two sorted halves back.

### `fibonacci`

```cpp
long long fibonacci(int n, std::vector<long long>& cache);
```

Return the nth Fibonacci number (fib(0)=0, fib(1)=1). The `cache` vector is
pre-sized and initialized to -1. Store computed values in `cache[n]` before
returning so that repeated sub-problems are not recomputed.

### `digit_sum`

```cpp
int digit_sum(int n);
```

Return the sum of the decimal digits of `n` (n >= 0). Example: digit_sum(493)
returns 16 (4+9+3). digit_sum(0) returns 0.

### `is_palindrome`

```cpp
bool is_palindrome(const std::string& s, int lo, int hi);
```

Return true if `s[lo..hi]` reads the same forwards and backwards. Use `lo` and
`hi` as your recursive window. A single character and an empty range are both
palindromes.

## Files

- `recursive_algorithms.hpp` -- declarations; do not modify
- `recursive_algorithms.cpp` -- your implementations (create this file)

## Compilation & Testing

```bash
g++ -std=c++17 -Wall -Wextra -o tests recursive_algorithms.cpp visible-tests/test_visible.cpp
./tests
```

## Constraints

- Each function must use recursion. Iterative implementations will not receive
  credit for that function.
- Do not use STL algorithms (std::sort, std::binary_search, etc.).
- No global variables.

## Grading

| Component | Points |
|---|---|
| binary_search (4 cases) | 20 |
| merge_sort (5 cases) | 25 |
| fibonacci (4 cases) | 20 |
| digit_sum (3 cases) | 15 |
| is_palindrome (4 cases) | 15 |
| Gimme (>= 50% correct) | 5 |
| **Total** | **100** |
