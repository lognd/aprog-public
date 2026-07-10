// ArrayDeque<T> -- a double-ended queue backed by a circular array buffer.
//
// Implement every member below. This is a header-only class template, so
// every member function must be defined here (there is no matching .cpp).
//
// Rules:
//   - Do not use std::vector, std::deque, or std::list anywhere in this
//     file. Manage a raw dynamically allocated T* array yourself.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not modify the class's public interface (the declarations below).
//   - pop_front() and pop_back() must be O(1). A pop_front() that shifts
//     every remaining element left (the way you might naively implement a
//     "front" on a plain array) does not meet the assignment's requirements
//     even if it produces correct answers -- see the README for why, and
//     how a circular buffer avoids it.
#pragma once

#include <cstddef>
#include <utility>

// A double-ended queue of T, stored in one dynamically allocated array that
// wraps around (a "circular buffer" / "ring buffer"): the logical first
// element does not have to live at index 0. head_ tracks the array index of
// the current front element; the deque occupies size_ consecutive slots
// starting at head_, wrapping around modulo capacity_ when it runs off the
// end of the array. See the README for the ASCII ring diagrams and the
// worked modulo-arithmetic example.
template <typename T>
class ArrayDeque {
public:
    // Starts empty with no allocation: data_ is nullptr, capacity_ 0,
    // head_ 0, size_ 0. The first push allocates an initial array.
    ArrayDeque() noexcept;

    // Deletes the underlying array (delete[]).
    ~ArrayDeque();

    // Deep copy: allocates a brand-new array of other's capacity and
    // copies other's size_ elements into it starting at index 0 (the copy
    // does NOT have to preserve other's head_ position -- re-linearizing
    // during the copy is fine and simpler). After copying, mutating this
    // deque must never affect other, and vice versa.
    ArrayDeque(const ArrayDeque& other);

    // Deep-copy assignment. Must handle self-assignment safely and must
    // not leak this deque's existing array.
    ArrayDeque& operator=(const ArrayDeque& other);

    // Steals other's array pointer and indices directly (no element
    // copies). other is left as a valid, empty deque (data_ nullptr,
    // capacity_ 0, head_ 0, size_ 0) -- safe to destroy, safe to reuse.
    ArrayDeque(ArrayDeque&& other) noexcept;

    // Move assignment. Must handle self-move safely, release this deque's
    // existing array before stealing other's, and leave other empty and
    // valid.
    ArrayDeque& operator=(ArrayDeque&& other) noexcept;

    // Inserts value as the new last element. Amortized O(1): if the array
    // is full, grow (see below) before inserting.
    void push_back(const T& value);

    // Inserts value as the new first element. Amortized O(1): if the array
    // is full, grow before inserting. Must be O(1) per call other than the
    // occasional grow -- do not shift any existing elements.
    void push_front(const T& value);

    // Removes the first element. Must be O(1) -- advance head_ (with
    // wraparound) and decrement size_; do not shift any remaining elements.
    // Returns true on success. If the deque is empty, does nothing and
    // returns false. No exceptions.
    bool pop_front();

    // Removes the last element. Must be O(1) -- decrement size_ only (the
    // slot is considered logically removed even though its old value is
    // still physically present in the array until overwritten). Returns
    // true on success. If the deque is empty, does nothing and returns
    // false. No exceptions.
    bool pop_back();

    // Reference to the first element. Only call when !empty().
    T& front();
    const T& front() const;

    // Reference to the last element. Only call when !empty().
    T& back();
    const T& back() const;

    // Returns the number of elements currently stored. O(1).
    std::size_t size() const noexcept;

    // Returns true if the deque has no elements.
    bool empty() const noexcept;

    // Returns the current allocated capacity (number of slots in the
    // underlying array, not the number of elements stored). Used by the
    // tests to check that capacity only grows when it needs to, and that
    // it grows by doubling.
    std::size_t capacity() const noexcept;

private:
    // Called by push_front/push_back before writing a new element. If
    // size_ == capacity_, allocate a new array of double the capacity (or
    // 8, if capacity_ was 0), copy every existing element into the new
    // array starting at index 0 in front-to-back logical order (this is
    // the "re-linearization" step -- it removes the wraparound, so head_
    // becomes 0 in the new array), free the old array, and update data_,
    // capacity_, and head_. See the README for why growth must
    // re-linearize instead of just delete[]-ing and new[]-ing the same
    // wrapped layout.
    void ensure_capacity();

    T* data_ = nullptr;
    std::size_t capacity_ = 0;
    std::size_t head_ = 0;
    std::size_t size_ = 0;
};

// ---------------------------------------------------------------------------
// TODO: implement every member declared above.
// ---------------------------------------------------------------------------
