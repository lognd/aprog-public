# Binary Search

Implement binary search on a sorted list of integers.

## Problem Statement

Implement the function `binary_search(arr, target)` that searches for
`target` in the sorted list `arr`. Return the index of `target` if found,
or `-1` if it is not present. You must use the binary search algorithm
(O(log n) time complexity).

## Function Signatures

```python
def binary_search(arr: list[int], target: int) -> int:
    """Return the index of target in arr, or -1 if not found."""
    ...
```

## Examples

### Example 1

```python
>>> binary_search([1, 3, 5, 7, 9], 5)
2
>>> binary_search([1, 3, 5, 7, 9], 4)
-1
>>> binary_search([], 1)
-1
```

## Constraints

- `arr` is sorted in ascending order with no duplicates
- `0 <= len(arr) <= 10^6`
- Values fit in a standard Python `int`

## Grading

| Component   | Points |
|-------------|--------|
| Correctness | 100    |

## Submission

Submit a single file named `binary-search.py` that defines `binary_search`.
Do not rename the function.
