# Stack ADT

Implement a Stack data structure using a Python list as the underlying storage.

## Problem Statement

Implement the `Stack` class with the following interface. The stack follows
last-in, first-out (LIFO) ordering.

## Interface

```python
class Stack:
    def push(self, value) -> None:
        """Push value onto the top of the stack."""

    def pop(self):
        """Remove and return the top element. Raise IndexError if empty."""

    def peek(self):
        """Return the top element without removing it. Raise IndexError if empty."""

    def is_empty(self) -> bool:
        """Return True if the stack has no elements."""

    def size(self) -> int:
        """Return the number of elements in the stack."""
```

## Examples

```python
s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.peek())   # 3
print(s.pop())    # 3
print(s.size())   # 2
print(s.is_empty())  # False
```

## Constraints

- `push`, `pop`, `peek`, `size`, and `is_empty` must all run in O(1) time
- Use a Python `list` as the internal storage; do not use `collections.deque`

## Grading

| Component     | Points |
|---------------|--------|
| Visible tests | 30     |
| Hidden tests  | 70     |

## Submission

Submit your implementation as `stack-adt.py`. The class must be named `Stack`.
