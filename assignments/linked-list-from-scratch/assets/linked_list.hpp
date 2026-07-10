// LinkedList<T> -- a singly linked list you build yourself.
//
// Implement every member below. This is a header-only class template, so
// every member function must be defined here (there is no matching .cpp).
//
// Rules:
//   - Do not use std::vector, std::list, or std::deque anywhere in this
//     file. The whole point is to build the node/pointer machinery
//     yourself.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//     Out-of-range insert_at/remove_at must return false instead of
//     throwing -- see the contract on each function below.
//   - Do not modify the class's public interface (the declarations below).
#pragma once

#include <cstddef>
#include <utility>

// A singly linked list of T, built from raw Node pointers and manual
// new/delete. LinkedList<T> owns every node it creates: the destructor,
// copy constructor, copy assignment, move constructor, and move assignment
// (the "Big 5") must all be implemented correctly, or copying/destroying a
// list will leak memory or double-delete nodes. See the README for the
// node/next-pointer mental model and worked ASCII diagrams.
template <typename T>
class LinkedList {
private:
    // One link in the chain: a value plus a pointer to the next Node (or
    // nullptr if this is the last node).
    struct Node {
        T data;
        Node* next;
    };

public:
    // Starts empty: no nodes, head_ and tail_ both nullptr, size_ 0.
    LinkedList() noexcept;

    // Deletes every node this list owns.
    ~LinkedList();

    // Deep copy: allocates a brand-new chain of nodes with copies of
    // other's data. After copying, mutating this list must never affect
    // other (and vice versa).
    LinkedList(const LinkedList& other);

    // Deep-copy assignment. Must handle self-assignment safely
    // (list = list;) and must not leak this list's existing nodes.
    LinkedList& operator=(const LinkedList& other);

    // Steals other's head/tail/size directly (no node copies). other is
    // left as a valid, empty list (safe to destroy, safe to reuse).
    LinkedList(LinkedList&& other) noexcept;

    // Move assignment. Must handle self-move safely (list = std::move(list);),
    // release this list's existing nodes before stealing other's, and leave
    // other empty and valid.
    LinkedList& operator=(LinkedList&& other) noexcept;

    // Inserts value as the new first element. O(1).
    void push_front(const T& value);

    // Inserts value as the new last element. Must be O(1) -- use tail_,
    // do not walk the list from head_ to find the last node.
    void push_back(const T& value);

    // Inserts value so it becomes the element at position index (0-based).
    // Valid range for index is [0, size()] inclusive -- index == size()
    // means "insert at the end", equivalent to push_back. Returns true on
    // success. If index is out of range (index > size()), does nothing and
    // returns false. No exceptions.
    bool insert_at(std::size_t index, const T& value);

    // Removes the element at position index (0-based). Valid range for
    // index is [0, size()) -- i.e. [0, size() - 1]. Returns true on
    // success. If index is out of range (index >= size(), including on an
    // empty list), does nothing and returns false. No exceptions.
    bool remove_at(std::size_t index);

    // Returns the index of the first element equal to value, or -1 if no
    // such element exists.
    long find(const T& value) const;

    // Returns the number of elements currently stored. Must be O(1) --
    // track a running count, do not walk the list to count nodes.
    std::size_t size() const noexcept;

    // Returns true if the list has no elements.
    bool empty() const noexcept;

    // Deletes every node and resets the list to empty (safe to call on an
    // already-empty list, and safe to keep using the list afterward).
    void clear();

    // Reference to the first element. Only call when !empty().
    T& front();
    const T& front() const;

    // Reference to the last element. Only call when !empty().
    T& back();
    const T& back() const;

private:
    Node* head_ = nullptr;
    Node* tail_ = nullptr;
    std::size_t size_ = 0;
};

// ---------------------------------------------------------------------------
// TODO: implement every member declared above.
// ---------------------------------------------------------------------------
