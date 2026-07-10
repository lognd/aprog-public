// Text Filters -- implement every member function and function template
// declared in this file.
//
// Part 1 asks you to implement the TextFilter interface and four concrete
// filters using virtual dispatch (runtime polymorphism).
//
// Part 2 asks you to implement three function templates that do the same
// kind of work without any interface at all (compile-time polymorphism).
//
// Rules:
//   - Do not use `new`, `delete`, or `throw` anywhere in this file.
//   - Do not use lambdas.
//   - Do not modify the signatures below.
#pragma once

#include <string>
#include <vector>

namespace tf {

// ---------------------------------------------------------------------------
// Part 1: interface / runtime polymorphism
// ---------------------------------------------------------------------------

// Common interface for all text filters. A filter takes a string and
// returns a new, transformed string -- it never mutates its argument.
class TextFilter {
public:
    virtual ~TextFilter() = default;
    virtual std::string apply(const std::string& s) const = 0;
};

// Converts every alphabetic character in s to uppercase.
class UppercaseFilter : public TextFilter {
public:
    std::string apply(const std::string& s) const override {
        // TODO
        return s;
    }
};

// Removes leading and trailing whitespace from s. Interior whitespace is
// left unchanged.
class TrimFilter : public TextFilter {
public:
    std::string apply(const std::string& s) const override {
        // TODO
        return s;
    }
};

// Replaces every non-overlapping occurrence of a stored word with asterisks
// of the same length. Scans left to right. If the stored word is empty,
// apply() returns s unchanged.
class CensorFilter : public TextFilter {
public:
    explicit CensorFilter(std::string word) : word_(std::move(word)) {}

    std::string apply(const std::string& s) const override {
        // TODO
        return s;
    }

private:
    std::string word_;
};

// Collapses every run of two or more consecutive space characters (' ')
// into a single space. Other whitespace characters (tabs, newlines) are
// left unchanged.
class SqueezeSpacesFilter : public TextFilter {
public:
    std::string apply(const std::string& s) const override {
        // TODO
        return s;
    }
};

// Applies each filter in filters to s, in order, feeding the output of one
// filter into the next. Returns s unchanged if filters is empty. Filters
// are non-owning pointers -- this function neither allocates nor frees them.
inline std::string apply_filters(const std::string& s, const std::vector<const TextFilter*>& filters) {
    // TODO
    return s;
}

// ---------------------------------------------------------------------------
// Part 2: templates / compile-time polymorphism
//
// None of the functions below mention TextFilter. F is any type with a
// method `std::string apply(const std::string&) const` -- the compiler only
// needs the expression f.apply(...) to compile, whether or not F derives
// from TextFilter.
// ---------------------------------------------------------------------------

// Applies f to s twice: f.apply(f.apply(s)).
template <typename F>
std::string apply_twice(const std::string& s, const F& f) {
    // TODO
    return s;
}

// Applies every filter in filters (all of the same type F) to s, in order,
// feeding the output of one into the next. Returns s unchanged if filters
// is empty.
template <typename F>
std::string apply_all(const std::string& s, const std::vector<F>& filters) {
    // TODO
    return s;
}

// Returns true if applying f to s twice produces the same result as
// applying it once: f.apply(f.apply(s)) == f.apply(s).
template <typename F>
bool is_idempotent(const std::string& s, const F& f) {
    // TODO
    return false;
}

} // namespace tf
