#pragma once
#include <string>
#include <vector>

namespace recur {

// Returns the index of target in the sorted range arr[lo..hi] (inclusive),
// or -1 if not found. Must be implemented recursively.
// Precondition: arr is sorted in ascending order. lo <= hi or lo > hi (empty).
int binary_search(const std::vector<int>& arr, int target, int lo, int hi);

// Sorts arr[lo..hi] (inclusive) in ascending order using merge sort.
// Must be implemented recursively (divide into two halves, sort each, merge).
void merge_sort(std::vector<int>& arr, int lo, int hi);

// Returns the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1, fib(2)=1).
// Must use cache to avoid recomputation: cache[i] holds fib(i) once computed,
// or -1 if not yet computed. Caller initializes cache to all -1s.
long long fibonacci(int n, std::vector<long long>& cache);

// Returns the sum of decimal digits of n (n >= 0).
// Example: digit_sum(493) == 16, digit_sum(0) == 0.
// Must be implemented recursively.
int digit_sum(int n);

// Returns true if s[lo..hi] is a palindrome, false otherwise.
// Must be implemented recursively using the lo and hi indices.
// A single character and an empty range are both palindromes.
bool is_palindrome(const std::string& s, int lo, int hi);

} // namespace recur
