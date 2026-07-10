// Stack<T, D> and Queue<T, D> -- container adapters over a deque backend.
//
// Implement every member below by delegating to the deque_ member. This
// mirrors how std::stack and std::queue are themselves implemented: they
// are not independent data structures, they are thin wrappers that pick a
// subset of an underlying container's operations and rename them (push_back
// becomes push, pop_front becomes pop, and so on).
//
// Rules:
//   - Every member must delegate to deque_. Do not add any other storage,
//     and do not reimplement push/pop logic from scratch here.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not modify the class's public interface (the declarations below).
#pragma once

#include <cstddef>

#include "array_deque.hpp"

// A LIFO (last-in, first-out) adapter over a deque backend D (ArrayDeque<T>
// by default -- see the README for why the deque type is a template
// parameter with a default, instead of a fixed choice). push/pop/top all
// operate on the back of the underlying deque.
template <typename T, typename D = ArrayDeque<T>>
class Stack {
public:
    // Pushes value onto the top of the stack. Delegates to deque_.push_back.
    void push(const T& value);

    // Removes the top element. Returns true on success, false and no-op if
    // the stack is empty. Delegates to deque_.pop_back.
    bool pop();

    // Reference to the top element. Only call when !empty(). Delegates to
    // deque_.back.
    T& top();
    const T& top() const;

    // Returns the number of elements currently stored.
    std::size_t size() const noexcept;

    // Returns true if the stack has no elements.
    bool empty() const noexcept;

private:
    D deque_;
};

// A FIFO (first-in, first-out) adapter over a deque backend D (ArrayDeque<T>
// by default). push adds to the back; pop/front remove/inspect the front.
template <typename T, typename D = ArrayDeque<T>>
class Queue {
public:
    // Pushes value onto the back of the queue. Delegates to
    // deque_.push_back.
    void push(const T& value);

    // Removes the front element. Returns true on success, false and no-op
    // if the queue is empty. Delegates to deque_.pop_front.
    bool pop();

    // Reference to the front element (the next one pop() will remove).
    // Only call when !empty(). Delegates to deque_.front.
    T& front();
    const T& front() const;

    // Reference to the back element (the most recently pushed). Only call
    // when !empty(). Delegates to deque_.back.
    T& back();
    const T& back() const;

    // Returns the number of elements currently stored.
    std::size_t size() const noexcept;

    // Returns true if the queue has no elements.
    bool empty() const noexcept;

private:
    D deque_;
};

// ---------------------------------------------------------------------------
// TODO: implement every member declared above.
// ---------------------------------------------------------------------------
