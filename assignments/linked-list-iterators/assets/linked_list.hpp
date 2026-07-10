// LinkedList<T> -- now with a forward iterator you implement yourself.
//
// The Big-5 and the basic push/insert/remove/find/size operations below
// are PROVIDED, complete, and working -- you built this exact class in
// the previous assignment (linked-list-from-scratch), so there is no
// reason to make you write it again. Your job this time is everything
// under "YOUR TASK" near the bottom: the nested Iterator and ConstIterator
// classes, begin()/end()/cbegin()/cend(), and three iterator-based member
// functions (find_it, insert_after, erase_after).
//
// Rules:
//   - Do not use std::vector, std::list, or std::deque anywhere in this
//     file.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not modify the public interface (the declarations already
//     present below) of anything OTHER than filling in the bodies you
//     are asked to write.
#pragma once

#include <cstddef>
#include <utility>

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
    // -----------------------------------------------------------------
    // PROVIDED: Big 5 and basic operations (from linked-list-from-scratch)
    // -----------------------------------------------------------------

    LinkedList() noexcept = default;

    ~LinkedList() {
        clear();
    }

    LinkedList(const LinkedList& other) {
        for (Node* cur = other.head_; cur != nullptr; cur = cur->next) {
            push_back(cur->data);
        }
    }

    LinkedList& operator=(const LinkedList& other) {
        if (this == &other) {
            return *this;
        }
        clear();
        for (Node* cur = other.head_; cur != nullptr; cur = cur->next) {
            push_back(cur->data);
        }
        return *this;
    }

    LinkedList(LinkedList&& other) noexcept
        : head_(other.head_), tail_(other.tail_), size_(other.size_) {
        other.head_ = nullptr;
        other.tail_ = nullptr;
        other.size_ = 0;
    }

    LinkedList& operator=(LinkedList&& other) noexcept {
        if (this == &other) {
            return *this;
        }
        clear();
        head_ = other.head_;
        tail_ = other.tail_;
        size_ = other.size_;
        other.head_ = nullptr;
        other.tail_ = nullptr;
        other.size_ = 0;
        return *this;
    }

    // Inserts value as the new first element. O(1).
    void push_front(const T& value) {
        Node* node = new Node{value, head_};
        head_ = node;
        if (tail_ == nullptr) {
            tail_ = node;
        }
        ++size_;
    }

    // Inserts value as the new last element. O(1) (uses tail_).
    void push_back(const T& value) {
        Node* node = new Node{value, nullptr};
        if (tail_ == nullptr) {
            head_ = node;
            tail_ = node;
        } else {
            tail_->next = node;
            tail_ = node;
        }
        ++size_;
    }

    // Inserts value at position index (0-based). Valid range is
    // [0, size()]. Returns true on success, false (no-op) if out of range.
    bool insert_at(std::size_t index, const T& value) {
        if (index > size_) {
            return false;
        }
        if (index == 0) {
            push_front(value);
            return true;
        }
        if (index == size_) {
            push_back(value);
            return true;
        }
        Node* prev = head_;
        for (std::size_t i = 0; i + 1 < index; ++i) {
            prev = prev->next;
        }
        Node* node = new Node{value, prev->next};
        prev->next = node;
        ++size_;
        return true;
    }

    // Removes the element at position index (0-based). Valid range is
    // [0, size()). Returns true on success, false (no-op) if out of range.
    bool remove_at(std::size_t index) {
        if (index >= size_) {
            return false;
        }
        Node* target;
        if (index == 0) {
            target = head_;
            head_ = head_->next;
            if (head_ == nullptr) {
                tail_ = nullptr;
            }
        } else {
            Node* prev = head_;
            for (std::size_t i = 0; i + 1 < index; ++i) {
                prev = prev->next;
            }
            target = prev->next;
            prev->next = target->next;
            if (target == tail_) {
                tail_ = prev;
            }
        }
        delete target;
        --size_;
        return true;
    }

    // Returns the index of the first element equal to value, or -1 if
    // no such element exists.
    long find(const T& value) const {
        long index = 0;
        for (Node* cur = head_; cur != nullptr; cur = cur->next, ++index) {
            if (cur->data == value) {
                return index;
            }
        }
        return -1;
    }

    std::size_t size() const noexcept {
        return size_;
    }

    bool empty() const noexcept {
        return size_ == 0;
    }

    void clear() {
        Node* cur = head_;
        while (cur != nullptr) {
            Node* next = cur->next;
            delete cur;
            cur = next;
        }
        head_ = nullptr;
        tail_ = nullptr;
        size_ = 0;
    }

    T& front() { return head_->data; }
    const T& front() const { return head_->data; }

    T& back() { return tail_->data; }
    const T& back() const { return tail_->data; }

    // -----------------------------------------------------------------
    // YOUR TASK: forward iterators
    // -----------------------------------------------------------------

    // A movable cursor that wraps a single Node* and walks the chain
    // forward one node at a time. See the README for the full mental
    // model (the "cursor" picture) and the begin()/end() fence-post
    // diagram before you start.
    class Iterator {
    public:
        // Wraps a raw node pointer. A default-constructed Iterator (node
        // == nullptr) must compare equal to end().
        explicit Iterator(Node* node = nullptr);

        // Returns a reference to the element this iterator currently
        // points at. Only call when the iterator does not equal end().
        T& operator*() const;

        // Returns a pointer to the element, so it2->member works.
        T* operator->() const;

        // Prefix: advances this iterator to the next node, THEN returns
        // a reference to *this (the now-advanced iterator).
        Iterator& operator++();

        // Postfix: returns a COPY of this iterator AS IT WAS BEFORE
        // advancing, THEN advances this iterator to the next node. Note
        // the order: postfix must save the old state before mutating.
        Iterator operator++(int);

        bool operator==(const Iterator& other) const;
        bool operator!=(const Iterator& other) const;

        // Exposed so LinkedList's own member functions (insert_after,
        // erase_after, find_it) can reach the underlying node directly.
        Node* node_;
    };

    // A read-only counterpart to Iterator: same cursor behavior, but
    // *it and it->member both yield const access, so code holding a
    // ConstIterator cannot use it to mutate the list.
    class ConstIterator {
    public:
        explicit ConstIterator(const Node* node = nullptr);

        const T& operator*() const;
        const T* operator->() const;

        ConstIterator& operator++();
        ConstIterator operator++(int);

        bool operator==(const ConstIterator& other) const;
        bool operator!=(const ConstIterator& other) const;

        const Node* node_;
    };

    // begin()/end() give the mutable Iterator pair that makes range-for
    // work: for (auto& x : list) { ... } desugars to using these.
    // end() must always represent "one past the last real node" -- a
    // default-constructed Iterator(nullptr) does exactly that, since
    // the last real node's `next` is nullptr.
    Iterator begin();
    Iterator end();

    // cbegin()/cend() give the read-only ConstIterator pair, usable
    // directly and also what a `for (auto& x : list)` loop uses when
    // list is itself const (via the const-qualified begin()/end()
    // overloads below, which forward to these).
    ConstIterator cbegin() const;
    ConstIterator cend() const;
    ConstIterator begin() const;
    ConstIterator end() const;

    // Returns an Iterator to the first element equal to value, or
    // end() if no such element exists.
    Iterator find_it(const T& value);

    // Inserts value immediately after the node pos points at. pos must
    // not be end() (there is nothing to insert "after" the fence post).
    // Returns true on success; if pos == end(), does nothing and
    // returns false.
    bool insert_after(Iterator pos, const T& value);

    // Removes the node immediately after the node pos points at. pos
    // must not be end(), and there must be a node after it. Returns
    // true on success; if pos == end() or pos is the last node
    // (nothing after it), does nothing and returns false.
    bool erase_after(Iterator pos);

private:
    Node* head_ = nullptr;
    Node* tail_ = nullptr;
    std::size_t size_ = 0;
};

// ---------------------------------------------------------------------------
// TODO: implement every Iterator/ConstIterator member, begin()/end(),
// cbegin()/cend(), find_it, insert_after, and erase_after declared above.
// ---------------------------------------------------------------------------
