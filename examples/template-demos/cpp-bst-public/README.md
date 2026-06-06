# Binary Search Tree

Implement a binary search tree (BST) that stores integers.

## Problem Statement

Implement the `BST` class declared in `cpp-bst.hpp`. The BST must support
insert, search, and in-order traversal. You must manage memory manually
(no STL containers for storing nodes).

## Interface

```cpp
class BST {
public:
    BST();
    ~BST();                              // free all nodes

    void insert(int value);              // insert value (ignore duplicates)
    bool search(int value) const;        // return true if value is in tree
    void inorder(std::ostream &out) const; // print space-separated values in sorted order
};
```

## Requirements

- Manage node memory manually with `new` / `delete`; no `std::set` or similar
- `insert` must ignore duplicate values
- `inorder` must print values in ascending order separated by spaces,
  followed by a newline

## Grading

| Component              | Points |
|------------------------|--------|
| Compilation            | 0 (required) |
| Visible tests (Catch2) | 60     |
| Hidden tests (Catch2)  | 45     |
| Memory safety          | 20     |
| Manual I/O cases       | 25     |
| Extra credit (diff)    | +15    |

## Submission

Submit a single file named `cpp-bst.hpp` that implements the declared
interface. Do not rename the file.

## Local Testing

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./cpp-bst_tests
```
