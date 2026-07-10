// ListDeque<T> -- a double-ended queue backed by a doubly linked list.
//
// Implement every member below. This is a header-only class template, so
// every member function must be defined here (there is no matching .cpp).
//
// Rules:
//   - Do not use std::vector, std::deque, or std::list anywhere in this
//     file. Build the node/pointer machinery yourself with raw Node
//     pointers and manual new/delete, the same way you did in the
//     linked-list-from-scratch assignment.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not modify the class's public interface (the declarations below).
#pragma once

#include <cstddef>
#include <utility>

// A double-ended queue of T, built from a doubly linked chain of nodes:
// each Node points to both the next node and the previous node, so both
// ends of the list can be reached in O(1) without traversal. ListDeque<T>
// owns every node it creates: the destructor, copy constructor, copy
// assignment, move constructor, and move assignment (the "Big 5") must all
// be implemented correctly, the same delete-order and deep-copy rules from
// linked-list-from-scratch apply here.
template <typename T>
class ListDeque {
private:
    // One link in the chain: a value, plus pointers to the previous and
    // next Node (nullptr at either end of the list).
    struct Node {
        T data;
        Node* prev;
        Node* next;
    };

public:
    // Starts empty: head_ and tail_ both nullptr, size_ 0.
    ListDeque() noexcept;

    // Deletes every node this deque owns.
    ~ListDeque();

    // Deep copy: allocates a brand-new chain of nodes with copies of
    // other's data, front to back. After copying, mutating this deque must
    // never affect other, and vice versa.
    ListDeque(const ListDeque& other);

    // Deep-copy assignment. Must handle self-assignment safely and must
    // not leak this deque's existing nodes.
    ListDeque& operator=(const ListDeque& other);

    // Steals other's head/tail/size directly (no node copies). other is
    // left as a valid, empty deque -- safe to destroy, safe to reuse.
    ListDeque(ListDeque&& other) noexcept;

    // Move assignment. Must handle self-move safely, release this deque's
    // existing nodes before stealing other's, and leave other empty and
    // valid.
    ListDeque& operator=(ListDeque&& other) noexcept;

    // Inserts value as the new last element. O(1) -- use tail_, do not
    // walk the list from head_.
    void push_back(const T& value);

    // Inserts value as the new first element. O(1).
    void push_front(const T& value);

    // Removes the first element. O(1). Returns true on success. If the
    // deque is empty, does nothing and returns false. No exceptions.
    bool pop_front();

    // Removes the last element. O(1) -- use tail_->prev, do not walk the
    // list from head_. Returns true on success. If the deque is empty,
    // does nothing and returns false. No exceptions.
    bool pop_back();

    // Reference to the first element. Only call when !empty().
    T& front();
    const T& front() const;

    // Reference to the last element. Only call when !empty().
    T& back();
    const T& back() const;

    // Returns the number of elements currently stored. Must be O(1) --
    // track a running count, do not walk the list to count nodes.
    std::size_t size() const noexcept;

    // Returns true if the deque has no elements.
    bool empty() const noexcept;

    // Deletes every node and resets the deque to empty (safe to call on an
    // already-empty deque, and safe to keep using the deque afterward).
    void clear();

private:
    Node* head_ = nullptr;
    Node* tail_ = nullptr;
    std::size_t size_ = 0;
};

// ---------------------------------------------------------------------------
// TODO: implement every member declared above.
// ---------------------------------------------------------------------------
