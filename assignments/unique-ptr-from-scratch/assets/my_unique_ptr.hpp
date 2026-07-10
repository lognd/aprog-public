// MyUniquePtr -- a simplified std::unique_ptr you build yourself.
//
// Implement every member below. This is a header-only class template, so
// every member function must be defined here (there is no matching .cpp).
//
// Rules:
//   - Do not use std::unique_ptr, std::shared_ptr, or any other smart
//     pointer type inside this file. The whole point is to build the
//     ownership logic yourself with a raw pointer.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not add a custom deleter template parameter. MyUniquePtr<T> always
//     deletes with a plain `delete`, matching object (not array) ownership.
//   - Do not modify the class's public interface (the declarations below).
#pragma once

#include <cstddef>
#include <utility>

// A simplified, single-object version of std::unique_ptr<T>.
//
// MyUniquePtr<T> owns exactly one heap-allocated T (or owns nothing, if it
// holds nullptr). Ownership can move between MyUniquePtr objects but can
// never be copied -- see the README for why copying a unique owner would
// be a contradiction.
template <typename T>
class MyUniquePtr {
public:
    // Takes ownership of p (may be nullptr). Does not allocate anything
    // itself -- the caller has already called `new`.
    explicit MyUniquePtr(T* p = nullptr) noexcept {
        // TODO: store p.
        (void)p;
    }

    // Deletes the owned pointer, if any.
    ~MyUniquePtr() {
        // TODO
    }

    // Copying a unique owner makes no sense: two MyUniquePtr objects would
    // then both believe they own the same T, and both destructors would
    // eventually call `delete` on it. Deleting these functions makes that
    // a compile error instead of a runtime double-delete.
    MyUniquePtr(const MyUniquePtr&) = delete;
    MyUniquePtr& operator=(const MyUniquePtr&) = delete;

    // Move construction: steal other's pointer and leave other empty.
    // other must be left owning nothing (its internal pointer must become
    // nullptr) so that when other's destructor runs, it deletes nothing.
    MyUniquePtr(MyUniquePtr&& other) noexcept {
        // TODO
        (void)other;
    }

    // Move assignment: release whatever *this currently owns, then steal
    // other's pointer and leave other empty.
    //
    // Contract: must be safe against self-move-assignment, i.e.
    //   p = std::move(p);
    // must not delete the object out from under itself. Check whether
    // `this == &other` before doing anything destructive.
    MyUniquePtr& operator=(MyUniquePtr&& other) noexcept {
        // TODO
        (void)other;
        return *this;
    }

    // Returns the raw pointer without giving up ownership. The returned
    // pointer must not be deleted by the caller -- MyUniquePtr still owns it.
    T* get() const noexcept {
        // TODO
        return nullptr;
    }

    // Gives up ownership and returns the raw pointer. After this call,
    // *this must own nothing (get() == nullptr), and the caller is now
    // responsible for eventually deleting the returned pointer.
    T* release() noexcept {
        // TODO
        return nullptr;
    }

    // Deletes the currently owned pointer (if any), then takes ownership
    // of p (may be nullptr).
    //
    // Contract: must be safe against reset(get()), i.e. resetting a
    // MyUniquePtr to the exact pointer it already owns must not delete the
    // object before re-storing it -- that would leave *this holding a
    // dangling pointer.  Compare against the currently stored pointer
    // before deleting.
    void reset(T* p = nullptr) noexcept {
        // TODO
        (void)p;
    }

    // Exchanges ownership with other. Neither object's owned T is deleted;
    // the two pointers simply swap places.
    void swap(MyUniquePtr& other) noexcept {
        // TODO
        (void)other;
    }

    // Dereferences the owned pointer. Calling this while get() == nullptr
    // is undefined behavior -- the same contract std::unique_ptr uses.
    T& operator*() const {
        // TODO
        static T* dummy = nullptr;
        return *dummy;
    }

    // Member access on the owned pointer. Same undefined-behavior contract
    // as operator*.
    T* operator->() const noexcept {
        // TODO
        return nullptr;
    }

    // true if *this owns a non-null pointer, false otherwise. Lets code
    // write `if (p) { ... }` the same way it would with std::unique_ptr.
    explicit operator bool() const noexcept {
        // TODO
        return false;
    }

private:
    T* ptr_ = nullptr;
};
