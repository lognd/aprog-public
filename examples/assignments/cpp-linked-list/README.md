# C++ Singly Linked List

Implement a singly linked list in C++ using raw pointers. STL containers (`std::vector`, `std::list`, etc.) are not allowed.

---

## Your task

Fill in `linked_list.hpp`. The file must define a class `LinkedList<T>` that satisfies the interface below. Do **not** modify the class name or method signatures  --  the grader compiles `main.cpp` against your header directly.

---

## Interface

```cpp
template <typename T>
class LinkedList {
public:
    LinkedList();                          // default-construct an empty list
    LinkedList(const LinkedList& other);   // deep-copy constructor
    ~LinkedList();                         // free all nodes

    void push_back(const T& value);        // append to tail
    void push_front(const T& value);       // prepend to head
    void pop_front();                      // remove head (no-op on empty list)
    void pop_back();                       // remove tail (no-op on empty list)

    T front() const;                       // return head value (undefined on empty)
    T back() const;                        // return tail value (undefined on empty)

    std::size_t size() const;              // number of elements
    bool empty() const;                    // true iff size() == 0

    void print() const;                    // print each element separated by a space,
                                           // followed by a newline
};
```

---

## Starter file

`assets/linked_list.hpp` contains the class skeleton with `TODO` placeholders. Copy it to your submission and fill in the method bodies.

---

## Example usage

```cpp
LinkedList<int> lst;
lst.push_back(1);
lst.push_back(2);
lst.push_back(3);
lst.print();       // "1 2 3\n"
lst.pop_front();
lst.print();       // "2 3\n"
std::cout << lst.size() << "\n";  // "2"

LinkedList<int> copy = lst;   // deep copy
copy.push_back(99);
lst.print();       // "2 3\n"   (original unchanged)
copy.print();      // "2 3 99\n"
```

---

## Compiling locally

```bash
g++ -std=c++17 -Wall -o test_visible visible-tests/test_visible.cpp
./test_visible
```

The visible test driver prints nothing on success and exits 0. If your implementation is incorrect it will print a failure message and exit 1.

You can also run the Catch2 test suite if you have it installed:

```bash
g++ -std=c++17 -Wall -o catch_tests visible-tests/test_catch.cpp
./catch_tests
```

---

## Constraints

- Do **not** use `std::vector`, `std::list`, `std::deque`, `std::forward_list`, or any other STL container.
- You **may** use `<iostream>`, `<stdexcept>`, `<cstddef>`, `<utility>`, and other non-container standard headers.
- Memory must be managed manually. Every `new` must have a matching `delete`. The grader runs Valgrind.
- The copy constructor must perform a **deep copy**  --  modifying the copy must not affect the original.

---

## Grading

| Section | Points | Visibility |
|---|---|---|
| Source constraint check (no STL) | 0 pts (+ 5 EC) | Visible |
| Compilation | 0 pts | Visible |
| Catch2 visible correctness | 60 pts | Visible |
| Valgrind memory check | 20 pts | Visible |
| Hidden correctness (oracle-generated) | 40 pts | After due date |
| Copy constructor challenge | +5 EC | After due date |

**Total: 120 pts + 10 extra credit**
