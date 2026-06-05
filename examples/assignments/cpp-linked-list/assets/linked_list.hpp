#pragma once
#include <cstddef>
#include <iostream>

// ---------------------------------------------------------------------------
// Node  --  internal use only; do not expose in your public interface.
// ---------------------------------------------------------------------------
template <typename T>
struct Node {
    T data;
    Node* next = nullptr;
    explicit Node(const T& value) : data(value) {}
};

// ---------------------------------------------------------------------------
// LinkedList<T>
//
// A singly linked list. Implement every method marked TODO.
// Do NOT use std::vector, std::list, std::deque, or any other STL container.
// ---------------------------------------------------------------------------
template <typename T>
class LinkedList {
public:
    // -----------------------------------------------------------------------
    // Construction / destruction
    // -----------------------------------------------------------------------

    // Default constructor: empty list.
    LinkedList() : head_(nullptr), tail_(nullptr), size_(0) {}

    // Deep-copy constructor: copy must not share nodes with `other`.
    LinkedList(const LinkedList& other) : head_(nullptr), tail_(nullptr), size_(0) {
        // TODO: walk other.head_ and push_back each element
    }

    // Destructor: free every node.
    ~LinkedList() {
        // TODO: delete all nodes so Valgrind reports zero leaks
    }

    // -----------------------------------------------------------------------
    // Modifiers
    // -----------------------------------------------------------------------

    void push_back(const T& value) {
        // TODO
    }

    void push_front(const T& value) {
        // TODO
    }

    // Remove the head node. No-op on an empty list.
    void pop_front() {
        // TODO
    }

    // Remove the tail node. No-op on an empty list.
    void pop_back() {
        // TODO
    }

    // -----------------------------------------------------------------------
    // Accessors
    // -----------------------------------------------------------------------

    // Behaviour is undefined when the list is empty.
    T front() const {
        // TODO
        return T{};
    }

    T back() const {
        // TODO
        return T{};
    }

    std::size_t size() const { return size_; }

    bool empty() const { return size_ == 0; }

    // Print all elements separated by spaces, followed by '\n'.
    void print() const {
        // TODO
    }

private:
    Node<T>* head_;
    Node<T>* tail_;
    std::size_t size_;
};
